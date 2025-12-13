"""Command runtime for session-bound command execution."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..core.errors import (
    CancelledError,
    CompileError,
    MaterializeError,
    PlanError,
    PulkaCoreError,
)
from ..core.viewer import viewer_public_state
from .parser import CommandDispatcher, CommandDispatchResult
from .registry import REGISTRY, CommandContext

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from ..api.session import Session
    from ..core.viewer import Viewer
    from ..logging import Recorder


@dataclass(frozen=True, slots=True)
class CommandRuntimeRenderIntent:
    """Describe how the caller should render after a command."""

    should_render: bool
    force_render: bool


@dataclass(frozen=True, slots=True)
class CommandRuntimeResult:
    """Structured command result returned by the session runtime."""

    dispatch: CommandDispatchResult | None
    render: CommandRuntimeRenderIntent
    message: str | None = None


class SessionCommandRuntime:
    """Execute commands for a :class:`~pulka.api.session.Session`."""

    def __init__(self, session: Session):
        self._session = session
        self._dispatcher = CommandDispatcher(session.commands)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def prepare_viewer(self, viewer: Viewer | None = None) -> Viewer:
        """Ensure ``viewer`` is instrumented for recorder callbacks."""

        target = viewer or self._require_active_viewer()
        self._ensure_perf_callback(target)
        return target

    def invoke(
        self,
        name: str,
        *,
        args: Sequence[str] | None = None,
        repeat: int = 1,
        source: str,
        viewer: Viewer | None = None,
        context_mutator: Callable[[CommandContext], None] | None = None,
        propagate: tuple[type[BaseException], ...] | None = None,
    ) -> CommandRuntimeResult:
        """Invoke ``name`` directly with parsed arguments."""

        arg_list = list(args or [])
        repeat_count = max(1, repeat)
        raw = name

        def _executor(context: CommandContext) -> CommandDispatchResult:
            return self._dispatcher.invoke(
                name,
                context,
                args=arg_list,
                repeat=repeat_count,
            )

        return self._execute(
            _executor,
            source=source,
            raw=raw,
            name_hint=name,
            viewer=viewer,
            context_mutator=context_mutator,
            propagate=propagate,
        )

    def dispatch_raw(
        self,
        text: str,
        *,
        source: str,
        viewer: Viewer | None = None,
        context_mutator: Callable[[CommandContext], None] | None = None,
        propagate: tuple[type[BaseException], ...] | None = None,
    ) -> CommandRuntimeResult:
        """Parse and dispatch ``text`` via the command dispatcher."""

        raw = text.strip()
        name_hint = self._name_hint_from_raw(raw)

        def _executor(context: CommandContext) -> CommandDispatchResult | None:
            return self._dispatcher.dispatch(raw, context)

        return self._execute(
            _executor,
            source=source,
            raw=raw,
            name_hint=name_hint,
            viewer=viewer,
            context_mutator=context_mutator,
            propagate=propagate,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _execute(
        self,
        executor: Callable[[CommandContext], CommandDispatchResult | None],
        *,
        source: str,
        raw: str,
        name_hint: str,
        viewer: Viewer | None,
        context_mutator: Callable[[CommandContext], None] | None,
        propagate: tuple[type[BaseException], ...] | None,
    ) -> CommandRuntimeResult:
        active_viewer = viewer or self._require_active_viewer()
        recorder = getattr(self._session, "recorder", None)
        recorder = recorder if recorder and recorder.enabled else None
        if recorder:
            recorder.ensure_env_recorded()
        self._ensure_perf_callback(active_viewer)
        context = self._build_context(active_viewer, context_mutator)

        payload: dict[str, object] | None = None
        if recorder:
            payload = self._make_payload(active_viewer, source=source, raw=raw, name=name_hint)

        dispatch: CommandDispatchResult | None = None
        message: str | None = None

        try:
            with self._bind_registry():
                if recorder and payload is not None:
                    with recorder.perf_timer(f"command.{name_hint}", payload=payload):
                        dispatch = executor(context)
                else:
                    dispatch = executor(context)
        except PulkaCoreError as exc:
            if propagate and isinstance(exc, propagate):
                raise
            category: str
            if isinstance(exc, PlanError):
                category = "plan"
            elif isinstance(exc, CompileError):
                category = "compile"
            elif isinstance(exc, MaterializeError):
                category = "materialize"
            elif isinstance(exc, CancelledError):
                category = "cancelled"
            else:
                category = "core"
            detail = str(exc).strip()
            message = f"{category} error: {detail}" if detail else f"{category} error"
            if recorder:
                recorder.record(
                    "error",
                    {
                        "source": source,
                        "raw": raw,
                        "message": detail or message,
                        "kind": "command",
                        "error_type": exc.__class__.__name__,
                        "category": category,
                    },
                )
        except ValueError as exc:
            if propagate and isinstance(exc, propagate):
                raise
            message = f"command error: {exc}"
            if recorder:
                recorder.record(
                    "error",
                    {
                        "source": source,
                        "raw": raw,
                        "message": str(exc),
                        "kind": "command",
                        "error_type": exc.__class__.__name__,
                    },
                )
        except Exception as exc:  # pragma: no cover - safety net
            if propagate and isinstance(exc, propagate):
                raise
            message = f"error: {exc}"
            if recorder:
                recorder.record(
                    "error",
                    {
                        "source": source,
                        "raw": raw,
                        "message": str(exc),
                        "kind": "command",
                        "error_type": exc.__class__.__name__,
                    },
                )
        finally:
            current = getattr(self._session, "viewer", None)
            if current is not None:
                self._ensure_perf_callback(current)

        if recorder and payload is not None:
            target_viewer = context.viewer
            state_after = viewer_public_state(target_viewer)
            if state_after is not None:
                payload.update(
                    {
                        "after_row": state_after.cursor.row,
                        "after_col": state_after.cursor.col,
                        "after_col0": state_after.viewport.col0,
                        "visible_cols_after": state_after.visible_column_count
                        or len(state_after.columns),
                    }
                )
            if dispatch is not None:
                payload.update(
                    {
                        "command": dispatch.spec.name,
                        "args": list(dispatch.args),
                        "repeat": dispatch.repeat,
                    }
                )

        if recorder and dispatch is not None:
            recorder.record(
                "command",
                {
                    "source": source,
                    "raw": raw,
                    "name": dispatch.spec.name,
                    "args": list(dispatch.args),
                    "repeat": dispatch.repeat,
                },
            )

        render_intent = self._build_render_intent(dispatch)
        return CommandRuntimeResult(dispatch=dispatch, render=render_intent, message=message)

    def _build_context(
        self,
        viewer: Viewer,
        context_mutator: Callable[[CommandContext], None] | None,
    ) -> CommandContext:
        recorder: Recorder | None = getattr(self._session, "recorder", None)
        context = CommandContext(
            viewer.sheet,
            viewer,
            session=self._session,
            view_stack=self._session.view_stack,
            recorder=recorder,
        )
        if context_mutator is not None:
            context_mutator(context)
        return context

    def _ensure_perf_callback(self, viewer: Viewer) -> None:
        if not hasattr(viewer, "set_perf_callback"):
            return
        recorder = getattr(self._session, "recorder", None)
        if recorder and recorder.enabled:
            viewer.set_perf_callback(
                lambda phase, duration_ms, payload: recorder.record_perf(
                    phase=phase,
                    duration_ms=duration_ms,
                    payload=payload,
                )
            )
        else:
            viewer.set_perf_callback(None)

    def _visible_column_count(self, viewer: Viewer) -> int:
        state = viewer_public_state(viewer)
        if state is None:  # pragma: no cover - defensive
            return 0
        return state.visible_column_count or len(state.columns)

    def _make_payload(
        self,
        viewer: Viewer,
        *,
        source: str,
        raw: str,
        name: str,
    ) -> dict[str, object]:
        state = viewer_public_state(viewer)
        if state is None:  # pragma: no cover - defensive
            msg = "Viewer snapshot unavailable"
            raise RuntimeError(msg)

        return {
            "context": source,
            "raw": raw,
            "command": name,
            "before_row": state.cursor.row,
            "before_col": state.cursor.col,
            "before_col0": state.viewport.col0,
            "visible_cols_before": state.visible_column_count or len(state.columns),
        }

    def _build_render_intent(
        self, dispatch: CommandDispatchResult | None
    ) -> CommandRuntimeRenderIntent:
        if dispatch is None:
            return CommandRuntimeRenderIntent(should_render=False, force_render=False)
        hints = dispatch.spec.ui_hints or {}
        mapping = hints if isinstance(hints, dict) else dict(hints)
        force_render = bool(mapping.get("force_render"))
        return CommandRuntimeRenderIntent(should_render=True, force_render=force_render)

    def _require_active_viewer(self) -> Viewer:
        viewer = getattr(self._session, "viewer", None)
        if viewer is None:
            msg = "Session has no active viewer"
            raise RuntimeError(msg)
        return viewer

    @contextmanager
    def _bind_registry(self):
        thread_local = getattr(REGISTRY, "_thread_local", None)
        previous = getattr(thread_local, "registry", None) if thread_local is not None else None
        REGISTRY.bind(self._session.commands)
        try:
            yield
        finally:
            if previous is None:
                REGISTRY.bind(None)
            else:
                REGISTRY.bind(previous)

    @staticmethod
    def _name_hint_from_raw(raw: str) -> str:
        if not raw:
            return "noop"
        stripped = raw.strip()
        if not stripped:
            return "noop"
        for delimiter in (" ", "\t", ":"):
            if delimiter in stripped:
                return stripped.split(delimiter, 1)[0]
        return stripped


__all__ = [
    "CommandRuntimeRenderIntent",
    "CommandRuntimeResult",
    "SessionCommandRuntime",
]

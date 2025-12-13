"""Headless runner for Pulka.

This module provides functionality for running Pulka in script mode without TUI,
processing commands and returning output programmatically.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

from ..command.runtime import CommandRuntimeRenderIntent, CommandRuntimeResult
from ..core.errors import (
    CancelledError,
    CompileError,
    MaterializeError,
    PlanError,
    PulkaCoreError,
)
from ..logging import frame_hash, viewer_state_snapshot
from ..render.status_bar import render_status_line_text

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ..api.session import Session
    from ..core.viewer import Viewer


def load_script_file(path: str) -> list[str]:
    """Load commands from a script file."""
    commands: list[str] = []
    with Path(path).open(encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            commands.append(stripped)
    return commands


def _blank_runtime_result(message: str | None = None) -> CommandRuntimeResult:
    return CommandRuntimeResult(
        dispatch=None,
        render=CommandRuntimeRenderIntent(should_render=False, force_render=False),
        message=message,
    )


def _format_core_error(error: PulkaCoreError) -> tuple[str, str, str]:
    """Return ``(category, message, detail)`` for ``error``."""

    if isinstance(error, PlanError):
        category = "plan"
    elif isinstance(error, CompileError):
        category = "compile"
    elif isinstance(error, MaterializeError):
        category = "materialize"
    elif isinstance(error, CancelledError):
        category = "cancelled"
    else:
        category = "core"

    detail = str(error).strip()
    message = f"{category} error: {detail}" if detail else f"{category} error"
    return category, message, detail


def apply_script_command(session: Session, raw: str) -> tuple[bool, CommandRuntimeResult]:
    """Dispatch ``raw`` using the session command runtime."""

    text = raw.strip()
    if not text or text.startswith("#"):
        return True, _blank_runtime_result()

    lowered = text.lower()
    if lowered in {"q", "quit", "exit"}:
        return False, _blank_runtime_result()

    if lowered == "help":
        commands = session.commands.list_commands()
        command_list = ", ".join(sorted(name for name, _ in commands))
        message = (
            f"Available commands: {command_list}" if command_list else "No commands registered"
        )
        return True, _blank_runtime_result(message=message)

    result = session.command_runtime.dispatch_raw(text, source="headless")
    return True, result


def run_script_mode(
    session: Session,
    commands: Iterable[str],
    *,
    auto_render: bool = True,
) -> list[str]:
    """Execute ``commands`` against ``session``'s active viewer."""

    def _current_viewer() -> Viewer:
        viewer = getattr(session, "viewer", None)
        if viewer is None:  # pragma: no cover - defensive guard
            raise RuntimeError("run_script_mode requires an active viewer")
        session.command_runtime.prepare_viewer(viewer)
        return viewer

    recorder = getattr(session, "recorder", None)
    active_recorder = recorder if recorder and recorder.enabled else None
    outputs: list[str] = []

    viewer = _current_viewer()
    viewer.update_terminal_metrics()
    viewer.clamp()

    if active_recorder:
        active_recorder.ensure_env_recorded()

    def _render_table(current: Viewer, trigger: str, *, command: str | None = None) -> str:
        from ..render.table import render_table

        if active_recorder:
            payload = {"context": "headless", "trigger": trigger}
            if command:
                payload["command"] = command
            with active_recorder.perf_timer("render.table", payload=payload):
                return render_table(current, include_status=True)
        return render_table(current, include_status=True)

    def _render_status(current: Viewer, trigger: str, *, command: str | None = None) -> str:
        if active_recorder:
            payload = {"context": "headless", "trigger": trigger}
            if command:
                payload["command"] = command
            with active_recorder.perf_timer("render.status", payload=payload):
                status = render_status_line_text(current)
                current.acknowledge_status_rendered()
                return status
        status = render_status_line_text(current)
        current.acknowledge_status_rendered()
        return status

    if auto_render:
        viewer = _current_viewer()
        frame_text = _render_table(viewer, "initial")
        outputs.append(frame_text)
        if active_recorder:
            state_snapshot = viewer_state_snapshot(viewer)
            status_text = _render_status(viewer, "initial")
            active_recorder.record_state(state_snapshot)
            if status_text:
                active_recorder.record_status(status_text)
            active_recorder.record_frame(
                frame_text=frame_text,
                frame_hash=frame_hash(frame_text),
            )

    for raw in commands:
        try:
            cont, runtime_result = apply_script_command(session, raw)
            message = runtime_result.message
            if message:
                outputs.append(message)

            intent = runtime_result.render
            dispatch = runtime_result.dispatch
            canonical = dispatch.spec.name if dispatch is not None else raw

            if intent.should_render and (auto_render or intent.force_render):
                viewer = _current_viewer()
                viewer.update_terminal_metrics()
                viewer.clamp()
                frame_text = _render_table(viewer, "command", command=canonical)
                outputs.append(frame_text)
                if active_recorder:
                    state_snapshot = viewer_state_snapshot(viewer)
                    status_text = _render_status(viewer, "command", command=canonical)
                    active_recorder.record_state(state_snapshot)
                    if status_text:
                        active_recorder.record_status(status_text)
                    active_recorder.record_frame(
                        frame_text=frame_text,
                        frame_hash=frame_hash(frame_text),
                    )

            if not cont:
                break
        except PulkaCoreError as exc:
            category, message, detail = _format_core_error(exc)
            if active_recorder:
                active_recorder.record(
                    "error",
                    {
                        "command": raw,
                        "message": detail or message,
                        "kind": category,
                        "error_type": exc.__class__.__name__,
                    },
                )
            outputs.append(message)
            break
        except Exception as exc:  # pragma: no cover - defensive guard
            if active_recorder:
                active_recorder.record("error", {"command": raw, "message": str(exc)})
            outputs.append(f"error: {exc}")
            break

    return outputs

"""Shared view stack management for Pulka viewers."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from contextlib import suppress

from .ui_hooks import NullViewerUIHooks, ViewerUIHooks
from .viewer import Viewer

ActiveViewerCallback = Callable[[Viewer], None]


class ViewStack:
    """Manage the stack of active :class:`Viewer` instances."""

    def __init__(self, *, ui_hooks: ViewerUIHooks | None = None) -> None:
        self._viewers: list[Viewer] = []
        self._ui_hooks: ViewerUIHooks = ui_hooks or NullViewerUIHooks()
        self._listeners: list[ActiveViewerCallback] = []

    # ------------------------------------------------------------------
    # Introspection helpers
    @property
    def viewers(self) -> tuple[Viewer, ...]:
        """Return a snapshot of the current viewer stack."""

        return tuple(self._viewers)

    @property
    def active(self) -> Viewer | None:
        """Return the active viewer or ``None`` when the stack is empty."""

        if not self._viewers:
            return None
        return self._viewers[-1]

    @property
    def parent(self) -> Viewer | None:
        """Return the viewer below the active viewer when available."""

        if len(self._viewers) < 2:
            return None
        return self._viewers[-2]

    def __len__(self) -> int:  # pragma: no cover - tiny utility
        return len(self._viewers)

    # ------------------------------------------------------------------
    # UI hook management
    @property
    def ui_hooks(self) -> ViewerUIHooks:
        """Expose the UI hook bridge applied to viewers in the stack."""

        return self._ui_hooks

    def set_ui_hooks(self, hooks: ViewerUIHooks | None) -> None:
        """Swap the UI hook bridge for every viewer in the stack."""

        self._ui_hooks = hooks or NullViewerUIHooks()
        for idx, viewer in enumerate(self._viewers):
            viewer.stack_depth = idx
            viewer.set_ui_hooks(self._ui_hooks)

    # ------------------------------------------------------------------
    # Stack mutation helpers
    def reset(self, root_viewer: Viewer) -> Viewer:
        """Replace the entire stack with ``root_viewer``."""

        self._viewers.clear()
        return self.push(root_viewer)

    def push(self, viewer: Viewer) -> Viewer:
        """Push ``viewer`` onto the stack and mark it active."""

        viewer.stack_depth = len(self._viewers)
        viewer.set_ui_hooks(self._ui_hooks)
        self._viewers.append(viewer)
        self._emit_active_changed(viewer)
        return viewer

    def extend(self, viewers: Iterable[Viewer]) -> None:
        """Push multiple viewers onto the stack in order."""

        for viewer in viewers:
            self.push(viewer)

    def pop(self) -> Viewer | None:
        """Pop the active viewer if a parent remains."""

        if len(self._viewers) <= 1:
            return None
        removed = self._viewers.pop()
        active = self._viewers[-1]
        active.stack_depth = len(self._viewers) - 1
        active.set_ui_hooks(self._ui_hooks)
        self._emit_active_changed(active)
        return removed

    # ------------------------------------------------------------------
    # Listener wiring
    def add_active_viewer_listener(self, callback: ActiveViewerCallback) -> Callable[[], None]:
        """Subscribe to active viewer changes.

        Returns a callable that removes ``callback`` when invoked.
        """

        self._listeners.append(callback)
        active = self.active
        if active is not None:
            callback(active)

        def _unsubscribe() -> None:
            with suppress(ValueError):
                self._listeners.remove(callback)

        return _unsubscribe

    # ------------------------------------------------------------------
    # Internal helpers
    def _emit_active_changed(self, viewer: Viewer) -> None:
        for listener in tuple(self._listeners):
            try:
                listener(viewer)
            except Exception:  # pragma: no cover - defensive
                continue

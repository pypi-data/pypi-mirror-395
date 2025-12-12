"""prompt_toolkit-backed implementation of :class:`ViewerUIHooks`."""

from __future__ import annotations

from collections.abc import Callable

from prompt_toolkit import Application
from prompt_toolkit.eventloop import call_soon_threadsafe

from ..core.viewer.ui_hooks import NullViewerUIHooks, ViewerUIHooks


class PromptToolkitViewerUIHooks(ViewerUIHooks):
    """Expose prompt_toolkit services through the viewer hook protocol."""

    __slots__ = ("_app",)

    def __init__(self, app: Application) -> None:
        self._app = app

    def get_terminal_size(self, fallback: tuple[int, int]) -> tuple[int, int]:
        try:
            size = self._app.output.get_size()
            return size.columns, size.rows
        except Exception:
            return NullViewerUIHooks().get_terminal_size(fallback)

    def invalidate(self) -> None:
        self._app.invalidate()

    def call_soon(self, callback: Callable[[], None]) -> None:
        try:
            call_soon_threadsafe(callback)
        except Exception:
            callback()


__all__ = ["PromptToolkitViewerUIHooks"]

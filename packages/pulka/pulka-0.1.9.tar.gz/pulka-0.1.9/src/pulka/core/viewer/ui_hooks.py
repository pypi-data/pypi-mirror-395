"""UI integration hooks for :class:`~pulka.core.viewer.viewer.Viewer`.

This module documents the thin boundary between the core viewer state machine
and any interactive UI runtime.  The viewer must remain portable across
prompt_toolkit, headless rendering, and scripted environments, so direct UI
framework calls are routed through the :class:`ViewerUIHooks` protocol.  The
protocol can be implemented by rich clients (for example prompt_toolkit) while
tests and headless callers can continue to rely on the ``NullViewerUIHooks``
implementation.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class ViewerUIHooks(Protocol):
    """Bridge between the viewer core and a concrete UI runtime.

    Implementations provide three small services:

    ``get_terminal_size``
        Returns the terminal width/height pair using a UI specific measurement
        API.  The ``fallback`` argument should be used when the real metrics
        are unavailable.

    ``invalidate``
        Request a redraw of the UI.  Rich clients typically forward this to
        their event loop, while headless implementations can treat it as a
        no-op.

    ``call_soon``
        Schedule ``callback`` to run in the UI thread.  This mirrors
        ``prompt_toolkit.eventloop.call_soon_threadsafe`` but keeps the viewer
        decoupled from prompt_toolkit itself.
    """

    def get_terminal_size(self, fallback: tuple[int, int]) -> tuple[int, int]:
        """Return ``(columns, rows)`` for the active terminal."""

    def invalidate(self) -> None:
        """Request a refresh of the UI surface hosting the viewer."""

    def call_soon(self, callback: Callable[[], None]) -> None:
        """Schedule ``callback`` to run on the UI thread as soon as possible."""


class NullViewerUIHooks:
    """Default hooks for headless or test environments.

    The implementation relies on :func:`shutil.get_terminal_size` for terminal
    metrics, treats ``invalidate`` as a no-op, and executes callbacks
    synchronously.  This keeps viewer behaviour predictable in environments
    without an event loop.
    """

    __slots__ = ()

    def get_terminal_size(self, fallback: tuple[int, int]) -> tuple[int, int]:
        size = shutil.get_terminal_size(fallback)
        return size.columns, size.lines

    def invalidate(self) -> None:
        return None

    def call_soon(self, callback: Callable[[], None]) -> None:
        callback()

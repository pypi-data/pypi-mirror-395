"""Terminal sizing and status helpers for the viewer."""

from __future__ import annotations

from typing import Any, Protocol


class TerminalConfigurable(Protocol):
    _viewport_rows_override: int | None
    _status_width_override_chars: int | None
    _view_width_override_chars: int | None
    view_width_chars: int
    status_width_chars: int
    view_height: int
    _visible_key: Any
    _status_dirty: bool

    def update_terminal_metrics(self) -> None: ...

    def invalidate_row_cache(self) -> None: ...


def set_status_width_override(target: TerminalConfigurable, width: int | None) -> None:
    """Force a specific status bar width independently of the table view."""

    if width is None:
        target._status_width_override_chars = None
        return
    target._status_width_override_chars = max(20, int(width))


def set_view_width_override(target: TerminalConfigurable, width: int | None) -> None:
    """Force a specific character width for test or headless rendering."""

    if width is None:
        target._view_width_override_chars = None
        return
    target._view_width_override_chars = max(20, int(width))


def mark_status_dirty(target: TerminalConfigurable) -> None:
    """Signal that the status bar should be re-rendered."""

    target._status_dirty = True


def acknowledge_status_rendered(target: TerminalConfigurable) -> None:
    """Mark the status bar as in sync with the latest render."""

    target._status_dirty = False


def is_status_dirty(target: TerminalConfigurable) -> bool:
    """Return whether the status bar needs to be re-rendered."""

    return target._status_dirty


def configure_terminal(
    target: TerminalConfigurable,
    *,
    width: int,
    height: int | None = None,
) -> None:
    """Configure explicit terminal metrics for deterministic renders."""

    clamped_width = max(20, int(width))
    if height is not None:
        target._viewport_rows_override = max(1, int(height))
    set_status_width_override(target, clamped_width)
    set_view_width_override(target, clamped_width)
    target.update_terminal_metrics()
    target.view_width_chars = clamped_width
    target.status_width_chars = clamped_width
    if height is not None:
        target.view_height = max(1, int(height))
    target._visible_key = None
    acknowledge_status_rendered(target)


__all__ = [
    "TerminalConfigurable",
    "acknowledge_status_rendered",
    "configure_terminal",
    "is_status_dirty",
    "mark_status_dirty",
    "set_status_width_override",
    "set_view_width_override",
]

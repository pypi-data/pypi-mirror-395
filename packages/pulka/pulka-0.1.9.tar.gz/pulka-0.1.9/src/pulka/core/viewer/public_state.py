# mypy: ignore-errors

"""Helpers for interacting with :func:`Viewer.snapshot`."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from .viewer import ViewerCursor, ViewerPublicState, ViewerViewport


def viewer_public_state(viewer: Any) -> ViewerPublicState | None:
    """Return a :class:`ViewerPublicState` for ``viewer`` when available."""

    snapshot_getter: Callable[[], ViewerPublicState] | None = getattr(viewer, "snapshot", None)
    if not callable(snapshot_getter):
        return _coerce_legacy_viewer_state(viewer)
    try:
        state = snapshot_getter()
    except Exception:  # pragma: no cover - defensive
        return _coerce_legacy_viewer_state(viewer)
    if isinstance(state, ViewerPublicState):
        return state
    return _coerce_legacy_viewer_state(viewer)


def _coerce_legacy_viewer_state(viewer: Any) -> ViewerPublicState | None:
    """Build a best-effort :class:`ViewerPublicState` for legacy viewers."""

    columns = _coerce_str_tuple(getattr(viewer, "columns", ()))
    visible_columns = _coerce_str_tuple(_maybe_call(getattr(viewer, "visible_cols", ())))
    hidden_from_attr = _coerce_str_tuple(_maybe_call(getattr(viewer, "hidden_columns", ())))
    hidden_from_private = _coerce_str_tuple(getattr(viewer, "_hidden_cols", ()))

    if not visible_columns:
        hidden_lookup = set(hidden_from_attr or hidden_from_private)
        if hidden_lookup:
            visible_columns = tuple(col for col in columns if col not in hidden_lookup)
        elif columns:
            visible_columns = columns

    hidden_columns = tuple(col for col in columns if col not in set(visible_columns))
    if not hidden_columns:
        hidden_columns = hidden_from_attr or hidden_from_private

    frozen_columns = _coerce_str_tuple(_maybe_call(getattr(viewer, "frozen_columns", ())))

    cursor_row = _coerce_int(getattr(viewer, "cur_row", 0))
    cursor_col = _coerce_int(getattr(viewer, "cur_col", 0))
    row0 = _coerce_int(getattr(viewer, "row0", 0))
    col0 = _coerce_int(getattr(viewer, "col0", 0))

    view_height = _coerce_int(getattr(viewer, "view_height", None))
    if view_height == 0:
        view_height = _coerce_int(getattr(viewer, "viewport_rows", None))
    visible_row_count = max(0, view_height)

    visible_column_count = len(visible_columns) if visible_columns else len(columns)
    total_columns = len(columns)

    viewport = ViewerViewport(
        row0=row0,
        rowN=row0 + max(0, visible_row_count - 1),
        col0=col0,
        colN=col0 + max(0, visible_column_count - 1),
        rows=visible_row_count,
        cols=visible_column_count,
    )

    highlighted_column: str | None = None
    if columns and 0 <= cursor_col < len(columns):
        highlighted_column = columns[cursor_col]

    width_state = _coerce_width_state(viewer)

    total_rows = _coerce_optional_int(getattr(viewer, "_total_rows", None))
    sort_column = _coerce_optional_str(getattr(viewer, "sort_col", None))
    filter_text = _coerce_optional_str(getattr(viewer, "filter_text", None))
    filter_kind = _coerce_optional_str(getattr(viewer, "filter_kind", None))
    search_text = _coerce_optional_str(getattr(viewer, "search_text", None))
    frequency_source_column = _coerce_optional_str(getattr(viewer, "freq_source_col", None))

    try:
        all_columns_maximized = bool(getattr(viewer, "all_columns_maximized", False))
    except Exception:  # pragma: no cover - defensive
        all_columns_maximized = False

    return ViewerPublicState(
        cursor=ViewerCursor(row=cursor_row, col=cursor_col),
        viewport=viewport,
        columns=columns,
        visible_columns=visible_columns,
        hidden_columns=hidden_columns,
        frozen_columns=frozen_columns,
        total_rows=total_rows,
        visible_row_count=visible_row_count,
        total_columns=total_columns,
        visible_column_count=visible_column_count,
        hidden_column_count=len(hidden_columns),
        status_message=_coerce_optional_str(getattr(viewer, "status_message", None)),
        highlighted_column=highlighted_column,
        width_mode=width_state["mode"],
        width_target=width_state["target"],
        all_columns_maximized=all_columns_maximized,
        sort_column=sort_column,
        sort_ascending=bool(getattr(viewer, "sort_asc", True)),
        filter_text=filter_text,
        filter_kind=filter_kind,
        search_text=search_text,
        frequency_mode=bool(getattr(viewer, "is_freq_view", False)),
        frequency_source_column=frequency_source_column,
    )


def _coerce_width_state(viewer: Any) -> dict[str, int | None | str]:
    state: dict[str, int | None | str] = {"mode": "default", "target": None}
    raw_state = _maybe_call(getattr(viewer, "width_mode_state", None))
    if isinstance(raw_state, dict):
        mode = raw_state.get("mode")
        if isinstance(mode, str) and mode in {"default", "single", "all"}:
            state["mode"] = mode
        target = raw_state.get("target")
        if isinstance(target, int):
            state["target"] = target

    mode_attr = getattr(viewer, "_width_mode", None)
    if isinstance(mode_attr, str) and mode_attr in {"default", "single", "all"}:
        state["mode"] = mode_attr

    target_attr = _maybe_call(getattr(viewer, "maximized_column_index", None))
    if not isinstance(target_attr, int):
        target_attr = getattr(viewer, "_width_target", None)
    if isinstance(target_attr, int):
        state["target"] = target_attr

    return state


def _coerce_str_tuple(value: Any) -> tuple[str, ...]:
    value = _maybe_call(value)
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        result: list[str] = []
        for item in value:
            if item is None:
                continue
            result.append(str(item))
        return tuple(result)
    return ()


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):  # pragma: no cover - defensive
        return default


def _coerce_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):  # pragma: no cover - defensive
        return None


def _coerce_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def _maybe_call(value: Any) -> Any:
    if callable(value):
        try:
            return value()
        except TypeError:  # pragma: no cover - defensive
            return value
    return value


__all__ = ["viewer_public_state"]

# mypy: ignore-errors

"""
Status bar rendering for Pulka.

This module provides functions for rendering the status bar that displays
metadata about the current view including filename, row position, column info,
filters, sort, and memory usage.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any

from ..utils import lazy_imports

if TYPE_CHECKING:
    StyleAndTextTuples = list[tuple[str, str]]  # type: ignore[assignment]
else:  # pragma: no cover - runtime import helper
    StyleAndTextTuples = lazy_imports.prompt_toolkit_style_and_text_tuples()

from ..core.formatting import (
    _format_large_number_compact,
    _format_number_with_thousands_separator,
    _simplify_dtype_text,
)
from ..testing import is_test_mode
from .style_resolver import get_active_style_resolver
from .styles import apply_style

# Constants for formatting and truncation
_LARGE_NUMBER_THRESHOLD = 999999  # Threshold for compact number formatting
_MEMORY_THRESHOLD = 1000000  # Threshold for memory usage interpretation


def sample_memory_usage(*, test_mode: bool) -> int | None:
    """Return current memory usage in MB with the same semantics as the status bar."""

    if test_mode:
        return 120

    try:
        import resource
    except Exception:  # pragma: no cover - resource module unavailable
        return None

    try:
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:  # pragma: no cover - getrusage failures are best-effort
        return None

    if usage > _MEMORY_THRESHOLD:
        return max(1, int(usage / 1024 / 1024))
    return max(1, int(usage / 1024))


def _truncate_middle(text: str, max_length: int) -> str:
    """Return ``text`` truncated around the middle to fit ``max_length``."""

    if max_length <= 0:
        return ""
    if len(text) <= max_length:
        return text

    ellipsis = "…"
    if max_length <= len(ellipsis):
        return ellipsis[:max_length]

    slice_length = max_length - len(ellipsis)
    front = (slice_length + 1) // 2
    back = slice_length // 2
    return f"{text[:front]}{ellipsis}{text[-back:] if back else ''}"


def render_status_line(
    v: Any,
    *,
    test_mode: bool | None = None,
    resource_sample: int | None = None,
) -> StyleAndTextTuples:
    """Render a ``prompt_toolkit`` fragment representing the status bar."""

    if test_mode is None:
        test_mode = is_test_mode()

    if not hasattr(v, "columns") or not hasattr(v, "cur_col"):
        raise TypeError(
            f"Expected Viewer-like object with columns and cur_col attributes, got {type(v)}"
        )

    sheet = getattr(v, "sheet", None)
    columns = list(getattr(v, "columns", []) or [])
    if columns:
        cur_index = min(max(int(getattr(v, "cur_col", 0)), 0), len(columns) - 1)
        current_col = str(columns[cur_index])
        sheet_schema = getattr(sheet, "schema", {}) if sheet is not None else {}
        schema = getattr(v, "schema", None) or sheet_schema
        col_dtype = schema.get(columns[cur_index], "unknown")
    else:
        current_col = "no columns"
        col_dtype = "N/A"

    total_rows = getattr(v, "_total_rows", None)
    row_count_stale = bool(getattr(v, "_row_count_stale", False))
    was_pending = row_count_stale or total_rows is None
    if row_count_stale or total_rows is None:
        ensure_total_rows = getattr(v, "_ensure_total_rows", None)
        if callable(ensure_total_rows):
            total_rows = ensure_total_rows()
        elif hasattr(v, "sheet") and hasattr(v.sheet, "__len__"):
            with contextlib.suppress(Exception):
                total_rows = len(v.sheet)

    current_row_formatted = _format_number_with_thousands_separator(
        int(getattr(v, "cur_row", 0)) + 1
    )
    pending_row_count = getattr(v, "_row_count_future", None)
    display_pending = bool(getattr(v, "_row_count_display_pending", False))
    if total_rows is not None:
        sheet_id = getattr(getattr(v, "sheet", None), "sheet_id", None)
        if not (display_pending or (was_pending and sheet_id is not None)):
            if total_rows > _LARGE_NUMBER_THRESHOLD:
                rows_total_text = _format_large_number_compact(total_rows)
            else:
                rows_total_text = _format_number_with_thousands_separator(total_rows)
        else:
            rows_total_text = "≈"
    else:
        rows_total_text = "≈" if (pending_row_count is not None or was_pending) else "?"

    if resource_sample is None:
        mem_mb = sample_memory_usage(test_mode=test_mode)
    else:
        mem_mb = resource_sample

    is_file_browser = bool(getattr(sheet, "is_file_browser", False))
    browser_path: str | None = None
    if is_file_browser:
        browser_path = getattr(sheet, "display_path", None)
        if not browser_path:
            directory = getattr(sheet, "directory", None)
            if directory is not None:
                browser_path = str(directory)
        if not browser_path:
            fallback = getattr(sheet, "sheet_id", None) or getattr(v, "_source_path", None)
            if fallback is not None:
                browser_path = str(fallback)

    simple_dtype = _simplify_dtype_text(col_dtype)
    if browser_path:
        left_parts = [browser_path]
    else:
        left_parts = [f"row {current_row_formatted} / col {current_col}[{simple_dtype}]"]

    filter_text = getattr(v, "filter_text", None)
    if filter_text:
        left_parts.append(f"F: {filter_text}")

    status_message = getattr(v, "status_message", None)
    if status_message:
        normalised_status = status_message.strip().lower()
        duplicate = False
        sort_status = False
        if normalised_status.startswith("sort"):
            has_error = "error" in normalised_status
            unsupported = "not supported" in normalised_status
            if not has_error and not unsupported:
                sort_status = True
        if filter_text:
            preview = filter_text if len(filter_text) <= 60 else f"{filter_text[:57]}..."
            filter_candidates = {
                filter_text.strip().lower(),
                preview.strip().lower(),
                f"filter: {filter_text.strip().lower()}",
                f"filter: {preview.strip().lower()}",
            }
            duplicate = normalised_status in filter_candidates
        if not duplicate and not sort_status:
            left_parts.append(status_message)

    left_text = " • ".join(left_parts)

    total_columns = len(columns)
    hidden_column_count = 0
    hidden_columns = getattr(v, "hidden_columns", None)
    if hidden_columns:
        hidden_column_count = len(tuple(hidden_columns))
    else:
        hidden_names = getattr(v, "_hidden_cols", None)
        if hidden_names and columns:
            hidden_set = set(hidden_names)
            hidden_column_count = sum(1 for name in columns if name in hidden_set)

    non_hidden_columns = total_columns - hidden_column_count
    if non_hidden_columns <= 0:
        visible_columns = list(getattr(v, "visible_cols", []) or [])
        visible_count = len(visible_columns)
        non_hidden_columns = visible_count or total_columns or visible_count

    right_parts = [f"depth {getattr(v, 'stack_depth', 0)}"]
    right_parts.append(f"{rows_total_text}×{max(0, non_hidden_columns)}")
    if mem_mb is not None:
        right_parts.append(f"mem {mem_mb}MB")
    right_text = " • ".join(right_parts)

    width_hint = getattr(v, "status_width_chars", None)
    if width_hint is None:
        width_hint = getattr(v, "view_width_chars", 80)
    width = max(20, int(width_hint or 0))
    right_text = _truncate_middle(right_text, width)
    available_left = max(0, width - len(right_text))
    if right_text and available_left > 0:
        available_left -= 1
    left_text = _truncate_middle(left_text, available_left) if available_left > 0 else ""

    if right_text:
        gap = max(1, width - len(left_text) - len(right_text))
        status = f"{left_text}{' ' * gap}{right_text}" if left_text else right_text.rjust(width)
    else:
        status = left_text

    status = status[:width]
    padded = status.ljust(width)
    if test_mode:
        style = ""
    else:
        resolver = get_active_style_resolver()
        style = resolver.prompt_toolkit_style_for_classes(("status",))
    return [(style, padded)]


def render_status_line_text(v: Any, *, test_mode: bool | None = None) -> str:
    """Return an ANSI string fallback for tests and non-PTK paths."""

    fragments = render_status_line(v, test_mode=test_mode)
    text = "".join(part for _, part in fragments)
    if not text:
        return text

    test_mode_flag = is_test_mode() if test_mode is None else test_mode
    resolver = get_active_style_resolver()
    components = resolver.resolve(("status",))
    style_str = components.to_prompt_toolkit() or None
    return apply_style(text, style_str, test_mode=test_mode_flag)

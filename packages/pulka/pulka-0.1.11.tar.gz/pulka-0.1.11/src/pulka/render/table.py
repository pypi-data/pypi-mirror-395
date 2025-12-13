"""Table rendering helpers shared across the TUI and headless paths."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..testing import is_test_mode
from .display import display_width, truncate_grapheme_safe
from .styles import segments_to_text
from .viewport_plan import Cell, ColumnPlan, ViewportPlan, compute_viewport_plan

if TYPE_CHECKING:  # pragma: no cover - typing helper
    from ..core.viewer import Viewer


@dataclass(frozen=True)
class Segment:
    """A chunk of text tagged with prompt_toolkit style classes."""

    text: str
    classes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RenderedLine:
    """Represents a single rendered line and optional cursor location."""

    segments: tuple[Segment, ...]
    plain_text: str
    cursor_x: int | None = None


def _style_classes_for_gap(
    *, is_header: bool, row_active: bool, row_selected: bool
) -> tuple[str, ...]:
    classes = ["table", "table.header" if is_header else "table.cell"]
    if row_selected and not is_header:
        classes.append("table.row.selected")
    if row_active and not is_header:
        classes.append("table.row.active")
        if row_selected:
            classes.append("table.row.selected.active")
    return tuple(classes)


def _style_classes_for_cell(cell: Cell, *, is_header: bool) -> tuple[str, ...]:
    classes = ["table"]
    if is_header:
        classes.append("table.header")
    else:
        classes.append("table.cell")
    row_selected = bool(getattr(cell, "selected_row", False))
    if row_selected and not is_header:
        classes.append("table.row.selected")
    if cell.active_row and not is_header:
        classes.append("table.row.active")
        if row_selected:
            classes.append("table.row.selected.active")
    if cell.active_col:
        classes.append("table.col.active")
    if cell.active_cell and not is_header:
        classes.append("table.cell.active")
    if not is_header and cell.is_null:
        classes.append("table.cell.null")
    return tuple(classes)


def _style_classes_for_border(*, row_active: bool, row_selected: bool) -> tuple[str, ...]:
    # Keep the frozen-column separator aligned with the header separator colour
    # while still letting the active-row background flow underneath. Combining
    # the separator style with the row-active class applies the highlight
    # without changing the foreground colour, so the border no longer flickers
    # yet the highlight remains uninterrupted across the boundary.
    classes: list[str] = []
    if row_selected:
        classes.append("table.row.selected")
    if row_active:
        classes.append("table.row.active")
        if row_selected:
            classes.append("table.row.selected.active")
    # Apply separator last so its foreground colour is not overridden by row states.
    classes.append("table.separator")
    if row_active:
        classes.append("table.separator.active")
    return tuple(classes)


def _truncate(text: str, width: int, use_ellipsis: bool) -> str:
    if width <= 0:
        return ""
    if not use_ellipsis or width <= 1:
        return truncate_grapheme_safe(text, width)
    slice_width = max(0, width - 1)
    base = truncate_grapheme_safe(text, slice_width)
    return f"{base}…"


def _format_cell_text(
    cell: Cell,
    width: int,
    use_ellipsis: bool,
    *,
    is_header: bool,
    truncated: bool = False,
) -> tuple[str, int]:
    if width <= 0:
        return "", 0

    text = cell.text
    is_numeric = bool(getattr(cell, "numeric", False))
    effective_ellipsis = use_ellipsis and not is_numeric
    display_len = display_width(text)

    if display_len > width:
        text = _truncate(text, width, effective_ellipsis)
        display_len = display_width(text)
    elif truncated and effective_ellipsis and width > 0:
        text = _truncate(text, width, True)
        display_len = display_width(text)

    if display_len < width:
        padding = " " * (width - display_len)
        text = f"{padding}{text}" if not is_header and cell.numeric else f"{text}{padding}"
        display_len = width

    return text, display_len


def _append_segment(
    segments: list[Segment],
    plain_parts: list[str],
    classes: Iterable[str],
    text: str,
) -> None:
    if not text:
        return
    segment = Segment(text=text, classes=tuple(classes))
    segments.append(segment)
    plain_parts.append(text)


def _segments_to_chars(segments: Sequence[Segment]) -> list[tuple[str, tuple[str, ...]]]:
    chars: list[tuple[str, tuple[str, ...]]] = []
    for segment in segments:
        if not segment.text:
            continue
        for ch in segment.text:
            chars.append((ch, segment.classes))
    return chars


def _chars_to_segments(chars: Sequence[tuple[str, tuple[str, ...]]]) -> list[Segment]:
    if not chars:
        return []
    segments: list[Segment] = []
    text_parts: list[str] = []
    current_classes = chars[0][1]
    for ch, classes in chars:
        if classes == current_classes:
            text_parts.append(ch)
            continue
        segments.append(Segment(text="".join(text_parts), classes=current_classes))
        text_parts = [ch]
        current_classes = classes
    if text_parts:
        segments.append(Segment(text="".join(text_parts), classes=current_classes))
    return segments


def apply_overflow_indicators(
    line: RenderedLine,
    *,
    show_left: bool,
    show_right: bool,
    is_header: bool,
) -> RenderedLine:
    """Decorate ``line`` with overflow arrows while preserving width."""

    if not show_left and not show_right:
        return line

    base_classes = ["table", "table.header" if is_header else "table.cell"]
    indicator_classes = (
        "table",
        "table.header" if is_header else "table.cell",
        "table.overflow_indicator",
    )
    gutter_classes = tuple(base_classes)
    chars = _segments_to_chars(line.segments)
    if not chars:
        return line

    if show_left:
        chars[0] = ("<", indicator_classes)
    if show_right:
        last_idx = len(chars) - 1
        gutter_idx = last_idx - 1
        chars[last_idx] = (">", indicator_classes)
        if gutter_idx >= 0:
            chars[gutter_idx] = (" ", gutter_classes)

    segments = _chars_to_segments(chars)
    plain_text = "".join(ch for ch, _ in chars)
    return RenderedLine(tuple(segments), plain_text, line.cursor_x)


def build_row_line(
    cells: Sequence[Cell],
    column_widths: Sequence[int],
    frozen_boundary: int | None,
    column_overflows: Sequence[bool],
    *,
    is_header: bool,
    row_active: bool | None = None,
    row_selected: bool | None = None,
    include_boundary: bool = True,
    column_plans: Sequence[ColumnPlan] | None = None,
) -> RenderedLine:
    """Render a row (header or body) into styled segments."""

    segments: list[Segment] = []
    plain_parts: list[str] = []
    cursor_x: int | None = None
    plain_length = 0

    if row_active is None:
        row_active = any(cell.active_row for cell in cells)
    if row_selected is None:
        row_selected = any(getattr(cell, "selected_row", False) for cell in cells)

    gap_classes = _style_classes_for_gap(
        is_header=is_header, row_active=row_active, row_selected=row_selected
    )
    border_classes = _style_classes_for_border(row_active=row_active, row_selected=row_selected)

    def append(classes: Iterable[str], text: str, segment_width: int) -> None:
        nonlocal plain_length, cursor_x
        if not text:
            return
        _append_segment(segments, plain_parts, classes, text)
        plain_length += max(segment_width, 0)

    marker = "•" if row_selected and not is_header else " "
    append(gap_classes, marker, 1)
    for idx, column_width in enumerate(column_widths):
        cell = cells[idx] if idx < len(cells) else None
        boundary_matches = frozen_boundary is not None and idx == frozen_boundary
        is_boundary = include_boundary and boundary_matches
        content_width = max(0, column_width - (1 if is_boundary else 0))

        if cell is None:
            cell_text = " " * content_width
            cell_width = content_width
            active_cell = False
            cell_classes: tuple[str, ...] = gap_classes
        else:
            truncated = getattr(cell, "truncated", False)
            use_ellipsis = column_overflows[idx] if idx < len(column_overflows) else False
            if truncated:
                use_ellipsis = True
            cell_text, cell_width = _format_cell_text(
                cell,
                content_width,
                use_ellipsis,
                is_header=is_header,
                truncated=truncated,
            )
            classes_list = list(_style_classes_for_cell(cell, is_header=is_header))
            is_sorted = False
            header_active = False
            if is_header and column_plans is not None and idx < len(column_plans):
                column_plan = column_plans[idx]
                is_sorted = column_plan.is_sorted
                header_active = column_plan.header_active
            if header_active:
                classes_list.append("table.header.active")
            cell_classes = tuple(classes_list)
            active_cell = bool(cell.active_cell and not is_header)

        if cell is not None and active_cell and cursor_x is None:
            cursor_x = plain_length

        if is_header and cell is not None and is_sorted and cell_text:
            indicator = cell_text[0]
            indicator_width = display_width(indicator)
            remainder = cell_text[1:]
            remainder_width = max(0, cell_width - indicator_width)

            indicator_classes: tuple[str, ...] = ("table", "table.header", "table.header.sorted")
            append(indicator_classes, indicator, indicator_width)
            if remainder_width > 0:
                append(cell_classes, remainder, remainder_width)
        else:
            append(cell_classes, cell_text, cell_width)

        if is_boundary:
            append(border_classes, "│", 1)
            append(gap_classes, " ", 1)
        elif idx < len(column_widths) - 1:
            append(gap_classes, " ", 1)

    append(gap_classes, " ", 1)

    plain_text = "".join(plain_parts)
    return RenderedLine(tuple(segments), plain_text, cursor_x)


def build_blank_line(
    column_widths: Sequence[int],
    frozen_boundary: int | None,
    column_overflows: Sequence[bool],
    *,
    header: bool,
    column_plans: Sequence[ColumnPlan] | None = None,
    row_active: bool = False,
    include_boundary: bool = True,
) -> RenderedLine:
    return build_row_line(
        [],
        column_widths,
        frozen_boundary,
        column_overflows,
        is_header=header,
        row_active=row_active,
        include_boundary=include_boundary,
        column_plans=column_plans,
    )


def determine_blank_line_highlights(plan: ViewportPlan) -> tuple[bool, bool]:
    """Return whether the padding rows should inherit the active-row style."""

    has_active_row = any(cell.active_row for row in plan.cells for cell in row)
    if has_active_row:
        return False, False

    active_row = getattr(plan, "active_row_index", None)
    if active_row is None:
        return False, False

    start = plan.row_offset
    end = plan.row_offset + plan.rows

    if active_row < start:
        return True, False
    if active_row >= end:
        return False, True
    return False, False


def build_separator_line(
    column_widths: Sequence[int],
    *,
    frozen_boundary: int | None = None,
) -> RenderedLine:
    segments: list[Segment] = []
    plain_parts: list[str] = []
    gap_classes = ("table", "table.separator")
    _append_segment(segments, plain_parts, gap_classes, " ")

    separator_parts: list[str] = []
    boundary_idx: int | None = (
        frozen_boundary
        if frozen_boundary is not None and 0 <= frozen_boundary < len(column_widths)
        else None
    )
    for idx, width in enumerate(column_widths):
        run_width = max(0, width)
        if run_width:
            segment = "─" * run_width
            if boundary_idx is not None and idx == boundary_idx:
                segment = f"{segment[:-1]}┼" if run_width > 0 else "┼"
            separator_parts.append(segment)
        if idx < len(column_widths) - 1:
            separator_parts.append("─")
    separator = "".join(separator_parts)
    _append_segment(segments, plain_parts, ("table.separator",), separator)
    _append_segment(segments, plain_parts, gap_classes, " ")

    plain_text = "".join(plain_parts)
    return RenderedLine(tuple(segments), plain_text)


def compute_column_overflows(columns: Sequence[ColumnPlan], has_rows: bool) -> list[bool]:
    overflows: list[bool] = []
    for column in columns:
        header_text = getattr(column, "header_label", column.name)
        needs_ellipsis = False
        if has_rows:
            needs_ellipsis = column.has_nulls or column.is_numeric
        min_header_width = display_width(header_text)
        if column.width < column.original_width or column.width < min_header_width:
            needs_ellipsis = True
        overflows.append(needs_ellipsis)
    return overflows


def render_plan_lines(plan: ViewportPlan, height: int) -> list[RenderedLine]:
    """Render the viewport plan into styled lines."""

    column_widths = [max(1, column.width) for column in plan.columns] or [1]
    frozen_boundary = plan.frozen_boundary_idx
    column_overflows = compute_column_overflows(plan.columns, plan.rows > 0)
    highlight_top_blank, highlight_bottom_blank = determine_blank_line_highlights(plan)

    lines: list[RenderedLine] = []
    table_height = max(0, height - 1)
    has_header = bool(plan.cells and plan.cells[0] and plan.cells[0][0].role == "header")
    body_rows = plan.cells[1:] if has_header else plan.cells

    if table_height > 0:
        lines.append(
            build_blank_line(
                column_widths,
                frozen_boundary,
                column_overflows,
                header=has_header,
                column_plans=plan.columns,
                row_active=highlight_top_blank,
                include_boundary=False,
            )
        )

    if has_header:
        header_cells = plan.cells[0]
        header_line = build_row_line(
            header_cells,
            column_widths,
            frozen_boundary,
            column_overflows,
            is_header=True,
            column_plans=plan.columns,
        )
        header_line = apply_overflow_indicators(
            header_line,
            show_left=plan.has_left_overflow,
            show_right=plan.has_right_overflow,
            is_header=True,
        )
        lines.append(header_line)
        if body_rows:
            lines.append(build_separator_line(column_widths, frozen_boundary=frozen_boundary))

    for row in body_rows:
        lines.append(
            build_row_line(
                row,
                column_widths,
                frozen_boundary,
                column_overflows,
                is_header=False,
            )
        )

    if height > 0:
        lines.append(
            build_blank_line(
                column_widths,
                frozen_boundary,
                column_overflows,
                header=False,
                column_plans=plan.columns,
                row_active=highlight_bottom_blank,
                include_boundary=False,
            )
        )

    return lines


def render_table(
    v: Viewer,
    *,
    include_status: bool = False,
    test_mode: bool | None = None,
) -> str:
    """Render the current viewer state as a formatted table string."""

    if test_mode is None:
        test_mode = is_test_mode()

    view_width = getattr(v, "view_width_chars", 80)
    view_height = getattr(v, "view_height", 20)
    plan = compute_viewport_plan(v, view_width, view_height)

    lines = render_plan_lines(plan, view_height)
    table_lines = [
        segments_to_text(
            [(segment.classes, segment.text) for segment in line.segments],
            test_mode=test_mode,
        )
        for line in lines
    ]
    table_str = "\n".join(table_lines)
    if table_lines:
        table_str += "\n"

    if include_status:
        from .status_bar import render_status_line_text

        status_line = render_status_line_text(v, test_mode=test_mode)
        v.acknowledge_status_rendered()
        if table_str.endswith("\n"):
            table_str = table_str.rstrip("\n")
        return f"{table_str}\n{status_line}\n"

    return table_str

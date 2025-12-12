"""Viewport planning for tabular renders.

This module computes a UI-neutral representation of the visible portion of a
table so renderers (Rich, prompt_toolkit, headless) can share sizing and cell
formatting logic without duplicating width calculations.
"""

from __future__ import annotations

import contextlib
import math
from collections.abc import Hashable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from ..core.engine.contracts import TableSlice
from ..core.formatting import _is_numeric_dtype
from .decimal_alignment import apply_decimal_alignment, compute_decimal_alignment
from .display import (
    display_width,
    pad_left_display,
    pad_right_display,
    truncate_grapheme_safe,
)

if TYPE_CHECKING:
    from ..core.viewer import Viewer


@dataclass(slots=True)
class Cell:
    """Rendered cell payload for a viewport column/row intersection."""

    text: str
    role: Literal["header", "body"]
    active_row: bool
    active_col: bool
    active_cell: bool
    selected_row: bool
    numeric: bool
    is_null: bool


@dataclass(slots=True)
class _ColumnMeta:
    """Internal helper metadata for planning column layout."""

    name: str
    dtype: Any
    is_numeric: bool
    has_nulls: bool
    min_width: int
    original_width: int
    header_active: bool
    is_sorted: bool
    is_frozen: bool


@dataclass(slots=True)
class ColumnPlan:
    """Metadata for a visible column within the viewport."""

    name: str
    header_label: str
    width: int
    min_width: int
    original_width: int
    is_numeric: bool
    has_nulls: bool
    header_active: bool
    is_sorted: bool


@dataclass(slots=True)
class ViewportPlan:
    """Collection of visible cells and sizing metadata for a table viewport."""

    columns: list[ColumnPlan]
    frozen_boundary_idx: int | None
    rows: int
    row_offset: int
    col_offset: int
    cells: list[list[Cell]]
    active_row_index: int


def fetch_visible_for_viewer(viewer: Viewer) -> TableSlice:
    """Return the visible slice for ``viewer`` honouring column visibility."""

    if hasattr(viewer, "visible_cols") and viewer.visible_cols:
        cols = list(viewer.visible_cols)
    else:
        cols = list(viewer.columns)
    return viewer.get_visible_table_slice(cols)


def _sort_directions(viewer: Viewer) -> dict[str, bool]:
    """Return a mapping of column name to descending flag."""

    sort_map: dict[str, bool] = {}
    current_plan = None
    with contextlib.suppress(Exception):
        current_plan = viewer._current_plan()

    sort_entries = getattr(current_plan, "sort", None)
    if sort_entries:
        for entry in sort_entries:
            try:
                column, desc = entry
            except Exception:
                continue
            sort_map[str(column)] = bool(desc)
        return sort_map

    sort_col = getattr(viewer, "sort_col", None)
    if sort_col is not None:
        sort_map[str(sort_col)] = not bool(getattr(viewer, "sort_asc", True))
    return sort_map


def _header_label_for_column(column_name: str, sort_map: dict[str, bool]) -> str:
    """Return the header label prefixed with the sort indicator."""

    indicator = " "
    desc = sort_map.get(column_name)
    if desc is not None:
        indicator = "↓" if desc else "↑"
    return f"{indicator}{column_name}"


def _table_border_overhead(column_count: int) -> int:
    """Return the width contribution of table borders and separators."""

    if column_count <= 0:
        return 0
    return column_count + 1


def _shrink_widths_to_fit(
    widths: list[int],
    minimums: list[int],
    target_total: int,
) -> list[int]:
    """Reduce widths while respecting per-column minimums."""

    if not widths or target_total <= 0:
        return widths

    total = sum(widths)
    if total <= target_total:
        return widths

    overflow = total - target_total
    while overflow > 0:
        slack = [(idx, w - minimums[idx]) for idx, w in enumerate(widths)]
        slack = [item for item in slack if item[1] > 0]
        if not slack:
            break

        share = max(1, overflow // len(slack))
        for idx, available in slack:
            delta = min(available, share, overflow)
            if delta <= 0:
                continue
            widths[idx] -= delta
            overflow -= delta
            if overflow <= 0:
                break

    return widths


def _allocate_widths(
    widths: list[int],
    caps: list[int],
    weights: list[int],
    remaining: int,
) -> int:
    """Grow ``widths`` toward ``caps`` using ``weights`` while columns remain."""

    if remaining <= 0:
        return 0

    size = len(widths)
    while remaining > 0:
        eligible = [idx for idx in range(size) if widths[idx] < caps[idx]]
        if not eligible:
            break

        total_weight = sum(max(0, weights[idx]) for idx in eligible)
        if total_weight <= 0:
            total_weight = len(eligible)
            weight_map = dict.fromkeys(eligible, 1)
        else:
            weight_map = {idx: max(0, weights[idx]) for idx in eligible}

        allocated = 0
        for idx in eligible:
            cap = caps[idx]
            if widths[idx] >= cap:
                continue
            weight = weight_map[idx] or 0
            if weight <= 0:
                continue
            share = int(remaining * weight / total_weight)
            gap = cap - widths[idx]
            if share <= 0:
                share = 1
            share = min(gap, share)
            if share <= 0:
                continue
            widths[idx] += share
            remaining -= share
            allocated += share
            if remaining <= 0:
                break

        if allocated == 0:
            # Fallback: allocate single columns in priority order to avoid stalls.
            eligible.sort(key=lambda idx: (-(weight_map[idx] or 0), idx))
            for idx in eligible:
                if remaining <= 0:
                    break
                if widths[idx] >= caps[idx]:
                    continue
                widths[idx] += 1
                remaining -= 1
            if remaining > 0 and not any(widths[idx] < caps[idx] for idx in eligible):
                break

    return remaining


def compute_viewport_plan(viewer: Viewer, width: int, height: int) -> ViewportPlan:
    """Compute a viewport plan for ``viewer`` constrained to ``width``×``height``."""

    sheet = getattr(viewer, "sheet", None)
    if sheet is not None and hasattr(sheet, "update_layout_for_view"):
        try:
            sheet.update_layout_for_view(
                view_width=width,
                view_height=height,
                viewer=viewer,
            )
        except TypeError:
            sheet.update_layout_for_view(width)

    table_slice = fetch_visible_for_viewer(viewer)
    cols = list(table_slice.column_names)
    sort_map = _sort_directions(viewer)
    header_labels = [_header_label_for_column(name, sort_map) for name in cols]
    header_label_widths = [display_width(label) for label in header_labels]

    frozen_cols = getattr(viewer, "frozen_columns", []) if hasattr(viewer, "frozen_columns") else []
    frozen_name_set = set(frozen_cols)
    frozen_boundary_idx: int | None = None
    if frozen_cols:
        boundary_name = frozen_cols[-1]
        if boundary_name in cols:
            frozen_boundary_idx = cols.index(boundary_name)

    header_widths = getattr(viewer, "_header_widths", [])
    autosized = getattr(viewer, "_autosized_widths", None)
    sticky_widths = getattr(viewer, "_sticky_column_widths", {})
    if not isinstance(sticky_widths, dict):
        sticky_widths = {}
    col_widths: list[int] = []
    seed_widths: list[int] = []
    original_widths: list[int] = []
    for idx, col_name in enumerate(cols):
        header_label_width = header_label_widths[idx] if idx < len(header_label_widths) else 0
        try:
            col_idx = viewer.columns.index(col_name)
        except ValueError:
            base_width = max(4, header_label_width)
        else:
            base_width = (
                header_widths[col_idx]
                if col_idx < len(header_widths)
                else max(4, header_label_width)
            )
            if autosized:
                base_width = autosized.get(col_idx, base_width)
        base_width = max(base_width, header_label_width)
        original_widths.append(base_width)
        sticky = sticky_widths.get(col_name)
        seed = base_width
        if isinstance(sticky, int) and sticky > 0:
            if frozen_boundary_idx is not None and idx == frozen_boundary_idx:
                seed = max(1, sticky - 1)
            else:
                seed = sticky
        seed = max(seed, header_label_width)
        col_widths.append(seed)
        seed_widths.append(seed)

    if frozen_boundary_idx is not None and 0 <= frozen_boundary_idx < len(col_widths):
        col_widths[frozen_boundary_idx] += 1
        seed_widths[frozen_boundary_idx] += 1
        original_widths[frozen_boundary_idx] += 1

    sheet_obj = getattr(viewer, "sheet", None)
    fill_column_name: str | None = None
    if sheet_obj is not None:
        preferred_fill = None
        if hasattr(sheet_obj, "preferred_fill_column"):
            preferred = sheet_obj.preferred_fill_column
            preferred_fill = preferred() if callable(preferred) else preferred
        if preferred_fill is None:
            preferred_fill = getattr(sheet_obj, "fill_column_name", None)
        if isinstance(preferred_fill, str) and preferred_fill in cols:
            fill_column_name = preferred_fill
    fill_idx = cols.index(fill_column_name) if fill_column_name else None

    all_maximized = getattr(viewer, "all_columns_maximized", False)
    col_maximized = getattr(viewer, "maximized_column_index", None)
    maximized_column_name: str | None = None
    if col_maximized is not None and 0 <= col_maximized < len(viewer.columns):
        maximized_column_name = viewer.columns[col_maximized]

    if (
        cols
        and fill_idx is None
        and not (col_maximized is not None or all_maximized)
        and hasattr(viewer, "_last_col_fits_completely")
        and not getattr(viewer, "_last_col_fits_completely", True)
    ):
        border_overhead = _table_border_overhead(len(cols))
        available_width = max(1, width - border_overhead)
        used_width = sum(col_widths[:-1])
        remaining_width = available_width - used_width
        last_header_width = header_label_widths[-1] if header_label_widths else len(cols[-1]) + 2
        min_last_width = max(4, last_header_width)
        extended_width = max(min_last_width, remaining_width)
        col_widths[-1] = extended_width

    if all_maximized and cols:
        border_overhead = _table_border_overhead(len(cols))
        available_inner = max(1, width - border_overhead)
        current_total = sum(col_widths)
        if current_total < available_inner:
            extra = available_inner - current_total
            share, remainder = divmod(extra, len(col_widths))
            if share:
                for idx in range(len(col_widths)):
                    col_widths[idx] += share
            if remainder:
                for idx in range(remainder):
                    col_widths[-(idx + 1)] += 1

    schema = getattr(viewer, "schema", None) or getattr(viewer.sheet, "schema", {})
    columns_data = [table_slice.column(name) for name in cols]

    current_visible_col_index: int | None = None
    if 0 <= viewer.cur_col < len(viewer.columns):
        current_col_name = viewer.columns[viewer.cur_col]
        try:
            current_visible_col_index = cols.index(current_col_name)
        except ValueError:
            current_visible_col_index = 0 if cols else None

    if current_visible_col_index is None and cols:
        current_visible_col_index = min(viewer.cur_col, len(cols) - 1)

    column_meta: list[_ColumnMeta] = []
    for idx, column_name in enumerate(cols):
        is_frozen = column_name in frozen_name_set
        dtype = schema.get(column_name)
        is_numeric = bool(dtype and _is_numeric_dtype(dtype))
        col_has_nulls = table_slice.height > 0 and columns_data[idx].null_count > 0
        header_display = (
            header_label_widths[idx]
            if idx < len(header_label_widths)
            else display_width(column_name)
        )
        min_width = max(4, min(original_widths[idx], header_display))
        if is_numeric:
            min_width = max(min_width, min(original_widths[idx], 8))
        header_active = idx == current_visible_col_index
        column_meta.append(
            _ColumnMeta(
                name=column_name,
                dtype=dtype,
                is_numeric=is_numeric,
                has_nulls=col_has_nulls,
                min_width=min_width,
                original_width=original_widths[idx],
                header_active=header_active,
                is_sorted=column_name in sort_map,
                is_frozen=is_frozen,
            )
        )

    border_overhead = _table_border_overhead(len(cols))
    available_inner = max(1, width - border_overhead) if cols else width

    allow_partial_last = (
        cols
        and fill_idx is None
        and not (col_maximized is not None or all_maximized)
        and hasattr(viewer, "_last_col_fits_completely")
        and not getattr(viewer, "_last_col_fits_completely", True)
    )

    min_widths: list[int] = []
    minimum_targets: list[int] = []
    for idx, meta in enumerate(column_meta):
        seed = seed_widths[idx] if idx < len(seed_widths) else meta.original_width
        base_min = max(meta.min_width, seed) if meta.is_frozen else meta.min_width
        min_widths.append(base_min)
        minimum_targets.append(base_min if meta.is_frozen else meta.min_width)

    if maximized_column_name:
        for idx, meta in enumerate(column_meta):
            if meta.name != maximized_column_name:
                continue
            max_target = max(seed_widths[idx], meta.original_width, min_widths[idx])
            min_widths[idx] = max_target
            seed_widths[idx] = max_target
            minimum_targets[idx] = max_target
            break

    if (
        allow_partial_last
        and min_widths
        and not column_meta[-1].is_frozen
        and not (maximized_column_name and column_meta[-1].name == maximized_column_name)
    ):
        min_widths[-1] = 1
        minimum_targets[-1] = 1

    col_widths = list(min_widths)

    total_min = sum(col_widths)
    if total_min > available_inner:
        col_widths = _shrink_widths_to_fit(col_widths, minimum_targets, available_inner)
    else:
        remaining = available_inner - total_min
        weights: list[int] = []
        targets: list[int] = []
        for idx, meta in enumerate(column_meta):
            sticky = sticky_widths.get(meta.name)
            seed = seed_widths[idx] if idx < len(seed_widths) else meta.original_width
            if meta.is_frozen:
                target = col_widths[idx]
                weights_val = 0
            else:
                target = max(meta.min_width, seed)
                if isinstance(sticky, int) and sticky > 0:
                    target = max(target, sticky)
                weights_val = 1
                if meta.is_numeric:
                    weights_val += 1
                if meta.header_active:
                    weights_val += 2
                if fill_idx is not None and idx == fill_idx:
                    weights_val += 1
                if maximized_column_name and meta.name == maximized_column_name:
                    weights_val += 3
                    target = max(target, available_inner)
                if getattr(viewer, "is_hist_view", False):
                    weights_val += 1
                if getattr(viewer, "freq_source_col", None) == meta.name:
                    weights_val += 1
                if all_maximized:
                    weights_val += 1
            weights.append(weights_val)
            targets.append(max(target, meta.min_width))

        remaining = _allocate_widths(col_widths, targets, weights, remaining)

        if remaining > 0:
            if (
                fill_idx is not None
                and 0 <= fill_idx < len(col_widths)
                and not column_meta[fill_idx].is_frozen
            ):
                col_widths[fill_idx] += remaining
                remaining = 0
            else:
                expanded_caps = []
                for idx in range(len(targets)):
                    if column_meta[idx].is_frozen:
                        expanded_caps.append(col_widths[idx])
                    else:
                        expanded_caps.append(targets[idx] + remaining)
                remaining = _allocate_widths(col_widths, expanded_caps, weights, remaining)

    column_plans: list[ColumnPlan] = []
    for idx, meta in enumerate(column_meta):
        header_label = (
            header_labels[idx]
            if idx < len(header_labels)
            else _header_label_for_column(meta.name, sort_map)
        )
        column_plans.append(
            ColumnPlan(
                name=meta.name,
                header_label=header_label,
                width=col_widths[idx],
                min_width=meta.min_width,
                original_width=meta.original_width,
                is_numeric=meta.is_numeric,
                has_nulls=meta.has_nulls,
                header_active=meta.header_active,
                is_sorted=meta.is_sorted,
            )
        )

    viewer._sticky_column_widths = {plan.name: plan.width for plan in column_plans}

    header_row: list[Cell] = []
    for column in column_plans:
        cell = Cell(
            text=column.header_label,
            role="header",
            active_row=False,
            active_col=column.header_active,
            active_cell=column.header_active,
            selected_row=False,
            numeric=False,
            is_null=False,
        )
        header_row.append(cell)

    pad = 1
    formatted_columns: list[Sequence[str]] = []
    column_inner_widths: list[int] = []
    for idx, column in enumerate(column_plans):
        column_width = max(1, column.width)
        border_offset = 1 if frozen_boundary_idx is not None and idx == frozen_boundary_idx else 0
        content_width = max(0, column_width - border_offset)
        padding = pad if content_width >= (pad * 2 + 1) else 0
        inner_width = max(0, content_width - (padding * 2))
        safe_max_chars = max(inner_width, 0) if column.name == "hist" else max(inner_width, 1, 20)
        formatted_columns.append(columns_data[idx].formatted(safe_max_chars))
        column_inner_widths.append(inner_width)

    decimal_cache = getattr(viewer, "_decimal_alignment_cache", None)
    if decimal_cache is None:
        decimal_cache = {}
        viewer._decimal_alignment_cache = decimal_cache

    decimal_alignments: list[tuple[int, int] | None] = []
    for idx, column in enumerate(column_plans):
        if not column.is_numeric:
            decimal_alignments.append(None)
            continue
        inner_width = column_inner_widths[idx]
        viewport_alignment = compute_decimal_alignment(formatted_columns[idx], inner_width)
        cached_alignment = decimal_cache.get(column.name)

        merged_alignment: tuple[int, int] | None = None
        if cached_alignment and viewport_alignment:
            merged_alignment = (
                max(cached_alignment[0], viewport_alignment[0]),
                cached_alignment[1],
            )
        elif cached_alignment:
            merged_alignment = cached_alignment
        else:
            merged_alignment = viewport_alignment

        if merged_alignment is not None:
            required_width = merged_alignment[0] + 1 + merged_alignment[1]
            if inner_width >= required_width:
                decimal_cache[column.name] = merged_alignment
                decimal_alignments.append(merged_alignment)
                continue

        decimal_alignments.append(None)

    row_positions = getattr(viewer, "visible_row_positions", [])
    selection_lookup = set(getattr(viewer, "_selected_row_ids", set()))
    selection_filter_matches: set[Hashable] | None = None
    selection_filter_expr = getattr(viewer, "_selection_filter_expr", None)
    if not selection_filter_expr:
        value_filter_expr_fn = getattr(viewer, "_value_selection_filter_expr", None)
        if callable(value_filter_expr_fn):
            try:
                selection_filter_expr = value_filter_expr_fn()
            except Exception:
                selection_filter_expr = None
    if selection_filter_expr and not selection_lookup:
        resolver = getattr(viewer, "_selection_matches_for_slice", None)
        if callable(resolver):
            original_expr = getattr(viewer, "_selection_filter_expr", None)
            try:
                if original_expr != selection_filter_expr:
                    viewer._selection_filter_expr = selection_filter_expr
                selection_filter_matches = resolver(table_slice, row_positions)
            except Exception:
                selection_filter_matches = None
            finally:
                if original_expr != selection_filter_expr:
                    viewer._selection_filter_expr = original_expr
        if selection_filter_matches is None:
            # Attempt to fetch required columns even when they are scrolled out of view.
            fetch_columns = list(table_slice.column_names)
            if selection_filter_expr:
                for name in getattr(viewer, "columns", ()):
                    if name not in fetch_columns:
                        fetch_columns.append(name)
            value_filter = getattr(viewer, "_value_selection_filter", None)
            filter_column = value_filter[0] if value_filter else None
            if filter_column and filter_column not in fetch_columns:
                fetch_columns.append(filter_column)
            row_id_column = getattr(getattr(viewer, "row_provider", None), "_row_id_column", None)
            if row_id_column and row_id_column not in fetch_columns:
                fetch_columns.append(row_id_column)

            start = table_slice.start_offset
            if start is None and row_positions:
                start = min(row_positions)
            if start is None:
                start = getattr(viewer, "row0", None)
            count = max(0, table_slice.height or len(row_positions))
            if fetch_columns and count > 0 and start is not None:
                plan = getattr(viewer, "_current_plan", None)
                row_provider = getattr(viewer, "row_provider", None)
                if callable(plan) and row_provider is not None:
                    try:
                        supplemental_slice, _status = row_provider.get_slice(
                            plan(),
                            fetch_columns,
                            int(start),
                            int(count),
                        )
                    except Exception:
                        supplemental_slice = None
                    if supplemental_slice is not None:
                        resolver = getattr(viewer, "_selection_matches_for_slice", None)
                        if callable(resolver):
                            try:
                                original_expr = getattr(viewer, "_selection_filter_expr", None)
                                if original_expr != selection_filter_expr:
                                    viewer._selection_filter_expr = selection_filter_expr
                                selection_filter_matches = resolver(
                                    supplemental_slice, row_positions
                                )
                            except Exception:
                                selection_filter_matches = None
                            finally:
                                if original_expr != selection_filter_expr:
                                    viewer._selection_filter_expr = original_expr
    resolve_row_id = getattr(viewer, "_row_identifier_for_slice", None)
    visible_frozen_rows = min(getattr(viewer, "visible_frozen_row_count", 0), table_slice.height)
    value_selection_filter = getattr(viewer, "_value_selection_filter", None)
    filter_column_index: int | None = None
    filter_value = None
    filter_is_nan = False
    if value_selection_filter is not None:
        filter_column, filter_value, filter_is_nan = value_selection_filter
        for idx, column in enumerate(column_plans):
            if column.name == filter_column:
                filter_column_index = idx
                break

    body_rows: list[list[Cell]] = []
    for r in range(table_slice.height):
        row_cells: list[Cell] = []
        row_index = row_positions[r] if r < len(row_positions) else viewer.row0 + r
        row_active = row_index == viewer.cur_row
        need_row_id = bool(selection_lookup or selection_filter_matches)
        row_identifier = None
        if need_row_id and callable(resolve_row_id):
            try:
                row_identifier = resolve_row_id(
                    table_slice,
                    r,
                    row_positions=row_positions,
                    absolute_row=row_index,
                )
            except Exception:
                row_identifier = None
        if need_row_id and row_identifier is None:
            if r < len(row_positions):
                row_identifier = row_positions[r]
            elif table_slice.start_offset is not None:
                row_identifier = table_slice.start_offset + r
        row_selected = bool(selection_lookup and row_identifier in selection_lookup)
        if not row_selected and selection_filter_matches:
            row_selected = row_identifier in selection_filter_matches
        if not row_selected and filter_column_index is not None:
            try:
                value = columns_data[filter_column_index].values[r]
            except Exception:
                value = None
            if filter_is_nan:
                row_selected = isinstance(value, float) and math.isnan(value)
            else:
                row_selected = value == filter_value
        for ci, column in enumerate(column_plans):
            meta = column_meta[ci]
            dtype = meta.dtype
            is_numeric = column.is_numeric
            width_hint = max(1, column.width)
            border_offset = (
                1 if frozen_boundary_idx is not None and ci == frozen_boundary_idx else 0
            )
            content_width = max(0, width_hint - border_offset)
            padding = pad if content_width >= (pad * 2 + 1) else 0
            inner_width = max(0, content_width - padding * 2)
            precomputed_txt = formatted_columns[ci][r]
            raw_value = columns_data[ci].values[r]

            is_null = raw_value is None or precomputed_txt == ""
            if is_null:
                base_txt = "null"
            elif isinstance(raw_value, float) and (math.isnan(raw_value) or math.isinf(raw_value)):
                base_txt = "NaN" if math.isnan(raw_value) else ("inf" if raw_value > 0 else "-inf")
            else:
                base_txt = precomputed_txt

            visible_txt = truncate_grapheme_safe(base_txt, inner_width) if inner_width > 0 else ""
            alignment = decimal_alignments[ci] if ci < len(decimal_alignments) else None
            aligned_candidate = (
                apply_decimal_alignment(base_txt, alignment, inner_width)
                if alignment is not None and inner_width > 0 and not is_null
                else None
            )
            if aligned_candidate is not None:
                aligned_txt = aligned_candidate
            elif is_numeric and inner_width > 0:
                aligned_txt = pad_left_display(visible_txt, inner_width)
            elif inner_width > 0:
                aligned_txt = pad_right_display(visible_txt, inner_width)
            else:
                aligned_txt = visible_txt

            cell_text = (" " * padding) + aligned_txt + (" " * padding)
            cell_width = display_width(cell_text)
            if content_width > 0 and cell_width < content_width:
                cell_text = pad_right_display(cell_text, content_width)
            elif content_width > 0 and cell_width > content_width:
                cell_text = truncate_grapheme_safe(cell_text, content_width)
            elif content_width == 0:
                cell_text = ""

            col_active = ci == current_visible_col_index
            cell = Cell(
                text=cell_text,
                role="body",
                active_row=row_active,
                active_col=col_active,
                active_cell=row_active and col_active,
                selected_row=row_selected,
                numeric=is_numeric,
                is_null=is_null,
            )
            row_cells.append(cell)
        body_rows.append(row_cells)

    cells: list[list[Cell]] = []
    if header_row:
        cells.append(header_row)
    cells.extend(body_rows)

    row_offset = max(0, viewer.row0)
    if visible_frozen_rows:
        row_offset = max(row_offset, visible_frozen_rows)

    col_offset = max(0, viewer.col0)

    return ViewportPlan(
        columns=column_plans,
        frozen_boundary_idx=frozen_boundary_idx,
        rows=table_slice.height,
        row_offset=row_offset,
        col_offset=col_offset,
        cells=cells,
        active_row_index=getattr(viewer, "cur_row", 0),
    )

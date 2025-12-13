"""Cursor and viewport helpers for :mod:`pulka.core.viewer`.

This module centralises the math required to keep the viewer's cursor and
viewport in sync with the underlying dataset. It also owns the undo/redo
snapshots that the transformation manager persists. The intent is to keep
``Viewer`` focused on high level workflows while this helper provides
deterministic primitives that are easy to unit test.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from .viewer import Viewer


@dataclass(slots=True)
class ViewerSnapshot:
    """State payload persisted for undo/redo operations."""

    hidden_cols: tuple[str, ...]
    header_widths: tuple[int, ...]
    cur_col: int
    col0: int
    cur_row: int
    row0: int
    selected_row_ids: tuple[Hashable, ...]
    selection_epoch: int
    selection_filter_expr: str | None
    value_selection_filter: tuple[str, object, bool] | None


class ViewerStateController:
    """Encapsulate cursor/viewport bookkeeping for a :class:`Viewer`."""

    def __init__(self, viewer: Viewer) -> None:
        self._viewer = viewer

    # ------------------------------------------------------------------
    # Snapshot helpers
    # ------------------------------------------------------------------

    def capture_snapshot(self) -> ViewerSnapshot:
        """Capture viewer-specific state required for undo/redo."""

        viewer = self._viewer
        hidden_cols = tuple(col for col in viewer.columns if col in viewer._hidden_cols)
        return ViewerSnapshot(
            hidden_cols=hidden_cols,
            header_widths=tuple(viewer._header_widths),
            cur_col=viewer.cur_col,
            col0=viewer.col0,
            cur_row=viewer.cur_row,
            row0=viewer.row0,
            selected_row_ids=tuple(viewer._selected_row_ids),
            selection_epoch=viewer._selection_epoch,
            selection_filter_expr=getattr(viewer, "_selection_filter_expr", None),
            value_selection_filter=viewer._value_selection_filter,
        )

    def restore_snapshot(self, state: ViewerSnapshot) -> None:
        """Restore viewer state from ``state`` and reconcile caches."""

        viewer = self._viewer
        current_columns = tuple(viewer.columns)
        projection = viewer._plan_projection_columns()
        if projection is not None:
            hidden_from_plan = {name for name in current_columns if name not in set(projection)}
            viewer._local_hidden_cols.clear()
            viewer._update_hidden_column_cache(hidden_from_plan, ensure_cursor=False)
        else:
            restored_hidden = {name for name in state.hidden_cols if name in current_columns}
            viewer._local_hidden_cols = set(restored_hidden)
            viewer._update_hidden_column_cache(restored_hidden, ensure_cursor=False)

        active_hidden = set(viewer._hidden_cols)

        expected_widths = len(current_columns)
        widths = list(state.header_widths[:expected_widths])
        defaults = viewer._default_header_widths
        if len(widths) < expected_widths:
            for idx in range(len(widths), expected_widths):
                baseline = defaults[idx] if idx < len(defaults) else viewer._min_col_width
                widths.append(max(baseline, viewer._min_col_width))
        for idx, name in enumerate(current_columns):
            is_hidden = name in active_hidden
            if idx >= len(widths):
                baseline = defaults[idx] if idx < len(defaults) else viewer._min_col_width
                widths.append(0 if is_hidden else max(baseline, viewer._min_col_width))
                continue
            if is_hidden:
                widths[idx] = 0
            else:
                widths[idx] = max(widths[idx], viewer._min_col_width)

        viewer._header_widths = widths[:expected_widths]

        if viewer.columns:
            viewer.cur_col = max(0, min(state.cur_col, len(viewer.columns) - 1))
            viewer.col0 = max(0, min(state.col0, len(viewer.columns) - 1))
        else:
            viewer.cur_col = 0
            viewer.col0 = 0

        viewer.cur_row = max(0, state.cur_row)
        viewer.row0 = max(0, state.row0)
        viewer._selected_row_ids = set(state.selected_row_ids)
        viewer._selection_epoch = state.selection_epoch
        viewer._selection_filter_expr = state.selection_filter_expr
        viewer._value_selection_filter = state.value_selection_filter

        viewer.invalidate_row_count()
        viewer._visible_key = None
        viewer._invalidate_frozen_columns_cache()
        viewer._reconcile_schema_changes()
        self.ensure_cursor_on_visible_column()
        viewer.clamp()

    # ------------------------------------------------------------------
    # Cursor + viewport math
    # ------------------------------------------------------------------

    def clamp(self) -> None:
        """Clamp the cursor and viewport to valid ranges."""

        viewer = self._viewer
        total_rows = viewer._total_rows
        if total_rows is not None and total_rows > 0:
            max_row_index = total_rows - 1
            viewer.cur_row = max(0, min(viewer.cur_row, max_row_index))
        else:
            viewer.cur_row = max(0, viewer.cur_row)

        if viewer.columns:
            if (
                viewer.cur_col < len(viewer.columns)
                and viewer.columns[viewer.cur_col] in viewer._hidden_cols
            ):
                next_visible = self.next_visible_col_index(viewer.cur_col)
                if next_visible is not None:
                    viewer.cur_col = next_visible
                else:
                    for i in range(viewer.cur_col - 1, -1, -1):
                        if viewer.columns[i] not in viewer._hidden_cols:
                            viewer.cur_col = i
                            break
                    else:
                        for i, col in enumerate(viewer.columns):
                            if col not in viewer._hidden_cols:
                                viewer.cur_col = i
                                break
            viewer.cur_col = max(0, min(viewer.cur_col, len(viewer.columns) - 1))

        frozen_row_min = viewer._effective_frozen_row_count()
        body_height = viewer._body_view_height()
        total_rows = viewer._total_rows if viewer._total_rows and viewer._total_rows > 0 else None
        max_row0 = self.max_row0_for_total(total_rows) if total_rows is not None else None

        if viewer.cur_row >= frozen_row_min:
            desired_row0 = min(viewer.row0, viewer.cur_row)
            if viewer.cur_row >= desired_row0 + body_height:
                desired_row0 = viewer.cur_row - body_height + 1
        else:
            desired_row0 = viewer.row0

        desired_row0 = max(frozen_row_min, desired_row0)
        if max_row0 is not None:
            desired_row0 = min(desired_row0, max_row0)
        viewer.row0 = desired_row0

        frozen_col_min = viewer._first_scrollable_col_index() if viewer.frozen_column_count else 0
        max_col_index = max(0, len(viewer.columns) - 1) if viewer.columns else 0
        desired_col0 = (
            min(viewer.col0, viewer.cur_col) if viewer.cur_col >= frozen_col_min else viewer.col0
        )
        desired_col0 = min(desired_col0, max_col_index)
        viewer.col0 = max(frozen_col_min, desired_col0)

        if __debug__:
            viewer._validate_state_consistency()

    def max_row0_for_total(self, total_rows: int) -> int:
        """Return the largest valid ``row0`` for ``total_rows`` rows."""

        viewer = self._viewer
        return max(0, total_rows - viewer._body_view_height())

    def next_visible_col_index(self, search_from: int) -> int | None:
        """Find the next visible column index, searching right then left."""

        viewer = self._viewer
        for i in range(search_from + 1, len(viewer.columns)):
            if viewer.columns[i] not in viewer._hidden_cols:
                return i
        for i in range(search_from - 1, -1, -1):
            if viewer.columns[i] not in viewer._hidden_cols:
                return i
        return None

    def move_cursor_to_next_visible_column(self) -> None:
        """Move cursor to the next visible column if available."""

        viewer = self._viewer
        next_visible_idx = self.next_visible_col_index(viewer.cur_col)
        if next_visible_idx is not None:
            viewer.cur_col = next_visible_idx
            if viewer.columns[
                viewer.cur_col
            ] not in viewer.visible_cols and not viewer._is_column_frozen(viewer.cur_col):
                viewer.col0 = min(viewer.col0, viewer.cur_col)

    def ensure_cursor_on_visible_column(self) -> None:
        """Ensure the cursor is positioned on a visible column."""

        viewer = self._viewer
        if not viewer.columns:
            return

        current_col_name = viewer.columns[viewer.cur_col]
        if current_col_name in viewer._hidden_cols:
            self.move_cursor_to_next_visible_column()
        else:
            if current_col_name not in viewer.visible_cols and not viewer._is_column_frozen(
                viewer.cur_col
            ):
                viewer.col0 = min(viewer.col0, viewer.cur_col)

from __future__ import annotations

import polars as pl

from pulka.core.engine.contracts import TableColumn, TableSlice
from pulka.core.row_identity import ROW_ID_COLUMN
from pulka.core.viewer import Viewer
from pulka.core.viewer.public_state import viewer_public_state
from pulka.core.viewer.row_count_tracker import RowCountTracker
from pulka.core.viewer.state import ViewerSnapshot
from pulka.core.viewer.ui_hooks import NullViewerUIHooks
from pulka.render.viewport_plan import compute_viewport_plan
from pulka.sheets.data_sheet import DataSheet


def _extract_id_from_signature(value):
    if isinstance(value, tuple) and value and isinstance(value[0], tuple):
        row_marker = None
        id_candidate = None
        column_candidate = None
        value_candidate = None
        for name, candidate in value:
            if name == "id":
                id_candidate = candidate
            elif name == "column":
                column_candidate = candidate
            elif name == "value":
                value_candidate = candidate
            elif name == "__row__":
                row_marker = candidate
        chosen = id_candidate if id_candidate is not None else column_candidate
        if chosen is None:
            chosen = value_candidate if value_candidate is not None else value[0][1]
        if row_marker is not None:
            if chosen is None:
                return row_marker
            return (chosen, row_marker)
        return chosen
    return value


def _extract_rows(selected):
    rows: set[int] = set()
    for item in selected:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], int):
            rows.add(item[1])
        elif isinstance(item, int):
            rows.add(item)
    return rows


def _make_plan_viewer(job_runner) -> Viewer:
    df = pl.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


class _LegacySheet:
    def __init__(self) -> None:
        self.columns = ["id", "name"]
        self.schema = {"id": pl.Int64, "name": pl.Utf8}

    def fetch_slice(self, row_start: int, row_count: int, columns: list[str]) -> pl.DataFrame:
        return pl.DataFrame({name: [] for name in columns})


def _make_legacy_viewer(job_runner) -> Viewer:
    sheet = _LegacySheet()
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


class _RowIdSheet:
    def __init__(self) -> None:
        self.columns = ["value"]
        self.schema = {"value": pl.Int64}
        self._data = pl.DataFrame({"value": [1, 2, 3]})

    def __len__(self) -> int:
        return len(self._data)

    def fetch_slice(self, row_start: int, row_count: int, columns: list[str]) -> TableSlice:
        frame = self._data.slice(row_start, row_count)
        column = TableColumn("value", tuple(frame["value"]), pl.Int64, 0)
        row_ids = tuple(f"row-{row_start + idx}" for idx in range(len(frame)))
        return TableSlice((column,), {"value": pl.Int64}, start_offset=row_start, row_ids=row_ids)


def test_state_snapshot_roundtrip_restores_hidden_columns(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    state = viewer.state_controller

    baseline_widths = tuple(viewer._header_widths)
    viewer._local_hidden_cols = {"name"}
    viewer._update_hidden_column_cache(set(viewer._local_hidden_cols))
    viewer.cur_row = 2
    viewer.row0 = 1
    viewer.cur_col = 0
    viewer.col0 = 0

    snapshot = state.capture_snapshot()

    viewer._hidden_cols.clear()
    viewer._local_hidden_cols.clear()
    viewer._header_widths = [1, 1]
    viewer.cur_row = 0
    viewer.row0 = 0

    state.restore_snapshot(snapshot)

    assert viewer._hidden_cols == {"name"}
    assert viewer._local_hidden_cols == {"name"}
    assert tuple(viewer._header_widths) == baseline_widths
    assert viewer.cur_row == 2
    assert viewer.row0 == 1


def test_state_clamp_skips_hidden_columns(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("name")
    viewer._local_hidden_cols = {"name"}
    viewer._update_hidden_column_cache(set(viewer._local_hidden_cols), ensure_cursor=False)

    viewer.clamp()

    assert viewer.columns[viewer.cur_col] == "id"


def test_state_restore_trims_unknown_hidden_columns_and_extends_widths(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    controller = viewer.state_controller

    viewer.columns.append("extra")
    viewer._default_header_widths.append(12)
    viewer._header_widths = [8, 9]  # shorter than columns on purpose
    viewer.cur_row = 0
    viewer.row0 = 0

    snapshot = ViewerSnapshot(
        hidden_cols=("missing",),
        header_widths=(5,),
        cur_col=0,
        col0=0,
        cur_row=2,
        row0=1,
        selected_row_ids=(),
        selection_epoch=0,
        selection_filter_expr=None,
        value_selection_filter=None,
    )

    controller.restore_snapshot(snapshot)

    assert viewer._hidden_cols == set()
    assert viewer._local_hidden_cols == set()
    assert len(viewer._header_widths) == len(viewer.columns)
    assert viewer._header_widths[-1] >= viewer._min_col_width


def test_row_selection_undo_redo(job_runner):
    viewer = _make_plan_viewer(job_runner)
    viewer.cur_row = 1

    baseline_epoch = viewer.selection_epoch
    viewer.toggle_row_selection()

    selected_ids = {_extract_id_from_signature(item) for item in viewer._selected_row_ids}
    assert selected_ids == {1}
    assert viewer.selection_epoch == baseline_epoch + 1

    viewer.undo_last_operation()
    assert not viewer._selected_row_ids
    assert viewer.selection_epoch == baseline_epoch

    viewer.redo_last_operation()
    selected_ids = {_extract_id_from_signature(item) for item in viewer._selected_row_ids}
    assert selected_ids == {1}
    assert viewer.selection_epoch == baseline_epoch + 1


def test_invert_selection_toggles_visible_rows(job_runner):
    viewer = _make_plan_viewer(job_runner)
    viewer.cur_row = 1

    viewer.toggle_row_selection()
    plan = viewer._current_plan()
    assert viewer._selection_count(plan) == 1
    viewer.invert_selection()

    invert_epoch = viewer.selection_epoch
    selection_after_first_invert = viewer._selection_count(plan)
    assert selection_after_first_invert == 2
    slice_after_invert = viewer.get_visible_table_slice(viewer.columns)
    matches = viewer._selection_matches_for_slice(slice_after_invert, viewer.visible_row_positions)
    assert matches is None or len(matches) == 2

    viewer.invert_selection()
    assert viewer._selection_count(plan) == 1
    slice_after_second = viewer.get_visible_table_slice(viewer.columns)
    matches_after_second = viewer._selection_matches_for_slice(
        slice_after_second, viewer.visible_row_positions
    )
    assert matches_after_second is None or len(matches_after_second) == 1

    assert viewer.selection_epoch == invert_epoch + 1

    viewer.undo_last_operation()
    assert viewer._selection_count(plan) == 2
    assert viewer._selection_filter_expr is not None
    assert viewer.selection_epoch == invert_epoch

    viewer.redo_last_operation()
    assert viewer._selection_count(plan) == 1
    assert viewer.selection_epoch == invert_epoch + 1


def test_invert_selection_selects_all_when_empty(job_runner):
    viewer = _make_plan_viewer(job_runner)

    viewer.invert_selection()

    assert viewer._selected_row_ids == {0, 1, 2}
    assert viewer.selection_epoch == 1
    assert (viewer.status_message or "").startswith("Selected")


def test_invert_selection_uses_row_ids(job_runner):
    viewer = Viewer(_RowIdSheet(), viewport_rows=5, viewport_cols=5, runner=job_runner)
    viewer.cur_row = 0
    viewer.invert_selection()

    selected_ids = {_extract_id_from_signature(item) for item in viewer._selected_row_ids}
    assert selected_ids == {"row-0", "row-1", "row-2"}
    assert viewer.status_message.startswith("Selected")

    viewer.toggle_row_selection()
    viewer.invert_selection()

    selected_ids = {_extract_id_from_signature(item) for item in viewer._selected_row_ids}
    assert selected_ids == {"row-0"}


def test_invert_selection_inverts_value_filter_when_column_missing(job_runner):
    viewer = _make_plan_viewer(job_runner)
    # Inject a value selection filter that does not match current columns to
    # simulate stale selection state.
    viewer._value_selection_filter = ("missing", "x", False)

    viewer.invert_selection()

    assert viewer._value_selection_filter is None
    assert viewer._selected_row_ids == set()
    assert viewer._selection_filter_expr == "~(c[\"missing\"] == lit('x'))"
    assert viewer.selection_epoch == 1


def test_invert_selection_marks_rows_via_filter(job_runner):
    df = pl.DataFrame({"id": [1, 2], "value": ["a", "b"]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_row = 0
    viewer.toggle_row_selection()  # select first row
    viewer.invert_selection()  # should select second row via filter expr

    plan = compute_viewport_plan(viewer, width=40, height=10)

    header, row0, row1 = plan.cells
    assert any(cell.selected_row for cell in row0) is False
    assert any(cell.selected_row for cell in row1) is True


def test_invert_selection_toggles_cleanly(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3], "value": ["a", "b", "c"]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_row = 0
    viewer.toggle_row_selection()  # select first row
    plan = viewer._current_plan()

    counts = []
    expr_lengths = []
    for _ in range(10):
        viewer.invert_selection()
        counts.append(viewer._selection_count(plan))
        expr = getattr(viewer, "_selection_filter_expr", "")
        expr_lengths.append(len(expr) if expr else 0)

    # Should alternate between selecting the other two rows and the original row.
    assert counts[0] == 2
    assert counts[1] == 1
    assert counts[-1] == 1  # even number of toggles returns to original

    # Clause length should stay bounded (no unbounded nesting).
    assert max(expr_lengths) < 200


def test_value_selection_highlight_survives_horizontal_scroll(job_runner):
    df = pl.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=2,
        runner=job_runner,
    )

    viewer.cur_col = viewer.columns.index("a")
    viewer.cur_row = 0
    viewer.select_matching_value_rows()

    # Hide the selection column by scrolling.
    viewer.col0 = 1
    plan = compute_viewport_plan(viewer, width=12, height=5)

    # Only the first row should be highlighted even when column 'a' is not visible.
    header, row0, row1 = plan.cells
    assert any(cell.selected_row for cell in row0) is True
    assert any(cell.selected_row for cell in row1) is False

    viewer.invert_selection()
    viewer.col0 = 1
    plan_after_invert = compute_viewport_plan(viewer, width=12, height=5)
    _, row0_after, row1_after = plan_after_invert.cells

    # Inversion should flip the highlight to the other row while still off-screen.
    assert any(cell.selected_row for cell in row0_after) is False
    assert any(cell.selected_row for cell in row1_after) is True


def test_clear_selection_handles_filter_selection(job_runner):
    df = pl.DataFrame({"a": [1, 2]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_col = 0
    viewer.cur_row = 0
    viewer.select_matching_value_rows()  # value-based selection filter
    assert viewer._selection_filter_expr is None
    assert viewer._value_selection_filter == ("a", 1, False)

    viewer.clear_row_selection()

    assert viewer._selection_filter_expr is None
    assert viewer._value_selection_filter is None
    assert viewer._selected_row_ids == set()
    assert (viewer.status_message or "").startswith("Cleared selection")


def test_clear_selection_tracks_undo(job_runner):
    viewer = _make_plan_viewer(job_runner)
    viewer.invert_selection()

    baseline_epoch = viewer.selection_epoch
    baseline_selection = set(viewer._selected_row_ids)

    viewer.clear_row_selection()

    assert not viewer._selected_row_ids
    assert viewer.selection_epoch == baseline_epoch + 1
    assert (viewer.status_message or "").startswith("Cleared selection")

    viewer.undo_last_operation()
    assert viewer._selected_row_ids == baseline_selection
    assert viewer.selection_epoch == baseline_epoch

    viewer.redo_last_operation()
    assert not viewer._selected_row_ids


def test_select_matching_value_rows_replaces_selection(job_runner):
    df = pl.DataFrame({"id": [1, 2, 1, 3], "name": ["a", "b", "a", "c"]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_col = viewer.columns.index("id")
    viewer.cur_row = 0
    viewer.select_matching_value_rows()

    assert viewer._value_selection_filter == ("id", 1, False)
    assert viewer._selected_row_ids == set()
    assert viewer.selection_epoch == 1

    viewer.cur_row = 1
    viewer.select_matching_value_rows()

    assert viewer._value_selection_filter == ("id", 2, False)
    assert viewer._selected_row_ids == set()
    assert viewer.selection_epoch == 2


def test_select_matching_value_handles_nan(job_runner):
    nan_values = [float("nan"), float("nan"), 1.0]
    df = pl.DataFrame({"value": nan_values})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_col = 0
    viewer.cur_row = 0
    viewer.select_matching_value_rows()

    column_name, target, is_nan = viewer._value_selection_filter or ("", None, False)
    assert column_name == "value"
    assert is_nan is True
    assert viewer.status_message.startswith("Selected 2 matching rows")
    assert viewer.selection_epoch == 1


def test_select_matching_value_survives_sort(job_runner):
    df = pl.DataFrame({"id": [1, 2, 1, 3], "name": ["b", "c", "a", "d"]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_col = viewer.columns.index("id")
    viewer.select_matching_value_rows()

    assert viewer._value_selection_filter == ("id", 1, False)
    selection_epoch = viewer.selection_epoch

    viewer.toggle_sort("id")

    assert viewer._value_selection_filter == ("id", 1, False)
    assert viewer.selection_epoch == selection_epoch + 1


def test_select_matching_value_rows_emits_progress_for_large_dataset(job_runner):
    df = pl.DataFrame({"value": [1] * 60_000})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_col = 0
    viewer.cur_row = 0
    viewer.select_matching_value_rows()

    assert viewer.status_message is not None
    assert viewer.status_message.startswith("Selected 60,000 matching rows")


def test_select_matching_value_rows_sets_progress_before_scan(monkeypatch, job_runner):
    df = pl.DataFrame({"value": [1, 2, 3]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    monkeypatch.setattr(viewer._row_counts, "ensure_total_rows", lambda: 100_000)

    class _Hook(NullViewerUIHooks):
        def __init__(self) -> None:
            self.invalidate_calls = 0
            self.scheduled_calls = 0

        def invalidate(self) -> None:
            self.invalidate_calls += 1

        def call_soon(self, callback):
            self.scheduled_calls += 1
            callback()

    hook = _Hook()
    viewer.set_ui_hooks(hook)

    seen: dict[str, str | None] = {}

    def _stub(plan):
        seen["status_before_scan"] = viewer.status_message
        return 2

    monkeypatch.setattr(viewer, "_selection_count", _stub)

    viewer.cur_col = 0
    viewer.cur_row = 0
    viewer.select_matching_value_rows()

    assert seen.get("status_before_scan", "").startswith("Selecting matching rows across ~100,000")
    assert viewer.status_message == "Selected 2 matching rows"
    assert hook.invalidate_calls >= 1
    assert hook.scheduled_calls >= 1


def test_selection_survives_sort_without_row_ids(job_runner):
    df = pl.DataFrame({"id": [2, 1, 3], "name": ["b", "a", "c"]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_row = 0
    viewer.toggle_row_selection()

    selected_before = set(viewer._selected_row_ids)
    assert len(selected_before) == 1

    viewer.toggle_sort("name")

    assert viewer._selected_row_ids == selected_before


def test_data_sheet_attaches_hidden_row_ids(job_runner):
    df = pl.DataFrame({"value": [10, 20, 30]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)

    assert ROW_ID_COLUMN not in sheet.columns

    table_slice = viewer.get_visible_table_slice(viewer.columns)
    assert ROW_ID_COLUMN not in table_slice.column_names
    assert table_slice.row_ids is not None
    assert len(table_slice.row_ids) == table_slice.height


def test_selection_stable_after_sort_with_injected_row_ids(job_runner):
    df = pl.DataFrame({"value": [1, 1, 2]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_row = 1
    viewer.toggle_row_selection()

    selected_before = set(viewer._selected_row_ids)
    assert len(selected_before) == 1

    viewer.toggle_sort("value")

    assert viewer._selected_row_ids == selected_before

    slice_after = viewer.get_visible_table_slice(viewer.columns)
    row_ids = getattr(slice_after, "row_ids", None)
    assert row_ids is not None
    matched_rows = {idx for idx in range(slice_after.height) if row_ids[idx] in selected_before}
    assert matched_rows


def test_selection_signature_handles_nan(job_runner):
    df = pl.DataFrame({"value": [float("nan"), 1.0]})
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=5,
        viewport_cols=5,
        runner=job_runner,
    )

    viewer.cur_row = 0
    viewer.toggle_row_selection()

    selected = next(iter(viewer._selected_row_ids))
    assert selected == 0

    viewer.toggle_sort("value")

    assert selected in viewer._selected_row_ids


def test_viewer_public_snapshot_exposes_sanitised_state(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    viewer.cur_row = 1
    viewer.row0 = 1
    viewer.cur_col = viewer.columns.index("name")
    viewer.col0 = 0
    viewer._local_hidden_cols = {"name"}
    viewer._update_hidden_column_cache(set(viewer._local_hidden_cols), ensure_cursor=False)

    state = viewer.snapshot()

    assert isinstance(state.visible_columns, tuple)
    assert isinstance(state.hidden_columns, tuple)
    assert state.cursor.row == 1
    assert state.cursor.col == viewer.columns.index("name")
    assert state.viewport.row0 == 1
    assert state.hidden_column_count == len(state.hidden_columns)
    assert "name" in state.hidden_columns
    assert "name" not in state.visible_columns


def test_viewer_public_state_helper_handles_missing_snapshot(job_runner):
    viewer = _make_legacy_viewer(job_runner)

    state = viewer_public_state(viewer)

    assert state is not None
    assert state.cursor.row == viewer.cur_row

    class _LegacyViewer:
        def __init__(self) -> None:
            self.cur_row = 0
            self.cur_col = 1
            self.row0 = 2
            self.col0 = 3
            self.columns = ["x", "y"]
            self.visible_cols = ["x"]
            self._hidden_cols = {"y"}
            self.sort_col = "x"
            self.sort_asc = True

    legacy = _LegacyViewer()

    legacy_state = viewer_public_state(legacy)

    assert legacy_state is not None
    assert legacy_state.cursor.row == 0
    assert legacy_state.cursor.col == 1
    assert legacy_state.viewport.row0 == 2
    assert legacy_state.visible_columns == ("x",)
    assert legacy_state.hidden_columns == ("y",)


def test_reconcile_schema_changes_respects_plan_projection(job_runner):
    viewer = _make_plan_viewer(job_runner)
    viewer.hide_current_column()
    viewer._reconcile_schema_changes()

    projection = tuple(viewer.sheet.plan.projection_or(viewer.columns))
    assert projection == tuple(viewer.visible_columns())
    assert viewer._local_hidden_cols == set()


def test_reconcile_schema_changes_unhides_everything_for_planless_sheet(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    viewer._local_hidden_cols = set(viewer.columns)
    viewer._update_hidden_column_cache(set(viewer._local_hidden_cols))

    viewer._reconcile_schema_changes()

    assert set(viewer.visible_columns()) == set(viewer.columns)
    assert viewer._local_hidden_cols == set()


def test_plan_controller_apply_plan_update_sets_limit(job_runner):
    viewer = _make_plan_viewer(job_runner)
    controller = viewer.plan_controller

    result = controller.apply_plan_update("limit", lambda plan: plan.with_limit(1))

    assert result is not None
    assert result.plan_changed is True
    assert viewer.sheet.plan.limit == 1


class _DummySheet:
    sheet_id = None

    def __len__(self) -> int:  # pragma: no cover - trivial
        return 8


class _DummyViewer:
    def __init__(self, runner) -> None:
        self.sheet = _DummySheet()
        self._total_rows: int | None = None
        self._row_count_stale = True
        self._row_count_future = None
        self._row_count_display_pending = False
        self._status_dirty = False
        self._ui_hooks = NullViewerUIHooks()
        self.invalidate_called = False
        self.job_runner = runner

    def invalidate_row_cache(self) -> None:
        self.invalidate_called = True

    def clamp(self) -> None:  # pragma: no cover - exercised indirectly
        pass

    @property
    def ui_hooks(self) -> NullViewerUIHooks:
        return self._ui_hooks

    def mark_status_dirty(self) -> None:
        self._status_dirty = True

    def acknowledge_status_rendered(self) -> None:
        self._status_dirty = False

    def is_status_dirty(self) -> bool:
        return self._status_dirty


def test_row_count_tracker_invalidates_and_counts(job_runner):
    dummy = _DummyViewer(job_runner)
    tracker = RowCountTracker(dummy, runner=job_runner)

    tracker.invalidate()

    assert dummy.is_status_dirty() is True
    assert dummy.invalidate_called is True
    assert dummy._total_rows is None

    total = tracker.ensure_total_rows()

    assert total == 8
    assert tracker.total_rows == 8
    assert dummy._total_rows == 8
    assert dummy._row_count_stale is False
    assert dummy._row_count_display_pending is False
    assert dummy.is_status_dirty() is True


def test_configure_terminal_clears_status_and_resets_cache(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    viewer.mark_status_dirty()
    viewer._visible_key = (1, 2, 3)
    viewer.configure_terminal(72, 10)

    assert viewer.view_width_chars == 72
    assert viewer.view_height == 10
    assert viewer._visible_key is None
    assert viewer.is_status_dirty() is False


def test_acknowledge_status_rendered_resets_flag(job_runner):
    viewer = _make_legacy_viewer(job_runner)
    viewer.mark_status_dirty()
    assert viewer.is_status_dirty() is True

    viewer.acknowledge_status_rendered()

    assert viewer.is_status_dirty() is False

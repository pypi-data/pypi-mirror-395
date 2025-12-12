import polars as pl

from pulka.core.viewer.viewer import Viewer
from pulka.sheets.data_sheet import DataSheet


class _PlanlessSheet:
    def __init__(self) -> None:
        self.columns = ["a", "b", "c"]
        self.schema = {"a": pl.Int64, "b": pl.Utf8, "c": pl.Int64}

    def fetch_slice(self, row_start: int, row_count: int, columns: list[str]) -> pl.DataFrame:
        return pl.DataFrame({name: [] for name in columns})


def _make_planless_viewer(job_runner) -> Viewer:
    sheet = _PlanlessSheet()
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


def _make_plan_viewer(job_runner) -> Viewer:
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


def test_filter_undo_redo(job_runner):
    viewer = _make_plan_viewer(job_runner)

    viewer.apply_filter("c.a > 1")
    assert viewer.filter_text == "c.a > 1"

    viewer.undo_last_operation()
    assert viewer.filter_text is None

    viewer.redo_last_operation()
    assert viewer.filter_text == "c.a > 1"


def test_reset_filters_history(job_runner):
    viewer = _make_plan_viewer(job_runner)

    viewer.apply_filter("c.a == 2")
    viewer.reset_filters()
    assert viewer.filter_text is None

    viewer.undo_last_operation()
    assert viewer.filter_text == "c.a == 2"

    viewer.redo_last_operation()
    assert viewer.filter_text is None


def test_hide_column_history(job_runner):
    viewer = _make_plan_viewer(job_runner)
    first_col = viewer.current_colname()

    viewer.hide_current_column()
    assert first_col not in viewer.visible_columns()
    projection_after_hide = viewer.sheet.plan.projection_or(viewer.columns)
    assert first_col not in projection_after_hide
    assert tuple(projection_after_hide) == tuple(viewer.visible_columns())

    viewer.undo_last_operation()
    assert first_col in viewer.visible_columns()
    projection_after_undo = viewer.sheet.plan.projection_or(viewer.columns)
    assert first_col in projection_after_undo

    viewer.redo_last_operation()
    assert first_col not in viewer.visible_columns()
    projection_after_redo = viewer.sheet.plan.projection_or(viewer.columns)
    assert first_col not in projection_after_redo


def test_hide_unhide_planless_sheet_uses_local_cache(job_runner):
    viewer = _make_planless_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("b")

    viewer.hide_current_column()

    assert viewer._local_hidden_cols == {"b"}
    assert viewer._hidden_cols == {"b"}
    assert "b" not in viewer.visible_columns()

    viewer.unhide_all_columns()

    assert viewer._local_hidden_cols == set()
    assert viewer._hidden_cols == set()
    assert set(viewer.visible_columns()) == set(viewer.columns)
    assert all(width >= viewer._min_col_width for width in viewer._header_widths)


def test_sort_history(job_runner):
    viewer = _make_plan_viewer(job_runner)

    viewer.toggle_sort()
    assert viewer.sort_col == viewer.current_colname()

    viewer.undo_last_operation()
    assert viewer.sort_col is None

    viewer.redo_last_operation()
    assert viewer.sort_col == viewer.current_colname()

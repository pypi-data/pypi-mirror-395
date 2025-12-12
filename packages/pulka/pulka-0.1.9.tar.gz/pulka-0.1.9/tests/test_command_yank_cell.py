import polars as pl

from pulka.command.builtins import _resolve_active_cell_display
from pulka.core.viewer import Viewer
from pulka.sheets.data_sheet import DataSheet


def _make_viewer(job_runner) -> Viewer:
    df = pl.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


class _FailingSheet:
    def __init__(self) -> None:
        self.columns = ["id", "name"]
        self.schema = {"id": pl.Int64, "name": pl.Utf8}

    def fetch_slice(self, row_start: int, row_count: int, columns):
        raise RuntimeError("slice unavailable")


def _make_failing_viewer(job_runner) -> Viewer:
    sheet = _FailingSheet()
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


def test_resolve_active_cell_display_returns_formatted_text(job_runner):
    viewer = _make_viewer(job_runner)
    viewer.cur_row = 1
    viewer.cur_col = viewer.columns.index("name")

    result = _resolve_active_cell_display(viewer)

    assert result == ("name", "b")


def test_resolve_active_cell_display_handles_errors(job_runner):
    viewer = _make_failing_viewer(job_runner)

    result = _resolve_active_cell_display(viewer)

    assert result is None

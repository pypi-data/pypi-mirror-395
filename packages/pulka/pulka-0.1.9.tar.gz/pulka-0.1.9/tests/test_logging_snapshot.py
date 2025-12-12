import polars as pl

from pulka.core.viewer import Viewer
from pulka.logging.snapshot import viewer_state_snapshot
from pulka.sheets.data_sheet import DataSheet


def _make_viewer(job_runner) -> Viewer:
    df = pl.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    return Viewer(sheet, viewport_rows=5, viewport_cols=5, runner=job_runner)


def test_viewer_state_snapshot_matches_public_snapshot(job_runner):
    viewer = _make_viewer(job_runner)
    viewer.cur_row = 1
    viewer.row0 = 1
    viewer.cur_col = viewer.columns.index("name")
    viewer.col0 = 0
    viewer.hide_current_column()

    public_state = viewer.snapshot()
    payload = viewer_state_snapshot(viewer)

    assert payload["cursor"] == {
        "row": public_state.cursor.row,
        "col": public_state.cursor.col,
    }
    assert payload["viewport"]["row0"] == public_state.viewport.row0
    assert payload["viewport"]["col0"] == public_state.viewport.col0
    assert payload["hidden_cols"] == list(public_state.hidden_columns)
    assert payload["visible_cols"] == list(public_state.visible_columns or public_state.columns)
    assert payload["maximized"]["mode"] == public_state.width_mode
    projection = viewer.sheet.plan.projection_or(viewer.columns)
    assert list(public_state.visible_columns) == list(projection)

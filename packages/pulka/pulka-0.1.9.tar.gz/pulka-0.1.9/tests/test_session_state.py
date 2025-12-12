import polars as pl
import pytest

from pulka.api import Session
from pulka.data.scanners import ScannerRegistry
from pulka.logging import Recorder, RecorderConfig
from pulka.sheets.file_browser_sheet import FileBrowserSheet


def test_session_state_json_uses_viewer_snapshot(tmp_path):
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": ["x", "y", "z", "w"],
            "c": [10, 20, 30, 40],
        }
    )
    dataset_path = tmp_path / "state.parquet"
    df.write_parquet(dataset_path)

    session = Session(str(dataset_path), viewport_rows=5, viewport_cols=3)
    viewer = session.viewer

    viewer.cur_row = 2
    viewer.row0 = 1
    viewer.cur_col = viewer.columns.index("b")
    viewer.col0 = 0
    viewer._hidden_cols.add("b")

    state = session.get_state_json()
    snapshot = viewer.snapshot()

    assert state["cursor_row"] == snapshot.cursor.row
    assert state["cursor_col"] == snapshot.cursor.col
    assert state["top_row"] == snapshot.viewport.row0
    assert state["left_col"] == snapshot.viewport.col0
    expected_rows = snapshot.total_rows or snapshot.visible_row_count
    expected_cols = snapshot.visible_column_count or snapshot.total_columns

    assert state["n_rows"] == expected_rows
    assert state["n_cols"] == expected_cols
    assert state["col_order"] == list(snapshot.visible_columns or snapshot.columns)


def test_session_tracks_dataset_path(tmp_path):
    df = pl.DataFrame({"a": [1, 2, 3]})
    first_path = tmp_path / "first.parquet"
    second_path = tmp_path / "second.parquet"
    df.write_parquet(first_path)
    pl.DataFrame({"a": [4, 5, 6]}).write_parquet(second_path)

    session = Session(str(first_path))
    assert session.dataset_path == first_path

    session.open(str(second_path))
    assert session.dataset_path == second_path

    lazyframe = pl.DataFrame({"b": [10]}).lazy()
    session.open_lazyframe(lazyframe, label="expr")
    assert session.dataset_path is None


def test_session_close_records_job_metrics(tmp_path):
    df = pl.DataFrame({"a": [1, 2, 3]})
    dataset_path = tmp_path / "metrics.parquet"
    df.write_parquet(dataset_path)
    recorder = Recorder(
        RecorderConfig(
            enabled=True,
            output_dir=tmp_path,
            compression="none",
            auto_flush_on_exit=False,
        )
    )
    session = Session(str(dataset_path), recorder=recorder)
    session.close()
    recorded_types = [event.type for event in recorder._buffer]
    assert "job_runner_metrics" in recorded_types


def test_session_dataset_path_tracks_view_stack(tmp_path):
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    browser_sheet = FileBrowserSheet(tmp_path, scanners=ScannerRegistry())
    session = Session(None, initial_sheet=browser_sheet)

    assert session.dataset_path is None

    _ = session.open_dataset_viewer(tmp_path / "data.csv")
    assert session.dataset_path == tmp_path / "data.csv"

    session._pop_viewer()
    assert session.dataset_path is None


def test_session_reload_viewer_preserves_stack(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("a\n1\n")
    browser_sheet = FileBrowserSheet(tmp_path, scanners=ScannerRegistry())
    session = Session(None, initial_sheet=browser_sheet)
    viewer = session.open_dataset_viewer(csv_path)
    stack_before = len(session.view_stack.viewers)

    session.reload_viewer(viewer)

    assert len(session.view_stack.viewers) == stack_before
    assert session.dataset_path == csv_path


def test_session_open_file_browser_defaults_to_dataset_dir(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    df = pl.DataFrame({"a": [1, 2]})
    dataset_path = workspace / "default.parquet"
    df.write_parquet(dataset_path)
    session = Session(str(dataset_path))

    session.open_file_browser()

    viewer = session.viewer
    assert isinstance(viewer.sheet, FileBrowserSheet)
    assert viewer.sheet.directory == workspace
    assert viewer.stack_depth == 0
    assert session.dataset_path is None
    assert viewer.status_message.endswith("entries")


def test_session_open_file_browser_allows_custom_directory(tmp_path):
    df = pl.DataFrame({"a": [1]})
    dataset_path = tmp_path / "custom.parquet"
    df.write_parquet(dataset_path)
    custom_dir = tmp_path / "other"
    custom_dir.mkdir()
    (custom_dir / "nested").mkdir()
    session = Session(str(dataset_path))

    session.open_file_browser(custom_dir)

    viewer = session.viewer
    assert isinstance(viewer.sheet, FileBrowserSheet)
    assert viewer.sheet.directory == custom_dir
    assert session.dataset_path is None
    assert viewer.status_message.endswith("entries")


def test_session_open_file_browser_requires_directory_when_unavailable():
    df = pl.DataFrame({"a": [1]}).lazy()
    session = Session(None, lazyframe=df)

    with pytest.raises(ValueError):
        session.open_file_browser()

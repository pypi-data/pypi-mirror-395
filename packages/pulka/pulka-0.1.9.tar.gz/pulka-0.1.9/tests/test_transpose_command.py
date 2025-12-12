import polars as pl

from pulka.api.session import Session
from pulka.command.registry import CommandContext
from pulka.core.viewer import Viewer, ViewStack
from pulka.sheets.data_sheet import DataSheet
from pulka_builtin_plugins.transpose.plugin import (
    TransposeSheet,
    _transpose_cmd,
    _transpose_current_row_cmd,
    open_transpose_viewer,
)


def test_transpose_command_freezes_columns_without_session(job_runner):
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    data_sheet = DataSheet(base_df.lazy(), runner=job_runner)
    viewer = Viewer(data_sheet, runner=job_runner)

    stack = ViewStack()
    stack.push(viewer)
    context = CommandContext(data_sheet, viewer, view_stack=stack)

    _transpose_cmd(context, [])

    assert len(stack.viewers) == 2
    derived_viewer = stack.active
    assert derived_viewer is context.viewer
    assert isinstance(derived_viewer.sheet, TransposeSheet)
    assert derived_viewer.stack_depth == 1
    assert derived_viewer.frozen_column_count == 2
    assert derived_viewer.frozen_columns[:2] == ["column", "dtype"]
    assert derived_viewer.columns[:2] == ["column", "dtype"]


def test_transpose_command_uses_session_helper(tmp_path) -> None:
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    path = tmp_path / "transpose.csv"
    base_df.write_csv(path)

    session = Session(str(path), viewport_rows=6)
    context = CommandContext(
        session.sheet,
        session.viewer,
        session=session,
        view_stack=session.view_stack,
    )

    _transpose_cmd(context, [])

    active_viewer = session.viewer
    assert isinstance(active_viewer.sheet, TransposeSheet)
    assert len(session.view_stack.viewers) == 2
    assert active_viewer is session.view_stack.active


def test_transpose_current_row_command_uses_cursor(job_runner) -> None:
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    data_sheet = DataSheet(base_df.lazy(), runner=job_runner)
    viewer = Viewer(data_sheet, runner=job_runner)
    viewer.cur_row = 1

    stack = ViewStack()
    stack.push(viewer)
    context = CommandContext(data_sheet, viewer, view_stack=stack)

    _transpose_current_row_cmd(context, [])

    derived_viewer = stack.active
    assert isinstance(derived_viewer.sheet, TransposeSheet)
    transpose_sheet = derived_viewer.sheet
    assert transpose_sheet.start_row == 1
    assert transpose_sheet.sample_rows == 1
    assert transpose_sheet.actual_sample_rows == 1
    assert derived_viewer.status_message == "transpose row 2"
    assert [col for col in transpose_sheet.data.columns if col.startswith("row_")] == ["row_2"]


def test_open_transpose_viewer_without_session_uses_view_stack(job_runner) -> None:
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    data_sheet = DataSheet(base_df.lazy(), runner=job_runner)
    viewer = Viewer(data_sheet, runner=job_runner)

    stack = ViewStack()
    stack.push(viewer)

    derived_viewer = open_transpose_viewer(viewer, view_stack=stack)

    assert derived_viewer is stack.active
    assert isinstance(derived_viewer.sheet, TransposeSheet)
    assert derived_viewer.frozen_column_count == 2


def test_open_transpose_viewer_with_session(tmp_path) -> None:
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    path = tmp_path / "transpose_helper.csv"
    base_df.write_csv(path)

    session = Session(str(path), viewport_rows=6)
    base_viewer = session.viewer

    derived_viewer = open_transpose_viewer(
        base_viewer,
        session=session,
        view_stack=session.view_stack,
    )

    assert derived_viewer is session.viewer
    assert derived_viewer is session.view_stack.active
    assert isinstance(derived_viewer.sheet, TransposeSheet)

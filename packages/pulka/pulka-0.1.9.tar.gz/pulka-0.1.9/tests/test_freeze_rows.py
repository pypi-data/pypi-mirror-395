"""Regression tests covering frozen row viewport behavior."""

from __future__ import annotations

import polars as pl

from pulka.core.viewer import Viewer
from pulka.sheets.data_sheet import DataSheet


def _make_viewer(
    *, rows: int = 128, frozen_rows: int = 2, viewport_rows: int = 12, runner=None
) -> Viewer:
    if runner is None:
        raise ValueError("runner fixture must be provided")
    df = pl.DataFrame({"value": list(range(rows))})
    sheet = DataSheet(df.lazy(), runner=runner)
    viewer = Viewer(sheet, viewport_rows=viewport_rows, runner=runner)
    if frozen_rows:
        viewer.set_frozen_rows(frozen_rows)
    return viewer


def test_frozen_rows_leave_margin_above_status_bar(job_runner) -> None:
    viewer = _make_viewer(frozen_rows=0, runner=job_runner)

    # Without any frozen rows the body height fills the table area.
    baseline = viewer.view_height
    assert viewer._body_view_height() == baseline

    viewer.set_frozen_rows(2)
    reserved = viewer._reserved_frozen_rows()
    body_height = viewer._body_view_height()

    # Reserving frozen rows should still leave a trailing margin for the status bar.
    assert body_height == max(1, viewer.view_height - reserved - 1)

    total_rows = len(viewer.sheet)
    viewer.cur_row = total_rows - 1
    viewer.row0 = total_rows
    viewer.clamp()

    # Populate the row cache so visible row positions reflect the current viewport.
    viewer.get_visible_table_slice(viewer.columns)
    positions = viewer.visible_row_positions
    frozen_visible = viewer.visible_frozen_row_count

    assert positions
    assert positions[-1] == total_rows - 1

    # The trailing margin ensures the last visible body row is one line above the status bar.
    assert len(positions) - frozen_visible <= body_height


def test_frozen_rows_limit_body_rows_to_view_height(job_runner) -> None:
    viewer = _make_viewer(rows=256, frozen_rows=2, runner=job_runner)

    # Position the viewport so that the scrollable body is filled with data.
    body_height = viewer._body_view_height()
    viewer.row0 = viewer._reserved_frozen_rows()
    viewer.cur_row = viewer.row0 + body_height - 1
    viewer.clamp()

    viewer.get_visible_table_slice(viewer.columns)
    frozen_visible = viewer.visible_frozen_row_count
    positions = viewer.visible_row_positions

    assert positions
    assert frozen_visible > 0

    body_positions = positions[frozen_visible:]
    assert len(body_positions) == body_height

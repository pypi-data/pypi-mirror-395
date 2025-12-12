"""Tests for status bar row count caching."""

from __future__ import annotations

import time
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import polars as pl

from pulka.core.engine.contracts import TableSlice
from pulka.core.engine.polars_adapter import table_slice_from_dataframe
from pulka.core.plan import QueryPlan
from pulka.core.viewer import Viewer
from pulka.render.status_bar import render_status_line


def _status_text(viewer: Viewer) -> str:
    fragments = render_status_line(viewer, test_mode=True)
    assert isinstance(fragments, list)
    return "".join(part for _, part in fragments)


class CountingSheet:
    """Minimal sheet implementation that tracks __len__ calls."""

    def __init__(self) -> None:
        self.columns = ["value"]
        self.schema = {"value": pl.Int64}
        self._len_calls = 0
        self._plan = QueryPlan()

    def __len__(self) -> int:
        self._len_calls += 1
        return 128

    def fetch_slice(self, row_start: int, row_count: int, columns: list[str]) -> TableSlice:
        data = {}
        for name in columns:
            data[name] = list(range(row_start, row_start + row_count))
        df = pl.DataFrame(data)
        return table_slice_from_dataframe(df, self.schema)

    @property
    def plan(self) -> QueryPlan:
        return self._plan


class AsyncCountingSheet(CountingSheet):
    def __init__(self, *, force_async: bool = False) -> None:
        super().__init__()
        self.sheet_id = f"async-counting-{uuid4().hex}"
        self._generation = 0
        self._len_failures_remaining = 1 if force_async else 0

    def __len__(self) -> int:
        if self._len_failures_remaining > 0:
            self._len_failures_remaining -= 1
            raise RuntimeError("len() not available yet")
        return super().__len__()

    def job_context(self) -> tuple[str, int, str]:
        return (self.sheet_id, self._generation, "static")


class StatusBarViewerStub:
    def __init__(
        self,
        *,
        total_rows: int = 529,
        hidden: list[str] | None = None,
        visible_cols: list[str] | None = None,
        sheet: Any | None = None,
    ) -> None:
        self.columns = [f"col_{idx}" for idx in range(4)]
        self.hidden_columns = list(hidden or [])
        hidden_set = set(self.hidden_columns)

        visible_source = self.columns[1:3] if visible_cols is None else list(visible_cols)

        filtered_visible = [col for col in visible_source if col not in hidden_set]
        if not filtered_visible:
            filtered_visible = [col for col in self.columns if col not in hidden_set]
        self.visible_cols = filtered_visible

        self.cur_col = 0
        self.cur_row = 0
        self._total_rows = total_rows
        self._row_count_stale = False
        self._row_count_future = None
        self._row_count_display_pending = False
        self.stack_depth = 0
        self.view_width_chars = 80
        self.schema = dict.fromkeys(self.columns, pl.Int64)
        self.sheet = sheet
        self.filter_text = None
        self.sort_col = None
        self.sort_asc = True
        self.status_message = None


def test_status_bar_row_count_cached_between_renders(job_runner):
    sheet = CountingSheet()
    viewer = Viewer(sheet, runner=job_runner)

    assert sheet._len_calls == 0

    render_status_line(viewer, test_mode=True)
    assert sheet._len_calls == 1

    render_status_line(viewer, test_mode=True)
    assert sheet._len_calls == 1

    viewer.invalidate_row_count()
    render_status_line(viewer, test_mode=True)
    assert sheet._len_calls == 2


def test_status_bar_updates_after_background_row_count_completion(job_runner):
    sheet = AsyncCountingSheet(force_async=True)
    viewer = Viewer(sheet, runner=job_runner)

    pending_status = _status_text(viewer)
    assert "≈" in pending_status

    future = viewer._row_count_future
    assert future is not None

    future.result(timeout=2)

    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline:
        if viewer._total_rows == 128 and viewer._row_count_future is None:
            break
        time.sleep(0.01)
    else:
        raise AssertionError("row count result was not applied")

    # Re-render once the cached count is available.
    updated_status = _status_text(viewer)
    assert "128" in updated_status
    assert "≈" not in updated_status

    viewer.job_runner.invalidate_sheet(sheet.sheet_id)


def test_status_bar_uses_len_for_async_sheet(job_runner):
    sheet = AsyncCountingSheet()
    viewer = Viewer(sheet, runner=job_runner)

    # First render triggers the synchronous len() path but still shows pending state.
    status_line = _status_text(viewer)
    assert viewer._row_count_future is None

    status_line = _status_text(viewer)

    assert "128" in status_line
    assert "≈" not in status_line


def test_status_bar_hides_sort_metadata(job_runner):
    sheet = CountingSheet()
    viewer = Viewer(sheet, runner=job_runner)

    sheet._plan = QueryPlan(sort=(("value", False),))
    viewer.status_message = "sort value ↑"

    status_line = _status_text(viewer)

    assert "S: value (↑)" not in status_line
    assert "sort value ↑" not in status_line


def test_status_bar_shows_sort_errors(job_runner):
    sheet = CountingSheet()
    viewer = Viewer(sheet, runner=job_runner)

    viewer.status_message = "sort error: boom"

    status_line = _status_text(viewer)

    assert "sort error: boom" in status_line


def test_status_bar_deduplicates_filter_status_message(job_runner):
    sheet = CountingSheet()
    sheet._plan = QueryPlan(filters=("value > 10",))
    viewer = Viewer(sheet, runner=job_runner)

    viewer.status_message = "filter: value > 10"

    status_line = _status_text(viewer)

    assert "F: value > 10" in status_line
    assert "filter: value > 10" not in status_line


def test_status_bar_deduplicates_sql_filter_status_message(job_runner):
    sheet = CountingSheet()
    sheet._plan = QueryPlan(sql_filter="value > 10")
    viewer = Viewer(sheet, runner=job_runner)

    viewer.status_message = "value > 10"

    status_line = _status_text(viewer)

    assert "F: SQL WHERE value > 10" in status_line
    assert status_line.count("value > 10") == 2


def test_status_bar_reports_total_column_count_not_visible_subset():
    stub = StatusBarViewerStub()
    status_line = "".join(part for _, part in render_status_line(stub, test_mode=True))

    assert "529×4" in status_line
    assert "529×2" not in status_line


def test_status_bar_excludes_hidden_columns_from_shape():
    stub = StatusBarViewerStub(hidden=["col_0"])
    status_line = "".join(part for _, part in render_status_line(stub, test_mode=True))

    assert "529×3" in status_line
    assert "529×4" not in status_line


def test_status_bar_shows_browser_path_instead_of_row_info():
    sheet = SimpleNamespace(
        is_file_browser=True,
        display_path="/tmp/data",
        directory="/tmp/data",
        sheet_id="file-browser:/tmp/data",
    )
    stub = StatusBarViewerStub(sheet=sheet)

    status_line = "".join(part for _, part in render_status_line(stub, test_mode=True))

    assert "/tmp/data" in status_line
    assert "row " not in status_line


def test_status_bar_truncates_browser_path_with_middle_ellipsis():
    long_path = "/very/long/path/that/should/be/truncated/in/the/middle/when/rendered"
    sheet = SimpleNamespace(
        is_file_browser=True,
        display_path=long_path,
        directory=long_path,
        sheet_id=f"file-browser:{long_path}",
    )
    stub = StatusBarViewerStub(sheet=sheet)
    stub.view_width_chars = 60

    status_line = "".join(part for _, part in render_status_line(stub, test_mode=True))

    assert "…" in status_line
    assert long_path[:8] in status_line
    assert long_path[-8:] in status_line

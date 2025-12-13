from __future__ import annotations

from concurrent.futures import Future
from datetime import date, datetime, timedelta
from decimal import Decimal

import polars as pl
import pytest

from pulka.api.runtime import Runtime
from pulka.api.session import Session
from pulka.command.registry import CommandContext
from pulka.core.formatting import (
    _one_line_repr,
    _simplify_dtype_text,
    _supports_min_max,
    _supports_numeric_stats,
)
from pulka.core.viewer import Viewer, ViewStack
from pulka.derived import build_column_summary_lazy
from pulka.sheets.data_sheet import DataSheet
from pulka.tui.screen import Screen
from pulka_builtin_plugins.summary.plugin import (
    SummarySheet,
    _parquet_metadata_summary_df,
    _pending_summary_df,
    _ProgressiveCsvSummaryJob,
    _summary_cmd,
    _SummaryUiHandle,
    compute_summary_df,
)


def make_data_sheet(lazy_frame, runner):
    return DataSheet(lazy_frame, runner=runner), runner


def _build_all_types_df() -> pl.DataFrame:
    """Create a compact DataFrame that hits all major Polars dtypes."""
    base = pl.DataFrame(
        {
            "int_col": [1, None, 3],
            "float_col": [1.5, 2.5, None],
            "bool_col": [True, False, None],
            "string_col": ["apple", None, "banana"],
            "date_col": [date(2024, 1, 1), date(2024, 1, 2), None],
            "datetime_col": [
                datetime(2024, 1, 1, 12, 0),
                None,
                datetime(2024, 1, 3, 18, 30),
            ],
            "duration_col": [timedelta(hours=1), timedelta(hours=2), None],
        }
    )

    cat_series = pl.Series("categorical_col", ["low", "medium", None], dtype=pl.Categorical)
    decimal_series = pl.Series(
        "decimal_col",
        [Decimal("1.23"), Decimal("4.56"), None],
        dtype=pl.Decimal(6, 2),
    )
    binary_series = pl.Series("binary_col", [b"aa", None, b"bbb"], dtype=pl.Binary)

    return base.with_columns([cat_series, decimal_series, binary_series])


def _expected_summary(df: pl.DataFrame) -> dict[str, dict[str, object]]:
    """Derive the expected summary metrics for each column."""
    rows = df.height
    expected: dict[str, dict[str, object]] = {}

    for name in df.columns:
        series = df.get_column(name)
        dtype = series.dtype
        nulls = int(series.null_count())
        non_nulls = rows - nulls
        unique = int(series.n_unique())

        clean = series.drop_nulls()
        modes = clean.mode().sort() if not clean.is_empty() else pl.Series([])
        mode = _one_line_repr(modes[0]) if modes.len() else ""

        min_str = max_str = ""
        if non_nulls and _supports_min_max(dtype):
            min_str = _one_line_repr(series.min())
            max_str = _one_line_repr(series.max())

        mean = std = median = None
        if non_nulls and _supports_numeric_stats(dtype):
            numeric = series.cast(pl.Float64, strict=False)
            mean_val = numeric.mean()
            std_val = numeric.std()
            median_val = numeric.median()
            mean = float(mean_val) if mean_val is not None else None
            std = float(std_val) if std_val is not None else None
            median = float(median_val) if median_val is not None else None

        expected[name] = {
            "dtype": _simplify_dtype_text(dtype),
            "mode": mode,
            "rows": rows,
            "non_nulls": non_nulls,
            "non_null_percent": (non_nulls / rows * 100) if rows else None,
            "nulls": nulls,
            "null_percent": (nulls / rows * 100) if rows else None,
            "unique": unique,
            "unique_percent": (unique / rows * 100) if rows else None,
            "min": min_str,
            "max": max_str,
            "mean": mean,
            "std": std,
            "median": median,
        }

    return expected


def test_summary_command_covers_all_dtypes(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    df = _build_all_types_df()
    path = tmp_path / "all_types.parquet"
    df.write_parquet(path)

    session = Session(str(path), viewport_rows=6, viewport_cols=6)
    summary_df = build_column_summary_lazy(session.viewer).collect()
    summary_dict = summary_df.to_dict(as_series=False)

    actual: dict[str, dict[str, object]] = {}
    for idx, col_name in enumerate(summary_dict["column"]):
        actual[col_name] = {key: summary_dict[key][idx] for key in summary_dict if key != "column"}

    expected = _expected_summary(pl.read_parquet(path))

    assert set(actual) == set(expected), "Summary should include every column"

    for column, expected_metrics in expected.items():
        actual_metrics = actual[column]

        assert actual_metrics["dtype"] == expected_metrics["dtype"]
        assert actual_metrics["mode"] == expected_metrics["mode"]
        assert actual_metrics["rows"] == expected_metrics["rows"]
        assert actual_metrics["non_nulls"] == expected_metrics["non_nulls"]
        assert actual_metrics["nulls"] == expected_metrics["nulls"]
        assert actual_metrics["unique"] == expected_metrics["unique"]

        for key in ("non_null_percent", "null_percent", "unique_percent", "mean", "std", "median"):
            expected_value = expected_metrics[key]
            actual_value = actual_metrics[key]
            if expected_value is None:
                assert actual_value is None
            else:
                assert actual_value == pytest.approx(expected_value, rel=1e-9, abs=1e-9)

        for key in ("min", "max"):
            assert actual_metrics[key] == expected_metrics[key]


def test_summary_placeholder_preserves_base_sheet_jobs(monkeypatch, job_runner):
    base_df = pl.DataFrame({"a": [1, 2, 3]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    viewer = Viewer(data_sheet, runner=runner)

    calls: list[str] = []

    def _record(sheet_id: str) -> None:
        calls.append(sheet_id)

    monkeypatch.setattr(runner, "invalidate_sheet", _record)

    placeholder_df = _pending_summary_df()
    placeholder = SummarySheet.from_dataframe(data_sheet, placeholder_df)
    viewer.replace_sheet(placeholder)

    assert calls == []


def test_summary_command_freezes_first_two_columns(job_runner):
    base_df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    viewer = Viewer(data_sheet, runner=runner)

    stack = ViewStack()
    stack.push(viewer)
    context = CommandContext(data_sheet, viewer, view_stack=stack)

    _summary_cmd(context, [])

    assert isinstance(viewer.sheet, SummarySheet)
    assert viewer.status_message == "summary view"
    assert viewer.frozen_column_count == 2
    assert viewer.frozen_columns[:2] == ["column", "dtype"]


def test_parquet_metadata_summary_uses_file_statistics(tmp_path):
    df = pl.DataFrame(
        {
            "numbers": [1, None, 5, 3, None, 8],
            "letters": ["z", "m", None, "a", "q", "b"],
        }
    )
    path = tmp_path / "stats.parquet"
    df.write_parquet(path, row_group_size=2, statistics=True)

    schema = df.schema
    summary_df = _parquet_metadata_summary_df(
        str(path),
        list(df.columns),
        schema,
    )

    assert summary_df is not None

    summary_dict = summary_df.to_dict(as_series=False)
    expected = _expected_summary(df)

    for column in df.columns:
        idx = summary_dict["column"].index(column)
        metrics = {key: summary_dict[key][idx] for key in summary_dict if key != "column"}
        expected_metrics = expected[column]

        assert metrics["dtype"] == expected_metrics["dtype"]
        assert metrics["rows"] == expected_metrics["rows"]
        assert metrics["nulls"] == expected_metrics["nulls"]
        assert metrics["non_nulls"] == expected_metrics["non_nulls"]

        if expected_metrics["null_percent"] is None:
            assert metrics["null_percent"] is None
            assert metrics["non_null_percent"] is None
        else:
            assert metrics["null_percent"] == pytest.approx(
                expected_metrics["null_percent"], rel=1e-9, abs=1e-9
            )
            assert metrics["non_null_percent"] == pytest.approx(
                expected_metrics["non_null_percent"], rel=1e-9, abs=1e-9
            )

        assert metrics["min"] == expected_metrics["min"]
        assert metrics["max"] == expected_metrics["max"]

        # Deferred computations (mode + numeric stats) should remain empty in the metadata pass.
        assert metrics["mode"] == ""
        assert metrics["mean"] is None
        assert metrics["std"] is None
        assert metrics["median"] is None


class _DummyScreen:
    def __init__(self, viewer: Viewer, stack: ViewStack):
        self.viewer = viewer
        self.view_stack = stack
        self._jobs: dict[Viewer, object] = {}
        self.app = None
        self.refresh_calls = 0
        self._history: list[Viewer] = list(stack.viewers)
        self._unsubscribe = stack.add_active_viewer_listener(self._on_active_viewer_changed)

    def _on_active_viewer_changed(self, viewer: Viewer) -> None:
        self.viewer = viewer
        self._history = list(self.view_stack.viewers)

    def refresh(self, *, skip_metrics: bool = False) -> None:  # pragma: no cover - simple stub
        self.refresh_calls += 1


class _SummarySelectionScreen:
    def __init__(self, stack: ViewStack):
        self.view_stack = stack
        self.viewer = stack.active

    def _pop_viewer(self):
        removed = self.view_stack.pop()
        if self.view_stack.active is not None:
            self.viewer = self.view_stack.active
        return removed

    def refresh(self, *, skip_metrics: bool = False):
        _ = skip_metrics
        return None


def test_summary_command_pushes_new_viewer(monkeypatch, job_runner):
    base_df = pl.DataFrame({"a": [1, 2, 3]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    viewer = Viewer(data_sheet, runner=runner)
    stack = ViewStack()
    stack.push(viewer)

    screen = _DummyScreen(viewer, stack)

    future: Future = Future()
    future.set_result(None)

    monkeypatch.setattr(runner, "enqueue", lambda req: future)

    context = CommandContext(
        data_sheet,
        viewer,
        session=None,
        view_stack=stack,
    )
    context.screen = screen

    _summary_cmd(context, [])

    assert len(stack.viewers) == 2, "summary command should push a derived viewer"
    derived_viewer = screen.viewer
    assert derived_viewer is stack.active
    assert derived_viewer.stack_depth == 1
    assert isinstance(derived_viewer.sheet, SummarySheet)
    assert getattr(derived_viewer.sheet, "source_sheet", None) is data_sheet
    assert screen._jobs.get(derived_viewer) is not None
    assert context.viewer is derived_viewer


def test_summary_rows_use_column_names_for_selection(job_runner):
    base_df = pl.DataFrame({"alpha": [1, 2], "beta": [3, 4], "gamma": [5, 6]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    summary_sheet = SummarySheet(data_sheet, runner=runner)
    summary_viewer = Viewer(summary_sheet, runner=runner)

    summary_viewer.cur_row = 1
    summary_viewer.toggle_row_selection()

    assert summary_viewer._selected_row_ids == {"beta"}

    table_slice = summary_sheet.fetch_slice(0, 3, summary_sheet.columns)
    assert table_slice.row_ids is not None
    assert tuple(table_slice.row_ids) == tuple(base_df.columns)


def test_keep_columns_hides_non_selected(job_runner):
    base_df = pl.DataFrame({"a": [1], "b": [2], "c": [3]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    viewer = Viewer(data_sheet, runner=runner)

    viewer.keep_columns(["c", "a"])

    assert viewer.visible_columns() == ["a", "c"]
    assert set(viewer.hidden_columns) == {"b"}
    assert (viewer.status_message or "").startswith("Showing")
    assert viewer.sheet.plan.projection == ("a", "c")


def test_summary_enter_hides_non_selected_columns(job_runner):
    base_df = pl.DataFrame({"a": [1], "b": [2], "c": [3]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    base_viewer = Viewer(data_sheet, runner=runner)
    stack = ViewStack()
    stack.push(base_viewer)

    summary_sheet = SummarySheet(data_sheet, runner=runner)
    summary_viewer = Viewer(summary_sheet, runner=runner)
    stack.push(summary_viewer)

    screen = _SummarySelectionScreen(stack)

    summary_viewer.toggle_row_selection()
    summary_viewer.cur_row = 2
    summary_viewer.toggle_row_selection()

    handled = Screen._apply_summary_selection(screen)

    assert handled is True
    assert stack.active is base_viewer
    assert summary_viewer._selected_row_ids == set()
    assert base_viewer.visible_columns() == ["a", "c"]
    assert set(base_viewer.hidden_columns) == {"b"}
    assert (base_viewer.status_message or "").startswith("Showing")


def test_summary_handle_accepts_missing_screen(monkeypatch, job_runner):
    base_df = pl.DataFrame({"a": [1, 2, 3]})
    data_sheet, runner = make_data_sheet(base_df.lazy(), job_runner)
    viewer = Viewer(data_sheet, runner=runner)

    monkeypatch.setattr(
        "pulka_builtin_plugins.summary.plugin._SummaryUiHandle._spinner_frames",
        (),
        raising=False,
    )
    monkeypatch.setattr(
        "pulka_builtin_plugins.summary.plugin._SummaryUiHandle._spinner_interval_ns",
        0,
        raising=False,
    )
    monkeypatch.setattr(runner, "get", lambda sheet_id, tag: None)

    handle = _SummaryUiHandle(data_sheet.sheet_id, "tag", None, runner)
    handle.prime(viewer)

    assert viewer.status_message == "Computing column summary…"
    assert handle.consume_update(viewer) is False


def test_screen_tracks_view_stack(tmp_path):
    data_path = tmp_path / "summary.parquet"
    pl.DataFrame({"a": [1, 2, 3]}).write_parquet(data_path)

    runtime = Runtime(load_entry_points=False)
    session = runtime.open(str(data_path))
    screen = Screen(session.viewer)

    try:
        root_viewer = session.viewer
        stack = session.view_stack

        derived_viewer = Viewer(
            root_viewer.sheet,
            viewport_rows=root_viewer._viewport_rows_override,
            viewport_cols=root_viewer._viewport_cols_override,
            source_path=None,
            session=session,
            runner=root_viewer.job_runner,
        )

        stack.push(derived_viewer)
        assert screen.viewer is derived_viewer
        assert session.viewer is derived_viewer
        assert stack.active is derived_viewer

        stack.pop()
        assert screen.viewer is root_viewer
        assert session.viewer is root_viewer
        assert stack.active is root_viewer
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            unsubscribe()


def test_progressive_csv_pipeline_matches_eager_summary(tmp_path, job_runner):
    df = pl.DataFrame(
        {
            "numbers": [0, 1, 2, 2, 2, 2],
            "floats": [0.0, 1.0, 2.0, 2.0, 2.0, 2.0],
            "letters": ["alpha", "beta", "omega", "omega", "omega", "omega"],
        }
    )
    csv_path = tmp_path / "sample.csv"
    df.write_csv(csv_path)

    class _StubHandle:
        def notify_ready(self) -> None:  # pragma: no cover - stub
            pass

        def notify_refresh(self) -> None:  # pragma: no cover - stub
            pass

    job = _ProgressiveCsvSummaryJob(
        sheet_id="sheet",
        generation=1,
        tag="tag",
        handle=_StubHandle(),
        path=str(csv_path),
        columns=list(df.columns),
        ordered_schema=df.schema,
        sample_rows=2,
        auto_start=False,
        runner=job_runner,
    )

    update0 = job._run_sniff()
    assert update0.stage == "sniff"
    assert not update0.done

    update1 = job._run_sample()
    assert update1.stage == "sample"
    assert not update1.done

    update2 = job._run_stream()
    assert update2.stage == "stream"
    assert not update2.done

    update3 = job._run_heavy()
    assert update3.stage == "final"
    assert update3.done

    final_df = update3.frame
    expected_df = compute_summary_df(df.lazy(), df.schema)
    assert final_df.to_dict(as_series=False) == expected_df.to_dict(as_series=False)

"""Frequency sheet plugin."""

from __future__ import annotations

import contextlib
import weakref
from collections.abc import Sequence
from concurrent.futures import Future
from dataclasses import dataclass
from time import time_ns
from typing import TYPE_CHECKING

import polars as pl
from prompt_toolkit.eventloop import call_soon_threadsafe

from pulka.core.column_insight import LOW_CARDINALITY_NUMERIC_LIMIT
from pulka.core.engine.contracts import EnginePayloadHandle, TableColumn, TableSlice
from pulka.core.engine.polars_adapter import (
    PlanCompiler,
    make_lazyframe_handle,
    table_slice_from_dataframe,
    unwrap_lazyframe_handle,
)
from pulka.core.formatting import (
    _format_large_number_compact,
    _supports_histogram_stats,
)
from pulka.core.jobs import JobResult, JobRunner
from pulka.core.plan_ops import reset as reset_plan
from pulka.core.row_provider import RowProvider
from pulka.core.sheet import Sheet
from pulka.core.viewer import Viewer, ViewStack
from pulka.render.braille import FILL_CHAR, SPROUT_CHAR, render_hist_bar
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.hist_sheet import HistogramSheet

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from pulka.api.session import Session
    from pulka.command.registry import CommandContext, CommandRegistry
    from pulka.data.scanners import ScannerRegistry
    from pulka.sheets.registry import SheetRegistry
    from pulka.tui.screen import Screen

# Maximum number of distinct values for which we eagerly materialize the
# miniature bar chart. The previous limit of 100 prevented histograms from
# appearing for moderately sized categorical/temporal columns (for example the
# 128 distinct dates in ``all_polars_dtypes.parquet``), so we relax it while
# still keeping an upper bound to avoid generating huge string columns for
# massive frequency tables.
_SMALL_CARDINALITY_THRESHOLD = 1024


@dataclass(slots=True)
class FrequencyJobValue:
    frame: pl.DataFrame
    unique_count: int
    histogram_available: bool


def _empty_frequency_frame(column: str) -> pl.DataFrame:
    return pl.DataFrame(
        {
            column: pl.Series(column, [], dtype=pl.Utf8),
            "count": pl.Series("count", [], dtype=pl.Int64),
            "percent": pl.Series("percent", [], dtype=pl.Float64),
            "hist": pl.Series("hist", [], dtype=pl.Utf8),
        }
    )


def _build_frequency_frame(base_lf: pl.LazyFrame, colname: str) -> FrequencyJobValue:
    try:
        freq_df = (
            base_lf.select(pl.col(colname))
            .group_by(colname)
            .agg(pl.len().alias("count"))
            .sort("count", descending=True, nulls_last=True)
            .collect()
        )
    except BaseException:
        return FrequencyJobValue(_empty_frequency_frame(str(colname)), 0, False)

    total = int(freq_df["count"].sum()) if freq_df.height else 0
    if total > 0:
        freq_df = freq_df.with_columns(
            (pl.col("count").cast(pl.Float64) * 100.0 / total).alias("percent")
        )
    else:
        freq_df = freq_df.with_columns(pl.lit(0.0).alias("percent"))

    nlevels = freq_df.height
    histogram_available = False
    if nlevels and nlevels <= _SMALL_CARDINALITY_THRESHOLD:
        try:
            max_count = int(freq_df["count"].max())
        except Exception:
            max_count = None
        if max_count and max_count > 0:
            bar_width = 20
            bar_lengths = (
                (freq_df["count"].cast(pl.Float64) / max_count * bar_width)
                .round(0)
                .cast(pl.Int32)
                .clip(0, bar_width)
            ).to_list()

            counts = freq_df["count"].to_list()
            bars = []
            for count, length in zip(counts, bar_lengths, strict=False):
                bar_len = int(length)
                bar_len = max(0, min(bar_width, bar_len))
                if count > 0 and bar_len == 0:
                    bar = (SPROUT_CHAR + (" " * (bar_width - 1)))[:bar_width]
                else:
                    filled = FILL_CHAR * bar_len
                    padding = " " * max(0, bar_width - bar_len)
                    bar = (filled + padding)[:bar_width]
                bars.append(bar)

            freq_df = freq_df.with_columns(pl.Series("hist", bars))
            histogram_available = True
    else:
        freq_df = freq_df.with_columns(pl.Series("hist", ["" for _ in range(freq_df.height)]))

    return FrequencyJobValue(
        frame=freq_df,
        unique_count=int(nlevels),
        histogram_available=histogram_available,
    )


def _distinct_count(base_sheet: Sheet, column_name: str) -> int | None:
    base_lf_candidate = getattr(base_sheet, "lf", None)
    if base_lf_candidate is None:
        base_lf_candidate = getattr(base_sheet, "lf0", None)
    if base_lf_candidate is None:
        return None
    if isinstance(base_lf_candidate, EnginePayloadHandle):
        base_lf = unwrap_lazyframe_handle(base_lf_candidate)
    else:
        base_lf = base_lf_candidate
    try:
        result = base_lf.select(
            pl.col(column_name).drop_nulls().n_unique().alias("distinct")
        ).collect()
    except Exception:
        return None
    if result.is_empty():
        return 0
    try:
        return int(result["distinct"][0])
    except Exception:
        return None


class FreqSheet(DataSheet):
    """Sheet implementation for frequency tables backed by the job runner."""

    def __init__(
        self,
        base_sheet: Sheet,
        column_name: str,
        *,
        runner: JobRunner,
    ) -> None:
        placeholder = _empty_frequency_frame(column_name)
        if runner is None:  # pragma: no cover - defensive guard
            msg = "FreqSheet requires a JobRunner instance"
            raise ValueError(msg)
        super().__init__(placeholder.lazy(), runner=runner)

        self.source_sheet = base_sheet
        self.freq_column = column_name
        self.unique_value_count: int = 0
        self.histogram_available: bool = False
        self._display_df: pl.DataFrame = placeholder
        self._result_ts: int = 0
        self._pending_future: Future[JobResult] | None = None
        self._cache_version: int = 0
        self._hist_max_count: int = 0
        self._job_sheet_id = getattr(base_sheet, "sheet_id", None)
        self._job_tag = f"freq:{column_name}:auto"
        self._preserve_jobs_from = self._job_sheet_id
        self._handle_ref: weakref.ReferenceType[_FrequencyUiHandle] | None = None
        self.compact_width_layout = False

        # Frequency sheets always serve cached rows from the in-memory frame, so
        # bypass the default plan-based provider to avoid compiling placeholder
        # plans that never produce data.
        self._row_provider = RowProvider.for_sheet(self, runner=runner)

        cached = self._refresh_from_cache()
        if not cached:
            self._ensure_job()

    # Sheet protocol overrides ----------------------------------------

    @property
    def cache_version(self) -> int:
        return self._cache_version

    def job_context(self) -> tuple[str, int, str]:
        source_context = getattr(self.source_sheet, "job_context", None)
        if callable(source_context):
            sheet_id, generation, _ = source_context()
            return (sheet_id, generation, f"freq:{self.freq_column}")
        return super().job_context()

    def __len__(self) -> int:  # pragma: no cover - simple delegation
        self._refresh_from_cache()
        return int(self._display_df.height)

    def fetch_slice(self, row_start: int, row_count: int, columns: Sequence[str]) -> TableSlice:
        self._refresh_from_cache()
        return self._materialize_slice(row_start, row_count, columns)

    def get_value_at(self, row_index: int, column_name: str | None = None) -> object:
        self._refresh_from_cache()
        if column_name is None:
            column_name = self.columns[0]
        if column_name not in self.columns:
            raise KeyError(column_name)
        if row_index < 0 or row_index >= self._display_df.height:
            raise IndexError(row_index)
        return self._display_df[column_name][row_index]

    def row_provider_config(self) -> dict[str, object]:
        """Serve cached frequency rows directly without compiling plans."""

        return {
            "fetcher": self._display_slice_fetcher,
            "job_context": self.job_context,
            "empty_result_factory": self._empty_result,
        }

    # Internal helpers -------------------------------------------------

    def _materialize_slice(
        self,
        row_start: int,
        row_count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        requested = list(columns) if columns else list(self.columns)
        available = [col for col in requested if col in self.columns]
        if not available:
            return TableSlice.empty(requested, self.schema)
        sliced = self._display_df.select(available).slice(row_start, row_count)
        table_slice = table_slice_from_dataframe(sliced, sliced.schema)
        if self.freq_column in sliced.columns:
            try:
                table_slice.row_ids = tuple(sliced.get_column(self.freq_column).to_list())
            except Exception:
                table_slice.row_ids = None
        if "hist" in available:
            table_slice = self._with_hist_display(table_slice, sliced, available)
        return table_slice

    @property
    def preferred_fill_column(self) -> str | None:
        return "hist" if "hist" in self.columns else None

    def _display_slice_fetcher(
        self,
        row_start: int,
        row_count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        self._refresh_from_cache()
        return self._materialize_slice(row_start, row_count, columns)

    def _with_hist_display(
        self,
        table_slice: TableSlice,
        sliced_df: pl.DataFrame,
        visible_columns: Sequence[str],
    ) -> TableSlice:
        """Attach a width-aware display function for histogram bars."""

        if not self.histogram_available:
            return table_slice

        try:
            hist_idx = list(visible_columns).index("hist")
        except ValueError:
            return table_slice

        if "count" in sliced_df.columns:
            try:
                counts = sliced_df.get_column("count").to_list()
            except Exception:
                counts = [0 for _ in range(len(sliced_df))]
        else:
            counts = [0 for _ in range(len(sliced_df))]

        max_count = self._hist_max_count if self._hist_max_count else max(counts or [0])
        hist_series = sliced_df.get_column("hist")
        dtype = hist_series.dtype
        null_count = int(hist_series.null_count())

        def _display_hist(row: int, _abs_row: int, _value: object, width: int | None) -> str:
            target_width = 0 if width is None else max(0, int(width))
            count_val = counts[row] if 0 <= row < len(counts) else 0
            return render_hist_bar(count_val, max_count, target_width)

        columns = list(table_slice.columns)
        columns[hist_idx] = TableColumn("hist", hist_series, dtype, null_count, _display_hist)
        return TableSlice(
            tuple(columns),
            table_slice.schema,
            table_slice.start_offset,
            table_slice.row_ids,
        )

    def _ensure_job(self, force: bool = False) -> None:
        if self._job_sheet_id is None:
            return
        if not force and self._pending_future is not None and not self._pending_future.done():
            return

        base_lf_candidate = getattr(self.source_sheet, "lf", None)
        if base_lf_candidate is None:
            base_lf_candidate = getattr(self.source_sheet, "lf0", None)
        if base_lf_candidate is None:
            return
        if isinstance(base_lf_candidate, EnginePayloadHandle):
            base_lf = unwrap_lazyframe_handle(base_lf_candidate)
        else:
            base_lf = base_lf_candidate

        def _compute(
            _: int,
            lf: pl.LazyFrame = base_lf,
            col: str = self.freq_column,
        ) -> FrequencyJobValue:
            return _build_frequency_frame(lf, col)

        runner = self.job_runner
        future = runner.submit(self.source_sheet, self._job_tag, _compute)
        self._pending_future = future
        self._attach_future_callback(future)

    def _refresh_from_cache(self) -> bool:
        if self._job_sheet_id is None:
            return False
        result = self.job_runner.get(self._job_sheet_id, self._job_tag)
        if result is None:
            return False
        if isinstance(result, JobResult) and result.error is not None:
            return False
        if isinstance(result, JobResult):
            if result.ts_ns <= self._result_ts:
                return True
            value = result.value
            ts_ns = result.ts_ns
        else:
            value = result
            ts_ns = time_ns()

        if not isinstance(value, FrequencyJobValue):
            return False

        self._apply_result(value, ts_ns)
        return True

    def _apply_result(self, payload: FrequencyJobValue, ts_ns: int) -> None:
        self._display_df = payload.frame
        lazy_display = self._display_df.lazy()
        self.lf0 = make_lazyframe_handle(lazy_display)
        try:
            self.schema = lazy_display.collect_schema()
        except Exception:
            self.schema = self._display_df.schema
        self.columns = list(self.schema.keys())
        self._compiler = PlanCompiler(
            lazy_display,
            columns=self.columns,
            schema=self.schema,
            sql_executor=self._sql_executor,
        )
        self._update_plan(reset_plan())
        self.unique_value_count = payload.unique_count
        self.histogram_available = payload.histogram_available
        if self._display_df.height:
            try:
                self._hist_max_count = int(self._display_df["count"].max())
            except Exception:
                self._hist_max_count = 0
        else:
            self._hist_max_count = 0
        self._result_ts = ts_ns
        self._cache_version += 1
        self._pending_future = None
        provider = getattr(self, "_row_provider", None)
        if provider is not None:
            with contextlib.suppress(Exception):
                provider.clear()

    def attach_ui_handle(self, handle: _FrequencyUiHandle) -> None:
        """Attach ``handle`` so UI refreshes when background jobs finish."""

        self._handle_ref = weakref.ref(handle)
        future = self._pending_future
        if future is not None:
            future.add_done_callback(handle.notify_ready)

    def detach_ui_handle(self, handle: _FrequencyUiHandle) -> None:
        """Detach ``handle`` when it is no longer active."""

        if self._handle_ref is None:
            return
        current = self._handle_ref()
        if current is handle:
            self._handle_ref = None

    def _attach_future_callback(self, future: Future[JobResult]) -> None:
        handle_ref = self._handle_ref
        if handle_ref is None:
            return
        handle = handle_ref()
        if handle is None:
            return
        future.add_done_callback(handle.notify_ready)


def _format_freq_status_message(freq_sheet: FreqSheet, column_name: str) -> str:
    """Return the status message for ``freq_sheet``."""

    freq_sheet._refresh_from_cache()
    if not freq_sheet.histogram_available and freq_sheet.unique_value_count:
        formatted_count = _format_large_number_compact(freq_sheet.unique_value_count)
        return f"High cardinality: {formatted_count} unique values"
    return f"frequency table: {column_name}"


def _activate_derived_viewer(
    base_viewer: Viewer,
    derived_viewer: Viewer,
    *,
    view_stack: ViewStack | None,
) -> Viewer:
    """Push ``derived_viewer`` onto ``view_stack`` or replace ``base_viewer``."""

    if view_stack is not None:
        view_stack.push(derived_viewer)
        return view_stack.active or derived_viewer

    base_viewer.replace_sheet(derived_viewer.sheet, source_path=None)
    base_viewer.is_freq_view = getattr(derived_viewer, "is_freq_view", False)
    base_viewer.is_hist_view = getattr(derived_viewer, "is_hist_view", False)
    base_viewer.freq_source_col = getattr(derived_viewer, "freq_source_col", None)
    base_viewer.status_message = getattr(derived_viewer, "status_message", None)
    return base_viewer


def open_frequency_viewer(
    base_viewer: Viewer,
    column_name: str,
    *,
    session: Session | None = None,
    view_stack: ViewStack | None = None,
    screen: Screen | None = None,
) -> Viewer:
    """Open a frequency or histogram view derived from ``base_viewer``."""

    schema = getattr(base_viewer, "schema", None) or getattr(base_viewer.sheet, "schema", {})
    dtype = schema.get(column_name)
    histogram_capable = dtype is not None and _supports_histogram_stats(dtype)
    distinct_count: int | None = None
    force_categorical = False
    if histogram_capable:
        distinct_count = _distinct_count(base_viewer.sheet, column_name)
    if distinct_count is not None and distinct_count <= LOW_CARDINALITY_NUMERIC_LIMIT:
        force_categorical = True

    preferred_height = getattr(base_viewer, "view_height", None)
    preferred_width = getattr(base_viewer, "view_width_chars", None)
    viewer_options = {"source_path": None}

    helper = getattr(session, "open_sheet_view", None) if session is not None else None
    if callable(helper):
        if histogram_capable and not force_categorical:
            derived_viewer = helper(
                "histogram",
                base_viewer=base_viewer,
                viewer_options=viewer_options,
                column_name=column_name,
                preferred_height=preferred_height,
                preferred_width=preferred_width,
                dtype=dtype,
            )
            derived_viewer.is_hist_view = True
            derived_viewer.freq_source_col = column_name
            derived_viewer.status_message = None
            with contextlib.suppress(Exception):
                derived_viewer.invalidate_row_count()
            return derived_viewer

        derived_viewer = helper(
            "freq",
            base_viewer=base_viewer,
            viewer_options=viewer_options,
            column_name=column_name,
        )
        derived_viewer.is_freq_view = True
        derived_viewer.freq_source_col = column_name
        freq_sheet = derived_viewer.sheet
        register_frequency_ui_handle(freq_sheet, derived_viewer, screen)
        derived_viewer.status_message = _format_freq_status_message(freq_sheet, column_name)
        return derived_viewer

    if histogram_capable and not force_categorical:
        hist_sheet = HistogramSheet(
            base_viewer.sheet,
            column_name,
            preferred_height=preferred_height,
            preferred_width=preferred_width,
            runner=base_viewer.job_runner,
            dtype=dtype,
        )
        derived_viewer = Viewer(
            hist_sheet,
            viewport_rows=base_viewer._viewport_rows_override,
            viewport_cols=base_viewer._viewport_cols_override,
            source_path=None,
            session=session,
            runner=base_viewer.job_runner,
        )
        derived_viewer.is_hist_view = True
        derived_viewer.freq_source_col = column_name
        derived_viewer.status_message = None
        with contextlib.suppress(Exception):
            derived_viewer.invalidate_row_count()
        return _activate_derived_viewer(base_viewer, derived_viewer, view_stack=view_stack)

    freq_sheet = FreqSheet(
        base_viewer.sheet,
        column_name,
        runner=base_viewer.job_runner,
    )
    derived_viewer = Viewer(
        freq_sheet,
        viewport_rows=base_viewer._viewport_rows_override,
        viewport_cols=base_viewer._viewport_cols_override,
        source_path=None,
        session=session,
        runner=base_viewer.job_runner,
    )
    derived_viewer.is_freq_view = True
    derived_viewer.freq_source_col = column_name
    active_viewer = _activate_derived_viewer(base_viewer, derived_viewer, view_stack=view_stack)
    register_frequency_ui_handle(freq_sheet, active_viewer, screen)
    active_viewer.status_message = _format_freq_status_message(freq_sheet, column_name)
    return active_viewer


def _freq_cmd(context: CommandContext, args: list[str]) -> None:
    if not context.viewer.columns:
        context.viewer.status_message = "no columns available"
        return

    if args and args[0]:
        col_name = args[0]
        if col_name not in context.viewer.columns:
            context.viewer.status_message = f"unknown column: {col_name}"
            return
    else:
        col_name = context.viewer.columns[context.viewer.cur_col]

    session = getattr(context, "session", None) or context.viewer.session
    screen = getattr(context, "screen", None)
    view_stack = getattr(context, "view_stack", None)
    if view_stack is None and session is not None:
        view_stack = getattr(session, "view_stack", None)
    try:
        derived_viewer = open_frequency_viewer(
            context.viewer,
            col_name,
            session=session,
            view_stack=view_stack,
            screen=screen,
        )
        context.viewer = derived_viewer
        context.sheet = derived_viewer.sheet
    except Exception as exc:  # pragma: no cover - guardrail
        context.viewer.status_message = f"freq error: {exc}"[:120]


def register(
    *,
    commands: CommandRegistry | None = None,
    sheets: SheetRegistry | None = None,
    scanners: ScannerRegistry | None = None,
) -> None:
    if sheets is not None:
        kinds = set(sheets.list_kinds())
        if "freq" not in kinds:
            sheets.register_sheet("freq", FreqSheet)
        if "histogram" not in kinds:
            sheets.register_sheet("histogram", HistogramSheet)

    if commands is not None:
        commands.register("freq", _freq_cmd, "Frequency table of current column", -1)
        commands.register_alias("F", "freq")

        def _open_freq(context: CommandContext) -> None:
            _freq_cmd(context, [])

        commands.register_sheet_opener("freq", _open_freq)

    _ = scanners


class _FrequencyUiHandle:
    """Polls the job runner for frequency results and refreshes the viewer."""

    def __init__(self, sheet: FreqSheet, screen: Screen | None) -> None:
        self._sheet_ref: weakref.ReferenceType[FreqSheet] | None = weakref.ref(sheet)
        self._screen_ref: weakref.ReferenceType[Screen] | None = (
            weakref.ref(screen) if screen is not None else None
        )
        self._last_result_ts: int = getattr(sheet, "_result_ts", 0)
        self._finished = False

    def _invalidate_screen(self) -> None:
        screen_ref = self._screen_ref
        if screen_ref is None:
            return
        screen = screen_ref()
        if screen is None:
            return
        app = getattr(screen, "app", None)
        if app is None:
            return
        try:
            call_soon_threadsafe(app.invalidate)
        except Exception:
            with contextlib.suppress(Exception):
                app.invalidate()

    def notify_ready(self, _future: Future[JobResult] | None = None) -> None:
        """Request a UI refresh when the background job finishes."""

        self._invalidate_screen()

    def consume_update(self, viewer: Viewer) -> bool:
        sheet = self._sheet_ref() if self._sheet_ref is not None else None
        if sheet is None or viewer.sheet is not sheet:
            self._finished = True
            return True

        sheet_id = getattr(sheet, "_job_sheet_id", None)
        tag = getattr(sheet, "_job_tag", None)
        if sheet_id is None or tag is None:
            self._finished = True
            sheet.detach_ui_handle(self)
            return True

        result = sheet.job_runner.get(sheet_id, tag)
        pending = sheet._pending_future
        if result is None or result.ts_ns <= self._last_result_ts:
            if pending is None:
                self._finished = True
                sheet.detach_ui_handle(self)
                return True
            return False

        self._last_result_ts = result.ts_ns

        if result.error is not None:
            viewer.status_message = f"freq error: {result.error!s}"[:120]
            self._finished = True
            sheet.detach_ui_handle(self)
            return True

        value = result.value
        if not isinstance(value, FrequencyJobValue):
            viewer.status_message = "frequency unavailable"
            self._finished = True
            sheet.detach_ui_handle(self)
            return True

        sheet._apply_result(value, result.ts_ns)
        viewer.invalidate_row_cache()
        viewer.invalidate_row_count()
        viewer.status_message = _format_freq_status_message(sheet, sheet.freq_column)
        self._finished = True
        sheet.detach_ui_handle(self)
        return True

    def cancel(self) -> None:
        self._finished = True
        sheet = self._sheet_ref() if self._sheet_ref is not None else None
        if sheet is not None:
            sheet.detach_ui_handle(self)
        self._sheet_ref = None
        self._screen_ref = None


def register_frequency_ui_handle(
    freq_sheet: FreqSheet,
    viewer: Viewer,
    screen: Screen | None,
) -> None:
    """Register a UI handle so the table refreshes when data is ready."""

    if screen is None:
        return

    handle = _FrequencyUiHandle(freq_sheet, screen)
    freq_sheet.attach_ui_handle(handle)
    screen._jobs[viewer] = handle
    if freq_sheet._pending_future is None:
        handle.notify_ready()

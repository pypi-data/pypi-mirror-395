"""Summary sheet plugin."""

from __future__ import annotations

import contextlib
import csv
import math
import weakref
from collections.abc import Mapping, Sequence
from concurrent.futures import Future
from dataclasses import dataclass, field
from pathlib import Path
from threading import Timer
from time import monotonic_ns
from typing import TYPE_CHECKING, Any, Literal

import polars as pl
from prompt_toolkit.eventloop import call_soon_threadsafe
from rich.spinner import SPINNERS

from pulka.core.engine.contracts import EnginePayloadHandle, TableSlice
from pulka.core.engine.polars_adapter import unwrap_lazyframe_handle
from pulka.core.formatting import (
    _is_nested_dtype,
    _one_line_repr,
    _simplify_dtype_text,
    _supports_min_max,
    _supports_numeric_stats,
)
from pulka.core.jobs import JobRequest, JobRunner
from pulka.core.plan import QueryPlan
from pulka.core.row_identity import ROW_ID_COLUMN
from pulka.core.sheet import Sheet
from pulka.core.viewer import Viewer
from pulka.data.scan import CSV_INFER_ROWS
from pulka.sheets.data_sheet import DataSheet

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from pulka.command.registry import CommandContext, CommandRegistry
    from pulka.core.viewer import Viewer
    from pulka.data.scanners import ScannerRegistry
    from pulka.sheets.registry import SheetRegistry
    from pulka.tui.screen import Screen


_SUMMARY_FIELD_SCHEMA: dict[str, pl.DataType] = {
    "column": pl.Utf8,
    "dtype": pl.Utf8,
    "mode": pl.Utf8,
    "rows": pl.Int64,
    "non_nulls": pl.Int64,
    "non_null_percent": pl.Float64,
    "nulls": pl.Int64,
    "null_percent": pl.Float64,
    "unique": pl.Int64,
    "unique_percent": pl.Float64,
    "min": pl.Utf8,
    "max": pl.Utf8,
    "mean": pl.Float64,
    "std": pl.Float64,
    "median": pl.Float64,
}

_SUMMARY_DISPLAY_FIELDS: tuple[str, ...] = ("mode", "min", "max")

_SUMMARY_FROZEN_COLUMNS = 2
_SUMMARY_MODE_SAMPLE_SIZE = 20_000


def _empty_summary_record(column: str, dtype: str) -> dict[str, Any]:
    record = dict.fromkeys(_SUMMARY_FIELD_SCHEMA, None)
    record["column"] = column
    record["dtype"] = dtype
    return record


def _init_column_summary_records(
    columns: list[str], schema: Mapping[str, pl.DataType]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in columns:
        dtype = schema.get(name, "unknown")
        records.append(_empty_summary_record(name, _simplify_dtype_text(dtype)))
    return records


def _summary_records_to_df(records: list[dict[str, Any]]) -> pl.DataFrame:
    if not records:
        return pl.DataFrame(
            {name: [] for name in _SUMMARY_FIELD_SCHEMA},
            schema=_SUMMARY_FIELD_SCHEMA,
        )

    def _stringify(value: Any) -> str:
        if value is None:
            return ""
        return _one_line_repr(value, max_items=4, max_chars=80)

    data: dict[str, list[Any]] = {name: [] for name in _SUMMARY_FIELD_SCHEMA}
    for rec in records:
        for name in data:
            value = rec.get(name)
            if name in _SUMMARY_DISPLAY_FIELDS:
                data[name].append(_stringify(value))
            else:
                data[name].append(value)

    return pl.DataFrame(data, schema=_SUMMARY_FIELD_SCHEMA)


_CSV_SNIFF_BYTES = 64 * 1024
_CSV_STAGE3_ROW_THRESHOLD = 200_000

StageName = Literal["sniff", "sample", "stream", "final"]


@dataclass(slots=True)
class SummaryProgressUpdate:
    """Incremental update emitted by the progressive summary pipeline."""

    frame: pl.DataFrame
    done: bool
    stage: StageName
    message: str | None = None


@dataclass(slots=True)
class _CsvSummaryState:
    path: Path
    ordered_schema: dict[str, pl.DataType]
    columns: list[str] = field(default_factory=list)
    delimiter: str = ","
    quote_char: str = '"'
    encoding: str = "utf8"
    records: list[dict[str, Any]] = field(default_factory=list)
    inferred_schema: dict[str, pl.DataType] = field(default_factory=dict)
    sample_row_count: int = 0
    total_rows: int | None = None
    needs_stage3: bool = False

    def effective_schema(self) -> dict[str, pl.DataType]:
        if self.inferred_schema:
            return self.inferred_schema
        if self.ordered_schema:
            return self.ordered_schema
        return dict.fromkeys(self.columns, pl.Utf8)


def _mode_value_expr(column: str, dtype: pl.DataType | None) -> pl.Expr:
    expr = pl.col(column).drop_nulls()
    if dtype is not None and _is_nested_dtype(dtype):
        return expr.first()
    return expr.mode().sort().first()


def _series_mode(series: pl.Series) -> Any | None:
    clean = series.drop_nulls()
    if clean.is_empty():
        return None

    dtype = series.dtype
    if _is_nested_dtype(dtype):
        return clean[0]

    with contextlib.suppress(Exception):
        modes = clean.mode().sort()
        if modes.is_empty():
            return None
        return modes[0]

    return clean[0]


def _pending_summary_df() -> pl.DataFrame:
    """Return a lightweight dataframe shown while the summary is computing."""

    placeholder = _empty_summary_record("(computing…)", "")
    placeholder["mode"] = "Computing summary…"
    return _summary_records_to_df([placeholder])


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result):
        return None
    return result


class _ProgressiveCsvSummaryJob:
    """Progressive CSV summary pipeline coordinating staged jobs.

    The pipeline executes four sequential stages:

    * **Sniff** – Detect delimiter/quote/encoding and populate header names.
    * **Sample** – Parse a bounded sample to infer schema and rough stats.
    * **Stream** – Stream the full file for exact counts and basic stats.
    * **Heavy** – Optionally compute medians/uniques when the dataset is small.

    Each stage posts a :class:`SummaryProgressUpdate` which the UI uses to
    refresh staged results and eventually render the final summary dataframe.
    """

    def __init__(
        self,
        *,
        sheet_id: str,
        generation: int,
        tag: str,
        handle: _SummaryUiHandle,
        path: str,
        columns: list[str],
        ordered_schema: Mapping[str, pl.DataType],
        sample_rows: int = CSV_INFER_ROWS,
        auto_start: bool = True,
        runner: JobRunner,
    ) -> None:
        self._sheet_id = sheet_id
        self._generation = generation
        self._tag = tag
        self._handle = handle
        self._runner: JobRunner = runner
        self._state = _CsvSummaryState(
            path=Path(path),
            ordered_schema=dict(ordered_schema),
            columns=list(columns),
        )
        if not self._state.records and self._state.columns:
            schema_hint = {
                name: self._state.ordered_schema.get(name, pl.Utf8) for name in self._state.columns
            }
            self._state.records = _init_column_summary_records(self._state.columns, schema_hint)
        self._sample_target = max(int(sample_rows), 0)
        self._pending: Future[Any] | None = None
        self._cancelled = False
        if auto_start:
            self._schedule_stage(0)

    def cancel(self) -> None:
        self._cancelled = True
        pending = self._pending
        if pending is not None:
            pending.cancel()
            self._pending = None

    def _build_df(self) -> pl.DataFrame:
        return _summary_records_to_df(self._state.records)

    def _schedule_stage(self, stage_idx: int) -> None:
        if self._cancelled:
            return

        def _fn(gen: int, *, stage: int = stage_idx) -> SummaryProgressUpdate:
            return self._run_stage(stage, gen)

        future = self._runner.enqueue(
            JobRequest(
                sheet_id=self._sheet_id,
                generation=self._generation,
                tag=self._tag,
                fn=_fn,
                cache_result=False,
            )
        )
        self._pending = future

        def _done(fut: Future[Any], *, stage: int = stage_idx) -> None:
            self._on_stage_done(stage, fut)

        future.add_done_callback(_done)

    def _on_stage_done(self, stage_idx: int, future: Future[Any]) -> None:
        if self._cancelled:
            return
        try:
            job_result = future.result()
        except Exception:
            return

        value = getattr(job_result, "value", None)
        done = True
        if isinstance(value, SummaryProgressUpdate):
            done = value.done

        if self._runner.current_generation(self._sheet_id) != self._generation:
            return

        if done:
            self._handle.notify_ready()
            return

        self._handle.notify_refresh()

        next_stage = stage_idx + 1
        if next_stage == 3 and not self._state.needs_stage3:
            self._handle.notify_ready()
            return
        if next_stage >= 4:
            return
        self._schedule_stage(next_stage)

    def _run_stage(self, stage_idx: int, generation: int) -> SummaryProgressUpdate:
        if stage_idx == 0:
            return self._run_sniff()
        if stage_idx == 1:
            return self._run_sample()
        if stage_idx == 2:
            return self._run_stream()
        if stage_idx == 3:
            return self._run_heavy()
        return SummaryProgressUpdate(
            frame=self._build_df(),
            done=True,
            stage="final",
            message="Column stats ready",
        )

    def _run_sniff(self) -> SummaryProgressUpdate:
        state = self._state
        delimiter = state.delimiter
        quote_char = state.quote_char
        header = list(state.columns)

        try:
            with state.path.open("rb") as fh:
                sample_bytes = fh.read(_CSV_SNIFF_BYTES)
        except OSError:
            sample_bytes = b""

        sample_text = sample_bytes.decode("utf-8", errors="ignore")
        sniffer = csv.Sniffer()
        with contextlib.suppress(csv.Error):
            dialect = sniffer.sniff(sample_text or ",")
            delimiter = getattr(dialect, "delimiter", delimiter) or delimiter
            quote_char = getattr(dialect, "quotechar", quote_char) or quote_char

        state.delimiter = delimiter
        state.quote_char = quote_char or state.quote_char
        state.encoding = "utf8-lossy"

        header_row: list[str] | None = None
        try:
            with state.path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
                reader = csv.reader(
                    fh,
                    delimiter=state.delimiter,
                    quotechar=state.quote_char,
                )
                header_row = next(reader, None)
        except Exception:
            header_row = None

        if header_row:
            header = [str(col) for col in header_row]
        elif not header and state.ordered_schema:
            header = list(state.ordered_schema.keys())

        state.columns = header
        schema_hint = {name: state.ordered_schema.get(name, pl.Utf8) for name in state.columns}
        state.records = _init_column_summary_records(state.columns, schema_hint)

        return SummaryProgressUpdate(
            frame=self._build_df(),
            done=False,
            stage="sniff",
            message="Sniffing CSV layout…",
        )

    def _run_sample(self) -> SummaryProgressUpdate:
        state = self._state
        if not state.columns:
            return SummaryProgressUpdate(
                frame=self._build_df(),
                done=False,
                stage="sample",
                message="Sampling CSV…",
            )

        sample_df = pl.read_csv(
            state.path,
            has_header=True,
            n_rows=self._sample_target or None,
            separator=state.delimiter,
            quote_char=state.quote_char,
            encoding="utf8-lossy",
            truncate_ragged_lines=True,
            ignore_errors=True,
        )

        state.sample_row_count = int(sample_df.height)
        inferred: dict[str, pl.DataType] = {}
        for name in state.columns:
            dtype = sample_df.schema.get(name)
            if dtype is None:
                dtype = state.ordered_schema.get(name, pl.Utf8)
            inferred[name] = dtype
        state.inferred_schema = inferred

        total = sample_df.height or None
        for rec in state.records:
            name = rec["column"]
            dtype = inferred.get(name, state.ordered_schema.get(name, pl.Utf8))
            rec["dtype"] = _simplify_dtype_text(dtype)
            if name not in sample_df.columns:
                continue

            series = sample_df.get_column(name)
            rec["mode"] = _series_mode(series)

            nulls = int(series.null_count())
            non_nulls = int(series.len() - nulls)
            rec["nulls"] = nulls
            rec["non_nulls"] = non_nulls
            if total is not None:
                rec["rows"] = int(total)
                if total > 0:
                    rec["null_percent"] = (nulls / total) * 100
                    rec["non_null_percent"] = (non_nulls / total) * 100

            if _supports_min_max(dtype):
                with contextlib.suppress(Exception):
                    rec["min"] = series.min()
                with contextlib.suppress(Exception):
                    rec["max"] = series.max()

            if _supports_numeric_stats(dtype):
                numeric = series.cast(pl.Float64, strict=False)
                rec["mean"] = _safe_float(numeric.mean())
                rec["std"] = _safe_float(numeric.std())
                rec["median"] = _safe_float(numeric.median())

            if not _is_nested_dtype(dtype):
                with contextlib.suppress(Exception):
                    unique = series.drop_nulls().n_unique()
                if unique is not None:
                    unique_int = int(unique)
                    rec["unique"] = unique_int
                    if total:
                        rec["unique_percent"] = (unique_int / total) * 100

        return SummaryProgressUpdate(
            frame=self._build_df(),
            done=False,
            stage="sample",
            message="Sampling CSV (approx stats)…",
        )

    def _run_stream(self) -> SummaryProgressUpdate:
        state = self._state
        schema = state.effective_schema()
        if not state.columns:
            return SummaryProgressUpdate(
                frame=self._build_df(),
                done=True,
                stage="stream",
                message="Streaming CSV stats…",
            )

        lf = pl.scan_csv(
            state.path,
            has_header=True,
            separator=state.delimiter,
            quote_char=state.quote_char,
            schema_overrides=schema,
            infer_schema_length=0,
            encoding="utf8-lossy",
            ignore_errors=True,
        )

        exprs: list[pl.Expr] = [pl.len().alias("__rows__")]
        for rec in state.records:
            name = rec["column"]
            exprs.append(pl.col(name).null_count().alias(f"{name}__nulls"))
            exprs.append(pl.col(name).count().alias(f"{name}__non_nulls"))
            dtype = schema.get(name, pl.Utf8)
            exprs.append(_mode_value_expr(name, dtype).alias(f"{name}__mode"))
            if _supports_min_max(dtype):
                exprs.append(pl.col(name).min().alias(f"{name}__min"))
                exprs.append(pl.col(name).max().alias(f"{name}__max"))
            if _supports_numeric_stats(dtype):
                exprs.append(pl.col(name).mean().alias(f"{name}__mean"))
                exprs.append(pl.col(name).std().alias(f"{name}__std"))

        try:
            stats_df = lf.select(exprs).collect(streaming=True)
        except Exception:
            stats_df = lf.select(exprs).collect()

        total_rows: int | None = None
        if "__rows__" in stats_df.columns:
            total_value = stats_df["__rows__"][0]
            if total_value is not None:
                total_rows = int(total_value)

        state.total_rows = total_rows

        for rec in state.records:
            name = rec["column"]
            null_alias = f"{name}__nulls"
            non_null_alias = f"{name}__non_nulls"
            mode_alias = f"{name}__mode"

            if null_alias in stats_df.columns:
                null_value = stats_df[null_alias][0]
                rec["nulls"] = int(null_value) if null_value is not None else None

            if non_null_alias in stats_df.columns:
                non_null_value = stats_df[non_null_alias][0]
                rec["non_nulls"] = int(non_null_value) if non_null_value is not None else None

            if mode_alias in stats_df.columns:
                rec["mode"] = stats_df[mode_alias][0]

            dtype = schema.get(name, pl.Utf8)
            if _supports_min_max(dtype):
                min_alias = f"{name}__min"
                max_alias = f"{name}__max"
                if min_alias in stats_df.columns:
                    rec["min"] = stats_df[min_alias][0]
                if max_alias in stats_df.columns:
                    rec["max"] = stats_df[max_alias][0]

            if _supports_numeric_stats(dtype):
                mean_alias = f"{name}__mean"
                std_alias = f"{name}__std"
                if mean_alias in stats_df.columns:
                    rec["mean"] = _safe_float(stats_df[mean_alias][0])
                if std_alias in stats_df.columns:
                    rec["std"] = _safe_float(stats_df[std_alias][0])

            if total_rows is not None:
                rec["rows"] = total_rows
                nulls = rec.get("nulls")
                non_nulls = rec.get("non_nulls")
                if nulls is not None and total_rows > 0:
                    rec["null_percent"] = (nulls / total_rows) * 100
                if non_nulls is not None and total_rows > 0:
                    rec["non_null_percent"] = (non_nulls / total_rows) * 100

        schema_values = list(schema.items())
        has_unique_candidates = any(not _is_nested_dtype(dtype) for _, dtype in schema_values)
        has_numeric_candidates = any(_supports_numeric_stats(dtype) for _, dtype in schema_values)
        state.needs_stage3 = bool(
            total_rows is not None
            and total_rows <= _CSV_STAGE3_ROW_THRESHOLD
            and (has_unique_candidates or has_numeric_candidates)
        )

        return SummaryProgressUpdate(
            frame=self._build_df(),
            done=not state.needs_stage3,
            stage="stream",
            message="Streaming CSV stats…",
        )

    def _run_heavy(self) -> SummaryProgressUpdate:
        state = self._state
        if not state.needs_stage3:
            return SummaryProgressUpdate(
                frame=self._build_df(),
                done=True,
                stage="final",
                message="Column stats ready",
            )

        schema = state.effective_schema()
        exprs: list[pl.Expr] = []
        for rec in state.records:
            name = rec["column"]
            dtype = schema.get(name)
            if dtype is None:
                continue
            if not _is_nested_dtype(dtype):
                exprs.append(pl.col(name).n_unique().alias(f"{name}__unique"))
            if _supports_numeric_stats(dtype):
                exprs.append(pl.col(name).median().alias(f"{name}__median"))

        if not exprs:
            return SummaryProgressUpdate(
                frame=self._build_df(),
                done=True,
                stage="final",
                message="Column stats ready",
            )

        lf = pl.scan_csv(
            state.path,
            has_header=True,
            separator=state.delimiter,
            quote_char=state.quote_char,
            schema_overrides=schema,
            infer_schema_length=0,
            encoding="utf8-lossy",
            ignore_errors=True,
        )
        stats_df = lf.select(exprs).collect()

        for rec in state.records:
            name = rec["column"]
            unique_alias = f"{name}__unique"
            median_alias = f"{name}__median"

            if unique_alias in stats_df.columns:
                unique_value = stats_df[unique_alias][0]
                if unique_value is not None:
                    unique_int = int(unique_value)
                    rec["unique"] = unique_int
                    rows = state.total_rows
                    if rows:
                        rec["unique_percent"] = (unique_int / rows) * 100

            if median_alias in stats_df.columns:
                rec["median"] = _safe_float(stats_df[median_alias][0])

        return SummaryProgressUpdate(
            frame=self._build_df(),
            done=True,
            stage="final",
            message="Column stats ready",
        )


def _column_summary_stage_counts(
    base_lf: pl.LazyFrame,
    columns: list[str],
    schema: Mapping[str, pl.DataType],
    records: list[dict[str, Any]],
) -> None:
    if not columns:
        return

    exprs: list[pl.Expr] = []
    added_aliases: set[str] = set()

    for rec in records:
        name = rec["column"]
        dtype = schema.get(name)
        if dtype is None:
            continue

        if rec["non_nulls"] is None:
            alias = f"{name}__non_nulls"
            if alias not in added_aliases:
                exprs.append(pl.col(name).count().alias(alias))
                added_aliases.add(alias)
        if rec["nulls"] is None:
            alias = f"{name}__nulls"
            if alias not in added_aliases:
                exprs.append(pl.col(name).null_count().alias(alias))
                added_aliases.add(alias)

        if dtype is not None and _supports_min_max(dtype):
            min_alias = f"{name}__min"
            max_alias = f"{name}__max"
            if min_alias not in added_aliases:
                exprs.append(pl.col(name).min().alias(min_alias))
                added_aliases.add(min_alias)
            if max_alias not in added_aliases:
                exprs.append(pl.col(name).max().alias(max_alias))
                added_aliases.add(max_alias)

    if not exprs:
        return

    try:
        counts_df = base_lf.select(exprs).collect()
    except Exception:
        return

    sample_df: pl.DataFrame | None = None
    if _SUMMARY_MODE_SAMPLE_SIZE > 0:
        with contextlib.suppress(Exception):
            # Sampling avoids the costly global mode aggregation on large datasets.
            sample_df = base_lf.head(_SUMMARY_MODE_SAMPLE_SIZE).collect()

    for rec in records:
        name = rec["column"]
        dtype = schema.get(name)
        if dtype is None:
            continue

        non_nulls_alias = f"{name}__non_nulls"
        nulls_alias = f"{name}__nulls"

        if non_nulls_alias in counts_df.columns:
            non_nulls = counts_df[non_nulls_alias][0]
            rec["non_nulls"] = int(non_nulls) if non_nulls is not None else None

        if nulls_alias in counts_df.columns:
            nulls = counts_df[nulls_alias][0]
            rec["nulls"] = int(nulls) if nulls is not None else None

        non_nulls = rec.get("non_nulls")
        nulls = rec.get("nulls")
        if non_nulls is not None and nulls is not None:
            total = non_nulls + nulls
            rec["rows"] = total
            if total > 0:
                rec["non_null_percent"] = (non_nulls / total) * 100
                rec["null_percent"] = (nulls / total) * 100
        if sample_df is not None and name in sample_df.columns:
            with contextlib.suppress(Exception):
                rec["mode"] = _series_mode(sample_df.get_column(name))

        if dtype is not None and _supports_min_max(dtype):
            min_alias = f"{name}__min"
            max_alias = f"{name}__max"
            if min_alias in counts_df.columns:
                rec["min"] = counts_df[min_alias][0]
            if max_alias in counts_df.columns:
                rec["max"] = counts_df[max_alias][0]


def _column_summary_stage_numeric(
    base_lf: pl.LazyFrame,
    columns: list[str],
    schema: Mapping[str, pl.DataType],
    records: list[dict[str, Any]],
) -> None:
    numeric_cols = [name for name in columns if _supports_numeric_stats(schema.get(name))]
    if not numeric_cols:
        return

    exprs: list[pl.Expr] = []
    for name in numeric_cols:
        exprs.append(pl.col(name).mean().alias(f"{name}__mean"))
        exprs.append(pl.col(name).std().alias(f"{name}__std"))
        exprs.append(pl.col(name).median().alias(f"{name}__median"))

    try:
        stats_df = base_lf.select(exprs).collect()
    except Exception:
        return

    for rec in records:
        name = rec["column"]
        if name not in numeric_cols:
            continue

        mean_alias = f"{name}__mean"
        std_alias = f"{name}__std"
        median_alias = f"{name}__median"

        if mean_alias in stats_df.columns:
            rec["mean"] = _safe_float(stats_df[mean_alias][0])
        if std_alias in stats_df.columns:
            rec["std"] = _safe_float(stats_df[std_alias][0])
        if median_alias in stats_df.columns:
            rec["median"] = _safe_float(stats_df[median_alias][0])


def _column_summary_stage_unique(
    base_lf: pl.LazyFrame,
    columns: list[str],
    schema: Mapping[str, pl.DataType],
    records: list[dict[str, Any]],
) -> None:
    if not columns:
        return

    exprs: list[pl.Expr] = []
    for name in columns:
        dtype = schema.get(name)
        if dtype is not None and not _is_nested_dtype(dtype):
            exprs.append(pl.col(name).n_unique().alias(f"{name}__unique"))

    if not exprs:
        return

    try:
        unique_df = base_lf.select(exprs).collect()
    except Exception:
        return

    for rec in records:
        name = rec["column"]
        unique_alias = f"{name}__unique"
        if unique_alias in unique_df.columns:
            value = unique_df[unique_alias][0]
            if value is not None:
                rec["unique"] = int(value)
                rows = rec.get("rows")
                if rows:
                    rec["unique_percent"] = (value / rows) * 100


def compute_summary_df(
    lf: pl.LazyFrame,
    schema: Mapping[str, pl.DataType],
    *,
    max_cols: int | None = None,
) -> pl.DataFrame:
    """Compute summary statistics for ``lf`` using ``schema``."""

    columns = list(schema.keys())
    if max_cols is not None:
        columns = columns[:max_cols]

    records = _init_column_summary_records(columns, schema)
    _column_summary_stage_counts(lf, columns, schema, records)
    _column_summary_stage_numeric(lf, columns, schema, records)
    _column_summary_stage_unique(lf, columns, schema, records)
    return _summary_records_to_df(records)


def _parquet_stat_value(stats: Any, attr: str) -> Any | None:
    """Best-effort extraction of a Parquet statistic attribute."""

    try:
        return getattr(stats, attr)
    except Exception:
        return None


def _coerce_parquet_stat_value(value: Any, dtype: pl.DataType | None) -> Any:
    """Cast Parquet metadata values to the schema dtype when possible."""

    if value is None or dtype is None:
        return value

    try:
        series = pl.Series([value])
    except Exception:
        return value

    if series.dtype == dtype:
        return value

    with contextlib.suppress(Exception):
        casted = series.cast(dtype, strict=False)
        return casted[0]

    return value


def _parquet_metadata_summary_df(
    path: str,
    columns: list[str],
    schema: Mapping[str, pl.DataType],
    *,
    max_cols: int | None = None,
) -> pl.DataFrame | None:
    """Build a partial summary dataframe using Parquet metadata when available."""

    try:
        import pyarrow.parquet as pq
    except Exception:
        return None

    try:
        parquet_file = pq.ParquetFile(path)
    except Exception:
        return None

    metadata = parquet_file.metadata
    if metadata is None:
        return None

    try:
        arrow_schema = parquet_file.schema_arrow
    except Exception:
        return None

    column_order = list(columns)
    if max_cols is not None:
        column_order = column_order[:max_cols]

    records = _init_column_summary_records(column_order, schema)

    name_to_index: dict[str, int] = {}
    for idx, arrow_field in enumerate(arrow_schema):
        name_to_index[arrow_field.name] = idx

    total_rows = int(metadata.num_rows) if metadata.num_rows is not None else None
    if total_rows is not None:
        for rec in records:
            rec["rows"] = total_rows

    row_groups = metadata.num_row_groups or 0
    if row_groups == 0:
        return _summary_records_to_df(records)

    for rec in records:
        name = rec["column"]
        arrow_index = name_to_index.get(name)
        if arrow_index is None:
            continue

        nulls_known = True
        column_nulls = 0
        min_max_complete = True
        min_values: list[Any] = []
        max_values: list[Any] = []
        unique_known = True
        unique_total = 0

        for group_idx in range(row_groups):
            column_chunk = metadata.row_group(group_idx).column(arrow_index)
            stats = getattr(column_chunk, "statistics", None)
            if stats is None:
                nulls_known = False
                min_max_complete = False
                unique_known = False
                continue

            null_count = getattr(stats, "null_count", None)
            if null_count is None:
                nulls_known = False
            else:
                column_nulls += int(null_count)

            has_min_max = getattr(stats, "has_min_max", False)
            if not has_min_max:
                min_max_complete = False
            else:
                min_value = _parquet_stat_value(stats, "min")
                max_value = _parquet_stat_value(stats, "max")
                if min_value is None or max_value is None:
                    min_max_complete = False
                else:
                    min_values.append(min_value)
                    max_values.append(max_value)

            distinct_count = getattr(stats, "distinct_count", None)
            if distinct_count is None:
                unique_known = False
            else:
                unique_total += int(distinct_count)

        if nulls_known and total_rows is not None:
            rec["nulls"] = column_nulls
            non_nulls = total_rows - column_nulls
            rec["non_nulls"] = non_nulls
            if total_rows > 0:
                rec["null_percent"] = (column_nulls / total_rows) * 100
                rec["non_null_percent"] = (non_nulls / total_rows) * 100

        if (
            min_max_complete
            and min_values
            and max_values
            and len(min_values) == row_groups
            and len(max_values) == row_groups
        ):
            dtype = schema.get(name)
            rec["min"] = _coerce_parquet_stat_value(min(min_values), dtype)
            rec["max"] = _coerce_parquet_stat_value(max(max_values), dtype)

        if unique_known:
            rec["unique"] = unique_total
            if total_rows and total_rows > 0:
                rec["unique_percent"] = (unique_total / total_rows) * 100

    return _summary_records_to_df(records)


class SummarySheet(DataSheet):
    """Sheet implementation for column summary statistics."""

    default_frozen_columns = _SUMMARY_FROZEN_COLUMNS

    def __init__(
        self,
        base_sheet: Sheet,
        summary_df: pl.DataFrame | None = None,
        *,
        plan: QueryPlan | None = None,
        schema: dict[str, pl.DataType] | None = None,
        columns: Sequence[str] | None = None,
        sheet_id: str | None = None,
        generation: int | None = None,
        compiler: Any | None = None,
        materializer: Any | None = None,
        runner: JobRunner,
    ) -> None:
        self.source_sheet = base_sheet
        self._preserve_jobs_from = getattr(base_sheet, "sheet_id", None)
        self.is_summary_view = True

        if summary_df is None:
            base_lf = getattr(base_sheet, "lf", None)
            if isinstance(base_lf, EnginePayloadHandle):
                base_lf = unwrap_lazyframe_handle(base_lf)
            if base_lf is None and hasattr(base_sheet, "to_lazy"):
                base_lf = base_sheet.to_lazy()
                if isinstance(base_lf, EnginePayloadHandle):
                    base_lf = unwrap_lazyframe_handle(base_lf)
            if base_lf is None:
                msg = "Base sheet does not provide a lazy frame"
                raise ValueError(msg)

            schema_mapping = getattr(base_sheet, "schema", {})
            ordered_schema: dict[str, pl.DataType] = {}
            for name in getattr(base_sheet, "columns", []):
                ordered_schema[name] = schema_mapping.get(name, pl.Utf8)

            summary_df = compute_summary_df(base_lf, ordered_schema)

        self._display_df = summary_df
        if runner is None:  # pragma: no cover - defensive guard
            msg = "SummarySheet requires a JobRunner instance"
            raise ValueError(msg)
        super().__init__(
            summary_df.lazy(),
            plan=plan,
            schema=schema,
            columns=columns,
            sheet_id=sheet_id,
            generation=generation,
            compiler=compiler,
            materializer=materializer,
            runner=runner,
        )

    def _attach_row_id_column(self, lf: pl.LazyFrame) -> tuple[pl.LazyFrame, str | None]:
        try:
            schema = lf.collect_schema()
        except Exception:
            schema = getattr(lf, "schema", {})

        if ROW_ID_COLUMN in schema:
            return lf, ROW_ID_COLUMN

        if "column" in schema:
            try:
                with_ids = lf.with_columns(pl.col("column").alias(ROW_ID_COLUMN))
                return with_ids, ROW_ID_COLUMN
            except Exception:
                return lf, None

        return lf, None

    def with_plan(self, plan: QueryPlan) -> SummarySheet:
        if plan == self.plan:
            return self
        return self.__class__(
            self.source_sheet,
            summary_df=self._display_df,
            plan=plan,
            schema=self.schema,
            columns=self.columns,
            sheet_id=self.sheet_id,
            generation=self.job_runner.bump_generation(self.sheet_id),
            compiler=self._compiler,
            materializer=self._materializer,
            runner=self.job_runner,
        )

    @classmethod
    def from_dataframe(cls, base_sheet: Sheet, df: pl.DataFrame) -> SummarySheet:
        """Construct a ``SummarySheet`` using a precomputed dataframe."""

        try:
            runner = base_sheet.job_runner  # type: ignore[attr-defined]
        except AttributeError as exc:
            msg = "SummarySheet.from_dataframe requires base_sheet.job_runner"
            raise ValueError(msg) from exc
        return cls(base_sheet, summary_df=df, runner=runner)

    def fetch_slice(self, row_start: int, row_count: int, columns: Sequence[str]) -> TableSlice:
        """Attach column-name row identifiers so selections survive resorting."""

        table_slice = super().fetch_slice(row_start, row_count, columns)
        if "column" not in table_slice.column_names:
            return table_slice

        try:
            names = table_slice.column("column").values
        except Exception:
            return table_slice

        with contextlib.suppress(Exception):
            table_slice.row_ids = tuple(names)
        return table_slice


class _SummaryUiHandle:
    """Handle that applies summary job results to the viewer."""

    _spinner_config = SPINNERS["dots"]
    _spinner_frames = tuple(_spinner_config["frames"]) if _spinner_config else ()
    _spinner_interval_ns = int(_spinner_config["interval"]) * 1_000_000 if _spinner_config else 0

    def __init__(
        self,
        sheet_id: str,
        tag: str,
        screen: Screen | None,
        runner: JobRunner,
    ) -> None:
        self._source_sheet_id = sheet_id
        self.tag = tag
        self._screen_ref: weakref.ReferenceType[Screen] | None = (
            weakref.ref(screen) if screen is not None else None
        )
        self._runner = runner
        self._job_finished = False
        self._frame_index = 0
        self._last_frame_ns = monotonic_ns()
        self._timer: Timer | None = None
        self._status_prefix = "Computing column summary…"
        self._last_result_ts: int = 0
        self._pipeline: _ProgressiveCsvSummaryJob | None = None

    def _on_timer(self) -> None:
        self._invalidate_screen()

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

    def _cancel_timer(self) -> None:
        timer = self._timer
        if timer is not None:
            timer.cancel()
            self._timer = None

    def _schedule_tick(self, delay_ns: int | None = None) -> None:
        if not self._spinner_frames or self._spinner_interval_ns <= 0:
            return

        interval_ns = self._spinner_interval_ns if delay_ns is None else delay_ns
        if interval_ns <= 0:
            interval_ns = self._spinner_interval_ns

        delay_s = interval_ns / 1_000_000_000
        if delay_s <= 0:
            return

        self._cancel_timer()
        timer = Timer(delay_s, self._on_timer)
        timer.daemon = True
        timer.start()
        self._timer = timer

    def prime(self, viewer: Viewer) -> None:
        """Install the initial loading message."""

        self._status_prefix = "Computing column summary…"
        if self._spinner_frames:
            frame = self._spinner_frames[0]
            viewer.status_message = f"{frame} {self._status_prefix}"
            self._frame_index = 0
            self._last_frame_ns = monotonic_ns()
            self._schedule_tick()
        else:
            viewer.status_message = self._status_prefix

    def notify_ready(self) -> None:
        """Mark the job as completed and request a UI refresh."""

        self._job_finished = True
        self._cancel_timer()
        self._invalidate_screen()

    def notify_refresh(self) -> None:
        """Request a UI refresh for an intermediate update."""

        self._invalidate_screen()

    def attach_pipeline(self, pipeline: _ProgressiveCsvSummaryJob) -> None:
        self._pipeline = pipeline

    def _advance_spinner(self, viewer: Viewer) -> None:
        if not self._spinner_frames or self._spinner_interval_ns <= 0:
            return

        interval_ns = self._spinner_interval_ns
        if interval_ns <= 0:
            return

        now = monotonic_ns()
        elapsed = now - self._last_frame_ns
        if elapsed < interval_ns:
            self._schedule_tick(interval_ns - elapsed)
            return

        self._frame_index = (self._frame_index + 1) % len(self._spinner_frames)
        self._last_frame_ns = now
        frame = self._spinner_frames[self._frame_index]
        viewer.status_message = f"{frame} {self._status_prefix}"
        self._invalidate_screen()
        self._schedule_tick()

    def consume_update(self, viewer: Viewer) -> bool:
        sheet = viewer.sheet
        source_sheet = getattr(sheet, "source_sheet", sheet)
        sheet_id = getattr(source_sheet, "sheet_id", None)
        if sheet_id != self._source_sheet_id:
            viewer.status_message = None
            self._cancel_timer()
            return True

        result = self._runner.get(self._source_sheet_id, self.tag)
        if result is None:
            if self._job_finished:
                viewer.status_message = None
                self._cancel_timer()
                return True
            self._advance_spinner(viewer)
            return False

        if result.ts_ns <= self._last_result_ts:
            if self._job_finished:
                viewer.status_message = None
                return True
            self._advance_spinner(viewer)
            return False

        self._last_result_ts = result.ts_ns

        if result.error is not None:
            viewer.status_message = f"summary error: {result.error!s}"[:120]
            self._cancel_timer()
            self._job_finished = True
            return True

        value = result.value
        if isinstance(value, SummaryProgressUpdate):
            summary_sheet = SummarySheet.from_dataframe(source_sheet, value.frame)
            viewer.replace_sheet(summary_sheet, source_path=None)
            if value.message:
                self._status_prefix = value.message
            if value.done:
                viewer.status_message = None
                self._cancel_timer()
                self._job_finished = True
                return True
            if self._spinner_frames:
                self._frame_index = 0
                self._last_frame_ns = monotonic_ns()
                viewer.status_message = f"{self._spinner_frames[0]} {self._status_prefix}"
                self._schedule_tick()
            else:
                viewer.status_message = self._status_prefix
            return False

        if not isinstance(value, pl.DataFrame):
            viewer.status_message = "summary unavailable"
            self._cancel_timer()
            self._job_finished = True
            return True

        summary_sheet = SummarySheet.from_dataframe(source_sheet, value)
        viewer.replace_sheet(summary_sheet, source_path=None)
        viewer.status_message = None
        self._cancel_timer()
        self._job_finished = True
        return True

    def cancel(self) -> None:
        self._cancel_timer()
        pipeline = self._pipeline
        if pipeline is not None:
            pipeline.cancel()


def _summary_cmd(context: CommandContext, args: list[str]) -> None:
    viewer = context.viewer
    sheet = viewer.sheet
    base_sheet = getattr(sheet, "source_sheet", sheet)
    try:
        runner = base_sheet.job_runner  # type: ignore[attr-defined]
    except AttributeError:
        runner = viewer.job_runner

    if not getattr(base_sheet, "columns", None):
        viewer.status_message = "no columns available"
        return

    job_context = getattr(base_sheet, "job_context", None)
    screen = getattr(context, "screen", None)
    session = getattr(context, "session", None) or viewer.session
    view_stack = getattr(context, "view_stack", None)
    if view_stack is None and session is not None:
        view_stack = getattr(session, "view_stack", None)
    if job_context is None or screen is None:
        try:
            summary_sheet = SummarySheet(base_sheet, runner=runner)
            viewer.replace_sheet(summary_sheet, source_path=None)
            viewer.status_message = "summary view"
        except Exception as exc:  # pragma: no cover - guardrail
            viewer.status_message = f"summary error: {exc}"[:120]
            if screen is not None:
                screen.refresh(skip_metrics=True)
        else:
            if screen is not None:
                screen.refresh(skip_metrics=True)
        return

    sheet_id, generation, plan_hash = job_context()

    column_signature = getattr(base_sheet, "_column_signature", None)
    if column_signature is None:
        viewer.status_message = "summary unavailable"
        return

    tag = f"summary:colsig={column_signature()}:plan={plan_hash}"

    cached_placeholder: pl.DataFrame | None = None
    cached = runner.get(sheet_id, tag)
    if cached is not None:
        if cached.error is not None:
            viewer.status_message = f"summary error: {cached.error!s}"[:120]
            screen.refresh(skip_metrics=True)
            return

        final_df: pl.DataFrame | None = None
        cached_value = cached.value
        if isinstance(cached_value, SummaryProgressUpdate):
            if cached_value.done:
                final_df = cached_value.frame
            else:
                cached_placeholder = cached_value.frame
        elif isinstance(cached_value, pl.DataFrame):
            final_df = cached_value
        else:
            viewer.status_message = "summary unavailable"
            screen.refresh(skip_metrics=True)
            return

        if final_df is not None:
            summary_sheet = SummarySheet.from_dataframe(base_sheet, final_df)
            active_viewer = viewer

            if sheet is base_sheet:
                if view_stack is not None:
                    new_viewer = Viewer(
                        summary_sheet,
                        viewport_rows=viewer._viewport_rows_override,
                        viewport_cols=viewer._viewport_cols_override,
                        source_path=None,
                        session=session,
                        runner=runner,
                    )
                    view_stack.push(new_viewer)
                    new_viewer.invalidate_row_count()
                    active_viewer = view_stack.active or new_viewer
                else:
                    viewer.replace_sheet(summary_sheet, source_path=None)
            else:
                viewer.replace_sheet(summary_sheet, source_path=None)

            active_viewer.status_message = None
            viewer.status_message = None
            context.viewer = active_viewer
            context.sheet = active_viewer.sheet
            screen.refresh(skip_metrics=True)
            return

    lazy_frame_candidate = getattr(base_sheet, "lf0", None)
    if lazy_frame_candidate is None:
        lazy_frame_candidate = getattr(base_sheet, "lf", None)
    if lazy_frame_candidate is None:
        viewer.status_message = "summary unavailable"
        return
    if isinstance(lazy_frame_candidate, EnginePayloadHandle):
        lazy_frame = unwrap_lazyframe_handle(lazy_frame_candidate)
    else:
        lazy_frame = lazy_frame_candidate

    schema_mapping = getattr(base_sheet, "schema", {})
    ordered_schema = {name: schema_mapping.get(name, pl.Utf8) for name in base_sheet.columns}

    def _fn(gen: int) -> pl.DataFrame | None:
        if runner.current_generation(sheet_id) != gen:
            return None
        return compute_summary_df(lazy_frame, ordered_schema)

    active_viewer = viewer
    source_path = getattr(viewer, "_source_path", None)
    progressive_enabled = isinstance(source_path, str) and source_path.lower().endswith(
        (".csv", ".tsv")
    )
    if sheet is base_sheet:
        placeholder_df = cached_placeholder
        if (
            placeholder_df is None
            and isinstance(source_path, str)
            and source_path.lower().endswith(".parquet")
        ):
            placeholder_df = _parquet_metadata_summary_df(
                source_path,
                list(base_sheet.columns),
                ordered_schema,
            )
        if placeholder_df is None:
            placeholder_df = _pending_summary_df()
        placeholder = SummarySheet.from_dataframe(base_sheet, placeholder_df)

        session = getattr(context, "session", None) or viewer.session

        try:
            runner = base_sheet.job_runner  # type: ignore[attr-defined]
        except AttributeError:
            runner = viewer.job_runner

        if view_stack is not None:
            new_viewer = Viewer(
                placeholder,
                viewport_rows=viewer._viewport_rows_override,
                viewport_cols=viewer._viewport_cols_override,
                source_path=None,
                session=session,
                runner=runner,
            )
            view_stack.push(new_viewer)
            new_viewer.invalidate_row_count()
            active_viewer = view_stack.active or new_viewer
        else:
            viewer.replace_sheet(placeholder, source_path=None)
            active_viewer = viewer

        context.viewer = active_viewer
        context.sheet = active_viewer.sheet

    handle = _SummaryUiHandle(sheet_id, tag, screen, runner)
    handle.prime(active_viewer)
    if screen is not None:
        screen._jobs[active_viewer] = handle

    if progressive_enabled and isinstance(source_path, str):
        pipeline = _ProgressiveCsvSummaryJob(
            sheet_id=sheet_id,
            generation=generation,
            tag=tag,
            handle=handle,
            path=source_path,
            columns=list(base_sheet.columns),
            ordered_schema=ordered_schema,
            runner=runner,
        )
        handle.attach_pipeline(pipeline)
    else:
        future = runner.enqueue(
            JobRequest(
                sheet_id=sheet_id,
                generation=generation,
                tag=tag,
                fn=_fn,
                cache_result=False,
            )
        )

        def _wake(_future: Future) -> None:
            handle.notify_ready()

        future.add_done_callback(_wake)
    if screen is not None:
        screen.refresh(skip_metrics=True)


def register(
    *,
    commands: CommandRegistry | None = None,
    sheets: SheetRegistry | None = None,
    scanners: ScannerRegistry | None = None,
) -> None:
    if sheets is not None:
        sheets.register_sheet("summary", SummarySheet)

    if commands is not None:
        with contextlib.suppress(ValueError):
            commands.register("summary", _summary_cmd, "Column summary sheet", 0)
        for alias in ("C", "columns", "cols"):
            with contextlib.suppress(ValueError):
                commands.register_alias(alias, "summary")

        def _open_summary(context: CommandContext) -> None:
            _summary_cmd(context, [])

        commands.register_sheet_opener("summary", _open_summary)

    _ = scanners  # Placate linters for unused default argument

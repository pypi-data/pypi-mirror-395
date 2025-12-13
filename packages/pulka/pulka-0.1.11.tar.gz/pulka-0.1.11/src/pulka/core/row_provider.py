"""Row slice provider that bridges viewer requests to engine adapters."""

from __future__ import annotations

import logging
from collections import OrderedDict
from collections.abc import Callable, Iterator, Sequence
from dataclasses import asdict, dataclass, field
from enum import Enum
from threading import RLock
from time import monotonic_ns
from typing import TYPE_CHECKING, Any, cast

import polars as pl

from ..config.settings import CACHE_DEFAULTS, STREAMING_DEFAULTS
from ..data import csv_checkpoints
from ..data.sidecar import SidecarStore
from .column_insight import CellPreview, summarize_value_preview
from .engine.contracts import TableColumn, TableSlice
from .engine.polars_adapter import table_slice_from_dataframe
from .errors import CompileError, MaterializeError, PulkaCoreError
from .interfaces import (
    EngineAdapterProtocol,
    JobRunnerProtocol,
    MaterializerProtocol,
    is_materializer_compatible,
)
from .jobs import JobRequest
from .plan import QueryPlan, normalized_columns_key
from .sheet import SHEET_FEATURE_SLICE, sheet_supports
from .strategy import Strategy, compile_strategy

RowKey = tuple[str | None, int, int, str]


LOGGER = logging.getLogger(__name__)


if TYPE_CHECKING:
    from .source_traits import SourceTraits


class SliceStatus(Enum):
    """Describe how closely a slice matches the requested schema."""

    OK = "ok"
    PARTIAL = "partial"
    SCHEMA_MISMATCH = "schema_mismatch"


@dataclass(slots=True, frozen=True)
class SliceStreamRequest:
    """Parameters for streaming a table slice."""

    plan: QueryPlan | None
    columns: Sequence[str]
    start: int
    count: int
    batch_rows: int | None = None
    streaming_enabled: bool | None = None
    telemetry: dict[str, Any] | None = None


@dataclass(slots=True)
class TableSliceChunk:
    """Chunk of a streaming slice, enriched with telemetry."""

    offset: int
    slice: TableSlice
    status: SliceStatus
    is_final: bool
    telemetry: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class _SidecarWindow:
    fetch_start: int
    fetch_count: int
    trim_leading: int
    used: bool
    checkpoint_row: int | None

    @classmethod
    def identity(cls, start: int, count: int) -> _SidecarWindow:
        return cls(start, count, 0, False, None)


@dataclass(slots=True)
class _SidecarProgress:
    max_seen_start: int = -1
    last_span: int = 0
    screens_seen: int = 0

    def reset(self) -> None:
        self.max_seen_start = -1
        self.last_span = 0
        self.screens_seen = 0

    def observe(self, *, start: int, span: int) -> None:
        if span > 0:
            self.last_span = span if self.last_span <= 0 else max(self.last_span, span)
        if start < 0:
            return
        if self.max_seen_start < 0:
            self.max_seen_start = start
            return
        if start <= self.max_seen_start:
            return
        height = self.last_span or span or 1
        delta = start - self.max_seen_start
        steps = max(1, delta // max(height, 1))
        self.screens_seen += steps
        self.max_seen_start = start
        self.last_span = span if span > 0 else self.last_span


@dataclass(slots=True)
class _SidecarState:
    store: SidecarStore
    offsets: tuple[int, ...] | None = None
    building: bool = False
    failed: bool = False
    progress: _SidecarProgress = field(default_factory=_SidecarProgress)
    generation: int | None = None


@dataclass(frozen=True)
class _PlanContext:
    plan: QueryPlan
    fetch_columns: tuple[str, ...]
    requested_columns: tuple[str, ...]
    missing_columns: tuple[str, ...]
    plan_hash: str | None
    sheet_id: str | None
    generation: int | None


class RowProvider:
    """Serve row slices for a sheet, optionally prefetching upcoming ranges."""

    __slots__ = (
        "_engine_factory",
        "_columns_getter",
        "_fetcher",
        "_job_context",
        "_runner",
        "_pending",
        "_pending_futures",
        "_lock",
        "_materializer",
        "_empty_result_factory",
        "_empty_template",
        "_cache",
        "_cache_cells",
        "_cache_evictions",
        "_max_cache_cells",
        "_max_cache_entries",
        "_streaming_enabled",
        "_streaming_batch_rows",
        "_streaming_last_chunks",
        "_streaming_last_rows",
        "_streaming_last_cells",
        "_streaming_last_duration_ns",
        "_streaming_last_mode",
        "_source_traits_cache",
        "_strategy",
        "_strategy_cache",
        "_streaming_enabled_configured",
        "_streaming_batch_rows_configured",
        "_sidecar_states",
        "_prefetched_keys",
        "_prefetch_scheduled",
        "_prefetch_hits",
        "_prefetch_evictions",
        "_row_id_column",
    )

    MAX_CACHE_CELLS = CACHE_DEFAULTS.row_provider_max_cells
    MAX_CACHE_ENTRIES = CACHE_DEFAULTS.row_provider_max_entries
    STREAMING_ENABLED = STREAMING_DEFAULTS.enabled
    STREAMING_BATCH_ROWS = STREAMING_DEFAULTS.batch_rows
    SOURCE_TRAITS_CACHE_LIMIT = 8
    STRATEGY_CACHE_LIMIT = SOURCE_TRAITS_CACHE_LIMIT

    def __init__(
        self,
        *,
        engine_factory: Callable[[], EngineAdapterProtocol] | None = None,
        columns_getter: Callable[[], Sequence[str]] | None = None,
        materializer: MaterializerProtocol | None = None,
        fetcher: Callable[[int, int, Sequence[str]], Any] | None = None,
        job_context: Callable[[], tuple[str, int, str]] | None = None,
        empty_result_factory: Callable[[], Any] | None = None,
        runner: JobRunnerProtocol,
        streaming_enabled: bool | None = None,
        streaming_batch_rows: int | None = None,
        row_id_column: str | None = None,
    ) -> None:
        if engine_factory is None:
            if fetcher is None:
                msg = "RowProvider requires either engine_factory or fetcher"
                raise ValueError(msg)
            self._fetcher: Callable[[int, int, Sequence[str]], Any] | None = fetcher
            self._engine_factory = None
            self._columns_getter = None
            self._materializer = None
        else:
            if columns_getter is None:
                msg = "columns_getter is required when engine_factory is provided"
                raise ValueError(msg)
            if materializer is None:
                msg = "materializer is required when engine_factory is provided"
                raise ValueError(msg)
            if not is_materializer_compatible(materializer):
                msg = "materializer must implement MaterializerProtocol"
                raise TypeError(msg)
            self._engine_factory = engine_factory
            self._columns_getter = columns_getter
            self._materializer = materializer
            self._fetcher = None

        if empty_result_factory is None:
            msg = "RowProvider requires an empty_result_factory"
            raise ValueError(msg)

        self._empty_result_factory = empty_result_factory
        self._job_context = job_context
        if runner is None:
            msg = "RowProvider requires a JobRunner instance"
            raise ValueError(msg)
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self._runner = runner
        self._empty_template: TableSlice | None = None
        self._cache: OrderedDict[RowKey, TableSlice] = OrderedDict()
        self._cache_cells = 0
        self._cache_evictions = 0
        self._prefetched_keys: set[RowKey] = set()
        self._prefetch_scheduled = 0
        self._prefetch_hits = 0
        self._prefetch_evictions = 0
        self._row_id_column = row_id_column
        self._max_cache_cells = self.MAX_CACHE_CELLS
        self._max_cache_entries = self.MAX_CACHE_ENTRIES
        self._streaming_enabled_configured = streaming_enabled is not None
        self._streaming_enabled = (
            self.STREAMING_ENABLED if streaming_enabled is None else bool(streaming_enabled)
        )
        batch_default = self.STREAMING_BATCH_ROWS
        self._streaming_batch_rows_configured = (
            streaming_batch_rows is not None and streaming_batch_rows > 0
        )
        if streaming_batch_rows is not None and streaming_batch_rows > 0:
            batch_default = int(streaming_batch_rows)
        self._streaming_batch_rows = max(1, batch_default)
        self._streaming_last_chunks = 0
        self._streaming_last_rows = 0
        self._streaming_last_cells = 0
        self._streaming_last_duration_ns = 0
        self._streaming_last_mode = "init"
        self._pending: set[RowKey] = set()
        self._pending_futures: dict[RowKey, Any] = {}
        self._lock = RLock()
        self._source_traits_cache: OrderedDict[str, SourceTraits] = OrderedDict()
        self._strategy: Strategy | None = None
        self._strategy_cache: OrderedDict[str, Strategy] = OrderedDict()
        self._sidecar_states: dict[str, _SidecarState] = {}

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def for_sheet(cls, sheet: Any, *, runner: JobRunnerProtocol) -> RowProvider:
        """Build a provider for ``sheet`` by introspecting available hooks."""

        config_factory = getattr(sheet, "row_provider_config", None)
        if callable(config_factory):
            config = dict(config_factory())
            return cls(runner=runner, **config)

        if sheet_supports(sheet, SHEET_FEATURE_SLICE):

            def fetcher(start: int, count: int, cols: Sequence[str]) -> Any:
                return sheet.fetch_slice(start, count, list(cols))

            def empty_result() -> Any:
                base_columns = list(getattr(sheet, "columns", []))
                try:
                    return sheet.fetch_slice(0, 0, base_columns)
                except Exception:
                    return sheet.fetch_slice(0, 0, [])

            job_ctx = getattr(sheet, "job_context", None)
            return cls(
                fetcher=fetcher,
                job_context=job_ctx,
                runner=runner,
                empty_result_factory=empty_result,
            )

        msg = "Sheet does not expose a supported row interface"
        raise TypeError(msg)

    @classmethod
    def for_plan_source(
        cls,
        *,
        engine_factory: Callable[[], EngineAdapterProtocol],
        columns_getter: Callable[[], Sequence[str]],
        job_context: Callable[[], tuple[str, int, str]] | None,
        materializer: MaterializerProtocol,
        empty_result_factory: Callable[[], Any],
        runner: JobRunnerProtocol,
        row_id_column: str | None = None,
    ) -> RowProvider:
        return cls(
            engine_factory=engine_factory,
            columns_getter=columns_getter,
            job_context=job_context,
            materializer=materializer,
            empty_result_factory=empty_result_factory,
            runner=runner,
            row_id_column=row_id_column,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_slice(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
    ) -> tuple[TableSlice, SliceStatus]:
        """Return ``count`` rows starting from ``start`` for ``columns``."""

        columns = tuple(columns)

        if count <= 0:
            empty = self._empty_slice(columns)
            status = SliceStatus.PARTIAL if columns else SliceStatus.OK
            return empty, status

        context = self._resolve_context(plan, columns)
        if context is None:
            empty = self._empty_slice(columns)
            return empty, SliceStatus.SCHEMA_MISMATCH

        key = self._cache_key(context.plan_hash, start, count, context.fetch_columns)
        with self._lock:
            cached = self._cache.get(key)
            if cached is not None:
                self._cache.move_to_end(key)
                self._note_prefetch_hit_locked(key)
        if cached is not None:
            return self._finalize_slice(context, cached)

        if not context.fetch_columns:
            raw_slice, _ = self._fetch_slice(context, start, count)
            with self._lock:
                self._store_cache_entry_locked(key, raw_slice)
            return self._finalize_slice(context, raw_slice)

        self._ensure_strategy_for_context(context)
        raw_slice, _ = self._fetch_slice(context, start, count)
        with self._lock:
            self._store_cache_entry_locked(key, raw_slice)
        return self._finalize_slice(context, raw_slice)

    def get_slice_stream(self, request: SliceStreamRequest) -> Iterator[TableSliceChunk]:
        """Yield streaming chunks that resolve to the requested slice."""

        columns = tuple(request.columns)
        start = int(request.start)
        request_start = start
        count = int(request.count)
        telemetry_base = dict(request.telemetry or {})

        if count <= 0:
            empty = self._empty_slice(columns)
            status = SliceStatus.PARTIAL if columns else SliceStatus.OK
            telemetry = {
                **telemetry_base,
                "mode": "empty",
                "chunks": 1,
                "rows": 0,
                "cells": 0,
                "duration_ns": 0,
                "offset": request_start,
            }
            with self._lock:
                self._update_streaming_metrics_locked(
                    mode="empty", chunks=1, rows=0, cells=0, duration_ns=0
                )
            yield TableSliceChunk(request_start, empty, status, True, telemetry)
            return

        context = self._resolve_context(request.plan, columns)
        if context is None:
            empty = self._empty_slice(columns)
            telemetry = {
                **telemetry_base,
                "mode": "schema_mismatch",
                "chunks": 1,
                "rows": 0,
                "cells": 0,
                "duration_ns": 0,
                "offset": request_start,
            }
            with self._lock:
                self._update_streaming_metrics_locked(
                    mode="schema_mismatch",
                    chunks=1,
                    rows=0,
                    cells=0,
                    duration_ns=0,
                )
            yield TableSliceChunk(
                request_start, empty, SliceStatus.SCHEMA_MISMATCH, True, telemetry
            )
            return

        if not context.fetch_columns:
            key = self._cache_key(
                context.plan_hash,
                request_start,
                count,
                context.fetch_columns,
            )
            with self._lock:
                cached = self._cache.get(key)
                if cached is not None:
                    self._cache.move_to_end(key)
                    self._note_prefetch_hit_locked(key)

            with self._lock:
                strategy = self._strategy
            strategy_payload = asdict(strategy) if strategy is not None else None

            if cached is not None:
                final_slice, status = self._finalize_slice(context, cached)
                cells = self._cell_count(final_slice)
                telemetry = self._augment_telemetry(
                    {
                        **telemetry_base,
                        "mode": "cache",
                        "chunks": 1,
                        "rows": final_slice.height,
                        "cells": cells,
                        "duration_ns": 0,
                        "offset": request_start,
                        "plan_hash": context.plan_hash,
                    },
                    strategy_payload=strategy_payload,
                )
                with self._lock:
                    self._update_streaming_metrics_locked(
                        mode="cache",
                        chunks=1,
                        rows=final_slice.height,
                        cells=cells,
                        duration_ns=0,
                    )
                self._schedule_prefetch_windows(
                    plan=request.plan,
                    columns=columns,
                    start=request_start,
                    count=count,
                    windows=strategy.prefetch_windows if strategy is not None else 0,
                )
                yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
                return

            raw = self._empty_slice(context.fetch_columns)
            final_slice, status = self._finalize_slice(context, raw)
            cells = self._cell_count(final_slice)
            telemetry = self._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "empty",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
            )
            with self._lock:
                self._store_cache_entry_locked(key, raw)
                self._update_streaming_metrics_locked(
                    mode="empty",
                    chunks=1,
                    rows=final_slice.height,
                    cells=cells,
                    duration_ns=0,
                )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        strategy = self._ensure_strategy_for_context(context)
        window = _SidecarWindow.identity(request_start, count)
        if self._fetcher is None:
            window = self._prepare_sidecar_window(
                context,
                request_start,
                count,
                record_progress=True,
            )

        strategy_payload = asdict(strategy) if strategy is not None else None

        key = self._cache_key(context.plan_hash, request_start, count, context.fetch_columns)
        with self._lock:
            cached = self._cache.get(key)
            if cached is not None:
                self._cache.move_to_end(key)
        if cached is not None:
            final_slice, status = self._finalize_slice(context, cached)
            cells = self._cell_count(final_slice)
            telemetry = self._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "cache",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            with self._lock:
                self._update_streaming_metrics_locked(
                    mode="cache", chunks=1, rows=final_slice.height, cells=cells, duration_ns=0
                )
            self._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        stream_enabled = (
            request.streaming_enabled
            if request.streaming_enabled is not None
            else self._streaming_enabled
        )
        batch_rows = (
            request.batch_rows
            if request.batch_rows and request.batch_rows > 0
            else self._streaming_batch_rows
        )

        if self._fetcher is not None:
            start_ns = monotonic_ns()
            raw_slice, _ = self._fetch_slice(
                context,
                request_start,
                count,
                record_progress=False,
            )
            final_slice, status = self._finalize_slice(context, raw_slice)
            duration_ns = monotonic_ns() - start_ns
            cells = self._cell_count(final_slice)
            telemetry = self._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "passthrough",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": duration_ns,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
            )
            with self._lock:
                self._store_cache_entry_locked(key, raw_slice)
                self._update_streaming_metrics_locked(
                    mode="passthrough",
                    chunks=1,
                    rows=final_slice.height,
                    cells=cells,
                    duration_ns=duration_ns,
                )
            self._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        start_ns = monotonic_ns()
        prepared = self._prepare_materializer(context.plan)
        if prepared is None:
            raw_slice = self._empty_slice(context.fetch_columns)
            final_slice, status = self._finalize_slice(context, raw_slice)
            cells = self._cell_count(final_slice)
            telemetry = self._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": "collect",
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": 0,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            with self._lock:
                self._store_cache_entry_locked(key, raw_slice)
                self._update_streaming_metrics_locked(
                    mode="collect",
                    chunks=1,
                    rows=final_slice.height,
                    cells=cells,
                    duration_ns=0,
                )
            self._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=strategy.prefetch_windows if strategy is not None else 0,
            )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        materializer, physical_plan = prepared
        self._record_source_traits(context.plan, physical_plan)
        stream_attr = getattr(materializer, "collect_slice_stream", None)
        stream_iterator: Iterator[TableSlice] | None = None
        stream_mode = "collect"
        stream_reason = "disabled"
        prefetch_windows = strategy.prefetch_windows if strategy is not None else 0
        prefetch_scheduled = False
        stream_kwargs = {
            "start": window.fetch_start,
            "length": window.fetch_count,
            "columns": tuple(context.fetch_columns),
        }
        if stream_enabled and callable(stream_attr):
            if batch_rows > 0:
                stream_kwargs["batch_rows"] = batch_rows
            try:
                stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
                stream_mode = "stream"
                stream_reason = "stream"
            except TypeError:
                stream_kwargs.pop("batch_rows", None)
                try:
                    stream_iterator = iter(stream_attr(physical_plan, **stream_kwargs))
                    stream_mode = "stream"
                    stream_reason = "stream"
                except TypeError:
                    stream_iterator = None
                    stream_reason = "type_error"
                except PulkaCoreError:
                    raise
                except Exception:
                    stream_iterator = None
                    stream_reason = "error"
            except PulkaCoreError:
                raise
            except Exception:
                stream_iterator = None
                stream_reason = "error"
        else:
            if not stream_enabled:
                stream_reason = "disabled"
            elif stream_attr is None:
                stream_reason = "missing"
            else:
                stream_reason = "invalid"

        if stream_iterator is None:
            try:
                raw = materializer.collect_slice(
                    physical_plan,
                    start=window.fetch_start,
                    length=window.fetch_count,
                    columns=tuple(context.fetch_columns),
                )
            except PulkaCoreError:
                raise
            except Exception as exc:  # pragma: no cover - defensive
                msg = "Failed to materialise row slice"
                raise MaterializeError(msg) from exc
            coerced = self._coerce_slice(raw, row_id_column=self._row_id_column)
            trimmed = self._apply_sidecar_window(coerced, window, count)
            final_slice, status = self._finalize_slice(context, trimmed)
            duration_ns = monotonic_ns() - start_ns
            cells = self._cell_count(final_slice)
            telemetry = self._augment_telemetry(
                {
                    **telemetry_base,
                    "mode": stream_mode,
                    "reason": stream_reason,
                    "chunks": 1,
                    "rows": final_slice.height,
                    "cells": cells,
                    "duration_ns": duration_ns,
                    "offset": request_start,
                    "plan_hash": context.plan_hash,
                },
                strategy_payload=strategy_payload,
                window=window,
            )
            with self._lock:
                self._store_cache_entry_locked(key, trimmed)
                self._update_streaming_metrics_locked(
                    mode=stream_mode,
                    chunks=1,
                    rows=final_slice.height,
                    cells=cells,
                    duration_ns=duration_ns,
                )
            yield TableSliceChunk(request_start, final_slice, status, True, telemetry)
            return

        total_rows = 0
        chunk_index = 0
        last_chunk_ns = start_ns
        skip_rows = window.trim_leading
        assembled_raw: TableSlice | None = None
        try:
            while True:
                try:
                    raw_chunk = next(stream_iterator)
                except StopIteration:
                    break
                chunk_slice = self._coerce_slice(raw_chunk, row_id_column=self._row_id_column)
                if chunk_slice.height <= 0:
                    continue
                if skip_rows > 0:
                    if chunk_slice.height <= skip_rows:
                        skip_rows -= chunk_slice.height
                        continue
                    chunk_slice = chunk_slice.slice(skip_rows, None)
                    skip_rows = 0
                remaining = max(0, count - total_rows)
                if remaining <= 0:
                    break
                if chunk_slice.height > remaining:
                    chunk_slice = chunk_slice.slice(0, remaining)
                if chunk_slice.height <= 0:
                    continue
                chunk_offset = request_start + total_rows
                total_rows += chunk_slice.height
                if chunk_slice.start_offset is None:
                    chunk_slice = TableSlice(
                        tuple(chunk_slice.columns),
                        chunk_slice.schema,
                        start_offset=chunk_offset,
                        row_ids=chunk_slice.row_ids,
                    )
                assembled_raw = (
                    chunk_slice
                    if assembled_raw is None
                    else assembled_raw.concat_vertical(chunk_slice)
                )
                finalized_chunk, chunk_status = self._finalize_slice(context, chunk_slice)
                now_ns = monotonic_ns()
                chunk_duration_ns = now_ns - last_chunk_ns
                last_chunk_ns = now_ns
                chunk_index += 1
                chunk_cells = self._cell_count(finalized_chunk)
                chunk_telemetry = self._augment_telemetry(
                    {
                        **telemetry_base,
                        "mode": stream_mode,
                        "reason": stream_reason,
                        "chunk_index": chunk_index,
                        "rows": finalized_chunk.height,
                        "cells": chunk_cells,
                        "duration_ns": chunk_duration_ns,
                        "offset": chunk_offset,
                        "plan_hash": context.plan_hash,
                    },
                    strategy_payload=strategy_payload,
                    window=window,
                )
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.stream_chunk",
                        extra={
                            "event": "row_stream_chunk",
                            "plan_hash": context.plan_hash,
                            "chunk_index": chunk_index,
                            "rows": finalized_chunk.height,
                            "offset": chunk_offset,
                        },
                    )
                yield TableSliceChunk(
                    chunk_offset,
                    finalized_chunk,
                    chunk_status,
                    False,
                    chunk_telemetry,
                )
                if not prefetch_scheduled and prefetch_windows > 0:
                    self._schedule_prefetch_windows(
                        plan=request.plan,
                        columns=columns,
                        start=request_start,
                        count=count,
                        windows=prefetch_windows,
                    )
                    prefetch_scheduled = True
                chunk_offset += chunk_slice.height
                if total_rows >= count:
                    break
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to materialise streaming slice"
            raise MaterializeError(msg) from exc

        if assembled_raw is None:
            assembled_raw = self._empty_slice(context.fetch_columns)
        total_duration_ns = monotonic_ns() - start_ns
        final_slice, status = self._finalize_slice(context, assembled_raw)
        final_cells = self._cell_count(final_slice)
        total_chunks = chunk_index + 1
        summary_telemetry = self._augment_telemetry(
            {
                **telemetry_base,
                "mode": stream_mode,
                "reason": stream_reason,
                "chunk_index": total_chunks,
                "chunks": total_chunks,
                "rows": final_slice.height,
                "cells": final_cells,
                "duration_ns": total_duration_ns,
                "offset": request_start,
                "plan_hash": context.plan_hash,
            },
            strategy_payload=strategy_payload,
            window=window,
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.stream_complete",
                extra={
                    "event": "row_stream_complete",
                    "plan_hash": context.plan_hash,
                    "chunks": total_chunks,
                    "rows": final_slice.height,
                    "duration_ns": total_duration_ns,
                },
            )
        with self._lock:
            self._store_cache_entry_locked(key, assembled_raw)
            self._update_streaming_metrics_locked(
                mode=stream_mode,
                chunks=total_chunks,
                rows=final_slice.height,
                cells=final_cells,
                duration_ns=total_duration_ns,
            )
        if not prefetch_scheduled and prefetch_windows > 0:
            self._schedule_prefetch_windows(
                plan=request.plan,
                columns=columns,
                start=request_start,
                count=count,
                windows=prefetch_windows,
            )
            prefetch_scheduled = True
        yield TableSliceChunk(request_start, final_slice, status, True, summary_telemetry)

    def build_plan_compiler(self) -> EngineAdapterProtocol | None:
        """Return an engine adapter for validation when exposed by the sheet."""

        return self._engine_adapter()

    def prefetch(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
    ) -> None:
        """Warm ``[start, start + count)`` in the background when possible."""

        if count <= 0:
            return

        if self._fetcher is not None:
            # Nothing clever to do for passthrough providers.
            return

        columns = tuple(columns)
        context = self._resolve_context(plan, columns)
        if context is None or not context.fetch_columns:
            return

        if context.sheet_id is None or context.generation is None:
            return

        key = self._cache_key(context.plan_hash, start, count, context.fetch_columns)
        scheduled = False
        with self._lock:
            if key in self._pending or key in self._cache:
                return
            self._pending.add(key)
            self._prefetch_scheduled += 1
            scheduled = True

        tag_hash = context.plan_hash or "none"
        cols_sig = normalized_columns_key(context.fetch_columns)
        job_tag = f"rows:{tag_hash}:{start}:{count}:{cols_sig}"

        def _job(_: int) -> Any:
            slice_result, _prefetch_window = self._fetch_slice(
                context,
                start,
                count,
                record_progress=False,
            )
            return slice_result

        req = JobRequest(
            sheet_id=context.sheet_id,
            generation=context.generation,
            tag=job_tag,
            fn=_job,
            cache_result=False,
        )
        future = self._runner.enqueue(req)
        with self._lock:
            self._pending_futures[key] = future
            scheduled_count = self._prefetch_scheduled
        if scheduled and LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.prefetch_schedule",
                extra={
                    "event": "row_prefetch_schedule",
                    "plan_hash": context.plan_hash,
                    "start": start,
                    "count": count,
                    "columns": cols_sig,
                    "scheduled": scheduled_count,
                },
            )

        def _store_result(fut: Any, *, row_key: RowKey = key) -> None:
            with self._lock:
                self._pending.discard(row_key)
                self._pending_futures.pop(row_key, None)

            try:
                result = fut.result()
            except Exception:
                return

            if getattr(result, "error", None) is not None:
                return

            value = getattr(result, "value", None)
            generation = getattr(result, "generation", None)
            if generation != context.generation:
                return

            if value is None:
                return

            with self._lock:
                self._store_cache_entry_locked(row_key, value, prefetched=True)

        future.add_done_callback(_store_result)

    def current_cell_value(
        self,
        plan: QueryPlan | None,
        column: str,
        row: int,
        *,
        preview_chars: int = 160,
    ) -> CellPreview | None:
        """Return a lightweight preview for ``column`` at ``row``."""

        if row < 0:
            return None

        slice_, _status = self.get_slice(plan, (column,), row, 1)
        if slice_.height <= 0:
            return None

        try:
            table_column = slice_.column(column)
        except KeyError:
            return None

        values = table_column.values
        try:
            raw_value = values[0]
        except (IndexError, TypeError):
            return None
        display, truncated = summarize_value_preview(raw_value, max_chars=preview_chars)
        dtype = str(table_column.dtype) if table_column.dtype is not None else None
        absolute_row = slice_.start_offset
        if absolute_row is None:
            absolute_row = row

        return CellPreview(
            column=column,
            row=row,
            absolute_row=absolute_row,
            dtype=dtype,
            raw_value=raw_value,
            display=display,
            truncated=truncated,
        )

    def get_source_traits(self, plan: QueryPlan | None) -> SourceTraits | None:
        """Return cached or inferred source traits for ``plan`` when available."""

        effective_plan = plan or QueryPlan()
        key = self._plan_signature(effective_plan)
        with self._lock:
            cached = self._source_traits_cache.get(key)
        if cached is not None:
            return cached

        if self._fetcher is not None:
            return None

        prepared = self._prepare_materializer(effective_plan)
        if prepared is None:
            return None
        _materializer, physical_plan = prepared
        self._record_source_traits(effective_plan, physical_plan)
        with self._lock:
            return self._source_traits_cache.get(key)

    def _ensure_strategy_for_context(self, context: _PlanContext) -> Strategy | None:
        plan = context.plan
        key = self._plan_signature(plan)
        with self._lock:
            cached = self._strategy_cache.get(key)
            if cached is not None:
                self._apply_strategy_locked(cached)
                return cached

        traits = self.get_source_traits(plan)
        if traits is None:
            return None

        strategy = compile_strategy(traits)
        with self._lock:
            cache = self._strategy_cache
            cache[key] = strategy
            cache.move_to_end(key)
            while len(cache) > self.STRATEGY_CACHE_LIMIT:
                cache.popitem(last=False)
            self._apply_strategy_locked(strategy)
        return strategy

    def _apply_strategy_locked(self, strategy: Strategy) -> None:
        self._strategy = strategy
        if not self._streaming_enabled_configured:
            self._streaming_enabled = strategy.mode == "streaming"
        if not self._streaming_batch_rows_configured:
            self._streaming_batch_rows = max(1, strategy.batch_rows)

    def clear(self) -> None:
        """Cancel pending work and drop cached prefetches."""

        with self._lock:
            for future in self._pending_futures.values():
                future.cancel()
            self._pending_futures.clear()
            self._pending.clear()
            self._cache.clear()
            self._cache_cells = 0
            self._source_traits_cache.clear()
            self._strategy_cache.clear()
            self._strategy = None
            self._sidecar_states.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _resolve_context(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
    ) -> _PlanContext | None:
        requested = tuple(columns)
        if self._fetcher is not None:
            sheet_id, generation, plan_hash = self._current_job_metadata(plan)
            effective_plan = plan or QueryPlan()
            base_columns = tuple(self._schema_template().column_names)
            available_set = set(base_columns)
            present = tuple(col for col in requested if col in available_set)
            missing = tuple(col for col in requested if col not in available_set)
            return _PlanContext(
                effective_plan,
                present,
                requested,
                missing,
                plan_hash,
                sheet_id,
                generation,
            )

        if self._engine_factory is None or self._columns_getter is None:
            return None

        available_columns = tuple(self._columns_getter())
        row_id_column = self._row_id_column
        if not available_columns:
            sheet_id, generation, plan_hash = self._current_job_metadata(plan)
            effective_plan = plan or QueryPlan()
            missing = tuple(requested)
            return _PlanContext(
                effective_plan,
                (),
                requested,
                missing,
                plan_hash,
                sheet_id,
                generation,
            )

        available_set = set(available_columns)
        if row_id_column:
            available_set.add(row_id_column)
        present = tuple(col for col in requested if col in available_set)

        effective_plan = (plan or QueryPlan()).with_limit(None).with_offset(0)

        if effective_plan.projection:
            plan_for_fetch = effective_plan
        else:
            projection: list[str] = []
            for name in present:
                if name not in projection:
                    projection.append(name)
            for column, _ in effective_plan.sort:
                if column in available_set and column not in projection:
                    projection.append(column)
            if not projection:
                projection = list(available_columns)
            plan_for_fetch = effective_plan.with_projection(projection)

        if plan_for_fetch.projection:
            visible_columns = tuple(name for name in present if name in plan_for_fetch.projection)
        else:
            visible_columns = present

        def _dedup(seq: Sequence[str]) -> tuple[str, ...]:
            seen: set[str] = set()
            unique: list[str] = []
            for name in seq:
                if name in seen:
                    continue
                seen.add(name)
                unique.append(name)
            return tuple(unique)

        if row_id_column and row_id_column in available_set:
            projection_for_fetch = (
                list(plan_for_fetch.projection) if plan_for_fetch.projection else []
            )
            if row_id_column not in projection_for_fetch:
                projection_for_fetch.append(row_id_column)
                plan_for_fetch = plan_for_fetch.with_projection(_dedup(projection_for_fetch))

        sheet_id, generation, plan_hash = self._current_job_metadata(plan_for_fetch)
        missing = tuple(col for col in requested if col not in available_set)
        fetch_columns: tuple[str, ...]
        if row_id_column and row_id_column in available_set:
            fetch_columns = _dedup(list(visible_columns) + [row_id_column])
        else:
            fetch_columns = visible_columns
        return _PlanContext(
            plan_for_fetch,
            fetch_columns,
            requested,
            missing,
            plan_hash,
            sheet_id,
            generation,
        )

    def _collect_plan_slice(
        self,
        plan: QueryPlan,
        start: int,
        count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        prepared = self._prepare_materializer(plan)
        if prepared is None:
            return self._empty_slice(columns)
        materializer, physical_plan = prepared
        self._record_source_traits(plan, physical_plan)

        try:
            raw = materializer.collect_slice(
                physical_plan,
                start=start,
                length=count,
                columns=tuple(columns),
            )
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to materialise row slice"
            raise MaterializeError(msg) from exc
        return self._coerce_slice(raw, row_id_column=self._row_id_column)

    def _prepare_sidecar_window(
        self,
        context: _PlanContext,
        start: int,
        count: int,
        *,
        record_progress: bool,
    ) -> _SidecarWindow:
        if self._fetcher is not None or count <= 0 or start < 0:
            return _SidecarWindow.identity(start, count)

        with self._lock:
            strategy = self._strategy
        if strategy is None or strategy.build_sidecar_after_screens is None:
            return _SidecarWindow.identity(start, count)

        traits = self.get_source_traits(context.plan)
        if traits is None or traits.kind not in {"csv", "tsv", "jsonl"}:
            return _SidecarWindow.identity(start, count)

        path = traits.path
        if not path:
            return _SidecarWindow.identity(start, count)

        interval = max(1, csv_checkpoints.CHECKPOINT_EVERY_ROWS)

        with self._lock:
            state = self._get_or_create_sidecar_state_locked(path)
            if context.generation is not None and state.generation != context.generation:
                state.progress.reset()
                state.generation = context.generation
                state.building = False
                state.failed = False

            if record_progress:
                state.progress.observe(start=start, span=count)
            elif count > 0 and state.progress.last_span <= 0:
                state.progress.last_span = count

            offsets = state.offsets
            threshold = strategy.build_sidecar_after_screens
            should_schedule = (
                record_progress
                and threshold is not None
                and state.progress.screens_seen >= threshold
                and not state.building
                and not state.failed
                and offsets is None
            )
            if should_schedule:
                self._schedule_sidecar_job_locked(state, path, context, interval)
            offsets = state.offsets

        if not offsets or len(offsets) <= 1:
            return _SidecarWindow.identity(start, count)

        index = max(0, min(len(offsets) - 1, start // interval))
        checkpoint_row = index * interval
        if checkpoint_row >= start and index > 0:
            checkpoint_row = (index - 1) * interval

        if checkpoint_row < 0 or checkpoint_row >= start:
            return _SidecarWindow.identity(start, count)

        trim_leading = start - checkpoint_row
        if trim_leading <= 0:
            return _SidecarWindow.identity(start, count)

        fetch_count = count + trim_leading
        return _SidecarWindow(
            fetch_start=checkpoint_row,
            fetch_count=fetch_count,
            trim_leading=trim_leading,
            used=True,
            checkpoint_row=checkpoint_row,
        )

    def _get_or_create_sidecar_state_locked(self, path: str) -> _SidecarState:
        state = self._sidecar_states.get(path)
        if state is not None:
            return state

        store = SidecarStore(path)
        offsets: tuple[int, ...] | None = None
        if store.has(csv_checkpoints.CHECKPOINT_ARTIFACT):
            try:
                offsets = store.read_offsets(csv_checkpoints.CHECKPOINT_ARTIFACT)
            except Exception as exc:  # pragma: no cover - defensive guardrail
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.sidecar_load_failed",
                        extra={
                            "event": "row_sidecar_load_failed",
                            "path": path,
                        },
                        exc_info=exc,
                    )
                offsets = None

        state = _SidecarState(store=store, offsets=offsets)
        self._sidecar_states[path] = state
        return state

    def _schedule_sidecar_job_locked(
        self,
        state: _SidecarState,
        path: str,
        context: _PlanContext,
        interval: int,
    ) -> None:
        sheet_id = context.sheet_id
        generation = context.generation
        if sheet_id is None or generation is None:
            return

        job_tag = f"sidecar:{state.store.key}:{csv_checkpoints.CHECKPOINT_ARTIFACT}"

        def _job(
            _: int,
            *,
            _path: str = path,
            _store: SidecarStore = state.store,
            _interval: int = interval,
        ) -> tuple[int, ...] | None:
            return csv_checkpoints.build_csv_checkpoints(_path, store=_store, every_n=_interval)

        req = JobRequest(
            sheet_id=sheet_id,
            generation=generation,
            tag=job_tag,
            fn=_job,
            cache_result=False,
        )

        future = self._runner.enqueue(req)
        state.building = True
        state.failed = False

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.sidecar_schedule",
                extra={
                    "event": "row_sidecar_schedule",
                    "path": path,
                    "interval": interval,
                    "plan_hash": context.plan_hash,
                },
            )

        def _on_done(fut: Any) -> None:
            try:
                result = fut.result()
            except Exception as exc:  # pragma: no cover - defensive guardrail
                if LOGGER.isEnabledFor(logging.WARNING):
                    LOGGER.warning(
                        "row_provider.sidecar_error",
                        extra={
                            "event": "row_sidecar_error",
                            "path": path,
                        },
                        exc_info=exc,
                    )
                with self._lock:
                    state.building = False
                    state.failed = True
                return

            if result.error is not None:
                if LOGGER.isEnabledFor(logging.WARNING):
                    LOGGER.warning(
                        "row_provider.sidecar_error",
                        extra={
                            "event": "row_sidecar_error",
                            "path": path,
                        },
                        exc_info=result.error,
                    )
                with self._lock:
                    state.building = False
                    state.failed = True
                return

            offsets_value = result.value or ()
            if result.generation != generation:
                with self._lock:
                    state.building = False
                return

            offsets_tuple = tuple(offsets_value)
            with self._lock:
                state.building = False
                state.offsets = offsets_tuple
                state.failed = False

        future.add_done_callback(_on_done)

    def _apply_sidecar_window(
        self,
        raw_slice: TableSlice,
        window: _SidecarWindow,
        requested_count: int,
    ) -> TableSlice:
        trimmed = raw_slice
        if window.trim_leading > 0:
            trimmed = trimmed.slice(window.trim_leading, None)

        if requested_count >= 0 and trimmed.height > requested_count:
            trimmed = trimmed.slice(0, requested_count)

        return trimmed

    def _prepare_materializer(self, plan: QueryPlan) -> tuple[MaterializerProtocol, Any] | None:
        adapter = self._engine_adapter()
        materializer = self._materializer
        if adapter is None or materializer is None:
            return None
        try:
            physical_plan = adapter.compile(plan)
        except PulkaCoreError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            msg = "Failed to compile plan for row slice"
            raise CompileError(msg) from exc
        return materializer, physical_plan

    def _record_source_traits(self, plan: QueryPlan, physical_plan: Any) -> None:
        traits = self._infer_source_traits_from_physical_plan(physical_plan)
        if traits is None:
            return
        key = self._plan_signature(plan)
        with self._lock:
            cache = self._source_traits_cache
            cache[key] = traits
            cache.move_to_end(key)
            while len(cache) > self.SOURCE_TRAITS_CACHE_LIMIT:
                cache.popitem(last=False)
            self._strategy_cache.pop(key, None)

    @staticmethod
    def _infer_source_traits_from_physical_plan(plan: Any) -> SourceTraits | None:
        try:
            from .engine.viewer_engine import infer_source_traits_from_plan
        except Exception:
            return None
        try:
            return infer_source_traits_from_plan(plan)
        except Exception:
            return None

    @staticmethod
    def _plan_signature(plan: QueryPlan) -> str:
        snapshot = plan.snapshot()
        return cast(str, snapshot["hash"])

    def _fetch_slice(
        self,
        context: _PlanContext,
        start: int,
        count: int,
        *,
        window: _SidecarWindow | None = None,
        record_progress: bool = True,
    ) -> tuple[TableSlice, _SidecarWindow]:
        if not context.fetch_columns:
            empty = self._empty_slice(context.fetch_columns)
            return empty, _SidecarWindow.identity(start, count)

        if self._fetcher is not None:
            raw = self._fetcher(start, count, context.fetch_columns)
            coerced = self._coerce_slice(raw, row_id_column=self._row_id_column)
            if coerced.start_offset is None:
                coerced = TableSlice(
                    coerced.columns,
                    coerced.schema,
                    start_offset=start,
                    row_ids=coerced.row_ids,
                )
            return coerced, _SidecarWindow.identity(start, count)

        effective_window = window or self._prepare_sidecar_window(
            context,
            start,
            count,
            record_progress=record_progress,
        )
        fetch_start = effective_window.fetch_start
        fetch_count = effective_window.fetch_count
        raw = self._collect_plan_slice(
            context.plan,
            fetch_start,
            fetch_count,
            context.fetch_columns,
        )
        if raw.start_offset is None:
            raw = TableSlice(
                raw.columns,
                raw.schema,
                start_offset=fetch_start,
                row_ids=raw.row_ids,
            )
        trimmed = self._apply_sidecar_window(raw, effective_window, count)
        return trimmed, effective_window

    def _engine_adapter(self) -> EngineAdapterProtocol | None:
        if self._engine_factory is None:
            return None
        adapter = self._engine_factory()
        if not isinstance(adapter, EngineAdapterProtocol):
            msg = "engine_factory must return an EngineAdapterProtocol"
            raise TypeError(msg)
        return adapter

    def _empty_slice(self, columns: Sequence[str] | None = None) -> TableSlice:
        template = self._schema_template()
        if columns is None:
            return TableSlice.empty(template.column_names, template.schema)
        return TableSlice.empty(columns, template.schema)

    @staticmethod
    def _coerce_slice(result: Any, *, row_id_column: str | None = None) -> TableSlice:
        if isinstance(result, TableSlice):
            return result
        if result is None:
            return TableSlice.empty()
        if isinstance(result, pl.DataFrame):
            schema = getattr(result, "schema", {})
            return table_slice_from_dataframe(result, schema, row_id_column=row_id_column)
        try:
            frame = pl.DataFrame(result)
        except Exception as exc:  # pragma: no cover - defensive
            msg = (
                "RowProvider requires slice results compatible with TableSlice; "
                f"received {type(result)!r}"
            )
            raise MaterializeError(msg) from exc
        return table_slice_from_dataframe(frame, frame.schema, row_id_column=row_id_column)

    def _schema_template(self) -> TableSlice:
        template = self._empty_template
        if template is None:
            template = self._coerce_slice(
                self._empty_result_factory(), row_id_column=self._row_id_column
            )
            self._empty_template = template
        return template

    def _finalize_slice(
        self,
        context: _PlanContext,
        raw_slice: TableSlice,
    ) -> tuple[TableSlice, SliceStatus]:
        status = SliceStatus.OK
        if context.missing_columns:
            status = self._merge_status(status, SliceStatus.PARTIAL)

        template = self._schema_template()
        schema = dict(template.schema)
        schema.update(raw_slice.schema)

        row_id_column = self._row_id_column

        raw_columns = {column.name: column for column in raw_slice.columns}
        raw_height = raw_slice.height

        row_ids = raw_slice.row_ids
        if row_id_column:
            column = raw_columns.pop(row_id_column, None)
            if row_ids is None and column is not None:
                row_ids = getattr(column, "data", None) or column.values

        result_columns: list[TableColumn] = []

        effective_expected = [
            name for name in context.fetch_columns if not row_id_column or name != row_id_column
        ]
        expected_fetch = set(effective_expected)
        missing_from_raw = [name for name in effective_expected if name not in raw_columns]
        if missing_from_raw:
            status = self._merge_status(status, SliceStatus.SCHEMA_MISMATCH)

        extra_columns = [
            name
            for name in raw_columns
            if name not in expected_fetch and (not row_id_column or name != row_id_column)
        ]
        if extra_columns:
            status = self._merge_status(status, SliceStatus.SCHEMA_MISMATCH)

        placeholder_reason = (
            SliceStatus.SCHEMA_MISMATCH
            if status is SliceStatus.SCHEMA_MISMATCH
            else SliceStatus.PARTIAL
        )

        for name in context.requested_columns:
            column = raw_columns.get(name)
            if column is not None:
                result_columns.append(column)
                continue
            dtype = schema.get(name)
            result_columns.append(
                self._placeholder_column(name, raw_height, dtype, placeholder_reason)
            )

        if not result_columns and raw_columns:
            result_columns.extend(raw_columns[name] for name in raw_slice.column_names)

        if row_id_column and row_ids is None and raw_height > 0:
            base_start = raw_slice.start_offset if raw_slice.start_offset is not None else 0
            row_ids = tuple(base_start + idx for idx in range(raw_height))

        final_slice = TableSlice(
            tuple(result_columns),
            schema,
            start_offset=raw_slice.start_offset,
            row_ids=row_ids,
        )
        return final_slice, status

    def _placeholder_column(
        self,
        name: str,
        height: int,
        dtype: Any,
        status: SliceStatus,
    ) -> TableColumn:
        values = tuple(None for _ in range(max(0, height)))
        null_count = len(values)

        label = "⟂ missing" if status is SliceStatus.PARTIAL else "⟂ schema"

        def _display(
            _row: int,
            _abs_row: int,
            _value: Any,
            _width: int | None,
            *,
            _label: str = label,
        ) -> str:
            return _label

        return TableColumn(name, values, dtype, null_count, _display)

    @staticmethod
    def _merge_status(left: SliceStatus, right: SliceStatus) -> SliceStatus:
        if right is SliceStatus.SCHEMA_MISMATCH:
            return SliceStatus.SCHEMA_MISMATCH
        if right is SliceStatus.PARTIAL and left is SliceStatus.OK:
            return SliceStatus.PARTIAL
        return left

    def _store_cache_entry_locked(
        self, key: RowKey, value: TableSlice, *, prefetched: bool = False
    ) -> None:
        existing = self._cache.pop(key, None)
        if existing is not None:
            self._cache_cells -= self._cell_count(existing)
            self._prefetched_keys.discard(key)
        self._cache[key] = value
        self._cache.move_to_end(key)
        self._cache_cells += self._cell_count(value)
        if prefetched:
            self._prefetched_keys.add(key)
        else:
            self._prefetched_keys.discard(key)
        self._enforce_cache_limits_locked()

    def _enforce_cache_limits_locked(self) -> None:
        while len(self._cache) > self._max_cache_entries or (
            self._max_cache_cells and self._cache_cells > self._max_cache_cells
        ):
            old_key, old_value = self._cache.popitem(last=False)
            removed_cells = self._cell_count(old_value)
            self._cache_cells -= removed_cells
            self._pending.discard(old_key)
            self._pending_futures.pop(old_key, None)
            if old_key in self._prefetched_keys:
                self._prefetched_keys.discard(old_key)
                self._prefetch_evictions += 1
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "row_provider.prefetch_evicted",
                        extra={
                            "event": "row_prefetch_evicted",
                            "plan_hash": old_key[0],
                            "start": old_key[1],
                            "count": old_key[2],
                            "columns": old_key[3],
                            "evictions": self._prefetch_evictions,
                        },
                    )
            self._cache_evictions += 1
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(
                    "row_provider.cache_eviction",
                    extra={
                        "event": "row_cache_eviction",
                        "plan_hash": old_key[0],
                        "start": old_key[1],
                        "count": old_key[2],
                        "columns": old_key[3],
                        "cells": removed_cells,
                        "evictions": self._cache_evictions,
                    },
                )

    @staticmethod
    def _cell_count(slice_: TableSlice) -> int:
        return slice_.height * len(slice_.column_names)

    @staticmethod
    def _augment_telemetry(
        payload: dict[str, Any],
        *,
        strategy_payload: dict[str, Any] | None,
        window: _SidecarWindow | None = None,
    ) -> dict[str, Any]:
        if strategy_payload is not None:
            payload["strategy"] = strategy_payload
        if window is not None and window.used:
            payload["sidecar"] = "checkpoints_used"
            if window.checkpoint_row is not None:
                payload["sidecar_checkpoint_row"] = window.checkpoint_row
        return payload

    def _update_streaming_metrics_locked(
        self,
        *,
        mode: str,
        chunks: int,
        rows: int,
        cells: int,
        duration_ns: int,
    ) -> None:
        self._streaming_last_mode = mode
        self._streaming_last_chunks = max(0, chunks)
        self._streaming_last_rows = max(0, rows)
        self._streaming_last_cells = max(0, cells)
        self._streaming_last_duration_ns = max(0, duration_ns)

    def cache_metrics(self) -> dict[str, int | str]:
        """Return current cache occupancy and eviction counters."""

        with self._lock:
            return {
                "entries": len(self._cache),
                "cells": self._cache_cells,
                "evictions": self._cache_evictions,
                "prefetch_scheduled": self._prefetch_scheduled,
                "prefetch_hits": self._prefetch_hits,
                "prefetch_evictions": self._prefetch_evictions,
                "max_entries": self._max_cache_entries,
                "max_cells": self._max_cache_cells,
                "streaming_last_mode": self._streaming_last_mode,
                "streaming_last_chunks": self._streaming_last_chunks,
                "streaming_last_rows": self._streaming_last_rows,
                "streaming_last_cells": self._streaming_last_cells,
                "streaming_last_duration_ns": self._streaming_last_duration_ns,
            }

    def _current_job_metadata(
        self, plan: QueryPlan | None
    ) -> tuple[str | None, int | None, str | None]:
        if self._job_context is None:
            plan_hash = plan.snapshot()["hash"] if plan is not None else None
            return None, None, plan_hash

        sheet_id, generation, plan_hash = self._job_context()
        if plan_hash is None and plan is not None:
            plan_hash = plan.snapshot()["hash"]
        return sheet_id, generation, plan_hash

    def _note_prefetch_hit_locked(self, key: RowKey) -> None:
        if key not in self._prefetched_keys:
            return
        self._prefetched_keys.discard(key)
        self._prefetch_hits += 1
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "row_provider.prefetch_hit",
                extra={
                    "event": "row_prefetch_hit",
                    "plan_hash": key[0],
                    "start": key[1],
                    "count": key[2],
                    "columns": key[3],
                    "hits": self._prefetch_hits,
                },
            )

    def _schedule_prefetch_windows(
        self,
        *,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
        windows: int,
    ) -> None:
        if windows <= 0 or count <= 0:
            return
        for window_index in range(1, windows + 1):
            next_start = start + window_index * count
            self.prefetch(plan, columns, next_start, count)

    @staticmethod
    def _cache_key(
        plan_hash: str | None,
        start: int,
        count: int,
        columns: Sequence[str],
    ) -> RowKey:
        cols_sig = normalized_columns_key(columns)
        return plan_hash, start, count, cols_sig


__all__ = [
    "CellPreview",
    "RowProvider",
    "SliceStatus",
    "SliceStreamRequest",
    "TableSliceChunk",
]

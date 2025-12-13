from __future__ import annotations

import contextlib
import math
import threading
import weakref
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import Future
from dataclasses import dataclass, field
from time import monotonic_ns
from typing import TYPE_CHECKING, Any

from ...config.settings import CACHE_DEFAULTS, STREAMING_DEFAULTS
from ..engine.contracts import TableSlice
from ..formatting import _format_float_two_decimals, _is_float_like
from ..row_provider import SliceStatus, SliceStreamRequest, TableSliceChunk

if TYPE_CHECKING:
    from .viewer import Viewer


@dataclass(slots=True)
class FreezePaneController:
    """Manage frozen row/column state for a :class:`Viewer`."""

    viewer: Viewer
    column_count: int = 0
    row_count: int = 0
    _columns_cache_valid: bool = False
    _column_indices_cache: tuple[int, ...] = field(default_factory=tuple)
    _column_names_cache: tuple[str, ...] = field(default_factory=tuple)
    _column_index_set_cache: frozenset[int] = frozenset()
    _column_name_set_cache: frozenset[str] = frozenset()

    def invalidate_cache(self) -> None:
        self._columns_cache_valid = False

    def ensure_cache(self) -> None:
        if self._columns_cache_valid:
            return

        viewer = self.viewer
        if self.column_count <= 0:
            self._column_indices_cache = ()
            self._column_names_cache = ()
            self._column_index_set_cache = frozenset()
            self._column_name_set_cache = frozenset()
            self._columns_cache_valid = True
            return

        indices: list[int] = []
        names: list[str] = []
        for idx, name in enumerate(viewer.columns):
            if name in viewer._hidden_cols:
                continue
            indices.append(idx)
            names.append(name)
            if len(indices) >= self.column_count:
                break

        self._column_indices_cache = tuple(indices)
        self._column_names_cache = tuple(names)
        self._column_index_set_cache = frozenset(indices)
        self._column_name_set_cache = frozenset(names)
        self._columns_cache_valid = True

    def column_indices(self) -> list[int]:
        self.ensure_cache()
        return list(self._column_indices_cache)

    def first_scrollable_col_index(self) -> int:
        indices = self.column_indices()
        if not indices:
            return 0
        last = indices[-1]
        return min(len(self.viewer.columns), last + 1)

    def is_column_frozen(self, idx: int) -> bool:
        self.ensure_cache()
        return idx in self._column_index_set_cache

    def effective_row_count(self) -> int:
        return max(0, self.row_count)

    def reserved_view_rows(self) -> int:
        viewer = self.viewer

        if viewer.view_height <= 1:
            return 0

        visible = viewer.visible_frozen_row_count
        if visible <= 0:
            visible = self.effective_row_count()
        return max(0, min(visible, viewer.view_height - 1))

    def body_view_height(self) -> int:
        viewer = self.viewer
        reserved = self.reserved_view_rows()
        margin = 1 if reserved and (viewer.view_height - reserved) >= 2 else 0
        return max(1, viewer.view_height - reserved - margin)

    def frozen_column_names(self) -> list[str]:
        self.ensure_cache()
        return list(self._column_names_cache)

    def column_index_set(self) -> frozenset[int]:
        self.ensure_cache()
        return self._column_index_set_cache

    def column_name_set(self) -> frozenset[str]:
        self.ensure_cache()
        return self._column_name_set_cache

    def set_frozen_columns(self, count: int) -> None:
        viewer = self.viewer
        new_count = max(0, count)
        if new_count == self.column_count:
            return

        self.column_count = new_count
        viewer._visible_key = None
        viewer._max_visible_col = None
        self.invalidate_cache()
        viewer.clamp()

    def set_frozen_rows(self, count: int) -> None:
        viewer = self.viewer
        new_count = max(0, count)
        if new_count == self.row_count:
            return

        self.row_count = new_count
        if self.row_count:
            viewer.row0 = max(viewer.row0, self.row_count)
        viewer.invalidate_row_cache()
        viewer.clamp()

    def clear(self) -> None:
        viewer = self.viewer
        if not (self.column_count or self.row_count):
            return

        self.column_count = 0
        self.row_count = 0
        viewer._visible_key = None
        viewer._max_visible_col = None
        self.invalidate_cache()
        viewer.invalidate_row_cache()
        viewer.clamp()


@dataclass(slots=True)
class _StreamContext:
    sheet_id: str | None
    generation: int | None
    plan_hash: str | None
    plan: Any
    columns: tuple[str, ...]
    column_count: int
    fetch_start: int
    fetch_count: int
    target_start: int
    target_end: int
    body_start: int
    body_end_needed: int
    direction: int
    backward_extra: int
    forward_extra: int
    window_cells_cap: int
    prefetch_span: int
    cache_status: str
    start_ns: int
    first_chunk_ns: int
    status: SliceStatus = SliceStatus.OK
    fetched_cells: int = 0
    batches: int = 0
    mode: str | None = None
    reason: str | None = None
    evicted_rows: int = 0
    prefetch_dir: str = "none"
    prefetch_rows: int = 0
    first_chunk_rows: int = 0
    first_chunk_cells: int = 0
    first_chunk_duration_ns: int = 0
    final_rows: int = 0
    final_cells: int = 0
    final_duration_ns: int = 0
    cancelled: bool = False


@dataclass(slots=True)
class RowCacheController:
    """Cache viewport slices to accelerate vertical scrolling."""

    DEFAULT_MAX_CELLS = CACHE_DEFAULTS.viewer_row_cache_max_cells
    APPROX_BYTES_PER_CELL = 16

    viewer: Viewer
    freeze: FreezePaneController
    streaming_enabled: bool = STREAMING_DEFAULTS.enabled
    streaming_batch_rows: int = STREAMING_DEFAULTS.batch_rows
    table: TableSlice | None = None
    start: int = 0
    end: int = 0
    cols: tuple[str, ...] = field(default_factory=tuple)
    plan_hash: str | None = None
    prefetch: int | None = None
    max_cells: int = DEFAULT_MAX_CELLS
    _visible_row_positions: list[int] = field(default_factory=list)
    _visible_frozen_row_count: int = 0
    _sheet_version: object | None = None
    _last_body_start: int | None = None
    _last_direction: int = 0
    _table_status: SliceStatus = SliceStatus.OK
    _last_warning_status: SliceStatus = SliceStatus.OK
    _stream_forced_eager: bool = False
    _active_stream_future: Future[Any] | None = None
    _active_stream_generation: int | None = None
    _active_stream_start_ns: int = 0
    _active_stream_first_chunk_ns: int = 0
    _active_stream_batches: int = 0
    _active_stream_rows: int = 0
    _active_stream_cells: int = 0
    _active_stream_mode: str | None = None
    _active_stream_reason: str | None = None
    _active_stream_prefetch_dir: str = "none"
    _active_stream_prefetch_rows: int = 0
    _active_stream_evicted_rows: int = 0
    _active_stream_context: _StreamContext | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cancel_active_stream(self) -> None:
        context = self._active_stream_context
        if context is not None:
            context.cancelled = True
        future = self._active_stream_future
        if future is not None:
            future.cancel()
        self._active_stream_future = None
        self._active_stream_generation = None
        self._active_stream_start_ns = 0
        self._active_stream_first_chunk_ns = 0
        self._active_stream_batches = 0
        self._active_stream_rows = 0
        self._active_stream_cells = 0
        self._active_stream_mode = None
        self._active_stream_reason = None
        self._active_stream_prefetch_dir = "none"
        self._active_stream_prefetch_rows = 0
        self._active_stream_evicted_rows = 0
        self._active_stream_context = None

    def _should_stream(self) -> bool:
        if not self.streaming_enabled:
            return False
        if self.streaming_batch_rows <= 0:
            return False
        if self._stream_forced_eager:
            return False
        viewer = self.viewer
        sheet_id = getattr(viewer.sheet, "sheet_id", None)
        return sheet_id is not None

    def _trim_table_for_budget(
        self,
        table: TableSlice,
        *,
        start: int,
        body_start: int,
        body_end_needed: int,
        direction: int,
        column_count: int,
        window_cells_cap: int,
    ) -> tuple[TableSlice, int, int, int]:
        total_rows = table.height
        if total_rows <= 0:
            return table, start, start, 0

        max_rows_allowed = max(1, window_cells_cap // max(1, column_count))
        keep_start = start
        keep_end = start + total_rows

        if direction > 0:
            keep_end = min(start + total_rows, keep_start + max_rows_allowed)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - max_rows_allowed)
        elif direction < 0:
            keep_start = start
            keep_end = min(start + total_rows, keep_start + max_rows_allowed)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - max_rows_allowed)
            if keep_start > body_start:
                keep_start = body_start
                keep_end = min(start + total_rows, keep_start + max_rows_allowed)
        else:
            keep_span = max_rows_allowed
            keep_start = max(
                start,
                body_start - max(0, keep_span - (body_end_needed - body_start)) // 2,
            )
            keep_end = min(start + total_rows, keep_start + keep_span)
            if keep_start > body_start:
                keep_start = body_start
                keep_end = min(start + total_rows, keep_start + keep_span)
            if keep_end < body_end_needed:
                keep_end = body_end_needed
                keep_start = max(start, keep_end - keep_span)

        keep_start = max(start, keep_start)
        keep_end = min(start + total_rows, keep_end)
        keep_end = max(keep_end, keep_start)

        evicted_rows = 0
        trim_front = max(0, keep_start - start)
        new_table = table
        new_start = start
        if trim_front:
            new_table = new_table.slice(trim_front, total_rows - trim_front)
            new_start += trim_front
            total_rows = new_table.height
            evicted_rows += trim_front

        trim_back = max(0, (new_start + total_rows) - keep_end)
        if trim_back:
            new_table = new_table.slice(0, total_rows - trim_back)
            total_rows = new_table.height
            evicted_rows += trim_back

        new_end = new_start + total_rows
        return new_table, new_start, new_end, evicted_rows

    def _try_stream_fetch(
        self,
        *,
        plan: Any,
        plan_hash: str | None,
        column_list: list[str],
        column_count: int,
        fetch_start: int,
        fetch_count: int,
        body_start: int,
        body_end_needed: int,
        direction: int,
        backward_extra: int,
        forward_extra: int,
        window_cells_cap: int,
        prefetch_span: int,
        cache_status: str,
        should_record: bool,
        start_ns: int,
    ) -> tuple[TableSliceChunk, bool] | None:
        if not self._should_stream():
            return None

        viewer = self.viewer
        request = SliceStreamRequest(
            plan=plan,
            columns=tuple(column_list),
            start=fetch_start,
            count=fetch_count,
            batch_rows=self.streaming_batch_rows,
            streaming_enabled=True,
            telemetry={
                "viewer": "row_cache",
                "cache": cache_status,
            },
        )

        row_provider = viewer.row_provider
        iterator: Iterator[TableSliceChunk]
        try:
            iterator = row_provider.get_slice_stream(request)
        except Exception:
            return None

        try:
            first_chunk = next(iterator)
        except StopIteration:
            empty = TableSlice.empty(column_list, viewer.schema)
            first_chunk = TableSliceChunk(
                fetch_start,
                empty,
                SliceStatus.OK,
                True,
                {"mode": "empty", "chunks": 1},
            )
            iterator = iter(())

        mode = first_chunk.telemetry.get("mode")
        reason = first_chunk.telemetry.get("reason")
        if mode != "stream":
            self._stream_forced_eager = True
            self._cancel_active_stream()
            self._active_stream_mode = mode
            self._active_stream_reason = reason
            self._active_stream_batches = int(first_chunk.telemetry.get("chunks", 1))
            rows = first_chunk.slice.height
            self._active_stream_rows = rows
            self._active_stream_cells = rows * column_count
            if should_record and start_ns:
                self._active_stream_first_chunk_ns = max(0, monotonic_ns() - start_ns)
            else:
                self._active_stream_first_chunk_ns = 0
            return first_chunk, False

        self._stream_forced_eager = False

        generation = viewer.job_generation()
        sheet_id = getattr(viewer.sheet, "sheet_id", None)

        context = _StreamContext(
            sheet_id=sheet_id,
            generation=generation,
            plan_hash=plan_hash,
            plan=plan,
            columns=tuple(column_list),
            column_count=column_count,
            fetch_start=fetch_start,
            fetch_count=fetch_count,
            target_start=fetch_start,
            target_end=fetch_start + fetch_count,
            body_start=body_start,
            body_end_needed=body_end_needed,
            direction=direction,
            backward_extra=backward_extra,
            forward_extra=forward_extra,
            window_cells_cap=window_cells_cap,
            prefetch_span=prefetch_span,
            cache_status=cache_status,
            start_ns=start_ns,
            first_chunk_ns=start_ns,
        )
        context.mode = mode
        context.reason = reason
        context.batches = 1
        context.first_chunk_rows = first_chunk.slice.height
        context.first_chunk_cells = first_chunk.slice.height * column_count
        context.fetched_cells = context.first_chunk_cells
        context.status = self._combine_status(context.status, first_chunk.status)
        if should_record and start_ns:
            context.first_chunk_duration_ns = max(0, monotonic_ns() - start_ns)
        else:
            context.first_chunk_duration_ns = 0
        if first_chunk.is_final:
            context.final_rows = first_chunk.slice.height
            context.final_cells = context.first_chunk_cells
            context.final_duration_ns = context.first_chunk_duration_ns

        self._cancel_active_stream()
        self._active_stream_context = context
        self._active_stream_generation = generation
        self._active_stream_start_ns = start_ns
        self._active_stream_first_chunk_ns = context.first_chunk_duration_ns
        self._active_stream_batches = context.batches
        self._active_stream_rows = first_chunk.slice.height
        self._active_stream_cells = context.first_chunk_cells
        self._active_stream_mode = mode
        self._active_stream_reason = reason
        self._active_stream_prefetch_dir = "none"
        self._active_stream_prefetch_rows = 0
        self._active_stream_evicted_rows = 0

        if first_chunk.is_final:
            self._finalize_stream_context(context)
            return first_chunk, True

        self._active_stream_future = self._schedule_stream_consumer(context, iterator)
        return first_chunk, True

    def _schedule_stream_consumer(
        self, context: _StreamContext, iterator: Iterator[TableSliceChunk]
    ) -> Future[Any] | None:
        viewer = self.viewer
        runner = viewer.job_runner
        sheet = viewer.sheet

        tag = "row-stream:{}:{}:{}".format(
            context.plan_hash or "none",
            context.fetch_start,
            context.fetch_count,
        )

        def _consume(
            _: int,
            *,
            ctx: _StreamContext = context,
            it: Iterator[TableSliceChunk] = iterator,
        ) -> None:
            for chunk in it:
                if ctx.cancelled:
                    break
                self._deliver_stream_chunk(ctx, chunk)
                if chunk.is_final:
                    break

        try:
            future = runner.submit(
                sheet,
                tag,
                _consume,
                cache_result=False,
                priority=1,
            )
        except Exception:
            thread = threading.Thread(
                target=_consume,
                args=(context.generation or 0,),
                daemon=True,
            )
            thread.start()
            return None
        return future

    def _deliver_stream_chunk(self, context: _StreamContext, chunk: TableSliceChunk) -> None:
        viewer = self.viewer
        viewer_ref = weakref.ref(viewer)

        def _apply() -> None:
            viewer_obj = viewer_ref()
            if viewer_obj is None:
                context.cancelled = True
                return
            if context.cancelled:
                return
            if context.generation is not None and context.sheet_id is not None:
                with contextlib.suppress(Exception):
                    current_gen = viewer.job_runner.current_generation(context.sheet_id)
                    if current_gen != context.generation:
                        context.cancelled = True
                        return
            if self._active_stream_context is not context:
                return
            self._apply_stream_chunk(context, chunk)
            hooks = viewer_obj.ui_hooks
            with contextlib.suppress(Exception):
                hooks.invalidate()

        hooks = viewer.ui_hooks
        try:
            hooks.call_soon(_apply)
        except Exception:
            timer = threading.Timer(0.01, _apply)
            timer.daemon = True
            timer.start()

    def _apply_stream_chunk(self, context: _StreamContext, chunk: TableSliceChunk) -> None:
        if context.cancelled:
            return
        if self._active_stream_context is not context:
            return

        self._active_stream_mode = chunk.telemetry.get("mode", context.mode)
        if self._active_stream_mode:
            context.mode = self._active_stream_mode
        reason = chunk.telemetry.get("reason")
        if reason:
            context.reason = reason
            self._active_stream_reason = reason

        context.status = self._combine_status(context.status, chunk.status)

        column_count = max(1, context.column_count)
        fetched_delta = chunk.slice.height * column_count
        chunk_index = chunk.telemetry.get("chunk_index")
        if chunk_index is not None:
            with contextlib.suppress(TypeError, ValueError):
                context.batches = max(context.batches, int(chunk_index))
        total_chunks = chunk.telemetry.get("chunks")
        if total_chunks is not None:
            with contextlib.suppress(TypeError, ValueError):
                context.batches = max(context.batches, int(total_chunks))
        if not chunk.is_final:
            context.batches += 1
            context.fetched_cells += fetched_delta

        if self.table is None or self.table.height == 0 or chunk.is_final:
            new_table = chunk.slice
            new_start = chunk.offset
        else:
            expected_offset = self.end
            if chunk.offset < self.start or (chunk.offset == self.start and chunk.is_final):
                new_table = chunk.slice
                new_start = chunk.offset
            elif chunk.offset >= expected_offset:
                new_table = self.table.concat_vertical(chunk.slice)
                new_start = self.start
            else:
                overlap_start = max(0, chunk.offset - self.start)
                head = self.table.slice(0, overlap_start) if overlap_start > 0 else None
                tail_start = overlap_start + chunk.slice.height
                tail = None
                if tail_start < self.table.height:
                    tail = self.table.slice(tail_start, self.table.height - tail_start)
                new_table = chunk.slice
                if head is not None:
                    new_table = head.concat_vertical(new_table)
                if tail is not None:
                    new_table = new_table.concat_vertical(tail)
                new_start = self.start

        trimmed_table, trimmed_start, trimmed_end, evicted = self._trim_table_for_budget(
            new_table,
            start=new_start,
            body_start=context.body_start,
            body_end_needed=context.body_end_needed,
            direction=context.direction,
            column_count=context.column_count,
            window_cells_cap=context.window_cells_cap,
        )

        self.table = trimmed_table
        self.start = trimmed_start
        self.end = trimmed_end
        context.evicted_rows += evicted
        self._active_stream_evicted_rows = context.evicted_rows

        self._table_status = context.status

        total_rows = self.table.height if self.table is not None else 0
        self._active_stream_rows = total_rows
        self._active_stream_cells = total_rows * column_count
        self._active_stream_batches = max(self._active_stream_batches, context.batches)

        if chunk.is_final:
            context.final_rows = total_rows
            context.final_cells = total_rows * column_count
            if context.start_ns:
                context.final_duration_ns = max(0, monotonic_ns() - context.start_ns)
            self._finalize_stream_context(context)

    def _finalize_stream_context(self, context: _StreamContext) -> None:
        if context.cancelled:
            return

        viewer = self.viewer
        row_provider = viewer.row_provider
        plan = context.plan
        columns = list(context.columns)

        prefetch_dir = "none"
        prefetch_rows = 0
        if context.direction < 0:
            prefetch_start = max(0, self.start - context.backward_extra)
            prefetch_rows = self.start - prefetch_start
            if prefetch_rows > 0:
                with contextlib.suppress(Exception):
                    row_provider.prefetch(plan, columns, prefetch_start, prefetch_rows)
                    prefetch_dir = "backward"
        else:
            prefetch_start = self.end
            prefetch_rows = context.forward_extra
            if prefetch_rows > 0:
                with contextlib.suppress(Exception):
                    row_provider.prefetch(plan, columns, prefetch_start, prefetch_rows)
                    prefetch_dir = "forward"

        context.prefetch_dir = prefetch_dir
        context.prefetch_rows = prefetch_rows

        self._active_stream_prefetch_dir = prefetch_dir
        self._active_stream_prefetch_rows = prefetch_rows
        self._active_stream_future = None
        self._active_stream_context = context

    def invalidate(self) -> None:
        self._cancel_active_stream()
        self.table = None
        self.cols = ()
        self.start = 0
        self.end = 0
        self.plan_hash = None
        self._visible_row_positions = []
        self._visible_frozen_row_count = 0
        self._sheet_version = None
        self._last_body_start = None
        self._last_direction = 0
        self._table_status = SliceStatus.OK
        self._last_warning_status = SliceStatus.OK

    def get_prefetch(self, hint: int | None = None) -> int:
        """Return the number of body rows to fetch for the active viewport."""

        viewer = self.viewer
        fallback = max(viewer.view_height * 2, 64)
        base = self.prefetch if self.prefetch is not None else fallback

        if hint is None or hint <= 0:
            return max(base, viewer.view_height)

        try:
            capped = int(hint)
        except (TypeError, ValueError):  # pragma: no cover - defensive
            return max(base, viewer.view_height)

        capped = max(viewer.view_height, capped)
        if base <= capped:
            return max(base, viewer.view_height)
        return capped

    def visible_row_positions(self) -> list[int]:
        return list(self._visible_row_positions)

    def visible_frozen_row_count(self) -> int:
        return self._visible_frozen_row_count

    def get_visible_table_slice(
        self, columns: Sequence[str], overscan_hint: int | None = None
    ) -> TableSlice:
        viewer = self.viewer

        if not columns:
            self._visible_row_positions = []
            self._visible_frozen_row_count = 0
            return TableSlice.empty()

        should_record = viewer._perf_callback is not None

        height = max(1, viewer.view_height)
        column_list = list(columns)
        col_key = tuple(column_list)
        plan = viewer._current_plan()
        plan_hash = viewer.plan_hash()
        row_provider = viewer.row_provider

        frozen_target = min(self.freeze.effective_row_count(), height)
        frozen_slices: list[TableSlice] = []
        frozen_positions: list[int] = []

        overall_status = SliceStatus.OK

        actual_frozen = 0
        if frozen_target > 0:
            try:
                frozen_slice, frozen_status = row_provider.get_slice(
                    plan,
                    column_list,
                    0,
                    frozen_target,
                )
            except Exception:
                self.invalidate()
                raise
            if frozen_slice.height > 0:
                frozen_slices.append(frozen_slice)
                actual_frozen = frozen_slice.height
                frozen_positions.extend(range(actual_frozen))
                overall_status = self._combine_status(overall_status, frozen_status)

        self._visible_frozen_row_count = actual_frozen

        remaining_height = min(self.freeze.body_view_height(), max(0, height - actual_frozen))
        body_start = max(0, viewer.row0)
        if actual_frozen:
            body_start = max(body_start, actual_frozen)

        body_slice = TableSlice.empty(column_list, viewer.schema)
        body_positions: list[int] = []

        body_start_ns = monotonic_ns() if (should_record and remaining_height > 0) else 0

        direction = 0
        if self._last_body_start is not None:
            if body_start > self._last_body_start:
                direction = 1
            elif body_start < self._last_body_start:
                direction = -1
            else:
                direction = self._last_direction
        self._last_body_start = body_start
        self._last_direction = direction

        column_count = len(col_key) or 1
        window_cells_cap = max(self.max_cells, column_count * max(1, remaining_height))
        prefetch_span = self.get_prefetch(overscan_hint)

        if direction > 0:
            backward_extra = max(viewer.view_height, prefetch_span // 4)
            forward_extra = prefetch_span
        elif direction < 0:
            forward_extra = max(viewer.view_height, prefetch_span // 4)
            backward_extra = prefetch_span
        else:
            forward_extra = max(viewer.view_height, prefetch_span // 2)
            backward_extra = forward_extra

        target_start = max(0, body_start - backward_extra)
        target_end = body_start + remaining_height + forward_extra

        body_start_ns = body_start_ns if remaining_height > 0 else 0
        fetched_cells = 0
        evicted_rows = 0
        cache_status = "hit"
        sheet_version = getattr(viewer.sheet, "cache_version", None)

        streaming_active = False

        def _fetch_slice(
            start: int, count: int, *, allow_stream: bool = False
        ) -> tuple[TableSlice, SliceStatus]:
            nonlocal fetched_cells, overall_status, streaming_active, cache_status
            if allow_stream and count > 0:
                result = self._try_stream_fetch(
                    plan=plan,
                    plan_hash=plan_hash,
                    column_list=column_list,
                    column_count=column_count,
                    fetch_start=start,
                    fetch_count=count,
                    body_start=body_start,
                    body_end_needed=body_start + remaining_height,
                    direction=direction,
                    backward_extra=backward_extra,
                    forward_extra=forward_extra,
                    window_cells_cap=window_cells_cap,
                    prefetch_span=prefetch_span,
                    cache_status=cache_status,
                    should_record=should_record,
                    start_ns=body_start_ns,
                )
                if result is not None:
                    chunk, is_streaming = result
                    slice_ = chunk.slice
                    status = chunk.status
                    fetched_cells += slice_.height * column_count
                    overall_status = self._combine_status(overall_status, status)
                    if is_streaming:
                        streaming_active = True
                        cache_status = "stream"
                    return slice_, status
            try:
                slice_, status = row_provider.get_slice(plan, column_list, start, count)
            except Exception:
                self.invalidate()
                raise
            fetched_cells += slice_.height * column_count
            overall_status = self._combine_status(overall_status, status)
            return slice_, status

        cache_valid = (
            self.table is not None and self.cols == col_key and self.plan_hash == plan_hash
        )
        if cache_valid and sheet_version is not None and sheet_version != self._sheet_version:
            cache_valid = False

        if cache_valid:
            current_start = self.start
            current_end = self.end
            if target_end <= current_start or target_start >= current_end:
                cache_valid = False

        new_table = self.table if cache_valid else None
        new_start = self.start if cache_valid else 0
        new_end = self.end if cache_valid else 0
        table_status = self._table_status if cache_valid else SliceStatus.OK
        if cache_valid:
            overall_status = self._combine_status(overall_status, table_status)

        if remaining_height > 0:
            if not cache_valid:
                fetch_start = max(0, target_start)
                fetch_count = max(remaining_height, target_end - fetch_start)
                table_slice, table_slice_status = _fetch_slice(
                    fetch_start, fetch_count, allow_stream=True
                )
                new_table = table_slice
                new_start = fetch_start
                new_end = fetch_start + table_slice.height
                table_status = table_slice_status
                cache_status = "miss"
                self.cols = col_key
                self.plan_hash = plan_hash
                self._sheet_version = sheet_version
            else:
                assert new_table is not None
                if target_start < new_start and not streaming_active:
                    fetch_start = max(0, target_start)
                    fetch_count = new_start - fetch_start
                    if fetch_count > 0:
                        leading, leading_status = _fetch_slice(fetch_start, fetch_count)
                        if leading.height > 0:
                            new_table = leading.concat_vertical(new_table)
                            new_start = fetch_start
                            table_status = self._combine_status(table_status, leading_status)
                            cache_status = "extend"
                if target_end > new_end and not streaming_active:
                    fetch_start = new_end
                    fetch_count = target_end - new_end
                    if fetch_count > 0:
                        trailing, trailing_status = _fetch_slice(fetch_start, fetch_count)
                        if trailing.height > 0:
                            new_table = (
                                trailing
                                if new_table is None
                                else new_table.concat_vertical(trailing)
                            )
                            new_end = fetch_start + trailing.height
                            table_status = self._combine_status(table_status, trailing_status)
                            cache_status = "extend"

            if new_table is None:
                new_table = TableSlice.empty(column_list, viewer.schema)
                new_start = max(0, target_start)
                new_end = new_start

            body_end_needed = body_start + remaining_height
            new_table, new_start, new_end, trimmed = self._trim_table_for_budget(
                new_table,
                start=new_start,
                body_start=body_start,
                body_end_needed=body_end_needed,
                direction=direction,
                column_count=column_count,
                window_cells_cap=window_cells_cap,
            )
            evicted_rows += trimmed

            self.table = new_table
            self.start = new_start
            self.end = new_end
            self.cols = col_key
            self.plan_hash = plan_hash
            self._sheet_version = sheet_version
            self._table_status = table_status

            offset = max(0, body_start - self.start)
            body_length = min(remaining_height, max(0, self.table.height - offset))
            if body_length > 0:
                body_slice = self.table.slice(offset, body_length)
            else:
                body_slice = TableSlice.empty(column_list, viewer.schema)

            stream_context = self._active_stream_context
            context_matches = False
            if stream_context is not None:
                expected_count = max(0, target_end - target_start)
                context_matches = (
                    stream_context.plan_hash == plan_hash
                    and stream_context.columns == col_key
                    and stream_context.fetch_start == target_start
                    and stream_context.fetch_count == expected_count
                )

            prefetch_dir = "none"
            prefetch_rows = 0
            if streaming_active or context_matches:
                prefetch_dir = self._active_stream_prefetch_dir
                prefetch_rows = self._active_stream_prefetch_rows
            else:
                if direction < 0:
                    prefetch_start = max(0, self.start - backward_extra)
                    prefetch_rows = self.start - prefetch_start
                    if prefetch_rows > 0:
                        row_provider.prefetch(plan, column_list, prefetch_start, prefetch_rows)
                        prefetch_dir = "backward"
                else:
                    prefetch_start = self.end
                    prefetch_rows = forward_extra
                    if prefetch_rows > 0:
                        row_provider.prefetch(plan, column_list, prefetch_start, prefetch_rows)
                        prefetch_dir = "forward"

            window_rows = self.table.height
            window_cells = window_rows * column_count

            if streaming_active or context_matches:
                stream_mode = self._active_stream_mode or "stream"
                stream_reason = self._active_stream_reason or "stream"
                stream_batches = max(1, self._active_stream_batches)
                stream_rows = self._active_stream_rows
                stream_cells = self._active_stream_cells
                first_batch_ns = self._active_stream_first_chunk_ns
            elif not self.streaming_enabled:
                stream_mode = "disabled"
                stream_reason = "flag"
                stream_batches = 0
                stream_rows = 0
                stream_cells = 0
                first_batch_ns = 0
            elif self._stream_forced_eager:
                stream_mode = self._active_stream_mode or "fallback"
                stream_reason = self._active_stream_reason or "fallback"
                stream_batches = max(1, self._active_stream_batches)
                stream_rows = self._active_stream_rows
                stream_cells = self._active_stream_cells
                first_batch_ns = self._active_stream_first_chunk_ns
            else:
                stream_mode = "eager"
                stream_reason = "not_streaming"
                stream_batches = 0
                stream_rows = 0
                stream_cells = 0
                first_batch_ns = 0

            first_batch_ms = first_batch_ns / 1_000_000 if first_batch_ns else 0.0

            payload: dict[str, int | float | str] = {
                "row0": body_start,
                "height": body_slice.height,
                "cache": cache_status,
                "cache_start": self.start,
                "cache_end": self.end,
                "cols": column_count,
                "window_rows": window_rows,
                "window_cells": window_cells,
                "window_bytes": window_cells * self.APPROX_BYTES_PER_CELL,
                "fetched_rows": fetched_cells // column_count if column_count else 0,
                "fetched_cells": fetched_cells,
                "evicted_rows": evicted_rows,
                "prefetch_dir": prefetch_dir,
                "prefetch_rows": prefetch_rows,
                "stream_mode": stream_mode,
                "stream_reason": stream_reason,
                "stream_batches": stream_batches,
                "stream_rows": stream_rows,
                "stream_cells": stream_cells,
                "first_batch_ms": first_batch_ms,
            }

            if should_record:
                duration_ms = (monotonic_ns() - body_start_ns) / 1_000_000 if body_start_ns else 0.0
                viewer._record_perf_event("viewer.row_cache", duration_ms, payload)

            body_positions.extend(range(body_start, body_start + body_slice.height))
        else:
            # No scrollable body; still honour frozen rows.
            self.table = TableSlice.empty(column_list, viewer.schema)
            self.start = body_start
            self.end = body_start
            self.cols = col_key
            self.plan_hash = plan_hash
            self._sheet_version = sheet_version
            self._table_status = SliceStatus.OK

        self._visible_row_positions = frozen_positions + body_positions

        slices: list[TableSlice] = []
        slices.extend(frozen_slices)
        if body_slice.height:
            slices.append(body_slice)

        if not slices:
            self._handle_slice_status(overall_status)
            return TableSlice.empty(column_list, viewer.schema)

        result = slices[0]
        for additional in slices[1:]:
            result = result.concat_vertical(additional)

        if result.row_ids is None:
            row_id_column = getattr(viewer.row_provider, "_row_id_column", None)
            if row_id_column:
                rescue_slice = None
                try:
                    rescue_slice, _ = row_provider.get_slice(
                        plan,
                        (row_id_column,),
                        max(0, result.start_offset or 0),
                        result.height,
                    )
                except Exception:
                    rescue_slice = None

                if rescue_slice is not None:
                    row_ids = rescue_slice.row_ids
                    if row_ids is None and row_id_column in rescue_slice.column_names:
                        try:
                            row_ids = rescue_slice.column(row_id_column).values
                        except Exception:
                            row_ids = None

                    if row_ids is not None:
                        result = TableSlice(
                            result.columns,
                            result.schema,
                            start_offset=result.start_offset,
                            row_ids=row_ids,
                        )
        self._handle_slice_status(overall_status)
        return result

    @staticmethod
    def _combine_status(left: SliceStatus, right: SliceStatus) -> SliceStatus:
        if right is SliceStatus.SCHEMA_MISMATCH:
            return SliceStatus.SCHEMA_MISMATCH
        if right is SliceStatus.PARTIAL and left is SliceStatus.OK:
            return SliceStatus.PARTIAL
        return left

    def _handle_slice_status(self, status: SliceStatus) -> None:
        if status is SliceStatus.OK:
            self._last_warning_status = SliceStatus.OK
            return
        if status is self._last_warning_status:
            return

        viewer = self.viewer
        if viewer.status_message:
            self._last_warning_status = status
            return

        if status is SliceStatus.SCHEMA_MISMATCH:
            message = "slice schema mismatch — check column names"
        else:
            message = "some requested columns are missing"
        viewer.status_message = message
        viewer.mark_status_dirty()
        self._last_warning_status = status


class ColumnWidthController:
    """Handle column width calculations and width modes."""

    WIDTH_SAMPLE_MAX_ROWS = 10_000
    WIDTH_SAMPLE_BATCH_ROWS = 1_000
    WIDTH_SAMPLE_BUDGET_NS = 100_000_000  # 100ms
    WIDTH_TARGET_PERCENTILE = 0.99
    WIDTH_PADDING = 2

    def __init__(self, viewer: Viewer) -> None:
        self.viewer = viewer

    def content_width_for_column(
        self,
        col_idx: int,
        *,
        sampled_lengths: dict[int, list[int]] | None = None,
    ) -> int:
        viewer = self.viewer
        if col_idx < 0 or col_idx >= len(viewer.columns):
            return viewer._min_col_width

        col_name = viewer.columns[col_idx]
        header_width = len(col_name) + self.WIDTH_PADDING

        samples = sampled_lengths or {}
        lengths = samples.get(col_idx)
        if lengths is None:
            lengths = self._sample_column_lengths((col_idx,)).get(col_idx, [])

        target_length = self._percentile_length(lengths) if lengths else 0
        content_width = target_length + self.WIDTH_PADDING

        width = max(header_width, content_width)
        width = self._clamp_width(width)
        return width

    def _clamp_width(self, width: int) -> int:
        viewer = self.viewer
        max_viewport = max(viewer._min_col_width, viewer.view_width_chars - 1)
        return max(viewer._min_col_width, min(width, max_viewport))

    def _percentile_length(self, lengths: Sequence[int]) -> int:
        if not lengths:
            return 0
        ordered = sorted(lengths)
        if len(ordered) == 1:
            return ordered[0]
        idx = math.ceil((len(ordered) - 1) * self.WIDTH_TARGET_PERCENTILE)
        idx = max(0, min(idx, len(ordered) - 1))
        return ordered[idx]

    def _coerce_display(self, raw_value: Any, rendered: str) -> str:
        if raw_value is None or rendered == "":
            return "null"
        if isinstance(raw_value, float) and (math.isnan(raw_value) or math.isinf(raw_value)):
            if math.isnan(raw_value):
                return "NaN"
            return "inf" if raw_value > 0 else "-inf"
        return rendered

    def _fallback_display(self, value: Any) -> str:
        if value is None:
            return "null"
        if _is_float_like(value):
            try:
                as_float = float(value)
            except Exception:
                return str(value)
            if math.isnan(as_float):
                return "NaN"
            if math.isinf(as_float):
                return "inf" if as_float > 0 else "-inf"
            return _format_float_two_decimals(as_float)
        return str(value)

    def _measure_column_lengths(
        self,
        column: Any,
        limit: int,
        budget_exceeded: Callable[[], bool],
    ) -> list[int]:
        if limit <= 0:
            return []

        lengths: list[int] = []
        try:
            formatted_values = column.formatted(0)
        except Exception:
            formatted_values = None

        if formatted_values:
            for raw_value, rendered in zip(column.values, formatted_values, strict=False):
                if len(lengths) >= limit or budget_exceeded():
                    break
                display = self._coerce_display(raw_value, rendered)
                lengths.append(len(display))
        else:
            for raw_value in column.values:
                if len(lengths) >= limit or budget_exceeded():
                    break
                lengths.append(len(self._fallback_display(raw_value)))
        return lengths

    def _sample_column_lengths(self, column_indices: Sequence[int]) -> dict[int, list[int]]:
        viewer = self.viewer
        if not column_indices:
            return {}

        valid_indices = [idx for idx in column_indices if 0 <= idx < len(viewer.columns)]
        if not valid_indices:
            return {}

        names = {idx: viewer.columns[idx] for idx in valid_indices}
        lengths: dict[int, list[int]] = {idx: [] for idx in valid_indices}

        total_rows_hint = getattr(viewer, "_total_rows", None)
        max_rows = self.WIDTH_SAMPLE_MAX_ROWS
        if isinstance(total_rows_hint, int) and total_rows_hint > 0:
            max_rows = min(max_rows, total_rows_hint)

        start_ns = monotonic_ns()

        def budget_exceeded() -> bool:
            return monotonic_ns() - start_ns >= self.WIDTH_SAMPLE_BUDGET_NS

        def measure(table_slice: Any) -> None:
            if table_slice is None or getattr(table_slice, "height", 0) <= 0:
                return
            for idx, name in names.items():
                if len(lengths[idx]) >= max_rows:
                    continue
                if name not in table_slice.column_names:
                    continue
                column = table_slice.column(name)
                remaining = max_rows - len(lengths[idx])
                samples = self._measure_column_lengths(column, remaining, budget_exceeded)
                if samples:
                    lengths[idx].extend(samples)
                if budget_exceeded():
                    return

        measure(getattr(viewer._row_cache, "table", None))

        next_offset = 0
        batch_rows = self.WIDTH_SAMPLE_BATCH_ROWS
        column_names = list(names.values())

        while not budget_exceeded():
            remaining_targets = [
                max_rows - len(lengths[idx])
                for idx in valid_indices
                if len(lengths[idx]) < max_rows
            ]
            if not remaining_targets:
                break

            rows_to_fetch = min(batch_rows, max(remaining_targets))
            try:
                sample_slice = viewer.sheet.fetch_slice(next_offset, rows_to_fetch, column_names)
            except Exception:
                break

            measure(sample_slice)

            consumed = getattr(sample_slice, "height", 0)
            if consumed <= 0:
                break
            next_offset += consumed
            if consumed < rows_to_fetch:
                break
            if (
                isinstance(total_rows_hint, int)
                and total_rows_hint > 0
                and next_offset >= total_rows_hint
            ):
                break

        return lengths

    def compute_initial_widths(self) -> list[int]:
        """Compute initial column widths based on header and sample data."""
        viewer = self.viewer
        if not viewer.columns:
            return []

        widths = []
        for col_name in viewer.columns:
            # Start with header width
            header_width = len(col_name) + 2  # +2 for padding

            # Sample data to estimate content width
            try:
                # Sample fewer rows for initial width calculation to keep it fast
                sample_rows = min(100, viewer._total_rows if viewer._total_rows else 50)
                sample_slice = viewer.sheet.fetch_slice(0, sample_rows, [col_name])

                if col_name in sample_slice.column_names and sample_slice.height > 0:
                    column = sample_slice.column(col_name)

                    try:
                        formatted_values = column.formatted(0)
                    except Exception:
                        formatted_values = None

                    if formatted_values:
                        max_display = header_width
                        for raw_value, rendered in zip(
                            column.values, formatted_values, strict=False
                        ):
                            if raw_value is None or rendered == "":
                                display = "null"
                            elif isinstance(raw_value, float) and (
                                math.isnan(raw_value) or math.isinf(raw_value)
                            ):
                                if math.isnan(raw_value):
                                    display = "NaN"
                                else:
                                    display = "inf" if raw_value > 0 else "-inf"
                            else:
                                display = rendered
                            max_display = max(max_display, len(display) + 2)
                        header_width = max(
                            header_width,
                            min(max_display, viewer._default_col_width_cap),
                        )
                    else:
                        lengths = [len(str(value)) for value in column.values if value is not None]
                        if lengths:
                            content_width = min(max(lengths) + 2, viewer._default_col_width_cap)
                            header_width = max(header_width, content_width)
            except Exception:
                # If sampling fails, fall back to header width
                pass

            # Ensure minimum width
            final_width = max(viewer._min_col_width, header_width)
            widths.append(final_width)

        return widths

    def invalidate_cache(self) -> None:
        viewer = self.viewer
        viewer._width_cache_all = None
        viewer._width_cache_single.clear()

    def ensure_default_widths(self) -> None:
        viewer = self.viewer
        if len(viewer._default_header_widths) == len(viewer.columns):
            return

        viewer._header_widths = self.compute_initial_widths()
        viewer._default_header_widths = list(viewer._header_widths)
        self.invalidate_cache()

    def normalize_mode(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer._width_mode = "default"
            viewer._width_target = None
            return

        if viewer._width_mode == "single":
            if viewer._width_target is None or not (
                0 <= viewer._width_target < len(viewer.columns)
            ):
                viewer._width_mode = "default"
                viewer._width_target = None
        elif viewer._width_mode == "all":
            viewer._width_target = None
        else:
            viewer._width_mode = "default"
            viewer._width_target = None

    def apply_width_mode(self) -> None:
        viewer = self.viewer
        self.ensure_default_widths()
        self.normalize_mode()

        if viewer._width_mode == "all":
            cache = viewer._width_cache_all
            if cache is None or len(cache) != len(viewer.columns):
                samples = self._sample_column_lengths(range(len(viewer.columns)))
                cache = [
                    self.content_width_for_column(idx, sampled_lengths=samples)
                    for idx in range(len(viewer.columns))
                ]
                viewer._width_cache_all = list(cache)
            viewer._header_widths = [self._clamp_width(width) for width in cache]
            viewer._width_cache_all = list(viewer._header_widths)
            viewer._width_cache_single.clear()
        elif viewer._width_mode == "single" and viewer._width_target is not None:
            target = viewer._width_target
            base_widths = list(viewer._default_header_widths)
            if 0 <= target < len(viewer.columns):
                width = viewer._width_cache_single.get(target)
                if width is None:
                    samples = self._sample_column_lengths((target,))
                    width = self.content_width_for_column(target, sampled_lengths=samples)
                width = self._clamp_width(width)
                viewer._width_cache_single[target] = width
                base_widths[target] = width
                viewer._header_widths = base_widths
            else:
                viewer._width_mode = "default"
                viewer._width_target = None
                viewer._header_widths = list(viewer._default_header_widths)
        else:
            viewer._header_widths = list(viewer._default_header_widths)
            if viewer._width_mode == "default":
                viewer._width_cache_single.clear()

        viewer._visible_key = None

    def autosize_visible_columns(self, column_indices: list[int]) -> None:
        viewer = self.viewer
        if not column_indices:
            viewer._autosized_widths.clear()
            return

        available_inner = max(1, viewer.view_width_chars - (len(column_indices) + 1))

        base_widths = [viewer._header_widths[idx] for idx in column_indices]
        base_total = sum(base_widths)

        compact_default = (
            getattr(viewer, "_compact_width_layout", False) and viewer._width_mode == "default"
        )
        if compact_default:
            capped_widths = [min(width, viewer._default_col_width_cap) for width in base_widths]
            viewer._autosized_widths = dict(zip(column_indices, capped_widths, strict=False))
            return

        if base_total >= available_inner:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        frozen_set = viewer._freeze.column_index_set()
        dynamic_positions = [pos for pos, idx in enumerate(column_indices) if idx not in frozen_set]

        slack = available_inner - base_total

        if not dynamic_positions:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        if viewer._width_mode == "single" and viewer._width_target is not None:
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        if viewer._width_mode != "default":
            viewer._autosized_widths = dict(zip(column_indices, base_widths, strict=False))
            return

        rooms: list[int] = []
        total_room = 0
        for pos in dynamic_positions:
            base = base_widths[pos]
            target = viewer._default_col_width_cap
            room = max(0, target - base)
            rooms.append(room)
            total_room += room

        new_widths = list(base_widths)

        if total_room <= 0:
            share, remainder = divmod(slack, len(dynamic_positions))
            if share:
                for pos in dynamic_positions:
                    new_widths[pos] += share
            if remainder:
                for offset in range(remainder):
                    pos = dynamic_positions[-(offset + 1)]
                    new_widths[pos] += 1
        else:
            allocations = [0] * len(dynamic_positions)
            for i, room in enumerate(rooms):
                if room == 0:
                    continue
                provisional = (slack * room) // total_room
                allocations[i] = min(room, provisional)

            allocated = sum(allocations)
            remaining = slack - allocated

            if remaining > 0:
                residual = [room - allocations[i] for i, room in enumerate(rooms)]
                while remaining > 0 and any(r > 0 for r in residual):
                    for i, rem in enumerate(residual):
                        if remaining == 0:
                            break
                        if rem > 0:
                            allocations[i] += 1
                            residual[i] -= 1
                            remaining -= 1
                    else:
                        break

            if remaining > 0:
                allocations[-1] += remaining

            for pos, alloc in zip(dynamic_positions, allocations, strict=False):
                new_widths[pos] += alloc

        current_total = sum(new_widths)
        if current_total < available_inner and new_widths:
            target_pos = dynamic_positions[-1] if dynamic_positions else len(new_widths) - 1
            new_widths[target_pos] += available_inner - current_total

        viewer._autosized_widths = dict(zip(column_indices, new_widths, strict=False))

    def force_default_mode(self) -> None:
        viewer = self.viewer
        viewer._width_mode = "default"
        viewer._width_target = None
        self.invalidate_cache()
        self.apply_width_mode()
        viewer._autosized_widths.clear()

    def toggle_maximize_current_col(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer.status_message = "no columns"
            return

        target = max(0, min(viewer.cur_col, len(viewer.columns) - 1))

        current_width = viewer._header_widths[target]
        desired_width = viewer._width_cache_single.get(target)
        if desired_width is None:
            desired_width = viewer._compute_content_width(target)
            viewer._width_cache_single[target] = desired_width

        if viewer._width_mode == "single" and viewer._width_target == target:
            viewer._width_mode = "default"
            viewer._width_target = None
            viewer.status_message = "width reset"
        else:
            if viewer._width_mode == "default" and desired_width <= current_width:
                viewer.status_message = f"'{viewer.columns[target]}' already at max width"
                viewer._visible_key = None
                viewer._autosized_widths.clear()
                viewer.clamp()
                return
            viewer._width_mode = "single"
            viewer._width_target = target
            viewer._width_cache_all = None
            viewer.status_message = f"maximize column '{viewer.columns[target]}'"

        self.apply_width_mode()

        if viewer._width_mode == "single":
            maximised_col_name = viewer.columns[target]
            if maximised_col_name not in viewer.visible_cols:
                viewer.col0 = target
                viewer._visible_key = None

        viewer.clamp()

    def toggle_maximize_all_cols(self) -> None:
        viewer = self.viewer
        if not viewer.columns:
            viewer.status_message = "no columns"
            return
        if viewer._width_mode == "all":
            viewer._width_mode = "default"
            viewer.status_message = "widths reset"
        else:
            viewer._width_mode = "all"
            viewer._width_target = None
            viewer._width_cache_all = None
            viewer._width_cache_single.clear()
            viewer.col0 = viewer.cur_col
            viewer.status_message = "maximize all columns"

        self.apply_width_mode()
        if viewer._width_mode != "default":
            viewer._autosized_widths.clear()
        viewer.clamp()

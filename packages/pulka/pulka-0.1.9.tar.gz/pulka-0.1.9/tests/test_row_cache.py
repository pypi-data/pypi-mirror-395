from __future__ import annotations

import threading
from collections.abc import Sequence
from concurrent.futures import Future
from typing import Any
from unittest.mock import patch

import polars as pl

from pulka.core.engine.contracts import TableColumn, TableSlice
from pulka.core.jobs import JobResult
from pulka.core.row_provider import RowProvider, SliceStatus, TableSliceChunk
from pulka.core.viewer.components import FreezePaneController, RowCacheController
from pulka.core.viewer.viewer import Viewer
from pulka.sheets.data_sheet import DataSheet


def _make_table_slice(columns: Sequence[str], start: int, length: int) -> TableSlice:
    schema = dict.fromkeys(columns, int)
    if length <= 0:
        return TableSlice.empty(columns, schema)

    table_columns: list[TableColumn] = []
    for name in columns:
        values = tuple(range(start, start + length))
        formatted = tuple(f"{name}:{row}" for row in range(start, start + length))

        def _formatter(
            max_chars: int,
            *,
            _formatted: tuple[str, ...] = formatted,
        ) -> tuple[str, ...]:
            return _formatted

        table_columns.append(TableColumn(name, values, int, 0, _formatter))
    return TableSlice(tuple(table_columns), schema)


class _StubRowProvider:
    def __init__(self, total_rows: int, columns: Sequence[str]) -> None:
        self.total_rows = total_rows
        self.schema = dict.fromkeys(columns, int)
        self.calls: list[tuple[int, int, int]] = []
        self.prefetch_calls: list[tuple[int, int]] = []

    def get_slice(
        self, plan: Any, columns: Sequence[str], start: int, count: int
    ) -> tuple[TableSlice, SliceStatus]:
        start = max(0, int(start))
        count = max(0, int(count))
        end = min(self.total_rows, start + count)
        actual = max(0, end - start)
        self.calls.append((start, count, actual))
        if actual <= 0:
            return TableSlice.empty(columns, self.schema), SliceStatus.OK
        return _make_table_slice(columns, start, actual), SliceStatus.OK

    def prefetch(self, plan: Any, columns: Sequence[str], start: int, count: int) -> None:
        start = max(0, int(start))
        count = max(0, int(count))
        if count <= 0:
            return
        self.prefetch_calls.append((start, count))


class _StubSheet:
    cache_version = 0
    sheet_id = "stub-sheet"


class _ImmediateUIHooks:
    def __init__(self) -> None:
        self.invalidations = 0

    def call_soon(self, callback: Any) -> None:
        callback()

    def invalidate(self) -> None:
        self.invalidations += 1


class _ThreadedJobRunner:
    def __init__(self) -> None:
        self._futures: list[Future[JobResult]] = []

    def get(self, sheet_id: str, tag: str) -> JobResult | None:
        return None

    def enqueue(self, req: Any) -> Future[JobResult]:
        def _fn(_: int) -> Any:
            return req.fn(req.generation)

        sheet = type("_SheetProxy", (), {"sheet_id": req.sheet_id})()
        return self.submit(
            sheet,
            req.tag,
            _fn,
            cache_result=req.cache_result,
            priority=req.priority,
        )

    def submit(
        self,
        sheet: Any,
        tag: str,
        fn: Any,
        *,
        cache_result: bool = True,
        priority: int = 0,
    ) -> Future[JobResult]:
        future: Future[JobResult] = Future()

        def _run() -> None:
            try:
                value = fn(0)
            except Exception as exc:  # pragma: no cover - defensive
                future.set_exception(exc)
                return
            sheet_id = getattr(sheet, "sheet_id", "stub-sheet")
            result = JobResult(sheet_id, 0, tag, value, None, 0, 0, cache_result)
            future.set_result(result)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        self._futures.append(future)
        return future

    def bump_generation(self, sheet_id: str) -> int:
        return 0

    def current_generation(self, sheet_id: str) -> int:
        return 0

    def invalidate_sheet(self, sheet_id: str) -> None:
        return None

    def purge_older_generations(self, sheet_id: str, keep: int) -> None:
        return None


class _StreamingStubRowProvider(_StubRowProvider):
    def __init__(
        self,
        total_rows: int,
        columns: Sequence[str],
        *,
        chunk_size: int = 2,
        mode: str = "stream",
        reason: str = "stream",
    ) -> None:
        super().__init__(total_rows, columns)
        self.chunk_size = max(1, chunk_size)
        self.stream_mode = mode
        self.stream_reason = reason
        self.stream_calls: list[tuple[int, int]] = []
        self.stream_completed = threading.Event()

    def get_slice_stream(self, request: Any):
        start = max(0, int(request.start))
        count = max(0, int(request.count))
        self.stream_calls.append((start, count))
        columns = tuple(request.columns)
        if count <= 0:
            self.stream_completed.set()
            telemetry = {"mode": self.stream_mode, "chunks": 1, "rows": 0, "cells": 0}
            yield TableSliceChunk(
                start, TableSlice.empty(columns, self.schema), SliceStatus.OK, True, telemetry
            )
            return

        if self.stream_mode != "stream":
            slice_, status = self.get_slice(request.plan, columns, start, count)
            telemetry = {
                "mode": self.stream_mode,
                "reason": self.stream_reason,
                "chunks": 1,
                "rows": slice_.height,
                "cells": slice_.height * len(columns),
            }
            self.stream_completed.set()
            yield TableSliceChunk(start, slice_, status, True, telemetry)
            return

        remaining = count
        offset = start
        chunk_index = 0
        while remaining > 0:
            size = min(self.chunk_size, remaining)
            chunk_slice = _make_table_slice(columns, offset, size)
            telemetry = {"mode": "stream", "chunk_index": chunk_index + 1}
            yield TableSliceChunk(offset, chunk_slice, SliceStatus.OK, False, telemetry)
            remaining -= size
            offset += size
            chunk_index += 1

        final_slice, status = self.get_slice(request.plan, columns, start, count)
        telemetry = {
            "mode": "stream",
            "chunks": chunk_index + 1,
            "rows": final_slice.height,
            "cells": final_slice.height * len(columns),
        }
        self.stream_completed.set()
        yield TableSliceChunk(start, final_slice, status, True, telemetry)


class _StubViewer:
    def __init__(
        self,
        provider: _StubRowProvider,
        *,
        columns: Sequence[str],
        view_height: int,
    ) -> None:
        self.columns = list(columns)
        self.schema = dict.fromkeys(columns, int)
        self.view_height = view_height
        self.row0 = 0
        self.sheet = _StubSheet()
        self._hidden_cols: set[str] = set()
        self._row_provider = provider
        self._perf_events: list[tuple[str, float, dict[str, Any]]] = []
        self._ui_hooks = _ImmediateUIHooks()
        self._job_runner = _ThreadedJobRunner()

        def _callback(phase: str, duration: float, payload: dict[str, Any]) -> None:
            self._perf_events.append((phase, duration, payload))

        self._perf_callback = _callback

    def _current_plan(self) -> None:
        return None

    def plan_hash(self) -> str:
        return "stub-plan"

    def job_generation(self) -> int:
        return 0

    def _record_perf_event(self, phase: str, duration: float, payload: dict[str, Any]) -> None:
        self._perf_events.append((phase, duration, payload))

    @property
    def row_provider(self) -> _StubRowProvider:
        return self._row_provider

    @property
    def visible_frozen_row_count(self) -> int:
        return 0

    @property
    def job_runner(self) -> _ThreadedJobRunner:
        return self._job_runner

    @property
    def ui_hooks(self) -> _ImmediateUIHooks:
        return self._ui_hooks


def _make_stub_cache(*, total_rows: int = 512, view_height: int = 8, max_cells: int | None = None):
    columns = ("c0", "c1", "c2")
    provider = _StubRowProvider(total_rows, columns)
    viewer = _StubViewer(provider, columns=columns, view_height=view_height)
    freeze = FreezePaneController(viewer)
    cache = RowCacheController(viewer, freeze)
    if max_cells is not None:
        cache.max_cells = max_cells
    return viewer, cache, provider


def test_row_cache_expands_bidirectionally_and_prefetches() -> None:
    viewer, cache, provider = _make_stub_cache(view_height=6, max_cells=6 * 3)
    columns = tuple(viewer.columns)

    cache.get_visible_table_slice(columns, overscan_hint=24)
    assert provider.calls, "initial fetch should occur"

    provider.calls.clear()
    provider.prefetch_calls.clear()
    viewer.row0 = 48
    cache.get_visible_table_slice(columns, overscan_hint=24)

    assert cache.start >= 0
    assert provider.prefetch_calls, "forward prefetch expected after downward scroll"
    forward_prefetch = provider.prefetch_calls[-1]
    assert forward_prefetch[0] >= cache.end - forward_prefetch[1]

    provider.calls.clear()
    provider.prefetch_calls.clear()
    previous_start = cache.start
    back_target = max(0, previous_start - 4)
    viewer.row0 = back_target
    cache.get_visible_table_slice(columns, overscan_hint=24)

    assert provider.calls, "backward fetch expected when scrolling above cached window"
    assert any(actual > 0 for _, _, actual in provider.calls)
    assert any(start <= previous_start for start, _, actual in provider.calls if actual > 0)
    assert cache.start <= back_target <= cache.end
    assert provider.prefetch_calls, "backward prefetch expected"
    assert provider.prefetch_calls[-1][0] <= cache.start


def test_row_cache_respects_cell_cap_and_reports_eviction() -> None:
    viewer, cache, provider = _make_stub_cache(view_height=8, max_cells=8 * 3)
    columns = tuple(viewer.columns)

    for row in (0, 40, 80, 120, 160):
        viewer.row0 = row
        cache.get_visible_table_slice(columns, overscan_hint=32)

    window_cells = (cache.end - cache.start) * len(columns)
    assert window_cells <= cache.max_cells

    evictions = [payload for _, _, payload in viewer._perf_events if payload.get("evicted_rows")]
    assert evictions, "eviction telemetry should be recorded when trimming the window"


def test_row_cache_streaming_first_chunk() -> None:
    columns = ("c0", "c1")
    provider = _StreamingStubRowProvider(64, columns, chunk_size=2)
    viewer = _StubViewer(provider, columns=columns, view_height=6)
    cache = RowCacheController(viewer, FreezePaneController(viewer))
    cache.streaming_batch_rows = 2

    first = cache.get_visible_table_slice(columns)
    assert first.height == 2, "first chunk should render immediately"

    assert provider.stream_calls, "streaming request should be issued"
    provider.stream_completed.wait(timeout=1.0)
    assert provider.stream_completed.is_set(), "stream should complete"

    cache.get_visible_table_slice(columns)

    payloads = [payload for _, _, payload in viewer._perf_events if payload.get("stream_mode")]
    assert payloads, "streaming telemetry should be recorded"
    last_payload = payloads[-1]
    assert last_payload["stream_mode"] == "stream"
    assert last_payload["stream_batches"] >= 1
    assert "first_batch_ms" in last_payload


def test_row_cache_streaming_respects_flag() -> None:
    columns = ("c0",)
    provider = _StreamingStubRowProvider(32, columns)
    viewer = _StubViewer(provider, columns=columns, view_height=6)
    cache = RowCacheController(viewer, FreezePaneController(viewer), streaming_enabled=False)

    cache.get_visible_table_slice(columns)

    assert not provider.stream_calls, "streaming should be disabled"
    payload = viewer._perf_events[-1][2]
    assert payload["stream_mode"] == "disabled"


def test_row_cache_streaming_fallback_to_eager() -> None:
    columns = ("c0",)
    provider = _StreamingStubRowProvider(16, columns, mode="collect", reason="disabled")
    viewer = _StubViewer(provider, columns=columns, view_height=6)
    cache = RowCacheController(viewer, FreezePaneController(viewer))

    cache.get_visible_table_slice(columns)
    provider.stream_completed.wait(timeout=1.0)
    assert provider.stream_completed.is_set(), "fallback stream should complete"

    assert cache._stream_forced_eager, "fallback should disable subsequent streaming attempts"
    assert len(provider.stream_calls) == 1
    payload = viewer._perf_events[-1][2]
    assert payload["stream_mode"] == "collect"
    assert payload["stream_reason"] == "disabled"

    cache.get_visible_table_slice(columns)
    assert len(provider.stream_calls) == 1, "fallback should avoid repeated streaming calls"
    assert len(provider.calls) >= 2, "eager fetch should be reused after fallback"


def _make_viewer(job_runner) -> Viewer:
    frame = pl.DataFrame(
        {
            "id": list(range(512)),
            "value": [f"v{i}" for i in range(512)],
            "flag": [i % 2 == 0 for i in range(512)],
        }
    )
    sheet = DataSheet(frame.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=12, viewport_cols=6, runner=job_runner)
    viewer.configure_terminal(width=100, height=24)
    return viewer


def test_row_cache_hit_rate_and_memory_bound(job_runner) -> None:
    viewer = _make_viewer(job_runner)
    sequence: list[int] = []
    step = max(1, viewer.view_height // 2)
    center = viewer.view_height * 4
    oscillation = [0, step, step * 2, step, 0, -step, -step * 2, -step]
    for _ in range(6):
        sequence.extend(max(0, center + offset) for offset in oscillation)

    events: list[dict[str, Any]] = []

    def _callback(phase: str, duration: float, payload: dict[str, Any]) -> None:
        if phase == "viewer.row_cache":
            events.append(payload)

    viewer.set_perf_callback(_callback)

    with patch.object(RowProvider, "prefetch", autospec=True, return_value=None):
        for row0 in sequence:
            viewer.row0 = max(0, row0)
            viewer.get_visible_table_slice(viewer.columns)

    cache_events = [payload for payload in events if payload.get("cache")]
    assert cache_events, "row cache events should be recorded"
    hit_count = sum(1 for payload in cache_events if payload.get("cache") in {"hit", "extend"})
    hit_rate = hit_count / len(cache_events)
    assert hit_rate >= 0.9

    cache = viewer._row_cache
    window_cells = (cache.end - cache.start) * len(viewer.columns)
    assert window_cells <= cache.max_cells


def test_viewer_warns_once_for_missing_columns(job_runner) -> None:
    viewer = _make_viewer(job_runner)
    columns = ("id", "missing")

    table_slice = viewer.get_visible_table_slice(columns)

    assert table_slice.column_names == columns

    missing_column = table_slice.column("missing")
    assert missing_column.values == tuple(None for _ in range(table_slice.height))
    assert missing_column.formatted(12) == tuple("⟂ missing" for _ in range(table_slice.height))

    first_warning = viewer.status_message
    assert first_warning is not None

    viewer.status_message = None
    viewer.get_visible_table_slice(columns)

    assert viewer.status_message is None

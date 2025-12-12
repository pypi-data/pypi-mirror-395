from __future__ import annotations

from collections.abc import Sequence

import polars as pl

from pulka.core.engine.contracts import TableColumn, TableSlice
from pulka.core.interfaces import EngineAdapterProtocol, MaterializerProtocol
from pulka.core.plan import QueryPlan
from pulka.core.row_provider import (
    RowProvider,
    SliceStatus,
    SliceStreamRequest,
)


def _make_table_slice(columns: Sequence[str], start: int, length: int) -> TableSlice:
    schema = dict.fromkeys(columns, pl.Int64)
    if length <= 0:
        return TableSlice.empty(columns, schema)

    table_columns: list[TableColumn] = []
    for name in columns:
        values = tuple(start + offset for offset in range(length))

        def _formatter(
            max_chars: int,
            *,
            _name: str = name,
            _values: tuple[int, ...] = values,
        ) -> tuple[str, ...]:
            return tuple(f"{_name}:{value}" for value in _values)

        table_columns.append(TableColumn(name, values, schema[name], 0, _formatter))
    return TableSlice(tuple(table_columns), schema)


class _EchoEngine(EngineAdapterProtocol):
    def compile(self, plan: QueryPlan) -> QueryPlan:
        return plan

    def validate_filter(self, clause: str) -> None:  # pragma: no cover - helper
        return None


class _StreamingMaterializer(MaterializerProtocol):
    def __init__(self, columns: Sequence[str], chunk_sizes: Sequence[int]) -> None:
        self.columns = tuple(columns)
        self.chunk_sizes = tuple(chunk_sizes)
        self.stream_batch_rows: list[int | None] = []

    def collect(self, plan):  # pragma: no cover - helper
        total = sum(self.chunk_sizes)
        return _make_table_slice(self.columns, 0, total)

    def collect_slice(
        self,
        plan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice:
        effective = tuple(columns or self.columns)
        return _make_table_slice(effective, start, length or 0)

    def collect_slice_stream(
        self,
        plan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
        batch_rows: int | None = None,
    ):
        self.stream_batch_rows.append(batch_rows)
        effective = tuple(columns or self.columns)
        remaining = length if length is not None else sum(self.chunk_sizes)
        offset = start
        for size in self.chunk_sizes:
            if remaining is not None and remaining <= 0:
                break
            chunk_len = min(size, remaining) if remaining is not None else size
            yield _make_table_slice(effective, offset, chunk_len)
            offset += chunk_len
            if remaining is not None:
                remaining -= chunk_len

    def count(self, plan):  # pragma: no cover - helper
        return sum(self.chunk_sizes)


def _concat_slices(slices: Sequence[TableSlice]) -> TableSlice:
    if not slices:
        return TableSlice.empty()
    result = slices[0]
    for slice_ in slices[1:]:
        result = result.concat_vertical(slice_)
    return result


def _slice_payload(slice_: TableSlice) -> tuple[tuple[str, ...], tuple[tuple[int, ...], ...]]:
    columns = slice_.column_names
    values = tuple(tuple(col.values) for col in slice_.columns)
    return columns, values


def test_row_provider_streams_batches_and_updates_cache(job_runner) -> None:
    columns = ("id", "value")
    engine = _EchoEngine()
    materializer = _StreamingMaterializer(columns, (3, 3))
    schema = dict.fromkeys(columns, pl.Int64)

    provider = RowProvider.for_plan_source(
        engine_factory=lambda: engine,
        columns_getter=lambda: columns,
        job_context=lambda: ("sheet", 1, "plan-hash"),
        materializer=materializer,
        empty_result_factory=lambda: TableSlice.empty(columns, schema),
        runner=job_runner,
    )

    plan = QueryPlan()
    request = SliceStreamRequest(
        plan=plan,
        columns=columns,
        start=0,
        count=6,
        telemetry={"request_id": "stream-test"},
    )

    chunks = list(provider.get_slice_stream(request))
    assert len(chunks) == 3
    assert [chunk.is_final for chunk in chunks] == [False, False, True]

    partial = _concat_slices([chunk.slice for chunk in chunks[:-1]])
    final_chunk = chunks[-1]
    final_slice = final_chunk.slice

    assert _slice_payload(partial) == _slice_payload(final_slice)

    baseline_slice, baseline_status = provider.get_slice(plan, columns, 0, 6)
    assert baseline_status is SliceStatus.OK
    assert _slice_payload(baseline_slice) == _slice_payload(final_slice)

    metrics = provider.cache_metrics()
    assert metrics["streaming_last_mode"] == "stream"
    assert metrics["streaming_last_chunks"] == len(chunks)
    assert metrics["streaming_last_rows"] == final_slice.height
    assert metrics["streaming_last_cells"] == final_slice.height * len(columns)
    assert metrics["entries"] == 1

    assert final_chunk.telemetry["mode"] == "stream"
    assert final_chunk.telemetry["reason"] == "stream"
    assert final_chunk.telemetry["chunks"] == len(chunks)
    assert final_chunk.telemetry["rows"] == final_slice.height
    assert final_chunk.telemetry["request_id"] == "stream-test"

    assert materializer.stream_batch_rows == [provider.STREAMING_BATCH_ROWS]

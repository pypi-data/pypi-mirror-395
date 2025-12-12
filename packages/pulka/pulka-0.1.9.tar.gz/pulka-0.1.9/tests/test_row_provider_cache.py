from __future__ import annotations

from collections.abc import Sequence

import polars as pl

from pulka.core.engine.contracts import TableColumn, TableSlice
from pulka.core.interfaces import EngineAdapterProtocol, MaterializerProtocol
from pulka.core.plan import QueryPlan
from pulka.core.row_provider import RowProvider, SliceStatus


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

    def validate_filter(self, clause: str) -> None:  # pragma: no cover - not exercised
        return None


class _SyntheticMaterializer(MaterializerProtocol):
    def collect(self, plan):  # pragma: no cover - helper
        return TableSlice.empty()

    def collect_slice(
        self,
        plan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice:
        effective_columns = tuple(columns or ())
        return _make_table_slice(effective_columns, start, length or 0)

    def count(self, plan):  # pragma: no cover - helper
        return 0


def _make_provider(job_runner, columns: Sequence[str] = ("id", "value")) -> RowProvider:
    engine = _EchoEngine()
    materializer = _SyntheticMaterializer()
    schema = dict.fromkeys(columns, pl.Int64)

    provider = RowProvider.for_plan_source(
        engine_factory=lambda: engine,
        columns_getter=lambda: tuple(columns),
        job_context=None,
        materializer=materializer,
        empty_result_factory=lambda: TableSlice.empty(columns, schema),
        runner=job_runner,
    )
    provider._max_cache_entries = 2  # type: ignore[attr-defined]
    provider._max_cache_cells = 6  # type: ignore[attr-defined]
    return provider


def test_row_provider_cache_enforces_lru_and_tracks_evictions(job_runner) -> None:
    provider = _make_provider(job_runner)
    plan = QueryPlan()

    provider.get_slice(plan, ["id"], 0, 2)
    provider.get_slice(plan, ["value"], 0, 2)
    provider.get_slice(plan, ["id"], 4, 2)

    metrics = provider.cache_metrics()
    assert metrics["entries"] <= provider._max_cache_entries  # type: ignore[attr-defined]
    assert metrics["cells"] <= provider._max_cache_cells  # type: ignore[attr-defined]
    assert metrics["evictions"] >= 1


def test_row_provider_emits_placeholders_for_missing_columns(job_runner) -> None:
    provider = _make_provider(job_runner)
    plan = QueryPlan()

    slice_, status = provider.get_slice(plan, ["id", "missing"], 0, 3)

    assert status is SliceStatus.PARTIAL
    assert slice_.column_names == ("id", "missing")

    missing_col = slice_.column("missing")
    assert missing_col.values == (None, None, None)
    assert missing_col.formatted(12) == ("⟂ missing", "⟂ missing", "⟂ missing")

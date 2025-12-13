# mypy: ignore-errors

"""Headless bridge for viewer interactions with the execution engine."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

try:
    import polars as pl
except ImportError:  # pragma: no cover - viewer engine is usable without Polars
    pl = None

from ..errors import MaterializeError, PlanError
from ..plan import QueryPlan
from ..row_provider import RowProvider
from ..source_traits import SourceTraits
from .contracts import EngineAdapter, TableColumn, TableSlice


def _slice_from_mapping(
    mapping: Mapping[str, Sequence[Any]],
    schema: Mapping[str, Any],
) -> TableSlice:
    schema_map = dict(schema)
    columns: list[TableColumn] = []
    for name, values in mapping.items():
        sequence = values
        null_count = sum(1 for value in sequence if value is None)
        columns.append(TableColumn(name, sequence, schema_map.get(name), null_count))
    if not columns:
        return TableSlice.empty(schema_map.keys(), schema_map)
    return TableSlice(tuple(columns), schema_map)


def _slice_from_rows(
    rows: Sequence[Mapping[str, Any]],
    schema: Mapping[str, Any],
) -> TableSlice:
    if not rows:
        return TableSlice.empty(schema.keys(), schema)
    column_order: list[str] = []
    for column in schema:
        if column not in column_order:
            column_order.append(column)
    for row in rows:
        for key in row:
            if key not in column_order:
                column_order.append(key)
    data: dict[str, list[Any]] = {name: [] for name in column_order}
    for row in rows:
        for name in column_order:
            data[name].append(row.get(name))
    return _slice_from_mapping(data, schema)


@dataclass(slots=True)
class ViewerEngine:
    """Adapter that exposes row access and validation for viewer code."""

    row_provider: RowProvider

    def fetch_slice(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
        *,
        schema: Mapping[str, Any],
    ) -> TableSlice:
        result, _status = self.row_provider.get_slice(plan, columns, start, count)
        if isinstance(result, TableSlice):
            return result
        if result is None:
            return TableSlice.empty(schema.keys(), schema)
        if isinstance(result, Mapping):
            return _slice_from_mapping(result, schema)
        if isinstance(result, Sequence):
            if not result:
                return TableSlice.empty(schema.keys(), schema)
            first = result[0]
            if isinstance(first, Mapping):
                return _slice_from_rows(result, schema)
        msg = f"Row provider returned an unsupported slice payload: {type(result)!r}"
        raise MaterializeError(msg)

    def prefetch(
        self,
        plan: QueryPlan | None,
        columns: Sequence[str],
        start: int,
        count: int,
    ) -> None:
        self.row_provider.prefetch(plan, columns, start, count)

    def validate_filter_clause(self, clause: str) -> None:
        compiler = self.row_provider.build_plan_compiler()
        if compiler is None:
            msg = "Filtering is not supported"
            raise PlanError(msg)
        validate = getattr(compiler, "validate_filter", None)
        if callable(validate):
            validate(clause)
            return

        legacy = getattr(compiler, "filter_expression", None)
        if callable(legacy):
            legacy(clause)
            return

        msg = "Filtering is not supported"
        raise PlanError(msg)

    def validate_sql_where(
        self,
        _sheet: Any,
        clause: str,
    ) -> None:
        compiler = self.row_provider.build_plan_compiler()
        validate = getattr(compiler, "validate_sql_where", None) if compiler else None
        if callable(validate):
            validate(clause)
            return
        msg = "SQL filtering not supported"
        raise PlanError(msg)

    def build_plan_compiler(self) -> EngineAdapter | None:
        return self.row_provider.build_plan_compiler()


def infer_source_traits_from_plan(plan: Any) -> SourceTraits | None:
    """Best-effort inference of :class:`~pulka.core.source_traits.SourceTraits`."""

    fallback_kind = getattr(plan, "source_kind", None)
    fallback_path = getattr(plan, "source_path", None)
    lazy_frame = getattr(plan, "lazy_frame", None)
    if lazy_frame is None:
        try:
            from .polars_adapter import coerce_physical_plan, unwrap_physical_plan
        except ImportError:
            return None
        handle = coerce_physical_plan(plan)
        if handle is None:
            return None
        try:
            physical_plan = unwrap_physical_plan(handle)
        except Exception:
            return None
        fallback_kind = getattr(physical_plan, "source_kind", fallback_kind)
        fallback_path = getattr(physical_plan, "source_path", fallback_path)
        lazy_frame = getattr(physical_plan, "lazy_frame", None)

    if lazy_frame is None:
        return None

    if pl is None:
        return None

    if not isinstance(lazy_frame, pl.LazyFrame):
        return None

    try:
        from ..source_traits import infer_from_lazyframe
    except ImportError:
        return None

    try:
        return infer_from_lazyframe(
            lazy_frame,
            fallback_kind=fallback_kind,
            fallback_path=fallback_path,
        )
    except Exception:
        return None


__all__ = ["ViewerEngine", "infer_source_traits_from_plan"]

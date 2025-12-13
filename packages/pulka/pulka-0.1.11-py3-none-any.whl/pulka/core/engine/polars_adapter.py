# mypy: ignore-errors

"""Polars-backed implementation of the core engine contracts."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import polars as pl

from ...data.filter_lang import FilterError, compile_filter_expression
from ..errors import CompileError, MaterializeError, PlanError
from ..formatting import _polars_format_with_dtype
from ..plan import QueryPlan
from ..row_identity import ROW_ID_COLUMN
from .contracts import EnginePayloadHandle, PhysicalPlan, TableColumn, TableSlice

POLARS_ENGINE = "polars"
"""Identifier used for handles backed by the Polars engine."""

_KIND_LAZYFRAME = "lazyframe"
_KIND_PHYSICAL_PLAN = "physical_plan"


@dataclass(slots=True)
class PolarsPhysicalPlan:
    """Wrapper around a compiled Polars ``LazyFrame`` with origin metadata."""

    lazy_frame: pl.LazyFrame
    source_kind: str | None = None
    source_path: str | None = None

    def __post_init__(self) -> None:
        self._attach_metadata(self.lazy_frame)

    def _attach_metadata(self, lazy_frame: pl.LazyFrame) -> None:
        if self.source_kind is not None:
            lazy_frame._pulka_source_kind = self.source_kind  # type: ignore[attr-defined]
        if self.source_path is not None:
            lazy_frame._pulka_path = self.source_path  # type: ignore[attr-defined]

    @classmethod
    def from_lazyframe(cls, lazy_frame: pl.LazyFrame) -> PolarsPhysicalPlan:
        """Create a physical plan wrapper from ``lazy_frame``."""

        return cls(
            lazy_frame,
            source_kind=getattr(lazy_frame, "_pulka_source_kind", None),
            source_path=getattr(lazy_frame, "_pulka_path", None),
        )

    def to_lazyframe(self) -> pl.LazyFrame:
        """Expose the underlying Polars lazy plan for compatibility consumers."""

        return self.lazy_frame

    def with_slice(self, offset: int, length: int | None = None) -> PolarsPhysicalPlan:
        return PolarsPhysicalPlan(
            self.lazy_frame.slice(offset, length),
            source_kind=self.source_kind,
            source_path=self.source_path,
        )

    def with_projection(self, columns: Sequence[str]) -> PolarsPhysicalPlan:
        return PolarsPhysicalPlan(
            self.lazy_frame.select([pl.col(name) for name in columns]),
            source_kind=self.source_kind,
            source_path=self.source_path,
        )

    def collect(self) -> pl.DataFrame:
        return self.lazy_frame.collect()


SqlExecutor = Callable[[pl.LazyFrame, str], pl.LazyFrame]


def default_sql_executor() -> SqlExecutor | None:
    """Return the default SQL executor for the active Polars build."""

    try:  # pragma: no cover - depends on optional polars SQL feature
        from polars import SQLContext
    except ImportError:  # pragma: no cover - fallback when SQL not available
        return None

    def _execute(lf: pl.LazyFrame, where_clause: str) -> pl.LazyFrame:
        ctx = SQLContext()
        ctx.register("data", lf)
        query = f"SELECT * FROM data WHERE {where_clause}"
        try:
            result = ctx.execute(query, lazy=True)
        except TypeError:  # pragma: no cover - depends on polars version
            result = ctx.execute(query)
        if isinstance(result, pl.LazyFrame):
            return result
        return result.lazy()

    return _execute


def _valid_projection(names: Iterable[str], available: Sequence[str]) -> list[str]:
    available_set = set(available)
    projection: list[str] = []
    for name in names:
        if name in available_set and name not in projection:
            projection.append(name)
    return projection


@dataclass(slots=True)
class PlanCompiler:
    """Turn :class:`QueryPlan` objects into Polars ``LazyFrame`` pipelines."""

    source: pl.LazyFrame
    columns: Sequence[str]
    schema: dict[str, pl.DataType]
    sql_executor: SqlExecutor | None = None
    _filter_cache: dict[str, pl.Expr] = field(default_factory=dict, init=False)
    _search_cache: dict[tuple[str, str], pl.Expr] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.columns = tuple(self.columns)
        self.schema = dict(self.schema)

    def compile(self, plan: QueryPlan) -> PhysicalPlan:
        lf = self.source

        source_kind = getattr(self.source, "_pulka_source_kind", None)
        source_path = getattr(self.source, "_pulka_path", None)

        try:
            sql_clauses = [c.text for c in plan.filter_clauses if c.kind == "sql"]
            expr_clauses = [c.text for c in plan.filter_clauses if c.kind == "expr"]

            if sql_clauses:
                if self.sql_executor is None:
                    msg = "SQL filtering is not supported by this engine"
                    raise PlanError(msg)
                for clause in sql_clauses:
                    lf = self.sql_executor(lf, clause)

            for clause in expr_clauses:
                expr = self._compile_filter_clause(clause)
                lf = lf.filter(expr)

            search_expr = self._compile_search(plan)
            if search_expr is not None:
                lf = lf.filter(search_expr)

            if plan.sort:
                lf = lf.sort(
                    by=list(plan.sort_columns()),
                    descending=list(plan.sort_descending()),
                    nulls_last=True,
                )

            if plan.offset or plan.limit is not None:
                lf = lf.slice(plan.offset, plan.limit)

            projection = plan.projection_or(self.columns)
            projection_cols = _valid_projection(projection, self.columns)
            if projection_cols:
                lf = lf.select([pl.col(name) for name in projection_cols])
        except PlanError:
            raise
        except Exception as exc:
            msg = "Failed to compile query plan"
            raise CompileError(msg) from exc

        return make_physical_plan_handle(
            PolarsPhysicalPlan(lf, source_kind=source_kind, source_path=source_path)
        )

    def validate_filter(self, clause: str) -> None:
        """Validate ``clause`` by compiling it to a Polars expression."""

        self.filter_expression(clause)

    def filter_expression(self, clause: str) -> pl.Expr:
        """Return a compiled Polars expression for ``clause``."""

        return self._compile_filter_clause(clause)

    def validate_sql_where(self, clause: str) -> None:
        """Ensure the configured SQL executor accepts ``clause``."""

        if self.sql_executor is None:
            msg = "SQL filtering not supported"
            raise PlanError(msg)

        try:
            candidate = self.sql_executor(self.source, clause)
            if hasattr(candidate, "limit"):
                candidate = candidate.limit(0)
            if not hasattr(candidate, "collect"):
                msg = "SQL executor must return an eager-collectable object"
                raise PlanError(msg)
            candidate.collect()
        except PlanError:
            raise
        except Exception as exc:
            msg = "SQL validation failed"
            raise PlanError(msg) from exc

    def _compile_filter_clause(self, clause: str) -> pl.Expr:
        cached = self._filter_cache.get(clause)
        if cached is not None:
            return cached
        try:
            expr = compile_filter_expression(clause, self.columns)
        except FilterError as exc:
            raise PlanError(str(exc)) from exc
        except Exception as exc:
            msg = "Failed to compile filter expression"
            raise CompileError(msg) from exc
        self._filter_cache[clause] = expr
        return expr

    def _compile_search(self, plan: QueryPlan) -> pl.Expr | None:
        if not plan.search_text:
            return None

        column = self._search_target_column(plan)
        if column is None:
            return None

        key = (column, plan.search_text)
        cached = self._search_cache.get(key)
        if cached is not None:
            return cached

        expr = _build_search_expr(column, plan.search_text, self.schema.get(column))
        self._search_cache[key] = expr
        return expr

    def _search_target_column(self, plan: QueryPlan) -> str | None:
        available = list(self.columns)
        if plan.projection:
            available = [col for col in plan.projection if col in self.schema]
        if plan.sort:
            for column, _ in plan.sort:
                if column in self.schema:
                    return column
        for column in available:
            if column in self.schema:
                return column
        for column in self.schema:
            return column
        return None


@dataclass(slots=True)
class Materializer:
    """Collect Polars ``LazyFrame`` objects into eager data structures."""

    row_id_column: str | None = ROW_ID_COLUMN

    def collect(self, plan: PhysicalPlan) -> TableSlice:
        polars_plan = unwrap_physical_plan(plan)
        try:
            df = polars_plan.lazy_frame.collect()
            schema = dict(df.schema)
            return table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
        except Exception as exc:
            msg = "Failed to materialise physical plan"
            raise MaterializeError(msg) from exc

    def collect_slice(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice:
        polars_plan = unwrap_physical_plan(plan)
        lf = polars_plan.lazy_frame
        if start or length is not None:
            lf = lf.slice(start, length)
        if columns:
            lf = lf.select([pl.col(name) for name in columns])
        try:
            df = lf.collect()
            schema = dict(df.schema)
            return table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
        except Exception as exc:
            msg = "Failed to materialise slice"
            raise MaterializeError(msg) from exc

    def collect_slice_stream(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
        batch_rows: int | None = None,
    ) -> Iterator[TableSlice]:
        polars_plan = unwrap_physical_plan(plan)
        lf = polars_plan.lazy_frame
        if start or length is not None:
            lf = lf.slice(start, length)
        if columns:
            lf = lf.select([pl.col(name) for name in columns])
        if not hasattr(lf, "collect_batches"):
            df = lf.collect()
            schema = dict(df.schema)
            yield table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
            return
        kwargs: dict[str, object] = {"streaming": True}
        if batch_rows is not None and batch_rows > 0:
            kwargs["n_rows"] = batch_rows
        try:
            batches = lf.collect_batches(**kwargs)
        except (TypeError, AttributeError):
            kwargs.pop("n_rows", None)
            try:
                batches = lf.collect_batches(**kwargs)
            except Exception:
                df = lf.collect()
                schema = dict(df.schema)
                yield table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
                return
        except Exception:
            df = lf.collect()
            schema = dict(df.schema)
            yield table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
            return

        try:
            iterator = iter(batches)
        except TypeError:
            df = lf.collect()
            schema = dict(df.schema)
            yield table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)
            return

        for df in iterator:
            schema = dict(df.schema)
            yield table_slice_from_dataframe(df, schema, row_id_column=self.row_id_column)

    def count(self, plan: PhysicalPlan) -> int | None:
        try:
            polars_plan = unwrap_physical_plan(plan)
            df = polars_plan.lazy_frame.select(pl.len().alias("__len__")).collect()
        except Exception:
            return None
        table_slice = table_slice_from_dataframe(df, df.schema)
        if table_slice.height == 0:
            return 0
        first_column = table_slice.column_at(0)
        if not first_column.values:
            return 0
        return int(first_column.values[0])


def _build_search_expr(column: str, text: str, dtype: pl.DataType | None) -> pl.Expr:
    pattern = f"(?i){re.escape(text)}"
    col_expr = pl.col(column)
    if dtype is not None and str(dtype).startswith(("String", "Utf8")):
        base = col_expr.fill_null("")
    else:
        base = col_expr.cast(pl.Utf8, strict=False).fill_null("")
    contains_expr = base.str.contains(pattern, literal=False).fill_null(False)
    normalized = text.strip().lower()
    if normalized in {"none", "null"}:
        return col_expr.is_null() | contains_expr
    return contains_expr


def table_slice_from_dataframe(
    df: pl.DataFrame,
    schema: Mapping[str, pl.DataType],
    *,
    row_id_column: str | None = None,
) -> TableSlice:
    """Convert a Polars DataFrame into a :class:`TableSlice`.

    When ``row_id_column`` is present in ``df`` it is removed from the visible
    columns and attached to the slice via ``TableSlice.row_ids``.
    """

    row_ids = None
    if row_id_column and row_id_column in df.columns:
        try:
            row_ids = df.get_column(row_id_column)
        except Exception:  # pragma: no cover - defensive
            row_ids = None
        schema = {name: dtype for name, dtype in schema.items() if name != row_id_column}

    column_names = tuple(name for name in df.columns if not row_id_column or name != row_id_column)
    columns: list[TableColumn] = []
    for name in column_names:
        series = df.get_column(name)
        dtype = schema.get(name, series.dtype)
        null_count = int(series.null_count())

        display_cache: dict[int | None, list[str]] = {}

        def _display(
            row: int,
            _abs_row: int,
            value: Any,
            width: int | None,
            *,
            _series=series,
            _cache=display_cache,
        ) -> str:
            key = None if width is None else max(width, 0)
            formatted = _cache.get(key)
            if formatted is None:
                max_chars = 0 if key is None else key
                formatted_list = _polars_format_with_dtype(
                    _series, max_items=4, max_chars=max_chars
                )
                formatted = list(formatted_list)
                _cache[key] = formatted
            if 0 <= row < len(formatted):
                return formatted[row]
            if value is None:
                return ""
            return str(value)

        columns.append(TableColumn(name, series, dtype, null_count, _display))

    return TableSlice(tuple(columns), schema, row_ids=row_ids)


def dataframe_from_table_slice(table_slice: TableSlice) -> pl.DataFrame:
    """Reconstruct a Polars ``DataFrame`` from a :class:`TableSlice`."""

    if not table_slice.columns:
        return pl.DataFrame()

    data: dict[str, pl.Series] = {}
    for column in table_slice.columns:
        data[column.name] = pl.Series(column.name, column.values, dtype=column.dtype)

    df = pl.DataFrame(data)
    ordered_names = list(table_slice.column_names)
    if set(ordered_names) == set(df.columns):
        return df.select(ordered_names)
    return df


def make_lazyframe_handle(lazy_frame: pl.LazyFrame) -> EnginePayloadHandle[pl.LazyFrame]:
    """Wrap ``lazy_frame`` in an engine-neutral handle."""

    return EnginePayloadHandle(POLARS_ENGINE, _KIND_LAZYFRAME, lazy_frame)


def unwrap_lazyframe_handle(handle: EnginePayloadHandle[pl.LazyFrame]) -> pl.LazyFrame:
    """Return the Polars ``LazyFrame`` stored in ``handle``."""

    if not isinstance(handle, EnginePayloadHandle):  # pragma: no cover - defensive
        msg = f"Expected EnginePayloadHandle, got {type(handle)!r}"
        raise TypeError(msg)
    return handle.unwrap(expected_engine=POLARS_ENGINE, expected_kind=_KIND_LAZYFRAME)


def make_physical_plan_handle(plan: PolarsPhysicalPlan) -> PhysicalPlan:
    """Wrap ``plan`` in an engine-neutral handle."""

    return EnginePayloadHandle(POLARS_ENGINE, _KIND_PHYSICAL_PLAN, plan)


def unwrap_physical_plan(handle: PhysicalPlan) -> PolarsPhysicalPlan:
    """Return the ``PolarsPhysicalPlan`` stored in ``handle``."""

    if not isinstance(handle, EnginePayloadHandle):  # pragma: no cover - defensive
        msg = f"Expected EnginePayloadHandle, got {type(handle)!r}"
        raise TypeError(msg)
    return handle.unwrap(expected_engine=POLARS_ENGINE, expected_kind=_KIND_PHYSICAL_PLAN)


def coerce_physical_plan(candidate: object) -> PhysicalPlan | None:
    """Return a Polars physical plan handle when ``candidate`` represents one."""

    if isinstance(candidate, EnginePayloadHandle):
        metadata = candidate.as_serializable()
        if metadata.get("engine") == POLARS_ENGINE and metadata.get("kind") == _KIND_PHYSICAL_PLAN:
            return candidate
        return None
    if isinstance(candidate, PolarsPhysicalPlan):
        return make_physical_plan_handle(candidate)
    if isinstance(candidate, pl.LazyFrame):
        return make_physical_plan_handle(PolarsPhysicalPlan.from_lazyframe(candidate))
    return None


__all__ = [
    "POLARS_ENGINE",
    "Materializer",
    "PlanCompiler",
    "PolarsPhysicalPlan",
    "SqlExecutor",
    "coerce_physical_plan",
    "make_lazyframe_handle",
    "make_physical_plan_handle",
    "default_sql_executor",
    "dataframe_from_table_slice",
    "unwrap_lazyframe_handle",
    "unwrap_physical_plan",
    "table_slice_from_dataframe",
]

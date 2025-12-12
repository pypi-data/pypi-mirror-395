"""Polars-backed sheet used across the application."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any, ClassVar, cast
from uuid import uuid4

import polars as pl

from ..core.engine.contracts import EnginePayloadHandle, PhysicalPlan, TableSlice
from ..core.engine.polars_adapter import Materializer as PolarsMaterializer
from ..core.engine.polars_adapter import (
    PlanCompiler,
    PolarsPhysicalPlan,
    coerce_physical_plan,
    dataframe_from_table_slice,
    default_sql_executor,
    make_lazyframe_handle,
    make_physical_plan_handle,
    unwrap_physical_plan,
)
from ..core.interfaces import (
    JobRunnerProtocol,
    MaterializerProtocol,
    is_materializer_compatible,
)
from ..core.plan import QueryPlan, normalized_columns_key
from ..core.plan_ops import set_projection as plan_set_projection
from ..core.plan_ops import toggle_sort as plan_toggle_sort
from ..core.row_identity import ROW_ID_COLUMN
from ..core.row_provider import RowProvider
from ..core.sheet import (
    SHEET_FEATURE_LEGACY_PREVIEW,
    SHEET_FEATURE_PLAN,
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    SheetFeature,
)


class DataSheet:
    """Sheet implementation wrapping a Polars ``LazyFrame``."""

    _CAPABILITIES: ClassVar[frozenset[SheetFeature]] = frozenset(
        {
            SHEET_FEATURE_PLAN,
            SHEET_FEATURE_PREVIEW,
            SHEET_FEATURE_SLICE,
            SHEET_FEATURE_VALUE_AT,
            SHEET_FEATURE_ROW_COUNT,
            SHEET_FEATURE_LEGACY_PREVIEW,
        }
    )

    def __init__(
        self,
        source: pl.LazyFrame | PhysicalPlan,
        *,
        plan: QueryPlan | None = None,
        schema: dict[str, pl.DataType] | None = None,
        columns: Sequence[str] | None = None,
        sheet_id: str | None = None,
        generation: int | None = None,
        compiler: PlanCompiler | None = None,
        materializer: MaterializerProtocol | None = None,
        runner: JobRunnerProtocol,
    ) -> None:
        physical_handle = self._coerce_physical_plan(source)
        base_physical = unwrap_physical_plan(physical_handle)
        base_lazyframe = base_physical.to_lazyframe()
        lf_with_ids, row_id_column = self._attach_row_id_column(base_lazyframe)
        self._row_id_column = row_id_column

        physical_with_ids = PolarsPhysicalPlan(
            lf_with_ids,
            source_kind=base_physical.source_kind,
            source_path=base_physical.source_path,
        )
        self._physical_source: PolarsPhysicalPlan = physical_with_ids
        self._physical_source_handle: PhysicalPlan = make_physical_plan_handle(physical_with_ids)
        self.lf0: EnginePayloadHandle[pl.LazyFrame] = make_lazyframe_handle(
            physical_with_ids.to_lazyframe()
        )
        if not isinstance(runner, JobRunnerProtocol):
            msg = "runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self.sheet_id = sheet_id or uuid4().hex
        self._runner = runner
        self._generation = generation or self._runner.bump_generation(self.sheet_id)

        if schema is None:
            try:
                schema = lf_with_ids.collect_schema()
            except Exception:
                schema = lf_with_ids.schema
        full_schema = dict(schema)
        self._full_schema: dict[str, pl.DataType] = dict(full_schema)
        if self._row_id_column and self._row_id_column in full_schema:
            full_schema.pop(self._row_id_column, None)
        self.schema: dict[str, pl.DataType] = full_schema

        self.columns = [
            name for name in (columns or self.schema.keys()) if name != self._row_id_column
        ]

        self._sql_executor = default_sql_executor()
        compiler_columns = list(self.columns)
        if self._row_id_column and self._row_id_column in self._full_schema:
            compiler_columns.append(self._row_id_column)

        self._compiler = compiler or PlanCompiler(
            lf_with_ids,
            columns=compiler_columns,
            schema=self._full_schema,
            sql_executor=self._sql_executor,
        )
        if materializer is None:
            materializer = PolarsMaterializer(row_id_column=self._row_id_column)
        elif not is_materializer_compatible(materializer):
            msg = "materializer must implement MaterializerProtocol"
            raise TypeError(msg)
        self._materializer = cast(MaterializerProtocol, materializer)

        self._plan: QueryPlan = plan or QueryPlan()

        self._row_provider = RowProvider.for_plan_source(
            engine_factory=self._compiler_factory,
            columns_getter=lambda: self.columns,
            job_context=self.job_context,
            materializer=self._materializer,
            empty_result_factory=self._empty_result,
            runner=self._runner,
            row_id_column=self._row_id_column,
        )

        self._cached_plan_snapshot: dict[str, Any] | None = None

    # Public accessors -------------------------------------------------
    @property
    def plan(self) -> QueryPlan:
        return self._plan

    def with_plan(self, plan: QueryPlan) -> DataSheet:
        if plan == self._plan:
            return self
        return self.__class__(
            self._physical_source_handle,
            plan=plan,
            schema=self.schema,
            columns=self.columns,
            sheet_id=self.sheet_id,
            generation=self._runner.bump_generation(self.sheet_id),
            compiler=self._compiler,
            materializer=self._materializer,
            runner=self._runner,
        )

    # ------------------------------------------------------------------
    # Sheet protocol helpers
    # ------------------------------------------------------------------
    def schema_dict(self) -> dict[str, pl.DataType]:
        """Return the cached schema mapping."""

        return dict(self.schema)

    def _column_signature(self) -> str:
        """Return a stable signature of the current column ordering."""

        return normalized_columns_key(self.columns)

    @property
    def lf(self) -> EnginePayloadHandle[pl.LazyFrame]:
        """Expose the current lazy plan for compatibility consumers."""

        compiled = self._compiler.compile(self._plan)
        polars_plan = unwrap_physical_plan(compiled)
        return make_lazyframe_handle(polars_plan.to_lazyframe())

    @property
    def source(self) -> EnginePayloadHandle[pl.LazyFrame]:
        """Alias of :pyattr:`lf` maintained for backwards compatibility."""

        return self.lf

    def to_lazyframe(self) -> EnginePayloadHandle[pl.LazyFrame]:
        """Return the underlying lazy source without active plan transforms."""

        return self.lf0

    def physical_plan(self) -> PhysicalPlan:
        """Expose the base physical plan for engine adapters."""

        return self._physical_source_handle

    def plan_snapshot(self) -> dict[str, Any]:
        """Return a snapshot payload for recorder hooks."""

        if self._cached_plan_snapshot is None:
            self._cached_plan_snapshot = self._plan.snapshot()
        return dict(self._cached_plan_snapshot)

    # ------------------------------------------------------------------
    # Core protocol
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        plan = self._compiler.compile(self._plan)
        count = self._materializer.count(plan)
        if count is None:
            return 0
        return int(count)

    def fetch_slice(self, row_start: int, row_count: int, columns: Sequence[str]) -> TableSlice:
        slice_, _status = self.row_provider.get_slice(
            self._plan,
            columns,
            row_start,
            row_count,
        )
        return slice_

    def get_value_at(self, row_index: int, column_name: str | None = None) -> object:
        if row_index < 0:
            raise IndexError("row index must be non-negative")

        available = self.columns
        if not available:
            raise IndexError("sheet has no columns")

        target_column = column_name or available[0]
        if target_column not in available:
            raise KeyError(f"unknown column: {target_column}")

        base_plan = self._plan
        projection = base_plan.projection
        if not projection:
            projection = [target_column]
            for column, _ in base_plan.sort:
                if column in available and column not in projection:
                    projection.append(column)
        plan_for_value = replace(base_plan, projection=tuple(projection))

        table_slice, _status = self.row_provider.get_slice(
            plan_for_value,
            [target_column],
            row_index,
            1,
        )
        if table_slice.height == 0:
            raise IndexError("row index out of range")
        column = table_slice.column(target_column)
        if not column.values:
            raise IndexError("row index out of range")
        return column.values[0]

    def snapshot_transforms(self) -> QueryPlan:
        return self._plan

    def restore_transforms(self, snapshot: QueryPlan) -> None:
        if isinstance(snapshot, QueryPlan):
            self._update_plan(snapshot)

    def restore_plan(self, plan: QueryPlan) -> None:
        self.restore_transforms(plan)

    # ------------------------------------------------------------------
    # Query helpers used by the viewer layer
    # ------------------------------------------------------------------
    def preview(self, rows: int, cols: Sequence[str] | None = None) -> TableSlice:
        projection = cols if cols is not None else self._plan.projection
        plan = plan_set_projection(self._plan, projection or self.columns)
        plan = replace(plan, offset=0, limit=rows)
        compiled = self._compiler.compile(plan)
        return self._materializer.collect(compiled)

    def preview_dataframe(self, rows: int, cols: Sequence[str] | None = None) -> pl.DataFrame:
        table_slice = self.preview(rows, cols)
        return dataframe_from_table_slice(table_slice)

    def toggle_sort(self, column: str) -> None:
        """Cycle the sort order for ``column`` on the underlying plan."""

        self._update_plan(plan_toggle_sort(self._plan, column))

    def value_at(self, row: int, col: str) -> object:
        return self.get_value_at(row, col)

    def row_count(self) -> int | None:
        plan = self._compiler.compile(self._plan)
        return self._materializer.count(plan)

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    # ------------------------------------------------------------------
    # Viewer/job helpers
    # ------------------------------------------------------------------
    @property
    def job_runner(self) -> JobRunnerProtocol:
        return self._runner

    @property
    def row_provider(self) -> RowProvider:
        return self._row_provider

    def row_provider_config(self) -> dict[str, Any]:
        """Return constructor kwargs for :class:`RowProvider` consumers."""

        return {
            "engine_factory": self._compiler_factory,
            "columns_getter": lambda: self.columns,
            "materializer": self._materializer,
            "job_context": self.job_context,
            "empty_result_factory": self._empty_result,
            "runner": self._runner,
            "row_id_column": self._row_id_column,
        }

    def job_context(self) -> tuple[str, int, str]:
        snapshot = self.plan_snapshot()
        return (self.sheet_id, self._generation, snapshot["hash"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _update_plan(self, plan: QueryPlan) -> None:
        if plan == self._plan:
            return
        self._plan = plan
        self._cached_plan_snapshot = None
        self._generation = self._runner.bump_generation(self.sheet_id)
        self._row_provider.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _compiler_factory(self) -> PlanCompiler:
        return self._compiler

    def _empty_result(self) -> TableSlice:
        return TableSlice.empty(self.columns, self.schema)

    def _attach_row_id_column(self, lf: pl.LazyFrame) -> tuple[pl.LazyFrame, str | None]:
        """Attach a stable row id column if the name is available."""

        target_column = ROW_ID_COLUMN
        try:
            existing = lf.collect_schema()
        except Exception:
            try:
                existing = lf.schema
            except Exception:
                existing = {}
        if target_column in existing:
            return lf, target_column

        try:
            with_ids = lf.with_row_count(name=target_column)
        except Exception:
            return lf, None
        return with_ids, target_column

    def _coerce_physical_plan(self, source: pl.LazyFrame | PhysicalPlan) -> PhysicalPlan:
        handle = coerce_physical_plan(source)
        if handle is not None:
            return handle
        to_lazy = getattr(source, "to_lazyframe", None)
        if callable(to_lazy):
            lazy = to_lazy()
            coerced = coerce_physical_plan(lazy)
            if coerced is not None:
                return coerced
        msg = "Unsupported source type for DataSheet"
        raise TypeError(msg)


__all__ = ["DataSheet", "normalized_columns_key"]

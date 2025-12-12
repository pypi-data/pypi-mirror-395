"""Legacy helpers for compiling query plans."""

from __future__ import annotations

from collections.abc import Sequence

import polars as pl

from ..core.engine.polars_adapter import PlanCompiler, SqlExecutor
from ..sheets.query_plan import QueryPlan


def _infer_schema(lf: pl.LazyFrame) -> dict[str, pl.DataType]:
    try:
        return lf.collect_schema()
    except Exception:
        return lf.schema


def compile_plan(
    plan: QueryPlan,
    *,
    source: pl.LazyFrame,
    columns: Sequence[str],
    sql_exec: SqlExecutor | None = None,
) -> pl.LazyFrame:
    """Return a ``LazyFrame`` produced by applying ``plan`` to ``source``."""

    compiler = PlanCompiler(
        source,
        columns=columns,
        schema=_infer_schema(source),
        sql_executor=sql_exec,
    )
    return compiler.compile(plan)


__all__ = ["compile_plan", "SqlExecutor"]

from __future__ import annotations

import polars as pl

from pulka.core.engine.polars_adapter import unwrap_physical_plan
from pulka.core.plan import FilterClause
from pulka.data.query import compile_plan
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.query_plan import QueryPlan


def test_snapshot_hash_stability_noop_changes() -> None:
    plan = QueryPlan(
        filters=("c.a > 1",),
        sort=(("b", False),),
        projection=("a", "b"),
        limit=None,
        offset=0,
    )

    snapshot_1 = plan.snapshot()
    snapshot_2 = plan.snapshot()

    assert snapshot_1 == snapshot_2


def test_compile_plan_supports_filters_projection_and_limit() -> None:
    lf = pl.DataFrame({"a": [1, 2, 3, 4], "b": ["w", "x", "y", "z"]}).lazy()
    plan = QueryPlan(filters=("c.a > 1",), projection=("b",), limit=2)

    compiled = compile_plan(plan, source=lf, columns=("a", "b"))
    result = unwrap_physical_plan(compiled).collect()

    assert result.to_dict(as_series=False) == {"b": ["x", "y"]}


def test_compile_plan_sorts_before_limit() -> None:
    lf = pl.DataFrame({"a": [1, 2, 3]}).lazy()
    plan = QueryPlan(sort=(("a", True),), limit=1)

    compiled = compile_plan(plan, source=lf, columns=("a",))
    result = unwrap_physical_plan(compiled).collect()

    assert result["a"].to_list() == [3]


def test_compile_plan_applies_sql_then_expr_filters() -> None:
    lf = pl.DataFrame({"a": [1, 2, 3, 4], "b": [0, 2, 3, 4]}).lazy()
    calls: list[tuple[str, str]] = []

    def sql_exec(lazyframe: pl.LazyFrame, clause: str) -> pl.LazyFrame:
        calls.append(("sql", clause))
        return lazyframe.filter(pl.col("b") > 1)

    plan = QueryPlan(
        filter_clauses=(
            FilterClause("expr", "c.a > 2"),
            FilterClause("sql", "b > 1"),
        )
    )

    compiled = compile_plan(plan, source=lf, columns=("a", "b"), sql_exec=sql_exec)
    result = unwrap_physical_plan(compiled).collect()

    assert calls == [("sql", "b > 1")]
    assert result.to_dict(as_series=False) == {"a": [3, 4], "b": [3, 4]}


def test_compile_plan_applies_sort_only_on_collect(monkeypatch, job_runner) -> None:
    df = pl.DataFrame({"a": [3, 1, 2]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    sheet.toggle_sort("a")

    lazy_type = type(df.lazy())
    call_count = 0

    original_collect = lazy_type.collect

    def wrapped(self, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        return original_collect(self, *args, **kwargs)

    monkeypatch.setattr(lazy_type, "collect", wrapped)

    out = sheet.fetch_slice(0, 2, ["a"])

    assert out.column_names == ("a",)
    assert list(out.column("a").values) == [1, 2]
    assert call_count == 1


def test_fetch_slice_respects_projection_and_sort(job_runner) -> None:
    df = pl.DataFrame({"id": [1, 2, 3], "value": [30, 10, 20], "extra": ["x", "y", "z"]})
    sheet = DataSheet(df.lazy(), runner=job_runner)
    sheet.toggle_sort("value")
    sheet._update_plan(sheet.plan.with_projection(["value", "id"]))

    out = sheet.fetch_slice(0, 2, ["value", "id", "extra"])

    assert out.column_names == ("value", "id", "extra")
    assert list(out.column("value").values) == [10, 20]
    assert list(out.column("id").values) == [2, 3]
    assert list(out.column("extra").values) == [None, None]

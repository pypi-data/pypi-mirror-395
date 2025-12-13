from __future__ import annotations

import threading

import pytest

from pulka.core.engine.contracts import TableSlice
from pulka.core.engine.viewer_engine import ViewerEngine
from pulka.core.errors import CancelledError, CompileError, MaterializeError, PlanError
from pulka.core.plan import QueryPlan
from pulka.core.plan_ops import toggle_sort
from pulka.core.row_provider import RowProvider
from pulka.core.viewer.plan_controller import PlanController
from pulka.core.viewer.viewer import Viewer


class _FailingAdapter:
    def compile(self, plan: QueryPlan) -> object:  # pragma: no cover - helper
        raise ValueError("boom")

    def validate_filter(self, clause: str) -> None:  # pragma: no cover - helper
        return None


class _CollectingAdapter:
    def __init__(self, payload: object) -> None:
        self._payload = payload

    def compile(self, plan: QueryPlan) -> object:  # pragma: no cover - helper
        return self._payload

    def validate_filter(self, clause: str) -> None:  # pragma: no cover - helper
        return None


class _FailingMaterializer:
    def collect(self, plan: object) -> TableSlice:  # pragma: no cover - helper
        raise ValueError("cannot collect")

    def collect_slice(self, *args, **kwargs):  # pragma: no cover - helper
        raise ValueError("cannot collect")

    def count(self, plan: object) -> int | None:  # pragma: no cover - helper
        return None


class _PassthroughMaterializer:
    def __init__(self, slice_: TableSlice) -> None:
        self._slice = slice_

    def collect(self, plan: object) -> TableSlice:  # pragma: no cover - helper
        return self._slice

    def collect_slice(self, *args, **kwargs):  # pragma: no cover - helper
        return self._slice

    def count(self, plan: object) -> int | None:  # pragma: no cover - helper
        return self._slice.height


class _MinimalSheet:
    def __init__(self, plan: QueryPlan) -> None:
        self._plan = plan
        self.columns = ("value",)
        self.schema = {"value": "i64"}

    def plan(self) -> QueryPlan:
        return self._plan

    def with_plan(self, plan: QueryPlan) -> _MinimalSheet:
        return _MinimalSheet(plan)

    def fetch_slice(self, start: int, count: int, columns: list[str]) -> TableSlice:
        return _empty_slice()


def _empty_slice() -> TableSlice:
    return TableSlice.empty(("value",), {"value": None})


class _NoFilterProvider:
    def build_plan_compiler(self):  # pragma: no cover - helper
        return None


def test_toggle_sort_invalid_cycle_raises_plan_error() -> None:
    plan = QueryPlan()
    with pytest.raises(PlanError, match="unsupported sort state"):
        toggle_sort(plan, "value", cycle=("bogus",))


def test_row_provider_wraps_compile_failures(job_runner) -> None:
    provider = RowProvider.for_plan_source(
        engine_factory=_FailingAdapter,
        columns_getter=lambda: ["value"],
        job_context=None,
        materializer=_PassthroughMaterializer(_empty_slice()),
        empty_result_factory=_empty_slice,
        runner=job_runner,
    )

    with pytest.raises(CompileError, match="Failed to compile"):
        provider.get_slice(QueryPlan(), ["value"], 0, 5)


def test_viewer_engine_reports_missing_filter_support() -> None:
    engine = ViewerEngine(_NoFilterProvider())

    with pytest.raises(PlanError, match="Filtering is not supported"):
        engine.validate_filter_clause("value > 1")


def test_row_provider_wraps_materialize_failures(job_runner) -> None:
    provider = RowProvider.for_plan_source(
        engine_factory=lambda: _CollectingAdapter(object()),
        columns_getter=lambda: ["value"],
        job_context=None,
        materializer=_FailingMaterializer(),
        empty_result_factory=_empty_slice,
        runner=job_runner,
    )

    with pytest.raises(MaterializeError, match="materialise row slice"):
        provider.get_slice(QueryPlan(), ["value"], 0, 5)


def test_job_runner_cancellation_raises_typed_error(job_runner) -> None:
    class _Sheet:
        sheet_id = "sheet"

        def job_context(self):  # pragma: no cover - helper
            return self.sheet_id, 0, "hash"

    sheet = _Sheet()

    block = threading.Event()

    def _slow(_: int) -> str:
        block.wait(0.5)
        return "first"

    first = job_runner.submit(sheet, "rows", _slow)
    second = job_runner.submit(sheet, "rows", lambda _: "second")

    assert second.result().value == "second"
    block.set()
    with pytest.raises(CancelledError):
        first.result()


def test_plan_controller_propagates_compile_errors(job_runner) -> None:
    sheet = _MinimalSheet(QueryPlan())
    viewer = Viewer(sheet, runner=job_runner)

    controller = PlanController(viewer)

    def _broken(plan: QueryPlan) -> QueryPlan:
        raise PlanError("broken plan")

    with pytest.raises(PlanError, match="broken plan"):
        controller.apply_plan_update("boom", _broken)

"""Protocols describing cross-layer service contracts for Pulka core."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import Future
from typing import Any, Protocol, runtime_checkable

from .engine.contracts import Materializer, PhysicalPlan, TableSlice
from .jobs import Generation, JobRequest, JobResult, JobTag


@runtime_checkable
class JobRunnerProtocol(Protocol):
    """Interface required by background job coordinators."""

    def get(self, sheet_id: str, tag: JobTag) -> JobResult | None: ...

    def enqueue(self, req: JobRequest) -> Future[JobResult]: ...

    def submit(
        self,
        sheet: Any,
        tag: JobTag,
        fn: Callable[[Generation], Any],
        *,
        cache_result: bool = True,
        priority: int = 0,
    ) -> Future[JobResult]: ...

    def bump_generation(self, sheet_id: str) -> Generation: ...

    def current_generation(self, sheet_id: str) -> Generation: ...

    def invalidate_sheet(self, sheet_id: str) -> None: ...

    def purge_older_generations(self, sheet_id: str, keep: Generation) -> None: ...


@runtime_checkable
class EngineAdapterProtocol(Protocol):
    """Compile logical query plans for execution."""

    def compile(self, plan: Any) -> PhysicalPlan: ...

    def validate_filter(self, clause: str) -> None: ...


@runtime_checkable
class MaterializerProtocol(Protocol):
    """Collect physical plans into table slices."""

    def collect(self, plan: PhysicalPlan) -> TableSlice: ...

    def collect_slice(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice: ...

    def collect_slice_stream(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
        batch_rows: int | None = None,
    ) -> Iterator[TableSlice]: ...

    def count(self, plan: PhysicalPlan) -> int | None: ...


def is_materializer_compatible(candidate: Any) -> bool:
    """Return ``True`` when ``candidate`` satisfies the materializer contract."""

    required = ("collect", "collect_slice", "count")
    for name in required:
        if not callable(getattr(candidate, name, None)):
            return False
    stream_attr = getattr(candidate, "collect_slice_stream", None)
    return stream_attr is None or callable(stream_attr)


__all__ = [
    "JobRunnerProtocol",
    "EngineAdapterProtocol",
    "MaterializerProtocol",
    "Materializer",
    "PhysicalPlan",
    "TableSlice",
    "is_materializer_compatible",
]

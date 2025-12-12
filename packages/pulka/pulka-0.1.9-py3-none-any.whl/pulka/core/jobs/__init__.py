"""Background job management for Pulka.

This module provides a job runner that executes background tasks in worker
threads. Jobs are keyed by logical ``JobTag`` values so callers can coalesce
duplicate work. Results are stored in a bounded in-memory cache that callers
poll from the UI thread without blocking the event loop.
"""

from __future__ import annotations

from collections import Counter, OrderedDict, defaultdict
from collections.abc import Callable
from concurrent.futures import Executor, Future, InvalidStateError
from dataclasses import dataclass, field
from heapq import heappop, heappush
from threading import RLock
from time import perf_counter_ns, time_ns
from typing import Any, cast

from ..errors import CancelledError

JobTag = str
JobKey = tuple[str, JobTag]
Generation = int

_CACHE_TTL_NS = int(120 * 1e9)
_CACHE_MAX_SIZE = 64


@dataclass(slots=True)
class JobRequest:
    sheet_id: str
    generation: Generation
    tag: JobTag
    fn: Callable[[Generation], Any]
    cache_result: bool = True
    priority: int = 0
    request_id: int = 0


@dataclass(slots=True)
class JobResult:
    sheet_id: str
    generation: Generation
    tag: JobTag
    value: Any
    error: Exception | None
    ts_ns: int
    duration_ns: int
    cacheable: bool


class _JobFuture(Future[JobResult]):
    """Future subclass aware of the job runner's cancellation semantics."""

    def __init__(
        self,
        runner: JobRunner,
        key: JobKey,
        request_id: int,
    ) -> None:
        super().__init__()
        self._runner = runner
        self._job_key = key
        self._request_id = request_id

    def cancel(self) -> bool:  # pragma: no cover - Future base not easily fuzzed
        if self.done():
            return False
        runner = self._runner
        key = self._job_key
        request_id = self._request_id
        return runner._cancel_client_future(key, request_id, self)

    def cancelled(self) -> bool:
        if super().cancelled():
            return True
        if not self.done():
            return False
        exc = super().exception()
        return isinstance(exc, CancelledError)


@dataclass(slots=True)
class _PendingJob:
    """Internal bookkeeping for coalesced jobs."""

    request: JobRequest
    waiters: list[tuple[int, Future[JobResult]]] = field(default_factory=list)
    running_request_id: int | None = None
    running_future: Future[JobResult] | None = None
    scheduled_request_id: int | None = None


@dataclass(order=True, slots=True)
class _ReadyJob:
    """Entry stored in the priority queue while waiting for worker capacity."""

    priority: int
    order: int
    key: JobKey
    request_id: int


class JobRunner:
    """Job runner with coalescing, caching, and tracing."""

    def __init__(
        self,
        *,
        executor: Executor | None = None,
        submit: Callable[[Callable[[], JobResult]], Future[JobResult]] | None = None,
        max_workers: int | None = None,
    ) -> None:
        self._lock = RLock()
        if submit is None:
            if executor is None:
                msg = "JobRunner requires either an executor or submit callback"
                raise ValueError(msg)
            submit = cast(
                Callable[[Callable[[], JobResult]], Future[JobResult]],
                executor.submit,
            )
        self._submit = submit
        self._executor = executor
        max_from_executor: int | None = None
        if max_workers is None and executor is not None:
            candidate = getattr(executor, "_max_workers", None)
            if isinstance(candidate, int):
                max_from_executor = candidate
        if isinstance(max_workers, int) and max_workers <= 0:
            max_workers = None
        if max_workers is None:
            max_workers = max_from_executor
        self._max_workers = max_workers
        self._running_jobs = 0
        self._ready_queue: list[_ReadyJob] = []
        self._ready_seq = 0
        self._pending: dict[JobKey, _PendingJob] = {}
        self._cache: OrderedDict[JobKey, JobResult] = OrderedDict()
        self._sheet_generation: dict[str, Generation] = {}
        self._request_seq: int = 0
        self._hit_counter: Counter[str] = Counter()
        self._miss_counter: Counter[str] = Counter()
        self._duration_stats: dict[str, list[int]] = defaultdict(lambda: [0, 0])

    # Cache interaction -------------------------------------------------

    def get(self, sheet_id: str, tag: JobTag) -> JobResult | None:
        """Return the cached result for ``(sheet_id, tag)`` when available."""

        key = (sheet_id, tag)
        with self._lock:
            self._evict_expired_locked(sheet_id=sheet_id)
            result = self._cache.get(key)
            if result is None:
                self._miss_counter[tag] += 1
                return None

            current_gen = self._sheet_generation.get(sheet_id, 0)
            if result.generation != current_gen or self._is_expired(result):
                self._cache.pop(key, None)
                self._miss_counter[tag] += 1
                return None

            self._cache.move_to_end(key)
            self._hit_counter[tag] += 1
            return result

    # Job submission ----------------------------------------------------

    def enqueue(self, req: JobRequest) -> Future[JobResult]:
        """Submit ``req`` for background execution and return the future."""

        key = (req.sheet_id, req.tag)
        with self._lock:
            req = self._prepare_request_locked(req)
            state = self._pending.get(key)
            client_future: Future[JobResult] = _JobFuture(self, key, req.request_id)
            if state is None:
                state = _PendingJob(request=req)
                state.waiters.append((req.request_id, client_future))
                self._pending[key] = state
                self._queue_ready_job_locked(key, state)
            else:
                state.request = req
                state.waiters.append((req.request_id, client_future))
                if state.running_request_id is None:
                    self._queue_ready_job_locked(key, state)
            return client_future

    def submit(
        self,
        sheet: Any,
        tag: JobTag,
        fn: Callable[[Generation], Any],
        *,
        cache_result: bool = True,
        priority: int = 0,
    ) -> Future[JobResult]:
        """Convenience wrapper to submit jobs bound to ``sheet`` metadata."""

        sheet_id = getattr(sheet, "sheet_id", None)
        if sheet_id is None:
            raise ValueError("sheet lacks sheet_id required for background jobs")

        job_context = getattr(sheet, "job_context", None)
        if callable(job_context):
            ctx_sheet_id, generation, _ = job_context()
        else:
            ctx_sheet_id = sheet_id
            generation = self.current_generation(sheet_id)

        request = JobRequest(
            sheet_id=ctx_sheet_id,
            generation=generation,
            tag=tag,
            fn=fn,
            cache_result=cache_result,
            priority=priority,
        )
        return self.enqueue(request)

    # Internal helpers --------------------------------------------------

    def _prepare_request_locked(self, req: JobRequest) -> JobRequest:
        self._request_seq += 1
        req.request_id = self._request_seq
        return req

    def _start_locked(self, key: JobKey, state: _PendingJob) -> None:
        request = state.request

        def _run(job_request: JobRequest = request) -> JobResult:
            start_ns = perf_counter_ns()
            try:
                value = job_request.fn(job_request.generation)
                error: Exception | None = None
            except Exception as exc:  # pragma: no cover - defensive guardrail
                value = None
                error = exc
            duration_ns = perf_counter_ns() - start_ns
            return JobResult(
                job_request.sheet_id,
                job_request.generation,
                job_request.tag,
                value,
                error,
                time_ns(),
                duration_ns,
                job_request.cache_result,
            )

        if self._max_workers is not None:
            self._running_jobs += 1

        try:
            future = self._submit(_run)
        except Exception:
            if self._max_workers is not None and self._running_jobs > 0:
                self._running_jobs -= 1
            raise

        state.running_request_id = request.request_id
        state.running_future = future

        def _done(
            fut: Future[JobResult],
            *,
            job_key: JobKey = key,
            rid: int = request.request_id,
        ) -> None:
            try:
                result = fut.result()
            except Exception:  # pragma: no cover - executor guarantees JobResult
                return
            self._on_job_finished(job_key, rid, result)

        future.add_done_callback(_done)

    def _cancel_client_future(
        self,
        key: JobKey,
        request_id: int,
        future: _JobFuture,
    ) -> bool:
        """Cancel a client future while keeping runner state consistent."""

        with self._lock:
            state = self._pending.get(key)
            if state is None:
                return False

            removed = False
            for waiter_id, waiter in list(state.waiters):
                if waiter_id == request_id and waiter is future:
                    state.waiters.remove((waiter_id, waiter))
                    removed = True
                    break

            if not removed:
                return False

            should_prune = not state.waiters and state.running_request_id is None

        try:
            future.set_exception(CancelledError("job cancelled by client"))
        except InvalidStateError:  # pragma: no cover - defensive
            return False

        if should_prune:
            with self._lock:
                state = self._pending.get(key)
                if state is not None and not state.waiters and state.running_request_id is None:
                    self._pending.pop(key, None)

        return True

    def _on_job_finished(self, key: JobKey, request_id: int, result: JobResult) -> None:
        tag = key[1]
        with self._lock:
            self._record_duration_locked(tag, result.duration_ns)
            if self._max_workers is not None and self._running_jobs > 0:
                self._running_jobs -= 1
            state = self._pending.get(key)
            if state is None:
                self._maybe_store_result_locked(key, result)
                self._dispatch_ready_jobs_locked()
                return

            if state.running_request_id != request_id:
                self._dispatch_ready_jobs_locked()
                return

            state.running_future = None
            state.running_request_id = None

            if state.request.request_id != request_id:
                self._cancel_waiters_locked(state, request_id)
                if state.waiters:
                    self._queue_ready_job_locked(key, state)
                else:
                    self._pending.pop(key, None)
                self._dispatch_ready_jobs_locked()
                return

            self._maybe_store_result_locked(key, result)

            for waiter_id, waiter in list(state.waiters):
                if waiter_id != request_id:
                    continue
                if result.error is not None:
                    waiter.set_exception(result.error)
                else:
                    waiter.set_result(result)
                state.waiters.remove((waiter_id, waiter))

            if state.waiters:
                self._queue_ready_job_locked(key, state)
            else:
                self._pending.pop(key, None)
            self._dispatch_ready_jobs_locked()

    def _cancel_waiters_locked(self, state: _PendingJob, request_id: int) -> None:
        for waiter_id, waiter in list(state.waiters):
            if waiter_id != request_id:
                continue
            if waiter.done():
                state.waiters.remove((waiter_id, waiter))
                continue
            try:
                waiter.set_exception(
                    CancelledError("job superseded by a newer request"),
                )
            except InvalidStateError:  # pragma: no cover - defensive
                waiter.cancel()
            state.waiters.remove((waiter_id, waiter))

    def _maybe_store_result_locked(self, key: JobKey, result: JobResult) -> None:
        if not result.cacheable:
            return
        sheet_id, _ = key
        current_gen = self._sheet_generation.get(sheet_id, 0)
        if current_gen != result.generation or self._is_expired(result):
            return
        self._cache[key] = result
        self._cache.move_to_end(key)
        self._evict_expired_locked()
        self._enforce_cache_size_locked()

    def _is_expired(self, result: JobResult) -> bool:
        return time_ns() - result.ts_ns > _CACHE_TTL_NS

    def _evict_expired_locked(self, *, sheet_id: str | None = None) -> None:
        keys_to_remove: list[JobKey] = []
        for key, value in list(self._cache.items()):
            if sheet_id is not None and key[0] != sheet_id:
                continue
            if value.generation != self._sheet_generation.get(key[0], 0) or self._is_expired(value):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self._cache.pop(key, None)

    def _enforce_cache_size_locked(self) -> None:
        while len(self._cache) > _CACHE_MAX_SIZE:
            self._cache.popitem(last=False)

    def _record_duration_locked(self, tag: JobTag, duration_ns: int) -> None:
        stats = self._duration_stats[tag]
        stats[0] += 1
        stats[1] += duration_ns

    # Sheet lifecycle ---------------------------------------------------

    def bump_generation(self, sheet_id: str) -> Generation:
        """Increment and return the active generation for ``sheet_id``."""

        with self._lock:
            current = self._sheet_generation.get(sheet_id, 0) + 1
            self._sheet_generation[sheet_id] = current
            self._evict_expired_locked(sheet_id=sheet_id)
            self._cancel_pending_locked(sheet_id)
            return current

    def current_generation(self, sheet_id: str) -> Generation:
        with self._lock:
            return self._sheet_generation.get(sheet_id, 0)

    def invalidate_sheet(self, sheet_id: str) -> None:
        """Cancel pending work and purge cache for ``sheet_id``."""

        with self._lock:
            self._cancel_pending_locked(sheet_id)

            cache_keys = [key for key in self._cache if key[0] == sheet_id]
            for key in cache_keys:
                self._cache.pop(key, None)

            self._sheet_generation.pop(sheet_id, None)

    def purge_older_generations(self, sheet_id: str, keep: Generation) -> None:
        """Drop cached results older than ``keep`` for ``sheet_id``."""

        with self._lock:
            stale_keys = [
                key
                for key, value in self._cache.items()
                if key[0] == sheet_id and value.generation < keep
            ]
            for key in stale_keys:
                self._cache.pop(key, None)

    def metrics(self) -> dict[str, Any]:
        """Return collected cache and execution metrics."""

        with self._lock:
            durations = {
                tag: {
                    "count": stats[0],
                    "total_ns": stats[1],
                    "avg_ns": stats[1] // stats[0] if stats[0] else 0,
                }
                for tag, stats in self._duration_stats.items()
            }
            return {
                "hits": dict(self._hit_counter),
                "misses": dict(self._miss_counter),
                "durations": durations,
                "cache_entries": len(self._cache),
                "ready_queue": len(self._ready_queue),
                "running": self._running_jobs,
            }

    def _cancel_pending_locked(self, sheet_id: str) -> None:
        keys = [key for key in self._pending if key[0] == sheet_id]
        for key in keys:
            state = self._pending.pop(key)
            for _, waiter in state.waiters:
                waiter.cancel()
            future = state.running_future
            if future is not None:
                future.cancel()
            state.scheduled_request_id = None

    # Ready queue helpers ----------------------------------------------

    def _queue_ready_job_locked(self, key: JobKey, state: _PendingJob) -> None:
        request = state.request
        request_id = request.request_id
        if state.running_request_id == request_id or state.scheduled_request_id == request_id:
            return
        state.scheduled_request_id = request_id
        priority = -int(request.priority or 0)
        self._ready_seq += 1
        heappush(self._ready_queue, _ReadyJob(priority, self._ready_seq, key, request_id))
        self._dispatch_ready_jobs_locked()

    def _dispatch_ready_jobs_locked(self) -> None:
        while self._ready_queue and self._can_start_more_locked():
            ready = heappop(self._ready_queue)
            state = self._pending.get(ready.key)
            if state is None or state.request.request_id != ready.request_id:
                continue
            state.scheduled_request_id = None
            self._start_locked(ready.key, state)

    def _can_start_more_locked(self) -> bool:
        if self._max_workers is None:
            return True
        return self._running_jobs < self._max_workers


__all__ = [
    "Generation",
    "JobRequest",
    "JobResult",
    "JobRunner",
    "JobKey",
    "JobTag",
]

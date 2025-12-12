from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock

from pulka.core.jobs import JobRunner


class _Sheet:
    def __init__(self, sheet_id: str) -> None:
        self.sheet_id = sheet_id

    def job_context(self) -> tuple[str, int, str]:
        return (self.sheet_id, 0, "ctx")


def test_job_runner_respects_priority_when_queueing() -> None:
    executor = ThreadPoolExecutor(max_workers=1)
    runner = JobRunner(executor=executor, max_workers=1)
    sheet = _Sheet("priority-sheet")

    slow_started = Event()
    slow_release = Event()

    def _slow_job(_: int) -> str:
        slow_started.set()
        slow_release.wait(timeout=1)
        return "slow"

    slow_future = runner.submit(sheet, "slow", _slow_job, priority=0)
    assert slow_started.wait(timeout=1)

    order: list[str] = []
    order_lock = Lock()

    def _queued(name: str):
        def _job(_: int) -> str:
            with order_lock:
                order.append(name)
            return name

        return _job

    low_future = runner.submit(sheet, "low", _queued("low"), priority=0)
    high_future = runner.submit(sheet, "high", _queued("high"), priority=1)

    slow_release.set()

    assert slow_future.result().value == "slow"
    assert high_future.result().value == "high"
    assert low_future.result().value == "low"
    assert order == ["high", "low"]

    executor.shutdown(wait=True)

"""Tests for the :write command helpers."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import Future
from pathlib import Path
from types import SimpleNamespace

from pulka.command.builtins import (
    _STATUS_MESSAGE_MAX_LENGTH,
    _make_write_completion_notifier,
    _normalise_status_message,
    _update_status,
    _WriteJobHandle,
    handle_write,
)


def test_write_completion_notifier_uses_call_soon_refresh() -> None:
    scheduled: list[Callable[[], None]] = []
    refreshed: list[bool] = []

    class DummyHooks:
        def call_soon(self, callback):
            scheduled.append(callback)

        def invalidate(self) -> None:  # pragma: no cover - unused path in this test
            refreshed.append(False)

    class DummyScreen:
        def __init__(self) -> None:
            self._viewer_ui_hooks = DummyHooks()

        def refresh(self, *, skip_metrics: bool = False) -> None:
            refreshed.append(skip_metrics)

    screen = DummyScreen()

    notifier = _make_write_completion_notifier(screen)

    assert notifier is not None

    notifier()

    assert len(scheduled) == 1

    scheduled[0]()

    assert refreshed == [True]


def test_write_job_handle_triggers_callback_once_and_sets_status() -> None:
    future: Future[Path] = Future()
    triggered: list[bool] = []

    handle = _WriteJobHandle(
        future,
        Path("export.parquet"),
        recorder=None,
        on_done=lambda: triggered.append(True),
    )

    viewer = SimpleNamespace(status_message=None)

    future.set_result(Path("export.parquet"))

    assert triggered == [True]

    assert handle.consume_update(viewer) is True

    assert viewer.status_message == "Export saved to: export.parquet"
    assert triggered == [True]


def test_handle_write_sets_progress_status_for_background_job() -> None:
    class DummySheet:
        plan = object()

        def with_plan(self, plan):  # pragma: no cover - defensive path unused
            return self

    class DummyRunner:
        def __init__(self) -> None:
            self.future: Future[Path] = Future()
            self.submissions: list[tuple[object, str, Callable[[int], Path]]] = []

        def submit(self, sheet, job_tag, job, *, cache_result: bool = True):
            self.submissions.append((sheet, job_tag, job))
            return self.future

    class DummyScreen:
        def __init__(self) -> None:
            self._jobs: dict[object, object] = {}

        def refresh(self, *, skip_metrics: bool = True) -> None:  # pragma: no cover - optional
            pass

    class DummyViewer:
        def __init__(self) -> None:
            self.sheet = DummySheet()
            self.status_message = None

        def __hash__(self) -> int:  # pragma: no cover - uses object identity
            return id(self)

    runner = DummyRunner()
    viewer = DummyViewer()
    session = SimpleNamespace(job_runner=runner)
    screen = DummyScreen()
    context = SimpleNamespace(viewer=viewer, session=session, screen=screen, recorder=None)

    handle_write(context, ["export.parquet"])

    assert viewer.status_message == "Export in progress..."


def test_update_status_truncates_and_records_long_messages() -> None:
    class DummyRecorder:
        enabled = True

        def __init__(self) -> None:
            self.messages: list[str] = []

        def record_status(self, message: str) -> None:
            self.messages.append(message)

    viewer = SimpleNamespace(status_message=None)
    recorder = DummyRecorder()

    message = (
        "write error: Failed to export data as 'xlsx': missing optional dependency xlsxwriter; "
        "install pulka[excel] to enable Excel exports"
    )

    _update_status(viewer, recorder, message)

    assert viewer.status_message == recorder.messages[0]
    assert len(viewer.status_message) <= _STATUS_MESSAGE_MAX_LENGTH
    assert viewer.status_message.endswith("…")


def test_normalise_status_message_collapses_whitespace() -> None:
    raw = "  write   error:   first line\nsecond line\tthird"

    normalised = _normalise_status_message(raw)

    assert "\n" not in normalised
    assert "\t" not in normalised
    assert "  " not in normalised

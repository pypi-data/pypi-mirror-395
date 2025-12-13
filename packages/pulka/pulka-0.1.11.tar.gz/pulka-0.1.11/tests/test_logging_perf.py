from __future__ import annotations

from pathlib import Path

import pytest

from pulka.api import Session
from pulka.logging import Recorder, RecorderConfig
from pulka.testing.data import make_df, write_df


@pytest.fixture
def sample_dataset(tmp_path: Path) -> str:
    df = make_df("mini_nav", rows=16, cols=4, seed=1234)
    dataset_path = tmp_path / "perf.parquet"
    write_df(df, dataset_path, "parquet")
    return str(dataset_path)


def _collect_perf_events(recorder: Recorder) -> list[dict[str, object]]:
    return [event.payload for event in recorder.iter_events() if event.type == "perf"]


def test_perf_timer_records_event(tmp_path: Path) -> None:
    config = RecorderConfig(
        enabled=True, output_dir=tmp_path, buffer_size=16, cell_redaction="none"
    )  # Don't redact for this test
    recorder = Recorder(config)

    with recorder.perf_timer("unit.test", payload={"context": "unit"}):
        pass

    perf_events = _collect_perf_events(recorder)
    assert perf_events, "Expected at least one perf event"
    payload = perf_events[-1]
    assert payload["phase"] == "unit.test"
    assert payload["context"] == "unit"
    assert payload["ok"] is True
    assert isinstance(payload["duration_ms"], float)


def test_headless_script_records_perf_events(sample_dataset: str, tmp_path: Path) -> None:
    config = RecorderConfig(
        enabled=True, output_dir=tmp_path, buffer_size=256, cell_redaction="none"
    )  # Don't redact for this test
    recorder = Recorder(config)
    session = Session(sample_dataset, viewport_rows=12, recorder=recorder)

    session.run_script(["down"], auto_render=True)

    perf_events = _collect_perf_events(recorder)
    assert perf_events, "Recorder should capture perf events during headless run"

    phases = {payload["phase"] for payload in perf_events}
    assert "render.table" in phases
    assert "render.status" in phases

    headless_events = [payload for payload in perf_events if payload.get("context") == "headless"]
    assert headless_events, "Expected headless perf events"

    command_events = [payload for payload in headless_events if payload.get("command")]
    assert any(payload["command"] == "down" for payload in command_events)

    durations = [payload["duration_ms"] for payload in perf_events]
    assert all(isinstance(value, float) and value >= 0 for value in durations)

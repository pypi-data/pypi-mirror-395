from pathlib import Path

import pytest

from pulka.api.runtime import Runtime
from pulka.api.session import Session
from pulka.command.registry import REGISTRY, CommandRegistry
from pulka.command.runtime import SessionCommandRuntime
from pulka.logging import Recorder, RecorderConfig
from pulka.sheets.file_browser_sheet import FileBrowserSheet
from pulka.testing.data import make_df, write_df
from pulka.tui.screen import Screen


@pytest.fixture
def sample_dataset(tmp_path):
    df = make_df("mini_nav", rows=8, cols=3, seed=123)
    path = tmp_path / "runtime.parquet"
    write_df(df, path, "parquet")
    return str(path)


def _make_recorder(tmp_path, name: str) -> Recorder:
    config = RecorderConfig(
        enabled=True,
        output_dir=tmp_path / name,
        buffer_size=128,
        cell_redaction="none",
    )
    return Recorder(config)


def _command_events(recorder: Recorder) -> list[dict[str, object]]:
    return [event.payload for event in recorder.iter_events() if event.type == "command"]


def _session_without_entrypoints(path: str, *, recorder: Recorder | None = None) -> Session:
    runtime = Runtime(load_entry_points=False)
    return runtime.open(path, viewport_rows=6, recorder=recorder)


def test_session_exposes_command_runtime(sample_dataset):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime
    assert isinstance(runtime, SessionCommandRuntime)

    viewer = runtime.prepare_viewer(session.viewer)
    assert viewer is session.viewer

    result = runtime.invoke("down", source="test", context_mutator=lambda ctx: None)
    assert result.dispatch is not None
    assert result.dispatch.spec.name == "down"
    assert result.render.should_render is True


def test_runtime_rejects_repeat_for_non_repeatable_command(sample_dataset):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime

    result = runtime.invoke("schema", repeat=2, source="test", context_mutator=lambda ctx: None)
    assert result.dispatch is None
    assert result.message is not None
    assert "does not support repeat" in result.message


def test_runtime_dispatch_raw_reports_unknown_command(sample_dataset):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime

    result = runtime.dispatch_raw("not-a-command", source="test")

    assert result.dispatch is None
    assert result.render.should_render is False
    assert result.message is not None
    assert "Unknown command" in result.message


def test_runtime_restores_previous_registry_binding(sample_dataset):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime

    sentinel_registry = CommandRegistry(load_builtin_commands=False)
    REGISTRY.bind(sentinel_registry)
    try:
        runtime.invoke("down", source="test", context_mutator=lambda ctx: None)
        assert REGISTRY._current() is sentinel_registry
    finally:
        REGISTRY.bind(None)


def test_prepare_viewer_installs_recorder_callbacks(sample_dataset, tmp_path, monkeypatch):
    recorder = _make_recorder(tmp_path, "runtime-perf")
    session = _session_without_entrypoints(sample_dataset, recorder=recorder)
    runtime = session.command_runtime

    captured: list[object] = []

    def _capture(callback):
        captured.append(callback)

    monkeypatch.setattr(session.viewer, "set_perf_callback", _capture)
    runtime.prepare_viewer(session.viewer)

    assert captured and callable(captured[-1])

    recorder.disable()
    runtime.prepare_viewer(session.viewer)

    assert captured[-1] is None


def test_runtime_records_command_events_for_headless_and_tui(sample_dataset, tmp_path):
    headless_recorder = _make_recorder(tmp_path, "headless-rec")
    session_headless = _session_without_entrypoints(sample_dataset, recorder=headless_recorder)
    session_headless.run_script(["down"], auto_render=False)
    headless_events = _command_events(headless_recorder)
    assert any(
        event.get("source") == "headless" and event.get("name") == "down"
        for event in headless_events
    )

    tui_recorder = _make_recorder(tmp_path, "tui-rec")
    session_tui = _session_without_entrypoints(sample_dataset, recorder=tui_recorder)
    screen = Screen(session_tui.viewer, recorder=tui_recorder)
    screen._execute_command("down")
    tui_events = _command_events(tui_recorder)
    assert any(event.get("source") == "tui" and event.get("name") == "down" for event in tui_events)

    unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
    if unsubscribe is not None:
        unsubscribe()


def test_browse_command_defaults_to_dataset_parent(sample_dataset):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime

    result = runtime.invoke("browse", source="test")

    assert result.dispatch is not None
    assert result.dispatch.spec.name == "browse"
    sheet = session.viewer.sheet
    assert isinstance(sheet, FileBrowserSheet)
    assert sheet.directory == Path(sample_dataset).parent
    assert session.dataset_path is None


def test_browse_command_accepts_explicit_directory(sample_dataset, tmp_path):
    session = _session_without_entrypoints(sample_dataset)
    runtime = session.command_runtime
    explicit_dir = tmp_path / "nested"
    explicit_dir.mkdir()

    runtime.invoke("browse", args=[str(explicit_dir)], source="test")

    sheet = session.viewer.sheet
    assert isinstance(sheet, FileBrowserSheet)
    assert sheet.directory == explicit_dir


def test_browse_command_requires_directory_when_unavailable():
    df = make_df("mini_nav", rows=2, cols=2, seed=5).lazy()
    session = Session(None, lazyframe=df)
    runtime = session.command_runtime

    runtime.invoke("browse", source="test")

    assert not isinstance(session.viewer.sheet, FileBrowserSheet)
    assert session.viewer.status_message == (
        "browse requires a directory path or file-backed dataset"
    )

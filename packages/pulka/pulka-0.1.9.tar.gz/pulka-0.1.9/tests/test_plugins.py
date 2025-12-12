from __future__ import annotations

import sys
import types
from importlib import metadata

import polars as pl
import pytest

from pulka.api.runtime import Runtime
from pulka.command.registry import CommandContext, CommandRegistry
from pulka.data.scanners import ScannerRegistry
from pulka.plugin.manager import PluginManager
from pulka.sheets.registry import SheetRegistry


class DummyEntryPoints(list):
    """Helper object that mimics ``entry_points().select``."""

    def select(self, *, group: str) -> DummyEntryPoints:
        if group == "pulka.plugins":
            return DummyEntryPoints(self)
        return DummyEntryPoints()


@pytest.fixture()
def registries() -> tuple[CommandRegistry, SheetRegistry, ScannerRegistry]:
    commands = CommandRegistry(load_builtin_commands=False)
    sheets = SheetRegistry()
    scanners = ScannerRegistry()
    return commands, sheets, scanners


def _install_module(monkeypatch: pytest.MonkeyPatch, name: str, register_fn) -> None:
    module = types.ModuleType(name)
    module.register = register_fn
    monkeypatch.setitem(sys.modules, name, module)


def _write_sample_dataset(tmp_path) -> str:
    df = pl.DataFrame({"fruit": ["apple", "banana", "apple"], "size": [1, 2, 3]})
    path = tmp_path / "sample.parquet"
    df.write_parquet(path)
    return str(path)


def test_plugin_manager_loads_modules_and_entry_points(monkeypatch: pytest.MonkeyPatch, registries):
    calls: list[str] = []

    def register_entry(*, commands=None, sheets=None, scanners=None):
        calls.append("entry")
        if commands is not None:
            commands.register("entry-cmd", lambda ctx, args: None, "entry")

    def register_module(*, commands=None, sheets=None, scanners=None):
        calls.append("module")
        if sheets is not None:

            class DummySheet:
                def __init__(self, base, *_args, **_kwargs):
                    self._base = base
                    self.columns = list(getattr(base, "columns", []))

                def fetch_slice(self, row_start, row_count, columns):
                    return self._base.fetch_slice(row_start, row_count, columns)

                def get_value_at(self, row_index, column_name=None):
                    return self._base.get_value_at(row_index, column_name)

            sheets.register_sheet("dummy", DummySheet)

    _install_module(monkeypatch, "tests.fake_entry", register_entry)
    _install_module(monkeypatch, "tests.fake_module", register_module)

    entry_point = metadata.EntryPoint(
        name="ep-plugin", value="tests.fake_entry:register", group="pulka.plugins"
    )
    monkeypatch.setattr(metadata, "entry_points", lambda: DummyEntryPoints([entry_point]))

    commands, sheets, scanners = registries
    manager = PluginManager(modules=["tests.fake_module"])

    loaded = manager.load(commands=commands, sheets=sheets, scanners=scanners)

    assert loaded == ["ep-plugin", "tests.fake_module"]
    assert calls == ["entry", "module"]
    assert commands.get_command("entry-cmd") is not None
    assert "dummy" in sheets.list_kinds()


def test_plugin_manager_handles_import_error(monkeypatch: pytest.MonkeyPatch, registries, caplog):
    caplog.set_level("ERROR", logger="pulka.plugin.manager")

    entry_point = metadata.EntryPoint(
        name="broken", value="missing.module:register", group="pulka.plugins"
    )
    monkeypatch.setattr(metadata, "entry_points", lambda: DummyEntryPoints([entry_point]))

    def register_module(*, commands=None, sheets=None, scanners=None):
        if commands is not None:
            commands.register("ok", lambda ctx, args: None)

    _install_module(monkeypatch, "tests.ok_module", register_module)

    commands, sheets, scanners = registries
    manager = PluginManager(modules=["tests.ok_module"])

    loaded = manager.load(commands=commands, sheets=sheets, scanners=scanners)

    assert loaded == ["tests.ok_module"]
    assert any("broken" in record.getMessage() for record in caplog.records)


def test_plugin_manager_duplicate_registration_errors(
    monkeypatch: pytest.MonkeyPatch, registries, caplog
):
    caplog.set_level("ERROR", logger="pulka.plugin.manager")

    def register_one(*, commands=None, sheets=None, scanners=None):
        if commands is not None:
            commands.register("dup", lambda ctx, args: None)

    def register_two(*, commands=None, sheets=None, scanners=None):
        if commands is not None:
            commands.register("dup", lambda ctx, args: None)

    _install_module(monkeypatch, "tests.first_plugin", register_one)
    _install_module(monkeypatch, "tests.second_plugin", register_two)

    commands, sheets, scanners = registries
    manager = PluginManager(modules=["tests.first_plugin", "tests.second_plugin"])

    loaded = manager.load(
        commands=commands,
        sheets=sheets,
        scanners=scanners,
        include_entry_points=False,
    )

    assert loaded == ["tests.first_plugin"]
    assert "Command 'dup' already provided by tests.first_plugin" in caplog.text


def test_builtin_plugins_available_by_default(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.delenv("PULKA_NO_ENTRYPOINTS", raising=False)
    monkeypatch.delenv("PULKA_CONFIG", raising=False)

    path = _write_sample_dataset(tmp_path)
    runtime = Runtime()
    session = runtime.open(path, viewport_rows=10, viewport_cols=6)

    assert {"pulka-summary", "pulka-freq", "pulka-transpose"} <= set(session.loaded_plugins)

    context = CommandContext(
        session.viewer.sheet,
        session.viewer,
        session=session,
        view_stack=session.view_stack,
    )
    session.commands.execute("summary", context, [])
    assert session.viewer.status_message == "summary view"
    assert session.viewer.sheet.__class__.__name__ == "SummarySheet"
    assert session.viewer.frozen_column_count == 2
    assert session.viewer.frozen_columns[:2] == ["column", "dtype"]
    assert session.view_stack.active is session.viewer

    session.open(path)
    assert session.view_stack.active is session.viewer
    context = CommandContext(
        session.viewer.sheet,
        session.viewer,
        session=session,
        view_stack=session.view_stack,
    )
    session.commands.execute("freq", context, ["fruit"])
    assert session.viewer.sheet.__class__.__name__ == "FreqSheet"
    assert session.viewer.is_freq_view is True
    assert session.viewer.stack_depth == 1
    assert len(session.view_stack.viewers) == 2
    assert session.view_stack.active is session.viewer

    session.open(path)
    assert len(session.view_stack.viewers) == 1
    assert session.view_stack.active is session.viewer
    context = CommandContext(
        session.viewer.sheet,
        session.viewer,
        session=session,
        view_stack=session.view_stack,
    )
    session.commands.execute("transpose", context, [])
    assert session.viewer.sheet.__class__.__name__ == "TransposeSheet"
    assert session.viewer.stack_depth == 1
    assert session.viewer.frozen_column_count == 2
    assert session.viewer.frozen_columns[:2] == ["column", "dtype"]
    assert len(session.view_stack.viewers) == 2
    assert session.view_stack.active is session.viewer


def test_open_sheet_view_reports_missing_runner_keyword(tmp_path):
    path = _write_sample_dataset(tmp_path)

    class LegacySheet:
        def __init__(self, base_sheet):
            self._base = base_sheet
            self.columns = list(getattr(base_sheet, "columns", []))
            self.schema = getattr(base_sheet, "schema", {})

        def fetch_slice(self, row_start, row_count, columns):
            return self._base.fetch_slice(row_start, row_count, columns)

        def get_value_at(self, row_index, column_name=None):
            return self._base.get_value_at(row_index, column_name)

    runtime = Runtime()
    runtime.sheets.register_sheet("legacy", LegacySheet)
    session = runtime.open(path, viewport_rows=6)

    with pytest.raises(TypeError) as excinfo:
        session.open_sheet_view("legacy", base_viewer=session.viewer)

    message = str(excinfo.value)
    assert "runner" in message
    assert "legacy" in message


def test_builtin_plugins_load_via_explicit_modules(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.setenv("PULKA_NO_ENTRYPOINTS", "1")
    monkeypatch.delenv("PULKA_CONFIG", raising=False)

    modules = [
        "pulka_builtin_plugins.summary.plugin",
        "pulka_builtin_plugins.freq.plugin",
        "pulka_builtin_plugins.transpose.plugin",
    ]

    path = _write_sample_dataset(tmp_path)
    runtime = Runtime(plugins=modules, load_entry_points=False)
    session = runtime.open(path, viewport_rows=10, viewport_cols=6)

    assert session.loaded_plugins == sorted(modules)

    context = CommandContext(
        session.viewer.sheet,
        session.viewer,
        session=session,
        view_stack=session.view_stack,
    )
    session.commands.execute("summary", context, [])
    assert session.viewer.sheet.__class__.__name__ == "SummarySheet"


def test_builtin_plugin_can_be_disabled_via_config(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.delenv("PULKA_NO_ENTRYPOINTS", raising=False)

    config = tmp_path / "pulka.toml"
    config.write_text('[plugins]\ndisable = ["pulka-summary"]\n', encoding="utf-8")
    monkeypatch.setenv("PULKA_CONFIG", str(config))

    path = _write_sample_dataset(tmp_path)
    runtime = Runtime()
    session = runtime.open(path, viewport_rows=10, viewport_cols=6)

    assert "pulka-summary" not in session.loaded_plugins
    assert session.commands.get_command("summary") is None
    assert session.commands.get_command("freq") is not None
    assert session.commands.get_command("transpose") is not None


def test_runtime_exposes_plugin_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.setenv("PULKA_NO_ENTRYPOINTS", "1")
    monkeypatch.delenv("PULKA_CONFIG", raising=False)

    modules = [
        "pulka_builtin_plugins.summary.plugin",
        "pulka_builtin_plugins.freq.plugin",
    ]

    runtime = Runtime(plugins=modules, load_entry_points=False)

    assert runtime.loaded_plugins == sorted(modules)
    assert runtime.disabled_plugins == []
    assert runtime.plugin_failures == []

    class DummyRecorder:
        def __init__(self) -> None:
            self.enabled = True
            self.calls: list[dict] = []

        def record_session_start(self, **payload):
            self.calls.append(payload)

    recorder = DummyRecorder()
    runtime.bootstrap_recorder(recorder)

    assert recorder.calls
    payload = recorder.calls[0]
    assert payload["plugins"] == runtime.recorder_bootstrap.plugins
    assert payload["disabled"] == runtime.recorder_bootstrap.disabled


def test_session_surfaces_plugin_failures(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.setenv("PULKA_NO_ENTRYPOINTS", "1")
    monkeypatch.delenv("PULKA_CONFIG", raising=False)

    def register_fail(**_registries):
        raise RuntimeError("boom")

    _install_module(monkeypatch, "tests.fail_plugin", register_fail)

    path = _write_sample_dataset(tmp_path)
    runtime = Runtime(plugins=["tests.fail_plugin"], load_entry_points=False)
    session = runtime.open(path, viewport_rows=10, viewport_cols=6)

    assert "tests.fail_plugin" not in session.loaded_plugins
    assert session.plugin_failures
    assert session.viewer.status_message == "Plugin tests.fail_plugin failed to load; see logs"


def test_run_script_mode_uses_updated_session_viewer(tmp_path, monkeypatch):
    monkeypatch.setenv("PULKA_TEST", "1")
    monkeypatch.delenv("PULKA_NO_ENTRYPOINTS", raising=False)
    monkeypatch.delenv("PULKA_CONFIG", raising=False)

    path = _write_sample_dataset(tmp_path)
    runtime = Runtime()
    session = runtime.open(path, viewport_rows=10, viewport_cols=6)

    outputs = session.run_script(["freq fruit", "render"], auto_render=False)

    assert session.viewer.is_freq_view is True
    assert session.viewer.stack_depth == 1
    assert "count" in session.viewer.columns
    assert outputs and "count" in outputs[-1]

"""Tests for the shared command parser and dispatcher."""

from __future__ import annotations

from types import SimpleNamespace

import polars as pl
import pytest

from pulka.api.runtime import Runtime
from pulka.command.parser import CommandDispatcher, CommandDispatchResult, CommandParser
from pulka.command.registry import CommandContext, CommandRegistry
from pulka.command.spec import CommandSpec
from pulka.core.viewer import ViewStack
from pulka.headless.runner import apply_script_command
from pulka.tui.screen import Screen


def _make_context() -> CommandContext:
    viewer = SimpleNamespace(set_ui_hooks=lambda hooks: None)
    sheet = SimpleNamespace()
    stack = ViewStack()
    stack.push(viewer)
    return CommandContext(sheet, viewer, view_stack=stack)


def test_parser_resolves_alias_and_repeat() -> None:
    registry = CommandRegistry(load_builtin_commands=False)
    calls: list[int] = []

    def _handler(ctx: CommandContext, args: list[str]) -> None:
        calls.append(1)

    registry.register(
        "move",
        _handler,
        "Stub move",
        0,
        aliases=("m",),
        repeatable=True,
    )

    parser = CommandParser(registry)

    invocation = parser.parse("m 5")
    assert invocation is not None
    assert invocation.spec.name == "move"
    assert invocation.repeat == 5
    assert invocation.args == ()

    invocation_leading = parser.parse("3 move")
    assert invocation_leading is not None
    assert invocation_leading.repeat == 3

    dispatcher = CommandDispatcher(registry)
    dispatcher.dispatch("move 2", _make_context())
    dispatcher.dispatch("2 m", _make_context())
    assert len(calls) == 4


def test_parser_honours_plugin_spec_metadata() -> None:
    registry = CommandRegistry(load_builtin_commands=False)

    def _handler(ctx: CommandContext, args: list[str]) -> None:  # pragma: no cover - stub
        ctx.viewer.last_args = args

    plugin_spec = CommandSpec(
        name="plugin-cmd",
        handler=_handler,
        description="Plugin provided command",
        argument_mode="single",
        aliases=("pc",),
    )
    registry.register_spec(plugin_spec)

    parser = CommandParser(registry)
    invocation = parser.parse("pc hello")
    assert invocation is not None
    assert invocation.spec.name == "plugin-cmd"
    assert invocation.args == ("hello",)
    assert invocation.repeat == 1

    with pytest.raises(ValueError):
        parser.parse("pc")


def test_headless_and_tui_use_shared_specs(monkeypatch, tmp_path) -> None:
    data_path = tmp_path / "tiny.parquet"
    pl.DataFrame({"a": [1, 2, 3]}).write_parquet(data_path)

    call_log: list[str] = []

    def _probe(ctx: CommandContext, args: list[str]) -> None:
        call_log.append(ctx.viewer.__class__.__name__)

    # Headless execution captures dispatcher output.
    runtime_headless = Runtime(load_entry_points=False)
    session_headless = runtime_headless.open(str(data_path))
    session_headless.commands.register(
        "probe",
        _probe,
        "Probe command",
        0,
        aliases=("pp",),
        repeatable=True,
    )

    captured_headless: list[CommandDispatchResult | None] = []
    original_dispatch = CommandDispatcher.dispatch

    def _recording_dispatch(self, raw, context):
        result = original_dispatch(self, raw, context)
        captured_headless.append(result)
        return result

    monkeypatch.setattr(CommandDispatcher, "dispatch", _recording_dispatch)

    cont, runtime_result = apply_script_command(session_headless, "pp 2")
    assert cont is True

    assert captured_headless and captured_headless[0] is not None
    headless_result = captured_headless[0]
    assert headless_result.spec.name == "probe"
    assert headless_result.repeat == 2
    assert runtime_result.dispatch == headless_result

    # Restore dispatch and exercise the TUI path via Screen._execute_command.
    monkeypatch.setattr(CommandDispatcher, "dispatch", original_dispatch)

    runtime_tui = Runtime(load_entry_points=False)
    session_tui = runtime_tui.open(str(data_path))
    session_tui.commands.register(
        "probe",
        _probe,
        "Probe command",
        0,
        aliases=("pp",),
        repeatable=True,
    )

    screen = Screen(session_tui.viewer)
    tui_result = screen._execute_command("probe", repeat=3)

    assert tui_result is not None
    assert tui_result.spec.name == "probe"
    assert tui_result.repeat == 3
    assert tui_result.spec == headless_result.spec
    assert len(call_log) == 5

"""Shared command parsing and dispatch helpers."""

from __future__ import annotations

import re
import shlex
from collections.abc import Sequence
from dataclasses import dataclass

from .registry import CommandContext, CommandRegistry
from .spec import CommandSpec


@dataclass(frozen=True, slots=True)
class CommandInvocation:
    """Structured representation of a parsed command."""

    spec: CommandSpec
    args: tuple[str, ...]
    repeat: int
    raw: str


@dataclass(frozen=True, slots=True)
class CommandDispatchResult:
    """Metadata describing a dispatched command."""

    spec: CommandSpec
    args: tuple[str, ...]
    repeat: int
    raw: str


class CommandParser:
    """Parse raw text into :class:`CommandInvocation` objects."""

    def __init__(self, registry: CommandRegistry):
        self._registry = registry

    def parse(self, raw: str) -> CommandInvocation | None:
        text = raw.strip()
        if not text or text.startswith("#"):
            return None

        repeat, remainder = self._extract_leading_repeat(text)
        name, arg_str = self._split_command(remainder)
        spec = self._registry.get_spec(name)
        if spec is None:
            raise ValueError(f"Unknown command: {name}")

        args, repeat = self._parse_arguments(spec, arg_str, repeat)
        return CommandInvocation(spec=spec, args=tuple(args), repeat=repeat, raw=text)

    @staticmethod
    def _extract_leading_repeat(command: str) -> tuple[int, str]:
        match = re.match(r"^(\d+)\s+(.*)$", command)
        if match:
            count = max(1, int(match.group(1)))
            return count, match.group(2).strip()
        return 1, command

    @staticmethod
    def _split_command(command: str) -> tuple[str, str]:
        if not command:
            return "", ""
        if " " in command or "\t" in command:
            name, remainder = command.split(None, 1)
            return name, remainder.strip()
        if ":" in command:
            name, remainder = command.split(":", 1)
            return name.strip(), remainder.strip()
        return command, ""

    def _parse_arguments(
        self, spec: CommandSpec, arg_str: str, repeat: int
    ) -> tuple[list[str], int]:
        if spec.argument_mode == "none":
            if arg_str:
                if spec.repeatable:
                    try:
                        repeat = max(1, int(arg_str))
                    except ValueError as exc:  # pragma: no cover - defensive guard
                        msg = f"Command {spec.name} does not accept arguments"
                        raise ValueError(msg) from exc
                else:
                    raise ValueError(f"Command {spec.name} does not accept arguments")
            return [], repeat

        if spec.argument_mode == "single":
            if not arg_str:
                raise ValueError(f"Command {spec.name} requires an argument")
            return [arg_str], repeat

        if not arg_str:
            return [], repeat

        try:
            parts = shlex.split(arg_str)
        except ValueError as exc:  # pragma: no cover - invalid quoting
            raise ValueError(
                f"Unable to parse arguments for {spec.name}: {exc}"  # noqa: TRY003
            ) from exc
        return parts, repeat


class CommandDispatcher:
    """Execute parsed commands against a :class:`CommandRegistry`."""

    def __init__(self, registry: CommandRegistry):
        self._registry = registry
        self._parser = CommandParser(registry)

    def parse(self, raw: str) -> CommandInvocation | None:
        return self._parser.parse(raw)

    def dispatch(self, raw: str, context: CommandContext) -> CommandDispatchResult | None:
        invocation = self._parser.parse(raw)
        if invocation is None:
            return None
        self._run(invocation, context)
        return CommandDispatchResult(
            spec=invocation.spec,
            args=invocation.args,
            repeat=invocation.repeat,
            raw=invocation.raw,
        )

    def invoke(
        self,
        name: str,
        context: CommandContext,
        *,
        args: Sequence[str] | None = None,
        repeat: int = 1,
    ) -> CommandDispatchResult:
        spec = self._registry.get_spec(name)
        if spec is None:
            raise ValueError(f"Unknown command: {name}")

        arg_list = list(args or [])
        spec.validate_arguments(arg_list)
        repeat_count = max(1, repeat)
        if repeat_count > 1 and not spec.repeatable:
            raise ValueError(f"Command {spec.name} does not support repeat counts")

        invocation = CommandInvocation(
            spec=spec,
            args=tuple(arg_list),
            repeat=repeat_count,
            raw=name,
        )
        self._run(invocation, context)
        return CommandDispatchResult(
            spec=spec,
            args=invocation.args,
            repeat=invocation.repeat,
            raw=invocation.raw,
        )

    def _run(self, invocation: CommandInvocation, context: CommandContext) -> None:
        spec = invocation.spec
        if invocation.repeat > 1 and not spec.repeatable:
            raise ValueError(f"Command {spec.name} does not support repeat counts")
        spec.validate_arguments(invocation.args)
        for _ in range(invocation.repeat):
            spec.handler(context, list(invocation.args))

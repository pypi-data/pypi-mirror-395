"""Command metadata structures used across Pulka runtimes."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from .registry import CommandContext


ArgumentMode = Literal["none", "single", "variadic"]


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Declarative command metadata shared by the dispatcher and UI."""

    name: str
    handler: Callable[[CommandContext, list[str]], None]
    description: str = ""
    argument_mode: ArgumentMode = "none"
    repeatable: bool = False
    aliases: tuple[str, ...] = ()
    provider: str = "core"
    ui_hints: Mapping[str, Any] | None = None

    def expects_arguments(self) -> bool:
        return self.argument_mode != "none"

    def validate_arguments(self, args: Sequence[str]) -> None:
        if self.argument_mode == "none":
            if args:
                raise ValueError(f"Command {self.name} does not accept arguments")
            return
        if self.argument_mode == "single":
            if len(args) != 1:
                raise ValueError(
                    f"Command {self.name} expects exactly one argument, got {len(args)}"
                )
            return
        # Variadic mode accepts any argument count.

    def with_aliases(self, aliases: Sequence[str]) -> CommandSpec:
        if not aliases:
            return self
        unique = tuple(dict.fromkeys(aliases))
        return replace(self, aliases=unique)

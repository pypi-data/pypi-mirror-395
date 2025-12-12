"""
Command registry for Pulka.

This module defines the registry that maps command names to handlers and provides
a command context for executing commands.
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import replace
from typing import Any

from ..core.sheet import Sheet
from ..core.viewer import Viewer
from .spec import ArgumentMode, CommandSpec


class CommandContext:
    """Context passed to command handlers containing session state."""

    def __init__(
        self,
        sheet: Sheet,
        viewer: Viewer,
        session: Any = None,
        *,
        view_stack: Any | None = None,
        recorder: Any | None = None,
    ):
        self.sheet = sheet
        self.viewer = viewer
        self.session = session  # Optional session reference
        self.view_stack = view_stack
        self.recorder = recorder


class CommandRegistry:
    """Registry for commands that can be executed in both TUI and headless modes."""

    def __init__(self, *, load_builtin_commands: bool = True):
        self._specs: dict[str, CommandSpec] = {}
        self._aliases: dict[str, str] = {}  # alias -> canonical name
        self._alias_providers: dict[str, str] = {}
        self._sheet_openers: dict[str, Callable[..., None]] = {}
        self._provider_stack: list[str] = ["core"]

        if load_builtin_commands:
            self.load_builtins()

    @contextmanager
    def provider_scope(self, provider: str):
        """Temporarily attribute registrations to ``provider``."""

        self._provider_stack.append(provider)
        try:
            yield
        finally:
            self._provider_stack.pop()

    def _current_provider(self) -> str:
        if not self._provider_stack:
            return "unknown"
        return self._provider_stack[-1]

    @staticmethod
    def _mode_from_arg_count(arg_count: int) -> ArgumentMode:
        if arg_count < 0:
            return "variadic"
        if arg_count == 0:
            return "none"
        if arg_count == 1:
            return "single"
        return "variadic"

    def _store_spec(self, spec: CommandSpec) -> None:
        self._specs[spec.name] = spec
        for alias in spec.aliases:
            self.register_alias(alias, spec.name, provider=spec.provider)

    def register_spec(self, spec: CommandSpec, *, provider: str | None = None) -> None:
        owner = provider or spec.provider or self._current_provider()
        canonical = spec if spec.provider == owner else replace(spec, provider=owner)
        if canonical.name in self._specs:
            existing = self._specs[canonical.name]
            msg = (
                f"Command '{canonical.name}' already provided by {existing.provider}; "
                f"{owner} attempted to register a duplicate"
            )
            raise ValueError(msg)
        if canonical.name in self._aliases:
            alias_owner = self._alias_providers.get(canonical.name, "unknown")
            msg = (
                f"Command '{canonical.name}' already registered as an alias by {alias_owner}; "
                f"{owner} attempted to register it as a command"
            )
            raise ValueError(msg)
        self._store_spec(canonical)

    def register(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        arg_count: int = 0,
        *,
        provider: str | None = None,
        aliases: Iterable[str] | None = None,
        argument_mode: ArgumentMode | None = None,
        repeatable: bool | None = None,
        ui_hints: Mapping[str, Any] | None = None,
    ):
        """Register a command handler."""
        owner = provider or self._current_provider()
        if name in self._specs:
            existing = self._specs[name]
            msg = (
                f"Command '{name}' already provided by {existing.provider}; "
                f"{owner} attempted to register a duplicate"
            )
            raise ValueError(msg)
        if name in self._aliases:
            alias_owner = self._alias_providers.get(name, "unknown")
            msg = (
                f"Command '{name}' already registered as an alias by {alias_owner}; "
                f"{owner} attempted to register it as a command"
            )
            raise ValueError(msg)
        mode = argument_mode or self._mode_from_arg_count(arg_count)
        spec = CommandSpec(
            name=name,
            handler=handler,
            description=description,
            argument_mode=mode,
            repeatable=bool(repeatable),
            aliases=tuple(aliases or ()),
            provider=owner,
            ui_hints=ui_hints,
        )
        self._store_spec(spec)

    def load_builtins(self) -> None:
        """Initialize built-in commands."""
        # Import here to avoid circular imports
        from .builtins import register_builtin_commands

        with self.provider_scope("builtin"):
            register_builtin_commands(self)

    def register_alias(
        self,
        alias: str,
        canonical_name: str,
        *,
        provider: str | None = None,
    ):
        """Register an alias for a command."""
        owner = provider or self._current_provider()
        if alias in self._specs:
            existing = self._specs[alias]
            msg = (
                f"Alias '{alias}' conflicts with command provided by {existing.provider}; "
                f"{owner} attempted to register it as an alias for '{canonical_name}'"
            )
            raise ValueError(msg)
        if alias in self._aliases:
            previous_owner = self._alias_providers.get(alias, "unknown")
            existing_target = self._aliases[alias]
            msg = (
                f"Alias '{alias}' already maps to '{existing_target}' from {previous_owner}; "
                f"{owner} attempted to remap it"
            )
            raise ValueError(msg)
        if canonical_name not in self._specs:
            raise ValueError(
                f"Cannot register alias '{alias}' for unknown command '{canonical_name}'"
            )
        self._aliases[alias] = canonical_name
        self._alias_providers[alias] = owner
        spec = self._specs[canonical_name]
        if alias not in spec.aliases:
            updated_aliases = (*spec.aliases, alias)
            self._specs[canonical_name] = replace(
                spec, aliases=tuple(dict.fromkeys(updated_aliases))
            )

    def register_sheet_opener(self, name: str, opener: Callable[..., None]) -> None:
        """Register a helper to open a sheet by name.

        Plugins can use this to expose helpers that switch the active sheet via
        commands without having to duplicate the lookup logic.
        """

        self._sheet_openers[name] = opener

    def remove_provider(self, provider: str) -> None:
        """Remove commands and aliases registered by ``provider``."""

        commands_to_remove = [
            name for name, spec in self._specs.items() if spec.provider == provider
        ]
        for name in commands_to_remove:
            self._specs.pop(name, None)

        aliases_to_remove = [
            alias for alias, owner in self._alias_providers.items() if owner == provider
        ]
        for alias in aliases_to_remove:
            canonical = self._aliases.pop(alias, None)
            self._alias_providers.pop(alias, None)
            if canonical and canonical in self._specs:
                spec = self._specs[canonical]
                if alias in spec.aliases:
                    filtered = tuple(a for a in spec.aliases if a != alias)
                    self._specs[canonical] = replace(spec, aliases=filtered)

    def execute(self, command_name: str, context: CommandContext, args: list[str]) -> bool:
        """Execute a command by name."""
        # Check if it's an alias
        spec = self.get_spec(command_name)
        if spec is None:
            hint = self._missing_command_hint(command_name, context)
            message = hint or f"Unknown command: {command_name}"
            raise ValueError(message)

        spec.validate_arguments(args)

        # Execute the command
        spec.handler(context, list(args))
        return True

    def get_command(self, name: str) -> CommandSpec | None:
        """Get a command definition by name."""
        return self.get_spec(name)

    def get_spec(self, name: str) -> CommandSpec | None:
        actual_name = self._aliases.get(name, name)
        return self._specs.get(actual_name)

    def iter_specs(self) -> Iterator[CommandSpec]:
        return iter(self._specs.values())

    def _missing_command_hint(self, requested: str, context: CommandContext | None) -> str | None:
        session = getattr(context, "session", None)
        if session is None:
            return None

        plugin_hint = self._plugin_hint_for(requested, session)
        if plugin_hint:
            return plugin_hint

        disabled = getattr(session, "disabled_plugins", None) or []
        failures = getattr(session, "plugin_failures", None) or []
        details: list[str] = []
        if disabled:
            details.append("disabled plugins: " + ", ".join(sorted(disabled)))
        if failures:
            failed_names = sorted(name for name, _ in failures)
            details.append("failed plugins: " + ", ".join(failed_names))
        if details:
            return f"Unknown command: {requested} ({'; '.join(details)})"
        return None

    def _plugin_hint_for(self, requested: str, session: Any) -> str | None:
        name = requested.lower()

        def _match_plugin(plugin_name: str) -> bool:
            candidate = plugin_name.lower()
            if candidate.endswith(f"-{name}"):
                return True
            tail = candidate.rsplit(".", 1)[-1]
            return tail == name

        disabled = getattr(session, "disabled_plugins", None) or []
        for plugin_name in disabled:
            if _match_plugin(plugin_name):
                return f"{requested} not available; plugin {plugin_name} disabled"

        failures = getattr(session, "plugin_failures", None) or []
        for plugin_name, _ in failures:
            if _match_plugin(plugin_name):
                return f"{requested} not available; plugin {plugin_name} failed to load"

        return None

    def list_commands(self) -> list[tuple[str, str]]:
        """List all available commands with their descriptions."""
        commands = []
        for name, spec in self._specs.items():
            commands.append((name, spec.description))
        return commands


class _RegistryProxy:
    """Compatibility adapter for legacy global registry usage."""

    def __init__(self) -> None:
        self._thread_local = threading.local()
        self._fallback = CommandRegistry()

    def bind(self, registry: CommandRegistry | None) -> None:
        """Bind a registry for the current thread."""

        if registry is None:
            if hasattr(self._thread_local, "registry"):
                delattr(self._thread_local, "registry")
        else:
            self._thread_local.registry = registry

    def _current(self) -> CommandRegistry:
        return getattr(self._thread_local, "registry", self._fallback)

    def execute(self, command_name: str, context: CommandContext, args: list[str]) -> bool:
        registry = getattr(self._thread_local, "registry", None)
        if registry is None:
            msg = (
                "REGISTRY.execute is deprecated; bind a session registry via "
                "REGISTRY.bind(session.commands) before use"
            )
            raise RuntimeError(msg)
        return registry.execute(command_name, context, args)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._current(), name)


# Global registry instance
# DEPRECATED: use Session.commands
# TODO: remove in a future release once external callers migrate.
REGISTRY = _RegistryProxy()

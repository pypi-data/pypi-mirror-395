"""Common plugin interfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from ..command.registry import CommandRegistry
    from ..data.scanners import ScannerRegistry
    from ..sheets.registry import SheetRegistry


class PluginError(Exception):
    """Raised when a plugin fails to register correctly."""


class CommandProvider(Protocol):
    """Protocol for objects that expose commands."""

    def register_commands(self, registry: CommandRegistry) -> None:  # pragma: no cover - Protocol
        ...


class SheetProvider(Protocol):
    """Protocol for objects that expose sheets."""

    def register_sheets(self, sheets: SheetRegistry) -> None:  # pragma: no cover - Protocol
        ...


class ScannerProvider(Protocol):
    """Protocol for objects that expose data scanners."""

    def register_scanners(self, scanners: ScannerRegistry) -> None:  # pragma: no cover - Protocol
        ...

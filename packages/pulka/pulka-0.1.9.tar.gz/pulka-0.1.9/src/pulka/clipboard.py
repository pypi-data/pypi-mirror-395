"""Clipboard helpers for Pulka.

This module provides a small extensible abstraction for copying text to the
system clipboard. The default implementation prioritises the Windows clipboard
bridge available inside WSL (`clip.exe`) but exposes a backend protocol so other
platform specific integrations (macOS `pbcopy`, Linux utilities, etc.) can be
added without touching call sites. The :func:`copy_to_clipboard` helper iterates
through registered backends until one succeeds, keeping the implementation easy
to extend.
"""

from __future__ import annotations

import os
import platform
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol


class ClipboardBackend(Protocol):
    """Protocol implemented by clipboard backends."""

    name: str

    def is_supported(self) -> bool:
        """Return ``True`` when the backend is viable on the current system."""

    def copy(self, text: str) -> bool:
        """Attempt to copy ``text`` to the clipboard, returning success state."""


@dataclass(frozen=True, slots=True)
class _CommandClipboardBackend:
    """Run a shell command to forward text into the system clipboard."""

    name: str
    command: tuple[str, ...]
    predicate: Callable[[], bool] | None = None

    def is_supported(self) -> bool:  # pragma: no cover - trivial
        if self.predicate is None:
            return True
        return bool(self.predicate())

    def copy(self, text: str) -> bool:
        try:
            subprocess.run(self.command, input=text, text=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            return False
        return True


def _is_windows() -> bool:
    return os.name == "nt"


def _is_wsl() -> bool:
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    release = platform.release().lower()
    return "microsoft" in release or "wsl" in release


def _is_macos() -> bool:
    return platform.system().lower() == "darwin"


def _supports_clip_exe() -> bool:
    return _is_windows() or _is_wsl()


_DEFAULT_BACKENDS: tuple[ClipboardBackend, ...] = (
    _CommandClipboardBackend("clip.exe", ("clip.exe",), predicate=_supports_clip_exe),
    _CommandClipboardBackend("clip", ("clip",), predicate=_is_windows),
    _CommandClipboardBackend("pbcopy", ("pbcopy",), predicate=_is_macos),
)


def copy_to_clipboard(text: str, *, backends: Sequence[ClipboardBackend] | None = None) -> bool:
    """Copy ``text`` to the clipboard using the first working backend.

    Args:
        text: The text payload to copy. Non-string input is coerced using ``str``.
        backends: Optional explicit backend list. When omitted, the module's
            default backends are used.

    Returns:
        ``True`` when a backend reported success, ``False`` otherwise.
    """

    payload = text if isinstance(text, str) else str(text)
    candidates = backends or _DEFAULT_BACKENDS

    for backend in candidates:
        try:
            if not backend.is_supported():
                continue
        except Exception:
            continue

        try:
            if backend.copy(payload):
                return True
        except Exception:
            continue

    return False

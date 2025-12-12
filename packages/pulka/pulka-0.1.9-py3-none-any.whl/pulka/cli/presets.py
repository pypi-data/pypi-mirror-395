"""User-editable presets for ``pulka generate``."""

from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

try:  # pragma: no cover - Python 3.11+ exposes tomllib
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for very old interpreters
    import tomli as tomllib  # type: ignore[no-redef]

PRESET_ENV_VAR = "PULKA_GENERATE_PRESET_FILE"
DEFAULT_PRESET_FILENAME = "generate_presets.toml"


class PresetConfigError(RuntimeError):
    """Raised when preset configuration cannot be parsed."""


@dataclass(frozen=True, slots=True)
class PresetStore:
    """Represents the active preset file and its entries."""

    path: Path
    presets: Mapping[str, str]
    builtin_presets: Mapping[str, str]

    def get(self, name: str) -> str | None:
        """Return the preset spec for ``name`` when it exists."""

        return self.presets.get(name)

    def __bool__(self) -> bool:
        return bool(self.presets)


def load_preset_store(path: Path | None = None) -> PresetStore:
    """Load presets from the configured file.

    Resolution order:

    1. ``PULKA_GENERATE_PRESET_FILE`` environment variable.
    2. Provided ``path`` argument.
    3. Platform-specific config directory (XDG/AppData) + ``generate_presets.toml``.
    """

    builtin_presets = _load_builtin_presets()
    resolved_path = _resolve_preset_path(path)
    if not resolved_path.exists():
        return PresetStore(
            path=resolved_path,
            presets=builtin_presets,
            builtin_presets=builtin_presets,
        )

    try:
        raw = resolved_path.read_text()
    except OSError as exc:  # pragma: no cover - IO errors are rare
        msg = f"Failed to read preset file {resolved_path}: {exc}"
        raise PresetConfigError(msg) from exc

    user_presets = _parse_preset_table(raw, source=str(resolved_path))
    combined = dict(builtin_presets)
    combined.update(user_presets)
    return PresetStore(path=resolved_path, presets=combined, builtin_presets=builtin_presets)


def _load_builtin_presets() -> dict[str, str]:
    default_path = resources.files("pulka.cli").joinpath("default_generate_presets.toml")
    raw = default_path.read_text()
    return _parse_preset_table(raw, source="built-in presets")


def _parse_preset_table(raw_text: str, *, source: str) -> dict[str, str]:
    try:
        data = tomllib.loads(raw_text)
    except tomllib.TOMLDecodeError as exc:  # pragma: no cover - invalid defaults caught in CI
        msg = f"Failed to parse presets from {source}: {exc}"
        raise PresetConfigError(msg) from exc

    raw_presets = data.get("presets", {})
    if raw_presets and not isinstance(raw_presets, Mapping):
        msg = f"Expected [presets] table in {source}"
        raise PresetConfigError(msg)

    parsed: dict[str, str] = {}
    for key, value in raw_presets.items():
        if not isinstance(key, str):
            continue
        if not isinstance(value, str):
            msg = f"Preset '{key}' in {source} must be a string"
            raise PresetConfigError(msg)
        stripped = value.strip()
        if stripped:
            parsed[key] = stripped
    return parsed


def _resolve_preset_path(path: Path | None) -> Path:
    env_override = os.environ.get(PRESET_ENV_VAR)
    if env_override:
        return Path(env_override).expanduser()
    if path is not None:
        return path.expanduser()
    base_dir = _default_config_dir()
    return (base_dir / DEFAULT_PRESET_FILENAME).expanduser()


def _default_config_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "Pulka"
        return Path.home() / "AppData" / "Roaming" / "Pulka"
    xdg_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_home:
        return Path(xdg_home) / "pulka"
    return Path.home() / ".config" / "pulka"


__all__ = [
    "DEFAULT_PRESET_FILENAME",
    "PRESET_ENV_VAR",
    "PresetConfigError",
    "PresetStore",
    "load_preset_store",
]

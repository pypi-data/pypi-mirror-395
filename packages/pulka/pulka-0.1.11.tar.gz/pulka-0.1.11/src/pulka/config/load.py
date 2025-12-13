"""Load Pulka configuration from ``pulka.toml`` files."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_CONFIG_FILENAMES = ("pulka.toml",)
_CONFIG_ENV_VARS = ("PULKA_CONFIG", "PD_CONFIG")


@dataclass(frozen=True)
class PluginsConfig:
    """User-configurable plugin settings."""

    modules: list[str] = field(default_factory=list)
    disable: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class JobsConfig:
    """Job runner configuration exposed to :class:`pulka.api.runtime.Runtime`."""

    max_workers: int | None = None


@dataclass(frozen=True)
class UserConfig:
    """Full user configuration for a session."""

    plugins: PluginsConfig = PluginsConfig()
    jobs: JobsConfig = JobsConfig()


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for env_var in _CONFIG_ENV_VARS:
        env = os.environ.get(env_var)
        if env:
            paths.append(Path(env).expanduser())
    cwd = Path.cwd()
    for name in _CONFIG_FILENAMES:
        paths.append(cwd / name)
    home = Path.home()
    for directory in (home / ".config" / "pulka", home / ".config" / "picodata"):
        for name in _CONFIG_FILENAMES:
            paths.append(directory / name)
    return paths


def _ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, (list, tuple, set)):
        result: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    return []


def _parse_plugins(section: Any) -> PluginsConfig:
    if not isinstance(section, dict):
        return PluginsConfig()
    modules = _ensure_list(section.get("modules"))
    disable = _ensure_list(section.get("disable"))
    return PluginsConfig(modules=modules, disable=disable)


def _parse_jobs(section: Any) -> JobsConfig:
    if not isinstance(section, dict):
        return JobsConfig()
    max_workers = section.get("max_workers")
    if max_workers is None:
        return JobsConfig()
    try:
        parsed = int(max_workers)
    except (TypeError, ValueError):
        return JobsConfig()
    if parsed <= 0:
        return JobsConfig()
    return JobsConfig(max_workers=parsed)


def load_user_config() -> UserConfig:
    """Load ``pulka.toml`` configuration from the usual locations."""

    for path in _candidate_paths():
        if not path.exists():
            continue
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        plugins_section: Any
        if "plugins" in data and isinstance(data["plugins"], dict):
            plugins_section = data["plugins"]
        else:
            plugins_section = {key: data[key] for key in ("modules", "disable") if key in data}
        plugins = _parse_plugins(plugins_section)
        jobs = _parse_jobs(data.get("jobs"))
        return UserConfig(plugins=plugins, jobs=jobs)

    return UserConfig()


__all__ = ["PluginsConfig", "JobsConfig", "UserConfig", "load_user_config"]

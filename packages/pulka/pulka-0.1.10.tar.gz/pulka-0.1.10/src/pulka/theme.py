from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .utils import lazy_imports

Style = lazy_imports.prompt_toolkit_style_class()

_CONFIG_FILENAMES = (
    "pulka-theme.toml",
    "pulka_theme.toml",
    "picodata-theme.toml",
    "picodata_theme.toml",
)
_THEME_ENV_VARS = ("PULKA_THEME_PATH", "PD_THEME_PATH")

_THEME_EPOCH = 0


def resolve_header_style(value: str | None) -> str | None:
    """Normalize header foregrounds so plain "white" renders as bright white."""

    from .render.style_resolver import normalize_header_color

    return normalize_header_color(value)


@dataclass(frozen=True)
class ThemeConfig:
    border_style: str | None
    table_style: str | None
    header_style: str | None
    header_active_style: str | None
    cell_style: str | None
    cell_null_style: str | None
    cell_active_style: str | None
    row_active_style: str | None
    row_selected_style: str | None
    row_selected_active_style: str | None
    status_style: str | None
    dialog_style: str | None

    def prompt_toolkit_style(self) -> Style:
        from .render.style_resolver import StyleResolver

        resolver = StyleResolver.from_theme(self)
        mapping = resolver.prompt_toolkit_rules()
        return Style.from_dict(mapping) if mapping else Style([])


DEFAULTS: dict[str, str] = {
    "border_style": "#505050",
    "table_style": "default",
    "header_style": "white",
    "header_active_style": "#f06595 bold",
    "cell_style": "#b8b8b8",
    "cell_null_style": "#707070",
    "cell_active_style": "black on #f06595",
    "row_active_style": "on #70465c",
    "row_selected_style": "#63e6be bold",
    "row_selected_active_style": "black on #63e6be",
    "status_style": "white on #3a3a3a",
    "dialog_style": "default",
}


def _normalize(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"default", "none", "null"}:
        return None
    return text


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for env_var in _THEME_ENV_VARS:
        env = os.environ.get(env_var)
        if env:
            paths.append(Path(env).expanduser())
    cwd = Path.cwd()
    for name in _CONFIG_FILENAMES:
        paths.append(cwd / name)
    home = Path.home()
    for config_dir in (home / ".config" / "pulka", home / ".config" / "picodata"):
        for name in _CONFIG_FILENAMES:
            paths.append(config_dir / name)
    return paths


def load_theme_document() -> tuple[dict[str, Any], Path | None]:
    """Return the raw parsed theme document and the path it originated from."""

    for path in _candidate_paths():
        if not path.exists():
            continue
        try:
            data = tomllib.loads(path.read_text())
        except Exception:
            continue
        if isinstance(data, dict):
            return data, path
    return {}, None


def _load_overrides() -> dict[str, str]:
    document, _ = load_theme_document()
    section: dict[str, Any] | None = None
    if document:
        maybe_section = document.get("theme") if isinstance(document, dict) else None
        if isinstance(maybe_section, dict):
            section = maybe_section
        elif isinstance(document, dict):
            section = document
    if not section:
        return {}
    return {
        key: str(value) for key, value in section.items() if key in DEFAULTS and value is not None
    }


def load_theme() -> ThemeConfig:
    merged = DEFAULTS.copy()
    overrides = _load_overrides()
    merged.update(overrides)
    normalized = {key: _normalize(value) for key, value in merged.items()}
    return ThemeConfig(**normalized)


def _apply_theme(config: ThemeConfig) -> None:
    global THEME, APP_STYLE, _THEME_EPOCH

    THEME = config
    APP_STYLE = THEME.prompt_toolkit_style()
    _THEME_EPOCH += 1


def theme_epoch() -> int:
    """Return the current theme epoch counter."""

    return _THEME_EPOCH


def reload_theme() -> None:
    """Reload theme configuration from disk and bump the epoch."""

    _apply_theme(load_theme())


def set_theme(config: ThemeConfig) -> None:
    """Apply ``config`` as the active theme and bump the epoch."""

    _apply_theme(config)


_apply_theme(load_theme())

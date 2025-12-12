"""Predefined colour palettes for quick theme switching."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any

from . import theme


@dataclass(frozen=True)
class ThemePalette:
    """Describe a set of theme overrides for highlight colours."""

    key: str
    label: str
    description: str
    overrides: Mapping[str, str | None]


_BASE_THEME = theme.THEME

_DEFAULT_PALETTE_DATA: dict[str, dict[str, Any]] = {
    "0": {
        "label": "Configured",
        "description": "Use the configured theme as-is",
    },
    "1": {
        "label": "Amber Focus",
        "description": "Warm amber accent with bold text highlights",
        "header_active_style": "#f6bd60 bold",
        "cell_active_style": "black on #f6bd60",
        "row_active_style": "on #70465c",
    },
    "2": {
        "label": "Lagoon",
        "description": "Cool cyan accents with bold column focus",
        "header_active_style": "#56cfe1 bold",
        "cell_active_style": "black on #56cfe1",
        "row_active_style": "on #70465c",
    },
    "3": {
        "label": "Orchid",
        "description": "Soft magenta highlights with bold emphasis",
        "header_active_style": "#f06595 bold",
        "cell_active_style": "black on #f06595",
        "row_active_style": "on #70465c",
    },
    "4": {
        "label": "Fresh Mint",
        "description": "Mint green accents for active selections",
        "header_active_style": "#80ed99 bold",
        "cell_active_style": "black on #80ed99",
        "row_active_style": "on #70465c",
    },
}


def _normalize_override(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "default"}:
        return None
    return text


def _palette_sort_order(keys: Iterable[str]) -> list[str]:
    def _key(value: str) -> tuple[int, int | None, str]:
        try:
            numeric = int(value)
        except ValueError:
            return (1, None, value)
        return (0, numeric, value)

    return sorted(keys, key=_key)


def _build_palettes() -> tuple[ThemePalette, ...]:
    config_data: dict[str, dict[str, Any]] = {
        key: dict(value) for key, value in _DEFAULT_PALETTE_DATA.items()
    }

    document, _ = theme.load_theme_document()
    if isinstance(document, dict):
        raw_palettes = document.get("palettes")
        if isinstance(raw_palettes, dict):
            for key, value in raw_palettes.items():
                if isinstance(value, dict):
                    config_data[key] = dict(value)

    base_default = _DEFAULT_PALETTE_DATA["0"]
    base_config = config_data.get("0", {})
    base_label = str(base_config.get("label", base_default.get("label", "Configured")))
    base_description = str(base_config.get("description", base_default.get("description", "")))

    palettes: list[ThemePalette] = [
        ThemePalette(
            key="0",
            label=base_label,
            description=base_description,
            overrides=MappingProxyType({}),
        )
    ]

    for key in _palette_sort_order(k for k in config_data if k != "0"):
        data = config_data[key]
        defaults = _DEFAULT_PALETTE_DATA.get(key, {"label": f"Palette {key}", "description": ""})
        label = str(data.get("label", defaults.get("label", f"Palette {key}")))
        description = str(data.get("description", defaults.get("description", "")))
        overrides = {
            field: _normalize_override(value)
            for field, value in data.items()
            if field not in {"label", "description"}
        }
        palettes.append(
            ThemePalette(
                key=key,
                label=label,
                description=description,
                overrides=MappingProxyType(dict(overrides)),
            )
        )

    return tuple(palettes)


_PALETTES = _build_palettes()

_PALETTE_INDEX = {palette.key: palette for palette in _PALETTES}


def list_palettes() -> Sequence[ThemePalette]:
    """Return the available palettes including the configured base theme."""

    return _PALETTES


def _normalise_identifier(identifier: str | int) -> str:
    text = str(identifier).strip()
    if not text:
        raise ValueError("palette identifier cannot be empty")
    return text


def get_palette(identifier: str | int) -> ThemePalette:
    """Return the palette referenced by ``identifier``."""

    key = _normalise_identifier(identifier)
    palette = _PALETTE_INDEX.get(key)
    if palette is None:
        raise ValueError(f"unknown palette '{identifier}'")
    return palette


def apply_palette(identifier: str | int) -> ThemePalette:
    """Apply ``identifier`` and return the resolved palette."""

    palette = get_palette(identifier)
    overrides = palette.overrides
    config = _BASE_THEME if not overrides else replace(_BASE_THEME, **overrides)
    theme.set_theme(config)
    return palette

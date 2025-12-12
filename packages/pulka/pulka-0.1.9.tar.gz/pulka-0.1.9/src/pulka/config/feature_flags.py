"""Feature flag helpers for Pulka runtime configuration."""

from __future__ import annotations

import os

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def _parse_bool_env(value: str | None) -> bool | None:
    """Normalise common truthy/falsey environment strings."""

    if value is None:
        return None
    text = value.strip().lower()
    if not text:
        return None
    if text in _TRUE_VALUES:
        return True
    if text in _FALSE_VALUES:
        return False
    try:
        return bool(int(text))
    except ValueError:
        return None


def use_prompt_toolkit_table() -> bool:
    """Return whether the prompt_toolkit-native table control should be used."""

    for key in ("PULKA_PTK_TABLE", "PD_PTK_TABLE"):
        override = _parse_bool_env(os.environ.get(key))
        if override is not None:
            return override
    # Default on; environment can disable when necessary.
    return True


__all__ = ["use_prompt_toolkit_table"]

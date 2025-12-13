"""Shared utilities for Pulka."""

from __future__ import annotations

import os

__all__ = ["_get_int_env"]


def _get_int_env(primary: str, legacy: str | None, default: int) -> int:
    """Return an integer environment variable with optional legacy fallback."""

    keys = [primary]
    if legacy:
        keys.append(legacy)
    for key in keys:
        value = os.environ.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except ValueError:
            continue
    return default

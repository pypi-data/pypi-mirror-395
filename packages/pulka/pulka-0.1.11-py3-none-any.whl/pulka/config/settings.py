"""Runtime settings and environment-aware defaults for streaming and caches."""

from __future__ import annotations

import os
from dataclasses import dataclass

from ..utils import _get_int_env

_BOOL_TRUE = {"1", "true", "yes", "on", "enabled"}
_BOOL_FALSE = {"0", "false", "no", "off", "disabled"}


def _get_bool_env(primary: str, legacy: str | None, default: bool) -> bool:
    """Return a boolean environment variable with optional legacy fallback."""

    keys = [primary]
    if legacy:
        keys.append(legacy)
    for key in keys:
        value = os.environ.get(key)
        if value is None:
            continue
        lowered = value.strip().lower()
        if lowered in _BOOL_TRUE:
            return True
        if lowered in _BOOL_FALSE:
            return False
    return default


@dataclass(frozen=True, slots=True)
class StreamingSettings:
    """Defaults that control row streaming behaviour."""

    enabled: bool
    batch_rows: int


@dataclass(frozen=True, slots=True)
class CacheBudgets:
    """Default cache budgets for row providers and viewers."""

    row_provider_max_cells: int
    row_provider_max_entries: int
    viewer_row_cache_max_cells: int


STREAMING_DEFAULTS = StreamingSettings(
    enabled=_get_bool_env("PULKA_STREAMING_ENABLED", "PD_STREAMING_ENABLED", True),
    batch_rows=max(1, _get_int_env("PULKA_STREAMING_BATCH_ROWS", "PD_STREAMING_BATCH_ROWS", 8192)),
)
"""Global streaming defaults resolved from the environment."""

CACHE_DEFAULTS = CacheBudgets(
    row_provider_max_cells=max(
        0,
        _get_int_env("PULKA_ROW_PROVIDER_MAX_CELLS", "PD_ROW_PROVIDER_MAX_CELLS", 1_000_000),
    ),
    row_provider_max_entries=max(
        1,
        _get_int_env("PULKA_ROW_PROVIDER_MAX_ENTRIES", "PD_ROW_PROVIDER_MAX_ENTRIES", 32),
    ),
    viewer_row_cache_max_cells=max(
        0,
        _get_int_env("PULKA_ROW_CACHE_MAX_CELLS", "PD_ROW_CACHE_MAX_CELLS", 256_000),
    ),
)
"""Cache budgets resolved from the environment."""


__all__ = [
    "StreamingSettings",
    "CacheBudgets",
    "STREAMING_DEFAULTS",
    "CACHE_DEFAULTS",
]

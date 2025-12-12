"""Cache helpers for status-line fragments."""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from dataclasses import dataclass
from time import monotonic
from typing import Any

from ..testing import is_test_mode
from .status_bar import render_status_line, sample_memory_usage


@dataclass(frozen=True, slots=True)
class CachedStatus:
    """Return payload for cached status-line fragments."""

    fragments: Sequence[tuple[str, str]]
    resource_sample: int | None
    recomputed: bool


class StatusLineCache:
    """Cache prompt_toolkit fragments for the status line."""

    def __init__(self, viewer: Any, *, resource_refresh_seconds: float = 5.0) -> None:
        self._viewer = viewer
        self._resource_refresh_seconds = resource_refresh_seconds
        self._cached: CachedStatus | None = None
        self._resource_sample: int | None = None
        self._resource_sample_at: float = 0.0

    def get_status(self) -> CachedStatus:
        """Return cached status fragments, recomputing if required."""

        should_recompute = self._cached is None
        if hasattr(self._viewer, "is_status_dirty"):
            try:
                should_recompute = should_recompute or bool(self._viewer.is_status_dirty())
            except Exception:  # pragma: no cover - defensive
                should_recompute = True
        else:
            should_recompute = True

        refresh_resource = self._should_refresh_resource()
        if not should_recompute and not refresh_resource and self._cached is not None:
            return CachedStatus(
                fragments=self._cached.fragments,
                resource_sample=self._cached.resource_sample,
                recomputed=False,
            )

        if refresh_resource or self._resource_sample is None:
            self._resource_sample = sample_memory_usage(test_mode=is_test_mode())
            self._resource_sample_at = monotonic()

        fragments = render_status_line(
            self._viewer,
            resource_sample=self._resource_sample,
        )

        if hasattr(self._viewer, "acknowledge_status_rendered"):
            with contextlib.suppress(Exception):
                self._viewer.acknowledge_status_rendered()

        cached = CachedStatus(
            fragments=fragments,
            resource_sample=self._resource_sample,
            recomputed=True,
        )
        self._cached = cached
        return cached

    def _should_refresh_resource(self) -> bool:
        if self._resource_refresh_seconds <= 0:
            return True
        if self._resource_sample_at == 0.0:
            return True
        delta = monotonic() - self._resource_sample_at
        return delta >= self._resource_refresh_seconds


__all__ = ["CachedStatus", "StatusLineCache"]

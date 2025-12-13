"""Extensible registry for dataset scanners."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path

import polars as pl

from ..core.engine.contracts import PhysicalPlan
from ..core.engine.polars_adapter import coerce_physical_plan
from .scan import is_supported_path, scan_any

Scanner = Callable[[Path], PhysicalPlan | pl.LazyFrame]


class ScannerRegistry:
    """Map file extensions or MIME types to scanner callables."""

    def __init__(self) -> None:
        self._scanners: dict[str, Scanner] = {}
        self._providers: dict[str, str] = {}
        self._provider_stack: list[str] = ["core"]

    @contextmanager
    def provider_scope(self, provider: str):
        """Attribute registrations within the scope to ``provider``."""

        self._provider_stack.append(provider)
        try:
            yield
        finally:
            self._provider_stack.pop()

    def _current_provider(self) -> str:
        if not self._provider_stack:
            return "unknown"
        return self._provider_stack[-1]

    def register_scanner(self, key: str, fn: Scanner) -> None:
        """Register a scanner for ``key``.

        ``key`` can be a file extension (``.csv``) or a MIME type
        (``text/csv``). Re-registering a key raises ``ValueError``.
        """

        normalized = key.lower()
        owner = self._current_provider()
        if normalized in self._scanners:
            existing = self._providers[normalized]
            msg = (
                f"Scanner already registered for '{key}' by {existing}; "
                f"{owner} attempted to register a duplicate"
            )
            raise ValueError(msg)

        self._scanners[normalized] = fn
        self._providers[normalized] = owner

    def scan(self, path: Path) -> PhysicalPlan:
        """Return a ``PhysicalPlan`` for ``path`` using a registered scanner."""

        scanner = self._resolve_scanner(path)
        if scanner is not None:
            return self._ensure_physical_plan(scanner(path))

        return self._ensure_physical_plan(scan_any(str(path)))

    def _resolve_scanner(self, path: Path) -> Scanner | None:
        suffixes = [suffix.lower() for suffix in path.suffixes]
        for suffix in reversed(suffixes):
            if suffix in self._scanners:
                return self._scanners[suffix]
            bare = suffix.lstrip(".")
            if bare and bare in self._scanners:
                return self._scanners[bare]

        mime = path.suffix.lower().lstrip(".")
        if mime:
            mime_key = f"mime:{mime}"
            if mime_key in self._scanners:
                return self._scanners[mime_key]

        return None

    def can_scan(self, path: Path) -> bool:
        """Return ``True`` when ``path`` is likely supported."""

        if self._resolve_scanner(path) is not None:
            return True
        return is_supported_path(str(path))

    def list_scanners(self) -> dict[str, Scanner]:
        """Return registered scanners."""

        return dict(self._scanners)

    @staticmethod
    def _ensure_physical_plan(candidate: PhysicalPlan | pl.LazyFrame) -> PhysicalPlan:
        plan = coerce_physical_plan(candidate)
        if plan is not None:
            return plan
        msg = (
            "Scanner returned unsupported plan type: "
            f"{type(candidate).__name__ if candidate is not None else 'None'}"
        )
        raise TypeError(msg)

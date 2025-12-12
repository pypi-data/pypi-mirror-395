"""Typed exception hierarchy for Pulka's core execution pipeline."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class PulkaCoreError(Exception):
    """Base class for errors surfaced by the core planning pipeline."""

    def __init__(
        self, message: str | None = None, *, context: Mapping[str, Any] | None = None
    ) -> None:
        detail = (message or self.__class__.__name__).strip()
        self.message = detail
        self.context = dict(context or {})
        super().__init__(detail)


class PlanError(PulkaCoreError):
    """Raised when a logical plan is invalid or cannot be satisfied."""


class CompileError(PulkaCoreError):
    """Raised when compilation of a logical plan into a physical one fails."""


class MaterializeError(PulkaCoreError):
    """Raised when a physical plan cannot be materialised into tabular data."""


class CancelledError(PulkaCoreError):
    """Raised when an in-flight job is cancelled before completion."""


__all__ = [
    "CancelledError",
    "CompileError",
    "MaterializeError",
    "PlanError",
    "PulkaCoreError",
]

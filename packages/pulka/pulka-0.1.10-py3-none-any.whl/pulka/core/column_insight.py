"""Dataclasses and helpers for column insight sidecar."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .formatting import _one_line_repr

# Numeric columns with this many or fewer distinct values are treated as categorical
LOW_CARDINALITY_NUMERIC_LIMIT = 5

_PREVIEW_MAX_CHARS = 160
_BINARY_PREVIEW_BYTES = 32


def _format_bytes_preview(value: bytes | bytearray) -> tuple[str, bool]:
    sample = bytes(value[:_BINARY_PREVIEW_BYTES])
    hex_repr = sample.hex()
    truncated = len(value) > _BINARY_PREVIEW_BYTES
    prefix = "0x"
    suffix = "…" if truncated else ""
    return f"{prefix}{hex_repr}{suffix}", truncated


def summarize_value_preview(value: Any, *, max_chars: int = _PREVIEW_MAX_CHARS) -> tuple[str, bool]:
    """Return a compact preview string for ``value`` and whether it was truncated."""

    if isinstance(value, (bytes, bytearray)):
        return _format_bytes_preview(value)
    try:
        preview = _one_line_repr(value, max_items=12, max_chars=max_chars)
    except Exception:  # pragma: no cover - defensive guard
        preview = str(value)
    truncated = len(preview) >= max_chars - 1 if max_chars > 0 else False
    return preview, truncated


@dataclass(frozen=True, slots=True)
class TopValue:
    """Value frequency summary for the insight sidecar."""

    value: Any
    display: str
    count: int
    fraction: float | None
    truncated: bool = False


@dataclass(frozen=True, slots=True)
class InsightHistogram:
    """Normalized histogram samples for numeric insight columns."""

    bins: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class CellPreview:
    """Preview of the value under the cursor."""

    column: str
    row: int
    absolute_row: int | None
    dtype: str | None
    raw_value: Any
    display: str
    truncated: bool


@dataclass(frozen=True, slots=True)
class ColumnInsight:
    """Aggregated metrics for a single column."""

    sheet_id: str | None
    plan_hash: str | None
    column_name: str
    dtype: str | None
    row_count: int | None
    non_null_count: int | None
    null_count: int | None
    null_fraction: float | None
    distinct_count: int | None
    stats: Mapping[str, Any]
    top_values: Sequence[TopValue]
    histogram: InsightHistogram | None = None
    source_path: str | None = None
    duration_ns: int | None = None
    error: str | None = None


__all__ = [
    "CellPreview",
    "ColumnInsight",
    "InsightHistogram",
    "LOW_CARDINALITY_NUMERIC_LIMIT",
    "TopValue",
    "summarize_value_preview",
]

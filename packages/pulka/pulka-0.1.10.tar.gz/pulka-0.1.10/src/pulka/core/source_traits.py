"""Per-source capability and cost hints inferred from ``polars.LazyFrame`` objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import polars as pl


@dataclass(frozen=True)
class Capabilities:
    """Describe high-level behaviours supported by a data source."""

    random_access: bool
    streaming: bool
    projection_pushdown: bool
    filter_pushdown: Literal["none", "partial", "full"]
    rowcount: Literal["exact", "estimate", "unknown"]
    stable_row_order: bool


@dataclass(frozen=True)
class CostModel:
    """Rudimentary latency and throughput hints for a data source."""

    seek_ms: float
    scan_rows_per_ms: float
    batch_preferred_rows: int


@dataclass(frozen=True)
class SourceTraits:
    """Aggregated traits derived from a ``LazyFrame`` origin."""

    kind: str
    path: str | None
    caps: Capabilities
    cost: CostModel


def infer_from_lazyframe(
    lf: pl.LazyFrame,
    *,
    fallback_kind: str | None = None,
    fallback_path: str | None = None,
) -> SourceTraits:
    """Infer :class:`SourceTraits` from a tagged ``polars.LazyFrame``.

    ``fallback_kind`` and ``fallback_path`` let callers supply origin metadata when
    the Polars operations that produced ``lf`` did not propagate Pulka's custom
    attributes.
    """

    kind = getattr(lf, "_pulka_source_kind", None) or fallback_kind or "unknown"
    path = getattr(lf, "_pulka_path", None)
    if path is None:
        path = fallback_path

    if kind in {"csv", "tsv", "jsonl"}:
        return SourceTraits(
            kind=kind,
            path=path,
            caps=Capabilities(
                random_access=False,
                streaming=True,
                projection_pushdown=False,
                filter_pushdown="partial",
                rowcount="estimate",
                stable_row_order=True,
            ),
            cost=CostModel(
                seek_ms=50.0,
                scan_rows_per_ms=600.0,
                batch_preferred_rows=8192,
            ),
        )

    if kind in {"parquet", "ipc"}:
        return SourceTraits(
            kind=kind,
            path=path,
            caps=Capabilities(
                random_access=True,
                streaming=True,
                projection_pushdown=True,
                filter_pushdown="full",
                rowcount="exact",
                stable_row_order=True,
            ),
            cost=CostModel(
                seek_ms=4.0,
                scan_rows_per_ms=4000.0,
                batch_preferred_rows=4096,
            ),
        )

    return SourceTraits(
        kind=kind,
        path=path,
        caps=Capabilities(
            random_access=False,
            streaming=True,
            projection_pushdown=False,
            filter_pushdown="partial",
            rowcount="unknown",
            stable_row_order=True,
        ),
        cost=CostModel(
            seek_ms=25.0,
            scan_rows_per_ms=1000.0,
            batch_preferred_rows=4096,
        ),
    )


__all__ = ["Capabilities", "CostModel", "SourceTraits", "infer_from_lazyframe"]

"""Compile row access strategies based on source traits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .source_traits import SourceTraits


@dataclass(frozen=True)
class Strategy:
    """Describe how a :class:`RowProvider` should access a data source."""

    mode: Literal["streaming", "random_access"]
    batch_rows: int
    prefetch_windows: int
    allow_skeleton_on_jump: bool
    downgrade_formatting_on_fast_scroll: bool
    build_sidecar_after_screens: int | None


def compile_strategy(traits: SourceTraits) -> Strategy:
    """Return a :class:`Strategy` tuned to ``traits``."""

    caps = traits.caps
    kind = traits.kind
    cost = traits.cost

    if caps.streaming and not caps.random_access:
        return Strategy(
            mode="streaming",
            batch_rows=max(8192, cost.batch_preferred_rows),
            prefetch_windows=2,
            allow_skeleton_on_jump=True,
            downgrade_formatting_on_fast_scroll=True,
            build_sidecar_after_screens=3 if kind in {"csv", "tsv", "jsonl"} else None,
        )

    if caps.random_access:
        return Strategy(
            mode="random_access",
            batch_rows=max(2048, cost.batch_preferred_rows),
            prefetch_windows=1,
            allow_skeleton_on_jump=False,
            downgrade_formatting_on_fast_scroll=True,
            build_sidecar_after_screens=None,
        )

    return Strategy(
        mode="streaming",
        batch_rows=4096,
        prefetch_windows=1,
        allow_skeleton_on_jump=True,
        downgrade_formatting_on_fast_scroll=True,
        build_sidecar_after_screens=None,
    )


__all__ = ["Strategy", "compile_strategy"]

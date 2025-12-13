"""Typed viewer snapshot structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ViewerCursor:
    """Immutable cursor position exposed to consumers."""

    row: int
    col: int


@dataclass(frozen=True, slots=True)
class ViewerViewport:
    """Immutable viewport bounds and span."""

    row0: int
    rowN: int  # noqa: N815 - keep mixedCase for parity with public snapshot
    col0: int
    colN: int  # noqa: N815 - keep mixedCase for parity with public snapshot
    rows: int
    cols: int


@dataclass(frozen=True, slots=True)
class ViewerPublicState:
    """Public, immutable snapshot of viewer state."""

    cursor: ViewerCursor
    viewport: ViewerViewport
    columns: tuple[str, ...]
    visible_columns: tuple[str, ...]
    hidden_columns: tuple[str, ...]
    frozen_columns: tuple[str, ...]
    total_rows: int | None
    visible_row_count: int
    total_columns: int
    visible_column_count: int
    hidden_column_count: int
    status_message: str | None
    highlighted_column: str | None
    width_mode: Literal["default", "single", "all"]
    width_target: int | None
    all_columns_maximized: bool
    sort_column: str | None
    sort_ascending: bool
    filter_text: str | None
    filter_kind: Literal["expr", "sql"] | None
    search_text: str | None
    frequency_mode: bool
    frequency_source_column: str | None

    @property
    def width_mode_state(self) -> dict[str, int | None | str]:
        """Return a serialisable representation of the active width mode."""

        return {"mode": self.width_mode, "target": self.width_target}


__all__ = ["ViewerCursor", "ViewerViewport", "ViewerPublicState"]

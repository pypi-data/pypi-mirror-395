"""Helpers to build immutable viewer snapshots."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, Protocol, cast

from .types import ViewerCursor, ViewerPublicState, ViewerViewport

literal_width_mode = Literal["default", "single", "all"]
literal_filter_kind = Literal["expr", "sql"]


class SnapshotSource(Protocol):
    """Structural protocol for objects that can emit public viewer state."""

    @property
    def columns(self) -> list[str]: ...

    @property
    def visible_cols(self) -> list[str]: ...

    @property
    def _hidden_cols(self) -> set[str]: ...

    @property
    def frozen_columns(self) -> Sequence[str]: ...

    @property
    def view_height(self) -> int: ...

    @property
    def row0(self) -> int: ...

    @property
    def col0(self) -> int: ...

    @property
    def cur_row(self) -> int: ...

    @property
    def cur_col(self) -> int: ...

    @property
    def _total_rows(self) -> int | None: ...

    @property
    def _width_mode(self) -> str: ...

    @property
    def sort_col(self) -> str | None: ...

    @property
    def sort_asc(self) -> bool: ...

    @property
    def filter_text(self) -> str | None: ...

    @property
    def filter_kind(self) -> str | None: ...

    @property
    def search_text(self) -> str | None: ...

    @property
    def is_freq_view(self) -> bool: ...

    @property
    def freq_source_col(self) -> str | None: ...

    @property
    def status_message(self) -> str | None: ...

    @property
    def maximized_column_index(self) -> int | None: ...

    @property
    def all_columns_maximized(self) -> bool: ...


def build_public_state(source: SnapshotSource) -> ViewerPublicState:
    """Return an immutable snapshot of the viewer suitable for public use."""

    columns = tuple(source.columns)
    visible_columns = tuple(source.visible_cols)
    hidden_columns = tuple(name for name in columns if name in source._hidden_cols)
    frozen_columns = tuple(source.frozen_columns)

    visible_row_count = max(0, source.view_height)
    visible_column_count = len(visible_columns)

    col_span = visible_column_count
    row_span = visible_row_count

    viewport = ViewerViewport(
        row0=source.row0,
        rowN=source.row0 + max(0, row_span - 1),
        col0=source.col0,
        colN=source.col0 + max(0, col_span - 1),
        rows=row_span,
        cols=col_span,
    )

    highlighted_column: str | None = None
    if columns and 0 <= source.cur_col < len(columns):
        highlighted_column = columns[source.cur_col]

    raw_width_mode: str = (
        source._width_mode if source._width_mode in {"default", "single", "all"} else "default"
    )
    width_mode = cast(literal_width_mode, raw_width_mode)

    raw_filter_kind: str | None = (
        source.filter_kind if source.filter_kind in {"expr", "sql"} else None
    )
    filter_kind = cast(literal_filter_kind | None, raw_filter_kind)

    return ViewerPublicState(
        cursor=ViewerCursor(row=source.cur_row, col=source.cur_col),
        viewport=viewport,
        columns=columns,
        visible_columns=visible_columns,
        hidden_columns=hidden_columns,
        frozen_columns=frozen_columns,
        total_rows=source._total_rows,
        visible_row_count=visible_row_count,
        total_columns=len(columns),
        visible_column_count=visible_column_count,
        hidden_column_count=len(hidden_columns),
        status_message=source.status_message,
        highlighted_column=highlighted_column,
        width_mode=width_mode,
        width_target=source.maximized_column_index,
        all_columns_maximized=source.all_columns_maximized,
        sort_column=source.sort_col,
        sort_ascending=source.sort_asc,
        filter_text=source.filter_text,
        filter_kind=filter_kind,
        search_text=source.search_text,
        frequency_mode=source.is_freq_view,
        frequency_source_column=source.freq_source_col,
    )


__all__ = ["build_public_state", "SnapshotSource"]

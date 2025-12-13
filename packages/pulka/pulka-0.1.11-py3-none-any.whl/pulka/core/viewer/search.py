from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any, Literal, Protocol, cast, runtime_checkable

import polars as pl

from ..plan import QueryPlan
from ..row_provider import RowProvider


@runtime_checkable
class SearchNavigation(Protocol):
    """Minimal surface that :class:`SearchController` needs from ``Viewer``."""

    columns: list[str]
    cur_row: int
    cur_col: int
    row0: int

    @property
    def sheet(self) -> Any: ...

    @property
    def row_provider(self) -> RowProvider: ...

    @property
    def status_message(self) -> str | None: ...

    @status_message.setter
    def status_message(self, message: str | None) -> None: ...

    def clamp(self) -> None: ...

    def center_current_row(self) -> None: ...

    def _body_view_height(self) -> int: ...

    def _effective_frozen_row_count(self) -> int: ...

    def _current_plan(self) -> QueryPlan | None: ...

    def _ensure_total_rows(self) -> int | None: ...


class SearchController:
    """Own search and diff-navigation state for the viewer."""

    def __init__(self, navigation: SearchNavigation) -> None:
        self._nav = navigation
        self._local_search_text: str | None = None
        self._last_search_kind: Literal["text", "value"] | None = None
        self._last_search_value: object | None = None
        self._last_search_column: str | None = None

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    @property
    def search_text(self) -> str | None:
        """Return the active search text tracked by the plan when available."""

        if self._local_search_text is not None:
            return self._local_search_text
        plan = self._nav._current_plan()
        if plan is None:
            return None
        return plan.search_text

    @search_text.setter
    def search_text(self, value: str | None) -> None:
        self._local_search_text = value

    @property
    def last_search_kind(self) -> Literal["text", "value"] | None:
        return self._last_search_kind

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _value_is_nan(value: object) -> bool:
        try:
            return bool(math.isnan(value))  # type: ignore[arg-type]
        except Exception:
            return False

    def _values_equal(self, left: object, right: object) -> bool:
        """Return True when ``left`` and ``right`` should be treated as equal for search."""

        if left is right:
            return True
        if left is None or right is None:
            return left is None and right is None
        if self._value_is_nan(left) and self._value_is_nan(right):
            return True
        if isinstance(left, pl.Series) or isinstance(right, pl.Series):
            left_values = left.to_list() if isinstance(left, pl.Series) else left
            right_values = right.to_list() if isinstance(right, pl.Series) else right
            return self._values_equal(left_values, right_values)
        if isinstance(left, Mapping) and isinstance(right, Mapping):
            if set(left.keys()) != set(right.keys()):
                return False
            return all(self._values_equal(left[key], right.get(key)) for key in left)
        if isinstance(left, Sequence) and not isinstance(left, (str, bytes, bytearray)):
            if not (isinstance(right, Sequence) and not isinstance(right, (str, bytes, bytearray))):
                return False
            left_seq = list(left)
            right_seq = list(right)
            if len(left_seq) != len(right_seq):
                return False
            return all(
                self._values_equal(lv, rv) for lv, rv in zip(left_seq, right_seq, strict=True)
            )
        try:
            return left == right
        except Exception:
            return False

    @staticmethod
    def _value_preview(value: object, *, max_length: int = 60) -> str:
        if value is None:
            text = "null"
        elif SearchController._value_is_nan(value):
            text = "NaN"
        else:
            try:
                text = repr(value)
            except Exception:
                text = "<unrepr>"
        if len(text) > max_length:
            return text[: max_length - 3] + "..."
        return text

    def _record_last_search(
        self,
        kind: Literal["text", "value"],
        *,
        column: str | None = None,
        value: object | None = None,
    ) -> None:
        self._last_search_kind = kind
        self._last_search_column = column
        self._last_search_value = value

    def clear_last_search(self) -> None:
        self._last_search_kind = None
        self._last_search_column = None
        self._last_search_value = None

    def _search_values(self, column: str) -> tuple[list[str], list[bool]]:
        """Return stringified column values and a null mask for search operations."""
        total_rows = self._nav._ensure_total_rows()
        if total_rows is None or total_rows <= 0:
            return [], []

        try:
            table_slice = self._nav.sheet.fetch_slice(0, total_rows, [column])
        except Exception:
            return [], []

        if column not in table_slice.column_names:
            return [], []

        column_slice = table_slice.column(column)
        values: list[str] = []
        nulls: list[bool] = []
        for val in column_slice.values:
            is_null = val is None
            nulls.append(is_null)
            if is_null:
                values.append("")
            elif isinstance(val, str):
                values.append(val)
            else:
                try:
                    values.append(str(val))
                except Exception:
                    values.append("")
        return values, nulls

    def _get_current_value(self) -> object | None:
        """Get the value at the current cursor position."""
        try:
            current_col = self._nav.columns[self._nav.cur_col]
            table_slice = self._nav.sheet.fetch_slice(self._nav.cur_row, 1, [current_col])
            if (
                table_slice.height > 0
                and current_col in table_slice.column_names
                and table_slice.column(current_col).values
            ):
                return cast(object, table_slice.column(current_col).values[0])
            return None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def set_search(self, text: str | None) -> None:
        """Record the active search text (whitespace-trimmed)."""
        cleaned = None if text is None else text.strip() or None
        self.search_text = cleaned
        term = self.search_text
        if term:
            self._nav.status_message = f"search: '{term}'"
            self._record_last_search("text", value=term)
        else:
            self._nav.status_message = "search cleared"
            if self._last_search_kind == "text":
                self.clear_last_search()

    def search(
        self,
        *,
        forward: bool,
        include_current: bool = False,
        center: bool = True,
        wrap: bool = True,
    ) -> bool:
        """Search within the current column for the recorded search string."""
        term = self.search_text
        self.search_text = term
        if not term:
            self._nav.status_message = "search: no active query"
            return False

        if not self._nav.columns:
            self._nav.status_message = f"search '{term}': no columns"
            return False

        values, nulls = self._search_values(self._nav.columns[self._nav.cur_col])
        total_rows = len(values)
        if total_rows == 0:
            self._nav.status_message = f"search '{term}': no rows"
            return False

        term_lower = term.lower()
        match_nulls = term_lower in {"none", "null"}
        start_idx = max(0, min(self._nav.cur_row, total_rows - 1))

        def _iter_positions() -> list[tuple[int, bool]]:
            if wrap:
                if forward:
                    first_segment = (
                        total_rows - start_idx
                        if include_current
                        else max(0, total_rows - (start_idx + 1))
                    )
                    idx = start_idx if include_current else start_idx + 1
                    step = 1
                else:
                    first_segment = start_idx + 1 if include_current else max(0, start_idx)
                    idx = start_idx if include_current else start_idx - 1
                    step = -1

                positions: list[tuple[int, bool]] = []
                current = idx
                for i in range(total_rows):
                    current %= total_rows
                    positions.append((current, i >= first_segment))
                    current += step
                return positions

            if forward:
                start = start_idx if include_current else start_idx + 1
                if start < 0:
                    start = 0
                if start >= total_rows:
                    return []
                return [(row, False) for row in range(start, total_rows)]
            start = start_idx if include_current else start_idx - 1
            if start < 0:
                return []
            if start >= total_rows:
                start = total_rows - 1
            return [(row, False) for row in range(start, -1, -1)]

        for row, wrapped in _iter_positions():
            value = values[row]
            is_null = nulls[row] if row < len(nulls) else False
            if (match_nulls and is_null) or term_lower in value.lower():
                self._nav.cur_row = row
                body_height = self._nav._body_view_height()
                frozen_min = self._nav._effective_frozen_row_count()
                if center:
                    half = max(1, body_height) // 2
                    self._nav.row0 = max(frozen_min, self._nav.cur_row - half)
                else:
                    if self._nav.cur_row < self._nav.row0:
                        self._nav.row0 = max(frozen_min, self._nav.cur_row)
                    elif self._nav.cur_row >= self._nav.row0 + body_height:
                        self._nav.row0 = max(frozen_min, self._nav.cur_row - body_height + 1)
                self._nav.clamp()
                wrap_msg = " (wrapped)" if wrapped else ""
                self._nav.status_message = f"search '{term}'{wrap_msg}"
                self._record_last_search(
                    "text",
                    column=self._nav.columns[self._nav.cur_col],
                    value=term,
                )
                return True

        if wrap:
            self._nav.status_message = f"search '{term}': no match"
        else:
            direction = "next" if forward else "previous"
            self._nav.status_message = f"search '{term}': no {direction} match"
        return False

    def search_value(
        self,
        *,
        forward: bool,
        include_current: bool = False,
        center: bool = True,
    ) -> bool:
        """Search within the current column for the active cell's value."""

        if (
            not self._nav.columns
            or self._nav.cur_col < 0
            or self._nav.cur_col >= len(self._nav.columns)
        ):
            self._nav.status_message = "value search: no columns"
            return False

        column_name = self._nav.columns[self._nav.cur_col]
        total_rows = self._nav._ensure_total_rows()
        if total_rows is None or total_rows <= 0:
            self._nav.status_message = "value search: no rows"
            return False

        plan = self._nav._current_plan()
        try:
            current_slice, _ = self._nav.row_provider.get_slice(
                plan,
                (column_name,),
                self._nav.cur_row,
                1,
            )
        except Exception as exc:  # pragma: no cover - defensive
            self._nav.status_message = f"value search error: {exc}"
            return False

        if current_slice.height <= 0 or column_name not in current_slice.column_names:
            self._nav.status_message = "value search: value unavailable"
            return False

        try:
            values = current_slice.column(column_name).values
            target_value = values[0] if values else None
        except Exception:
            self._nav.status_message = "value search: value unavailable"
            return False

        self._record_last_search("value", column=column_name, value=target_value)

        preview = self._value_preview(target_value)
        start_row = (
            self._nav.cur_row
            if include_current
            else (self._nav.cur_row + 1 if forward else self._nav.cur_row - 1)
        )
        direction = "next" if forward else "previous"

        if forward and start_row >= total_rows:
            self._nav.status_message = f"value search: no {direction} match for {preview}"
            return False
        if not forward and start_row < 0:
            self._nav.status_message = f"value search: no {direction} match for {preview}"
            return False

        row_provider = self._nav.row_provider
        chunk = 1024
        current_plan = plan

        if forward:
            row = start_row
            while row < total_rows:
                fetch_count = min(chunk, total_rows - row)
                try:
                    table_slice, _ = row_provider.get_slice(
                        current_plan,
                        (column_name,),
                        row,
                        fetch_count,
                    )
                except Exception as exc:  # pragma: no cover - defensive
                    self._nav.status_message = f"value search error: {exc}"
                    return False

                if table_slice.height <= 0:
                    break
                if column_name not in table_slice.column_names:
                    self._nav.status_message = "value search: column unavailable"
                    return False

                base_row = table_slice.start_offset if table_slice.start_offset is not None else row
                try:
                    column_values = table_slice.column(column_name).values
                except Exception:
                    column_values = ()

                for idx, candidate in enumerate(column_values):
                    abs_row = base_row + idx
                    if abs_row == self._nav.cur_row and not include_current:
                        continue
                    if self._values_equal(candidate, target_value):
                        self._nav.cur_row = abs_row
                        if center:
                            self._nav.center_current_row()
                        else:
                            self._nav.clamp()
                        self._nav.status_message = f"value search: {direction} match for {preview}"
                        return True

                row = base_row + table_slice.height
        else:
            row = start_row
            while row >= 0:
                fetch_count = min(chunk, row + 1)
                fetch_start = row - fetch_count + 1
                try:
                    table_slice, _ = row_provider.get_slice(
                        current_plan,
                        (column_name,),
                        fetch_start,
                        fetch_count,
                    )
                except Exception as exc:  # pragma: no cover - defensive
                    self._nav.status_message = f"value search error: {exc}"
                    return False

                if table_slice.height <= 0:
                    break
                if column_name not in table_slice.column_names:
                    self._nav.status_message = "value search: column unavailable"
                    return False

                base_row = (
                    table_slice.start_offset
                    if table_slice.start_offset is not None
                    else fetch_start
                )
                try:
                    column_values = table_slice.column(column_name).values
                except Exception:
                    column_values = ()

                for idx in range(len(column_values) - 1, -1, -1):
                    abs_row = base_row + idx
                    if abs_row == self._nav.cur_row and not include_current:
                        continue
                    if abs_row > row:
                        continue
                    if self._values_equal(column_values[idx], target_value):
                        self._nav.cur_row = abs_row
                        if center:
                            self._nav.center_current_row()
                        else:
                            self._nav.clamp()
                        self._nav.status_message = f"value search: {direction} match for {preview}"
                        return True

                row = base_row - 1

        self._nav.status_message = f"value search: no {direction} match for {preview}"
        return False

    def next_search_match(self) -> bool:
        """Advance to the next row search match."""

        return self.search(forward=True, include_current=False, center=True, wrap=False)

    def prev_search_match(self) -> bool:
        """Move to the previous row search match."""

        return self.search(forward=False, include_current=False, center=True, wrap=False)

    def repeat_last_search(self, *, forward: bool) -> bool:
        """Repeat the last search (text or value), advancing in ``forward`` direction."""

        if self._last_search_kind == "value":
            if not self._nav.columns:
                self._nav.status_message = "value search: no columns"
                return False
            if self._nav.cur_col < 0 or self._nav.cur_col >= len(self._nav.columns):
                self._nav.status_message = "value search: no columns"
                return False
            if (
                self._last_search_column
                and self._nav.columns[self._nav.cur_col] != self._last_search_column
            ):
                self._nav.status_message = "value search: column changed"
                return False
            return self.search_value(forward=forward, include_current=False, center=True)

        return self.search(forward=forward, include_current=False, center=True, wrap=False)

    def prev_different_value(self) -> bool:
        """Navigate to the previous row with a different value in the current column."""
        if self._nav.cur_row <= 0:
            self._nav.status_message = "already at top"
            return False

        current_value = self._get_current_value()
        current_col = self._nav.columns[self._nav.cur_col]

        try:
            start_idx = max(0, self._nav.cur_row - 1000)
            table_slice = self._nav.sheet.fetch_slice(
                start_idx,
                self._nav.cur_row - start_idx,
                [current_col],
            )

            if current_col not in table_slice.column_names:
                raise ValueError("column not in slice")

            values = table_slice.column(current_col).values

            for i in range(table_slice.height - 1, -1, -1):
                if values[i] != current_value:
                    target_row = start_idx + i
                    target_value = values[i]
                    self._nav.cur_row = target_row
                    self._nav.clamp()
                    self._nav.status_message = f"found different value: {target_value}"
                    return True

        except Exception:
            pass

        self._nav.status_message = "no different value found above"
        return False

    def next_different_value(self) -> bool:
        """Navigate to the next row with a different value in the current column."""
        current_value = self._get_current_value()
        current_col = self._nav.columns[self._nav.cur_col]

        try:
            table_slice = self._nav.sheet.fetch_slice(
                self._nav.cur_row + 1,
                1000,
                [current_col],
            )

            if current_col not in table_slice.column_names:
                raise ValueError("column not in slice")

            values = table_slice.column(current_col).values

            for i, value in enumerate(values):
                if value != current_value:
                    target_row = self._nav.cur_row + 1 + i
                    target_value = value
                    self._nav.cur_row = target_row
                    self._nav.clamp()
                    self._nav.status_message = f"found different value: {target_value}"
                    return True

        except Exception:
            pass

        self._nav.status_message = "no different value found below"
        return False

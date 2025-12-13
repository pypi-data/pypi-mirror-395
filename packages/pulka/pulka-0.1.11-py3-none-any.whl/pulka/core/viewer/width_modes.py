from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from time import monotonic_ns
from typing import Any, Literal, Protocol, runtime_checkable

type VisibleCacheKey = (
    tuple[int, int, int, int | None, tuple[str, ...], tuple[int, ...], tuple[int, ...]] | None
)


@dataclass(slots=True)
class VisibleColumnsCache:
    """Cache key and payload for visible column calculations."""

    key: VisibleCacheKey = None
    columns: list[str] = field(default_factory=list)
    last_col_fits_completely: bool = True


@runtime_checkable
class WidthNavigation(Protocol):
    """Minimal surface that :class:`WidthModeController` needs from ``Viewer``."""

    columns: list[str]
    col0: int
    cur_col: int
    view_width_chars: int
    _viewport_cols_override: int | None
    _hidden_cols: set[str]
    _header_widths: list[int]
    _default_header_widths: list[int]
    _compact_width_layout: bool
    _aligning_active_column: bool
    _max_visible_col: int | None
    status_message: str | None

    @property
    def frozen_columns(self) -> list[str]: ...

    def _frozen_column_indices(self) -> list[int]: ...

    def _frozen_column_name_set(self) -> frozenset[str]: ...

    def _first_scrollable_col_index(self) -> int: ...

    def _ensure_col_visible_right_aligned(self, target: int) -> None: ...

    def clamp(self) -> None: ...

    @property
    def _perf_callback(self) -> Callable[[str, float, dict[str, Any]], None] | None: ...

    def _record_perf_event(
        self, phase: str, duration_ms: float, payload: dict[str, Any]
    ) -> None: ...


@runtime_checkable
class WidthCalculator(Protocol):
    """Narrow interface for width computations."""

    def apply_width_mode(self) -> None: ...

    def autosize_visible_columns(self, column_indices: list[int]) -> None: ...

    def force_default_mode(self) -> None: ...

    def toggle_maximize_current_col(self) -> None: ...

    def toggle_maximize_all_cols(self) -> None: ...


class WidthModeController:
    """Own width mode state, caching, and visible column planning."""

    def __init__(
        self,
        navigation: WidthNavigation,
        *,
        widths: WidthCalculator,
        initial_visible_cols: list[str] | None = None,
    ) -> None:
        self._nav = navigation
        self._widths = widths

        self._width_mode: Literal["default", "single", "all"] = "default"
        self._width_target: int | None = None
        self._width_cache_all: list[int] | None = None
        self._width_cache_single: dict[int, int] = {}
        self._autosized_widths: dict[int, int] = {}
        self._sticky_column_widths: dict[str, int] = {}
        self._has_partial_column: bool = False
        self._partial_column_index: int | None = None
        self._stretch_last_for_slack: bool = False
        self._visible_cache = VisibleColumnsCache(
            key=None,
            columns=list(initial_visible_cols or []),
            last_col_fits_completely=True,
        )

    # ------------------------------------------------------------------
    # State accessors
    # ------------------------------------------------------------------

    @property
    def width_mode(self) -> Literal["default", "single", "all"]:
        return self._width_mode

    @width_mode.setter
    def width_mode(self, value: Literal["default", "single", "all"]) -> None:
        self._width_mode = value

    @property
    def width_target(self) -> int | None:
        return self._width_target

    @width_target.setter
    def width_target(self, value: int | None) -> None:
        self._width_target = value

    @property
    def width_cache_all(self) -> list[int] | None:
        return self._width_cache_all

    @width_cache_all.setter
    def width_cache_all(self, value: list[int] | None) -> None:
        self._width_cache_all = value

    @property
    def width_cache_single(self) -> dict[int, int]:
        return self._width_cache_single

    @width_cache_single.setter
    def width_cache_single(self, value: dict[int, int]) -> None:
        self._width_cache_single = value

    @property
    def autosized_widths(self) -> dict[int, int]:
        return self._autosized_widths

    @autosized_widths.setter
    def autosized_widths(self, value: dict[int, int]) -> None:
        self._autosized_widths = value

    @property
    def sticky_column_widths(self) -> dict[str, int]:
        return self._sticky_column_widths

    @sticky_column_widths.setter
    def sticky_column_widths(self, value: dict[str, int]) -> None:
        self._sticky_column_widths = value

    @property
    def has_partial_column(self) -> bool:
        return self._has_partial_column

    @has_partial_column.setter
    def has_partial_column(self, value: bool) -> None:
        self._has_partial_column = value

    @property
    def partial_column_index(self) -> int | None:
        return self._partial_column_index

    @partial_column_index.setter
    def partial_column_index(self, value: int | None) -> None:
        self._partial_column_index = value

    @property
    def stretch_last_for_slack(self) -> bool:
        return self._stretch_last_for_slack

    @stretch_last_for_slack.setter
    def stretch_last_for_slack(self, value: bool) -> None:
        self._stretch_last_for_slack = value

    @property
    def visible_cache(self) -> VisibleColumnsCache:
        return self._visible_cache

    # ------------------------------------------------------------------
    # Width helpers
    # ------------------------------------------------------------------

    def apply_width_mode(self) -> None:
        self._widths.apply_width_mode()

    def force_default_mode(self) -> None:
        self._widths.force_default_mode()

    def autosize_visible_columns(self, column_indices: list[int]) -> None:
        self._widths.autosize_visible_columns(column_indices)

    def toggle_maximize_current_col(self) -> None:
        self._widths.toggle_maximize_current_col()

    def toggle_maximize_all_cols(self) -> None:
        self._widths.toggle_maximize_all_cols()

    @property
    def maximized_column_index(self) -> int | None:
        if self._width_mode == "single" and self._width_target is not None:
            return self._width_target
        return None

    @property
    def all_columns_maximized(self) -> bool:
        return self._width_mode == "all"

    @property
    def width_mode_state(self) -> dict[str, int | None | str]:
        return {"mode": self._width_mode, "target": self.maximized_column_index}

    def invalidate_visible_cache(self) -> None:
        self._visible_cache.key = None

    # ------------------------------------------------------------------
    # Visible columns planning
    # ------------------------------------------------------------------

    def compute_visible_columns(self) -> list[str]:
        nav = self._nav
        visible_columns = [col for col in nav.columns if col not in nav._hidden_cols]
        frozen_indices = nav._frozen_column_indices()
        frozen_names = nav.frozen_columns
        frozen_set = nav._frozen_column_name_set()

        def _has_more_to_right(current: list[str]) -> bool:
            if not current:
                return False
            try:
                last_name = current[-1]
                last_idx = nav.columns.index(last_name)
            except (ValueError, IndexError):
                return False
            for idx in range(last_idx + 1, len(nav.columns)):
                name = nav.columns[idx]
                if name in nav._hidden_cols or name in frozen_set:
                    continue
                return True
            return False

        if nav._viewport_cols_override is not None:
            should_record = nav._perf_callback is not None
            start_ns = monotonic_ns() if should_record else 0

            max_dynamic = max(1, nav._viewport_cols_override)
            scroll_start = max(nav.col0, nav._first_scrollable_col_index())
            dynamic: list[str] = []
            for idx in range(scroll_start, len(nav.columns)):
                name = nav.columns[idx]
                if name in nav._hidden_cols or name in frozen_set:
                    continue
                dynamic.append(name)
                if len(dynamic) >= max_dynamic:
                    break

            result = frozen_names + dynamic
            self._visible_cache.last_col_fits_completely = True
            self._visible_cache.columns = result
            self._visible_cache.key = None

            index_lookup = {name: idx for idx, name in enumerate(nav.columns)}
            visible_indices = [index_lookup[col] for col in result if col in index_lookup]
            self.autosize_visible_columns(visible_indices)

            if should_record:
                duration_ms = (monotonic_ns() - start_ns) / 1_000_000
                payload = {
                    "viewport_override": True,
                    "col0": nav.col0,
                    "visible_count": len(result),
                    "hidden_count": len(nav._hidden_cols),
                    "frozen": len(frozen_names),
                }
                nav._record_perf_event("viewer.visible_cols", duration_ms, payload)
            return result

        key: VisibleCacheKey = (
            nav.col0,
            nav.cur_col,
            nav.view_width_chars,
            nav._viewport_cols_override,
            tuple(sorted(nav._hidden_cols)),
            tuple(nav._header_widths),
            tuple(frozen_indices),
        )
        if key == self._visible_cache.key and not (
            nav._compact_width_layout
            and self._width_mode == "default"
            and _has_more_to_right(self._visible_cache.columns)
        ):
            return self._visible_cache.columns

        self._has_partial_column = False
        self._partial_column_index = None
        self._stretch_last_for_slack = False

        should_record = nav._perf_callback is not None
        start_ns = monotonic_ns() if should_record else 0
        evaluated = 0

        max_width = max(20, nav.view_width_chars)
        allow_partial_width = self._width_mode == "default"
        used = 1  # left border
        res: list[str] = []
        last_fits_completely = True

        for idx in frozen_indices:
            name = nav.columns[idx]
            if name in nav._hidden_cols:
                continue
            res.append(name)
            used += nav._header_widths[idx] + 1

        if used > max_width:
            last_fits_completely = False

        scroll_start = max(nav.col0, nav._first_scrollable_col_index())

        last_iter_idx = scroll_start - 1
        partial_min_width = 2
        for idx in range(scroll_start, len(nav.columns)):
            name = nav.columns[idx]
            if name in nav._hidden_cols or name in frozen_set:
                continue

            evaluated += 1
            last_iter_idx = idx
            w = nav._header_widths[idx]

            if used + w + 1 <= max_width:
                used += w + 1
                res.append(name)
            else:
                remaining = max_width - used
                min_required = partial_min_width + 1
                if remaining >= min_required and (
                    len(res) == len(frozen_names) or allow_partial_width
                ):
                    res.append(name)
                    last_fits_completely = False
                    self._has_partial_column = True
                    self._partial_column_index = idx
                break

        active_name: str | None = None
        if 0 <= nav.cur_col < len(nav.columns):
            active_name = nav.columns[nav.cur_col]

        active_is_partial_last = (
            allow_partial_width
            and not last_fits_completely
            and not nav._aligning_active_column
            and nav._viewport_cols_override is None
            and res
            and active_name is not None
            and res[-1] == active_name
        )

        if active_is_partial_last:
            prev_col0 = nav.col0
            nav._aligning_active_column = True
            try:
                nav._ensure_col_visible_right_aligned(nav.cur_col)
            finally:
                nav._aligning_active_column = False
            if nav.col0 != prev_col0:
                self._visible_cache.key = None
                return self.compute_visible_columns()

        if allow_partial_width and res and not self._has_partial_column:
            remaining = max_width - used
            min_required = partial_min_width + 1
            next_idx: int | None = None
            for idx in range(last_iter_idx + 1, len(nav.columns)):
                name = nav.columns[idx]
                if name in nav._hidden_cols or name in frozen_set:
                    continue
                next_idx = idx
                break

            if (
                next_idx is not None
                and nav.columns[next_idx] not in res
                and remaining >= min_required
            ):
                res.append(nav.columns[next_idx])
                last_fits_completely = False
                self._has_partial_column = True
                self._partial_column_index = next_idx
            elif (
                next_idx is not None
                and remaining > 0
                and remaining < min_required
                and nav._compact_width_layout
                and self._width_mode == "default"
            ):
                self._stretch_last_for_slack = True
            else:
                self._stretch_last_for_slack = False
        else:
            self._stretch_last_for_slack = False

        if not res and visible_columns:
            for col in visible_columns:
                col_idx = nav.columns.index(col)
                if col_idx >= scroll_start:
                    res = [col]
                    break
            if not res:
                res = [visible_columns[0]]

        if (
            nav._max_visible_col is not None
            and res
            and not (nav._compact_width_layout and self._width_mode == "default")
        ):
            truncated_res = []
            for col in res:
                col_idx = nav.columns.index(col)
                if col in frozen_set or col_idx <= nav._max_visible_col:
                    truncated_res.append(col)
                else:
                    break
            res = truncated_res

        self._has_partial_column = self._has_partial_column and len(res) > len(frozen_names)
        if not self._has_partial_column:
            self._partial_column_index = None

        index_lookup = {name: idx for idx, name in enumerate(nav.columns)}
        visible_indices = [index_lookup[col] for col in res if col in index_lookup]
        self.autosize_visible_columns(visible_indices)

        self._visible_cache.key = key
        self._visible_cache.columns = res
        self._visible_cache.last_col_fits_completely = last_fits_completely

        if should_record:
            duration_ms = (monotonic_ns() - start_ns) / 1_000_000
            visible_payload: dict[str, object] = {
                "viewport_override": False,
                "col0": nav.col0,
                "visible_count": len(res),
                "evaluated": evaluated,
                "hidden_count": len(nav._hidden_cols),
                "max_width": max_width,
                "fits_full": last_fits_completely,
                "max_visible_col": nav._max_visible_col,
                "frozen": len(frozen_names),
            }
            nav._record_perf_event("viewer.visible_cols", duration_ms, visible_payload)
        return res

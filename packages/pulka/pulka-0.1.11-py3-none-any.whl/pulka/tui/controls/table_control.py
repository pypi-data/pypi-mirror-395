"""prompt_toolkit-native table control that renders from a viewport plan."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import nullcontext, suppress
from dataclasses import dataclass, replace
from time import perf_counter
from types import MethodType
from typing import TYPE_CHECKING, Any
from weakref import ReferenceType, ref

from prompt_toolkit.data_structures import Point
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.layout.controls import UIContent, UIControl
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType, MouseModifier

from ...logging import Recorder, frame_hash, viewer_state_snapshot
from ...render.status_bar import render_status_line
from ...render.style_resolver import get_active_style_resolver
from ...render.table import (
    RenderedLine,
    apply_overflow_indicators,
    build_blank_line,
    build_row_line,
    build_separator_line,
    compute_column_overflows,
    determine_blank_line_highlights,
)
from ...render.viewport_plan import Cell, ViewportPlan, compute_viewport_plan
from ...theme import theme_epoch

PlanCacheKey = tuple[Any, int, int, int, int, Any, int, int, Any, int]
LineCacheKey = tuple[Any, ...]

if TYPE_CHECKING:  # pragma: no cover - import cycles in typing context only
    from prompt_toolkit.key_binding.key_bindings import NotImplementedOrNone

    from ...core.viewer import Viewer
else:  # pragma: no cover - fallback for runtime typing introspection
    Viewer = Any


@dataclass(slots=True)
class _LineRender:
    """Container for rendered line fragments and plain text."""

    fragments: StyleAndTextTuples
    plain_text: str
    cursor_x: int | None = None
    source: RenderedLine | None = None


@dataclass(frozen=True, slots=True)
class _BudgetPlan:
    """Per-frame rendering adjustments when the budget guard triggers."""

    overscan_hint: int | None = None
    minimal_styles: bool = False
    drop_borders: bool = False
    coalesce_multiplier: float = 1.0

    def is_default(self) -> bool:
        return (
            self.overscan_hint is None
            and not self.minimal_styles
            and not self.drop_borders
            and self.coalesce_multiplier == 1.0
        )


class RenderBudgetGuard:
    """Track frame timings and request temporary render degradations."""

    def __init__(self, *, budget_ms: float = 18.0, alpha: float = 0.25) -> None:
        self._budget_ms = budget_ms
        self._alpha = alpha
        self._avg_ms: float | None = None
        self._degrade_next = False
        self._sample_count = 0

    def plan_frame(self, viewer: Viewer) -> _BudgetPlan:
        if not self._degrade_next:
            return _BudgetPlan()

        self._degrade_next = False
        overscan = max(1, int(getattr(viewer, "view_height", 1) or 1))
        return _BudgetPlan(
            overscan_hint=overscan,
            minimal_styles=True,
            drop_borders=True,
            coalesce_multiplier=2.0,
        )

    def record_frame(self, render_ms: float, paint_ms: float) -> None:
        total = render_ms + paint_ms
        self._sample_count += 1
        if self._avg_ms is None:
            self._avg_ms = total
        else:
            self._avg_ms = (1 - self._alpha) * self._avg_ms + self._alpha * total

        if self._sample_count >= 2 and (
            total > self._budget_ms or (self._avg_ms or 0.0) > self._budget_ms
        ):
            self._degrade_next = True

    @property
    def average_ms(self) -> float | None:
        return self._avg_ms


class TableControl(UIControl):
    """A prompt_toolkit ``UIControl`` that draws table cells from a viewport plan."""

    def __init__(
        self,
        viewer: Viewer,
        *,
        apply_pending_moves: Callable[[], None],
        poll_background_jobs: Callable[[], None],
        set_status: Callable[[StyleAndTextTuples], None],
        apply_budget_plan: Callable[[_BudgetPlan], None] | None = None,
        recorder: Recorder | None = None,
    ) -> None:
        self._viewer = viewer
        self._apply_pending_moves = apply_pending_moves
        self._poll_background_jobs = poll_background_jobs
        self._set_status = set_status
        self._apply_budget_plan = apply_budget_plan
        self._recorder = recorder
        self._cached_plan: ViewportPlan | None = None
        self._plan_cache_key: PlanCacheKey | None = None
        self._line_cache: dict[LineCacheKey, _LineRender] = {}
        self._wrapped_ui_hooks: set[Any] = set()
        self._wrapped_ui_hook_refs: list[ReferenceType[Any]] = []
        self._wrapped_ui_hook_ids: set[int] = set()
        self._budget_guard = RenderBudgetGuard()
        self._current_budget_plan = _BudgetPlan()
        self._current_theme_epoch = theme_epoch()
        self._recorded_style_epoch: int | None = None
        self._last_plan_cache_hit = False
        self._last_frame_finished_at: float | None = None
        self._last_move_direction: int = 0
        self._last_move_time: float | None = None
        self._last_coalesced_steps: int = 0
        self._last_overscan_rows: int = 0
        self._coalesce_hot_window = 0.25
        self._overscan_ratio = 0.25

    def update_viewer(self, viewer: Viewer) -> None:
        """Point the control at the active viewer."""

        self._viewer = viewer
        self._invalidate_cache()

    def attach_ui_hooks(self, ui_hooks: Any) -> Any:
        """Wrap ``ui_hooks.invalidate`` to clear cached render state."""

        invalidate = getattr(ui_hooks, "invalidate", None)
        if invalidate is None:
            return ui_hooks

        hook_id = id(ui_hooks)

        try:
            if ui_hooks in self._wrapped_ui_hooks:
                return ui_hooks
        except TypeError:
            pass

        for hook_ref in list(self._wrapped_ui_hook_refs):
            hook = hook_ref()
            if hook is None:
                self._wrapped_ui_hook_refs.remove(hook_ref)
                continue
            if hook is ui_hooks:
                return ui_hooks

        if hook_id in self._wrapped_ui_hook_ids:
            return ui_hooks

        bound_self = getattr(invalidate, "__self__", None)
        bound_func = getattr(invalidate, "__func__", None)

        def _wrapped_invalidate(*args: Any, **kwargs: Any) -> Any:
            self._invalidate_cache()
            if bound_self is not None and bound_func is not None:
                return bound_func(bound_self, *args[1:], **kwargs)
            return invalidate(*args[1:], **kwargs) if args else invalidate(**kwargs)

        ui_hooks.invalidate = MethodType(_wrapped_invalidate, ui_hooks)
        try:
            self._wrapped_ui_hooks.add(ui_hooks)
        except TypeError:
            try:
                self._wrapped_ui_hook_refs.append(ref(ui_hooks))
            except TypeError:
                self._wrapped_ui_hook_ids.add(hook_id)
        return ui_hooks

    def preferred_width(self, max_available_width: int) -> int | None:  # noqa: D401
        _ = max_available_width
        return None

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Callable[[int], str] | None,
    ) -> int | None:  # noqa: D401
        _ = (width, max_available_height, wrap_lines, get_line_prefix)
        return None

    def is_focusable(self) -> bool:  # noqa: D401
        return True

    def create_content(self, width: int, height: int) -> UIContent:  # noqa: D401
        viewer = self._viewer
        recorder = self._recorder if self._recorder and self._recorder.enabled else None

        move_controller = getattr(self._apply_pending_moves, "__self__", None)
        base_steps = (
            max(1, int(getattr(move_controller, "_max_steps_per_frame", 1)))
            if move_controller is not None
            else 1
        )
        pending_before = (
            abs(int(getattr(move_controller, "_pending_row_delta", 0)))
            if move_controller is not None
            else 0
        )
        previous_direction = self._last_move_direction
        burst_multiplier = self._compute_burst_multiplier(
            pending_before, base_steps, previous_direction
        )

        budget_plan = self._budget_guard.plan_frame(viewer)
        if burst_multiplier > getattr(budget_plan, "coalesce_multiplier", 1.0):
            budget_plan = replace(budget_plan, coalesce_multiplier=burst_multiplier)
        self._current_budget_plan = budget_plan
        previous_theme_epoch = self._current_theme_epoch
        self._current_theme_epoch = theme_epoch()
        if previous_theme_epoch != self._current_theme_epoch:
            self._recorded_style_epoch = None
        if self._apply_budget_plan is not None:
            self._apply_budget_plan(budget_plan)
        if budget_plan.overscan_hint is not None:
            with suppress(Exception):
                viewer.request_frame_budget_overscan(budget_plan.overscan_hint)

        direction, _total_steps, coalesced_steps = self._apply_pending_moves_with_coalesce(
            budget_plan,
            previous_direction,
            base_steps,
            move_controller,
        )
        self._poll_background_jobs()
        overscan_rows = self._maybe_prime_overscan(
            viewer,
            height,
            budget_plan,
            direction,
            previous_direction,
            move_controller,
        )

        perf_ctx = (
            recorder.perf_timer(
                "render.table",
                payload={"context": "tui", "trigger": "refresh"},
            )
            if recorder
            else nullcontext()
        )

        render_start = perf_counter()
        with perf_ctx:
            plan, plan_cache_hit = self._get_plan(viewer, width, height)
            rendered, line_stats = self._render_lines(plan, height)
        render_end = perf_counter()

        status_ctx = (
            recorder.perf_timer(
                "render.status",
                payload={"context": "tui", "trigger": "refresh"},
            )
            if recorder
            else nullcontext()
        )
        status_fragments: StyleAndTextTuples = []
        with status_ctx:
            status_fragments = render_status_line(viewer)
        self._set_status(status_fragments)
        viewer.acknowledge_status_rendered()
        status_text = "".join(fragment for _, fragment in status_fragments)

        if recorder:
            state_snapshot = viewer_state_snapshot(viewer)
            recorder.record_state(state_snapshot)
            if status_text:
                recorder.record_status(status_text)

        if recorder:
            self._maybe_record_line_styles(rendered, recorder)

        fragments: list[StyleAndTextTuples] = [line.fragments for line in rendered]
        plain_lines = [line.plain_text for line in rendered]

        cursor_position = self._locate_cursor(rendered)

        content = UIContent(
            get_line=lambda line_index: fragments[line_index],
            line_count=len(fragments),
            cursor_position=cursor_position,
            show_cursor=True,
        )

        paint_end = perf_counter()

        if recorder and not budget_plan.is_default():
            recorder.record(
                "render_budget",
                {
                    "avg_ms": self._budget_guard.average_ms,
                    "render_ms": (render_end - render_start) * 1000,
                    "paint_ms": (paint_end - render_end) * 1000,
                },
            )

        self._budget_guard.record_frame(
            (render_end - render_start) * 1000,
            (paint_end - render_end) * 1000,
        )

        if recorder:
            frame_lines = plain_lines[:]
            if status_text:
                frame_lines.append(status_text)
            frame_capture = "\n".join(frame_lines)
            recorder.record_frame(
                frame_text=frame_capture,
                frame_hash=frame_hash(frame_capture),
            )
            total_bytes = sum(len(line) for line in plain_lines)
            recorder.record(
                "render_stats",
                {
                    "component": "table_control",
                    "lines": len(rendered),
                    "rendered_lines": line_stats["rendered"],
                    "reused_lines": line_stats["reused"],
                    "plan_cache": "hit" if plan_cache_hit else "miss",
                    "plain_bytes": total_bytes,
                    "coalesced_steps": coalesced_steps,
                    "overscan_rows": overscan_rows,
                },
            )

        self._last_plan_cache_hit = plan_cache_hit
        self._last_frame_finished_at = paint_end
        self._last_coalesced_steps = coalesced_steps
        self._last_overscan_rows = overscan_rows

        try:
            return content
        finally:
            self._current_budget_plan = _BudgetPlan()
            if self._apply_budget_plan is not None:
                self._apply_budget_plan(_BudgetPlan())

    def mouse_handler(self, mouse_event: MouseEvent) -> NotImplementedOrNone:  # noqa: D401
        """Translate mouse wheel events into queued viewer moves."""

        if mouse_event.event_type not in {
            MouseEventType.SCROLL_DOWN,
            MouseEventType.SCROLL_UP,
        }:
            return NotImplemented

        controller = getattr(self._apply_pending_moves, "__self__", None)
        if controller is None:
            return NotImplemented

        queue_move = getattr(controller, "_queue_move", None)
        refresh = getattr(controller, "refresh", None)
        if queue_move is None or refresh is None:
            return NotImplemented

        direction = 1 if mouse_event.event_type == MouseEventType.SCROLL_DOWN else -1
        if MouseModifier.CONTROL in mouse_event.modifiers:
            queue_move(dc=direction)
        else:
            queue_move(dr=direction)

        refresh()
        return None

    def _render_lines(
        self, plan: ViewportPlan, height: int
    ) -> tuple[list[_LineRender], dict[str, int]]:
        column_widths = [max(1, column.width) for column in plan.columns] or [1]
        frozen_boundary = plan.frozen_boundary_idx
        column_overflows = compute_column_overflows(plan.columns, plan.rows > 0)
        column_widths_key = tuple(column_widths)
        column_overflows_key = tuple(column_overflows)
        cache_hits = 0
        cache_misses = 0
        used_keys: set[LineCacheKey] = set()
        highlight_top_blank, highlight_bottom_blank = determine_blank_line_highlights(plan)

        def _cache_lookup(key: LineCacheKey, builder: Callable[[], _LineRender]) -> _LineRender:
            nonlocal cache_hits, cache_misses
            cached = self._line_cache.get(key)
            if cached is not None:
                cache_hits += 1
                used_keys.add(key)
                return cached
            cache_misses += 1
            line = builder()
            self._line_cache[key] = line
            used_keys.add(key)
            return line

        def _blank_line(
            *, header: bool = False, row_active: bool = False, include_boundary: bool = True
        ) -> _LineRender:
            key = self._blank_line_key(
                column_widths_key,
                frozen_boundary,
                column_overflows_key,
                header=header,
                row_active=row_active,
                include_boundary=include_boundary,
            )
            return _cache_lookup(
                key,
                lambda: self._to_line_render(
                    build_blank_line(
                        column_widths,
                        frozen_boundary,
                        column_overflows,
                        header=header,
                        column_plans=plan.columns,
                        row_active=row_active,
                        include_boundary=include_boundary,
                    )
                ),
            )

        lines: list[_LineRender] = []

        table_height = max(0, height - 1)
        has_header = bool(plan.cells and plan.cells[0] and plan.cells[0][0].role == "header")
        body_rows = plan.cells[1:] if has_header else plan.cells
        drop_borders = self._current_budget_plan.drop_borders
        include_boundary = not drop_borders or plan.frozen_boundary_idx is not None

        if table_height > 0:
            lines.append(
                _blank_line(
                    header=has_header,
                    row_active=highlight_top_blank,
                    include_boundary=False,
                )
            )

        if has_header:
            header_cells = plan.cells[0]
            header_key = self._row_line_key(
                header_cells,
                column_widths_key,
                column_overflows_key,
                frozen_boundary,
                is_header=True,
                include_boundary=include_boundary,
                overflow_left=plan.has_left_overflow,
                overflow_right=plan.has_right_overflow,
            )
            lines.append(
                _cache_lookup(
                    header_key,
                    lambda cells=header_cells: self._to_line_render(
                        apply_overflow_indicators(
                            build_row_line(
                                cells,
                                column_widths,
                                frozen_boundary,
                                column_overflows,
                                is_header=True,
                                row_active=False,
                                column_plans=plan.columns,
                                include_boundary=include_boundary,
                            ),
                            show_left=plan.has_left_overflow,
                            show_right=plan.has_right_overflow,
                            is_header=True,
                        )
                    ),
                )
            )
            if body_rows:
                sep_key = self._separator_line_key(
                    column_widths_key,
                    frozen_boundary=frozen_boundary if include_boundary else None,
                )
                lines.append(
                    _cache_lookup(
                        sep_key,
                        lambda: self._to_line_render(
                            build_separator_line(
                                column_widths,
                                frozen_boundary=frozen_boundary if include_boundary else None,
                            )
                        ),
                    )
                )

        for row in body_rows:
            row_key = self._row_line_key(
                row,
                column_widths_key,
                column_overflows_key,
                frozen_boundary,
                is_header=False,
                include_boundary=include_boundary,
            )
            lines.append(
                _cache_lookup(
                    row_key,
                    lambda row=row: self._to_line_render(
                        build_row_line(
                            row,
                            column_widths,
                            frozen_boundary,
                            column_overflows,
                            is_header=False,
                            column_plans=plan.columns,
                            include_boundary=include_boundary,
                        )
                    ),
                )
            )

        if height > 0:
            lines.append(_blank_line(row_active=highlight_bottom_blank, include_boundary=False))

        stats = {"reused": cache_hits, "rendered": cache_misses}
        current_cache = self._line_cache
        self._line_cache = {key: current_cache[key] for key in used_keys if key in current_cache}
        return lines, stats

    def _locate_cursor(self, lines: list[_LineRender]) -> Point:
        line_index = 0
        cursor_x = 0
        for idx, line in enumerate(lines):
            cx = getattr(line, "cursor_x", None)
            if cx is not None:
                line_index = idx
                cursor_x = cx
                break
        return Point(x=cursor_x, y=line_index)

    def _to_line_render(self, line: RenderedLine) -> _LineRender:
        fragments: StyleAndTextTuples = []
        for segment in line.segments:
            style = self._style_from_classes(segment.classes)
            fragments.append((style, segment.text))
        return _LineRender(fragments, line.plain_text, line.cursor_x, line)

    def _style_from_classes(self, classes: Sequence[str]) -> str:
        filtered = self._filter_classes(classes)
        if not filtered:
            return ""
        resolver = get_active_style_resolver()
        style = resolver.prompt_toolkit_style_for_classes(filtered)
        return style or ""

    def _filter_classes(self, classes: Sequence[str]) -> tuple[str, ...]:
        if not self._current_budget_plan.minimal_styles:
            return tuple(classes)

        essential = {
            "table",
            "table.header",
            "table.cell",
            "table.cell.null",
            "table.row.active",
            "table.row.selected",
            "table.row.selected.active",
            "table.cell.active",
            "table.col.active",
            "table.header.active",
            "table.header.sorted",
            "table.separator",
            "table.separator.active",
            "table.overflow_indicator",
        }
        return tuple(cls for cls in classes if cls in essential)

    def _maybe_record_line_styles(self, lines: Sequence[_LineRender], recorder: Recorder) -> None:
        if self._recorded_style_epoch == self._current_theme_epoch:
            return

        resolver = get_active_style_resolver()
        captured: list[dict[str, Any]] = []

        for index, line in enumerate(lines):
            source = line.source
            if source is None:
                continue
            if not any("table.header" in segment.classes for segment in source.segments):
                continue

            segments_payload: list[dict[str, Any]] = []
            for segment in source.segments:
                components = resolver.resolve(segment.classes)
                segments_payload.append(
                    {
                        "text": segment.text,
                        "classes": list(segment.classes),
                        "foreground": components.foreground,
                        "background": components.background,
                        "extras": list(components.extras),
                    }
                )

            if segments_payload:
                captured.append(
                    {
                        "line_index": index,
                        "plain_text": source.plain_text,
                        "segments": segments_payload,
                    }
                )
            break

        if not captured:
            return

        recorder.record_render_line_styles(
            component="table_control",
            lines=captured,
            metadata={"theme_epoch": self._current_theme_epoch},
        )
        self._recorded_style_epoch = self._current_theme_epoch

    def _get_plan(self, viewer: Viewer, width: int, height: int) -> tuple[ViewportPlan, bool]:
        key_hint = self._make_plan_key(viewer, width, height)
        if self._cached_plan is not None and self._plan_cache_key == key_hint:
            return self._cached_plan, True

        plan = compute_viewport_plan(viewer, width, height)
        epoch = self._current_epoch(viewer)
        selection_epoch = getattr(viewer, "selection_epoch", None)
        view_id = self._view_identity(viewer)
        self._cached_plan = plan
        self._plan_cache_key = (
            view_id,
            plan.row_offset,
            plan.col_offset,
            width,
            height,
            epoch,
            getattr(viewer, "cur_row", 0),
            getattr(viewer, "cur_col", 0),
            selection_epoch,
            self._current_theme_epoch,
        )
        # Column level cache must be invalidated when plan changes.
        self._line_cache = {}
        return plan, False

    def _make_plan_key(self, viewer: Viewer, width: int, height: int) -> PlanCacheKey:
        view_id = self._view_identity(viewer)
        row_offset = self._estimate_row_offset(viewer)
        col_offset = max(0, getattr(viewer, "col0", 0))
        epoch = self._current_epoch(viewer)
        cur_row = getattr(viewer, "cur_row", 0)
        cur_col = getattr(viewer, "cur_col", 0)
        theme_ep = getattr(self, "_current_theme_epoch", theme_epoch())
        selection_epoch = getattr(viewer, "selection_epoch", None)
        return (
            view_id,
            row_offset,
            col_offset,
            width,
            height,
            epoch,
            cur_row,
            cur_col,
            selection_epoch,
            theme_ep,
        )

    def _estimate_row_offset(self, viewer: Viewer) -> int:
        row0 = max(0, getattr(viewer, "row0", 0))
        frozen_rows = getattr(viewer, "visible_frozen_row_count", 0)
        if isinstance(frozen_rows, int) and frozen_rows > 0:
            row0 = max(row0, frozen_rows)
        return row0

    def _current_epoch(self, viewer: Viewer) -> Any:
        sheet = getattr(viewer, "sheet", None)
        if sheet is not None:
            version = getattr(sheet, "cache_version", None)
            if version is not None:
                return version
        generation_getter = getattr(viewer, "job_generation", None)
        if callable(generation_getter):
            try:
                return generation_getter()
            except Exception:  # pragma: no cover - defensive
                return None
        return None

    def _view_identity(self, viewer: Viewer) -> Any:
        sheet_id = getattr(viewer, "sheet_id", None)
        if sheet_id is not None:
            return sheet_id
        return id(viewer)

    def _invalidate_cache(self) -> None:
        self._cached_plan = None
        self._plan_cache_key = None
        self._line_cache = {}

    def _row_line_key(
        self,
        cells: list[Cell],
        column_widths: tuple[int, ...],
        column_overflows: tuple[bool, ...],
        frozen_boundary: int | None,
        *,
        is_header: bool,
        include_boundary: bool,
        overflow_left: bool = False,
        overflow_right: bool = False,
    ) -> LineCacheKey:
        cell_key: tuple[Any, ...] = tuple(
            (
                cell.text,
                cell.active_row,
                cell.active_col,
                cell.active_cell,
                getattr(cell, "selected_row", False),
                cell.role,
            )
            for cell in cells
        )
        return (
            "row",
            is_header,
            include_boundary,
            column_widths,
            frozen_boundary,
            column_overflows,
            cell_key,
            overflow_left,
            overflow_right,
            self._current_theme_epoch,
            self._current_budget_plan.minimal_styles,
            self._current_budget_plan.drop_borders,
        )

    def _blank_line_key(
        self,
        column_widths: tuple[int, ...],
        frozen_boundary: int | None,
        column_overflows: tuple[bool, ...],
        *,
        header: bool,
        row_active: bool,
        include_boundary: bool,
    ) -> LineCacheKey:
        return (
            "blank",
            header,
            row_active,
            column_widths,
            frozen_boundary,
            column_overflows,
            include_boundary,
            self._current_theme_epoch,
            self._current_budget_plan.minimal_styles,
            self._current_budget_plan.drop_borders,
        )

    def _separator_line_key(
        self, column_widths: tuple[int, ...], *, frozen_boundary: int | None
    ) -> LineCacheKey:
        return (
            "separator",
            column_widths,
            frozen_boundary,
            self._current_theme_epoch,
            self._current_budget_plan.drop_borders,
        )

    def _apply_pending_moves_with_coalesce(
        self,
        budget_plan: _BudgetPlan,
        previous_direction: int,
        base_steps: int,
        controller: Any | None,
    ) -> tuple[int, int, int]:
        viewer = self._viewer
        before_row = getattr(viewer, "cur_row", 0)

        self._apply_pending_moves()

        after_row = getattr(viewer, "cur_row", before_row)
        delta = after_row - before_row
        direction = 0
        if delta > 0:
            direction = 1
        elif delta < 0:
            direction = -1
        consumed = abs(delta)
        total_moved = consumed
        coalesced = 0

        if (
            direction != 0
            and controller is not None
            and self._is_previous_frame_hot(previous_direction)
        ):
            pending_remaining = getattr(controller, "_pending_row_delta", 0)
            pending_same_dir = (
                max(0, int(pending_remaining)) if direction > 0 else max(0, -int(pending_remaining))
            )
            if pending_same_dir > 0:
                multiplier = float(getattr(budget_plan, "coalesce_multiplier", 1.0) or 1.0)
                multiplier = min(4.0, max(1.0, multiplier))
                max_allowed = max(base_steps, int(round(base_steps * multiplier)))
                remaining_budget = max(0, max_allowed - consumed)
                if remaining_budget > 0:
                    move_fn = getattr(viewer, "move_down" if direction > 0 else "move_up", None)
                    if callable(move_fn):
                        before_extra_row = after_row
                        move_fn(min(pending_same_dir, remaining_budget))
                        new_row = getattr(viewer, "cur_row", before_extra_row)
                        actual_extra = new_row - after_row if direction > 0 else after_row - new_row
                        actual_extra = max(0, actual_extra)
                        if actual_extra > 0:
                            total_moved += actual_extra
                            coalesced = actual_extra
                            if direction > 0:
                                with suppress(Exception):
                                    controller._pending_row_delta = max(
                                        0,
                                        int(getattr(controller, "_pending_row_delta", 0))
                                        - actual_extra,
                                    )
                            else:
                                with suppress(Exception):
                                    controller._pending_row_delta = min(
                                        0,
                                        int(getattr(controller, "_pending_row_delta", 0))
                                        + actual_extra,
                                    )

        if total_moved > 0:
            self._last_move_direction = direction
            self._last_move_time = perf_counter()
        else:
            self._last_move_direction = 0
        self._last_coalesced_steps = coalesced
        return direction, total_moved, coalesced

    def _compute_burst_multiplier(
        self, pending_rows: int, base_steps: int, previous_direction: int
    ) -> float:
        if base_steps <= 0:
            return 1.0
        if pending_rows <= base_steps:
            return 1.0
        if not self._is_previous_frame_hot(previous_direction):
            return 1.0
        blocks = (pending_rows + base_steps - 1) // base_steps
        extra = max(0, min(3, blocks - 1))
        if extra <= 0:
            return 1.0
        return 1.0 + float(extra)

    def _is_previous_frame_hot(self, previous_direction: int) -> bool:
        if previous_direction == 0:
            return False
        last_finish = self._last_frame_finished_at
        if last_finish is None:
            return False
        return (perf_counter() - last_finish) <= self._coalesce_hot_window

    def _maybe_prime_overscan(
        self,
        viewer: Viewer,
        height: int,
        budget_plan: _BudgetPlan,
        direction: int,
        previous_direction: int,
        controller: Any | None,
    ) -> int:
        max_extra_from_budget: int | None = None
        if budget_plan.overscan_hint is not None:
            try:
                hint_value = int(budget_plan.overscan_hint)
            except (TypeError, ValueError):  # pragma: no cover - defensive
                hint_value = 0
            body_height = max(0, height - 1)
            max_extra_from_budget = max(0, hint_value - body_height)
        hot_motion = self._is_previous_frame_hot(previous_direction)
        if not hot_motion:
            # Allow immediate same-direction scrolls even if the previous frame fell
            # outside the hot window (e.g. under CI load) so overscan still primes.
            same_direction = direction != 0 and direction == previous_direction
            if not same_direction:
                return 0
        if direction == 0:
            pending = (
                abs(int(getattr(controller, "_pending_row_delta", 0)))
                if controller is not None
                else 0
            )
            if pending <= 0:
                return 0
        body_height = max(0, height - 1)
        if body_height <= 0:
            return 0
        overscan_rows = int(body_height * self._overscan_ratio)
        if overscan_rows <= 0 and body_height > 0:
            overscan_rows = 1
        overscan_rows = min(overscan_rows, body_height * 3)
        if max_extra_from_budget is not None:
            overscan_rows = min(overscan_rows, max_extra_from_budget)
        if overscan_rows <= 0:
            return 0
        columns = self._visible_column_names(viewer)
        if not columns:
            return 0
        try:
            viewer.get_visible_table_slice(columns, overscan_hint=body_height + overscan_rows)
        except Exception:  # pragma: no cover - defensive
            return 0
        return overscan_rows

    def _visible_column_names(self, viewer: Viewer) -> list[str]:
        columns = getattr(viewer, "visible_cols", None)
        if columns:
            return list(columns)
        columns = getattr(viewer, "columns", None)
        if columns:
            return list(columns)
        return []

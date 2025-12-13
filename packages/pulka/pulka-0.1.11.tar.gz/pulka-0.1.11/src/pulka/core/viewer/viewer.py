"""Viewer state management for Pulka.

The heavy lifting is delegated to small helper components housed in
``plan_controller``, ``row_count_tracker`` and ``state``. ``Viewer`` now wires
those helpers together while exposing a stable orchestration surface for the
rest of the application.
"""

from __future__ import annotations

import contextlib
import math
import weakref
from collections import deque
from collections.abc import Callable, Hashable, Mapping, Sequence
from time import monotonic_ns
from typing import TYPE_CHECKING, Any, Literal

import polars as pl

from ...config.settings import STREAMING_DEFAULTS
from ...data.filter_lang import compile_filter_expression
from ...sheets.data_sheet import DataSheet
from ...sheets.transformation_history import (
    SupportsSnapshots,
    TransformationHistory,
    TransformationSnapshot,
)
from ...testing import is_test_mode
from ..engine.contracts import TableSlice
from ..engine.viewer_engine import ViewerEngine
from ..errors import (
    CancelledError,
    CompileError,
    MaterializeError,
    PlanError,
    PulkaCoreError,
)
from ..interfaces import JobRunnerProtocol
from ..plan import QueryPlan
from ..plan_ops import FilterMode
from ..plan_ops import clear_sort as plan_clear_sort
from ..plan_ops import reset as plan_reset
from ..plan_ops import set_filter as plan_set_filter
from ..plan_ops import set_projection as plan_set_projection
from ..plan_ops import set_sql_filter as plan_set_sql_filter
from ..plan_ops import toggle_sort as plan_toggle_sort
from ..row_provider import RowProvider
from ..sheet import SHEET_FEATURE_PLAN, sheet_supports
from .components import ColumnWidthController, FreezePaneController, RowCacheController
from .plan_controller import PlanController
from .row_count_tracker import RowCountTracker
from .search import SearchController
from .selection import SelectionController
from .snapshot_builder import build_public_state
from .state import ViewerSnapshot, ViewerStateController
from .terminal import (
    acknowledge_status_rendered,
    configure_terminal,
    is_status_dirty,
    mark_status_dirty,
    set_status_width_override,
    set_view_width_override,
)
from .transformation_manager import ChangeResult, ViewerTransformationManager
from .types import ViewerPublicState
from .ui_hooks import NullViewerUIHooks, ViewerUIHooks

type VisibleCacheKey = (
    tuple[int, int, int, int | None, tuple[str, ...], tuple[int, ...], tuple[int, ...]] | None
)


def build_filter_expr_for_values(column_name: str, values: Sequence[object]) -> str:
    """Return a filter expression that matches any of ``values`` for ``column_name``."""

    seen: set[tuple[object, type[object]]] = set()
    unique: list[object] = []
    for value in values:
        try:
            key = (value, type(value))
            hash(key)
        except Exception:
            key = (repr(value), type(value))
        if key in seen:
            continue
        seen.add(key)
        unique.append(value)

    if not unique:
        msg = "no values provided"
        raise ValueError(msg)

    def _format_value(val: object) -> str:
        if isinstance(val, float) and math.isnan(val):
            return "float('nan')"
        if val is None:
            return "None"
        return repr(val)

    formatted = [_format_value(val) for val in unique]
    col_expr = f"c.{column_name}" if column_name.isidentifier() else f"c[{repr(column_name)}]"

    if len(formatted) == 1:
        raw = unique[0]
        if raw is None:
            return f"{col_expr}.is_null()"
        return f"{col_expr}.eq({formatted[0]})"

    values_expr = ", ".join(formatted)
    return f"{col_expr}.is_in([{values_expr}])"


if TYPE_CHECKING:
    from ...api.session import Session
    from ..sheet import Sheet
else:
    Sheet = object
    Session = object


class Viewer:
    def __init__(
        self,
        sheet: Sheet,
        *,
        viewport_rows: int | None = None,
        viewport_cols: int | None = None,
        source_path: str | None = None,
        session: Session | None = None,
        row_provider: RowProvider | None = None,
        ui_hooks: ViewerUIHooks | None = None,
        runner: JobRunnerProtocol,
    ):
        self.sheet = sheet
        self.columns: list[str] = list(sheet.columns)
        self._schema_cache = getattr(sheet, "schema", {})
        self._source_path = source_path
        self._session_ref: weakref.ReferenceType[Session] | None = (
            weakref.ref(session) if session is not None else None
        )
        self._runner: JobRunnerProtocol = runner

        # Cursor & viewport
        self.cur_row = 0
        self.cur_col = 0
        self.row0 = 0
        self.col0 = 0
        self._total_rows: int | None = None
        self._row_count_stale: bool = True
        self._row_count_future = None
        self._row_count_display_pending: bool = False
        self._max_visible_col: int | None = None  # Limit rightmost visible column when set
        self._status_dirty: bool = False
        self._status_message: str | None = None

        # Terminal metrics
        self._viewport_rows_override = viewport_rows
        self._viewport_cols_override = viewport_cols
        # Column width heuristics - sample-based dynamic allocation
        self._min_col_width = 4
        preferred_compact = getattr(sheet, "compact_width_layout", None)
        if preferred_compact is None:
            self._compact_width_layout = isinstance(sheet, DataSheet)
        else:
            self._compact_width_layout = bool(preferred_compact)
        self._default_col_width_cap = 25 if self._compact_width_layout else 20
        self._sep_overhead = 3
        # Column hiding functionality
        self._hidden_cols: set[str] = set()  # effective hidden column names
        self._local_hidden_cols: set[str] = set()  # legacy cache when no plan is present

        self._view_width_override_chars: int | None = None
        self._status_width_override_chars: int | None = None
        self.view_width_chars: int = 80
        self.status_width_chars: int = 80
        self.view_height: int = 0

        # Controllers for modular responsibilities
        self._streaming_enabled_default = STREAMING_DEFAULTS.enabled
        self._streaming_batch_rows_default = STREAMING_DEFAULTS.batch_rows

        self._freeze = FreezePaneController(self)
        self._row_cache = RowCacheController(
            self,
            self._freeze,
            streaming_enabled=self._streaming_enabled_default,
            streaming_batch_rows=self._streaming_batch_rows_default,
        )
        self._widths = ColumnWidthController(self)
        self._stretch_last_for_slack = False

        # UI integration bridge (prompt_toolkit, headless, etc.).
        self._ui_hooks: ViewerUIHooks = ui_hooks or NullViewerUIHooks()

        provider = row_provider or getattr(sheet, "row_provider", None)
        if provider is None:
            provider = RowProvider.for_sheet(sheet, runner=self._runner)
        elif getattr(provider, "_runner", None) is None:
            with contextlib.suppress(Exception):
                provider._runner = self._runner
        self._row_provider = provider
        self._engine = ViewerEngine(self._row_provider)

        self._header_widths = self._compute_initial_column_widths()
        self._default_header_widths = list(self._header_widths)  # baseline to revert to
        self._width_mode: Literal["default", "single", "all"] = "default"
        self._width_target: int | None = None
        self._width_cache_all: list[int] | None = None
        self._width_cache_single: dict[int, int] = {}
        self._autosized_widths: dict[int, int] = {}
        self._sticky_column_widths: dict[str, int] = {}
        self._decimal_alignment_cache: dict[str, tuple[int, int]] = {}
        self._partial_column_index: int | None = None
        self._has_partial_column: bool = False

        self._state = ViewerStateController(self)
        self._transformations = self._create_transformation_manager(sheet)
        self._row_counts = RowCountTracker(self, runner=self._runner)
        self._selection = SelectionController(
            self,
            row_provider=self._row_provider,
            row_counts=self._row_counts,
            transformations=self._transformations,
        )
        self._search = SearchController(self)
        self._plan_controller = PlanController(self)

        self.update_terminal_metrics()
        # Cache for visible columns calculation
        self._visible_key: VisibleCacheKey = None
        self._visible_cols_cached: list[str] = self.columns[:1] if self.columns else []
        self._aligning_active_column: bool = False

        # Row velocity tracking for adaptive overscan
        self._row0_velocity_samples: deque[tuple[int, int]] = deque(maxlen=6)
        self._last_row0_sample: int = self.row0
        self._last_row0_ns: int | None = None
        self._last_velocity_event_ns: int | None = None
        self._local_filter_text: str | None = None
        self._local_filter_kind: Literal["expr", "sql"] | None = None
        self.is_freq_view: bool = False
        self.freq_source_col: str | None = None
        # Histogram: track whether this viewer hosts the numeric histogram sheet.
        self.is_hist_view: bool = False
        self._perf_callback: Callable[[str, float, dict[str, Any]], None] | None = None

        # Track the viewer's position within the sheet stack (0 = root dataset).
        self.stack_depth: int = 0
        self._frame_budget_overscan_hint: int | None = None

        self._apply_sheet_freeze_defaults(sheet)
        self._apply_file_browser_layout_defaults(sheet)
        self._clear_last_search()
        self._sync_hidden_columns_from_plan()

    @property
    def sheet_id(self) -> str | None:
        """Expose the sheet identifier when available."""

        return getattr(self.sheet, "sheet_id", None)

    @property
    def job_runner(self) -> JobRunnerProtocol:
        return self._runner

    @property
    def row_provider(self) -> RowProvider:
        """Return the service responsible for fetching row slices."""

        return self._row_provider

    @property
    def engine(self) -> ViewerEngine:
        """Return the viewer engine responsible for data access."""

        return self._engine

    @property
    def state_controller(self) -> ViewerStateController:
        """Expose the controller that manages cursor and viewport state."""

        return self._state

    @property
    def plan_controller(self) -> PlanController:
        """Expose the controller that manages query plan mutations."""

        return self._plan_controller

    @property
    def row_count_tracker(self) -> RowCountTracker:
        """Expose the tracker responsible for refreshing row counts."""

        return self._row_counts

    def job_generation(self) -> int:
        """Return the sheet generation tracked by the job runner."""

        context = getattr(self.sheet, "job_context", None)
        if context is None:
            return 0
        _, generation, _ = context()
        try:
            return int(generation)
        except Exception:
            return 0

    def plan_hash(self) -> str | None:
        """Return the current plan hash for job coalescing."""

        context = getattr(self.sheet, "job_context", None)
        if context is None:
            return None
        _, _, plan_hash = context()
        return plan_hash if isinstance(plan_hash, str) else None

    def _current_plan(self) -> QueryPlan | None:
        """Return the current plan object when available."""

        return self._plan_controller.current_plan()

    def _plan_projection_columns(self) -> tuple[str, ...] | None:
        """Return the active plan projection constrained to known columns."""

        plan = self._current_plan()
        if not isinstance(plan, QueryPlan):
            return None

        projection = plan.projection_or(self.columns)
        if not projection:
            return tuple(self.columns)

        known = set(self.columns)
        return tuple(name for name in projection if name in known)

    def _plan_compiler_for_validation(self) -> Any:
        """Return a plan compiler suitable for validating plan mutations."""

        return self._plan_controller.plan_compiler_for_validation()

    @property
    def session(self) -> Session | None:
        """Return the owning session when available."""

        if self._session_ref is None:
            return None
        return self._session_ref()

    @property
    def ui_hooks(self) -> ViewerUIHooks:
        """Return the UI hook bridge active for this viewer."""

        return self._ui_hooks

    def set_ui_hooks(self, hooks: ViewerUIHooks | None) -> None:
        """Swap the active UI hooks and refresh terminal metrics."""

        self._ui_hooks = hooks or NullViewerUIHooks()
        with contextlib.suppress(Exception):
            self.update_terminal_metrics()

    @property
    def schema(self) -> dict[str, pl.DataType]:
        """Expose the current schema, delegating to the underlying sheet."""
        schema = getattr(self.sheet, "schema", None)
        if schema is None:
            return {}
        if not isinstance(schema, Mapping):
            return {}
        typed_schema = dict(schema)
        self._schema_cache = typed_schema
        return typed_schema

    @property
    def filter_kind(self) -> Literal["expr", "sql"] | None:
        """Return the kind of active filter tracked by the current plan."""

        plan = self._current_plan()
        if plan is None:
            return self._local_filter_kind
        has_expr = any(clause.kind == "expr" for clause in plan.filter_clauses)
        has_sql = any(clause.kind == "sql" for clause in plan.filter_clauses)
        if has_expr:
            return "expr"
        if has_sql:
            return "sql"
        return None

    @property
    def filter_text(self) -> str | None:
        """Return the human readable filter description for the active plan."""

        plan = self._current_plan()
        if plan is None:
            return self._local_filter_text
        return plan.combined_filter_text()

    @filter_text.setter
    def filter_text(self, value: str | None) -> None:
        self._local_filter_text = value
        self._local_filter_kind = None
        if value is not None:
            prefix = "SQL WHERE "
            self._local_filter_kind = "sql" if value.startswith(prefix) else "expr"

    @property
    def filters(self) -> tuple[object, ...]:
        """Return the ordered filter clauses tracked by the active plan."""

        plan = self._current_plan()
        if plan is None:
            return ()
        return tuple(plan.filter_clauses)

    @property
    def sql_filter_text(self) -> str | None:
        """Return the raw SQL WHERE clause when an SQL filter is active."""

        plan = self._current_plan()
        if plan is None:
            if self._local_filter_kind == "sql" and self._local_filter_text:
                prefix = "SQL WHERE "
                if self._local_filter_text.startswith(prefix):
                    return self._local_filter_text[len(prefix) :]
                return self._local_filter_text
            return None
        return plan.sql_filter

    @property
    def search_text(self) -> str | None:
        """Return the active search text tracked by the plan when available."""

        return self._search.search_text

    @search_text.setter
    def search_text(self, value: str | None) -> None:
        self._search.search_text = value

    @property
    def sort_col(self) -> str | None:
        """Expose the primary sort column derived from the current plan."""

        plan = self._current_plan()
        if plan is None or not plan.sort:
            return None
        return plan.sort[0][0]

    @property
    def sort_asc(self) -> bool:
        """Expose whether the primary sort column is ascending."""

        plan = self._current_plan()
        if plan is None or not plan.sort:
            return True
        return not plan.sort[0][1]

    def set_perf_callback(
        self,
        callback: Callable[[str, float, dict[str, Any]], None] | None,
    ) -> None:
        """Register a lightweight perf callback for internal hotspots."""
        self._perf_callback = callback

    def _record_perf_event(
        self,
        phase: str,
        duration_ms: float,
        payload: dict[str, Any],
    ) -> None:
        if not self._perf_callback:
            return
        with contextlib.suppress(Exception):
            self._perf_callback(phase, duration_ms, payload)

    def invalidate_row_cache(self) -> None:
        """Drop the cached row window used for fast vertical scrolling."""
        self._row_cache.invalidate()

    def _get_row_cache_prefetch(self) -> int:
        return self._row_cache.get_prefetch()

    # ------------------------------------------------------------------
    # Freeze panes helpers

    def _invalidate_frozen_columns_cache(self) -> None:
        self._freeze.invalidate_cache()

    def _apply_sheet_freeze_defaults(self, sheet: Sheet | None = None) -> None:
        target = self.sheet if sheet is None else sheet
        if target is None:
            return

        default_cols = getattr(target, "default_frozen_columns", None)
        if isinstance(default_cols, int) and default_cols >= 0:
            self.set_frozen_columns(default_cols)

        default_rows = getattr(target, "default_frozen_rows", None)
        if isinstance(default_rows, int) and default_rows >= 0:
            self.set_frozen_rows(default_rows)

    def _apply_file_browser_layout_defaults(self, sheet: Sheet | None = None) -> None:
        target = self.sheet if sheet is None else sheet
        if target is None or not getattr(target, "is_file_browser", False):
            return
        if not self.columns:
            return

        self._force_default_width_mode()

    def _ensure_frozen_columns_cache(self) -> None:
        self._freeze.ensure_cache()

    def _frozen_column_indices(self) -> list[int]:
        return self._freeze.column_indices()

    def _first_scrollable_col_index(self) -> int:
        return self._freeze.first_scrollable_col_index()

    def _is_column_frozen(self, idx: int) -> bool:
        return self._freeze.is_column_frozen(idx)

    @property
    def frozen_column_count(self) -> int:
        return self._freeze.column_count

    @property
    def frozen_row_count(self) -> int:
        return self._freeze.row_count

    def _effective_frozen_row_count(self) -> int:
        return self._freeze.effective_row_count()

    def _reserved_frozen_rows(self) -> int:
        """Return how many rows at the top of the viewport are occupied by frozen rows."""

        return self._freeze.reserved_view_rows()

    def _body_view_height(self) -> int:
        """Return how many rows are available for the scrollable body."""

        return self._freeze.body_view_height()

    def _max_row0_for_total(self, total_rows: int) -> int:
        """Return the largest valid ``row0`` for a dataset with ``total_rows`` rows."""

        return self._state.max_row0_for_total(total_rows)

    @property
    def frozen_columns(self) -> list[str]:
        return self._freeze.frozen_column_names()

    def _frozen_column_index_set(self) -> frozenset[int]:
        return self._freeze.column_index_set()

    def _frozen_column_name_set(self) -> frozenset[str]:
        return self._freeze.column_name_set()

    @property
    def visible_row_positions(self) -> list[int]:
        return self._row_cache.visible_row_positions()

    @property
    def visible_frozen_row_count(self) -> int:
        return self._row_cache.visible_frozen_row_count()

    @property
    def selection_epoch(self) -> int:
        """Monotonic token that changes whenever row selection mutates."""

        return self._selection.selection_epoch

    # Selection controller state proxies ------------------------------------------------

    @property
    def _selected_row_ids(self) -> set[Hashable]:
        return self._selection.selected_row_ids

    @_selected_row_ids.setter
    def _selected_row_ids(self, value: set[Hashable]) -> None:
        self._selection.selected_row_ids = value

    @property
    def _selection_filter_expr(self) -> str | None:
        return self._selection.selection_filter_expr

    @_selection_filter_expr.setter
    def _selection_filter_expr(self, value: str | None) -> None:
        self._selection.selection_filter_expr = value

    @property
    def _value_selection_filter(self) -> tuple[str, Any, bool] | None:
        return self._selection.value_selection_filter

    @_value_selection_filter.setter
    def _value_selection_filter(self, value: tuple[str, Any, bool] | None) -> None:
        self._selection.value_selection_filter = value

    @property
    def _uses_row_ids(self) -> bool | None:
        return self._selection.uses_row_ids

    @_uses_row_ids.setter
    def _uses_row_ids(self, value: bool | None) -> None:
        self._selection.uses_row_ids = value

    @property
    def _selection_epoch(self) -> int:
        return self._selection.selection_epoch

    @_selection_epoch.setter
    def _selection_epoch(self, value: int) -> None:
        self._selection.selection_epoch = value

    def _encode_filter_literal(self, value: object) -> str | None:
        return self._selection.encode_filter_literal(value)

    def _value_selection_filter_expr(self) -> str | None:
        return self._selection.value_selection_filter_expr()

    @staticmethod
    def _toggle_inversion_clause(selection_clause: str) -> str:
        return SelectionController.toggle_inversion_clause(selection_clause)

    def _selection_filter_clause(self, plan_columns: Sequence[str]) -> str | None:
        return self._selection.selection_filter_clause(plan_columns)

    def _selection_matches_for_slice(
        self, table_slice: TableSlice, row_positions: Sequence[int] | None
    ) -> set[Hashable] | None:
        """Return row ids matching the selection expression within ``table_slice``."""

        expr_text = self._selection_filter_expr
        if not expr_text:
            return None

        row_id_column = getattr(self.row_provider, "_row_id_column", None)
        columns = list(table_slice.column_names)
        data = {}

        try:
            for column in table_slice.columns:
                data[column.name] = column.values
            if row_id_column and table_slice.row_ids is not None:
                data[row_id_column] = table_slice.row_ids
                if row_id_column not in columns:
                    columns.append(row_id_column)
            df = pl.DataFrame(data)
            expr = compile_filter_expression(expr_text, columns)
            mask = df.select(expr.alias("__match__")).to_series()
        except Exception:
            return None

        matches: set[Hashable] = set()
        for idx, flag in enumerate(mask):
            try:
                matched = bool(flag)
            except Exception:
                matched = False
            if not matched:
                continue
            row_id = self._row_identifier_for_slice(
                table_slice, idx, row_positions=row_positions, absolute_row=None
            )
            if row_id is not None:
                matches.add(row_id)
        return matches

    def _count_plan_rows(self, plan: QueryPlan) -> int | None:
        """Return the row count for ``plan`` without bumping sheet generation."""

        compiler = self.row_provider.build_plan_compiler()
        materializer = getattr(self.row_provider, "_materializer", None)
        if compiler is None or materializer is None:
            compiler = getattr(self.sheet, "_compiler", None)
            materializer = getattr(self.sheet, "_materializer", None)

        if compiler is None or materializer is None:
            return None

        try:
            physical_plan = compiler.compile(plan)
            count = materializer.count(physical_plan)
        except Exception:
            return None

        if count is None:
            return None

        try:
            return int(count)
        except Exception:
            return None

    def _selection_count(self, plan: QueryPlan) -> int | None:
        """Return the number of rows currently selected using a filter-friendly path."""

        return self._selection.selection_count(plan)

    # ------------------------------------------------------------------
    # Row selection helpers

    @staticmethod
    def _coerce_row_identifier(
        candidate: object | None, *, fallback: int | None
    ) -> Hashable | None:
        """Return ``candidate`` when hashable, else ``fallback``."""

        if candidate is None:
            return fallback
        try:
            hash(candidate)
        except Exception:
            return fallback
        return candidate

    def _row_identifier_for_slice(
        self,
        table_slice: TableSlice,
        row_index: int,
        *,
        row_positions: Sequence[int] | None = None,
        absolute_row: int | None = None,
    ) -> Hashable | None:
        """Resolve a stable row identifier for ``row_index`` within ``table_slice``."""

        fallback_abs = absolute_row
        if fallback_abs is None and row_positions and 0 <= row_index < len(row_positions):
            fallback_abs = row_positions[row_index]
        if fallback_abs is None and table_slice.start_offset is not None:
            fallback_abs = table_slice.start_offset + row_index

        row_ids = getattr(table_slice, "row_ids", None)
        if row_ids is not None:
            try:
                candidate = row_ids[row_index]
            except Exception:
                candidate = None
            row_id = self._coerce_row_identifier(candidate, fallback=fallback_abs)
            if row_id is not None:
                return row_id

        if getattr(self.sheet, "is_summary_view", False) and "column" in table_slice.column_names:
            try:
                col_values = table_slice.column("column").values
            except Exception:
                col_values = ()
            if 0 <= row_index < len(col_values):
                candidate = col_values[row_index]
                row_id = self._coerce_row_identifier(candidate, fallback=fallback_abs)
                if row_id is not None:
                    return row_id

        if fallback_abs is not None:
            row_id = self._coerce_row_identifier(fallback_abs, fallback=fallback_abs)
            if row_id is not None:
                return row_id

        signature: Hashable | None = None
        try:
            columns = table_slice.columns
        except Exception:
            columns = ()

        if columns:
            normalized: list[tuple[str, Hashable]] = []
            for column in columns:
                try:
                    value = column.values[row_index]
                except Exception:
                    value = None
                if isinstance(value, float) and math.isnan(value):
                    value = ("__nan__", column.dtype)
                else:
                    try:
                        hash(value)
                    except Exception:
                        value = repr(value)
                normalized.append((column.name, value))
            signature = tuple(normalized)

        if signature:
            return signature

        if row_positions and 0 <= row_index < len(row_positions):
            row_id = self._coerce_row_identifier(row_positions[row_index], fallback=fallback_abs)
            if row_id is not None:
                return row_id

        if table_slice.start_offset is not None:
            row_id = self._coerce_row_identifier(
                table_slice.start_offset + row_index, fallback=fallback_abs
            )
            if row_id is not None:
                return row_id

        return fallback_abs

    def _row_index_for_selection(
        self, *, target_row: int, row_positions: Sequence[int], table_slice: TableSlice
    ) -> int | None:
        return self._selection._row_index_for_selection(
            target_row=target_row, row_positions=row_positions, table_slice=table_slice
        )

    def toggle_row_selection(self) -> None:
        """Toggle selection for the currently focused row."""

        self._selection.toggle_row_selection()

    def _row_ids_need_materialization(self) -> bool:
        return self._selection._row_ids_need_materialization()

    def _detect_row_ids(self) -> bool:
        return self._selection._detect_row_ids()

    def _collect_row_ids(self, total_rows: int) -> set[Hashable]:
        return self._selection._collect_row_ids(total_rows)

    def invert_selection(self) -> None:
        """Invert selection state for all rows."""

        self._selection.invert_selection()

    def _clear_selection_state(self) -> bool:
        """Clear any stored selection without recording history."""

        return self._selection._clear_selection_state()

    def _clear_selection_recorded(self, description: str = "clear selection") -> bool:
        """Clear selection and persist an undo snapshot when changed."""

        return self._selection.clear_selection_recorded(description)

    def clear_row_selection(self) -> None:
        """Clear any selected rows."""

        self._selection.clear_row_selection()

    def _matching_row_ids_for_value(
        self,
        column_name: str,
        target_value: object,
        *,
        is_target_nan: bool,
        plan: Any | None = None,
        total_rows: int | None = None,
    ) -> tuple[set[Hashable], bool]:
        return self._selection.matching_row_ids_for_value(
            column_name,
            target_value,
            is_target_nan=is_target_nan,
            plan=plan,
            total_rows=total_rows,
        )

    def select_matching_value_rows(self) -> None:
        """Select all rows matching the current cell's value in the active column."""

        self._selection.select_matching_value_rows(selection_count_fn=self._selection_count)

    def set_frozen_columns(self, count: int) -> None:
        self._freeze.set_frozen_columns(count)

    def set_frozen_rows(self, count: int) -> None:
        self._freeze.set_frozen_rows(count)

    def clear_freeze(self) -> None:
        self._freeze.clear()

    @property
    def hidden_columns(self) -> list[str]:
        """Return the columns currently hidden from the table."""

        if not self._hidden_cols:
            return []
        hidden: list[str] = []
        hidden_set = self._hidden_cols
        for name in self.columns:
            if name in hidden_set:
                hidden.append(name)
        return hidden

    def _update_row_velocity(self) -> int:
        now_ns = monotonic_ns()
        last_ns = self._last_row0_ns
        last_row0 = self._last_row0_sample
        delta = self.row0 - last_row0 if last_ns is not None else 0

        if last_ns is not None and now_ns > last_ns:
            if delta:
                self._row0_velocity_samples.append((abs(delta), now_ns - last_ns))
                self._last_velocity_event_ns = now_ns
            elif (
                self._last_velocity_event_ns is not None
                and now_ns - self._last_velocity_event_ns > 750_000_000
            ):
                self._row0_velocity_samples.clear()
                self._last_velocity_event_ns = None

        self._last_row0_sample = self.row0
        self._last_row0_ns = now_ns
        return now_ns

    def _estimate_overscan_from_velocity(self, now_ns: int) -> int | None:
        if not self._row0_velocity_samples:
            return None

        last_event = self._last_velocity_event_ns
        if last_event is not None and now_ns - last_event > 750_000_000:
            self._row0_velocity_samples.clear()
            self._last_velocity_event_ns = None
            return None

        total_dt = sum(dt for _, dt in self._row0_velocity_samples)
        if total_dt <= 0:
            return None

        total_delta = sum(delta for delta, _ in self._row0_velocity_samples)
        rows_per_ns = total_delta / total_dt
        if rows_per_ns <= 0:
            return None

        rows_per_second = rows_per_ns * 1_000_000_000
        lookahead_seconds = 0.35
        hint = int(rows_per_second * lookahead_seconds)
        if hint <= 0:
            return None

        max_hint = max(0, self.view_height) * 10 or hint
        return max(0, min(hint, max_hint))

    def get_visible_table_slice(
        self, columns: Sequence[str], overscan_hint: int | None = None
    ) -> TableSlice:
        """Return the current viewport slice as an engine-agnostic table."""

        now_ns = self._update_row_velocity()
        if overscan_hint is None:
            overscan_hint = self._estimate_overscan_from_velocity(now_ns)

        budget_hint = self._frame_budget_overscan_hint
        self._frame_budget_overscan_hint = None
        if budget_hint is not None:
            if overscan_hint is None:
                overscan_hint = budget_hint
            else:
                overscan_hint = min(overscan_hint, budget_hint)

        return self._row_cache.get_visible_table_slice(columns, overscan_hint)

    def request_frame_budget_overscan(self, hint: int | None) -> None:
        """Limit overscan for the next visible slice fetch."""

        if hint is None:
            self._frame_budget_overscan_hint = None
            return
        try:
            value = int(hint)
        except (TypeError, ValueError):  # pragma: no cover - defensive
            self._frame_budget_overscan_hint = None
            return
        self._frame_budget_overscan_hint = max(0, value)

    def get_visible_dataframe(self, columns: Sequence[str]) -> pl.DataFrame:
        """Return the current viewport slice as a Polars DataFrame."""

        table_slice = self.get_visible_table_slice(columns)
        if not table_slice.columns:
            return pl.DataFrame()

        data = {
            column.name: pl.Series(column.name, list(column.values), dtype=column.dtype)
            for column in table_slice.columns
        }
        return pl.DataFrame(data)

    def update_terminal_metrics(self) -> None:
        # Start from actual terminal size via the injected UI hooks.
        prev_width = getattr(self, "view_width_chars", 0)
        prev_height = getattr(self, "view_height", 0)
        prev_prefetch = self._row_cache.prefetch
        prev_status_width = getattr(self, "status_width_chars", None)

        try:
            cols, rows = self._ui_hooks.get_terminal_size((100, 30))
        except Exception:
            cols, rows = NullViewerUIHooks().get_terminal_size((100, 30))

        cols = max(20, cols)
        rows = max(1, rows)

        # Width estimate per column override only affects rendering width hints
        if self._viewport_cols_override is not None:
            cols = max(20, self._viewport_cols_override * 12)

        if (
            is_test_mode()
            and self._status_width_override_chars is None
            and self._view_width_override_chars is None
        ):
            cols = max(20, 100)

        status_width = (
            max(20, self._status_width_override_chars)
            if self._status_width_override_chars is not None
            else cols
        )

        if self._view_width_override_chars is not None:
            cols = max(20, self._view_width_override_chars)
        else:
            cols = status_width

        # Reserve lines for table header, separator, and status bar.
        # Required: header (1) + header separator (1) + empty line before status (1)
        # + status bar (1) + margin (1)
        reserved = 5
        base_view_height = max(1, rows - reserved)
        if self._viewport_rows_override is not None:
            # Never exceed the available height; honor override within bounds.
            view_height = max(1, min(base_view_height, self._viewport_rows_override))
        else:
            view_height = base_view_height
        view_width = max(20, cols)

        self.status_width_chars = status_width
        self.view_height = view_height
        prev_width_chars = getattr(self, "view_width_chars", None)
        self.view_width_chars = view_width
        self._autosized_widths.clear()
        # Re-apply maximize mode widths against the new terminal size
        self._apply_width_mode()

        new_prefetch = max(self.view_height * 4, 64)
        self._row_cache.prefetch = new_prefetch

        prefetch_changed = prev_prefetch is None or new_prefetch != prev_prefetch
        if view_width != prev_width or view_height != prev_height or prefetch_changed:
            self.invalidate_row_cache()
        status_width_changed = prev_status_width is None or prev_status_width != status_width
        if prev_width_chars is None or prev_width_chars != view_width or status_width_changed:
            self.mark_status_dirty()

    def configure_terminal(self, width: int, height: int | None = None) -> None:
        """Configure explicit terminal metrics for deterministic renders."""

        configure_terminal(self, width=width, height=height)

    def set_status_width_override(self, width: int | None) -> None:
        """Force a specific status bar width independently of the table view."""

        set_status_width_override(self, width)

    def set_view_width_override(self, width: int | None) -> None:
        """Force a specific character width for test or headless rendering."""

        set_view_width_override(self, width)

    def mark_status_dirty(self) -> None:
        """Signal that the status bar should be re-rendered."""

        mark_status_dirty(self)

    def acknowledge_status_rendered(self) -> None:
        """Mark the status bar as in sync with the latest render."""

        acknowledge_status_rendered(self)

    def is_status_dirty(self) -> bool:
        """Return whether the status bar needs to be re-rendered."""

        return is_status_dirty(self)

    @property
    def status_message(self) -> str | None:
        """Return the current status message displayed in the footer."""

        return self._status_message

    @status_message.setter
    def status_message(self, message: str | None) -> None:
        """Set the status message and mark the footer dirty if it changed."""

        if message == self._status_message:
            return
        self._status_message = message
        self.mark_status_dirty()

    def clamp(self) -> None:
        """Clamp the cursor and viewport to valid ranges."""

        before = (self.cur_row, self.cur_col, self.row0, self.col0)
        self._state.clamp()
        after = (self.cur_row, self.cur_col, self.row0, self.col0)
        if after != before:
            self.mark_status_dirty()

    def invalidate_row_count(self) -> None:
        """Mark the cached row count as stale."""
        self._row_counts.invalidate()

    def _ensure_total_rows(self) -> int | None:
        """Ensure we have an up-to-date total row count and return it."""
        return self._row_counts.ensure_total_rows()

    def goto_col(self, name: str) -> bool:
        """Move cursor to the column with the given name."""
        try:
            idx = self.columns.index(name)
        except ValueError:
            self.status_message = f"unknown column '{name}'"
            return False

        self.cur_col = idx
        if self.columns[idx] not in self.visible_cols and not self._is_column_frozen(idx):
            self.col0 = idx
        self.clamp()
        return True

    def _create_transformation_manager(self, sheet: Sheet) -> ViewerTransformationManager:
        """Build a transformation manager bound to ``sheet``."""

        sheet_for_history: SupportsSnapshots | None
        if hasattr(sheet, "snapshot_transforms") and hasattr(sheet, "restore_transforms"):
            sheet_for_history = sheet  # type: ignore[assignment]
        else:
            sheet_for_history = None
        return ViewerTransformationManager(
            history=TransformationHistory(sheet_for_history),
            capture_view_state=self._capture_view_state,
            restore_view_state=self._restore_view_state,
        )

    def _apply_plan_update(
        self, description: str, builder: Callable[[QueryPlan], QueryPlan]
    ) -> ChangeResult | None:
        """Apply a pure plan update produced by ``builder``."""

        return self._plan_controller.apply_plan_update(description, builder)

    def _status_from_error(self, operation: str, error: PulkaCoreError) -> None:
        """Format ``error`` into a viewer status message."""

        if isinstance(error, PlanError):
            category = "plan"
        elif isinstance(error, CompileError):
            category = "compile"
        elif isinstance(error, MaterializeError):
            category = "materialize"
        elif isinstance(error, CancelledError):
            category = "cancelled"
        else:
            category = "internal"

        detail = str(error).strip()
        if detail:
            message = f"{operation} {category} error: {detail}"
        else:
            message = f"{operation} {category} error"
        self.status_message = message[:120]

    def toggle_sort(self, col_name: str | None = None) -> None:
        """Toggle sort on the specified column (defaults to current column)."""
        if not self.columns:
            self.status_message = "no columns to sort"
            return

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "sorting not supported"
            return

        target = col_name or self.columns[self.cur_col]
        try:
            result = self._apply_plan_update(
                f"sort {target}", lambda plan: plan_toggle_sort(plan, target)
            )
        except PulkaCoreError as exc:
            self._status_from_error("sort", exc)
            return
        except Exception as exc:
            self.status_message = f"sort error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "sorting not supported"
            return

        if not result.plan_changed:
            self.status_message = None
            return

        # Reset navigation after sort to mirror TUI behaviour
        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        self.status_message = None

        if self._value_selection_filter is not None:
            self._selection_epoch += 1

        self.clamp()

    def reset_sorting(self) -> None:
        """Clear any active sort order."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "sorting not supported"
            return

        try:
            result = self._apply_plan_update("clear sort", plan_clear_sort)
        except PulkaCoreError as exc:
            self._status_from_error("sort", exc)
            return
        except Exception as exc:
            self.status_message = f"sort error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "sorting not supported"
            return

        if not result.plan_changed:
            self.status_message = "no active sort"
            return

        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        self.status_message = "sort cleared"

        if self._value_selection_filter is not None:
            self._selection_epoch += 1

        self.clamp()

    def apply_filter(self, filter_text: str | None, *, mode: FilterMode = "replace") -> None:
        """Apply a filter expression to the active sheet (append or replace)."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "filtering not supported"
            return

        normalized = None
        if filter_text is not None:
            stripped = filter_text.strip()
            normalized = stripped or None

        if normalized is not None:
            try:
                self.engine.validate_filter_clause(normalized)
            except PlanError as exc:
                detail = str(exc).strip()
                message = f"filter error: {detail}" if detail else "filter error"
                self.status_message = message[:120]
                return
            except Exception as exc:
                self.status_message = f"filter error: {exc}"[:120]
                return

        try:
            result = self._apply_plan_update(
                "filter change", lambda plan: plan_set_filter(plan, filter_text, mode=mode)
            )
        except PulkaCoreError as exc:
            self._status_from_error("filter", exc)
            return
        except Exception as exc:
            self.status_message = f"filter error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "filtering not supported"
            return

        if not result.plan_changed:
            self.status_message = "filter unchanged"
            return
        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        active = self.filter_text
        if active:
            preview = active if len(active) <= 60 else active[:57] + "..."
            self.status_message = f"filter: {preview}"
        else:
            self.status_message = "filter cleared"
        self.clamp()

    def reset_expression_filter(self) -> None:
        """Clear any expression filters while preserving SQL filters."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "filtering not supported"
            return

        try:
            result = self._apply_plan_update(
                "clear expression filter",
                lambda plan: plan_set_filter(plan, None, mode="replace"),
            )
        except PulkaCoreError as exc:
            self._status_from_error("filter", exc)
            return
        except Exception as exc:
            self.status_message = f"filter error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "filtering not supported"
            return

        if not result.plan_changed:
            self.status_message = "expression filter already cleared"
            return
        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        active = self.filter_text
        if active:
            preview = active if len(active) <= 60 else active[:57] + "..."
            self.status_message = preview
        else:
            self.status_message = "expression filter cleared"
        self.clamp()

    def append_filter_for_current_value(self) -> None:
        """Append a filter for the active cell's value on the current column."""

        filter_expr = self._filter_expr_for_current_value(exclude=False)
        if filter_expr is None:
            return

        self.apply_filter(filter_expr, mode="append")

    def append_negative_filter_for_current_value(self) -> None:
        """Append a negative filter for the active cell's value on the current column."""

        filter_expr = self._filter_expr_for_current_value(exclude=True)
        if filter_expr is None:
            return

        self.apply_filter(filter_expr, mode="append")

    def _filter_expr_for_current_value(self, *, exclude: bool) -> str | None:
        """Build a filter expression for the active cell value."""

        if not self.columns:
            self.status_message = "no columns to filter"
            return None

        try:
            column_name = self.columns[self.cur_col]
        except Exception:
            self.status_message = "no columns to filter"
            return None

        plan = self._current_plan()
        try:
            table_slice, _ = self.row_provider.get_slice(plan, (column_name,), self.cur_row, 1)
        except Exception as exc:  # pragma: no cover - defensive
            self.status_message = f"filter error: {exc}"[:120]
            return None

        if table_slice.height <= 0:
            self.status_message = "no rows to filter"
            return None

        try:
            values = table_slice.column(column_name).values
            target_value = values[0] if values else None
        except Exception:  # pragma: no cover - defensive
            self.status_message = "value unavailable"
            return None

        try:
            filter_expr = build_filter_expr_for_values(column_name, [target_value])
            if exclude:
                filter_expr = f"~({filter_expr})"
        except Exception as exc:  # pragma: no cover - defensive
            self.status_message = f"filter error: {exc}"[:120]
            return None

        return filter_expr

    def apply_sql_filter(self, where_clause: str | None, *, mode: FilterMode = "replace") -> None:
        """Apply an SQL WHERE-clause filter to the active sheet (append or replace)."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "SQL filtering not supported"
            return

        normalized_clause: str | None = None
        if where_clause is not None:
            trimmed = where_clause.strip()
            normalized_clause = trimmed or None

        if normalized_clause is not None:
            try:
                self.engine.validate_sql_where(self.sheet, normalized_clause)
            except PlanError as exc:
                detail = str(exc).strip()
                message = f"sql filter error: {detail}" if detail else "sql filter error"
                self.status_message = message[:120]
                return
            except Exception as exc:
                self.status_message = f"sql filter error: {exc}"[:120]
                return

        try:
            result = self._apply_plan_update(
                "sql filter change",
                lambda plan: plan_set_sql_filter(plan, normalized_clause, mode=mode),
            )
        except PulkaCoreError as exc:
            self._status_from_error("sql filter", exc)
            return
        except Exception as exc:
            self.status_message = f"sql filter error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "SQL filtering not supported"
            return

        if not result.plan_changed:
            self.status_message = "filter unchanged"
            return
        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        active = self.filter_text
        if active:
            preview = active if len(active) <= 60 else active[:57] + "..."
            self.status_message = preview
        else:
            self.status_message = "filter cleared"
        self.clamp()

    def reset_sql_filter(self) -> None:
        """Clear any SQL WHERE-clause filters while preserving expression filters."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            self.status_message = "SQL filtering not supported"
            return

        try:
            result = self._apply_plan_update(
                "clear sql filter",
                lambda plan: plan_set_sql_filter(plan, None, mode="replace"),
            )
        except PulkaCoreError as exc:
            self._status_from_error("sql filter", exc)
            return
        except Exception as exc:
            self.status_message = f"sql filter error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "SQL filtering not supported"
            return

        if not result.plan_changed:
            self.status_message = "SQL filter already cleared"
            return
        self.cur_row = 0
        self.row0 = 0
        self.invalidate_row_count()
        active = self.filter_text
        if active:
            preview = active if len(active) <= 60 else active[:57] + "..."
            self.status_message = preview
        else:
            self.status_message = "SQL filter cleared"
        self.clamp()

    def reset_filters(self) -> None:
        """Reset filters, sorting, and selection on the active sheet."""

        if not sheet_supports(self.sheet, SHEET_FEATURE_PLAN):
            selection_cleared = self._clear_selection_recorded("reset selection")
            self.status_message = "reset not supported"
            if selection_cleared:
                self.status_message = "selection reset"
            return

        try:
            result = self._apply_plan_update("reset filters", lambda _: plan_reset())
        except PulkaCoreError as exc:
            self._status_from_error("reset", exc)
            return
        except Exception as exc:
            self.status_message = f"reset error: {exc}"[:120]
            return

        if result is None:
            selection_cleared = self._clear_selection_recorded("reset selection")
            self.status_message = "reset not supported"
            if selection_cleared:
                self.status_message = "selection reset"
            return

        if result.plan_changed:
            selection_cleared = self._clear_selection_state()
        else:
            selection_cleared = self._clear_selection_recorded("reset selection")

        if not result.plan_changed and not selection_cleared:
            self.status_message = "filters already reset"
            return

        if result.plan_changed:
            self.cur_row = 0
            self.row0 = 0
            self.invalidate_row_count()
            self._local_filter_text = None
            self._local_filter_kind = None
            self.search_text = None
            if self.last_search_kind == "text":
                self._clear_last_search()

        if selection_cleared and result.plan_changed:
            self.status_message = "filters, sorts, and selection reset"
        elif result.plan_changed:
            self.status_message = "filters and sorts reset"
        elif selection_cleared:
            self.status_message = "selection reset"
        else:  # pragma: no cover - defensive guard
            self.status_message = "reset complete"

        self.clamp()

    def set_search(self, text: str | None) -> None:
        """Record the active search text (whitespace-trimmed)."""
        self._search.set_search(text)

    def _clear_last_search(self) -> None:
        self._search.clear_last_search()

    def search(
        self,
        *,
        forward: bool,
        include_current: bool = False,
        center: bool = True,
        wrap: bool = True,
    ) -> bool:
        """Search within the current column for the recorded search string."""

        return self._search.search(
            forward=forward,
            include_current=include_current,
            center=center,
            wrap=wrap,
        )

    def search_value(
        self,
        *,
        forward: bool,
        include_current: bool = False,
        center: bool = True,
    ) -> bool:
        """Search within the current column for the active cell's value."""

        return self._search.search_value(
            forward=forward,
            include_current=include_current,
            center=center,
        )

    def next_search_match(self) -> bool:
        """Advance to the next row search match."""

        return self._search.next_search_match()

    def prev_search_match(self) -> bool:
        """Move to the previous row search match."""

        return self._search.prev_search_match()

    @property
    def last_search_kind(self) -> Literal["text", "value"] | None:
        """Return the most recent search mode (text or value)."""

        return self._search.last_search_kind

    def repeat_last_search(self, *, forward: bool) -> bool:
        """Repeat the last search (text or value), advancing in ``forward`` direction."""

        return self._search.repeat_last_search(forward=forward)

    def replace_sheet(self, sheet: Sheet, *, source_path: str | None = None) -> None:
        """Swap the viewer to operate on a new sheet instance."""
        old_sheet = getattr(self, "sheet", None)
        if old_sheet is not None and old_sheet is not sheet:
            old_id = getattr(old_sheet, "sheet_id", None)
            preserve_id = getattr(sheet, "_preserve_jobs_from", None)
            if old_id is not None and old_id != preserve_id and self._runner is not None:
                with contextlib.suppress(Exception):
                    self._runner.invalidate_sheet(old_id)

        self.sheet = sheet
        self.columns = list(sheet.columns)
        self._schema_cache = getattr(sheet, "schema", {})
        self._source_path = source_path
        self._transformations = self._create_transformation_manager(sheet)
        provider = getattr(sheet, "row_provider", None)
        if provider is None:
            provider = RowProvider.for_sheet(sheet, runner=self._runner)
        elif getattr(provider, "_runner", None) is None:
            with contextlib.suppress(Exception):
                provider._runner = self._runner
        self._row_provider = provider
        self._engine = ViewerEngine(self._row_provider)
        self.cur_row = 0
        self.row0 = 0
        self.cur_col = 0
        self.col0 = 0
        self.invalidate_row_count()
        self._hidden_cols.clear()
        self._invalidate_frozen_columns_cache()
        self._header_widths = self._compute_initial_column_widths()
        self._default_header_widths = list(self._header_widths)
        self._width_mode = "default"
        self._width_target = None
        self._invalidate_width_cache()
        self._visible_key = None
        self._visible_cols_cached = self.columns[:1] if self.columns else []
        self.is_freq_view = False
        self.freq_source_col = None
        self.is_hist_view = False
        self.status_message = None
        self.update_terminal_metrics()
        self.clamp()
        self._reconcile_schema_changes()
        self._apply_sheet_freeze_defaults(sheet)
        self._apply_file_browser_layout_defaults(sheet)

    def replace_data(self, new_lf: pl.LazyFrame, *, source_path: str | None = None) -> None:
        """Compatibility helper that swaps in a new LazyFrame via DataSheet."""
        new_sheet = DataSheet(new_lf, runner=self._runner)
        self.replace_sheet(new_sheet, source_path=source_path)

    def _compute_initial_column_widths(self) -> list[int]:
        """Compute initial column widths based on header and sample data."""
        width_getter = getattr(self.sheet, "get_column_widths", None)
        if callable(width_getter):
            try:
                provided = width_getter()
            except Exception:
                provided = None
            if isinstance(provided, Mapping):
                widths: list[int] = []
                for name in self.columns:
                    raw = provided.get(name)
                    if isinstance(raw, int):
                        widths.append(max(self._min_col_width, raw))
                    else:
                        widths.append(max(self._min_col_width, len(name) + 2))
                if widths:
                    return widths
        return self._widths.compute_initial_widths()

    def _compute_content_width(
        self,
        col_idx: int,
        *,
        sampled_lengths: dict[int, list[int]] | None = None,
    ) -> int:
        """Compute a sampled content width for a column."""
        return self._widths.content_width_for_column(
            col_idx,
            sampled_lengths=sampled_lengths,
        )

    def _invalidate_width_cache(self) -> None:
        """Drop cached content width calculations."""
        self._widths.invalidate_cache()

    def _ensure_default_widths(self) -> None:
        """Ensure default header widths align with the current schema."""
        self._widths.ensure_default_widths()

    def _normalize_width_mode(self) -> None:
        """Validate current width mode against the active columns."""
        self._widths.normalize_mode()

    def _apply_width_mode(self) -> None:
        """Rebuild header widths according to the active width mode."""
        self._widths.apply_width_mode()

    def _autosize_visible_columns(self, column_indices: list[int]) -> None:
        """Stretch visible column widths to fill the viewport when possible."""
        self._widths.autosize_visible_columns(column_indices)

    def _force_default_width_mode(self) -> None:
        """Reset width mode to default and reapply widths."""
        self._widths.force_default_mode()

    def toggle_maximize_current_col(self) -> None:
        """Toggle maximisation for the active column."""
        self._widths.toggle_maximize_current_col()

    def toggle_maximize_all_cols(self) -> None:
        """Toggle maximisation for every column."""
        self._widths.toggle_maximize_all_cols()

    # Width mode helpers exposed for other components ---------------------------------

    @property
    def maximized_column_index(self) -> int | None:
        """Return the index of the maximised column when in single-column mode."""
        if self._width_mode == "single" and self._width_target is not None:
            return self._width_target
        return None

    @property
    def all_columns_maximized(self) -> bool:
        """Return True when all columns are currently maximised."""
        return self._width_mode == "all"

    @property
    def width_mode_state(self) -> dict[str, int | None | str]:
        """Return a serialisable representation of the active width mode."""
        return {"mode": self._width_mode, "target": self.maximized_column_index}

    def snapshot(self) -> ViewerPublicState:
        """Return an immutable snapshot of the viewer suitable for public use."""

        return build_public_state(self)

    # Navigation helpers (shared with keybindings and scripted mode)
    def move_down(self, steps: int = 1) -> None:
        for _ in range(max(steps, 0)):
            # Stop at the last row if we know the total
            if (
                self._total_rows is not None
                and self._total_rows > 0
                and self.cur_row >= self._total_rows - 1
            ):
                break
            self.cur_row += 1
            if self.cur_row >= self.row0 + self._body_view_height():
                # Don't scroll past the end of the data
                if self._total_rows is not None and self._total_rows > 0:
                    max_row0 = self._max_row0_for_total(self._total_rows)
                    self.row0 = min(self.row0 + 1, max_row0)
                else:
                    self.row0 += 1
        self.clamp()

    def move_up(self, steps: int = 1) -> None:
        for _ in range(max(steps, 0)):
            self.cur_row = max(0, self.cur_row - 1)
            self.row0 = min(self.row0, self.cur_row)
        self.clamp()

    def move_right(self, steps: int = 1) -> None:
        """
        Move cursor right following predictable behavior:
        1. Move cursor to next visible column
        2. If cursor is not visible after move, shift viewport just enough to make it visible
        3. Always move cursor to next column (no jumps), ensuring sequential progression
        """
        # Clear any previous max visible column constraint for normal navigation
        self._max_visible_col = None
        self._visible_key = None

        for _ in range(max(steps, 0)):
            # Find next visible column
            next_col = self.cur_col + 1
            while next_col < len(self.columns) and self.columns[next_col] in self._hidden_cols:
                next_col += 1

            # Stop if we've reached the last column
            if next_col >= len(self.columns):
                break

            if (
                self._compact_width_layout
                and self._width_mode == "default"
                and self._has_partial_column
                and self._partial_column_index is not None
                and next_col == self._partial_column_index
            ):
                # First press after a partial is shown scrolls to make it fully visible
                # as the rightmost column and moves selection onto it.
                target = self._partial_column_index
                self._ensure_col_visible_right_aligned(target)
                self.cur_col = target
                self._visible_key = None
                self._has_partial_column = False
                self._partial_column_index = None
                continue

            # Check if target column is currently visible
            target_col_visible = self.columns[next_col] in self.visible_cols

            # Move cursor to next column
            self.cur_col = next_col

            # CRITICAL: Ensure cursor is never behind the viewport
            # This prevents the bug where cursor becomes invisible
            if self.cur_col < self.col0:
                self.col0 = self.cur_col

            # If we're moving to a column that wasn't visible, position it as rightmost
            if not target_col_visible:
                self._ensure_col_visible_right_aligned(self.cur_col)

        self.clamp()

    def move_left(self, steps: int = 1) -> None:
        # Clear any previous max visible column constraint for normal navigation
        self._max_visible_col = None
        self._visible_key = None

        for _ in range(max(steps, 0)):
            # Find previous visible column
            prev_col = self.cur_col - 1
            while prev_col >= 0 and self.columns[prev_col] in self._hidden_cols:
                prev_col -= 1
            if prev_col >= 0:
                self.cur_col = prev_col
                # Adjust viewport if needed
                visible_cols = self.visible_cols
                if (
                    visible_cols
                    and self.columns[self.cur_col] not in visible_cols
                    and not self._is_column_frozen(self.cur_col)
                ):
                    # Adjust col0 to make current column visible
                    self.col0 = min(self.col0, self.cur_col)
        self.clamp()

    def page_down(self) -> None:
        step = self._body_view_height()
        if self._total_rows is not None and self._total_rows > 0:
            self.cur_row = min(self.cur_row + step, self._total_rows - 1)
            self.row0 = min(self.row0 + step, self._max_row0_for_total(self._total_rows))
        else:
            self.cur_row += step
            self.row0 += step
        self.clamp()

    def page_up(self) -> None:
        step = self._body_view_height()
        self.cur_row = max(0, self.cur_row - step)
        self.row0 = max(0, self.row0 - step)
        self.clamp()

    def go_top(self) -> None:
        self.cur_row = 0
        self.row0 = 0
        self.clamp()

    def go_bottom(self) -> None:
        # Jump to the known last row if we have a count; otherwise best-effort
        total_rows = self._ensure_total_rows()
        if total_rows is not None and total_rows > 0:
            self.cur_row = total_rows - 1
            self.row0 = self._max_row0_for_total(total_rows)
        else:
            self.cur_row += 1_000_000
            self.row0 = max(self.row0, self.cur_row - self._body_view_height() + 1)
        self.clamp()

    def first_col(self) -> None:
        # Go to the leftmost visible column
        visible = self.visible_cols
        if visible:
            try:
                self.cur_col = self.columns.index(visible[0])
            except ValueError:
                self.cur_col = max(0, self.col0)
        else:
            self.cur_col = max(0, self.col0)
        self.clamp()

    def last_col(self) -> None:
        # Go to rightmost visible column
        visible = self.visible_cols
        if visible:
            try:
                self.cur_col = self.columns.index(visible[-1])
            except ValueError:
                self.cur_col = max(0, self.col0)
        else:
            self.cur_col = max(0, self.col0)
        self.clamp()

    def first_col_overall(self) -> None:
        # Go to very first column overall
        self.cur_col = 0
        # Ensure the first column is visible by adjusting viewport
        self.col0 = min(self.col0, self.cur_col)
        self.clamp()

    def _ensure_col_visible_right_aligned(self, target: int) -> None:
        """Make sure `target` is visible as the RIGHTMOST visible column."""
        should_record = self._perf_callback is not None
        start_ns = monotonic_ns() if should_record else 0
        iterations = 0
        start_col0 = self.col0

        self._visible_key = None

        # Set the max visible column constraint to ensure target is rightmost when
        # we're not in the compact/default layout where we still want a trailing
        # partial column to hint at more data to the right.
        if self._compact_width_layout and self._width_mode == "default":
            self._max_visible_col = None
        else:
            self._max_visible_col = target

        if self._is_column_frozen(target):
            # Frozen columns are always visible; no need to adjust scroll state
            if should_record:
                duration_ms = (monotonic_ns() - start_ns) / 1_000_000
                payload = {
                    "target": target,
                    "iterations": 0,
                    "start_col0": start_col0,
                    "final_col0": self.col0,
                    "viewport_override": bool(self._viewport_cols_override),
                    "frozen": True,
                }
                self._record_perf_event("viewer.ensure_right_aligned", duration_ms, payload)
            return

        # If user forced a fixed number of visible columns, this is trivial.
        if self._viewport_cols_override:
            max_cols = max(1, self._viewport_cols_override)
            new_col0 = max(0, target - max_cols + 1)
            self.col0 = max(self._first_scrollable_col_index(), new_col0)
            if should_record:
                duration_ms = (monotonic_ns() - start_ns) / 1_000_000
                payload = {
                    "target": target,
                    "iterations": 0,
                    "start_col0": start_col0,
                    "final_col0": self.col0,
                    "viewport_override": True,
                }
                self._record_perf_event("viewer.ensure_right_aligned", duration_ms, payload)
            return

        max_width = max(20, self.view_width_chars)
        frozen_indices = self._frozen_column_indices()
        frozen_set = self._frozen_column_index_set()

        used_width = 1  # table border on the left
        for idx in frozen_indices:
            name = self.columns[idx]
            if name in self._hidden_cols:
                continue
            used_width += self._header_widths[idx] + 1

        new_col0 = target
        idx = target

        # Always account for the target column even if it exceeds the viewport on its own.
        while idx >= 0:
            iterations += 1
            name = self.columns[idx]
            if name in self._hidden_cols or idx in frozen_set:
                idx -= 1
                continue

            width_with_border = self._header_widths[idx] + 1
            if idx == target:
                used_width += width_with_border
                new_col0 = idx
                idx -= 1
                continue

            if used_width + width_with_border > max_width:
                break

            used_width += width_with_border
            new_col0 = idx
            idx -= 1

        computed_col0 = max(self._first_scrollable_col_index(), new_col0)
        if target >= start_col0:
            computed_col0 = max(computed_col0, start_col0)
        self.col0 = computed_col0

        if should_record:
            duration_ms = (monotonic_ns() - start_ns) / 1_000_000
            payload = {
                "target": target,
                "iterations": iterations,
                "start_col0": start_col0,
                "final_col0": self.col0,
                "viewport_override": False,
            }
            self._record_perf_event("viewer.ensure_right_aligned", duration_ms, payload)

    def last_col_overall(self) -> None:
        self.cur_col = len(self.columns) - 1
        self._ensure_col_visible_right_aligned(self.cur_col)
        self.clamp()

    def slide_column_left(self) -> None:
        """Slide the current column one visible slot to the left."""
        self._slide_current_column("left", to_edge=False)

    def slide_column_right(self) -> None:
        """Slide the current column one visible slot to the right."""
        self._slide_current_column("right", to_edge=False)

    def slide_column_to_start(self) -> None:
        """Slide the current column to the first visible position."""
        self._slide_current_column("left", to_edge=True)

    def slide_column_to_end(self) -> None:
        """Slide the current column to the last visible position."""
        self._slide_current_column("right", to_edge=True)

    def _slide_current_column(self, direction: Literal["left", "right"], *, to_edge: bool) -> None:
        if not self.columns:
            self.status_message = "no columns to move"
            return

        current_idx = self.cur_col
        if not (0 <= current_idx < len(self.columns)):
            self.status_message = "column index out of range"
            return

        current_name = self.columns[current_idx]
        if current_name in self._hidden_cols:
            self.status_message = "cannot move hidden column"
            return

        visible_indices = [
            idx for idx, name in enumerate(self.columns) if name not in self._hidden_cols
        ]
        if len(visible_indices) <= 1:
            self.status_message = "no other visible columns"
            return

        try:
            visible_pos = visible_indices.index(current_idx)
        except ValueError:
            self.status_message = "column is not visible"
            return

        if direction == "left":
            if visible_pos == 0:
                self.status_message = "already at left edge"
                return
            target_visible_pos = 0 if to_edge else visible_pos - 1
            target_idx = visible_indices[target_visible_pos]
            insert_at = target_idx
        else:
            last_pos = len(visible_indices) - 1
            if visible_pos == last_pos:
                self.status_message = "already at right edge"
                return
            target_visible_pos = last_pos if to_edge else visible_pos + 1
            target_idx = visible_indices[target_visible_pos]
            insert_at = target_idx + 1

        new_order = list(self.columns)
        removed = new_order.pop(current_idx)
        if target_idx > current_idx:
            insert_at -= 1
        insert_at = max(0, min(insert_at, len(new_order)))
        new_order.insert(insert_at, removed)

        if new_order == list(self.columns):
            self.status_message = "column already positioned"
            return

        if to_edge and direction == "left":
            desc = f"move {current_name} to first column"
            status = f"{current_name} moved to first column"
        elif to_edge and direction == "right":
            desc = f"move {current_name} to last column"
            status = f"{current_name} moved to last column"
        elif direction == "left":
            desc = f"move {current_name} left"
            status = f"{current_name} moved left"
        else:
            desc = f"move {current_name} right"
            status = f"{current_name} moved right"

        def mutate() -> bool:
            self._apply_column_reorder(new_order, active_column=current_name)
            return True

        result = self._transformations.record_change(desc, mutate)
        if result.committed:
            self.status_message = status

    def _apply_column_reorder(self, new_order: Sequence[str], *, active_column: str) -> None:
        old_order = tuple(self.columns)
        if tuple(new_order) == old_order:
            return

        index_lookup = {name: idx for idx, name in enumerate(old_order)}

        def _reorder_widths(values: Sequence[int]) -> list[int]:
            if not values:
                return [self._min_col_width] * len(new_order)
            reordered: list[int] = []
            for name in new_order:
                idx = index_lookup.get(name)
                if idx is None or idx >= len(values):
                    reordered.append(self._min_col_width)
                else:
                    reordered.append(values[idx])
            return reordered

        self.columns = list(new_order)
        self._header_widths = _reorder_widths(self._header_widths)
        self._default_header_widths = _reorder_widths(self._default_header_widths)

        width_target_name: str | None = None
        if (
            self._width_mode == "single"
            and self._width_target is not None
            and 0 <= self._width_target < len(old_order)
        ):
            width_target_name = old_order[self._width_target]

        self._invalidate_width_cache()
        self._autosized_widths.clear()
        self._visible_key = None
        self._visible_cols_cached = self.columns[:1] if self.columns else []
        self._max_visible_col = None
        self._invalidate_frozen_columns_cache()
        self.invalidate_row_cache()

        if width_target_name is not None and width_target_name in self.columns:
            self._width_target = self.columns.index(width_target_name)
        elif self._width_mode == "single":
            self._width_mode = "default"
            self._width_target = None

        if active_column in self.columns:
            self.cur_col = self.columns.index(active_column)
        else:
            self.cur_col = 0

        self.clamp()

        if self.columns:
            active_name = self.columns[self.cur_col]
            if active_name not in self.visible_cols and not self._is_column_frozen(self.cur_col):
                self._ensure_col_visible_right_aligned(self.cur_col)
                self.clamp()

    def center_current_row(self) -> None:
        """Center the current row in the viewport."""
        half = max(1, self._body_view_height()) // 2
        self.row0 = max(self._effective_frozen_row_count(), self.cur_row - half)
        self.clamp()

    def prev_different_value(self) -> bool:
        """Navigate to the previous row with a different value in the current column."""
        return self._search.prev_different_value()

    def next_different_value(self) -> bool:
        """Navigate to the next row with a different value in the current column."""
        return self._search.next_different_value()

    @property
    def visible_cols(self) -> list[str]:
        # Determine visible columns based on new dynamic width allocation logic
        visible_columns = [col for col in self.columns if col not in self._hidden_cols]
        frozen_indices = self._frozen_column_indices()
        frozen_names = self.frozen_columns
        frozen_set = self._frozen_column_name_set()

        def _has_more_to_right(current: list[str]) -> bool:
            if not current:
                return False
            try:
                last_name = current[-1]
                last_idx = self.columns.index(last_name)
            except (ValueError, IndexError):
                return False
            for idx in range(last_idx + 1, len(self.columns)):
                name = self.columns[idx]
                if name in self._hidden_cols or name in frozen_set:
                    continue
                return True
            return False

        # Handle viewport override early (fixed number of columns regardless of width).
        if self._viewport_cols_override is not None:
            should_record = self._perf_callback is not None
            start_ns = monotonic_ns() if should_record else 0

            max_dynamic = max(1, self._viewport_cols_override)
            scroll_start = max(self.col0, self._first_scrollable_col_index())
            dynamic: list[str] = []
            for idx in range(scroll_start, len(self.columns)):
                name = self.columns[idx]
                if name in self._hidden_cols or name in frozen_set:
                    continue
                dynamic.append(name)
                if len(dynamic) >= max_dynamic:
                    break

            result = frozen_names + dynamic
            self._last_col_fits_completely = True
            self._visible_cols_cached = result
            self._visible_key = None

            index_lookup = {name: idx for idx, name in enumerate(self.columns)}
            visible_indices = [index_lookup[col] for col in result if col in index_lookup]
            self._autosize_visible_columns(visible_indices)

            if should_record:
                duration_ms = (monotonic_ns() - start_ns) / 1_000_000
                payload = {
                    "viewport_override": True,
                    "col0": self.col0,
                    "visible_count": len(result),
                    "hidden_count": len(self._hidden_cols),
                    "frozen": len(frozen_names),
                }
                self._record_perf_event("viewer.visible_cols", duration_ms, payload)
            return result

        key: VisibleCacheKey = (
            self.col0,
            self.cur_col,
            self.view_width_chars,
            self._viewport_cols_override,
            tuple(sorted(self._hidden_cols)),
            tuple(self._header_widths),
            tuple(frozen_indices),
        )
        if key == self._visible_key and not (
            self._compact_width_layout
            and self._width_mode == "default"
            and _has_more_to_right(self._visible_cols_cached)
        ):
            return self._visible_cols_cached

        self._has_partial_column = False
        self._partial_column_index = None
        self._stretch_last_for_slack = False

        should_record = self._perf_callback is not None
        start_ns = monotonic_ns() if should_record else 0
        evaluated = 0

        max_width = max(20, self.view_width_chars)
        allow_partial_width = self._width_mode == "default"
        used = 1  # left border
        res: list[str] = []
        last_fits_completely = True

        for idx in frozen_indices:
            name = self.columns[idx]
            if name in self._hidden_cols:
                continue
            res.append(name)
            used += self._header_widths[idx] + 1

        if used > max_width:
            last_fits_completely = False

        scroll_start = max(self.col0, self._first_scrollable_col_index())

        self._has_partial_column = False
        last_iter_idx = scroll_start - 1
        partial_min_width = 2
        for idx in range(scroll_start, len(self.columns)):
            name = self.columns[idx]
            if name in self._hidden_cols or name in frozen_set:
                continue

            evaluated += 1
            last_iter_idx = idx
            w = self._header_widths[idx]

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
        if 0 <= self.cur_col < len(self.columns):
            active_name = self.columns[self.cur_col]

        active_is_partial_last = (
            allow_partial_width
            and not last_fits_completely
            and not self._aligning_active_column
            and self._viewport_cols_override is None
            and res
            and active_name is not None
            and res[-1] == active_name
        )

        if active_is_partial_last:
            prev_col0 = self.col0
            self._aligning_active_column = True
            try:
                self._ensure_col_visible_right_aligned(self.cur_col)
            finally:
                self._aligning_active_column = False
            if self.col0 != prev_col0:
                self._visible_key = None
                return self.visible_cols

        if allow_partial_width and res and not self._has_partial_column:
            remaining = max_width - used
            # Require space for both the column body and its right border.
            min_required = partial_min_width + 1
            next_idx: int | None = None
            for idx in range(last_iter_idx + 1, len(self.columns)):
                name = self.columns[idx]
                if name in self._hidden_cols or name in frozen_set:
                    continue
                next_idx = idx
                break

            if (
                next_idx is not None
                and self.columns[next_idx] not in res
                and remaining >= min_required
            ):
                res.append(self.columns[next_idx])
                last_fits_completely = False
                self._has_partial_column = True
                self._partial_column_index = next_idx
            elif (
                next_idx is not None
                and remaining > 0
                and remaining < min_required
                and self._compact_width_layout
                and self._width_mode == "default"
            ):
                # Not enough room to show even a partial column; remember the slack so
                # the viewport planner can optionally stretch the last visible column.
                self._stretch_last_for_slack = True
            else:
                self._stretch_last_for_slack = False
        else:
            self._stretch_last_for_slack = False

        if not res and visible_columns:
            for col in visible_columns:
                col_idx = self.columns.index(col)
                if col_idx >= scroll_start:
                    res = [col]
                    break
            if not res:
                res = [visible_columns[0]]

        if (
            self._max_visible_col is not None
            and res
            and not (self._compact_width_layout and self._width_mode == "default")
        ):
            truncated_res = []
            for col in res:
                col_idx = self.columns.index(col)
                if col in frozen_set or col_idx <= self._max_visible_col:
                    truncated_res.append(col)
                else:
                    break
            res = truncated_res

        self._has_partial_column = self._has_partial_column and len(res) > len(frozen_names)
        if not self._has_partial_column:
            self._partial_column_index = None

        index_lookup = {name: idx for idx, name in enumerate(self.columns)}
        visible_indices = [index_lookup[col] for col in res if col in index_lookup]
        self._autosize_visible_columns(visible_indices)

        self._visible_key = key
        self._visible_cols_cached = res
        self._last_col_fits_completely = last_fits_completely

        if should_record:
            duration_ms = (monotonic_ns() - start_ns) / 1_000_000
            visible_payload: dict[str, object] = {
                "viewport_override": False,
                "col0": self.col0,
                "visible_count": len(res),
                "evaluated": evaluated,
                "hidden_count": len(self._hidden_cols),
                "max_width": max_width,
                "fits_full": last_fits_completely,
                "max_visible_col": self._max_visible_col,
                "frozen": len(frozen_names),
            }
            self._record_perf_event("viewer.visible_cols", duration_ms, visible_payload)
        return res

    # Column hiding functionality
    def keep_columns(self, columns: Sequence[str]) -> None:
        """Keep only ``columns``, hiding everything else."""

        if not self.columns:
            self.status_message = "no columns to keep"
            return

        available = set(self.columns)
        normalized: list[str] = []
        seen: set[str] = set()
        for name in columns:
            if not isinstance(name, str):
                continue
            if name in seen or name not in available:
                continue
            normalized.append(name)
            seen.add(name)

        if not normalized:
            self.status_message = "no matching columns selected"
            return

        selected = set(normalized)

        def builder(plan: QueryPlan) -> QueryPlan:
            base_projection = plan.projection_or(self.columns)
            desired = [name for name in base_projection if name in selected]
            if not desired:
                desired = [name for name in self.columns if name in selected]
            if not desired:
                return plan
            return plan_set_projection(plan, desired)

        try:
            result = self._apply_plan_update(
                f"keep {len(selected)} column" + ("s" if len(selected) != 1 else ""),
                builder,
            )
        except PulkaCoreError as exc:
            self._status_from_error("keep columns", exc)
            return
        except Exception as exc:  # pragma: no cover - defensive
            self.status_message = f"keep columns error: {exc}"[:120]
            return

        if result is None:
            self.status_message = "column projection not supported"
            return

        if not result.committed or not result.plan_changed:
            self.status_message = "columns unchanged"
            return

        self._visible_key = None
        self._reconcile_schema_changes()

        remaining = len(self.visible_columns())
        if remaining == 1:
            self.status_message = f"Showing column: {self.visible_columns()[0]}"
        else:
            self.status_message = f"Showing {remaining} columns"

        if __debug__:
            self._validate_state_consistency()

    def hide_current_column(self) -> None:
        """Hide the current column (- key)."""
        if not self.columns:
            self.status_message = "No columns to hide"
            return

        current_col_name = self.columns[self.cur_col]

        # If column is already hidden, no-op
        if current_col_name in self._hidden_cols:
            self.status_message = f"Column already hidden: {current_col_name}"
            return

        # If this is the last visible column, block the operation
        visible_columns = self.visible_columns()
        if len(visible_columns) == 1 and visible_columns[0] == current_col_name:
            self.status_message = f"Cannot hide the last visible column: {current_col_name}"
            return

        def builder(plan: QueryPlan) -> QueryPlan:
            base_projection = list(plan.projection_or(self.columns))
            if current_col_name not in base_projection:
                return plan
            updated = [name for name in base_projection if name != current_col_name]
            if not updated:
                return plan
            return plan_set_projection(plan, updated)

        try:
            result = self._apply_plan_update(f"hide {current_col_name}", builder)
        except PulkaCoreError as exc:
            self._status_from_error("hide column", exc)
            return

        if result is None:

            def mutate() -> bool:
                self._local_hidden_cols.add(current_col_name)
                self._update_hidden_column_cache(set(self._local_hidden_cols))
                return True

            result = self._transformations.record_change(f"hide {current_col_name}", mutate)
            if not result.committed:
                return
        elif not result.committed:
            return

        self.status_message = f"Removed column: {current_col_name}"
        self._visible_key = None
        self._reconcile_schema_changes()

        if __debug__:
            self._validate_state_consistency()

    def unhide_all_columns(self) -> None:
        """Unhide all hidden columns (gv command)."""
        # If no hidden columns, no-op
        if not self._hidden_cols:
            self.status_message = "No hidden columns to restore"
            return

        def builder(plan: QueryPlan) -> QueryPlan:
            return plan_set_projection(plan, self.columns)

        try:
            result = self._apply_plan_update("unhide all columns", builder)
        except PulkaCoreError as exc:
            self._status_from_error("unhide", exc)
            return

        if result is None:

            def mutate() -> bool:
                self._local_hidden_cols.clear()
                self._update_hidden_column_cache(set())
                return True

            result = self._transformations.record_change("unhide all columns", mutate)
            if not result.committed:
                return
        elif not result.committed:
            return

        self.status_message = "Restored all hidden columns"
        self._visible_key = None
        self._reconcile_schema_changes()

        if __debug__:
            self._validate_state_consistency()

    def undo_last_operation(self) -> None:
        """Undo last operation (u key)."""

        snapshot = self._transformations.undo()
        if snapshot is None:
            self.status_message = "Nothing to undo"
            return
        if snapshot.description:
            self.status_message = f"Undo: {snapshot.description}"
        else:
            self.status_message = "Undid last change"

        self.search_text = self.search_text

        if __debug__:
            self._validate_state_consistency()

    def redo_last_operation(self) -> None:
        """Redo last undone operation (U key)."""

        snapshot = self._transformations.redo()
        if snapshot is None:
            self.status_message = "Nothing to redo"
            return
        if snapshot.description:
            self.status_message = f"Redo: {snapshot.description}"
        else:
            self.status_message = "Redid last change"

        self.search_text = self.search_text

        if __debug__:
            self._validate_state_consistency()

    def visible_columns(self) -> list[str]:
        """Return the ordered list of columns marked visible by the active plan."""

        projection = self._plan_projection_columns()
        if projection is not None:
            order_index = {name: idx for idx, name in enumerate(self.columns)}
            filtered = [name for name in projection if name in order_index]
            filtered.sort(key=lambda name: order_index.get(name, len(self.columns)))
            return filtered
        return [col for col in self.columns if col not in self._hidden_cols]

    def current_colname(self) -> str:
        """Return the name of the current column."""
        return self.columns[self.cur_col]

    def _capture_view_state(self) -> ViewerSnapshot:
        """Capture viewer-specific state required for undo/redo."""

        return self._state.capture_snapshot()

    def _restore_view_state(self, state: ViewerSnapshot) -> None:
        """Restore viewer state from ``state`` and reconcile caches."""

        self._state.restore_snapshot(state)

    def next_visible_col_index(self, search_from: int) -> int | None:
        """Find the next visible column index, searching rightward, else leftward as fallback."""
        return self._state.next_visible_col_index(search_from)

    def _move_cursor_to_next_visible_column(self) -> None:
        """Move cursor to the next visible column."""
        self._state.move_cursor_to_next_visible_column()

    def _ensure_cursor_on_visible_column(self) -> None:
        """Ensure cursor is positioned on a visible column."""
        self._state.ensure_cursor_on_visible_column()

    def _update_hidden_column_cache(self, hidden: set[str], *, ensure_cursor: bool = True) -> None:
        """Apply ``hidden`` as the canonical hidden column set."""

        normalized = {name for name in hidden if name in self.columns}
        self._hidden_cols = normalized
        self._invalidate_frozen_columns_cache()
        self._visible_key = None

        if len(self._header_widths) < len(self.columns):
            for idx in range(len(self._header_widths), len(self.columns)):
                baseline = (
                    self._default_header_widths[idx]
                    if idx < len(self._default_header_widths)
                    else self._min_col_width
                )
                self._header_widths.append(max(baseline, self._min_col_width))

        for idx, name in enumerate(self.columns):
            if idx >= len(self._header_widths):
                break
            if name in normalized:
                self._header_widths[idx] = 0
            elif self._header_widths[idx] == 0:
                baseline = (
                    self._default_header_widths[idx]
                    if idx < len(self._default_header_widths)
                    else self._min_col_width
                )
                self._header_widths[idx] = max(baseline, self._min_col_width)

        if ensure_cursor:
            self._ensure_cursor_on_visible_column()

    def _sync_hidden_columns_from_plan(self) -> None:
        """Align hidden columns with the authoritative projection source."""

        if not self.columns:
            self._local_hidden_cols.clear()
            self._update_hidden_column_cache(set())
            return

        projection = self._plan_projection_columns()
        if projection is None:
            self._local_hidden_cols.intersection_update(self.columns)
            self._update_hidden_column_cache(set(self._local_hidden_cols))
            return

        projected = set(projection)
        hidden = {name for name in self.columns if name not in projected}
        self._local_hidden_cols.clear()
        self._update_hidden_column_cache(hidden)

    def _reconcile_schema_changes(self) -> None:
        """
        Reconcile internal state after schema changes:
        - Reconcile hidden set with current schema
        - Rebuild column widths to align with current schema
        - Invalidate all caches related to visibility and rendering
        - Re-snap cursor to the nearest visible column
        - Clean undo stack by dropping references to removed columns
        """
        # Refresh cached schema snapshot
        self._schema_cache = getattr(self.sheet, "schema", self._schema_cache)

        # Align hidden caches with the authoritative plan/local projection
        self._sync_hidden_columns_from_plan()
        self._local_hidden_cols.intersection_update(self.columns)

        # Rebuild column widths to align with current schema
        # Ensure widths array matches current columns
        if len(self._header_widths) != len(self.columns):
            # Rebuild widths arrays to match current schema
            self._header_widths = self._compute_initial_column_widths()
            self._default_header_widths = list(self._header_widths)
            self._force_default_width_mode()
        else:
            self._apply_width_mode()

        # Invalidate all visibility-related caches
        self._visible_key = None
        self._visible_cols_cached = self.columns[:1] if self.columns else []

        # Re-snap cursor to the nearest visible column
        # Cursor must always land on a visible column
        if self.columns:
            self.cur_col = max(0, min(self.cur_col, len(self.columns) - 1))
            # Ensure cursor is on a visible column
            if self.cur_col < len(self.columns) and self.columns[self.cur_col] in self._hidden_cols:
                # Try to find next visible column
                next_visible = self.next_visible_col_index(self.cur_col)
                if next_visible is not None:
                    self.cur_col = next_visible
                else:
                    # If no next visible, find first visible column
                    for i, col in enumerate(self.columns):
                        if col not in self._hidden_cols:
                            self.cur_col = i
                            break
                    else:
                        # Emergency fallback - reset to first column
                        self.cur_col = 0

        # Prune transformation history snapshots referencing stale columns
        column_set = set(self.columns)

        def _is_valid(snapshot: TransformationSnapshot) -> bool:
            state = snapshot.view_state
            if not isinstance(state, ViewerSnapshot):
                return True
            if len(state.header_widths) != len(self.columns):
                return False
            return set(state.hidden_cols).issubset(column_set)

        self._transformations.filter_history(_is_valid)

        # Ensure at least one column remains visible
        visible_columns = self.visible_columns()
        if not visible_columns and self.columns and self._plan_projection_columns() is None:
            # Only legacy, planless sheets can end up hiding everything.
            self._local_hidden_cols.clear()
            self._update_hidden_column_cache(set())
            self._force_default_width_mode()

    def _validate_state_consistency(self) -> None:
        """Validate that internal state is consistent.

        This method checks for common consistency issues that could lead to
        UI synchronization problems.
        """
        # Ensure cursor is on a valid column
        if not (0 <= self.cur_col < len(self.columns)):
            raise AssertionError(
                f"Cursor column index {self.cur_col} out of bounds [0, {len(self.columns)})"
            )

        # Ensure cursor is on a visible column (unless all hidden, shouldn't happen)
        if self.columns and self.columns[self.cur_col] in self._hidden_cols:
            raise AssertionError(f"Cursor is on hidden column {self.columns[self.cur_col]}")

        missing_hidden = self._hidden_cols - set(self.columns)
        if missing_hidden:
            raise AssertionError(f"Hidden columns out of schema: {sorted(missing_hidden)}")

        missing_local = self._local_hidden_cols - set(self.columns)
        if missing_local:
            raise AssertionError(f"Local hidden columns out of schema: {sorted(missing_local)}")

        projection = self._plan_projection_columns()
        if projection is not None:
            expected_hidden = {name for name in self.columns if name not in set(projection)}
            if expected_hidden != self._hidden_cols:
                raise AssertionError(
                    "Plan projection mismatch:"
                    f" expected {sorted(expected_hidden)}, got {sorted(self._hidden_cols)}"
                )
            expected_visible = [name for name in projection if name in self.columns]
            if expected_visible != self.visible_columns():
                raise AssertionError(
                    "Plan projection mismatch:",
                    f" visible {expected_visible} != {self.visible_columns()}",
                )

        # Ensure header widths array matches columns length
        if len(self._header_widths) != len(self.columns):
            raise AssertionError(
                f"Header widths mismatch: got {len(self._header_widths)}, want {len(self.columns)}"
            )

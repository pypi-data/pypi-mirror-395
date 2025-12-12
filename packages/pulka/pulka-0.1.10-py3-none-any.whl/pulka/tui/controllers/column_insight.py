"""Controller coordinating the column insight sidecar."""

from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

import polars as pl

from ...core.column_insight import ColumnInsight
from ...core.formatting import _supports_numeric_stats
from ...core.jobs import JobResult
from ...core.jobs.column_insight_job import (
    ColumnInsightJobConfig,
    compute_column_insight,
)
from ...core.row_provider import RowProvider
from ...core.viewer import Viewer
from ...logging import Recorder
from ...utils import _get_int_env
from ..controls.column_insight_panel import ColumnInsightPanel


@dataclass(frozen=True, slots=True)
class _InsightRequestContext:
    viewer_id: int
    column: str
    plan_hash: str | None
    sheet_id: str | None
    source_path: str | None
    lazyframe: pl.LazyFrame
    schema: Mapping[str, pl.DataType] | None
    sheet: Any
    signature: tuple[str | None, str | None, str]


class ColumnInsightController:
    """Manage scheduling and rendering of column insights."""

    _PREFETCH_LIMIT = 2
    _PREFETCH_CANDIDATE_MAX = 6

    def __init__(
        self,
        *,
        viewer: Viewer,
        panel: ColumnInsightPanel,
        recorder: Recorder | None,
        invalidate: Callable[[], None],
        call_soon: Callable[[Callable[[], None]], None],
        debounce_ms: int | None = None,
    ) -> None:
        self._viewer = viewer
        self._panel = panel
        self._recorder = recorder
        self._runner = viewer.job_runner
        self._enabled = True
        self._lock = threading.RLock()
        self._invalidate = invalidate
        self._call_soon = call_soon
        self._last_cursor_sig: tuple[str, int, str | None] | None = None
        self._last_signature: tuple[str | None, str | None, str] | None = None
        self._pending_context: _InsightRequestContext | None = None
        self._pending_timer: threading.Timer | None = None
        self._inflight_signature: tuple[str | None, str | None, str] | None = None
        self._latest_insight: ColumnInsight | None = None
        self._debounce_ms = (
            debounce_ms
            if debounce_ms is not None
            else max(0, _get_int_env("PULKA_INSIGHT_DEBOUNCE_MS", None, 150))
        )
        self._insight_cache: OrderedDict[tuple[str | None, str | None, str], ColumnInsight] = (
            OrderedDict()
        )
        self._cache_limit = 32
        self._schema_cache: tuple[int, dict[str, pl.DataType]] | None = None
        self._prefetch_signatures: set[tuple[str | None, str | None, str]] = set()
        self._prefetch_contexts: dict[
            tuple[str | None, str | None, str], _InsightRequestContext
        ] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_enabled(self, enabled: bool) -> None:
        with self._lock:
            if self._enabled == enabled:
                return
            self._enabled = enabled
            if not enabled:
                self._cancel_pending_locked()
                self._panel.set_disabled("Insight panel hidden")
                self._prefetch_signatures.clear()
                self._prefetch_contexts.clear()
            else:
                self._last_signature = None
                self._latest_insight = None
                self._insight_cache.clear()
                self._panel.set_unavailable("Select a column to view stats.")
                self._prefetch_signatures.clear()
                self._prefetch_contexts.clear()
        self._invalidate()

    def on_viewer_changed(self, viewer: Viewer) -> None:
        with self._lock:
            self._viewer = viewer
            self._runner = viewer.job_runner
            self._last_signature = None
            self._latest_insight = None
            self._cancel_pending_locked()
            self._last_cursor_sig = None
            self._insight_cache.clear()
            self._schema_cache = None
            self._prefetch_signatures.clear()
            self._prefetch_contexts.clear()

    def on_refresh(self) -> None:
        if not self._enabled:
            return
        viewer = self._viewer
        if not viewer.columns:
            self._panel.set_unavailable("No columns in this sheet.")
            self._invalidate()
            return
        if viewer.cur_col < 0 or viewer.cur_col >= len(viewer.columns):
            self._panel.set_unavailable("Select a column to view stats.")
            self._invalidate()
            return
        column = viewer.columns[viewer.cur_col]
        row = max(0, viewer.cur_row)
        signature = self._current_signature(viewer, column)
        if signature is None:
            self._panel.set_unavailable("Insight requires a plan-backed sheet.")
            self._invalidate()
            return
        plan_hash = signature[1]
        self._update_cell_preview(viewer, column, row, plan_hash)
        self._maybe_schedule_insight(viewer, column, signature)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _update_cell_preview(
        self,
        viewer: Viewer,
        column: str,
        row: int,
        plan_hash: str | None,
    ) -> None:
        cursor_sig = (column, row, plan_hash)
        if self._last_cursor_sig == cursor_sig:
            return
        self._last_cursor_sig = cursor_sig
        row_provider = viewer.row_provider
        plan = getattr(viewer.sheet, "plan", None)
        preview = None
        if isinstance(row_provider, RowProvider):
            try:
                preview = row_provider.current_cell_value(plan, column, row)
            except Exception:
                preview = None
        self._panel.set_cell_preview(preview)
        self._invalidate()

    def _maybe_schedule_insight(
        self,
        viewer: Viewer,
        column: str,
        signature: tuple[str | None, str | None, str],
    ) -> None:
        cached = self._insight_cache.get(signature)
        if cached is not None:
            self._panel.set_insight(cached)
            self._latest_insight = cached
            self._last_signature = signature
            self._invalidate()
            self._maybe_schedule_prefetches(viewer)
            return

        if self._inflight_signature == signature:
            # Job already running; keep status as loading.
            return

        schema_map = self._schema_mapping(viewer.sheet)
        has_numeric_histogram = self._column_is_numeric(column, schema_map)
        context = self._build_context(viewer, column, signature, schema_override=schema_map)
        if context is None:
            self._panel.set_unavailable("Insight requires a lazy frame source.")
            self._invalidate()
            return
        self._prefetch_contexts.pop(signature, None)
        self._prefetch_signatures.discard(signature)
        self._panel.set_loading(column, histogram_expected=has_numeric_histogram)
        self._invalidate()
        self._schedule_request(context)
        self._maybe_schedule_prefetches(viewer)

    def _current_signature(
        self,
        viewer: Viewer,
        column: str,
    ) -> tuple[str | None, str | None, str] | None:
        sheet = viewer.sheet
        sheet_id = getattr(sheet, "sheet_id", None)
        plan_hash = None
        snapshot = getattr(sheet, "plan_snapshot", None)
        if callable(snapshot):
            try:
                plan_hash = snapshot().get("hash")
            except Exception:
                plan_hash = None
        if sheet_id is None and plan_hash is None:
            return None
        return (sheet_id, plan_hash, column)

    def _build_context(
        self,
        viewer: Viewer,
        column: str,
        signature: tuple[str | None, str | None, str],
        *,
        schema_override: Mapping[str, pl.DataType] | None = None,
    ) -> _InsightRequestContext | None:
        sheet = viewer.sheet
        lazyframe_handle = getattr(sheet, "lf", None)
        if lazyframe_handle is None:
            return None
        try:
            from ...core.engine.polars_adapter import unwrap_lazyframe_handle

            lf = unwrap_lazyframe_handle(lazyframe_handle)
        except Exception:
            return None

        schema = schema_override if schema_override is not None else self._schema_mapping(sheet)

        plan_hash = signature[1]
        sheet_id = signature[0]
        source_path = getattr(viewer, "_source_path", None)
        return _InsightRequestContext(
            viewer_id=id(viewer),
            column=column,
            plan_hash=plan_hash,
            sheet_id=sheet_id,
            source_path=source_path,
            lazyframe=lf,
            schema=schema,
            sheet=sheet,
            signature=signature,
        )

    def _column_is_numeric(
        self,
        column: str,
        schema: Mapping[str, pl.DataType] | None,
    ) -> bool:
        if schema is None:
            return False
        dtype = schema.get(column)
        if dtype is None:
            return False
        try:
            return _supports_numeric_stats(dtype)
        except Exception:
            return False

    def _schema_mapping(self, sheet: Any) -> dict[str, pl.DataType] | None:
        raw_schema = getattr(sheet, "schema", None)
        if raw_schema is None:
            self._schema_cache = None
            return None
        cache = self._schema_cache
        key = id(raw_schema)
        if cache and cache[0] == key:
            return cache[1]
        mapping = self._coerce_schema_dict(raw_schema)
        if mapping is None:
            self._schema_cache = None
            return None
        self._schema_cache = (key, mapping)
        return mapping

    @staticmethod
    def _coerce_schema_dict(schema_obj: Any) -> dict[str, pl.DataType] | None:
        try:
            return dict(schema_obj)
        except Exception:
            pass
        try:
            return dict(schema_obj)
        except Exception:
            return None

    def _maybe_schedule_prefetches(self, viewer: Viewer | None) -> None:
        if not self._enabled or viewer is None:
            return
        available = self._PREFETCH_LIMIT - len(self._prefetch_signatures)
        if available <= 0:
            return
        columns = getattr(viewer, "columns", [])
        if not columns:
            return
        cur_idx = getattr(viewer, "cur_col", -1)
        if cur_idx < 0 or cur_idx >= len(columns):
            return
        current_col = columns[cur_idx]
        candidates = self._prefetch_candidate_columns(viewer, current_col)
        for column in candidates:
            if available <= 0:
                break
            signature = self._current_signature(viewer, column)
            if signature is None:
                continue
            if signature in self._insight_cache:
                continue
            if signature == self._inflight_signature:
                continue
            if signature in self._prefetch_signatures:
                continue
            pending = self._pending_context
            if pending is not None and pending.signature == signature:
                continue
            context = self._build_context(viewer, column, signature)
            if context is None:
                continue
            self._start_prefetch(context)
            available -= 1

    def _prefetch_candidate_columns(self, viewer: Viewer, current: str) -> list[str]:
        ordered: list[str] = []
        ordered.extend(self._neighbor_columns(viewer))
        ordered.extend(self._viewport_columns(viewer, current))
        seen: set[str] = set()
        result: list[str] = []
        for name in ordered:
            if not name or name == current or name in seen:
                continue
            result.append(name)
            seen.add(name)
            if len(result) >= self._PREFETCH_CANDIDATE_MAX:
                break
        return result

    def _neighbor_columns(self, viewer: Viewer) -> list[str]:
        columns = getattr(viewer, "columns", [])
        idx = getattr(viewer, "cur_col", -1)
        neighbors: list[str] = []
        if not columns or idx < 0 or idx >= len(columns):
            return neighbors
        if idx + 1 < len(columns):
            neighbors.append(columns[idx + 1])
        if idx - 1 >= 0:
            neighbors.append(columns[idx - 1])
        return neighbors

    def _viewport_columns(self, viewer: Viewer, current: str) -> list[str]:
        visible = list(getattr(viewer, "visible_cols", ()) or ())
        if not visible:
            return []
        try:
            pos = visible.index(current)
            ordered = visible[pos + 1 :] + visible[:pos]
        except ValueError:
            ordered = visible
        return [name for name in ordered if name and name != current]

    def _start_prefetch(self, context: _InsightRequestContext) -> None:
        signature = context.signature
        self._prefetch_signatures.add(signature)
        self._prefetch_contexts[signature] = context

        def _job(_: int) -> ColumnInsight:
            config = ColumnInsightJobConfig(
                column_name=context.column,
                plan_hash=context.plan_hash,
                sheet_id=context.sheet_id,
                source_path=context.source_path,
            )
            lazyframe = (
                context.lazyframe.clone()
                if hasattr(context.lazyframe, "clone")
                else context.lazyframe
            )
            return compute_column_insight(
                lazyframe=lazyframe,
                config=config,
                schema=context.schema,
            )

        try:
            future = self._runner.submit(
                context.sheet,
                f"insight:{signature}",
                _job,
                cache_result=False,
            )
        except Exception:
            self._prefetch_contexts.pop(signature, None)
            self._prefetch_signatures.discard(signature)
            return

        def _on_done(fut):
            try:
                result: JobResult = fut.result()
            except Exception:  # pragma: no cover - defensive
                self._call_soon(lambda sig=signature: self._finalize_prefetch(sig))
                return
            if result.error is not None:
                self._call_soon(lambda sig=signature: self._finalize_prefetch(sig))
                return
            value = result.value
            if not isinstance(value, ColumnInsight):
                self._call_soon(lambda sig=signature: self._finalize_prefetch(sig))
                return
            self._call_soon(
                lambda sig=signature, insight=value: self._finalize_prefetch(sig, insight)
            )

        future.add_done_callback(_on_done)

    def _finalize_prefetch(
        self,
        signature: tuple[str | None, str | None, str],
        insight: ColumnInsight | None = None,
    ) -> None:
        context = self._prefetch_contexts.pop(signature, None)
        self._prefetch_signatures.discard(signature)
        if context is None:
            return
        if insight is not None:
            self._stash_cache_entry(signature, insight)
        self._maybe_schedule_prefetches(self._viewer)

    def _schedule_request(self, context: _InsightRequestContext) -> None:
        delay = max(0, self._debounce_ms) / 1000
        with self._lock:
            self._cancel_timer_locked()
            self._pending_context = context
            if delay <= 0:
                self._launch_pending_locked()
                return
            timer = threading.Timer(delay, self._launch_pending_locked)
            timer.daemon = True
            self._pending_timer = timer
            timer.start()

    def _launch_pending_locked(self) -> None:
        with self._lock:
            context = self._pending_context
            self._pending_context = None
            self._pending_timer = None
        if context is None:
            return

        def _job(_: int) -> ColumnInsight:
            config = ColumnInsightJobConfig(
                column_name=context.column,
                plan_hash=context.plan_hash,
                sheet_id=context.sheet_id,
                source_path=context.source_path,
            )
            lazyframe = (
                context.lazyframe.clone()
                if hasattr(context.lazyframe, "clone")
                else context.lazyframe
            )
            return compute_column_insight(
                lazyframe=lazyframe,
                config=config,
                schema=context.schema,
            )

        signature = context.signature
        try:
            future = self._runner.submit(
                context.sheet,
                f"insight:{signature}",
                _job,
                cache_result=False,
            )
        except Exception as exc:
            self._panel.set_error(str(exc))
            return

        self._inflight_signature = signature

        def _on_done(fut):
            try:
                result: JobResult = fut.result()
            except Exception as exc:  # pragma: no cover - defensive
                self._call_soon(lambda err=exc: self._apply_error(signature, str(err)))
                return
            if result.error is not None:
                self._call_soon(lambda: self._apply_error(signature, str(result.error)))
                return
            value = result.value
            if not isinstance(value, ColumnInsight):
                self._call_soon(lambda: self._apply_error(signature, "unexpected insight result"))
                return
            self._call_soon(lambda: self._apply_result(signature, value))

        future.add_done_callback(_on_done)

    def _apply_result(
        self,
        signature: tuple[str | None, str | None, str],
        insight: ColumnInsight,
    ) -> None:
        with self._lock:
            if signature != self._inflight_signature:
                return
            self._latest_insight = insight
            self._last_signature = signature
            self._inflight_signature = None

        self._panel.set_insight(insight)
        self._invalidate()
        self._record_snapshot()
        self._stash_cache_entry(signature, insight)
        self._maybe_schedule_prefetches(self._viewer)

    def _apply_error(self, signature: tuple[str | None, str | None, str], message: str) -> None:
        with self._lock:
            if signature != self._inflight_signature:
                return
        self._inflight_signature = None
        self._panel.set_error(message)
        self._invalidate()

    def _record_snapshot(self) -> None:
        recorder = self._recorder
        if recorder is None or not recorder.enabled:
            return
        payload = self._panel.snapshot_for_recorder(recorder.cell_redaction_policy)
        recorder.record("insight", payload)

    def _stash_cache_entry(
        self,
        signature: tuple[str | None, str | None, str],
        insight: ColumnInsight,
    ) -> None:
        cache = self._insight_cache
        cache[signature] = insight
        cache.move_to_end(signature)
        while len(cache) > self._cache_limit:
            cache.popitem(last=False)

    def _cancel_pending_locked(self) -> None:
        self._cancel_timer_locked()
        self._pending_context = None
        self._inflight_signature = None
        self._prefetch_signatures.clear()
        self._prefetch_contexts.clear()

    def _cancel_timer_locked(self) -> None:
        timer = self._pending_timer
        if timer is not None:
            timer.cancel()
            self._pending_timer = None


__all__ = ["ColumnInsightController"]

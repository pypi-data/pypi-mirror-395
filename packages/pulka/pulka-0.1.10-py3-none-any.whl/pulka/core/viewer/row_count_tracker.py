# mypy: ignore-errors

"""Row count orchestration helpers for :mod:`pulka.core.viewer`.

The viewer exposes row counts in its status bar and orchestrates background
jobs to compute them. This helper centralises the state machine that used to be
spread throughout :class:`pulka.core.viewer.viewer.Viewer` so it can be tested in
isolation.
"""

from __future__ import annotations

import contextlib
import threading
import weakref
from concurrent.futures import Future
from typing import TYPE_CHECKING

from ..interfaces import JobRunnerProtocol
from ..jobs import JobResult
from .ui_hooks import NullViewerUIHooks

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from .viewer import Viewer


class RowCountTracker:
    """Track and refresh row count metadata for a :class:`Viewer`."""

    def __init__(self, viewer: Viewer, runner: JobRunnerProtocol) -> None:
        self._viewer = viewer
        self._runner = runner

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    @property
    def total_rows(self) -> int | None:
        """Expose the cached total row count."""

        return self._viewer._total_rows

    def invalidate(self) -> None:
        """Mark the cached row count as stale."""

        viewer = self._viewer
        viewer._total_rows = None
        viewer._row_count_stale = True
        viewer._row_count_future = None
        viewer._row_count_display_pending = False
        viewer.mark_status_dirty()
        viewer.invalidate_row_cache()

    def ensure_total_rows(self) -> int | None:
        """Ensure the total row count is up to date and return it."""

        viewer = self._viewer
        total_rows = viewer._total_rows
        if total_rows is not None and not viewer._row_count_stale:
            return total_rows

        sheet_id = getattr(viewer.sheet, "sheet_id", None)
        tag = "row-count"
        runner = self._runner

        if sheet_id is not None:
            cached = runner.get(sheet_id, tag)
            if cached is not None and cached.error is None:
                value = cached.value
                if isinstance(value, int):
                    viewer._total_rows = value
                    viewer._row_count_stale = False
                    viewer._row_count_future = None
                    viewer._row_count_display_pending = False
                    viewer.mark_status_dirty()
                    return viewer._total_rows

        if not hasattr(viewer.sheet, "__len__"):
            return viewer._total_rows

        if sheet_id is None:
            with contextlib.suppress(Exception):
                total = len(viewer.sheet)  # type: ignore[arg-type]
                viewer._total_rows = int(total)
                viewer._row_count_stale = False
                viewer._row_count_display_pending = False
                viewer.mark_status_dirty()
            return viewer._total_rows

        future = viewer._row_count_future
        if future is None or future.done():
            if hasattr(viewer.sheet, "__len__"):
                with contextlib.suppress(Exception):
                    total = len(viewer.sheet)  # type: ignore[arg-type]
                    viewer._total_rows = int(total)
                    viewer._row_count_stale = False
                    viewer._row_count_display_pending = False
                    viewer._row_count_future = None
                    viewer.mark_status_dirty()
                    return viewer._total_rows

            def _compute(_: int, sheet=viewer.sheet) -> int | None:
                with contextlib.suppress(Exception):
                    return int(len(sheet))  # type: ignore[arg-type]
                return None

            submitted = runner.submit(
                viewer.sheet,
                tag,
                _compute,
                cache_result=True,
                priority=1,
            )
            viewer._row_count_future = submitted
            viewer._row_count_display_pending = True

            viewer_ref = weakref.ref(viewer)
            sheet_id_for_job = sheet_id

            def _apply_result(result: JobResult) -> None:
                viewer_obj = viewer_ref()
                if viewer_obj is None:
                    return
                if viewer_obj._row_count_future is not submitted:
                    return
                if result.sheet_id != sheet_id_for_job:
                    return
                if result.error is not None or not isinstance(result.value, int):
                    viewer_obj._row_count_future = None
                    viewer_obj._row_count_stale = True
                    viewer_obj._row_count_display_pending = False
                    viewer_obj.mark_status_dirty()
                    return

                current_gen = runner.current_generation(sheet_id_for_job)
                if result.generation != current_gen:
                    return

                viewer_obj._total_rows = int(result.value)
                viewer_obj._row_count_stale = False
                viewer_obj._row_count_future = None
                viewer_obj._row_count_display_pending = False
                viewer_obj.mark_status_dirty()
                viewer_obj.clamp()

                hooks = viewer_obj.ui_hooks
                with contextlib.suppress(Exception):
                    hooks.invalidate()

            def _on_done(fut: Future[JobResult]) -> None:
                try:
                    result = fut.result()
                except Exception:
                    return

                def _deliver() -> None:
                    _apply_result(result)

                hooks = viewer.ui_hooks
                if isinstance(hooks, NullViewerUIHooks):
                    timer = threading.Timer(0.01, _deliver)
                    timer.daemon = True
                    timer.start()
                else:
                    try:
                        hooks.call_soon(_deliver)
                    except Exception:
                        timer = threading.Timer(0.01, _deliver)
                        timer.daemon = True
                        timer.start()

            submitted.add_done_callback(_on_done)

        return viewer._total_rows

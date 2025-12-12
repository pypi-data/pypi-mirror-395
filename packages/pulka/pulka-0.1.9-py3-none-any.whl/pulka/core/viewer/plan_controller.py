# mypy: ignore-errors

"""Plan mutation helpers for :mod:`pulka.core.viewer`.

The :class:`~pulka.core.viewer.viewer.Viewer` coordinates undo/redo snapshots
and UI side-effects while this helper focuses on the mechanics of compiling and
applying ``QueryPlan`` updates. Isolating the behaviour makes the plan surface
straightforward to test without instantiating the full viewer stack.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from ..engine.viewer_engine import ViewerEngine
from ..errors import PulkaCoreError
from ..row_provider import RowProvider
from ..sheet import SHEET_FEATURE_PLAN, sheet_supports
from .transformation_manager import ChangeResult

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from ...sheets.transformation_history import SupportsSnapshots
    from ..plan import QueryPlan
    from .viewer import Viewer


class PlanController:
    """Encapsulate plan reads and mutations for a :class:`Viewer`."""

    def __init__(self, viewer: Viewer) -> None:
        self._viewer = viewer

    # ------------------------------------------------------------------
    # Plan inspection helpers
    # ------------------------------------------------------------------

    def current_plan(self) -> QueryPlan | None:
        """Return the current plan object when available."""

        plan_attr = getattr(self._viewer.sheet, "plan", None)
        if callable(plan_attr):
            try:
                return plan_attr()
            except PulkaCoreError:
                raise
            except Exception:
                return None
        return plan_attr

    def plan_compiler_for_validation(self) -> Any:
        """Return a plan compiler suitable for validating plan mutations."""

        engine = getattr(self._viewer, "_engine", None)
        if engine is None:
            return None
        try:
            return engine.build_plan_compiler()
        except PulkaCoreError:
            raise
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Plan mutation helpers
    # ------------------------------------------------------------------

    def apply_plan_update(
        self, description: str, builder: Callable[[QueryPlan], QueryPlan]
    ) -> ChangeResult | None:
        """Apply a pure plan update produced by ``builder``."""

        viewer = self._viewer
        if not sheet_supports(viewer.sheet, SHEET_FEATURE_PLAN):
            return None

        current_plan = self.current_plan()
        if current_plan is None:
            return None

        def mutate() -> object | None:
            plan_before = self.current_plan()
            if plan_before is None:
                return False
            new_plan = builder(plan_before)
            if new_plan == plan_before:
                return False
            compiler = self.plan_compiler_for_validation()
            compile_plan = getattr(compiler, "compile", None) if compiler is not None else None
            if callable(compile_plan):
                compile_plan(new_plan)
            new_sheet = viewer.sheet.with_plan(new_plan)
            self._adopt_sheet(new_sheet)
            return None

        return viewer._transformations.record_change(description, mutate)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _adopt_sheet(self, sheet) -> None:
        """Adopt ``sheet`` without resetting viewer-local state."""

        viewer = self._viewer
        previous_columns = tuple(viewer.columns)
        viewer.sheet = sheet
        viewer._schema_cache = getattr(sheet, "schema", viewer._schema_cache)

        new_columns = list(getattr(sheet, "columns", []))
        viewer.columns = new_columns

        provider = getattr(sheet, "row_provider", None)
        if provider is None:
            provider = RowProvider.for_sheet(sheet, runner=viewer.job_runner)
        elif getattr(provider, "_runner", None) is None:
            with contextlib.suppress(Exception):
                provider._runner = viewer.job_runner  # type: ignore[attr-defined]
        viewer._row_provider = provider
        viewer._engine = ViewerEngine(viewer._row_provider)

        sheet_for_history: SupportsSnapshots | None
        if hasattr(sheet, "snapshot_transforms") and hasattr(sheet, "restore_transforms"):
            sheet_for_history = sheet  # type: ignore[assignment]
        else:
            sheet_for_history = None
        viewer._transformations.rebind_sheet(sheet_for_history)

        viewer._sync_hidden_columns_from_plan()
        if tuple(new_columns) != previous_columns:
            viewer._reconcile_schema_changes()

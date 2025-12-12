"""Undo/redo support for sheet transformations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from .query_plan import QueryPlan


class SupportsSnapshots(Protocol):
    """Protocol describing the snapshot interface exposed by sheets."""

    def snapshot_transforms(self) -> QueryPlan: ...

    def restore_transforms(self, snapshot: QueryPlan) -> None: ...


@dataclass(slots=True)
class TransformationSnapshot:
    """Serializable record for a single transformation state."""

    plan: QueryPlan | None
    view_state: Any
    description: str | None


class TransformationHistory:
    """Centralized undo/redo stack shared between viewer and sheets."""

    def __init__(self, sheet: SupportsSnapshots | None) -> None:
        self._sheet = sheet
        self._undo: list[TransformationSnapshot] = []
        self._redo: list[TransformationSnapshot] = []

    # ------------------------------------------------------------------
    # Snapshot lifecycle helpers

    def capture(
        self,
        description: str | None,
        *,
        view_state: Any,
    ) -> TransformationSnapshot:
        """Capture the current plan/view state prior to a change."""

        plan: QueryPlan | None = None
        if self._sheet is not None:
            plan = self._sheet.snapshot_transforms()
        return TransformationSnapshot(plan=plan, view_state=view_state, description=description)

    def commit(self, snapshot: TransformationSnapshot | None) -> None:
        """Push ``snapshot`` onto the undo stack."""

        if snapshot is None:
            return
        self._undo.append(snapshot)
        self._redo.clear()

    # ------------------------------------------------------------------
    # Undo/redo mechanics

    def undo(self, *, current_view_state: Any) -> TransformationSnapshot | None:
        """Restore the most recent snapshot and return it for view reconciliation."""

        if not self._undo:
            return None

        redo_plan: QueryPlan | None = None
        if self._sheet is not None:
            redo_plan = self._sheet.snapshot_transforms()

        current_snapshot = TransformationSnapshot(
            plan=redo_plan,
            view_state=current_view_state,
            description=None,
        )
        self._redo.append(current_snapshot)

        snapshot = self._undo.pop()
        if self._sheet is not None and snapshot.plan is not None:
            self._sheet.restore_transforms(snapshot.plan)
        return snapshot

    def redo(self, *, current_view_state: Any) -> TransformationSnapshot | None:
        """Reapply a snapshot from the redo stack."""

        if not self._redo:
            return None

        undo_plan: QueryPlan | None = None
        if self._sheet is not None:
            undo_plan = self._sheet.snapshot_transforms()

        current_snapshot = TransformationSnapshot(
            plan=undo_plan,
            view_state=current_view_state,
            description=None,
        )
        self._undo.append(current_snapshot)

        snapshot = self._redo.pop()
        if self._sheet is not None and snapshot.plan is not None:
            self._sheet.restore_transforms(snapshot.plan)
        return snapshot

    # ------------------------------------------------------------------
    # Maintenance helpers

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    def filter(self, predicate: Callable[[TransformationSnapshot], bool]) -> None:
        """Remove snapshots for which ``predicate`` returns ``False``."""

        self._undo = [snap for snap in self._undo if predicate(snap)]
        self._redo = [snap for snap in self._redo if predicate(snap)]

    def plan_has_changed_since(self, snapshot: TransformationSnapshot) -> bool:
        """Return ``True`` when the sheet's plan differs from ``snapshot``."""

        if self._sheet is None or snapshot.plan is None:
            return False
        try:
            current_plan = self._sheet.snapshot_transforms()
        except Exception:
            return False
        return current_plan != snapshot.plan

    def rebind(self, sheet: SupportsSnapshots | None) -> None:
        """Update the sheet reference used for future snapshots."""

        self._sheet = sheet

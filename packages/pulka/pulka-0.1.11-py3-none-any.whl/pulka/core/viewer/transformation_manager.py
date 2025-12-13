"""Helpers for coordinating viewer state with transformation history."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ...sheets.transformation_history import (
    SupportsSnapshots,
    TransformationHistory,
    TransformationSnapshot,
)


@dataclass(slots=True)
class ChangeResult:
    """Result returned from :meth:`ViewerTransformationManager.record_change`."""

    committed: bool
    plan_changed: bool
    view_changed: bool


class ViewerTransformationManager:
    """Wrap :class:`TransformationHistory` with viewer-specific helpers."""

    def __init__(
        self,
        history: TransformationHistory,
        *,
        capture_view_state: Callable[[], Any],
        restore_view_state: Callable[[Any], None],
    ) -> None:
        self._history = history
        self._capture_view_state = capture_view_state
        self._restore_view_state = restore_view_state

    @property
    def history(self) -> TransformationHistory:
        """Expose the underlying history instance."""

        return self._history

    def record_change(
        self,
        description: str | None,
        mutate: Callable[[], object | None],
    ) -> ChangeResult:
        """Capture state, run ``mutate``, and persist snapshots when changed.

        Parameters
        ----------
        description:
            Human readable summary used in undo/redo status messages.
        mutate:
            Callable that performs the desired mutation. Returning ``True`` (or any
            truthy value) signals that the viewer state has changed even when the
            underlying sheet plan is unchanged. Returning ``False``/``None``
            indicates that only the sheet mutation should be considered.

        ``mutate`` is invoked exactly once. If it raises, the snapshot is discarded
        and the exception is propagated to the caller.
        """

        snapshot = self._history.capture(description, view_state=self._capture_view_state())

        mutate_result = mutate()

        plan_changed = self._history.plan_has_changed_since(snapshot)
        view_changed = self._coerce_view_change(mutate_result)

        if plan_changed or view_changed:
            self._history.commit(snapshot)
            return ChangeResult(
                committed=True, plan_changed=plan_changed, view_changed=view_changed
            )

        return ChangeResult(committed=False, plan_changed=False, view_changed=view_changed)

    def undo(self) -> TransformationSnapshot | None:
        """Undo the most recent change and restore the viewer state."""

        snapshot = self._history.undo(current_view_state=self._capture_view_state())
        if snapshot is None:
            return None
        self._restore_view_state(snapshot.view_state)
        return snapshot

    def redo(self) -> TransformationSnapshot | None:
        """Redo the most recently undone change and restore the viewer state."""

        snapshot = self._history.redo(current_view_state=self._capture_view_state())
        if snapshot is None:
            return None
        self._restore_view_state(snapshot.view_state)
        return snapshot

    def clear(self) -> None:
        """Reset the undo/redo stacks."""

        self._history.clear()

    def filter_history(self, predicate: Callable[[TransformationSnapshot], bool]) -> None:
        """Filter the stored snapshots using ``predicate``."""

        self._history.filter(predicate)

    def rebind_sheet(self, sheet: SupportsSnapshots | None) -> None:
        """Point the history at ``sheet`` for subsequent snapshots."""

        self._history.rebind(sheet)

    @staticmethod
    def _coerce_view_change(result: object | None) -> bool:
        """Interpret ``mutate`` return value as a view-change flag."""

        if result is None:
            return False
        if isinstance(result, bool):
            return result
        return True

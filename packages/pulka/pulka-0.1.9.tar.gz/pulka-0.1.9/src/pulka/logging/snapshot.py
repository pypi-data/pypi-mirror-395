"""Helpers to extract structured state snapshots for the recorder."""

from __future__ import annotations

import hashlib
from typing import Any

from ..core.viewer import Viewer, ViewerPublicState, viewer_public_state


def viewer_state_snapshot(viewer: Viewer) -> dict[str, Any]:
    """Return a serialisable snapshot of the viewer."""

    sheet = viewer.sheet

    public_state: ViewerPublicState | None = viewer_public_state(viewer)
    if public_state is None:  # pragma: no cover - defensive
        msg = "Viewer snapshot unavailable"
        raise RuntimeError(msg)

    visible_cols = list(public_state.visible_columns or public_state.columns)
    state = {
        "sheet_type": type(sheet).__name__,
        "cursor": {"row": public_state.cursor.row, "col": public_state.cursor.col},
        "viewport": {
            "row0": public_state.viewport.row0,
            "rowN": public_state.viewport.rowN,
            "col0": public_state.viewport.col0,
            "colN": public_state.viewport.colN,
        },
        "visible_cols": visible_cols,
        "highlighted_col": public_state.highlighted_column,
        "sort": {
            "column": public_state.sort_column,
            "ascending": public_state.sort_ascending,
        },
        "filter": public_state.filter_text,
        "hidden_cols": list(public_state.hidden_columns),
        "maximized": {
            "mode": public_state.width_mode,
            "target": public_state.width_target,
            "single": public_state.width_target,
            "all": public_state.all_columns_maximized,
        },
    }
    if hasattr(sheet, "schema") and sheet.schema:
        state["schema"] = {name: str(dtype) for name, dtype in sheet.schema.items()}

    snapshot_getter = getattr(sheet, "plan_snapshot", None)
    if callable(snapshot_getter):
        try:
            plan_snapshot = snapshot_getter()
        except Exception:
            plan_snapshot = None
        if plan_snapshot is not None:
            state["plan"] = plan_snapshot
    return state


def frame_hash(frame_text: str) -> str:
    """Return a stable hash for the rendered frame."""
    data = frame_text.encode("utf-8", "replace")
    return hashlib.sha256(data).hexdigest()


__all__ = ["viewer_state_snapshot", "frame_hash"]

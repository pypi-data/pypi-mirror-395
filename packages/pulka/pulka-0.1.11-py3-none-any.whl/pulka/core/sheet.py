"""Definition of the core sheet protocol."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final, Literal, Protocol, runtime_checkable

from .engine.contracts import TableSlice
from .plan import QueryPlan

TabularData = TableSlice | Mapping[str, Sequence[Any]] | Sequence[Mapping[str, Any]]
"""Engine-neutral representation for tabular preview results."""


SheetFeature = Literal[
    "plan",
    "preview",
    "slice",
    "value-at",
    "row-count",
    "legacy-preview",
]
"""Named capability flags that sheet implementations may expose."""

SHEET_FEATURE_PLAN: Final[SheetFeature] = "plan"
SHEET_FEATURE_PREVIEW: Final[SheetFeature] = "preview"
SHEET_FEATURE_SLICE: Final[SheetFeature] = "slice"
SHEET_FEATURE_VALUE_AT: Final[SheetFeature] = "value-at"
SHEET_FEATURE_ROW_COUNT: Final[SheetFeature] = "row-count"
SHEET_FEATURE_LEGACY_PREVIEW: Final[SheetFeature] = "legacy-preview"


class Sheet(Protocol):
    """Minimal interface implemented by data sheets."""

    @property
    def columns(self) -> list[str]: ...

    def schema_dict(self) -> Mapping[str, Any]: ...

    def plan_snapshot(self) -> Mapping[str, object]: ...

    @property
    def plan(self) -> QueryPlan: ...

    def with_plan(self, plan: QueryPlan) -> Sheet: ...

    def fetch_slice(
        self,
        row_start: int,
        row_count: int,
        columns: Sequence[str],
    ) -> TableSlice: ...

    def preview(self, rows: int, cols: Sequence[str] | None = None) -> TableSlice: ...

    def value_at(self, row: int, col: str) -> object:  # noqa: ANN401 - heterogenous return
        ...

    def row_count(self) -> int | None: ...

    def supports(self, feature: SheetFeature, /) -> bool:
        """Return whether ``feature`` is supported by this sheet."""


@runtime_checkable
class SupportsLegacyPreview(Protocol):
    """Optional shim for callers that still expect DataFrame previews."""

    def preview_dataframe(self, rows: int, cols: Sequence[str] | None = None) -> Any: ...


def sheet_supports(sheet: object, feature: SheetFeature) -> bool:
    """Return whether ``sheet`` advertises support for ``feature``.

    The helper defers to ``sheet.supports`` when available and falls back to
    best-effort duck-typing for legacy implementations.
    """

    supports = getattr(sheet, "supports", None)
    if callable(supports):
        try:
            return bool(supports(feature))
        except Exception:
            return False

    if feature == SHEET_FEATURE_PLAN:
        return hasattr(sheet, "plan") and hasattr(sheet, "with_plan")
    if feature == SHEET_FEATURE_PREVIEW:
        return hasattr(sheet, "preview")
    if feature == SHEET_FEATURE_SLICE:
        return hasattr(sheet, "fetch_slice")
    if feature == SHEET_FEATURE_VALUE_AT:
        return hasattr(sheet, "value_at") or hasattr(sheet, "get_value_at")
    if feature == SHEET_FEATURE_ROW_COUNT:
        return hasattr(sheet, "row_count")
    if feature == SHEET_FEATURE_LEGACY_PREVIEW:
        return isinstance(sheet, SupportsLegacyPreview)
    return False


__all__ = [
    "Sheet",
    "SheetFeature",
    "SupportsLegacyPreview",
    "TabularData",
    "SHEET_FEATURE_PLAN",
    "SHEET_FEATURE_PREVIEW",
    "SHEET_FEATURE_SLICE",
    "SHEET_FEATURE_VALUE_AT",
    "SHEET_FEATURE_ROW_COUNT",
    "SHEET_FEATURE_LEGACY_PREVIEW",
    "sheet_supports",
]

import polars as pl

from pulka.core.sheet import (
    SHEET_FEATURE_LEGACY_PREVIEW,
    SHEET_FEATURE_PLAN,
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    sheet_supports,
)
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.hist_sheet import HistogramSheet


def test_data_sheet_reports_core_capabilities(job_runner) -> None:
    lf = pl.DataFrame({"a": [1, 2], "b": ["x", "y"]}).lazy()
    sheet = DataSheet(lf, runner=job_runner)

    for feature in (
        SHEET_FEATURE_PLAN,
        SHEET_FEATURE_PREVIEW,
        SHEET_FEATURE_SLICE,
        SHEET_FEATURE_VALUE_AT,
        SHEET_FEATURE_ROW_COUNT,
        SHEET_FEATURE_LEGACY_PREVIEW,
    ):
        assert sheet.supports(feature)
        assert sheet_supports(sheet, feature)


def test_histogram_sheet_capabilities(job_runner) -> None:
    base = DataSheet(pl.DataFrame({"value": [1, 2, 3]}).lazy(), runner=job_runner)
    hist = HistogramSheet(base, "value", runner=job_runner)

    assert hist.supports(SHEET_FEATURE_SLICE)
    assert hist.supports(SHEET_FEATURE_VALUE_AT)
    assert not hist.supports(SHEET_FEATURE_PLAN)
    assert not sheet_supports(hist, SHEET_FEATURE_PREVIEW)


def test_sheet_supports_falls_back_to_duck_typing() -> None:
    class LegacySheet:
        columns = ["a"]

        def fetch_slice(self, row_start: int, row_count: int, columns: list[str]):
            return None

    class LegacyPreview:
        def preview_dataframe(self, rows: int, cols=None):
            return None

    legacy = LegacySheet()
    legacy_preview = LegacyPreview()

    assert sheet_supports(legacy, SHEET_FEATURE_SLICE)
    assert not sheet_supports(legacy, SHEET_FEATURE_PLAN)
    assert sheet_supports(legacy_preview, SHEET_FEATURE_LEGACY_PREVIEW)

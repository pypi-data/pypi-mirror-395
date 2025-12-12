"""Helpers for building derived views and lazy frames used across Pulka."""

from __future__ import annotations

import polars as pl

from .core.engine.polars_adapter import unwrap_lazyframe_handle
from .core.viewer import Viewer


def build_column_summary_lazy(viewer: Viewer) -> pl.LazyFrame:
    """Return a lazy frame containing per-column summary statistics."""
    session = viewer.session
    if session is not None:
        try:
            summary_sheet = session.sheets.create("summary", viewer.sheet, runner=viewer.job_runner)
        except KeyError:  # pragma: no cover - plugin disabled
            from pulka_builtin_plugins.summary import SummarySheet as _SummarySheet

            summary_sheet = _SummarySheet(viewer.sheet, runner=viewer.job_runner)
    else:
        from pulka_builtin_plugins.summary import SummarySheet as _SummarySheet

        summary_sheet = _SummarySheet(viewer.sheet, runner=viewer.job_runner)

    return unwrap_lazyframe_handle(summary_sheet.lf)


def build_freq_lazy(viewer: Viewer, colname: str) -> pl.LazyFrame:
    """Return a lazy frame representing value frequencies for ``colname``."""
    session = viewer.session
    if session is not None:
        try:
            freq_sheet = session.sheets.create(
                "freq", viewer.sheet, colname, runner=viewer.job_runner
            )
        except KeyError:  # pragma: no cover - plugin disabled
            from pulka_builtin_plugins.freq import FreqSheet as _FreqSheet

            freq_sheet = _FreqSheet(viewer.sheet, colname, runner=viewer.job_runner)
    else:
        from pulka_builtin_plugins.freq import FreqSheet as _FreqSheet

        freq_sheet = _FreqSheet(viewer.sheet, colname, runner=viewer.job_runner)

    return unwrap_lazyframe_handle(freq_sheet.lf)


def build_transpose_df(
    viewer: Viewer, sample_rows: int | None = None
) -> tuple[pl.DataFrame, int, int]:
    """Build a transposed DataFrame and report sample sizes.

    Returns a tuple of ``(dataframe, actual_sample_rows, requested_sample_rows)`` to
    mirror the legacy helper that powered scripted mode.
    """
    session = viewer.session
    if session is not None:
        try:
            transpose_sheet = session.sheets.create(
                "transpose", viewer.sheet, sample_rows, runner=viewer.job_runner
            )
        except KeyError:  # pragma: no cover - plugin disabled
            from pulka_builtin_plugins.transpose import TransposeSheet as _TransposeSheet

            transpose_sheet = _TransposeSheet(viewer.sheet, sample_rows, runner=viewer.job_runner)
    else:
        from pulka_builtin_plugins.transpose import TransposeSheet as _TransposeSheet

        transpose_sheet = _TransposeSheet(viewer.sheet, sample_rows, runner=viewer.job_runner)
    df = unwrap_lazyframe_handle(transpose_sheet.lf).collect()
    actual = getattr(transpose_sheet, "actual_sample_rows", df.height)
    requested = (
        transpose_sheet.requested_sample_rows
        if getattr(transpose_sheet, "requested_sample_rows", None) is not None
        else actual
    )
    return df, actual, requested


__all__ = [
    "build_column_summary_lazy",
    "build_freq_lazy",
    "build_transpose_df",
]

"""Utilities to extract reproducible data slices from the active viewer."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

from ..api.session import Session
from ..core.engine.contracts import EnginePayloadHandle, TableSlice
from ..core.engine.polars_adapter import (
    dataframe_from_table_slice,
    unwrap_lazyframe_handle,
)
from ..core.plan import QueryPlan
from ..core.plan_ops import set_projection as plan_set_projection

if TYPE_CHECKING:
    from ..logging.redaction import RedactionPolicy


def build_repro_slice(
    session: Session, *, row_margin: int = 10, include_all_columns: bool = False
) -> pl.DataFrame:
    """Build a reproducible slice of the active sheet data for export.

    Args:
        session: The active session to extract data from.
        row_margin: Number of rows to include above/below the current viewport.
        include_all_columns: If True, export all columns; if False, only visible ones.

    Returns:
        DataFrame containing the extracted data slice.

    Raises:
        ValueError: If the active sheet doesn't have a lazy_frame attribute.
        RuntimeError: If the dataset is in-memory or synthetic (not backed by a file).

    Note:
        This function works with LazyFrame-backed datasets only. It respects
        existing filters and sorts applied to the sheet, and extracts a slice
        around the current viewport with the specified margin.
    """
    viewer = session.viewer
    sheet = viewer.sheet

    # Check if the sheet has LazyFrame support
    # DataSheet instances have 'lf' attribute
    if hasattr(sheet, "lf"):
        # DataSheet case: use the current lazy frame
        lf_candidate = sheet.lf
        if isinstance(lf_candidate, EnginePayloadHandle):
            lf = unwrap_lazyframe_handle(lf_candidate)
        elif isinstance(lf_candidate, pl.LazyFrame):
            lf = lf_candidate
        else:
            raise TypeError(
                "Repro export expected a Polars LazyFrame or EnginePayloadHandle, "
                f"but got {type(lf_candidate)!r}"
            )
    else:
        raise RuntimeError(
            "Repro export only works with LazyFrame-backed datasets, "
            f"but got {type(sheet).__name__}"
        )

    # Determine viewport bounds
    viewport_top = viewer.row0
    viewport_bottom = (
        min(viewer.row0 + viewer.view_height, len(sheet))
        if hasattr(sheet, "__len__")
        else viewer.row0 + viewer.view_height
    )

    # Calculate slice bounds with margin
    slice_start = max(0, viewport_top - row_margin)
    slice_end = viewport_bottom + row_margin

    # Get total row count to clamp properly
    total_rows = len(sheet) if hasattr(sheet, "__len__") else lf.select(pl.len()).collect().item()
    slice_end = min(slice_end, total_rows)

    plan_obj = getattr(sheet, "plan", None)
    if callable(plan_obj):
        plan_obj = plan_obj()

    if isinstance(plan_obj, QueryPlan):
        projected_columns = list(plan_obj.projection_or(viewer.columns))
    else:
        projected_columns = list(viewer.visible_cols)

    export_columns = list(viewer.columns) if include_all_columns else projected_columns

    row_provider = getattr(sheet, "row_provider", None)
    if isinstance(plan_obj, QueryPlan) and hasattr(row_provider, "get_slice"):
        slice_length = max(0, slice_end - slice_start)
        plan_for_export = plan_set_projection(plan_obj, export_columns)
        slice_result, _status = row_provider.get_slice(
            plan_for_export,
            export_columns,
            slice_start,
            slice_length,
        )
        if isinstance(slice_result, TableSlice):
            return dataframe_from_table_slice(slice_result)
        return slice_result

    # Fallback to LazyFrame slicing when row provider is unavailable
    available_columns = list(getattr(lf, "schema", {}).keys())
    columns_to_select = [
        col for col in export_columns if not available_columns or col in available_columns
    ]
    sliced_lf = lf.slice(slice_start, slice_end - slice_start).select(columns_to_select)
    return sliced_lf.collect()


def write_repro_parquet(
    df: pl.DataFrame | TableSlice,
    destination: str | Path,
    policy: RedactionPolicy,
) -> None:
    """Write a DataFrame to Parquet with redaction policy applied.

    Args:
        df: The DataFrame to export.
        destination: Path where the Parquet file should be written.
        policy: The redaction policy to apply to string columns.

    Note:
        Applies redaction to string columns according to the specified policy.
        For HashStringsPolicy, replaces values with their digest info.
        For MaskPatternsPolicy, applies masking patterns to values.
        Preserves original column names/dtypes where possible.
    """
    from ..logging.redaction import (
        HashStringsPolicy,
        MaskPatternsPolicy,
        NoRedactionPolicy,
    )

    if isinstance(df, TableSlice):
        df = dataframe_from_table_slice(df)

    # Apply redaction to string columns based on the policy
    redacted_df = df.clone()

    for col_name in df.columns:
        col_dtype = df.schema[col_name]

        # Only apply redaction to string columns
        if col_dtype in [pl.Utf8, pl.String]:
            original_series = df[col_name]

            if isinstance(policy, HashStringsPolicy):
                # For HashStringsPolicy: convert each value to {hash, length} dict
                redacted_values = []
                for value in original_series:
                    if value is None or (isinstance(value, str) and value == ""):
                        redacted_values.append({"hash": "", "length": 0})
                    else:
                        import hashlib

                        hash_val = hashlib.sha1(str(value).encode("utf-8")).hexdigest()
                        redacted_values.append({"hash": hash_val, "length": len(str(value))})

                # Create a new struct column with hash/length info
                redacted_df = redacted_df.with_columns(
                    pl.Series(
                        col_name,
                        redacted_values,
                        dtype=pl.Struct([pl.Field("hash", pl.Utf8), pl.Field("length", pl.Int64)]),
                    )
                )

            elif isinstance(policy, MaskPatternsPolicy):
                # For MaskPatternsPolicy: apply masking patterns to the values
                redacted_values = []
                for value in original_series:
                    if value is None:
                        redacted_values.append(value)
                    else:
                        redacted_str = policy.apply_to_value(str(value))
                        redacted_values.append(redacted_str)

                redacted_df = redacted_df.with_columns(
                    pl.Series(col_name, redacted_values, dtype=col_dtype)
                )

            elif isinstance(policy, NoRedactionPolicy):
                # For NoRedactionPolicy: keep values unchanged
                pass

    # Write the redacted DataFrame to Parquet
    redacted_df.write_parquet(destination, compression="zstd", statistics=True)


def get_redacted_df_for_policy(df: pl.DataFrame, policy: RedactionPolicy) -> pl.DataFrame:
    """Helper to apply redaction policy to a DataFrame without writing to disk.

    Args:
        df: The DataFrame to redact.
        policy: The redaction policy to apply to string columns.

    Returns:
        A new DataFrame with redaction applied.
    """
    from ..logging.redaction import (
        HashStringsPolicy,
        MaskPatternsPolicy,
        NoRedactionPolicy,
    )

    # Apply redaction to string columns based on the policy
    redacted_df = df.clone()

    for col_name in df.columns:
        col_dtype = df.schema[col_name]

        # Only apply redaction to string columns
        if col_dtype in [pl.Utf8, pl.String]:
            original_series = df[col_name]

            if isinstance(policy, HashStringsPolicy):
                # For HashStringsPolicy: convert each value to {hash, length} dict
                redacted_values = []
                for value in original_series:
                    if value is None or (isinstance(value, str) and value == ""):
                        redacted_values.append(
                            {"hash": "", "length": 0} if value is not None else None
                        )
                    else:
                        import hashlib

                        hash_val = hashlib.sha1(str(value).encode("utf-8")).hexdigest()
                        redacted_values.append({"hash": hash_val, "length": len(str(value))})

                # Create a new struct column with hash/length info
                redacted_df = redacted_df.with_columns(
                    pl.Series(
                        col_name,
                        redacted_values,
                        dtype=pl.Struct([pl.Field("hash", pl.Utf8), pl.Field("length", pl.Int64)]),
                    )
                )

            elif isinstance(policy, MaskPatternsPolicy):
                # For MaskPatternsPolicy: apply masking patterns to the values
                redacted_values = []
                for value in original_series:
                    if value is None:
                        redacted_values.append(value)
                    else:
                        redacted_str = policy.apply_to_value(str(value))
                        redacted_values.append(redacted_str)

                redacted_df = redacted_df.with_columns(
                    pl.Series(col_name, redacted_values, dtype=col_dtype)
                )

            elif isinstance(policy, NoRedactionPolicy):
                # For NoRedactionPolicy: keep values unchanged
                pass

    return redacted_df

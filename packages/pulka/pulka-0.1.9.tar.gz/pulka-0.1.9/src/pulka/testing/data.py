"""
Test data generation utilities for Pulka testing.

This module provides utilities for creating deterministic test datasets
and writing them to various formats with consistent options.
"""

from __future__ import annotations

import random
from datetime import date, datetime
from pathlib import Path
from typing import Any

import polars as pl


def _get_dtype_name(i: int) -> str:
    """Get dtype name for column index."""
    dtype_names = [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint32",
        "float32",
        "float64",
        "bool",
        "string",
        "date",
        "datetime",
        "duration",
        "binary",
        "categorical",
        "decimal",
    ]
    return dtype_names[i % len(dtype_names)]


def make_df(
    fixture_type: str, *, rows: int | None = None, cols: int | None = None, seed: int = 42
) -> pl.DataFrame:
    """
    Create a test DataFrame based on fixture type.

    Args:
        fixture_type: Type of fixture ('mini_nav', 'wide_20cols', 'strings_edge')
        rows: Number of rows (uses fixture default if None)
        cols: Number of columns (uses fixture default if None)
        seed: Random seed for reproducible results

    Returns:
        Generated DataFrame
    """
    rng = random.Random(seed)

    if fixture_type == "mini_nav":
        # Small navigation test data with comprehensive dtypes: 40x8
        actual_rows = rows or 40
        actual_cols = cols or 8
        data: dict[str, Any] = {}

        # Generate different column types with nulls
        for i in range(actual_cols):
            col_name = f"col_{i:02d}"

            if i == 0:
                # ID column (integer, no nulls)
                data[col_name] = list(range(actual_rows))
            elif i == 1:
                # Category column (string with nulls)
                categories = ["alpha", "beta", "gamma", "delta", "epsilon", None]
                data[col_name] = [categories[j % len(categories)] for j in range(actual_rows)]
            elif i == 2:
                # Float column (with nulls)
                data[col_name] = [
                    None if j % 7 == 0 else round(rng.random() * 100, 2) for j in range(actual_rows)
                ]
            elif i == 3:
                # Boolean column (with nulls)
                data[col_name] = [None if j % 11 == 0 else (j % 3 == 0) for j in range(actual_rows)]
            elif i == 4:
                # Date column (with nulls)
                data[col_name] = [
                    None if j % 9 == 0 else date(2024, 1, (j % 28) + 1) for j in range(actual_rows)
                ]
            elif i == 5:
                # Datetime column (with nulls)
                data[col_name] = [
                    None if j % 13 == 0 else datetime(2024, 1, (j % 28) + 1, j % 24, (j * 15) % 60)
                    for j in range(actual_rows)
                ]
            elif i == 6:
                # Large integer column (with nulls)
                data[col_name] = [
                    None if j % 8 == 0 else j * 1000000 + rng.randint(0, 999999)
                    for j in range(actual_rows)
                ]
            else:
                # String columns (with nulls)
                data[col_name] = [
                    None if j % 6 == 0 else f"val_{i}_{j}" for j in range(actual_rows)
                ]

        return pl.DataFrame(data)

    elif fixture_type == "wide_datatypes":
        # Wide test data with comprehensive Polars dtypes: 10x15
        actual_rows = rows or 10
        actual_cols = cols or 15
        data = {}

        for i in range(actual_cols):
            dtype_name = _get_dtype_name(i)
            col_name = f"{dtype_name}_col"

            if i == 0:
                # Int8 column
                data[col_name] = [None if j % 7 == 0 else j * 10 for j in range(actual_rows)]
            elif i == 1:
                # Int16 column
                data[col_name] = [None if j % 8 == 0 else j * 1000 for j in range(actual_rows)]
            elif i == 2:
                # Int32 column
                data[col_name] = [None if j % 6 == 0 else j * 100000 for j in range(actual_rows)]
            elif i == 3:
                # Int64 column
                data[col_name] = [None if j % 9 == 0 else j * 10000000 for j in range(actual_rows)]
            elif i == 4:
                # UInt32 column
                data[col_name] = [
                    None if j % 7 == 0 else abs(j * 50000) for j in range(actual_rows)
                ]
            elif i == 5:
                # Float32 column
                data[col_name] = [
                    None if j % 5 == 0 else round(rng.random() * 1000, 2)
                    for j in range(actual_rows)
                ]
            elif i == 6:
                # Float64 column
                data[col_name] = [
                    None if j % 6 == 0 else rng.random() * 1000000 for j in range(actual_rows)
                ]
            elif i == 7:
                # Boolean column
                data[col_name] = [None if j % 4 == 0 else j % 2 == 0 for j in range(actual_rows)]
            elif i == 8:
                # String column
                data[col_name] = [
                    None if j % 5 == 0 else f"string_{j}_{chr(65 + j % 26)}"
                    for j in range(actual_rows)
                ]
            elif i == 9:
                # Date column
                data[col_name] = [
                    None if j % 8 == 0 else date(2024, (j % 12) + 1, (j % 28) + 1)
                    for j in range(actual_rows)
                ]
            elif i == 10:
                # Datetime column
                data[col_name] = [
                    None
                    if j % 7 == 0
                    else datetime(2024, 1, (j % 28) + 1, j % 24, (j * 15) % 60, (j * 30) % 60)
                    for j in range(actual_rows)
                ]
            elif i == 11:
                # Duration column (as string representation for CSV compatibility)
                data[col_name] = [
                    None if j % 6 == 0 else f"{j}h{j * 10}m{j * 5}s" for j in range(actual_rows)
                ]
            elif i == 12:
                # Binary column (as hex string for CSV compatibility)
                data[col_name] = [
                    None if j % 9 == 0 else f"binary_data_{j}".encode().hex()
                    for j in range(actual_rows)
                ]
            elif i == 13:
                # Categorical column
                categories = ["cat_A", "cat_B", "cat_C", "cat_D", "cat_E"]
                data[col_name] = [
                    None if j % 5 == 0 else categories[j % len(categories)]
                    for j in range(actual_rows)
                ]
            else:
                # Decimal/numeric column
                data[col_name] = [
                    None if j % 7 == 0 else round(rng.random() * 999.99, 4)
                    for j in range(actual_rows)
                ]

        # Create DataFrame and apply proper dtypes
        df = pl.DataFrame(data)

        # Apply specific dtypes where needed
        dtype_casts = {}
        for i in range(actual_cols):
            dtype_name = _get_dtype_name(i)
            col_name = f"{dtype_name}_col"

            if i == 13:  # Categorical
                dtype_casts[col_name] = pl.Categorical

        if dtype_casts:
            df = df.cast(dtype_casts)

        return df

    elif fixture_type == "strings_edge":
        # Edge case strings: 10x3
        actual_rows = rows or 10

        # Column with various string edge cases
        edge_strings = [
            "normal_string",
            "string with spaces",
            "string\twith\ttabs",
            "string\nwith\nnewlines",
            "string,with,commas",
            'string"with"quotes',
            "string'with'apostrophes",
            "unicode_μñíçødé",
            "",  # empty string
            "very_long_string_" * 10,  # long string
        ]

        # Repeat pattern to fill rows
        col1_data = [edge_strings[i % len(edge_strings)] for i in range(actual_rows)]
        col2_data = [f"index_{i}" for i in range(actual_rows)]
        col3_data = [len(s) for s in col1_data]

        return pl.DataFrame(
            {
                "edge_strings": col1_data,
                "index_ref": col2_data,
                "str_length": col3_data,
            }
        )

    else:
        raise ValueError(f"Unknown fixture type: {fixture_type}")


def write_df(df: pl.DataFrame, path: Path, format: str) -> None:
    """
    Write DataFrame to file with deterministic options.

    Args:
        df: DataFrame to write
        path: Output file path
        format: Output format ('csv', 'parquet')
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == "csv":
        df.write_csv(path)
    elif format.lower() == "parquet":
        # Use deterministic options for consistent results across machines
        df.write_parquet(
            path,
            compression="snappy",
            use_pyarrow=True,
            statistics=True,
            row_group_size=None,  # Use default
        )
    else:
        raise ValueError(f"Unsupported format: {format}. Only 'csv' and 'parquet' are supported.")


def get_fixture_info(fixture_type: str) -> dict[str, Any]:
    """
    Get default information about a fixture type.

    Args:
        fixture_type: Type of fixture

    Returns:
        Dictionary with fixture metadata
    """
    fixtures = {
        "mini_nav": {
            "description": "Small navigation test with comprehensive dtypes and nulls",
            "default_rows": 40,
            "default_cols": 8,
            "formats": ["csv", "parquet"],
        },
        "wide_datatypes": {
            "description": "Wide table with all major Polars dtypes",
            "default_rows": 10,
            "default_cols": 15,
            "formats": ["csv", "parquet"],
        },
        "strings_edge": {
            "description": "String edge cases and parser tests",
            "default_rows": 10,
            "default_cols": 3,
            "formats": ["csv"],  # Only CSV for parser edge cases
        },
    }

    if fixture_type not in fixtures:
        raise ValueError(f"Unknown fixture type: {fixture_type}")

    return fixtures[fixture_type]

# mypy: ignore-errors

"""
Data formatting utilities for Pulka.

This module provides dtype-aware formatting helpers for rendering values in a
human-readable form, including number formatting, truncation, and type-specific
representation.
"""

from __future__ import annotations

from collections.abc import Mapping
from collections.abc import Sequence as SeqABC
from itertools import islice

import polars as pl

# Constants for recursion depth and formatting
_MAX_DEPTH = 2
_HISTORY_MAX_SIZE = 20
_SMALL_CARDINALITY_THRESHOLD = 100
_K_VALUE = 1000
_M_VALUE = 1000000
_B_VALUE = 1000000000


def _is_string_dtype(dtype: pl.DataType) -> bool:
    if hasattr(pl.datatypes, "is_string"):
        return pl.datatypes.is_string(dtype)  # type: ignore[attr-defined]
    return dtype in {pl.datatypes.String, pl.datatypes.Utf8}


def _is_numeric_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_numeric", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    numeric_names = {
        "Int8",
        "Int16",
        "Int32",
        "Int64",
        "UInt8",
        "UInt16",
        "UInt32",
        "UInt64",
        "Float32",
        "Float64",
        "Decimal",
    }
    return type(dtype).__name__ in numeric_names or str(dtype).startswith("Decimal")


def _is_temporal_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_temporal", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    temporal_names = {"Date", "Datetime", "Time", "Duration"}
    return type(dtype).__name__ in temporal_names


def _is_boolean_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_boolean", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    return type(dtype).__name__ == "Boolean"


def _is_list_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_list", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    return type(dtype).__name__ == "List"


def _is_array_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_array", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    return type(dtype).__name__ == "Array"


def _is_struct_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_struct", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    return type(dtype).__name__ == "Struct"


def _is_nested_dtype(dtype: pl.DataType) -> bool:
    fn = getattr(pl.datatypes, "is_nested", None)
    if fn is not None:
        try:
            return bool(fn(dtype))
        except Exception:
            return False
    return _is_list_dtype(dtype) or _is_struct_dtype(dtype) or _is_array_dtype(dtype)


def _supports_min_max(dtype: pl.DataType) -> bool:
    return (
        _is_numeric_dtype(dtype)
        or _is_temporal_dtype(dtype)
        or _is_string_dtype(dtype)
        or _is_boolean_dtype(dtype)
    )


def _supports_numeric_stats(dtype: pl.DataType) -> bool:
    # Restrict to primitive numeric types (skip temporal/duration dtypes).
    return _is_numeric_dtype(dtype) and not _is_temporal_dtype(dtype)


def _truncate(s: str, max_chars: int) -> str:
    if max_chars is None or max_chars <= 0:
        return s
    return s if len(s) <= max_chars else s[: max(1, max_chars - 1)] + "…"


def _format_number_with_thousands_separator(num: int) -> str:
    """Format a number with thousands separators."""
    # Format with commas as thousand separators
    return f"{num:,}"


def _format_large_number_compact(num: int) -> str:
    """Format large numbers in compact form (e.g., 1.2M, 3.4B)."""
    if num < _K_VALUE:
        return str(num)
    elif num < _M_VALUE:
        return f"{num / _K_VALUE:.1f}K".rstrip("0").rstrip(".")
    elif num < _B_VALUE:
        return f"{num / _M_VALUE:.1f}M".rstrip("0").rstrip(".")
    else:
        return f"{num / _B_VALUE:.1f}B".rstrip("0").rstrip(".")


def _one_line_repr(obj, *, max_items: int = 5, max_chars: int = 80, _depth: int = 0) -> str:
    # Cap recursion depth to keep this cheap
    if _depth > _MAX_DEPTH:
        try:
            return _truncate(str(obj), max_chars)
        except Exception:
            return "…"
    if obj is None:
        return ""
    # Polars nested values (e.g., List cell yields a Series)
    if isinstance(obj, pl.Series):
        m = max(1, max_items)
        try:
            total = int(obj.len())
        except Exception:
            total = None
        try:
            preview = obj.head(m).to_list()
        except Exception:
            preview = []
        parts = [
            _one_line_repr(x, max_items=max_items, max_chars=max_chars // 2, _depth=_depth + 1)
            for x in preview
        ]
        if (total is not None and total > m) or (total is None and len(preview) >= m):
            parts.append("…")
        s = "[" + ", ".join(parts) + "]"
        s = s.replace("\n", " ")
        return _truncate(s, max_chars)
    if isinstance(obj, str):
        s = obj.replace("\n", " ").replace("\r", " ")
        return _truncate(s, max_chars)
    if isinstance(obj, float):
        try:
            # Adaptive formatting: 6 significant digits, scientific for very small/large
            s = f"{obj:.6g}"
        except Exception:
            s = str(obj)
        return s
    if isinstance(obj, (int, bool)):
        return str(obj)
    if isinstance(obj, (bytes, bytearray)):
        try:
            # Use Python's repr for parity with Polars output and other complex types.
            rendered = repr(obj)
        except Exception:
            rendered = f"<{len(obj)} bytes>"
        rendered = rendered.replace("\n", " ").replace("\r", " ")
        return _truncate(rendered, max_chars)
    # Dict-like (e.g., struct)
    if isinstance(obj, Mapping):
        m = max(1, max_items)
        parts: list[str] = []
        over = False
        for _i, (k, v) in enumerate(islice(obj.items(), m)):
            max_chars_v = max_chars // 2
            repr_v = _one_line_repr(
                v, max_items=max_items, max_chars=max_chars_v, _depth=_depth + 1
            )
            parts.append(f"{k}: {repr_v}")
        # detect overflow cheaply
        try:
            next(islice(obj.items(), m, m + 1))
            over = True
        except StopIteration:
            over = False
        except Exception:
            over = False
        if over:
            parts.append("…")
        s = "{" + ", ".join(parts) + "}"
        s = s.replace("\n", " ")
        return _truncate(s, max_chars)
    # Sequence-like (lists/arrays/tuples); but avoid treating str/bytes as seq due to above checks.
    if isinstance(obj, SeqABC) and not isinstance(obj, (str, bytes, bytearray)):
        m = max(1, max_items)
        parts: list[str] = []
        seq_iter = iter(obj)
        for x in islice(seq_iter, m):
            parts.append(
                _one_line_repr(x, max_items=max_items, max_chars=max_chars // 2, _depth=_depth + 1)
            )
        over = False
        try:
            next(seq_iter)
            over = True
        except StopIteration:
            over = False
        except Exception:
            over = False
        if over:
            parts.append("…")
        s = "[" + ", ".join(parts) + "]"
        s = s.replace("\n", " ")
        return _truncate(s, max_chars)
    # Fallback
    try:
        s = str(obj)
    except Exception:
        s = repr(obj)
    s = s.replace("\n", " ").replace("\r", " ")
    return _truncate(s, max_chars)


def _polars_format_with_dtype(
    series: pl.Series, *, max_items: int = 4, max_chars: int = 80
) -> list[str]:
    """
    Format a Polars Series to string representations based on its data type for optimal performance.
    """
    dtype = series.dtype

    # Handle different Polars dtypes efficiently
    if dtype == pl.Null:
        return [""] * len(series)
    elif dtype in [pl.String, pl.Utf8]:
        # For string types, apply truncation efficiently
        try:
            # Replace newlines with spaces
            clean_series = series.str.replace("\n", " ").str.replace("\r", " ")
            # Truncate to max_chars if specified
            if max_chars and max_chars > 0:
                truncated = clean_series.str.slice(0, max_chars - 1).fill_null(
                    ""
                ) + clean_series.str.slice(max_chars - 1).apply(
                    lambda x: "…" if x and len(x) > (max_chars - 1) else ""
                )
                return truncated.to_list()
            else:
                return clean_series.fill_null("").to_list()
        except Exception:
            return [
                s.replace("\n", " ").replace("\r", " ")[:max_chars] + "…"
                if len(s) > max_chars
                else s
                for s in series.fill_null("").to_list()
            ]
    elif dtype in [
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    ]:
        # For integer types, convert directly to string
        return series.cast(pl.String).fill_null("").to_list()
    elif dtype in [pl.Float32, pl.Float64]:
        # For float types, use scientific notation for very large/small numbers
        try:
            # Convert to Python list and handle each value with proper formatting
            float_values = series.to_list()
            formatted = []
            for val in float_values:
                if val is None:
                    formatted.append("")
                elif isinstance(val, float):
                    try:
                        s = f"{val:.6g}"
                        formatted.append(s)
                    except Exception:
                        formatted.append(str(val))
                else:
                    formatted.append(str(val))
            return formatted
        except Exception:
            return [
                f"{val:.6g}" if isinstance(val, float) else str(val) for val in series.to_list()
            ]
    elif dtype == pl.Boolean:
        # For boolean types, convert to string
        return series.cast(pl.String).fill_null("").to_list()
    elif _is_temporal_dtype(dtype):
        # For temporal types, convert to string with appropriate format
        try:
            return series.cast(pl.String).fill_null("").to_list()
        except Exception:
            # Fallback: use Python formatting
            values = series.to_list()
            return [_one_line_repr(val, max_items=max_items, max_chars=max_chars) for val in values]
    elif _is_nested_dtype(dtype):
        # For nested types (List, Struct, Array), use the element-wise approach
        values = series.to_list()
        return [_one_line_repr(val, max_items=max_items, max_chars=max_chars) for val in values]
    else:
        # For other types, use the general conversion
        values = series.to_list()
        return [_one_line_repr(val, max_items=max_items, max_chars=max_chars) for val in values]


def _format_transpose_value(val: object) -> str | None:
    if val is None:
        return None
    try:
        return _one_line_repr(val, max_items=6, max_chars=120)
    except Exception:
        try:
            return str(val)
        except Exception:
            return "«err»"


def _polars_format_transpose_values(series: pl.Series) -> list[str | None]:
    """Efficiently format a series of values for transpose view using Polars operations."""
    try:
        # Use the dtype-aware formatter for better performance
        formatted_values = _polars_format_with_dtype(series, max_items=6, max_chars=120)
        # Convert any empty strings back to None for consistency with original behavior
        return [val if val != "" else None for val in formatted_values]
    except Exception:
        # Fallback to element-wise processing
        values = series.to_list()
        return [_format_transpose_value(val) for val in values]

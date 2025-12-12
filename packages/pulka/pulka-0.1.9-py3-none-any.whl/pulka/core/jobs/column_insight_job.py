"""Background job helpers for column insight calculations."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Any

import polars as pl

from ..column_insight import (
    LOW_CARDINALITY_NUMERIC_LIMIT,
    ColumnInsight,
    InsightHistogram,
    TopValue,
    summarize_value_preview,
)
from ..formatting import _is_string_dtype, _supports_min_max, _supports_numeric_stats

_MAX_TOP_VALUES = 10
_HISTOGRAM_BIN_COUNT = 48


@dataclass(frozen=True, slots=True)
class ColumnInsightJobConfig:
    """Parameters captured when scheduling a column insight job."""

    column_name: str
    plan_hash: str | None
    sheet_id: str | None
    source_path: str | None = None
    top_values: int = _MAX_TOP_VALUES


def compute_column_insight(
    *,
    lazyframe: pl.LazyFrame,
    config: ColumnInsightJobConfig,
    schema: Mapping[str, pl.DataType] | None = None,
) -> ColumnInsight:
    """Compute metrics for ``config.column_name`` using ``lazyframe``."""

    start_ns = perf_counter_ns()
    column_name = config.column_name
    dtype = _resolve_dtype(column_name, schema, lazyframe)

    if dtype is None and column_name not in lazyframe.columns:
        duration = perf_counter_ns() - start_ns
        return ColumnInsight(
            config.sheet_id,
            config.plan_hash,
            column_name,
            None,
            None,
            None,
            None,
            None,
            None,
            {},
            (),
            None,
            source_path=config.source_path,
            duration_ns=duration,
            error=f"unknown column: {column_name}",
        )

    try:
        stats_frame = lazyframe.select(_build_aggregations(column_name, dtype)).collect()
    except Exception as exc:  # pragma: no cover - upstream polars failures
        duration = perf_counter_ns() - start_ns
        return ColumnInsight(
            config.sheet_id,
            config.plan_hash,
            column_name,
            _dtype_str(dtype),
            None,
            None,
            None,
            None,
            None,
            {},
            (),
            None,
            source_path=config.source_path,
            duration_ns=duration,
            error=str(exc),
        )

    stats_row = stats_frame.to_dicts()[0] if stats_frame.height else {}
    row_count = _to_int(stats_row.get("row_count"))
    non_null_count = _to_int(stats_row.get("non_null_count"))
    null_count = _to_int(stats_row.get("null_count"))
    distinct_count = _to_int(stats_row.get("distinct_count"))
    null_fraction = _fraction(null_count, row_count)
    low_cardinality_numeric = _is_low_cardinality_numeric(dtype, distinct_count)

    stats_payload = _filter_stats(stats_row)
    top_value_limit = (
        max(0, config.top_values)
        if _supports_top_value_summary(dtype) or low_cardinality_numeric
        else 0
    )
    top_values = _collect_top_values(
        lazyframe,
        column_name,
        limit=top_value_limit,
        non_null_count=non_null_count,
    )
    histogram = None
    if not low_cardinality_numeric:
        histogram = _collect_histogram(
            lazyframe,
            column_name,
            dtype=dtype,
            stats_row=stats_row,
            non_null_count=non_null_count,
        )

    duration = perf_counter_ns() - start_ns
    return ColumnInsight(
        config.sheet_id,
        config.plan_hash,
        column_name,
        _dtype_str(dtype),
        row_count,
        non_null_count,
        null_count,
        null_fraction,
        distinct_count,
        stats_payload,
        top_values,
        histogram,
        source_path=config.source_path,
        duration_ns=duration,
    )


def _build_aggregations(column: str, dtype: pl.DataType | None) -> Sequence[pl.Expr]:
    col_expr = pl.col(column)
    aggs: list[pl.Expr] = [
        pl.len().alias("row_count"),
        col_expr.is_not_null().sum().alias("non_null_count"),
        col_expr.is_null().sum().alias("null_count"),
        col_expr.n_unique().alias("distinct_count"),
    ]

    if dtype is not None and _supports_min_max(dtype):
        aggs.extend(
            [
                col_expr.min().alias("min"),
                col_expr.max().alias("max"),
            ]
        )

    if dtype is not None and _supports_numeric_stats(dtype):
        aggs.extend(
            [
                col_expr.mean().alias("mean"),
                col_expr.median().alias("median"),
                col_expr.quantile(0.95, interpolation="nearest").alias("p95"),
                col_expr.quantile(0.05, interpolation="nearest").alias("p05"),
                col_expr.std().alias("std"),
            ]
        )

    return aggs


def _collect_top_values(
    lazyframe: pl.LazyFrame,
    column: str,
    *,
    limit: int,
    non_null_count: int | None,
) -> tuple[TopValue, ...]:
    if limit <= 0 or not non_null_count:
        return ()

    try:
        top_frame = (
            lazyframe.select(pl.col(column))
            .drop_nulls()
            .group_by(column)
            .agg(pl.len().alias("count"))
            .sort("count", descending=True)
            .limit(limit)
            .collect()
        )
    except Exception:
        return ()

    values: list[TopValue] = []
    for row in top_frame.to_dicts():
        count = _to_int(row.get("count")) or 0
        raw_value = row.get(column)
        display, truncated = summarize_value_preview(raw_value, max_chars=48)
        fraction = _fraction(count, non_null_count)
        values.append(TopValue(raw_value, display, count, fraction, truncated))
    return tuple(values)


def _collect_histogram(
    lazyframe: pl.LazyFrame,
    column: str,
    *,
    dtype: pl.DataType | None,
    stats_row: Mapping[str, Any],
    non_null_count: int | None,
) -> InsightHistogram | None:
    if dtype is None or not _supports_numeric_stats(dtype):
        return None
    if non_null_count in (None, 0):
        return None
    minimum = stats_row.get("min")
    maximum = stats_row.get("max")
    if minimum is None or maximum is None:
        return None
    try:
        min_value = float(minimum)
        max_value = float(maximum)
    except Exception:
        return None
    if not (math.isfinite(min_value) and math.isfinite(max_value)):
        return None
    if max_value < min_value:
        min_value, max_value = max_value, min_value
    if math.isclose(max_value, min_value):
        bins = tuple(1.0 if idx == 0 else 0.0 for idx in range(_HISTOGRAM_BIN_COUNT))
        return InsightHistogram(bins)
    bin_count = _HISTOGRAM_BIN_COUNT
    width = (max_value - min_value) / bin_count
    if width <= 0 or not math.isfinite(width):
        return None
    col_expr = pl.col(column)
    try:
        bin_expr = ((col_expr - min_value) / width).floor()
        binned = (
            lazyframe.select(
                pl.when(col_expr.is_null())
                .then(None)
                .otherwise(
                    pl.when(bin_expr < 0)
                    .then(0)
                    .when(bin_expr >= bin_count)
                    .then(bin_count - 1)
                    .otherwise(bin_expr)
                    .cast(pl.Int64)
                )
                .alias("__bin")
            )
            .drop_nulls("__bin")
            .group_by("__bin")
            .agg(pl.len().alias("count"))
            .collect()
        )
    except Exception:
        return None
    counts = [0] * bin_count
    for row in binned.iter_rows():
        idx, count = row
        try:
            pos = int(idx)
        except Exception:
            continue
        if 0 <= pos < bin_count:
            try:
                counts[pos] = int(count)
            except Exception:
                continue
    max_count = max(counts) if counts else 0
    if max_count <= 0:
        return None
    normalized = tuple(count / max_count for count in counts)
    return InsightHistogram(normalized)


def _supports_top_value_summary(dtype: pl.DataType | None) -> bool:
    if dtype is None:
        return False
    if _is_string_dtype(dtype):
        return True
    is_categorical = getattr(pl.datatypes, "is_categorical", None)
    if is_categorical is not None:
        try:
            if is_categorical(dtype):
                return True
        except Exception:
            pass
    dtype_name = type(dtype).__name__.lower()
    return "categorical" in dtype_name or "enum" in dtype_name


def _is_low_cardinality_numeric(dtype: pl.DataType | None, distinct_count: int | None) -> bool:
    if dtype is None or distinct_count is None:
        return False
    if distinct_count < 0:
        return False
    if distinct_count > LOW_CARDINALITY_NUMERIC_LIMIT:
        return False
    try:
        return _supports_numeric_stats(dtype)
    except Exception:
        return False


def _filter_stats(row: Mapping[str, Any]) -> dict[str, Any]:
    skip = {"row_count", "non_null_count", "null_count", "distinct_count"}
    return {key: row.get(key) for key in row if key not in skip}


def _fraction(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    try:
        assert numerator is not None
        assert denominator is not None
        return float(numerator) / float(denominator)
    except Exception:
        return None


def _to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _resolve_dtype(
    column: str,
    schema: Mapping[str, pl.DataType] | None,
    lazyframe: pl.LazyFrame,
) -> pl.DataType | None:
    if schema and column in schema:
        return schema[column]
    try:
        collected = lazyframe.schema
        if column in collected:
            return collected[column]
    except Exception:  # pragma: no cover - schema fetch may fail on older polars
        pass
    try:
        inferred = lazyframe.collect_schema()
        return inferred.get(column)
    except Exception:
        return None


def _dtype_str(dtype: pl.DataType | None) -> str | None:
    if dtype is None:
        return None
    try:
        text = str(dtype)
    except Exception:
        return dtype.__class__.__name__
    simple = dtype.__class__.__name__
    if text.startswith(f"{simple}("):
        return simple
    return text


__all__ = [
    "ColumnInsightJobConfig",
    "compute_column_insight",
]

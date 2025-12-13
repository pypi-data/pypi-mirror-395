"""Background job helpers for column insight calculations."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import timedelta
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
from ..formatting import (
    _is_string_dtype,
    _is_temporal_dtype,
    _is_time_dtype,
    _supports_histogram_stats,
    _supports_min_max,
    _supports_numeric_or_temporal_stats,
)

_MAX_TOP_VALUES = 10
_HISTOGRAM_BIN_COUNT = 48
_DAY_NS = 86_400_000_000_000


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
    if dtype is not None and _is_temporal_dtype(dtype):
        stats_payload = _normalize_temporal_stats(stats_payload, dtype, non_null_count)
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
    stats_expr = (
        col_expr.cast(pl.Int64) if dtype is not None and _is_temporal_dtype(dtype) else col_expr
    )
    is_time = dtype is not None and _is_time_dtype(dtype)
    aggs: list[pl.Expr] = [
        pl.len().alias("row_count"),
        col_expr.is_not_null().sum().alias("non_null_count"),
        col_expr.is_null().sum().alias("null_count"),
        col_expr.n_unique().alias("distinct_count"),
    ]

    if dtype is not None and _supports_min_max(dtype):
        min_max_expr = stats_expr if dtype is not None and _is_temporal_dtype(dtype) else col_expr
        aggs.extend(
            [
                min_max_expr.min().alias("min"),
                min_max_expr.max().alias("max"),
            ]
        )

    if _supports_numeric_or_temporal_stats(dtype):
        aggs.extend(
            [
                stats_expr.mean().alias("mean"),
                stats_expr.median().alias("median"),
                stats_expr.quantile(0.95, interpolation="nearest").alias("p95"),
                stats_expr.quantile(0.05, interpolation="nearest").alias("p05"),
            ]
        )
        if not is_time:
            aggs.append(stats_expr.std().alias("std"))
        else:
            angle_expr = (stats_expr.cast(pl.Float64) / float(_DAY_NS)) * math.tau
            aggs.extend(
                [
                    angle_expr.cos().sum().alias("time_sum_cos"),
                    angle_expr.sin().sum().alias("time_sum_sin"),
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
    if dtype is None or not _supports_histogram_stats(dtype):
        return None
    is_temporal = _is_temporal_dtype(dtype)
    if non_null_count in (None, 0):
        return None
    minimum = stats_row.get("min")
    maximum = stats_row.get("max")
    bounds = _coerce_histogram_bounds(minimum, maximum, dtype)
    if bounds is None:
        return None
    min_value, max_value = bounds
    if not (math.isfinite(min_value) and math.isfinite(max_value)):
        return None
    if max_value < min_value:
        min_value, max_value = max_value, min_value
    if (max_value == min_value) if is_temporal else math.isclose(max_value, min_value):
        bins = tuple(1.0 if idx == 0 else 0.0 for idx in range(_HISTOGRAM_BIN_COUNT))
        return InsightHistogram(bins)
    bin_count = _HISTOGRAM_BIN_COUNT
    bin_width: float
    if is_temporal:
        min_int = int(min_value)
        max_int = int(max_value)
        value_range = max_int - min_int
        effective_bins = max(1, min(bin_count, value_range + 1))
        bin_width = float(max(1, math.ceil(value_range / effective_bins)))
        bin_count = effective_bins
        col_expr = pl.col(column).cast(pl.Int64)
        bin_expr = (col_expr - min_int) // bin_width
    else:
        bin_width = (max_value - min_value) / bin_count
        if bin_width <= 0 or not math.isfinite(bin_width):
            return None
        col_expr = pl.col(column)
        bin_expr = ((col_expr - min_value) / bin_width).floor()
    try:
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


def _coerce_histogram_bounds(
    minimum: Any, maximum: Any, dtype: pl.DataType
) -> tuple[float | int, float | int] | None:
    if minimum is None or maximum is None:
        return None
    if _is_temporal_dtype(dtype):
        try:
            series = pl.Series([minimum, maximum], dtype=dtype).cast(pl.Int64, strict=False)
            min_value = _to_int(series.min())
            max_value = _to_int(series.max())
        except Exception:
            return None
        if min_value is None or max_value is None:
            return None
        return min_value, max_value
    try:
        return float(minimum), float(maximum)
    except Exception:
        return None


def _normalize_temporal_stats(
    stats: dict[str, Any], dtype: pl.DataType, non_null_count: int | None
) -> dict[str, Any]:
    if not stats:
        return stats
    sum_cos = stats.get("time_sum_cos")
    sum_sin = stats.get("time_sum_sin")

    def _convert(value: Any, target_dtype: pl.DataType) -> Any:
        if value is None:
            return None
        try:
            series = pl.Series([value]).cast(target_dtype, strict=False)
            return series[0]
        except Exception:
            return value

    normalized = dict(stats)
    if _is_time_dtype(dtype):
        mean_value = _compute_circular_mean_time(sum_cos, sum_sin, non_null_count, dtype)
        if mean_value is not None:
            normalized["mean"] = mean_value
    for key in ("min", "max", "mean", "median", "p05", "p95"):
        if key in normalized:
            normalized[key] = _convert(normalized.get(key), dtype)
    if _is_time_dtype(dtype):
        std_value = _compute_circular_std(sum_cos, sum_sin, non_null_count)
        if std_value is not None:
            normalized["std"] = std_value
    elif "std" in normalized:
        normalized["std"] = _convert_temporal_std(normalized.get("std"), dtype)
    normalized.pop("time_sum_cos", None)
    normalized.pop("time_sum_sin", None)
    return normalized


def _convert_temporal_std(value: Any, dtype: pl.DataType) -> Any:
    if value is None:
        return None
    try:
        numeric = float(value)
    except Exception:
        return value

    unit = _temporal_base_unit(dtype)
    if unit == "days":
        return timedelta(days=numeric)
    if unit == "ms":
        return timedelta(milliseconds=numeric)
    if unit == "us":
        return timedelta(microseconds=numeric)
    # Default to nanoseconds for datetime/time/duration in ns.
    return timedelta(microseconds=numeric / 1000.0)


def _temporal_base_unit(dtype: pl.DataType) -> str:
    if type(dtype).__name__ == "Date":
        return "days"
    time_unit = getattr(dtype, "time_unit", None)
    if isinstance(time_unit, str):
        return time_unit
    return "ns"


def _compute_circular_std(sum_cos: Any, sum_sin: Any, count: int | None) -> timedelta | None:
    if sum_cos is None or sum_sin is None or not count:
        return None
    try:
        n = float(count)
        c = float(sum_cos)
        s = float(sum_sin)
    except Exception:
        return None
    if n <= 0:
        return None
    c_mean = c / n
    s_mean = s / n
    r = math.hypot(c_mean, s_mean)
    if r <= 0.0 or r > 1.0:
        return None
    try:
        std_radians = math.sqrt(max(0.0, -2.0 * math.log(r)))
    except Exception:
        return None
    # Convert the circular spread back into seconds on a 24h clock.
    seconds = (std_radians / math.tau) * (_DAY_NS / 1_000_000_000)
    return timedelta(seconds=seconds)


def _compute_circular_mean_time(
    sum_cos: Any, sum_sin: Any, count: int | None, dtype: pl.DataType
) -> Any:
    if sum_cos is None or sum_sin is None or not count:
        return None
    try:
        n = float(count)
        c = float(sum_cos)
        s = float(sum_sin)
    except Exception:
        return None
    if n <= 0:
        return None
    c_mean = c / n
    s_mean = s / n
    angle = math.atan2(s_mean, c_mean)
    if math.isnan(angle):
        return None
    if angle < 0:
        angle += math.tau
    try:
        ns_value = (angle / math.tau) * _DAY_NS
        series = pl.Series([ns_value]).cast(dtype, strict=False)
        return series[0]
    except Exception:
        return None


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
        return _supports_numeric_or_temporal_stats(dtype)
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

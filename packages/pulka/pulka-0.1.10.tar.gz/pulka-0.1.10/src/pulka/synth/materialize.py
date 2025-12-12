"""Materialise synthetic dataset specs into Polars DataFrames."""

from __future__ import annotations

import ast
import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

import polars as pl

from .determinism import DeterministicRNG, derive_seed, normalized_spec_hash
from .normalize import normalize_spec
from .types import (
    GeneratedColumnSpec,
    GeneratorKind,
    GeneratorSpec,
    Modifier,
    ModifierKind,
    SeasonComponent,
    Spec,
    StructFieldSpec,
)


class MaterializationError(RuntimeError):
    """Raised when a specification cannot be materialised."""


@dataclass
class _ColumnContext:
    name: str
    index: int
    rows: int
    global_seed: bytes


def materialize_spec(spec: Spec, normalized: str | None = None) -> pl.DataFrame:
    """Materialise ``spec`` into a deterministic :class:`polars.DataFrame`."""

    if normalized is None:
        normalized = normalize_spec(spec)
    global_seed = normalized_spec_hash(normalized)

    df = pl.DataFrame({})
    built_columns: list[str] = []

    for index, column in enumerate(spec.columns):
        ctx = _ColumnContext(name=column.name, index=index, rows=spec.rows, global_seed=global_seed)
        definition = column.definition
        if isinstance(definition, GeneratedColumnSpec):
            series = _generate_series(definition.generator, ctx, column.name)
            series = _apply_modifiers(series, definition, ctx)
            series = _cast_series_dtype(series, column.dtype)
            if df.height == 0:
                df = series.to_frame()
            else:
                if series.len() != df.height:
                    raise MaterializationError(
                        f"column '{column.name}' produced {series.len()} rows "
                        f"but expected {df.height}"
                    )
                df = df.with_columns(series)
            built_columns.append(column.name)
        else:
            expr = _compile_expression(definition.expression, built_columns, column.name)
            if df.height == 0:
                raise MaterializationError(
                    f"expression column '{column.name}' requires preceding columns but none exist"
                )
            if column.dtype is not None:
                expr = expr.cast(column.dtype)
            df = df.with_columns(expr.alias(column.name))
            built_columns.append(column.name)
    return df


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------


def _generate_series(generator: GeneratorSpec, ctx: _ColumnContext, column_name: str) -> pl.Series:
    kind = generator.kind
    if kind is GeneratorKind.SEQUENCE:
        return _generate_sequence_series(generator, ctx, column_name)
    if kind is GeneratorKind.TIME_SERIES:
        return _generate_time_series(generator.params, ctx, column_name)
    values = _generate_values(generator, ctx)
    series = _to_series(column_name, values)
    if kind is GeneratorKind.DATETIME:
        series = _cast_datetime_series(series, generator.params)
    return series


def _generate_values(generator: GeneratorSpec, ctx: _ColumnContext) -> list[Any]:
    seed = derive_seed(ctx.global_seed, ctx.index, ctx.name, "generator")
    rng = DeterministicRNG(seed)
    n = ctx.rows
    kind = generator.kind
    params = generator.params

    if kind is GeneratorKind.NORMAL:
        mean = float(params["mean"])
        stddev = float(params["stddev"])
        return [rng.normal(mean, stddev) for _ in range(n)]
    if kind is GeneratorKind.LOGNORMAL:
        mean = float(params["mean"])
        stddev = float(params["stddev"])
        return [math.exp(rng.normal(mean, stddev)) for _ in range(n)]
    if kind is GeneratorKind.UNIFORM:
        low = float(params["low"])
        high = float(params["high"])
        return [rng.uniform(low, high) for _ in range(n)]
    if kind is GeneratorKind.EXP:
        lam = float(params["lambda"])
        return [rng.exponential(lam) for _ in range(n)]
    if kind is GeneratorKind.BETA:
        alpha = float(params["alpha"])
        beta = float(params["beta"])
        return [rng.beta(alpha, beta) for _ in range(n)]
    if kind is GeneratorKind.LAPLACE:
        mean = float(params["mean"])
        scale = float(params["scale"])
        return [_laplace_sample(rng, mean, scale) for _ in range(n)]
    if kind is GeneratorKind.WEIBULL:
        shape = float(params["shape"])
        scale = float(params["scale"])
        return [_weibull_sample(rng, shape, scale) for _ in range(n)]
    if kind is GeneratorKind.POISSON:
        lam = float(params["lambda"])
        if lam <= 0:
            raise MaterializationError("poisson() requires positive lambda")
        return [rng.poisson(lam) for _ in range(n)]
    if kind is GeneratorKind.GAMMA:
        shape = float(params["shape"])
        scale = float(params["scale"])
        if shape <= 0 or scale <= 0:
            raise MaterializationError("gamma() requires positive shape and scale")
        return [rng.gamma(shape, scale) for _ in range(n)]
    if kind is GeneratorKind.ZIPF:
        alpha = float(params["alpha"])
        if alpha <= 1:
            raise MaterializationError("zipf() requires alpha > 1")
        return [rng.zipf(alpha) for _ in range(n)]
    if kind is GeneratorKind.PARETO:
        alpha = float(params["alpha"])
        if alpha <= 0:
            raise MaterializationError("pareto() requires alpha > 0")
        return [rng.pareto(alpha) for _ in range(n)]
    if kind is GeneratorKind.CATEGORICAL:
        count = int(params["count"])
        if count <= 0:
            raise MaterializationError("categorical() requires a positive count")
        labels = [f"v{i}" for i in range(count)]
        return [labels[int(rng.random() * count)] for _ in range(n)]
    if kind is GeneratorKind.ENUM:
        labels = list(params["labels"])
        if not labels:
            raise MaterializationError("enum[] requires at least one label")
        size = len(labels)
        return [labels[int(rng.random() * size)] for _ in range(n)]
    if kind is GeneratorKind.DATE:
        start = date.fromisoformat(params["start"])
        end = date.fromisoformat(params["end"])
        if end < start:
            raise MaterializationError("date[...] end must be >= start")
        start_ord = start.toordinal()
        span = end.toordinal() - start_ord
        return [date.fromordinal(start_ord + int(rng.random() * (span + 1))) for _ in range(n)]
    if kind is GeneratorKind.BOOLEAN:
        return [rng.random() < 0.5 for _ in range(n)]
    if kind is GeneratorKind.BINARY:
        length = int(params["length"])
        return [rng.randbytes(length) for _ in range(n)]
    if kind is GeneratorKind.DATETIME:
        return _generate_datetime_values(params, rng, n)
    if kind is GeneratorKind.TIME:
        return _generate_time_values(params, rng, n)
    if kind is GeneratorKind.DURATION:
        low = float(params["low"])
        high = float(params["high"])
        if high < low:
            raise MaterializationError("duration upper bound must be >= lower bound")
        return [timedelta(seconds=rng.uniform(low, high)) for _ in range(n)]
    if kind is GeneratorKind.LIST_INT:
        return _generate_list_int_values(params, rng, n)
    if kind is GeneratorKind.LIST:
        return _generate_list_values(params, rng, ctx)
    if kind is GeneratorKind.ARRAY:
        return _generate_array_values(params, rng, ctx)
    if kind is GeneratorKind.STRUCT:
        return _generate_struct_values(params, rng, ctx)
    if kind is GeneratorKind.NULL:
        return [None for _ in range(n)]
    raise MaterializationError(f"unsupported generator kind: {kind}")


def _generate_sequence_series(
    generator: GeneratorSpec, ctx: _ColumnContext, column_name: str
) -> pl.Series:
    start = generator.params["start"]
    step = generator.params["step"]
    rows = ctx.rows

    if _is_integral(start) and _is_integral(step):
        start_int = int(start)
        step_int = int(step)
        if rows == 0:
            return pl.Series(column_name, [], dtype=pl.Int64)
        if step_int == 0:
            return pl.repeat(start_int, rows, eager=True).cast(pl.Int64).rename(column_name)
        stop = start_int + step_int * rows
        return pl.arange(start_int, stop, step_int, eager=True).rename(column_name)

    start_float = float(start)
    step_float = float(step)
    if rows == 0:
        return pl.Series(column_name, [], dtype=pl.Float64)
    if step_float == 0.0:
        return pl.repeat(start_float, rows, eager=True).cast(pl.Float64).rename(column_name)
    stop = start_float + step_float * rows
    return pl.arange(start_float, stop, step_float, eager=True).cast(pl.Float64).rename(column_name)


def _generate_time_series(
    params: dict[str, Any], ctx: _ColumnContext, column_name: str
) -> pl.Series:
    trend = float(params.get("trend", 0))
    start_token = params.get("start", "")
    base = 0.0
    if start_token:
        try:
            if len(start_token) <= 10:
                base = float(date.fromisoformat(start_token).toordinal())
            else:
                base = float(datetime.fromisoformat(start_token).timestamp())
        except ValueError:
            base = 0.0
    seasons: Sequence[SeasonComponent] = params.get("seasons", ())
    noise_spec: GeneratorSpec | None = params.get("noise")

    idx_series = pl.arange(0, ctx.rows, eager=True).rename("__ts_idx")
    if idx_series.is_empty():
        result = pl.Series(column_name, [], dtype=pl.Float64)
    else:
        frame = pl.DataFrame({idx_series.name: idx_series})
        expr = pl.lit(base) + pl.col(idx_series.name) * trend
        for component in seasons:
            period = float(component.period)
            amplitude = float(component.amplitude)
            if period == 0:
                continue
            expr = expr + amplitude * ((2.0 * math.pi * pl.col(idx_series.name)) / period).sin()
        result = frame.select(expr.alias(column_name)).to_series().cast(pl.Float64)

    if noise_spec is not None and ctx.rows:
        if noise_spec.kind is not GeneratorKind.NORMAL:
            raise MaterializationError("ts noise must be normal(mean,stddev)")
        noise_seed = derive_seed(ctx.global_seed, ctx.index, ctx.name, "generator", "noise")
        noise_rng = DeterministicRNG(noise_seed)
        mean = float(noise_spec.params["mean"])
        stddev = float(noise_spec.params["stddev"])
        noise_series = pl.Series(
            f"__noise_{ctx.index}",
            [noise_rng.normal(mean, stddev) for _ in range(ctx.rows)],
            dtype=pl.Float64,
        )
        base = result if result.dtype == pl.Float64 else result.cast(pl.Float64)
        result = (base + noise_series).rename(column_name)

    return result


def _generate_datetime_values(
    params: dict[str, Any], rng: DeterministicRNG, count: int
) -> list[datetime]:
    if count == 0:
        return []
    start = datetime.fromisoformat(params["start"])
    end = datetime.fromisoformat(params["end"])
    tz_name = params.get("time_zone")
    if tz_name:
        tz = ZoneInfo(tz_name)
        if start.tzinfo is None:
            start = start.replace(tzinfo=tz)
        if end.tzinfo is None:
            end = end.replace(tzinfo=tz)
    if end < start:
        raise MaterializationError("datetime end must be >= start")
    if count == 1:
        return [start]
    span = end - start
    step = span / (count - 1)
    return [start + step * idx for idx in range(count)]


def _generate_time_values(params: dict[str, Any], rng: DeterministicRNG, count: int) -> list[time]:
    if count == 0:
        return []
    start_token = params.get("start")
    end_token = params.get("end")
    if start_token is None or end_token is None:
        return [_random_time(rng) for _ in range(count)]
    start = time.fromisoformat(start_token)
    end = time.fromisoformat(end_token)
    start_us = _time_to_microseconds(start)
    end_us = _time_to_microseconds(end)
    if end_us < start_us:
        raise MaterializationError("time end must be >= start")
    if count == 1:
        values = [start_us]
    else:
        span = end_us - start_us
        values = [start_us + (span * idx) // (count - 1) for idx in range(count)]
    return [_microseconds_to_time(us) for us in values]


def _generate_list_int_values(
    params: dict[str, Any], rng: DeterministicRNG, count: int
) -> list[list[int]]:
    min_length = int(params["min_length"])
    max_length = int(params["max_length"])
    low = int(params["low"])
    high = int(params["high"])
    if max_length < min_length:
        raise MaterializationError("list_int max length must be >= min length")
    if high < low:
        raise MaterializationError("list_int high must be >= low")
    result: list[list[int]] = []
    for _ in range(count):
        length = min_length if max_length <= min_length else rng.randint(min_length, max_length)
        if length <= 0:
            result.append([])
            continue
        span = high - low
        if span <= 0:
            values = [low for _ in range(length)]
        else:
            values = [rng.randint(low, high) for _ in range(length)]
        result.append(values)
    return result


def _generate_list_values(
    params: dict[str, Any], rng: DeterministicRNG, ctx: _ColumnContext
) -> list[list[Any]]:
    element: GeneratedColumnSpec = params["element"]
    min_length = int(params["min_length"])
    max_length = int(params["max_length"])
    if min_length < 0 or max_length < 0:
        raise MaterializationError("list lengths must be non-negative")
    if max_length < min_length:
        raise MaterializationError("list max length must be >= min length")
    values: list[list[Any]] = []
    for row_index in range(ctx.rows):
        length = min_length if min_length == max_length else rng.randint(min_length, max_length)
        if length <= 0:
            values.append([])
            continue
        nested_ctx = _nested_context(ctx, "list", row_index, length)
        series = _materialize_generated_series(
            element,
            nested_ctx,
            f"{ctx.name}__list_{row_index}",
        )
        if series.len() != length:
            raise MaterializationError("list element generator produced unexpected length")
        values.append(series.to_list())
    return values


def _generate_array_values(
    params: dict[str, Any], rng: DeterministicRNG, ctx: _ColumnContext
) -> list[list[Any]]:
    element: GeneratedColumnSpec = params["element"]
    size = int(params["size"])
    if size < 0:
        raise MaterializationError("array size must be non-negative")
    values: list[list[Any]] = []
    for row_index in range(ctx.rows):
        if size == 0:
            values.append([])
            continue
        nested_ctx = _nested_context(ctx, "array", row_index, size)
        series = _materialize_generated_series(
            element,
            nested_ctx,
            f"{ctx.name}__array_{row_index}",
        )
        if series.len() != size:
            raise MaterializationError("array element generator produced unexpected length")
        values.append(series.to_list())
    return values


def _generate_struct_values(
    params: dict[str, Any], rng: DeterministicRNG, ctx: _ColumnContext
) -> list[dict[str, Any]]:
    fields: Sequence[StructFieldSpec] = params["fields"]
    records: list[dict[str, Any]] = []
    for row_index in range(ctx.rows):
        record: dict[str, Any] = {}
        for field in fields:
            nested_ctx = _nested_context(ctx, "struct", row_index, 1, qualifier=field.name)
            series = _materialize_generated_series(
                field.definition,
                nested_ctx,
                f"{ctx.name}__{field.name}_{row_index}",
            )
            if series.is_empty():
                record[field.name] = None
            else:
                record[field.name] = series.to_list()[0]
        records.append(record)
    return records


def _materialize_generated_series(
    definition: GeneratedColumnSpec, ctx: _ColumnContext, column_name: str
) -> pl.Series:
    series = _generate_series(definition.generator, ctx, column_name)
    return _apply_modifiers(series, definition, ctx)


def _nested_context(
    parent: _ColumnContext,
    role: str,
    row_index: int,
    rows: int,
    *,
    qualifier: str | None = None,
) -> _ColumnContext:
    seed_parts: list[str | int] = [parent.index, parent.name, role, row_index]
    if qualifier is not None:
        seed_parts.append(qualifier)
    nested_seed = derive_seed(parent.global_seed, *seed_parts)
    name = f"{parent.name}|{role}|{row_index}"
    if qualifier is not None:
        name += f"|{qualifier}"
    return _ColumnContext(name=name, index=parent.index, rows=rows, global_seed=nested_seed)


def _random_time(rng: DeterministicRNG) -> time:
    hour = rng.randint(0, 23)
    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    microsecond = int(rng.random() * 1_000_000)
    return time(hour, minute, second, microsecond)


def _time_to_microseconds(value: time) -> int:
    total_seconds = ((value.hour * 60) + value.minute) * 60 + value.second
    return total_seconds * 1_000_000 + value.microsecond


def _microseconds_to_time(value: int) -> time:
    seconds, micro = divmod(value, 1_000_000)
    hour, rem = divmod(seconds, 3600)
    minute, second = divmod(rem, 60)
    hour = int(hour) % 24
    return time(hour=hour, minute=int(minute), second=int(second), microsecond=int(micro))


# ---------------------------------------------------------------------------
# Modifiers
# ---------------------------------------------------------------------------


def _apply_modifiers(
    series: pl.Series, definition: GeneratedColumnSpec, ctx: _ColumnContext
) -> pl.Series:
    null_percent: float | None = None
    unique_requested = False
    result = series
    for modifier in definition.modifiers:
        if modifier.kind is ModifierKind.NULL_PERCENT:
            null_percent = float(modifier.params["value"])
            continue
        if modifier.kind is ModifierKind.UNIQUE:
            unique_requested = True
            continue
        result = _apply_modifier(result, modifier, definition.generator, ctx)

    if null_percent is not None:
        result = _apply_nulls(result, null_percent, ctx)
    if unique_requested:
        if definition.generator.kind in {
            GeneratorKind.LIST,
            GeneratorKind.ARRAY,
            GeneratorKind.STRUCT,
        }:
            raise MaterializationError("unique modifier is not supported for nested generators")
        result = _enforce_unique_series(result, definition.generator, ctx)
    return result


def _apply_modifier(
    series: pl.Series, modifier: Modifier, generator: GeneratorSpec, ctx: _ColumnContext
) -> pl.Series:
    kind = modifier.kind
    params = modifier.params
    if kind is ModifierKind.CLIP:
        low = float(params["low"])
        high = float(params["high"])
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64).clip(low, high))
    if kind is ModifierKind.NOISE_NORMAL:
        mean = float(params["mean"])
        stddev = float(params["stddev"])
        seed = derive_seed(ctx.global_seed, ctx.index, ctx.name, "modifier", "noise")
        rng = DeterministicRNG(seed)
        noise = [rng.normal(mean, stddev) for _ in range(series.len())]
        noise_series = pl.Series(f"__noise_{ctx.index}", noise, dtype=pl.Float64)
        base = series if series.dtype == pl.Float64 else series.cast(pl.Float64)
        return (base + noise_series).rename(series.name)
    if kind is ModifierKind.LOG:
        frame = series.to_frame()
        invalid = frame.select(
            ((pl.col(series.name) <= 0) & pl.col(series.name).is_not_null()).any()
        ).item()
        if invalid:
            raise MaterializationError(
                f"log modifier received invalid value in column '{ctx.name}'"
            )
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64).log())
    if kind is ModifierKind.EXP:
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64).exp())
    if kind is ModifierKind.ABS:
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64).abs())
    if kind is ModifierKind.SCALE:
        factor = float(params["value"])
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64) * factor)
    if kind is ModifierKind.OFFSET:
        offset = float(params["value"])
        return _evaluate_unary(series, pl.col(series.name).cast(pl.Float64) + offset)
    raise MaterializationError(f"unsupported modifier {kind}")


def _apply_nulls(series: pl.Series, percent: float, ctx: _ColumnContext) -> pl.Series:
    if percent <= 0:
        return series
    if percent >= 100:
        return pl.Series(series.name, [None] * series.len(), dtype=series.dtype)
    threshold = percent / 100.0
    seed = derive_seed(ctx.global_seed, ctx.index, ctx.name, "nulls")
    rng = DeterministicRNG(seed)
    mask = [rng.random() < threshold for _ in range(series.len())]
    mask_series = pl.Series(f"__nulls_{ctx.index}", mask, dtype=pl.Boolean)
    null_lit = pl.lit(None)
    if series.dtype != pl.Null:
        null_lit = null_lit.cast(series.dtype)
    return (
        pl.DataFrame({series.name: series, mask_series.name: mask_series})
        .select(
            pl.when(pl.col(mask_series.name))
            .then(null_lit)
            .otherwise(pl.col(series.name))
            .alias(series.name)
        )
        .to_series()
    )


def _enforce_unique(values: list[Any], generator: GeneratorSpec, ctx: _ColumnContext) -> list[Any]:
    if generator.kind is GeneratorKind.SEQUENCE:
        return values
    if generator.kind is GeneratorKind.CATEGORICAL:
        domain = generator.params["count"]
        if ctx.rows > domain:
            raise MaterializationError(
                f"column '{ctx.name}' cannot be unique with "
                f"categorical({domain}) and {ctx.rows} rows"
            )
    if generator.kind is GeneratorKind.ENUM:
        domain = len(generator.params["labels"])
        if ctx.rows > domain:
            raise MaterializationError(
                f"column '{ctx.name}' cannot be unique with {domain} "
                f"enum labels and {ctx.rows} rows"
            )

    seen: set[Any] = set()
    duplicates: list[int] = []
    for idx, value in enumerate(values):
        if value is None:
            continue
        if value in seen:
            duplicates.append(idx)
        else:
            seen.add(value)
    if not duplicates:
        return values

    result = list(values)
    max_attempts = 5
    attempt = 0
    while duplicates and attempt < max_attempts:
        attempt += 1
        next_duplicates: list[int] = []
        for pos in duplicates:
            subseed = derive_seed(ctx.global_seed, ctx.index, ctx.name, "unique", attempt, pos)
            rng = DeterministicRNG(subseed)
            sample = _generate_single(generator, rng)
            if sample is None:
                continue
            if sample in seen:
                next_duplicates.append(pos)
            else:
                seen.add(sample)
                result[pos] = sample
        duplicates = next_duplicates

    if duplicates:
        raise MaterializationError(
            f"failed to enforce uniqueness for column '{ctx.name}' after {max_attempts} attempts"
        )
    return result


def _enforce_unique_series(
    series: pl.Series, generator: GeneratorSpec, ctx: _ColumnContext
) -> pl.Series:
    values = series.to_list()
    unique_values = _enforce_unique(values, generator, ctx)
    return _to_series(series.name, unique_values)


def _generate_single(generator: GeneratorSpec, rng: DeterministicRNG) -> Any:
    if generator.kind is GeneratorKind.NORMAL:
        return rng.normal(float(generator.params["mean"]), float(generator.params["stddev"]))
    if generator.kind is GeneratorKind.LOGNORMAL:
        return math.exp(
            rng.normal(
                float(generator.params["mean"]),
                float(generator.params["stddev"]),
            )
        )
    if generator.kind is GeneratorKind.UNIFORM:
        return rng.uniform(float(generator.params["low"]), float(generator.params["high"]))
    if generator.kind is GeneratorKind.EXP:
        return rng.exponential(float(generator.params["lambda"]))
    if generator.kind is GeneratorKind.BETA:
        return rng.beta(float(generator.params["alpha"]), float(generator.params["beta"]))
    if generator.kind is GeneratorKind.LAPLACE:
        return _laplace_sample(
            rng,
            float(generator.params["mean"]),
            float(generator.params["scale"]),
        )
    if generator.kind is GeneratorKind.WEIBULL:
        return _weibull_sample(
            rng,
            float(generator.params["shape"]),
            float(generator.params["scale"]),
        )
    if generator.kind is GeneratorKind.POISSON:
        lam = float(generator.params["lambda"])
        if lam <= 0:
            return 0
        return rng.poisson(lam)
    if generator.kind is GeneratorKind.GAMMA:
        shape = float(generator.params["shape"])
        scale = float(generator.params["scale"])
        if shape <= 0 or scale <= 0:
            return 0.0
        return rng.gamma(shape, scale)
    if generator.kind is GeneratorKind.ZIPF:
        alpha = float(generator.params["alpha"])
        if alpha <= 1:
            return 1
        return rng.zipf(alpha)
    if generator.kind is GeneratorKind.PARETO:
        alpha = float(generator.params["alpha"])
        if alpha <= 0:
            return 1.0
        return rng.pareto(alpha)
    if generator.kind is GeneratorKind.CATEGORICAL:
        count = int(generator.params["count"])
        return f"v{int(rng.random() * count)}"
    if generator.kind is GeneratorKind.ENUM:
        labels = generator.params["labels"]
        size = len(labels)
        return labels[int(rng.random() * size)]
    if generator.kind is GeneratorKind.SEQUENCE:
        start = generator.params["start"]
        step = generator.params["step"]
        if _is_integral(step):
            return int(start)
        return float(start)
    if generator.kind is GeneratorKind.DATE:
        start = date.fromisoformat(generator.params["start"])
        end = date.fromisoformat(generator.params["end"])
        start_ord = start.toordinal()
        span = end.toordinal() - start_ord
        return date.fromordinal(start_ord + int(rng.random() * (span + 1)))
    if generator.kind is GeneratorKind.BOOLEAN:
        return rng.random() < 0.5
    if generator.kind is GeneratorKind.BINARY:
        length = int(generator.params["length"])
        return rng.randbytes(length)
    if generator.kind is GeneratorKind.DATETIME:
        start = datetime.fromisoformat(generator.params["start"])
        end = datetime.fromisoformat(generator.params["end"])
        tz_name = generator.params.get("time_zone")
        if tz_name:
            tz = ZoneInfo(tz_name)
            if start.tzinfo is None:
                start = start.replace(tzinfo=tz)
            if end.tzinfo is None:
                end = end.replace(tzinfo=tz)
        if end <= start:
            return start
        return start + (end - start) * rng.random()
    if generator.kind is GeneratorKind.TIME:
        start_token = generator.params.get("start")
        end_token = generator.params.get("end")
        if start_token is None or end_token is None:
            return _random_time(rng)
        start_us = _time_to_microseconds(time.fromisoformat(start_token))
        end_us = _time_to_microseconds(time.fromisoformat(end_token))
        if end_us <= start_us:
            return _microseconds_to_time(start_us)
        offset = int(rng.random() * (end_us - start_us + 1))
        return _microseconds_to_time(start_us + offset)
    if generator.kind is GeneratorKind.DURATION:
        low = float(generator.params["low"])
        high = float(generator.params["high"])
        if high <= low:
            return timedelta(seconds=low)
        return timedelta(seconds=rng.uniform(low, high))
    if generator.kind is GeneratorKind.LIST_INT:
        min_length = int(generator.params["min_length"])
        max_length = int(generator.params["max_length"])
        low = int(generator.params["low"])
        high = int(generator.params["high"])
        length = min_length if max_length <= min_length else rng.randint(min_length, max_length)
        if length <= 0:
            return []
        if high <= low:
            return [low for _ in range(length)]
        return [rng.randint(low, high) for _ in range(length)]
    if generator.kind is GeneratorKind.NULL:
        return None
    if generator.kind is GeneratorKind.TIME_SERIES:
        return rng.normal(0.0, 1.0)
    raise MaterializationError(f"unsupported generator kind for unique resample: {generator.kind}")


# ---------------------------------------------------------------------------
# Expressions
# ---------------------------------------------------------------------------


class ExpressionError(MaterializationError):
    """Raised when an expression column fails to compile."""


_ALLOWED_NAMES = {
    "pl",
    "idx",
    "dayofyear",
    "log",
    "exp",
    "abs",
    "sin",
    "cos",
    "pi",
    "None",
    "True",
    "False",
}


def _compile_expression(raw_expression: str, available: Sequence[str], column_name: str) -> pl.Expr:
    expression = raw_expression.strip()
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(f"invalid expression for column '{column_name}': {exc}") from exc

    inspector = _ExpressionInspector()
    inspector.visit(tree)

    missing = inspector.column_refs.difference(available)
    if missing:
        missing_name = sorted(missing)[0]
        pointer = _build_pointer(expression, missing_name)
        raise ExpressionError(
            f"column '{missing_name}' referenced before definition in '{column_name}' expression\n"
            f"{expression}\n{pointer}"
        )

    env = _expression_env()
    try:
        compiled = eval(compile(tree, filename="<expr>", mode="eval"), {"__builtins__": {}}, env)
    except Exception as exc:
        raise ExpressionError(f"error evaluating expression for '{column_name}': {exc}") from exc

    if not isinstance(compiled, pl.Expr):
        compiled = pl.lit(compiled)
    return compiled


class _ExpressionInspector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.column_refs: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        if node.id not in _ALLOWED_NAMES:
            raise ExpressionError(f"name '{node.id}' is not allowed in expressions")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name) and func.id == "idx" and node.args:
            raise ExpressionError("idx() does not accept arguments")
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "col"
            and isinstance(func.value, ast.Name)
            and func.value.id == "pl"
        ):
            if (
                not node.args
                or not isinstance(node.args[0], ast.Constant)
                or not isinstance(node.args[0].value, str)
            ):
                raise ExpressionError("pl.col expects a string literal")
            self.column_refs.add(node.args[0].value)
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(
            node,
            (
                ast.Import,
                ast.ImportFrom,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.Lambda,
                ast.ListComp,
                ast.SetComp,
                ast.GeneratorExp,
                ast.DictComp,
                ast.ClassDef,
                ast.While,
                ast.For,
                ast.AsyncFor,
                ast.With,
                ast.If,
                ast.Assert,
                ast.Delete,
                ast.Try,
            ),
        ):
            raise ExpressionError("statement forms are not allowed in expressions")
        super().generic_visit(node)


def _expression_env() -> dict[str, Any]:
    def _ensure_expr(value: Any) -> pl.Expr:
        return value if isinstance(value, pl.Expr) else pl.lit(value)

    return {
        "pl": pl,
        "idx": lambda: pl.int_range(0, pl.len()),
        "dayofyear": lambda expr: _ensure_expr(expr).dt.ordinal_day(),
        "log": lambda expr: _ensure_expr(expr).log(),
        "exp": lambda expr: _ensure_expr(expr).exp(),
        "abs": lambda expr: _ensure_expr(expr).abs(),
        "sin": lambda expr: _ensure_expr(expr).sin(),
        "cos": lambda expr: _ensure_expr(expr).cos(),
        "pi": math.pi,
        "True": True,
        "False": False,
        "None": None,
    }


def _build_pointer(expression: str, missing: str) -> str:
    target = f'"{missing}"'
    index = expression.find(target)
    if index == -1:
        index = expression.find(missing)
    if index == -1:
        return "^"
    return " " * index + "^"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cast_datetime_series(series: pl.Series, params: dict[str, Any]) -> pl.Series:
    time_unit = params.get("time_unit")
    time_zone = params.get("time_zone")
    if time_unit is None and time_zone is None:
        return series

    current_dtype = series.dtype if isinstance(series.dtype, pl.Datetime) else None
    current_unit = current_dtype.time_unit if current_dtype is not None else None
    current_zone = current_dtype.time_zone if current_dtype is not None else None

    target_unit = time_unit or current_unit or "us"
    target_zone = time_zone if time_zone is not None else current_zone
    target_dtype = pl.Datetime(time_unit=target_unit, time_zone=target_zone)

    if series.dtype == target_dtype:
        return series

    return series.cast(target_dtype)


def _cast_series_dtype(series: pl.Series, dtype: Any | None) -> pl.Series:
    if dtype is None:
        return series
    return series.cast(dtype)


def _evaluate_unary(series: pl.Series, expr: pl.Expr) -> pl.Series:
    return series.to_frame().select(expr.alias(series.name)).to_series()


def _is_integral(number: Decimal) -> bool:
    return number == number.to_integral_value()


def _to_series(name: str, values: list[Any]) -> pl.Series:
    if values and isinstance(values[0], date):
        return pl.Series(name, values, dtype=pl.Date)
    if values and isinstance(values[0], datetime):
        return pl.Series(name, values, dtype=pl.Datetime)
    return pl.Series(name, values)


def _laplace_sample(rng: DeterministicRNG, mean: float, scale: float) -> float:
    if scale <= 0:
        raise MaterializationError("laplace() scale must be positive")
    u = rng.random() - 0.5
    sign = -1.0 if u < 0 else 1.0
    return mean - scale * sign * math.log(1 - 2 * abs(u))


def _weibull_sample(rng: DeterministicRNG, shape: float, scale: float) -> float:
    if shape <= 0 or scale <= 0:
        raise MaterializationError("weibull() expects positive shape and scale")
    u = max(1.0 - rng.random(), 1e-12)
    return scale * (-math.log(u)) ** (1.0 / shape)


__all__ = ["MaterializationError", "materialize_spec"]

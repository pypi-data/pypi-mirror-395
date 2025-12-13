"""Normalization helpers for semi-compact synthetic dataset specs."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, getcontext

from .dtypes import format_dtype
from .types import (
    ColumnSpec,
    ExpressionColumnSpec,
    GeneratedColumnSpec,
    GeneratorKind,
    GeneratorSpec,
    Modifier,
    ModifierKind,
    SeasonComponent,
    Spec,
)

__all__ = [
    "format_decimal",
    "format_int",
    "format_row_count",
    "normalize_spec",
    "normalize_string",
    "normalize_generated_definition",
    "to_decimal",
]

NumberLike = int | float | Decimal | str

# Provide sufficient precision for intermediate arithmetic
getcontext().prec = 28


def to_decimal(value: NumberLike) -> Decimal:
    """Convert ``value`` into a :class:`~decimal.Decimal`."""

    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, str):
        return Decimal(value)
    raise TypeError(f"Unsupported number type: {type(value)!r}")


def format_decimal(value: NumberLike) -> str:
    """Return the canonical textual form for ``value``."""

    dec = to_decimal(value)
    if dec.is_nan() or dec.is_infinite():
        raise ValueError("NaN or infinite values are not supported")
    if dec == 0:
        return "0"

    normalized = dec.normalize()
    sign = "-" if normalized.is_signed() else ""
    digits = "".join(str(d) for d in normalized.as_tuple().digits)
    exponent = normalized.as_tuple().exponent

    # Plain representation
    if exponent >= 0:
        plain = sign + digits + ("0" * exponent)
    else:
        split = len(digits) + exponent
        if split > 0:
            plain = sign + digits[:split] + "." + digits[split:]
        else:
            plain = sign + "0." + "0" * (-split) + digits
        plain = plain.rstrip("0").rstrip(".")

    # Scientific representation
    sci_exponent = exponent + len(digits) - 1
    mantissa_digits = digits[0]
    if len(digits) > 1:
        mantissa_digits += "." + digits[1:]
    mantissa_digits = mantissa_digits.rstrip("0").rstrip(".")
    sci = f"{sign}{mantissa_digits}e{sci_exponent}"

    if exponent >= 6 or exponent <= -3:
        return sci
    return plain


def format_int(value: int) -> str:
    """Format an integer for normalized output."""

    return str(int(value))


ROW_SUFFIXES: Sequence[tuple[str, int]] = (
    ("t", 1_000_000_000_000),
    ("g", 1_000_000_000),
    ("m", 1_000_000),
    ("k", 1_000),
)


def format_row_count(rows: int) -> str:
    """Return canonical row-count token (e.g. ``100kr``)."""

    for suffix, multiplier in ROW_SUFFIXES:
        if rows % multiplier == 0:
            scaled = rows // multiplier
            if 1 <= scaled < 1000:
                return f"{scaled}{suffix}r"
    return f"{rows}r"


def normalize_spec(spec: Spec) -> str:
    """Render ``spec`` as the canonical semi-compact string."""

    head = format_row_count(spec.rows)
    body = ";".join(_normalize_column(column) for column in spec.columns)
    return f"{head}/{body}"


def normalize_string(source: str) -> str:
    """Parse and normalize ``source`` into its canonical form."""

    from .parser import parse_spec

    return normalize_spec(parse_spec(source))


def _normalize_column(column: ColumnSpec) -> str:
    dtype_fragment = f":{format_dtype(column.dtype)}" if column.dtype is not None else ""
    if isinstance(column.definition, ExpressionColumnSpec):
        expr = column.definition.expression.strip()
        return f"{column.name}{dtype_fragment}=@({expr})"
    assert isinstance(column.definition, GeneratedColumnSpec)
    generator_fragment = normalize_generated_definition(column.definition)
    return f"{column.name}{dtype_fragment}={generator_fragment}"


def normalize_generated_definition(definition: GeneratedColumnSpec) -> str:
    generator = _normalize_generator(definition.generator)
    modifiers = "".join(_normalize_modifier(mod) for mod in definition.modifiers)
    return f"{generator}{modifiers}"


def _normalize_generator(generator: GeneratorSpec) -> str:
    params = generator.params
    if generator.kind is GeneratorKind.NORMAL:
        return f"normal({format_decimal(params['mean'])},{format_decimal(params['stddev'])})"
    if generator.kind is GeneratorKind.LOGNORMAL:
        return f"lognormal({format_decimal(params['mean'])},{format_decimal(params['stddev'])})"
    if generator.kind is GeneratorKind.UNIFORM:
        return f"uniform({format_decimal(params['low'])},{format_decimal(params['high'])})"
    if generator.kind is GeneratorKind.EXP:
        return f"exp({format_decimal(params['lambda'])})"
    if generator.kind is GeneratorKind.BETA:
        return f"beta({format_decimal(params['alpha'])},{format_decimal(params['beta'])})"
    if generator.kind is GeneratorKind.LAPLACE:
        return f"laplace({format_decimal(params['mean'])},{format_decimal(params['scale'])})"
    if generator.kind is GeneratorKind.WEIBULL:
        return f"weibull({format_decimal(params['shape'])},{format_decimal(params['scale'])})"
    if generator.kind is GeneratorKind.POISSON:
        return f"poisson({format_decimal(params['lambda'])})"
    if generator.kind is GeneratorKind.GAMMA:
        return f"gamma({format_decimal(params['shape'])},{format_decimal(params['scale'])})"
    if generator.kind is GeneratorKind.ZIPF:
        return f"zipf({format_decimal(params['alpha'])})"
    if generator.kind is GeneratorKind.PARETO:
        return f"pareto({format_decimal(params['alpha'])})"
    if generator.kind is GeneratorKind.CATEGORICAL:
        return f"categorical({format_int(params['count'])})"
    if generator.kind is GeneratorKind.ENUM:
        labels = ",".join(params["labels"])
        return f"enum[{labels}]"
    if generator.kind is GeneratorKind.SEQUENCE:
        return f"sequence({format_decimal(params['start'])},{format_decimal(params['step'])})"
    if generator.kind is GeneratorKind.DATE:
        return f"date[{params['start']},{params['end']}]"
    if generator.kind is GeneratorKind.BOOLEAN:
        return "bool()"
    if generator.kind is GeneratorKind.BINARY:
        return f"binary({format_int(params['length'])})"
    if generator.kind is GeneratorKind.DATETIME:
        pieces = [params["start"], params["end"], f"unit={params['time_unit']}"]
        time_zone = params.get("time_zone")
        if time_zone:
            pieces.append(f"tz={time_zone}")
        return f"datetime[{','.join(pieces)}]"
    if generator.kind is GeneratorKind.TIME:
        start = params.get("start")
        end = params.get("end")
        if start is None or end is None:
            return "time[]"
        return f"time[{start},{end}]"
    if generator.kind is GeneratorKind.DURATION:
        return f"duration({format_decimal(params['low'])},{format_decimal(params['high'])})"
    if generator.kind is GeneratorKind.LIST_INT:
        return "list_int({},{},{},{})".format(
            format_int(params["min_length"]),
            format_int(params["max_length"]),
            format_int(params["low"]),
            format_int(params["high"]),
        )
    if generator.kind is GeneratorKind.LIST:
        element = normalize_generated_definition(params["element"])
        min_length = int(params["min_length"])
        max_length = int(params["max_length"])
        if min_length == max_length:
            bounds = format_int(min_length)
        else:
            bounds = f"{format_int(min_length)},{format_int(max_length)}"
        return f"list{{{element}}}({bounds})"
    if generator.kind is GeneratorKind.ARRAY:
        element = normalize_generated_definition(params["element"])
        size = format_int(params["size"])
        return f"array{{{element}}}({size})"
    if generator.kind is GeneratorKind.STRUCT:
        field_parts = [
            f"{field.name}={normalize_generated_definition(field.definition)}"
            for field in params["fields"]
        ]
        joined = ",".join(field_parts)
        return f"struct{{{joined}}}"
    if generator.kind is GeneratorKind.NULL:
        return "null()"
    if generator.kind is GeneratorKind.TIME_SERIES:
        return _normalize_time_series(params)
    raise ValueError(f"Unsupported generator kind: {generator.kind}")


def _normalize_time_series(params: Mapping[str, object]) -> str:
    freq = params["freq"]
    start = params["start"]
    trend = format_decimal(params["trend"])
    segments: list[str] = [f"ts({freq},{start},trend={trend}"]
    seasons: Iterable[SeasonComponent] = params.get("seasons", ())
    if seasons:
        season_str = "+".join(
            f"{format_decimal(component.period)}:{format_decimal(component.amplitude)}"
            for component in seasons
        )
        segments.append(f"season={season_str}")
    noise: GeneratorSpec | None = params.get("noise")
    if noise is not None:
        noise_str = _normalize_generator(noise)
        segments.append(f"noise={noise_str}")
    return ",".join(segments) + ")"


def _normalize_modifier(modifier: Modifier) -> str:
    params = modifier.params
    if modifier.kind is ModifierKind.CLIP:
        return f"~clip({format_decimal(params['low'])},{format_decimal(params['high'])})"
    if modifier.kind is ModifierKind.NOISE_NORMAL:
        return f"+noise normal({format_decimal(params['mean'])},{format_decimal(params['stddev'])})"
    if modifier.kind is ModifierKind.LOG:
        return "|log"
    if modifier.kind is ModifierKind.EXP:
        return "|exp"
    if modifier.kind is ModifierKind.ABS:
        return "|abs"
    if modifier.kind is ModifierKind.SCALE:
        return f"*{format_decimal(params['value'])}"
    if modifier.kind is ModifierKind.OFFSET:
        return f"+{format_decimal(params['value'])}"
    if modifier.kind is ModifierKind.NULL_PERCENT:
        return f"?{format_decimal(params['value'])}"
    if modifier.kind is ModifierKind.UNIQUE:
        return "!"
    raise ValueError(f"Unsupported modifier: {modifier.kind}")


__all__ = [
    "format_decimal",
    "format_int",
    "format_row_count",
    "normalize_spec",
    "normalize_string",
    "to_decimal",
]

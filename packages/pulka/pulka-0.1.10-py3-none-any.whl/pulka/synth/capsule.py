"""Capsule64 encoding for synthetic dataset specifications."""

from __future__ import annotations

import base64
import re
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from .determinism import normalized_spec_hash
from .dtypes import DTypeParseError, format_dtype, parse_dtype
from .normalize import (
    format_decimal,
    normalize_generated_definition,
    normalize_spec,
    to_decimal,
)
from .parser import parse_spec
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
    StructFieldSpec,
)

_HEADER_BYTE = 0x24  # enc=0b001, spec_version=0b001, reserved=0b00
_TRAILER_LEN = 16
_CAPSULE_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class CapsuleError(ValueError):
    """Raised when capsule encoding or decoding fails."""


@dataclass
class CapsulePayload:
    spec: Spec
    normalized: str


_GENERATOR_OPCODE: dict[GeneratorKind, int] = {
    GeneratorKind.UNIFORM: 0x01,
    GeneratorKind.NORMAL: 0x02,
    GeneratorKind.LOGNORMAL: 0x03,
    GeneratorKind.EXP: 0x05,
    GeneratorKind.BETA: 0x07,
    GeneratorKind.CATEGORICAL: 0x0A,
    GeneratorKind.ENUM: 0x0B,
    GeneratorKind.SEQUENCE: 0x0C,
    GeneratorKind.DATE: 0x0D,
    GeneratorKind.TIME_SERIES: 0x0E,
    GeneratorKind.LAPLACE: 0x10,
    GeneratorKind.WEIBULL: 0x11,
    GeneratorKind.BOOLEAN: 0x12,
    GeneratorKind.BINARY: 0x13,
    GeneratorKind.DATETIME: 0x14,
    GeneratorKind.TIME: 0x15,
    GeneratorKind.DURATION: 0x16,
    GeneratorKind.LIST_INT: 0x17,
    GeneratorKind.NULL: 0x18,
    GeneratorKind.POISSON: 0x19,
    GeneratorKind.GAMMA: 0x1A,
    GeneratorKind.ZIPF: 0x1B,
    GeneratorKind.PARETO: 0x1C,
    GeneratorKind.LIST: 0x1D,
    GeneratorKind.ARRAY: 0x1E,
    GeneratorKind.STRUCT: 0x1F,
}

_GENERATOR_FROM_OPCODE = {value: key for key, value in _GENERATOR_OPCODE.items()}

_EXPRESSION_OPCODE = 0x0F

_MODIFIER_OPCODE: dict[ModifierKind, int] = {
    ModifierKind.CLIP: 0x21,
    ModifierKind.NOISE_NORMAL: 0x22,
    ModifierKind.LOG: 0x23,
    ModifierKind.EXP: 0x24,
    ModifierKind.ABS: 0x25,
    ModifierKind.SCALE: 0x26,
    ModifierKind.OFFSET: 0x27,
    ModifierKind.NULL_PERCENT: 0x28,
    ModifierKind.UNIQUE: 0x29,
}

_MODIFIER_FROM_OPCODE = {value: key for key, value in _MODIFIER_OPCODE.items()}


def to_capsule(spec: Spec, normalized: str | None = None) -> str:
    """Encode ``spec`` into a capsule64 string."""

    normalized = normalized or normalize_spec(spec)
    buffer = bytearray()
    buffer.append(_HEADER_BYTE)
    buffer.extend(_encode_varint(spec.rows))
    buffer.extend(_encode_varint(len(spec.columns)))
    for column in spec.columns:
        buffer.extend(_encode_column(column))
    trailer = normalized_spec_hash(normalized)
    buffer.extend(trailer)
    token = base64.urlsafe_b64encode(bytes(buffer)).rstrip(b"=")
    return token.decode("ascii")


def from_capsule(token: str) -> CapsulePayload:
    """Decode ``token`` back into :class:`Spec` plus normalized text."""

    if not _CAPSULE_RE.match(token):
        raise CapsuleError("capsule string must be base64url characters only")
    data = _decode_base64(token)
    if len(data) <= _TRAILER_LEN:
        raise CapsuleError("capsule too short")
    if data[0] != _HEADER_BYTE:
        raise CapsuleError("invalid capsule header")

    view = memoryview(data)
    offset = 1
    rows, offset = _decode_varint(view, offset)
    column_count, offset = _decode_varint(view, offset)

    columns: list[ColumnSpec] = []
    for _ in range(column_count):
        column, offset = _decode_column(view, offset)
        columns.append(column)

    if len(data) - offset != _TRAILER_LEN:
        raise CapsuleError("extra data before trailer")
    trailer = bytes(view[offset : offset + _TRAILER_LEN])

    spec = Spec(rows=rows, columns=tuple(columns))
    normalized = normalize_spec(spec)
    expected = normalized_spec_hash(normalized)
    if expected != trailer:
        raise CapsuleError("capsule integrity failure")
    return CapsulePayload(spec=spec, normalized=normalized)


def is_capsule(candidate: str) -> bool:
    """Return ``True`` if ``candidate`` looks like a capsule string."""

    if not _CAPSULE_RE.match(candidate):
        return False
    try:
        data = _decode_base64(candidate)
    except CapsuleError:
        return False
    return bool(data) and data[0] == _HEADER_BYTE


# ---------------------------------------------------------------------------
# Encoding helpers
# ---------------------------------------------------------------------------


def _encode_column(column: ColumnSpec) -> bytes:
    payload = bytearray()
    payload.extend(_encode_string(column.name))
    definition = column.definition
    dtype = column.dtype
    dtype_flag = dtype is not None
    if isinstance(definition, ExpressionColumnSpec):
        opcode = _EXPRESSION_OPCODE | (0x80 if dtype_flag else 0)
        payload.append(opcode)
        if dtype_flag:
            payload.extend(_encode_string(format_dtype(dtype)))
        payload.extend(_encode_string(definition.expression.strip()))
        return bytes(payload)

    generator = definition.generator
    opcode = _GENERATOR_OPCODE.get(generator.kind)
    if opcode is None:
        raise CapsuleError(f"unsupported generator kind {generator.kind}")
    opcode |= 0x80 if dtype_flag else 0
    payload.append(opcode)
    if dtype_flag:
        payload.extend(_encode_string(format_dtype(dtype)))
    payload.extend(_encode_generator(generator))
    payload.extend(_encode_modifiers(definition.modifiers))
    return bytes(payload)


def _encode_generator(generator: GeneratorSpec) -> bytes:
    params = generator.params
    kind = generator.kind
    data = bytearray()
    if kind is GeneratorKind.UNIFORM:
        data.extend(_encode_string(format_decimal(params["low"])))
        data.extend(_encode_string(format_decimal(params["high"])))
    elif kind in {GeneratorKind.NORMAL, GeneratorKind.LOGNORMAL}:
        data.extend(_encode_string(format_decimal(params["mean"])))
        data.extend(_encode_string(format_decimal(params["stddev"])))
    elif kind is GeneratorKind.EXP:
        data.extend(_encode_string(format_decimal(params["lambda"])))
    elif kind is GeneratorKind.BETA:
        data.extend(_encode_string(format_decimal(params["alpha"])))
        data.extend(_encode_string(format_decimal(params["beta"])))
    elif kind is GeneratorKind.LAPLACE:
        data.extend(_encode_string(format_decimal(params["mean"])))
        data.extend(_encode_string(format_decimal(params["scale"])))
    elif kind is GeneratorKind.WEIBULL:
        data.extend(_encode_string(format_decimal(params["shape"])))
        data.extend(_encode_string(format_decimal(params["scale"])))
    elif kind is GeneratorKind.POISSON:
        data.extend(_encode_string(format_decimal(params["lambda"])))
    elif kind is GeneratorKind.GAMMA:
        data.extend(_encode_string(format_decimal(params["shape"])))
        data.extend(_encode_string(format_decimal(params["scale"])))
    elif kind in {GeneratorKind.ZIPF, GeneratorKind.PARETO}:
        data.extend(_encode_string(format_decimal(params["alpha"])))
    elif kind is GeneratorKind.CATEGORICAL:
        data.extend(_encode_varint(params["count"]))
    elif kind is GeneratorKind.ENUM:
        labels = params["labels"]
        data.extend(_encode_varint(len(labels)))
        for label in labels:
            data.extend(_encode_string(label))
    elif kind is GeneratorKind.SEQUENCE:
        data.extend(_encode_string(format_decimal(params["start"])))
        data.extend(_encode_string(format_decimal(params["step"])))
    elif kind is GeneratorKind.DATE:
        data.extend(_encode_string(params["start"]))
        data.extend(_encode_string(params["end"]))
    elif kind is GeneratorKind.BOOLEAN:
        pass
    elif kind is GeneratorKind.BINARY:
        data.extend(_encode_varint(int(params["length"])))
    elif kind is GeneratorKind.DATETIME:
        data.extend(_encode_string(params["start"]))
        data.extend(_encode_string(params["end"]))
        data.extend(_encode_string(params["time_unit"]))
        time_zone = params.get("time_zone")
        if time_zone is None:
            data.extend(_encode_varint(0))
        else:
            data.extend(_encode_varint(1))
            data.extend(_encode_string(time_zone))
    elif kind is GeneratorKind.TIME:
        start = params.get("start")
        if start is None:
            data.extend(_encode_varint(0))
        else:
            data.extend(_encode_varint(1))
            data.extend(_encode_string(start))
            data.extend(_encode_string(params["end"]))
    elif kind is GeneratorKind.DURATION:
        data.extend(_encode_string(format_decimal(params["low"])))
        data.extend(_encode_string(format_decimal(params["high"])))
    elif kind is GeneratorKind.LIST_INT:
        data.extend(_encode_varint(int(params["min_length"])))
        data.extend(_encode_varint(int(params["max_length"])))
        data.extend(_encode_varint(int(params["low"])))
        data.extend(_encode_varint(int(params["high"])))
    elif kind is GeneratorKind.LIST:
        element_fragment = normalize_generated_definition(params["element"])
        data.extend(_encode_string(element_fragment))
        data.extend(_encode_varint(int(params["min_length"])))
        data.extend(_encode_varint(int(params["max_length"])))
    elif kind is GeneratorKind.ARRAY:
        element_fragment = normalize_generated_definition(params["element"])
        data.extend(_encode_string(element_fragment))
        data.extend(_encode_varint(int(params["size"])))
    elif kind is GeneratorKind.STRUCT:
        fields: Sequence[StructFieldSpec] = params["fields"]
        data.extend(_encode_varint(len(fields)))
        for field in fields:
            data.extend(_encode_string(field.name))
            data.extend(_encode_string(normalize_generated_definition(field.definition)))
    elif kind is GeneratorKind.NULL:
        pass
    elif kind is GeneratorKind.TIME_SERIES:
        data.extend(_encode_string(params["freq"]))
        data.extend(_encode_string(params["start"]))
        data.extend(_encode_string(format_decimal(params["trend"])))
        seasons: Sequence[SeasonComponent] = params.get("seasons", ())
        data.extend(_encode_varint(len(seasons)))
        for component in seasons:
            data.extend(_encode_string(format_decimal(component.period)))
            data.extend(_encode_string(format_decimal(component.amplitude)))
        noise: GeneratorSpec | None = params.get("noise")
        if noise is None:
            data.append(0)
        else:
            data.append(1)
            data.extend(_encode_string(format_decimal(noise.params["mean"])))
            data.extend(_encode_string(format_decimal(noise.params["stddev"])))
    else:
        raise CapsuleError(f"unsupported generator {generator.kind}")
    return bytes(data)


def _encode_modifiers(modifiers: Sequence[Modifier]) -> bytes:
    payload = bytearray()
    payload.extend(_encode_varint(len(modifiers)))
    for modifier in modifiers:
        opcode = _MODIFIER_OPCODE.get(modifier.kind)
        if opcode is None:
            raise CapsuleError(f"unsupported modifier {modifier.kind}")
        payload.append(opcode)
        params = modifier.params
        if modifier.kind is ModifierKind.CLIP:
            payload.extend(_encode_string(format_decimal(params["low"])))
            payload.extend(_encode_string(format_decimal(params["high"])))
        elif modifier.kind is ModifierKind.NOISE_NORMAL:
            payload.extend(_encode_string(format_decimal(params["mean"])))
            payload.extend(_encode_string(format_decimal(params["stddev"])))
        elif modifier.kind in {
            ModifierKind.LOG,
            ModifierKind.EXP,
            ModifierKind.ABS,
            ModifierKind.UNIQUE,
        }:
            continue
        elif modifier.kind in {
            ModifierKind.SCALE,
            ModifierKind.OFFSET,
            ModifierKind.NULL_PERCENT,
        }:
            payload.extend(_encode_string(format_decimal(params["value"])))
        else:
            raise CapsuleError(f"unsupported modifier {modifier.kind}")
    return bytes(payload)


# ---------------------------------------------------------------------------
# Decoding helpers
# ---------------------------------------------------------------------------


def _decode_column(data: memoryview, offset: int) -> tuple[ColumnSpec, int]:
    name, offset = _decode_string(data, offset)
    opcode = data[offset]
    offset += 1
    has_dtype = bool(opcode & 0x80)
    base_opcode = opcode & 0x7F
    dtype = None
    if has_dtype:
        dtype_text, offset = _decode_string(data, offset)
        try:
            dtype = parse_dtype(dtype_text)
        except DTypeParseError as exc:
            raise CapsuleError(f"invalid dtype annotation: {exc}") from exc

    if base_opcode == _EXPRESSION_OPCODE:
        expr, offset = _decode_string(data, offset)
        column = ColumnSpec(
            name=name,
            dtype=dtype,
            definition=ExpressionColumnSpec(expression=expr),
        )
        return column, offset

    generator_kind = _GENERATOR_FROM_OPCODE.get(base_opcode)
    if generator_kind is None:
        raise CapsuleError(f"unknown generator opcode {opcode:#x}")
    generator, offset = _decode_generator(generator_kind, data, offset)
    modifiers, offset = _decode_modifiers(data, offset)
    column = ColumnSpec(
        name=name,
        dtype=dtype,
        definition=GeneratedColumnSpec(generator=generator, modifiers=tuple(modifiers)),
    )
    return column, offset


def _decode_generator(
    kind: GeneratorKind, data: memoryview, offset: int
) -> tuple[GeneratorSpec, int]:
    if kind is GeneratorKind.UNIFORM:
        low, offset = _decode_decimal(data, offset)
        high, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"low": low, "high": high}), offset
    if kind in {GeneratorKind.NORMAL, GeneratorKind.LOGNORMAL}:
        mean, offset = _decode_decimal(data, offset)
        stddev, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"mean": mean, "stddev": stddev}), offset
    if kind is GeneratorKind.EXP:
        lam, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"lambda": lam}), offset
    if kind is GeneratorKind.BETA:
        alpha, offset = _decode_decimal(data, offset)
        beta_value, offset = _decode_decimal(data, offset)
        if alpha != alpha.to_integral() or beta_value != beta_value.to_integral():
            raise CapsuleError("beta() capsule stored non-integer parameters")
        return (
            GeneratorSpec(
                kind=kind,
                params={"alpha": int(alpha), "beta": int(beta_value)},
            ),
            offset,
        )
    if kind is GeneratorKind.LAPLACE:
        mean, offset = _decode_decimal(data, offset)
        scale, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"mean": mean, "scale": scale}), offset
    if kind is GeneratorKind.WEIBULL:
        shape, offset = _decode_decimal(data, offset)
        scale, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"shape": shape, "scale": scale}), offset
    if kind is GeneratorKind.POISSON:
        lam, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"lambda": lam}), offset
    if kind is GeneratorKind.GAMMA:
        shape, offset = _decode_decimal(data, offset)
        scale, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"shape": shape, "scale": scale}), offset
    if kind in {GeneratorKind.ZIPF, GeneratorKind.PARETO}:
        alpha, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"alpha": alpha}), offset
    if kind is GeneratorKind.CATEGORICAL:
        count, offset = _decode_varint(data, offset)
        return GeneratorSpec(kind=kind, params={"count": count}), offset
    if kind is GeneratorKind.ENUM:
        label_count, offset = _decode_varint(data, offset)
        labels: list[str] = []
        for _ in range(label_count):
            label, offset = _decode_string(data, offset)
            labels.append(label)
        return GeneratorSpec(kind=kind, params={"labels": tuple(labels)}), offset
    if kind is GeneratorKind.SEQUENCE:
        start, offset = _decode_decimal(data, offset)
        step, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"start": start, "step": step}), offset
    if kind is GeneratorKind.DATE:
        start, offset = _decode_string(data, offset)
        end, offset = _decode_string(data, offset)
        return GeneratorSpec(kind=kind, params={"start": start, "end": end}), offset
    if kind is GeneratorKind.BOOLEAN:
        return GeneratorSpec(kind=kind, params={}), offset
    if kind is GeneratorKind.BINARY:
        length, offset = _decode_varint(data, offset)
        return GeneratorSpec(kind=kind, params={"length": length}), offset
    if kind is GeneratorKind.DATETIME:
        start, offset = _decode_string(data, offset)
        end, offset = _decode_string(data, offset)
        unit, offset = _decode_string(data, offset)
        tz_flag, offset = _decode_varint(data, offset)
        time_zone: str | None = None
        if tz_flag:
            time_zone, offset = _decode_string(data, offset)
        params = {
            "start": start,
            "end": end,
            "time_unit": unit,
            "time_zone": time_zone,
        }
        return GeneratorSpec(kind=kind, params=params), offset
    if kind is GeneratorKind.TIME:
        flag, offset = _decode_varint(data, offset)
        if flag:
            start, offset = _decode_string(data, offset)
            end, offset = _decode_string(data, offset)
        else:
            start = None
            end = None
        return GeneratorSpec(kind=kind, params={"start": start, "end": end}), offset
    if kind is GeneratorKind.DURATION:
        low, offset = _decode_decimal(data, offset)
        high, offset = _decode_decimal(data, offset)
        return GeneratorSpec(kind=kind, params={"low": low, "high": high}), offset
    if kind is GeneratorKind.LIST_INT:
        min_length, offset = _decode_varint(data, offset)
        max_length, offset = _decode_varint(data, offset)
        low, offset = _decode_varint(data, offset)
        high, offset = _decode_varint(data, offset)
        params = {
            "min_length": int(min_length),
            "max_length": int(max_length),
            "low": int(low),
            "high": int(high),
        }
        return GeneratorSpec(kind=kind, params=params), offset
    if kind is GeneratorKind.LIST:
        fragment, offset = _decode_string(data, offset)
        element = _parse_generated_definition(fragment)
        min_length, offset = _decode_varint(data, offset)
        max_length, offset = _decode_varint(data, offset)
        params = {
            "element": element,
            "min_length": int(min_length),
            "max_length": int(max_length),
        }
        return GeneratorSpec(kind=kind, params=params), offset
    if kind is GeneratorKind.ARRAY:
        fragment, offset = _decode_string(data, offset)
        element = _parse_generated_definition(fragment)
        size, offset = _decode_varint(data, offset)
        params = {"element": element, "size": int(size)}
        return GeneratorSpec(kind=kind, params=params), offset
    if kind is GeneratorKind.STRUCT:
        field_count, offset = _decode_varint(data, offset)
        fields: list[StructFieldSpec] = []
        for _ in range(field_count):
            name, offset = _decode_string(data, offset)
            fragment, offset = _decode_string(data, offset)
            definition = _parse_generated_definition(fragment)
            fields.append(StructFieldSpec(name=name, definition=definition))
        return GeneratorSpec(kind=kind, params={"fields": tuple(fields)}), offset
    if kind is GeneratorKind.NULL:
        return GeneratorSpec(kind=kind, params={}), offset
    if kind is GeneratorKind.TIME_SERIES:
        freq, offset = _decode_string(data, offset)
        start, offset = _decode_string(data, offset)
        trend, offset = _decode_decimal(data, offset)
        season_count, offset = _decode_varint(data, offset)
        seasons: list[SeasonComponent] = []
        for _ in range(season_count):
            period, offset = _decode_decimal(data, offset)
            amplitude, offset = _decode_decimal(data, offset)
            seasons.append(SeasonComponent(period=period, amplitude=amplitude))
        noise_flag = data[offset]
        offset += 1
        noise: GeneratorSpec | None = None
        if noise_flag:
            mean, offset = _decode_decimal(data, offset)
            stddev, offset = _decode_decimal(data, offset)
            noise = GeneratorSpec(
                kind=GeneratorKind.NORMAL,
                params={"mean": mean, "stddev": stddev},
            )
        params = {
            "freq": freq,
            "start": start,
            "trend": trend,
            "seasons": tuple(seasons),
            "noise": noise,
        }
        return GeneratorSpec(kind=kind, params=params), offset
    raise CapsuleError(f"unsupported generator {kind}")


def _decode_modifiers(data: memoryview, offset: int) -> tuple[list[Modifier], int]:
    count, offset = _decode_varint(data, offset)
    modifiers: list[Modifier] = []
    for _ in range(count):
        opcode = data[offset]
        offset += 1
        kind = _MODIFIER_FROM_OPCODE.get(opcode)
        if kind is None:
            raise CapsuleError(f"unknown modifier opcode {opcode:#x}")
        if kind is ModifierKind.CLIP:
            low, offset = _decode_decimal(data, offset)
            high, offset = _decode_decimal(data, offset)
            modifiers.append(Modifier(kind=kind, params={"low": low, "high": high}))
        elif kind is ModifierKind.NOISE_NORMAL:
            mean, offset = _decode_decimal(data, offset)
            stddev, offset = _decode_decimal(data, offset)
            modifiers.append(Modifier(kind=kind, params={"mean": mean, "stddev": stddev}))
        elif kind in {ModifierKind.LOG, ModifierKind.EXP, ModifierKind.ABS, ModifierKind.UNIQUE}:
            modifiers.append(Modifier(kind=kind, params={}))
        elif kind in {ModifierKind.SCALE, ModifierKind.OFFSET, ModifierKind.NULL_PERCENT}:
            value, offset = _decode_decimal(data, offset)
            modifiers.append(Modifier(kind=kind, params={"value": value}))
        else:
            raise CapsuleError(f"unsupported modifier {kind}")
    return modifiers, offset


# ---------------------------------------------------------------------------
# Primitive encoding helpers
# ---------------------------------------------------------------------------


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise CapsuleError("negative varint not supported")
    out = bytearray()
    while True:
        to_write = value & 0x7F
        value >>= 7
        if value:
            out.append(0x80 | to_write)
        else:
            out.append(to_write)
            break
    return bytes(out)


def _decode_varint(data: memoryview, offset: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise CapsuleError("unterminated varint")
        byte = data[offset]
        offset += 1
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
        if shift > 63:
            raise CapsuleError("varint too large")
    return result, offset


def _encode_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return _encode_varint(len(encoded)) + encoded


def _decode_string(data: memoryview, offset: int) -> tuple[str, int]:
    length, offset = _decode_varint(data, offset)
    end = offset + length
    if end > len(data):
        raise CapsuleError("string exceeds capsule length")
    return data[offset:end].tobytes().decode("utf-8"), end


def _decode_decimal(data: memoryview, offset: int) -> tuple[Decimal, int]:
    text, offset = _decode_string(data, offset)
    return to_decimal(text), offset


def _decode_base64(token: str) -> bytes:
    padding = (-len(token)) % 4
    padded = token + "=" * padding
    try:
        return base64.urlsafe_b64decode(padded.encode("ascii"))
    except Exception as exc:  # pragma: no cover
        raise CapsuleError("invalid base64 encoding") from exc


def _parse_generated_definition(fragment: str) -> GeneratedColumnSpec:
    fake_spec = f"1r/__={fragment}"
    spec = parse_spec(fake_spec)
    if len(spec.columns) != 1:
        raise CapsuleError("nested generator must resolve to a single column")
    column = spec.columns[0]
    if not isinstance(column.definition, GeneratedColumnSpec):
        raise CapsuleError("nested generator cannot be an expression")
    return column.definition


__all__ = ["CapsuleError", "CapsulePayload", "from_capsule", "is_capsule", "to_capsule"]

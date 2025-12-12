"""Data models for Pulka synthetic dataset specifications."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any

from polars.datatypes import DataType, DataTypeClass


class GeneratorKind(str, Enum):
    """Enumerates supported generator primitives."""

    NORMAL = "normal"
    LOGNORMAL = "lognormal"
    UNIFORM = "uniform"
    EXP = "exp"
    BETA = "beta"
    LAPLACE = "laplace"
    WEIBULL = "weibull"
    POISSON = "poisson"
    GAMMA = "gamma"
    ZIPF = "zipf"
    PARETO = "pareto"
    CATEGORICAL = "categorical"
    ENUM = "enum"
    SEQUENCE = "sequence"
    DATE = "date"
    TIME_SERIES = "ts"
    BOOLEAN = "bool"
    BINARY = "binary"
    DATETIME = "datetime"
    TIME = "time"
    DURATION = "duration"
    LIST_INT = "list_int"
    LIST = "list"
    ARRAY = "array"
    STRUCT = "struct"
    NULL = "null"
    EXPRESSION = "expr"


class ModifierKind(str, Enum):
    """Enumerates supported column modifiers."""

    CLIP = "clip"
    NOISE_NORMAL = "noise_normal"
    LOG = "log"
    EXP = "exp"
    ABS = "abs"
    SCALE = "scale"
    OFFSET = "offset"
    NULL_PERCENT = "null_percent"
    UNIQUE = "unique"


@dataclass(frozen=True)
class GeneratorSpec:
    """Represents a generator invocation with typed parameters."""

    kind: GeneratorKind
    params: Mapping[str, Any]


@dataclass(frozen=True)
class Modifier:
    """Represents a modifier applied to the output of a generator."""

    kind: ModifierKind
    params: Mapping[str, Any]


@dataclass(frozen=True)
class SeasonComponent:
    """Encodes a seasonal component for the ``ts`` generator."""

    period: Decimal
    amplitude: Decimal


@dataclass(frozen=True)
class GeneratedColumnSpec:
    """A column produced by a generator with optional modifiers."""

    generator: GeneratorSpec
    modifiers: Sequence[Modifier]


@dataclass(frozen=True)
class StructFieldSpec:
    """Represents an individual field within a struct generator."""

    name: str
    definition: GeneratedColumnSpec


@dataclass(frozen=True)
class ExpressionColumnSpec:
    """A column derived from a Polars expression referencing prior columns."""

    expression: str


ColumnDefinition = GeneratedColumnSpec | ExpressionColumnSpec


@dataclass(frozen=True)
class ColumnSpec:
    """A named column in the synthetic dataset specification."""

    name: str
    definition: ColumnDefinition
    dtype: DataType | DataTypeClass | None = None


@dataclass(frozen=True)
class Spec:
    """Top-level specification consisting of row count and column specs."""

    rows: int
    columns: Sequence[ColumnSpec]

    def column_names(self) -> Iterable[str]:
        """Yield the column names in declaration order."""

        for column in self.columns:
            yield column.name

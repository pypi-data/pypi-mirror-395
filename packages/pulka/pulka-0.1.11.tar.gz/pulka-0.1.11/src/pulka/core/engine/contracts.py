"""Engine-facing protocols and tabular data abstractions."""

from __future__ import annotations

import inspect
from collections.abc import Callable, Iterator, Mapping, Sequence, Sized
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, cast, overload

from wcwidth import wcswidth, wcwidth  # type: ignore[import-untyped]

from ...utils import _get_int_env
from ..formatting import _format_float_two_decimals, _is_float_like


@dataclass(slots=True, frozen=True)
class EnginePayloadHandle[PayloadT]:
    """Opaque wrapper describing an engine-specific payload."""

    engine: str
    kind: str
    _payload: PayloadT = field(repr=False)

    def unwrap(
        self,
        *,
        expected_engine: str | None = None,
        expected_kind: str | None = None,
    ) -> PayloadT:
        """Return the underlying payload after validating ``engine``/``kind``."""

        if expected_engine is not None and self.engine != expected_engine:
            msg = f"Handle is backed by engine '{self.engine}', not '{expected_engine}'"
            raise ValueError(msg)
        if expected_kind is not None and self.kind != expected_kind:
            msg = f"Handle is of kind '{self.kind}', not '{expected_kind}'"
            raise ValueError(msg)
        return self._payload

    def as_serializable(self) -> Mapping[str, str]:
        """Return metadata that can be safely serialised."""

        return {"engine": self.engine, "kind": self.kind}


_USE_ARRAY_BACKING = _get_int_env("PULKA_FF_ARRAY_SLICE", None, 1) != 0


def _array_len(array: Any) -> int:
    if isinstance(array, Sized):
        return len(array)
    if hasattr(array, "len"):
        return int(array.len())
    msg = f"Unsupported column backing without __len__: {type(array)!r}"
    raise TypeError(msg)


def _array_slice(array: Any, start: int, length: int | None = None) -> Any:
    length = None if length is None else max(0, length)
    slice_fn = getattr(array, "slice", None)
    if callable(slice_fn):
        slice_length = length if length is not None else _array_len(array) - start
        return slice_fn(start, slice_length)
    if hasattr(array, "__getitem__"):
        end = None if length is None else start + length
        return array[start:end]
    end = _array_len(array) if length is None else start + length
    return tuple(_array_get(array, idx) for idx in range(start, end))


def _array_get(array: Any, index: int) -> Any:
    item = getattr(array, "item", None)
    if callable(item):
        return item(index)
    if hasattr(array, "__getitem__"):
        return array[index]
    msg = f"Unsupported column backing without item access: {type(array)!r}"
    raise TypeError(msg)


def _array_iter(array: Any) -> Iterator[Any]:
    for idx in range(_array_len(array)):
        yield _array_get(array, idx)


def _array_null_count(array: Any) -> int:
    null_count_fn = getattr(array, "null_count", None)
    if callable(null_count_fn):
        try:
            return int(null_count_fn())
        except TypeError:
            pass
    is_null_fn = getattr(array, "is_null", None)
    if callable(is_null_fn):
        try:
            is_null = is_null_fn()
            sum_fn = getattr(is_null, "sum", None)
            if callable(sum_fn):
                return int(sum_fn())
        except Exception:  # pragma: no cover - best effort
            pass
    return sum(1 for value in _array_iter(array) if value is None)


def _concat_arrays(left: Any, right: Any) -> Any:
    try:  # pragma: no cover - Polars fast path
        import polars as pl

        if isinstance(left, pl.Series) and isinstance(right, pl.Series):
            return pl.concat([left, right], rechunk=False)
    except Exception:
        pass
    return tuple(_array_iter(left)) + tuple(_array_iter(right))


def _materialise_if_requested(array: Any) -> Any:
    if _USE_ARRAY_BACKING:
        return array
    return tuple(_array_iter(array))


def _maybe_legacy_formatter(
    candidate: Callable[..., Any] | None,
) -> Callable[[int], tuple[str, ...]] | None:
    if candidate is None:
        return None
    try:
        signature = inspect.signature(candidate)
    except (TypeError, ValueError):  # pragma: no cover - dynamic callables
        return None
    positional = [
        param
        for param in signature.parameters.values()
        if param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    if len(positional) == 1:
        return cast(Callable[[int], tuple[str, ...]], candidate)
    return None


class DisplayCache:
    """Cache for lazily formatted display strings."""

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: dict[tuple[int, int, int | None], str] = {}

    def get(self, column_key: int, row: int, width: int | None) -> str | None:
        return self._data.get((column_key, row, width))

    def put(self, column_key: int, row: int, width: int | None, value: str) -> None:
        self._data[(column_key, row, width)] = value

    def clear_column(self, column_key: int) -> None:
        to_delete = [key for key in self._data if key[0] == column_key]
        for key in to_delete:
            self._data.pop(key, None)


def _display_width(value: str) -> int:
    width = wcswidth(value)
    if width < 0:
        return len(value)
    return int(width)


def _grapheme_clip(value: str, width: int) -> str:
    if width <= 0:
        return ""
    if _display_width(value) <= width:
        return value
    if width == 1:
        return "…"
    current = 0
    pieces: list[str] = []
    for char in value:
        char_width = wcwidth(char)
        if char_width is None or char_width < 0:
            char_width = 1
        if current + char_width > width - 1:
            break
        pieces.append(char)
        current += char_width
    while pieces and current > width - 1:
        removed = pieces.pop()
        removed_width = wcwidth(removed)
        if removed_width is None or removed_width < 0:
            removed_width = 1
        current -= removed_width
    return "".join(pieces) + "…"


def _format_scalar(value: Any) -> str:
    if value is None:
        return ""
    if _is_float_like(value):
        return _format_float_two_decimals(value)
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:  # pragma: no cover - defensive
            return value.decode("utf-8", errors="ignore")
    return str(value)


class ColumnValuesView(Sequence[Any]):
    __slots__ = ("_slice", "_column_index")

    def __init__(self, table_slice: TableSlice, column_index: int) -> None:
        self._slice = table_slice
        self._column_index = column_index

    def __len__(self) -> int:
        return self._slice.height

    def __getitem__(self, index: int | slice) -> Any:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return tuple(
                self._slice._get_value(self._column_index, idx) for idx in range(start, stop, step)
            )
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)
        return self._slice._get_value(self._column_index, index)

    def __iter__(self) -> Iterator[Any]:
        for idx in range(len(self)):
            yield self._slice._get_value(self._column_index, idx)

    def __eq__(self, other: object) -> bool:  # pragma: no cover - simple helper
        if isinstance(other, Sequence):
            return list(self) == list(other)
        return NotImplemented


class ColumnFormattedView(Sequence[str]):
    __slots__ = ("_slice", "_column_index", "_width")

    def __init__(self, table_slice: TableSlice, column_index: int, width: int) -> None:
        self._slice = table_slice
        self._column_index = column_index
        self._width = width

    def __len__(self) -> int:
        return self._slice.height

    @overload
    def __getitem__(self, index: int) -> str:  # pragma: no cover - signature only
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[str]:  # pragma: no cover - signature only
        ...

    def __getitem__(self, index: int | slice) -> str | Sequence[str]:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return tuple(
                self._slice._get_display(
                    self._column_index, idx, None if self._width == 0 else self._width
                )
                for idx in range(start, stop, step)
            )
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)
        return self._slice._get_display(
            self._column_index, index, None if self._width == 0 else self._width
        )

    def __iter__(self) -> Iterator[str]:
        for idx in range(len(self)):
            yield self._slice._get_display(
                self._column_index, idx, None if self._width == 0 else self._width
            )

    def __eq__(self, other: object) -> bool:  # pragma: no cover - simple helper
        if isinstance(other, Sequence):
            return list(self) == list(other)
        return NotImplemented


@dataclass(slots=True)
class TableColumn:
    """Column-oriented view over a tabular slice."""

    name: str
    data: Any
    dtype: Any
    null_count: int
    _display_fn: Callable[[int, int, Any, int | None], str] | None = field(default=None, repr=False)
    _owner: TableSlice | None = field(default=None, init=False, repr=False)
    _index: int = field(default=-1, init=False, repr=False)
    _values_view: ColumnValuesView | None = field(default=None, init=False, repr=False)
    _local_display_cache: dict[int, tuple[str, ...]] = field(
        default_factory=dict, init=False, repr=False
    )
    _local_values_cache: tuple[Any, ...] | None = field(default=None, init=False, repr=False)
    _legacy_formatter: Callable[[int], tuple[str, ...]] | None = field(
        default=None, init=False, repr=False
    )
    _legacy_display_cache: dict[int, tuple[str, ...]] = field(
        default_factory=dict, init=False, repr=False
    )
    _slice_offset: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        if not _USE_ARRAY_BACKING and not isinstance(self.data, tuple):
            object.__setattr__(self, "data", tuple(_array_iter(self.data)))
        legacy = _maybe_legacy_formatter(self._display_fn)
        if legacy is not None:
            self._legacy_formatter = legacy
            self._display_fn = None

    def _bind(self, owner: TableSlice, index: int) -> None:
        object.__setattr__(self, "_owner", owner)
        object.__setattr__(self, "_index", index)
        object.__setattr__(self, "_values_view", ColumnValuesView(owner, index))

    @property
    def values(self) -> Sequence[Any]:
        owner = self._owner
        if owner is None:
            cached = self._local_values_cache
            if cached is None:
                cached = tuple(_array_get(self.data, idx) for idx in range(len(self)))
                self._local_values_cache = cached
            return cached
        assert self._values_view is not None
        return self._values_view

    def formatted(self, max_chars: int) -> Sequence[str]:
        owner = self._owner
        if owner is None:
            width = max(max_chars, 0)
            if self._legacy_formatter is not None:
                cached = self._legacy_display_cache.get(width)
                if cached is None:
                    cached = self._legacy_formatter(width)
                    self._legacy_display_cache[width] = cached
                start = self._slice_offset
                end = start + len(self)
                return cached[start:end]
            cached = self._local_display_cache.get(width)
            if cached is not None:
                return cached
            base_values = self.values
            rendered = tuple(_format_scalar(value) for value in base_values)
            if width > 0:
                rendered = tuple(_grapheme_clip(text, width) for text in rendered)
            self._local_display_cache[width] = rendered
            return rendered
        safe_width = max(max_chars, 0)
        return ColumnFormattedView(owner, self._index, safe_width)

    def slice(self, start: int, length: int | None = None) -> TableColumn:
        data_slice = _array_slice(self.data, start, length)
        length_val = _array_len(data_slice) if length is None else max(0, length)
        null_count = _array_null_count(data_slice) if length_val else 0
        column = TableColumn(
            self.name,
            _materialise_if_requested(data_slice),
            self.dtype,
            null_count,
            self._display_fn,
        )
        column._legacy_formatter = self._legacy_formatter
        column._legacy_display_cache = self._legacy_display_cache
        column._slice_offset = self._slice_offset + start
        column._local_display_cache = self._local_display_cache
        column._local_values_cache = None
        return column

    def __len__(self) -> int:
        return _array_len(self.data)


@dataclass(slots=True)
class TableSlice:
    """Immutable window of table data returned to presentation layers."""

    columns: tuple[TableColumn, ...]
    schema: Mapping[str, Any]
    start_offset: int | None = None
    row_ids: Any | None = None
    _row_count: int = field(init=False, repr=False)
    _display_cache: DisplayCache = field(default_factory=DisplayCache, init=False, repr=False)
    _value_cache: dict[tuple[int, int], Any] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        columns = tuple(self.columns)
        object.__setattr__(self, "columns", columns)
        schema_proxy = MappingProxyType(dict(self.schema))
        object.__setattr__(self, "schema", schema_proxy)
        for idx, column in enumerate(columns):
            column._bind(self, idx)

        if not columns:
            object.__setattr__(self, "_row_count", 0)
            return

        lengths = {len(column) for column in columns}
        if len(lengths) != 1:
            msg = "All columns must share the same row count"
            raise ValueError(msg)
        (row_count,) = lengths
        object.__setattr__(self, "_row_count", row_count)

    @classmethod
    def empty(
        cls,
        columns: Sequence[str] | None = None,
        schema: Mapping[str, Any] | None = None,
    ) -> TableSlice:
        base_schema = dict(schema or {})
        column_names = tuple(columns or base_schema.keys())
        table_columns: list[TableColumn] = []

        for name in column_names:
            dtype = base_schema.get(name)
            table_columns.append(TableColumn(name, (), dtype, 0))
            if name not in base_schema:
                base_schema[name] = dtype

        return cls(tuple(table_columns), base_schema)

    @property
    def column_names(self) -> tuple[str, ...]:
        return tuple(column.name for column in self.columns)

    @property
    def height(self) -> int:
        return self._row_count

    def __len__(self) -> int:
        return self.height

    def column(self, name: str) -> TableColumn:
        for column in self.columns:
            if column.name == name:
                return column
        msg = f"Unknown column: {name}"
        raise KeyError(msg)

    def column_at(self, index: int) -> TableColumn:
        return self.columns[index]

    def value_at(self, row: int, column_index: int) -> Any:
        return self._get_value(column_index, row)

    def get_cell(self, row: int, column_index: int, *, width: int | None = None) -> str:
        safe_width = None if width is None else max(width, 0)
        return self._get_display(column_index, row, safe_width)

    def iter_rows(self, start: int = 0, stop: int | None = None) -> Iterator[list[str]]:
        end = self.height if stop is None else min(stop, self.height)
        for row in range(start, end):
            yield [self.get_cell(row, col) for col in range(len(self.columns))]

    def slice(self, start: int, length: int | None = None) -> TableSlice:
        if length is None:
            sliced_columns = tuple(column.slice(start, None) for column in self.columns)
        else:
            sliced_columns = tuple(column.slice(start, length) for column in self.columns)
        row_ids = None
        if self.row_ids is not None:
            row_ids = _array_slice(self.row_ids, start, length)
        offset = None if self.start_offset is None else self.start_offset + start
        return TableSlice(sliced_columns, self.schema, start_offset=offset, row_ids=row_ids)

    def view(self, row_start: int, row_len: int) -> TableSlice:
        return self.slice(row_start, row_len)

    def concat_vertical(self, other: TableSlice) -> TableSlice:
        if self.column_names != other.column_names:
            msg = "Table slices must share the same column ordering"
            raise ValueError(msg)
        merged: list[TableColumn] = []
        for left, right in zip(self.columns, other.columns, strict=True):
            combined = _concat_arrays(left.data, right.data)
            null_count = left.null_count + right.null_count
            merged.append(
                TableColumn(
                    left.name,
                    _materialise_if_requested(combined),
                    left.dtype,
                    null_count,
                    left._display_fn,
                )
            )
            merged[-1]._legacy_formatter = left._legacy_formatter
            merged[-1]._legacy_display_cache = left._legacy_display_cache
            merged[-1]._slice_offset = left._slice_offset
        row_ids = None
        if self.row_ids is not None or other.row_ids is not None:
            left_ids = self.row_ids if self.row_ids is not None else ()
            right_ids = other.row_ids if other.row_ids is not None else ()
            row_ids = _concat_arrays(left_ids, right_ids)
        start_offset = self.start_offset
        if start_offset is None and other.start_offset is not None:
            candidate = other.start_offset - len(self)
            if candidate >= 0:
                start_offset = candidate
        return TableSlice(
            tuple(merged),
            self.schema,
            start_offset=start_offset,
            row_ids=row_ids,
        )

    def _absolute_row(self, row: int) -> int:
        if self.start_offset is None:
            return row
        return self.start_offset + row

    def _get_value(self, column_index: int, row: int) -> Any:
        abs_row = self._absolute_row(row)
        column = self.columns[column_index]
        key = (id(column.data), abs_row)
        cached = self._value_cache.get(key)
        if cached is not None:
            return cached
        value = _array_get(column.data, row)
        self._value_cache[key] = value
        return value

    def _get_display(self, column_index: int, row: int, width: int | None) -> str:
        column = self.columns[column_index]
        abs_row = self._absolute_row(row)
        key_width = width
        cached = self._display_cache.get(id(column.data), abs_row, key_width)
        if cached is not None:
            return cached
        raw_value = self._get_value(column_index, row)
        if column._legacy_formatter is not None:
            width_key = max(width or 0, 0)
            formatted = column._legacy_display_cache.get(width_key)
            if formatted is None:
                formatted = column._legacy_formatter(width_key)
                column._legacy_display_cache[width_key] = formatted
            idx = column._slice_offset + row
            text = formatted[idx] if 0 <= idx < len(formatted) else ""
            if width is not None:
                text = _grapheme_clip(text, width)
            self._display_cache.put(id(column.data), abs_row, key_width, text)
            return text
        display_fn = column._display_fn
        if display_fn is not None:
            display_row = row + column._slice_offset
            text = display_fn(display_row, abs_row, raw_value, width)
            if width is not None:
                text = _grapheme_clip(text, width)
        else:
            text = _format_scalar(raw_value)
            if width is not None:
                text = _grapheme_clip(text, width)
        self._display_cache.put(id(column.data), abs_row, key_width, text)
        return text


PhysicalPlanHandle = EnginePayloadHandle[Any]
"""Engine-neutral handle representing a compiled physical plan."""

# Backwards compatibility for legacy imports that still refer to ``PhysicalPlan``.
PhysicalPlan = PhysicalPlanHandle


class EngineAdapter(Protocol):
    """Compile logical plans and validate predicates for a storage engine."""

    def compile(self, plan: Any) -> PhysicalPlan: ...

    def validate_filter(self, clause: str) -> None: ...


class Materializer(Protocol):
    """Collect physical plans into :class:`TableSlice` objects."""

    def collect(self, plan: PhysicalPlan) -> TableSlice: ...

    def collect_slice(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
    ) -> TableSlice: ...

    def collect_slice_stream(
        self,
        plan: PhysicalPlan,
        *,
        start: int = 0,
        length: int | None = None,
        columns: Sequence[str] | None = None,
        batch_rows: int | None = None,
    ) -> Iterator[TableSlice]: ...

    def count(self, plan: PhysicalPlan) -> int | None: ...


__all__ = [
    "EnginePayloadHandle",
    "EngineAdapter",
    "Materializer",
    "PhysicalPlan",
    "PhysicalPlanHandle",
    "TableColumn",
    "TableSlice",
]

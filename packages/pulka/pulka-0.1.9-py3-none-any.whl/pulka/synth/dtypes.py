"""Helpers for parsing and formatting Polars dtypes in synth specs."""

from __future__ import annotations

import ast
from typing import Any

import polars as pl
import polars.datatypes as dt
from polars.datatypes import DataType, DataTypeClass, parse_into_dtype

__all__ = ["DTypeParseError", "format_dtype", "parse_dtype"]


class DTypeParseError(ValueError):
    """Raised when a dtype annotation cannot be parsed."""


def parse_dtype(source: str) -> DataType | DataTypeClass:
    """Parse ``source`` into a Polars :class:`~polars.datatypes.DataType`."""

    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as exc:  # pragma: no cover - surfaced via parser tests
        raise DTypeParseError(f"invalid dtype expression: {exc}") from exc

    evaluator = _DTypeExpressionEvaluator()
    try:
        value = evaluator.evaluate(tree.body)
    except DTypeParseError:
        raise
    except Exception as exc:  # pragma: no cover - defensive re-wrap
        raise DTypeParseError(str(exc)) from exc

    try:
        return parse_into_dtype(value)
    except TypeError as exc:  # pragma: no cover - bubbled through parser tests
        raise DTypeParseError(str(exc)) from exc


def format_dtype(dtype: DataType | DataTypeClass) -> str:
    """Return the canonical textual representation for ``dtype``."""

    parsed = parse_into_dtype(dtype)

    if isinstance(parsed, DataTypeClass):
        name = _SIMPLE_NAMES.get(parsed, parsed.__name__)
        return f"pl.{name}"

    if isinstance(parsed, dt.Decimal):
        return f"pl.Decimal(precision={parsed.precision},scale={parsed.scale})"

    if isinstance(parsed, dt.Datetime):
        args = [f"time_unit='{parsed.time_unit}'"]
        if parsed.time_zone is not None:
            args.append(f"time_zone='{parsed.time_zone}'")
        return f"pl.Datetime({','.join(args)})"

    if isinstance(parsed, dt.Duration):
        return f"pl.Duration(time_unit='{parsed.time_unit}')"

    if isinstance(parsed, dt.List):
        inner = format_dtype(parsed.inner)
        return f"pl.List({inner})"

    if isinstance(parsed, dt.Array):
        inner = format_dtype(parsed.inner)
        return f"pl.Array({inner},{parsed.size})"

    if isinstance(parsed, dt.Struct):
        fields = ",".join(f"'{field.name}':{format_dtype(field.dtype)}" for field in parsed.fields)
        return f"pl.Struct({{{fields}}})"

    if isinstance(parsed, dt.Enum):
        categories = ",".join(repr(value) for value in parsed.categories.to_list())
        return f"pl.Enum([{categories}])"

    raise DTypeParseError(f"unsupported dtype for formatting: {parsed!r}")


_SIMPLE_NAMES: dict[DataTypeClass, str] = {
    pl.Boolean: "Boolean",
    pl.Int8: "Int8",
    pl.Int16: "Int16",
    pl.Int32: "Int32",
    pl.Int64: "Int64",
    pl.UInt8: "UInt8",
    pl.UInt16: "UInt16",
    pl.UInt32: "UInt32",
    pl.UInt64: "UInt64",
    pl.Float32: "Float32",
    pl.Float64: "Float64",
    pl.Decimal: "Decimal",
    pl.Utf8: "Utf8",
    pl.String: "Utf8",
    pl.Binary: "Binary",
    pl.Date: "Date",
    pl.Time: "Time",
    pl.Categorical: "Categorical",
    pl.Enum: "Enum",
    pl.Null: "Null",
}


class _DTypeExpressionEvaluator(ast.NodeVisitor):
    """AST evaluator restricted to Polars dtype constructors."""

    _ALLOWED_CONSTANTS = {"True": True, "False": False, "None": None}

    def evaluate(self, node: ast.AST) -> Any:
        return self.visit(node)

    def visit_Name(self, node: ast.Name) -> Any:  # noqa: N802
        if node.id == "pl":
            return pl
        if node.id in self._ALLOWED_CONSTANTS:
            return self._ALLOWED_CONSTANTS[node.id]
        attr = getattr(pl, node.id, None)
        if isinstance(attr, (DataType, DataTypeClass)):
            return attr
        raise DTypeParseError(f"unknown name '{node.id}' in dtype expression")

    def visit_Attribute(self, node: ast.Attribute) -> Any:  # noqa: N802
        base = self.visit(node.value)
        attr = getattr(base, node.attr, None)
        if isinstance(attr, (DataType, DataTypeClass)):
            return attr
        raise DTypeParseError(f"attribute '{node.attr}' is not a dtype")

    def visit_Call(self, node: ast.Call) -> Any:  # noqa: N802
        func = self.visit(node.func)
        if not isinstance(func, DataTypeClass):
            raise DTypeParseError("dtype calls must target Polars dtype constructors")
        args = [self.visit(arg) for arg in node.args]
        kwargs: dict[str, Any] = {}
        for keyword in node.keywords:
            if keyword.arg is None:
                raise DTypeParseError("**kwargs unpacking is not supported in dtype expressions")
            kwargs[keyword.arg] = self.visit(keyword.value)
        return func(*args, **kwargs)

    def visit_List(self, node: ast.List) -> Any:  # noqa: N802
        return [self.visit(element) for element in node.elts]

    def visit_Tuple(self, node: ast.Tuple) -> Any:  # noqa: N802
        return tuple(self.visit(element) for element in node.elts)

    def visit_Dict(self, node: ast.Dict) -> Any:  # noqa: N802
        result: dict[str, Any] = {}
        for key_node, value_node in zip(node.keys, node.values, strict=True):
            if key_node is None:
                raise DTypeParseError("dict unpacking is not supported in dtype expressions")
            key = self.visit(key_node)
            if not isinstance(key, str):
                raise DTypeParseError("struct field names must be strings")
            result[key] = self.visit(value_node)
        return result

    def visit_Constant(self, node: ast.Constant) -> Any:  # noqa: N802
        if isinstance(node.value, (int, float, str, type(None), bool)):
            return node.value
        raise DTypeParseError(f"unsupported literal {node.value!r} in dtype expression")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:  # noqa: N802
        if isinstance(node.op, ast.USub):
            operand = self.visit(node.operand)
            if isinstance(operand, (int, float)):
                return -operand
        raise DTypeParseError("unsupported unary operation in dtype expression")

    def generic_visit(self, node: ast.AST) -> Any:  # noqa: N802
        raise DTypeParseError(f"unsupported syntax '{node.__class__.__name__}' in dtype expression")

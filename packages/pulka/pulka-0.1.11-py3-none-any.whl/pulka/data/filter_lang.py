"""
Filter language compiler for Pulka.

This module handles the parsing and compilation of filter expressions to Polars
expressions, including AST validation and namespace resolution.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Sequence

import polars as pl

from ..sheets.query_plan import normalized_columns_key


class FilterError(ValueError):
    """Raised when a filter expression cannot be parsed or evaluated."""


class ColumnNamespace:
    """Attribute/Item access helper that maps column names to Polars expressions."""

    def __init__(self, columns: Sequence[str]):
        self._columns = list(columns)
        self._column_set = set(columns)

    def __getattr__(self, name: str) -> pl.Expr:
        if name.startswith("_") or name not in self._column_set or not name.isidentifier():
            raise AttributeError(f"No column named '{name}'")
        return pl.col(name)

    def __getitem__(self, key: str) -> pl.Expr:
        if key not in self._column_set:
            raise KeyError(f"No column named '{key}'")
        return pl.col(key)

    def __dir__(self) -> list[str]:
        return sorted([c for c in self._columns if c.isidentifier()])

    @property
    def columns(self) -> Sequence[str]:
        return tuple(self._columns)


_FILTER_CACHE: dict[tuple[str, str], pl.Expr] = {}


def compile_filter_expression(text: str, columns: Sequence[str]) -> pl.Expr:
    """Return a cached Polars expression for ``text`` and ``columns``."""

    normalized = text.strip()
    key = (normalized, normalized_columns_key(columns))
    expr = _FILTER_CACHE.get(key)
    if expr is None:
        expr = _compile_filter_expression(normalized, columns)
        _FILTER_CACHE[key] = expr
    return expr


def clear_filter_cache() -> None:
    """Clear the cached filter expressions."""

    _FILTER_CACHE.clear()


_INDEX_NODE = getattr(ast, "Index", None)
_ALLOWED_FILTER_NODE_TYPES = (
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Call,
    ast.Attribute,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Subscript,
    ast.Slice,
    ast.keyword,
) + ((_INDEX_NODE,) if _INDEX_NODE is not None else ())


def _detect_precedence_issues(text: str) -> None:
    """Detect common operator precedence issues and provide helpful error messages."""
    # Pattern: comparison == literal & other_expr (without parentheses)
    # This will be parsed as: comparison == (literal & other_expr)
    pattern1 = re.compile(r"\b\w+(?:\.\w+)*\s*==\s*(?:True|False|\w+)\s*&\s*\w+")
    if pattern1.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a == b) & (c op d)"
        )

    # Pattern: comparison == literal | other_expr (without parentheses)
    pattern2 = re.compile(r"\b\w+(?:\.\w+)*\s*==\s*(?:True|False|\w+)\s*\|\s*\w+")
    if pattern2.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a == b) | (c op d)"
        )

    # Pattern: comparison != literal & other_expr (without parentheses)
    pattern3 = re.compile(r"\b\w+(?:\.\w+)*\s*!=\s*(?:True|False|\w+)\s*&\s*\w+")
    if pattern3.search(text):
        raise FilterError(
            f"Operator precedence issue detected in '{text}'. "
            "Use parentheses to clarify: (a != b) & (c op d)"
        )


def _validate_filter_ast(node: ast.AST, allowed_names: set[str]) -> None:
    extra_allowed = (ast.operator, ast.boolop, ast.unaryop, ast.cmpop)
    for child in ast.walk(node):
        if not isinstance(child, _ALLOWED_FILTER_NODE_TYPES + extra_allowed):
            raise FilterError("Unsupported syntax in filter expression")
        if isinstance(child, ast.Attribute):
            if child.attr.startswith("_"):
                raise FilterError("Attribute access starting with '_' is not allowed")
        elif isinstance(child, ast.Name) and child.id not in allowed_names:
            raise FilterError(f"Unknown name '{child.id}' in filter expression")


def _compile_filter_expression(text: str, columns: Sequence[str]) -> pl.Expr:
    namespace = ColumnNamespace(columns)

    # Check for common precedence issues before parsing
    _detect_precedence_issues(text)

    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise FilterError(f"Invalid filter syntax: {exc.msg}") from exc

    _validate_filter_ast(tree, {"c", "pl", "lit", "col", "True", "False", "None"})

    env = {
        "c": namespace,
        "pl": pl,
        "lit": pl.lit,
        "col": pl.col,
        "True": True,
        "False": False,
        "None": None,
    }

    try:
        compiled = eval(compile(tree, "<filter>", "eval"), {"__builtins__": {}}, env)
    except FilterError:
        raise
    except Exception as exc:
        raise FilterError(str(exc)) from exc

    if not isinstance(compiled, pl.Expr):
        raise FilterError("Filter expression must produce a Polars expression")
    return compiled

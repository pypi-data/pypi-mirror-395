"""Expression sandbox used for CLI ``--expr`` support."""

from __future__ import annotations

import ast
from collections.abc import Sequence
from datetime import date, datetime, time
from pathlib import Path

import polars as pl

from ..core.engine.polars_adapter import coerce_physical_plan, unwrap_physical_plan
from ..data.filter_lang import ColumnNamespace


class ExpressionError(ValueError):
    """Raised when a dataset expression cannot be evaluated safely."""


_INDEX_NODE = getattr(ast, "Index", None)
try:  # pragma: no cover - optional selectors module
    from polars import selectors as _polars_selectors
except ImportError:  # pragma: no cover - selectors unavailable
    _polars_selectors = None


_ALLOWED_NODE_TYPES = (
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


def _expression_uses_name(tree: ast.AST, name: str) -> bool:
    return any(isinstance(node, ast.Name) and node.id == name for node in ast.walk(tree))


def _validate_expression_ast(tree: ast.AST, allowed_names: set[str]) -> None:
    extra_allowed = (ast.operator, ast.boolop, ast.unaryop, ast.cmpop)
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODE_TYPES + extra_allowed):
            raise ExpressionError("Unsupported syntax in expression")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise ExpressionError("Attribute access starting with '_' is not allowed")
        if isinstance(node, ast.Name) and node.id not in allowed_names:
            raise ExpressionError(f"Unknown name '{node.id}' in expression")


def _coerce_lazyframe(candidate: object) -> pl.LazyFrame:
    if isinstance(candidate, pl.LazyFrame):
        return candidate
    if isinstance(candidate, pl.DataFrame):
        return candidate.lazy()

    plan_handle = coerce_physical_plan(candidate)
    if plan_handle is not None:
        return unwrap_physical_plan(plan_handle).to_lazyframe()

    raise ExpressionError("Expression must return a Polars LazyFrame or DataFrame")


def _selectors_namespace(columns: Sequence[str] | None) -> object:  # columns kept for parity
    if _polars_selectors is not None:
        return _polars_selectors

    class _SelectorFallback:
        def __init__(self, column_names: Sequence[str] | None):
            self._column_names = list(column_names) if column_names is not None else None

        def _ensure_columns(self) -> list[str]:
            if self._column_names is None:
                raise ExpressionError("Column selectors require a dataset with known columns")
            return self._column_names

        def starts_with(self, prefix: str) -> list[pl.Expr]:
            columns = self._ensure_columns()
            return [pl.col(name) for name in columns if name.startswith(prefix)]

        def ends_with(self, suffix: str) -> list[pl.Expr]:
            columns = self._ensure_columns()
            return [pl.col(name) for name in columns if name.endswith(suffix)]

        def contains(self, substring: str) -> list[pl.Expr]:
            columns = self._ensure_columns()
            return [pl.col(name) for name in columns if substring in name]

        @staticmethod
        def all() -> pl.Expr:
            return pl.all()

        @staticmethod
        def any() -> pl.Expr:
            return pl.all()

    return _SelectorFallback(columns)


def _install_glimpse_method() -> None:
    if hasattr(pl.LazyFrame, "glimpse"):
        return

    def _glimpse(self: pl.LazyFrame, max_rows: int = 6) -> pl.LazyFrame:
        limit = max(1, min(5, int(max_rows)))
        try:
            preview = self.head(limit).collect()
        except Exception as exc:  # pragma: no cover - passthrough
            raise ExpressionError(f"glimpse failed: {exc}") from exc

        preview.glimpse()
        return self

    pl.LazyFrame.glimpse = _glimpse  # type: ignore[attr-defined]


_install_glimpse_method()


def _scan(path: str | Path) -> pl.LazyFrame:
    """Lightweight dispatcher for common scan_* functions."""

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".parquet", ".parq", ".pq"}:
        return pl.scan_parquet(resolved)
    if suffix in {".ipc", ".feather", ".arrow"}:
        return pl.scan_ipc(resolved)
    if suffix in {".ndjson", ".jsonl"}:
        return pl.scan_ndjson(resolved)
    if suffix == ".tsv":
        return pl.scan_csv(resolved, separator="\t")
    if suffix == ".csv":
        return pl.scan_csv(resolved)

    raise ExpressionError(f"Unsupported file extension for scan(): '{suffix or '<none>'}'")


def _dbg(value: object, label: str = "") -> object:
    """Print a short summary for debugging without breaking expression chains."""

    def _fmt_columns(obj: object) -> str | None:
        # Avoid LazyFrame.columns because it emits a PerformanceWarning; use schema names instead.
        if isinstance(obj, pl.LazyFrame):
            try:
                cols = obj.collect_schema().names()
            except Exception:
                return None
        else:
            cols = getattr(obj, "columns", None)
        if cols:
            preview = list(cols)
            return f"cols={preview}"
        return None

    parts: list[str] = [type(value).__name__]
    if hasattr(value, "shape"):
        try:
            rows, cols = value.shape  # type: ignore[assignment]
            parts.append(f"shape={rows}x{cols}")
        except Exception:
            pass

    cols_repr = _fmt_columns(value)
    if cols_repr:
        parts.append(cols_repr)

    prefix = "[dbg" + (f" {label}" if label else "") + "]"
    print(f"{prefix} {' '.join(parts)}")
    return value


def _cfg_rows(rows: int, frame: pl.LazyFrame | pl.DataFrame | None = None) -> pl.LazyFrame | None:
    """Set row display budget and return the provided frame unchanged."""

    pl.Config.set_tbl_rows(rows)
    return frame


def _cfg_cols(cols: int, frame: pl.LazyFrame | pl.DataFrame | None = None) -> pl.LazyFrame | None:
    """Set column display budget and return the provided frame unchanged."""

    pl.Config.set_tbl_cols(cols)
    return frame


def _cfg_fmt_str_lengths(
    length: int, frame: pl.LazyFrame | pl.DataFrame | None = None
) -> pl.LazyFrame | None:
    """Set string truncation budget and return the provided frame unchanged."""

    pl.Config.set_fmt_str_lengths(length)
    return frame


def evaluate_dataset_expression(
    text: str,
    *,
    df: pl.LazyFrame | None = None,
    columns: Sequence[str] | None = None,
) -> pl.LazyFrame:
    """Return a lazily-evaluated frame produced by ``text``."""

    normalized = text.strip()
    if not normalized:
        raise ExpressionError("Expression cannot be empty")

    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(f"Invalid expression syntax: {exc.msg}") from exc

    references_df = _expression_uses_name(tree, "df")
    if references_df and df is None:
        raise ExpressionError("Expression references 'df' but no dataset path was provided")

    column_helper = None
    if columns:
        column_helper = ColumnNamespace(columns)

    allowed_names = {
        "pl",
        "lit",
        "col",
        "when",
        "duration",
        "True",
        "False",
        "None",
        "cs",
        "scan",
        "dbg",
        "cfg_rows",
        "cfg_cols",
        "cfg_fmt_str_lengths",
        "len",
        "min",
        "max",
        "sum",
        "range",
        "Path",
        "datetime",
        "date",
        "time",
    }
    if df is not None:
        allowed_names.add("df")
    if column_helper is not None:
        allowed_names.add("c")

    _validate_expression_ast(tree, allowed_names)

    env: dict[str, object] = {
        "pl": pl,
        "lit": pl.lit,
        "col": pl.col,
        "when": pl.when,
        "duration": pl.duration,
        "True": True,
        "False": False,
        "None": None,
        "cs": _selectors_namespace(columns),
        "scan": _scan,
        "dbg": _dbg,
        "cfg_rows": _cfg_rows,
        "cfg_cols": _cfg_cols,
        "cfg_fmt_str_lengths": _cfg_fmt_str_lengths,
        "len": len,
        "min": min,
        "max": max,
        "sum": sum,
        "range": range,
        "Path": Path,
        "datetime": datetime,
        "date": date,
        "time": time,
    }
    if df is not None:
        env["df"] = df
    if column_helper is not None:
        env["c"] = column_helper

    try:
        value = eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, env)
    except ExpressionError:
        raise
    except Exception as exc:  # pragma: no cover - safety belt
        raise ExpressionError(str(exc)) from exc

    return _coerce_lazyframe(value)


__all__ = ["ExpressionError", "evaluate_dataset_expression"]

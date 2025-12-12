"""Utilities for exporting viewer data to disk."""

from __future__ import annotations

import ast
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import polars as pl
from polars.datatypes import (
    Binary,
    Categorical,
    Datetime,
    Duration,
    Enum,
    Struct,
    Time,
)
from polars.datatypes import (
    List as PolarsList,
)
from polars.datatypes import (
    Object as PolarsObject,
)

from ..core.engine.contracts import EnginePayloadHandle
from ..core.engine.polars_adapter import unwrap_lazyframe_handle
from ..logging.redaction import redact_path

__all__ = ["write_view_to_path"]


@dataclass(frozen=True)
class _ExportSpec:
    """Description of how to serialise a lazy frame to disk."""

    format_name: str
    lazy_method: str | None = None
    frame_method: str | None = None
    default_options: Mapping[str, Any] = field(default_factory=dict)


_NORMALISED_FORMATS: dict[str, _ExportSpec] = {}


def _register_specs() -> None:
    """Populate the export spec registry once at import time."""

    lazyframe = pl.LazyFrame
    dataframe = pl.DataFrame

    def lazy_available(method: str) -> str | None:
        return method if hasattr(lazyframe, method) else None

    def frame_available(method: str) -> str | None:
        return method if hasattr(dataframe, method) else None

    specs: dict[str, _ExportSpec] = {
        "parquet": _ExportSpec(
            "parquet",
            lazy_method=lazy_available("sink_parquet"),
            frame_method=frame_available("write_parquet"),
        ),
        "ipc": _ExportSpec(
            "ipc",
            lazy_method=lazy_available("sink_ipc"),
            frame_method=frame_available("write_ipc"),
        ),
        "csv": _ExportSpec(
            "csv",
            lazy_method=lazy_available("sink_csv"),
            frame_method=frame_available("write_csv"),
        ),
        "tsv": _ExportSpec(
            "tsv",
            lazy_method=lazy_available("sink_csv"),
            frame_method=frame_available("write_csv"),
            default_options={"separator": "\t"},
        ),
        "json": _ExportSpec(
            "json",
            lazy_method=lazy_available("sink_json"),
            frame_method=frame_available("write_json"),
        ),
        "ndjson": _ExportSpec(
            "ndjson",
            lazy_method=lazy_available("sink_ndjson"),
            frame_method=frame_available("write_ndjson"),
        ),
        "avro": _ExportSpec(
            "avro",
            frame_method=frame_available("write_avro"),
        ),
        "excel": _ExportSpec(
            "excel",
            frame_method=frame_available("write_excel"),
        ),
        "delta": _ExportSpec(
            "delta",
            frame_method=frame_available("write_delta"),
        ),
        "orc": _ExportSpec(
            "orc",
            frame_method=frame_available("write_orc"),
        ),
    }

    alias_to_format = {
        "pq": "parquet",
        "feather": "ipc",
        "arrow": "ipc",
        "ipc": "ipc",
        "csv": "csv",
        "txt": "csv",
        "tsv": "tsv",
        "tab": "tsv",
        "json": "json",
        "jsonl": "ndjson",
        "ndjson": "ndjson",
        "avro": "avro",
        "xslx": "excel",
        "xlsx": "excel",
        "xls": "excel",
        "xlsm": "excel",
        "excel": "excel",
        "delta": "delta",
        "orc": "orc",
        "parquet": "parquet",
    }

    for alias, format_name in alias_to_format.items():
        spec = specs.get(format_name)
        if spec is None:
            continue
        if spec.lazy_method is None and spec.frame_method is None:
            # Skip formats unsupported by the current Polars build.
            continue
        _NORMALISED_FORMATS[alias] = spec


_register_specs()


def write_view_to_path(
    viewer_or_sheet: Any,
    path: str | Path,
    *,
    format_hint: str | None = None,
    options: Mapping[str, Any] | Iterable[str] | None = None,
) -> Path:
    """Write the active viewer or sheet contents to ``path``.

    Args:
        viewer_or_sheet: Viewer or sheet exposing a Polars ``LazyFrame``.
        path: Destination path for the export.
        format_hint: Optional override for the export format.
        options: Optional mapping or iterable of ``key=value`` overrides.

    Returns:
        The destination path as a :class:`~pathlib.Path`.

    Raises:
        ValueError: If the sheet cannot provide a LazyFrame, the format is unknown,
            or the underlying Polars write fails.
    """

    destination = Path(path)
    sheet, session = _resolve_sheet_and_session(viewer_or_sheet)
    lazy_frame = _extract_lazyframe(sheet)

    format_key = _normalise_format(destination, format_hint=format_hint)
    spec = _NORMALISED_FORMATS.get(format_key)
    if spec is None:
        msg = f"Unsupported export format '{format_key}'"
        raise ValueError(msg)

    parsed_options = _parse_options(options)
    call_options = {**spec.default_options, **parsed_options}

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        _write_lazyframe(lazy_frame, destination, spec, call_options)
    except Exception as exc:  # pragma: no cover - wrapped for user context
        msg = f"Failed to export data as '{spec.format_name}': {exc}"
        raise ValueError(msg) from exc

    _record_export_event(session, sheet, destination, spec.format_name, call_options)
    return destination


def _normalise_format(path: Path, *, format_hint: str | None = None) -> str:
    if format_hint:
        key = format_hint.lower().lstrip(".")
        return key
    suffix = path.suffix
    if not suffix:
        msg = "Destination path must include a file extension when format_hint is omitted"
        raise ValueError(msg)
    return suffix.lower().lstrip(".")


def _parse_options(
    options: Mapping[str, Any] | Iterable[str] | None,
) -> dict[str, Any]:
    if options is None:
        return {}
    if isinstance(options, Mapping):
        return {str(key): value for key, value in options.items()}
    if isinstance(options, Iterable):
        parsed: dict[str, Any] = {}
        for option in options:
            if not isinstance(option, str):
                msg = "Options iterable must contain strings of the form key=value"
                raise ValueError(msg)
            if "=" not in option:
                msg = f"Invalid option '{option}', expected key=value"
                raise ValueError(msg)
            key, value = option.split("=", 1)
            key = key.strip()
            if not key:
                msg = f"Invalid option '{option}', key cannot be empty"
                raise ValueError(msg)
            stripped = value.strip()
            parsed_value = stripped if stripped else value
            parsed[key] = _coerce_option_value(parsed_value)
        return parsed
    msg = "Options must be a mapping or iterable of key=value strings"
    raise TypeError(msg)


def _coerce_option_value(value: str) -> Any:
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "none":
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    for caster in (int, float):
        try:
            return caster(value)
        except ValueError:
            continue
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return bytes(value, "utf-8").decode("unicode_escape")


def _resolve_sheet_and_session(candidate: Any) -> tuple[Any, Any | None]:
    if hasattr(candidate, "sheet"):
        viewer = candidate
        sheet = viewer.sheet
        session = getattr(viewer, "session", None)
        return sheet, session
    sheet = candidate
    viewer = getattr(sheet, "viewer", None)
    session = None
    if viewer is not None:
        session = getattr(viewer, "session", None)
    if session is None:
        session = getattr(sheet, "session", None)
    return sheet, session


def _extract_lazyframe(sheet: Any) -> pl.LazyFrame:
    for attr in ("lf", "lf0", "lazyframe", "lazy_frame"):
        if not hasattr(sheet, attr):
            continue
        candidate = getattr(sheet, attr)
        lazy = _unwrap_lazyframe_candidate(candidate)
        if lazy is not None:
            return lazy
    to_lazyframe = getattr(sheet, "to_lazyframe", None)
    if callable(to_lazyframe):
        candidate = to_lazyframe()
        lazy = _unwrap_lazyframe_candidate(candidate)
        if lazy is not None:
            return lazy
    available_attrs = ", ".join(
        attr for attr in ("lf", "lf0", "lazyframe", "lazy_frame") if hasattr(sheet, attr)
    )
    msg = f"Sheet does not expose a Polars LazyFrame (checked attributes: {available_attrs})"
    raise ValueError(msg)


def _unwrap_lazyframe_candidate(candidate: Any) -> pl.LazyFrame | None:
    if isinstance(candidate, EnginePayloadHandle):
        return unwrap_lazyframe_handle(candidate)
    if isinstance(candidate, pl.LazyFrame):
        return candidate
    return None


def _write_lazyframe(
    lazy_frame: pl.LazyFrame,
    destination: Path,
    spec: _ExportSpec,
    options: Mapping[str, Any],
) -> None:
    if spec.lazy_method is not None and hasattr(lazy_frame, spec.lazy_method):
        sink = getattr(lazy_frame, spec.lazy_method)
        sink(destination, **options)
        return
    if spec.frame_method is not None and hasattr(pl.DataFrame, spec.frame_method):
        df = lazy_frame.collect()
        df = _prepare_frame_for_format(df, spec)
        writer = getattr(df, spec.frame_method)
        writer(destination, **options)
        return
    msg = f"Polars build does not provide an export routine for '{spec.format_name}'"
    raise ValueError(msg)


def _record_export_event(
    session: Any | None,
    sheet: Any,
    destination: Path,
    format_name: str,
    options: Mapping[str, Any],
) -> None:
    recorder = getattr(session, "recorder", None) if session is not None else None
    if recorder is None or not getattr(recorder, "enabled", False):
        return
    payload: dict[str, Any] = {
        "path": redact_path(str(destination)),
        "_raw_path": str(destination),
        "format": format_name,
    }
    sheet_id = getattr(sheet, "sheet_id", None)
    if sheet_id is not None:
        payload["sheet_id"] = sheet_id
    if options:
        payload["options"] = {key: _stringify_option_value(value) for key, value in options.items()}
    recorder.record("export", payload)


def _stringify_option_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _prepare_frame_for_format(df: pl.DataFrame, spec: _ExportSpec) -> pl.DataFrame:
    if spec.format_name != "excel":
        return df

    updates = []
    for name, dtype in df.schema.items():
        base_type = dtype.base_type() if hasattr(dtype, "base_type") else dtype

        if base_type == Datetime and getattr(dtype, "time_zone", None) is not None:
            updates.append(pl.col(name).dt.replace_time_zone(None).alias(name))
            continue
        if base_type == Binary:
            updates.append(pl.col(name).bin.encode("hex").alias(name))
            continue
        if base_type in {Categorical, Enum}:
            updates.append(pl.col(name).cast(pl.Utf8).alias(name))
            continue
        if base_type == PolarsList:
            updates.append(
                pl.col(name).map_elements(_stringify_nested_value, return_dtype=pl.Utf8).alias(name)
            )
            continue
        if base_type == Struct:
            updates.append(
                pl.col(name).map_elements(_stringify_nested_value, return_dtype=pl.Utf8).alias(name)
            )
            continue
        if base_type == Duration:
            updates.append(pl.col(name).dt.to_string().alias(name))
            continue
        if base_type == Time:
            updates.append(pl.col(name).cast(pl.Utf8).alias(name))
            continue
        if base_type == PolarsObject:
            updates.append(
                pl.col(name).map_elements(_stringify_object_value, return_dtype=pl.Utf8).alias(name)
            )

    if not updates:
        return df

    # Excel stores datetime cells without timezone metadata and has limited
    # native support for binary, nested, or Python object columns. Coerce the
    # problematic columns to timezone-naive or string values ahead of the export
    # to avoid runtime failures.
    return df.with_columns(updates)


def _stringify_nested_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, pl.Series):
        return repr(value.to_list())
    return repr(value)


def _stringify_object_value(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)

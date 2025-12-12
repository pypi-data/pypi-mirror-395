"""
Dataset scanning utilities for Pulka.

This module provides functions for opening and scanning various file formats
(CSV/TSV, Parquet, Arrow/Feather/IPCs) using Polars with appropriate overrides.
"""

import contextlib
import csv
import os
import weakref
from pathlib import Path
from tempfile import SpooledTemporaryFile

import polars as pl
import zstandard

from ..utils import _get_int_env

# Configuration for CSV schema inference
CSV_INFER_ROWS = _get_int_env("PULKA_CSV_INFER_ROWS", "PD_CSV_INFER_ROWS", 20000)

_JSONL_EXTENSIONS = (".jsonl", ".ndjson")
_JSONL_ZST_EXTENSIONS = tuple(ext + ".zst" for ext in _JSONL_EXTENSIONS)
_ZSTD_CHUNK_SIZE = 1 << 20  # 1 MiB
_SPOOLED_MAX_SIZE = 8 << 20  # Spill to disk beyond 8 MiB
_BROWSER_STRICT_ENV = os.getenv("PULKA_BROWSER_STRICT_EXTENSIONS")
if _BROWSER_STRICT_ENV is None:
    _BROWSER_STRICT_EXTENSIONS = True
else:
    _BROWSER_STRICT_EXTENSIONS = _BROWSER_STRICT_ENV.strip().lower() in {"1", "true", "yes", "on"}


def _csv_schema_overrides(path: str, separator: str) -> dict[str, pl.DataType]:
    """Detect and return schema overrides for CSV files based on header patterns."""
    try:
        with Path(path).open(newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter=separator)
            header = next(reader)
    except (OSError, StopIteration):
        return {}

    overrides: dict[str, pl.DataType] = {}
    for name in header:
        key = name.strip().strip('"')
        lower = key.lower()
        if lower.endswith("id") or lower.endswith("_id") or lower.endswith("id_"):
            overrides[key] = pl.Utf8
    return overrides


def _tag_lazy_frame(lazy_frame: pl.LazyFrame, *, kind: str, path: str | Path) -> pl.LazyFrame:
    """Attach Pulka-specific metadata to ``lazy_frame`` and return it."""

    lazy_frame._pulka_source_kind = kind  # type: ignore[attr-defined]
    lazy_frame._pulka_path = str(path)  # type: ignore[attr-defined]
    return lazy_frame


def detect_scan_kind(path: str) -> str | None:
    """Return the dataset kind inferred from ``path`` based on its extension."""
    lower = path.lower()
    if lower.endswith(".csv"):
        return "csv"
    if lower.endswith(".tsv"):
        return "tsv"
    if lower.endswith(".parquet"):
        return "parquet"
    if lower.endswith((".feather", ".ipc", ".arrow")):
        return "ipc"
    if lower.endswith(_JSONL_ZST_EXTENSIONS):
        return "jsonl-zst"
    if lower.endswith(_JSONL_EXTENSIONS):
        return "jsonl"
    return None


def is_supported_path(path: str) -> bool:
    """Return whether ``path`` looks like a supported dataset."""

    if detect_scan_kind(path) is not None:
        return True
    return not _BROWSER_STRICT_EXTENSIONS


def scan_any(path: str) -> pl.LazyFrame:
    """Scan any supported file format and return a Polars LazyFrame."""
    kind = detect_scan_kind(path)
    if kind in {"csv", "tsv"}:
        sep = "\t" if kind == "tsv" else ","
        overrides = _csv_schema_overrides(path, sep)
        lf = pl.scan_csv(
            path,
            separator=sep,
            infer_schema_length=CSV_INFER_ROWS,
            schema_overrides=overrides if overrides else None,
        )
        return _tag_lazy_frame(lf, kind=kind, path=path)
    if kind == "parquet":
        return _tag_lazy_frame(pl.scan_parquet(path), kind="parquet", path=path)
    if kind == "ipc":
        return _tag_lazy_frame(pl.scan_ipc(path), kind="ipc", path=path)
    if kind == "jsonl-zst":
        return _scan_jsonl_zst(path)
    if kind == "jsonl":
        return _tag_lazy_frame(pl.scan_ndjson(path), kind="jsonl", path=path)
    # Fallback: try CSV for unknown extensions
    overrides = _csv_schema_overrides(path, ",")
    lf = pl.scan_csv(
        path,
        separator=",",
        infer_schema_length=CSV_INFER_ROWS,
        schema_overrides=overrides if overrides else None,
    )
    return _tag_lazy_frame(lf, kind="csv", path=path)


def _scan_jsonl_zst(path: str) -> pl.LazyFrame:
    """Scan a Zstandard-compressed JSONL/NDJSON file lazily."""
    buffer = SpooledTemporaryFile(mode="w+b", max_size=_SPOOLED_MAX_SIZE)  # noqa: SIM115
    decompressor = zstandard.ZstdDecompressor()
    try:
        with Path(path).open("rb") as source, decompressor.stream_reader(source) as reader:
            while True:
                chunk = reader.read(_ZSTD_CHUNK_SIZE)
                if not chunk:
                    break
                buffer.write(chunk)
        buffer.seek(0)
        lazy_frame = pl.scan_ndjson(buffer)
        _tag_lazy_frame(lazy_frame, kind="jsonl", path=path)
    except Exception:
        buffer.close()
        raise

    def _close_buffer(file_obj: SpooledTemporaryFile) -> None:
        with contextlib.suppress(OSError):
            file_obj.close()

    # Keep a reference to the buffer so it stays alive for the duration of the LazyFrame.
    lazy_frame._pulka_jsonl_source = buffer
    lazy_frame._pulka_jsonl_source_finalizer = weakref.finalize(lazy_frame, _close_buffer, buffer)
    return lazy_frame

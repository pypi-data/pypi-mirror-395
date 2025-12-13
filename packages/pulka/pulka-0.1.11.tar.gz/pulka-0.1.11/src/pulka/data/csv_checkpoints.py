"""Utilities for building newline checkpoints over CSV-like sources."""

from __future__ import annotations

import logging
from pathlib import Path

from .sidecar import SidecarStore

LOGGER = logging.getLogger(__name__)

CHECKPOINT_EVERY_ROWS = 10_000
CHECKPOINT_ARTIFACT = "checkpoints"
_READ_CHUNK_SIZE = 1 << 20  # 1 MiB


def build_csv_checkpoints(
    path: str | Path,
    *,
    store: SidecarStore | None = None,
    every_n: int = CHECKPOINT_EVERY_ROWS,
) -> tuple[int, ...]:
    """Scan ``path`` once and persist newline checkpoints."""

    target = Path(path)
    if every_n <= 0:
        raise ValueError("checkpoint interval must be positive")

    artefact_store = store or SidecarStore(str(target))

    offsets = _collect_newline_offsets(target, every_n=every_n)
    artefact_store.write_offsets(CHECKPOINT_ARTIFACT, offsets)
    LOGGER.debug(
        "csv_checkpoints.write",
        extra={
            "event": "csv_checkpoints_write",
            "path": str(target),
            "rows_per_checkpoint": every_n,
            "offsets": len(offsets),
        },
    )
    return tuple(offsets)


def _collect_newline_offsets(path: Path, *, every_n: int) -> list[int]:
    """Return byte offsets for every ``every_n``-th data row."""

    offsets: list[int] = [0]
    row_index = -1  # Start at -1 so the first newline records row 0.
    leftover = b""

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(_READ_CHUNK_SIZE)
            if not chunk:
                if not leftover:
                    break
                data = leftover
                base = handle.tell() - len(data)
                leftover = b""
            else:
                data = leftover + chunk
                base = handle.tell() - len(chunk) - len(leftover)
                leftover = b""

            cursor = 0
            data_len = len(data)
            while True:
                newline_idx = data.find(b"\n", cursor)
                if newline_idx == -1:
                    break
                row_index += 1
                row_start = base + newline_idx + 1
                if row_index >= 0 and row_index % every_n == 0:
                    offsets.append(row_start)
                cursor = newline_idx + 1

            if cursor < data_len:
                leftover = data[cursor:]
            if not chunk:
                break

    return offsets


__all__ = ["CHECKPOINT_ARTIFACT", "CHECKPOINT_EVERY_ROWS", "build_csv_checkpoints"]

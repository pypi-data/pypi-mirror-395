"""Sidecar storage helpers for lightweight dataset indexes."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Sequence
from pathlib import Path


def _default_cache_dir() -> Path:
    """Return the root directory for cached sidecar artefacts."""

    override = os.environ.get("PULKA_CACHE_DIR")
    if override:
        return Path(override).expanduser()

    return Path("~/.pulka_cache").expanduser()


class SidecarStore:
    """Persist per-dataset sidecar artefacts under a deterministic path."""

    __slots__ = ("key", "dir")

    def __init__(self, uri: str, *, base: str | os.PathLike[str] | None = None) -> None:
        cache_root = Path(base) if base is not None else _default_cache_dir()
        self.key = hashlib.sha1(uri.encode("utf-8")).hexdigest()[:16]
        self.dir = cache_root.expanduser() / self.key
        self.dir.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        """Return the filesystem path for ``name`` within the store."""

        safe = name.strip().replace(os.sep, "_")
        return self.dir / f"{safe}.bin"

    def has(self, name: str) -> bool:
        """Return ``True`` when an artefact named ``name`` exists."""

        return self.path(name).exists()

    def write_offsets(self, name: str, offsets: Sequence[int]) -> None:
        """Persist ``offsets`` as little-endian unsigned 64-bit integers."""

        target = self.path(name)
        tmp_path = target.with_suffix(".tmp")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)

        with tmp_path.open("wb") as buffer:
            for offset in offsets:
                buffer.write(int(offset).to_bytes(8, "little", signed=False))

        tmp_path.replace(target)

    def read_offsets(self, name: str) -> tuple[int, ...]:
        """Load offsets previously stored via :meth:`write_offsets`."""

        path = self.path(name)
        data = path.read_bytes()
        if len(data) % 8 != 0:
            raise ValueError("sidecar offsets payload must be aligned to 8 bytes")
        return tuple(
            int.from_bytes(data[index : index + 8], "little", signed=False)
            for index in range(0, len(data), 8)
        )


__all__ = ["SidecarStore"]

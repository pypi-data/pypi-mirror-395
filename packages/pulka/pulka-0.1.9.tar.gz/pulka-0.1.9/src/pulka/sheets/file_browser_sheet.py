from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Literal

from ..core.engine.contracts import TableColumn, TableSlice
from ..core.plan import QueryPlan
from ..core.sheet import (
    SHEET_FEATURE_PREVIEW,
    SHEET_FEATURE_ROW_COUNT,
    SHEET_FEATURE_SLICE,
    SHEET_FEATURE_VALUE_AT,
    SheetFeature,
)
from ..data.scanners import ScannerRegistry


@dataclass(slots=True, frozen=True)
class FileBrowserAction:
    type: Literal["enter-directory", "open-file"]
    path: Path


@dataclass(slots=True)
class _FileBrowserEntry:
    row: dict[str, Any]
    path: Path
    is_dir: bool
    openable: bool


@dataclass(slots=True)
class _FileBrowserSnapshot:
    entries: list[_FileBrowserEntry]
    rows: list[dict[str, Any]]
    signature: tuple[tuple[str, str, str, str, bool], ...]
    error: str | None


class FileBrowserSheet:
    """Sheet that lists openable datasets and directories within a folder."""

    _COLUMNS: ClassVar[tuple[str, ...]] = ("name", "type", "size", "modified")
    _CAPABILITIES: ClassVar[frozenset[SheetFeature]] = frozenset(
        {
            SHEET_FEATURE_PREVIEW,
            SHEET_FEATURE_SLICE,
            SHEET_FEATURE_VALUE_AT,
            SHEET_FEATURE_ROW_COUNT,
        }
    )

    def __init__(self, directory: Path, *, scanners: ScannerRegistry):
        self.is_file_browser = True
        self._scanners = scanners
        self._plan = QueryPlan()
        self.sheet_id = f"file-browser:{directory}"
        self.directory = self._normalise_path(directory)
        self._schema = {
            "name": str,
            "type": str,
            "size": str,
            "modified": str,
        }
        self._entries: list[_FileBrowserEntry] = []
        self._rows: list[dict[str, Any]] = []
        self._error: str | None = None
        self._entries_signature: tuple[tuple[str, str, str, str, bool], ...] | None = None
        snapshot = self._capture_directory_snapshot()
        self._apply_snapshot(snapshot)

    @staticmethod
    def _normalise_path(path: Path) -> Path:
        candidate = Path(path).expanduser()
        try:
            return candidate.resolve()
        except OSError:
            return candidate.absolute()

    @property
    def columns(self) -> list[str]:
        return list(self._COLUMNS)

    @property
    def display_path(self) -> str:
        return str(self.directory)

    @property
    def status_message(self) -> str | None:
        return self._error

    def schema_dict(self) -> dict[str, Any]:
        return dict(self._schema)

    def plan_snapshot(self) -> dict[str, object]:
        return {"kind": "file-browser", "path": str(self.directory)}

    @property
    def plan(self) -> QueryPlan:
        return self._plan

    def with_plan(self, plan: QueryPlan) -> FileBrowserSheet:
        del plan
        return self

    def _capture_directory_snapshot(self) -> _FileBrowserSnapshot:
        entries: list[_FileBrowserEntry] = []
        rows: list[dict[str, Any]] = []
        fingerprint: list[tuple[str, str, str, str, bool]] = []
        error: str | None = None

        parent = self.directory.parent
        if parent != self.directory:
            entry = self._build_entry(
                name="..",
                path=parent,
                is_dir=True,
                openable=True,
                size_display="",
                modified_display="",
            )
            entries.append(entry)
            rows.append(entry.row)
            fingerprint.append(self._entry_signature(entry))

        try:
            children = sorted(
                self.directory.iterdir(),
                key=lambda path: (not path.is_dir(), path.name.lower()),
            )
        except OSError as exc:
            error = f"dir error: {exc}"
            return _FileBrowserSnapshot(entries, rows, tuple(fingerprint), error)

        dirs: list[_FileBrowserEntry] = []
        files: list[_FileBrowserEntry] = []
        for child in children:
            is_dir = child.is_dir()
            is_openable = self._scanners.can_scan(child)
            if is_dir:
                entry = self._format_entry(child, is_dir=True, openable=True)
                dirs.append(entry)
                continue
            if not child.is_file():
                continue
            if not is_openable:
                continue
            entry = self._format_entry(child, is_dir=False, openable=True)
            files.append(entry)

        for entry in (*dirs, *files):
            entries.append(entry)
            rows.append(entry.row)
            fingerprint.append(self._entry_signature(entry))

        return _FileBrowserSnapshot(entries, rows, tuple(fingerprint), error)

    def _apply_snapshot(self, snapshot: _FileBrowserSnapshot) -> None:
        self._entries = snapshot.entries
        self._rows = snapshot.rows
        self._entries_signature = snapshot.signature
        self._error = snapshot.error

    def refresh_from_disk(self) -> bool:
        snapshot = self._capture_directory_snapshot()
        signature_changed = snapshot.signature != self._entries_signature
        error_changed = snapshot.error != self._error
        if not signature_changed and not error_changed:
            return False
        self._apply_snapshot(snapshot)
        return True

    def _format_entry(self, path: Path, *, is_dir: bool, openable: bool) -> _FileBrowserEntry:
        try:
            stat_result = path.stat()
        except OSError:
            stat_result = None
        size_display = "" if is_dir else self._format_size(stat_result)
        modified_display = self._format_modified(stat_result)
        name = f"{path.name}/" if is_dir else path.name
        return self._build_entry(
            name=name or path.as_posix(),
            path=path,
            is_dir=is_dir,
            openable=openable,
            size_display=size_display,
            modified_display=modified_display,
        )

    @staticmethod
    def _build_entry(
        *,
        name: str,
        path: Path,
        is_dir: bool,
        openable: bool,
        size_display: str,
        modified_display: str,
    ) -> _FileBrowserEntry:
        row = {
            "name": name,
            "type": "dir" if is_dir else "file",
            "size": size_display,
            "modified": modified_display,
        }
        return _FileBrowserEntry(row=row, path=path, is_dir=is_dir, openable=openable)

    @staticmethod
    def _entry_signature(entry: _FileBrowserEntry) -> tuple[str, str, str, str, bool]:
        row = entry.row
        return (
            str(row.get("name", "")),
            str(row.get("type", "")),
            str(row.get("size", "")),
            str(row.get("modified", "")),
            bool(entry.openable),
        )

    @staticmethod
    def _format_size(stat_result: Any | None) -> str:
        if stat_result is None:
            return "?"
        size = getattr(stat_result, "st_size", None)
        if not isinstance(size, int) or size < 0:
            return "?"
        units = ("B", "KB", "MB", "GB", "TB")
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:.0f}{unit}" if unit == "B" else f"{value:.1f}{unit}"
            value /= 1024
        return f"{size}B"

    @staticmethod
    def _format_modified(stat_result: Any | None) -> str:
        timestamp = getattr(stat_result, "st_mtime", None)
        if not isinstance(timestamp, (int, float)):
            return ""
        try:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        except (OverflowError, OSError, ValueError):
            return ""

    def fetch_slice(
        self,
        row_start: int,
        row_count: int,
        columns: Sequence[str],
    ) -> TableSlice:
        if row_count <= 0:
            return TableSlice.empty(columns=columns or self.columns, schema=self._schema)

        start = max(row_start, 0)
        end = min(start + row_count, len(self._rows))
        if start >= end:
            return TableSlice.empty(columns=columns or self.columns, schema=self._schema)

        requested = list(columns or self.columns)
        column_data: dict[str, list[Any]] = {name: [] for name in requested}
        for row in self._rows[start:end]:
            for name in requested:
                column_data[name].append(row.get(name, ""))

        table_columns = tuple(
            TableColumn(name, tuple(values), self._schema.get(name), 0)
            for name, values in column_data.items()
        )
        return TableSlice(table_columns, self._schema)

    def preview(self, rows: int, cols: Sequence[str] | None = None) -> TableSlice:
        return self.fetch_slice(0, rows, cols or self.columns)

    def value_at(self, row: int, col: str) -> Any:
        entry = self._entry_at(row)
        if entry is None:
            return None
        return entry.row.get(col)

    def row_count(self) -> int | None:
        return len(self._rows)

    def supports(self, feature: SheetFeature, /) -> bool:
        return feature in self._CAPABILITIES

    def __len__(self) -> int:
        return len(self._rows)

    def action_for_row(self, row: int) -> FileBrowserAction | None:
        entry = self._entry_at(row)
        if entry is None:
            return None
        if entry.is_dir:
            return FileBrowserAction(type="enter-directory", path=entry.path)
        if entry.openable:
            return FileBrowserAction(type="open-file", path=entry.path)
        return None

    def at_path(self, directory: Path) -> FileBrowserSheet:
        return FileBrowserSheet(directory, scanners=self._scanners)

    def _entry_at(self, row: int) -> _FileBrowserEntry | None:
        if row < 0 or row >= len(self._entries):
            return None
        return self._entries[row]


def file_browser_status_text(sheet: FileBrowserSheet) -> str:
    message = getattr(sheet, "status_message", None)
    if message:
        return message
    count = sheet.row_count() or 0
    return f"{count} entries"


__all__ = ["FileBrowserAction", "FileBrowserSheet", "file_browser_status_text"]

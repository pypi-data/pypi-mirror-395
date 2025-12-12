"""Structured flight recorder for Pulka sessions."""

from __future__ import annotations

import json
import os
import platform
import socket
import subprocess
from collections import deque
from collections.abc import Generator, Iterable
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from time import monotonic_ns
from typing import Any, Literal

from .redaction import RedactionPolicy, redact_path, redact_paths, redaction_policy_from_name

try:  # pragma: no cover - dependency may be absent in minimal envs
    import importlib.metadata as importlib_metadata
except Exception:  # pragma: no cover - fallback for very old Pythons
    import importlib_metadata  # type: ignore

try:  # pragma: no cover - optional compression
    import zstandard as zstd
except Exception:  # pragma: no cover - graceful degrade if zstd missing
    zstd = None

MAX_DEFAULT_BUFFER = 1_000
DEFAULT_OUTPUT_DIR = Path.home() / ".pulka" / "sessions"


def _default_session_id() -> str:
    ts = datetime.now(UTC).isoformat().replace(":", "-")
    return f"{ts}".replace("+00:00", "Z")


def _json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    return str(obj)


@dataclass(slots=True)
class RecorderConfig:
    """Configuration for the flight recorder."""

    enabled: bool = False
    buffer_size: int = MAX_DEFAULT_BUFFER
    output_dir: Path = field(default_factory=lambda: DEFAULT_OUTPUT_DIR)
    compression: Literal["zst", "none"] = "zst"
    compression_level: int = 5
    session_id: str | None = None
    auto_flush_on_exit: bool = True
    cell_redaction: Literal["none", "hash_strings", "mask_patterns"] = "hash_strings"

    def __post_init__(self) -> None:
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
        if self.buffer_size <= 0:
            raise ValueError("buffer_size must be positive")
        if self.compression == "zst" and zstd is None:
            # Silent downgrade if zstd not present
            self.compression = "none"
        if self.cell_redaction not in ("none", "hash_strings", "mask_patterns"):
            msg = (
                f"cell_redaction must be one of 'none', 'hash_strings', 'mask_patterns', "
                f"got '{self.cell_redaction}'"
            )
            raise ValueError(msg)


@dataclass(slots=True)
class RecorderEvent:
    """A structured recorder event."""

    type: str
    payload: dict[str, Any]
    timestamp_ms: int
    monotonic_ns: int
    step_index: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "payload": self.payload,
            "timestamp_ms": self.timestamp_ms,
            "monotonic_ns": self.monotonic_ns,
            "step_index": self.step_index,
        }


class Recorder:
    """Collects structured runtime events and persists them as JSONL."""

    def __init__(self, config: RecorderConfig | None = None):
        self.config = config or RecorderConfig()
        self._enabled = self.config.enabled
        self._buffer: deque[RecorderEvent] = deque(maxlen=self.config.buffer_size)
        self._start_ns = monotonic_ns()
        self._event_counter = 0
        self._session_id = self.config.session_id or _default_session_id()
        self._session_started_at = datetime.now(UTC)
        self._output_path: Path | None = None
        self._env_recorded = False
        # Instantiate the active redaction policy
        self._cell_redaction_policy = redaction_policy_from_name(self.config.cell_redaction)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------
    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    @property
    def cell_redaction_policy(self) -> RedactionPolicy:
        """Expose the active cell redaction policy."""

        return self._cell_redaction_policy

    def record(self, event_type: str, payload: dict[str, Any] | None = None) -> None:
        if not self._enabled:
            return
        payload = payload or {}
        # Automatically redact path values in the payload (shallow processing only)
        # Note: limitation - won't recursively check nested structures beyond top-level
        processed_payload = redact_paths(payload)
        # Apply cell redaction policy after path redaction but before buffering
        processed_payload = self._apply_cell_redaction(processed_payload, event_type=event_type)
        now_ns = monotonic_ns()
        event = RecorderEvent(
            type=event_type,
            payload=processed_payload,
            timestamp_ms=(now_ns - self._start_ns) // 1_000_000,
            monotonic_ns=now_ns,
            step_index=self._event_counter,
        )
        self._event_counter += 1
        self._buffer.append(event)

    def record_perf(
        self,
        *,
        phase: str,
        duration_ms: float,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Record a performance timing event when recording is enabled."""
        if not self._enabled:
            return
        data = {"phase": phase, "duration_ms": duration_ms}
        if payload:
            data.update(payload)
        self.record("perf", data)

    def _apply_cell_redaction(self, payload: dict[str, Any], *, event_type: str) -> dict[str, Any]:
        """Apply cell redaction policy to a payload dictionary.

        Args:
            payload: Dictionary to process

        Returns:
            New dictionary with cell values redacted where appropriate

        Note:
            Avoids redacting core recorder/system fields to maintain event integrity.
            Preserves system fields but redacts nested user data within them.
        """
        from .redaction import _looks_redacted

        # Work on a shallow copy so the caller's dict isn't mutated in place
        result: dict[str, Any] = {}
        for key, value in payload.items():
            if isinstance(key, str) and key.startswith("_"):
                # Private fields (e.g. _raw_path) preserve their original value
                result[key] = value
                continue

            if _looks_redacted(value):
                result[key] = value
                continue

            if key == "schema":
                # Schema strings must remain readable for downstream tooling
                result[key] = value
                continue

            # Core system fields whose values should NOT be redacted (but nested content may be)
            system_fields = {
                "type",
                "timestamp_ms",
                "monotonic_ns",
                "step_index",
                "phase",
                "duration_ms",
                "ok",
                "error",
                "hash",
                "lazy",
            }

            if key in system_fields:
                # Don't redact the system field itself, but process nested content
                if isinstance(value, (list, tuple)):
                    result[key] = [self._apply_redaction_to_value(item) for item in value]
                elif isinstance(value, dict):
                    # Process each value in system dict (but keep dict structure)
                    processed_dict = {}
                    for k, v in value.items():
                        if isinstance(k, str) and k.startswith("_"):
                            processed_dict[k] = v  # Preserve private keys in nested dicts
                        elif _looks_redacted(v):
                            processed_dict[k] = v
                        else:
                            processed_dict[k] = self._apply_redaction_to_value(v)
                    result[key] = processed_dict
                else:
                    # For primitive system field values, preserve as-is
                    result[key] = value
            elif key == "text" and event_type == "status":
                # Special case: 'text' field in status events is system-provided content
                result[key] = value
            elif key == "text" and event_type == "frame":
                # Special case: 'text' field in frame events is the rendered table content
                result[key] = value
            elif (
                key == "path"
            ):  # already handled by path redaction, skip to avoid double processing
                result[key] = value
            else:
                # For all other fields (user data), apply full redaction policy
                result[key] = self._apply_redaction_to_value(value)

        return result

    def _apply_redaction_to_value(self, value: Any) -> Any:
        """Apply redaction policy to a value, handling nested structures."""
        from .redaction import _looks_redacted

        # Skip if already redacted
        if _looks_redacted(value):
            return value

        if isinstance(value, str):
            # Apply policy to string values
            return self._cell_redaction_policy.apply_to_value(value)
        elif isinstance(value, (list, tuple)):
            # Map policy over each element in lists/tuples
            return [self._apply_redaction_to_value(item) for item in value]
        elif isinstance(value, dict):
            # Only touch top-level string values in dicts (no deep recursion beyond one level)
            result = {}
            for k, v in value.items():
                if isinstance(k, str) and k.startswith("_"):
                    # Preserve private keys in nested dicts too
                    result[k] = v
                elif isinstance(v, str):
                    result[k] = self._cell_redaction_policy.apply_to_value(v)
                else:
                    # Non-string values pass through unchanged
                    result[k] = v
            return result
        else:
            # Non-string, non-container values pass through unchanged
            return value

    @contextmanager
    def perf_timer(
        self,
        phase: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> Generator[None, None, None]:
        """Measure a code block and emit a perf event (no-op when disabled)."""
        if not self._enabled:
            yield
            return

        start_ns = monotonic_ns()
        error: Exception | None = None
        try:
            yield
        except Exception as exc:  # pragma: no cover - propagated upstream
            error = exc
            raise
        finally:
            duration_ms = (monotonic_ns() - start_ns) / 1_000_000
            event_payload: dict[str, Any] = {"ok": error is None}
            if payload:
                event_payload.update(payload)
            if error is not None:
                event_payload["error"] = str(error)
                event_payload["error_type"] = error.__class__.__name__
            self.record_perf(phase=phase, duration_ms=duration_ms, payload=event_payload)

    def iter_events(self) -> Iterable[RecorderEvent]:
        return tuple(self._buffer)

    def flush(self, *, reason: str | None = None) -> Path | None:
        if not self._buffer:
            return None
        try:
            self.config.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            return None

        suffix = "session"
        if reason:
            suffix = f"{suffix}-{reason}"
        filename = f"{self._session_id}-{suffix}.pulka.jsonl"
        if self.config.compression == "zst":
            filename += ".zst"
        path = self.config.output_dir / filename

        if self.config.compression == "zst" and zstd is not None:
            compressor = zstd.ZstdCompressor(level=self.config.compression_level)
            with path.open("wb") as fh, compressor.stream_writer(fh) as writer:
                for event in self._buffer:
                    line = (
                        json.dumps(
                            event.to_dict(),
                            ensure_ascii=False,
                            default=_json_default,
                        )
                        + "\n"
                    )
                    writer.write(line.encode("utf-8"))
        else:
            with path.open("w", encoding="utf-8") as fh:
                for event in self._buffer:
                    line = (
                        json.dumps(
                            event.to_dict(),
                            ensure_ascii=False,
                            default=_json_default,
                        )
                        + "\n"
                    )
                    fh.write(line)

        return path

    def flush_and_clear(self, *, reason: str | None = None) -> Path | None:
        path = self.flush(reason=reason)
        self._buffer.clear()
        return path

    def on_process_exit(self, *, reason: str | None = None) -> Path | None:
        if not self.config.auto_flush_on_exit:
            return None
        return self.flush(reason=reason)

    # ------------------------------------------------------------------
    # High level helpers
    # ------------------------------------------------------------------
    def ensure_env_recorded(self) -> None:
        if not self._enabled or self._env_recorded:
            return
        self.record("env", _collect_environment_payload())
        self._env_recorded = True

    def record_dataset_open(self, *, path: str, schema: dict[str, Any], lazy: bool) -> None:
        redacted_path = redact_path(path)
        payload = {
            "path": redacted_path,
            "schema": {name: str(dtype) for name, dtype in schema.items()},
            "lazy": lazy,
            "_raw_path": path,  # Keep original path for internal replay purposes
        }
        self.record("dataset_open", payload)

    def record_status(self, status_text: str) -> None:
        self.record("status", {"text": status_text})

    def record_state(self, state_payload: dict[str, Any]) -> None:
        self.record("state", state_payload)

    def record_session_start(
        self,
        *,
        plugins: list[dict[str, Any]],
        disabled: list[str],
        configured: list[str] | None = None,
        failures: list[tuple[str, str]] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "plugins": plugins,
            "disabled": disabled,
        }
        if configured is not None:
            payload["disabled_configured"] = configured
        if failures:
            payload["plugin_failures"] = [
                {"name": name, "error": error} for name, error in failures
            ]
        self.record("session_start", payload)

    def record_frame(self, *, frame_text: str, frame_hash: str) -> None:
        self.record("frame", {"hash": frame_hash, "text": frame_text})

    def record_exception(self, *, message: str, stack: str | None = None) -> None:
        payload = {"message": message}
        if stack:
            payload["stack"] = stack
        self.record("exception", payload)

    def record_render_line_styles(
        self,
        *,
        component: str,
        lines: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {"component": component, "lines": lines}
        if metadata:
            payload.update(metadata)
        self.record("render_line_styles", payload)

    def export_repro_slice(
        self, *, session: Any, row_margin: int = 10, include_all_columns: bool = False
    ) -> Path:
        """Export a reproducible slice of the active sheet data.

        Args:
            session: The active Pulka session to extract data from.
            row_margin: Number of rows to include above/below the current viewport.
            include_all_columns: If True, export all columns; if False, only visible ones.

        Returns:
            Path to the generated Parquet file.

        Raises:
            RuntimeError: If the export fails.
        """

        from ..data.repro import build_repro_slice, write_repro_parquet

        # Build the reproducible slice
        df = build_repro_slice(
            session, row_margin=row_margin, include_all_columns=include_all_columns
        )

        # Create destination path in the session directory
        session_dir = self.config.output_dir
        session_dir.mkdir(parents=True, exist_ok=True)
        destination = session_dir / f"{self._session_id}-repro.parquet"

        # Apply the current redaction policy and write to Parquet
        write_repro_parquet(df, destination, self._cell_redaction_policy)

        # Record the export event with redacted path
        redacted_path = redact_path(str(destination))
        self.record(
            "repro_export",
            {
                "path": redacted_path,
                "rows": len(df),
                "cols": len(df.columns),
                "_raw_path": str(destination),  # Keep raw path for internal tooling
            },
        )

        return destination


def _collect_environment_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {}
    payload["timestamp"] = datetime.now(UTC).isoformat()
    payload["hostname"] = socket.gethostname()
    payload["platform"] = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
    }
    payload["term"] = {
        "TERM": os.getenv("TERM"),
        "COLORTERM": os.getenv("COLORTERM"),
    }
    payload["window_size"] = {
        "columns": os.getenv("COLUMNS"),
        "lines": os.getenv("LINES"),
    }
    # Gather Pulka metadata
    metadata: dict[str, Any] = {}
    try:
        metadata["pulka_version"] = importlib_metadata.version("pulka")
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        metadata["pulka_version"] = "unknown"
    payload["app"] = metadata

    payload["git"] = _collect_git_info()
    payload["locale"] = {
        "LANG": os.getenv("LANG"),
        "LC_ALL": os.getenv("LC_ALL"),
    }
    return payload


def _collect_git_info() -> dict[str, Any]:
    info: dict[str, Any] = {}
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        info["sha"] = result.stdout.strip()
    except Exception:
        info["sha"] = None
    return info

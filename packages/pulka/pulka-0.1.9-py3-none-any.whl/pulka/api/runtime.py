"""Runtime bootstrap for Pulka sessions.

The :class:`Runtime` encapsulates the expensive one-time setup required before
opening datasets: user configuration, registry construction, and plugin
discovery. Reusing a runtime across sessions avoids reloading plugins and keeps
metadata available for headless utilities that do not immediately open a
dataset.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

from ..command.registry import CommandRegistry
from ..config.load import load_user_config
from ..core.interfaces import JobRunnerProtocol
from ..core.jobs import JobRunner
from ..data.scanners import ScannerRegistry
from ..logging import Recorder
from ..plugin.manager import PluginManager
from ..sheets.registry import SheetRegistry

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ..core.viewer.ui_hooks import ViewerUIHooks
    from .session import Session


def _env_flag(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class RuntimeRecorderBootstrap:
    """Recorder metadata captured during runtime initialisation."""

    plugins: list[dict[str, str | None]]
    disabled: list[str]
    configured: list[str]
    failures: list[tuple[str, str]]


class Runtime:
    """Shared bootstrap context for Pulka sessions."""

    def __init__(
        self,
        *,
        registry: CommandRegistry | None = None,
        sheets: SheetRegistry | None = None,
        scanners: ScannerRegistry | None = None,
        plugins: Iterable[str] | None = None,
        load_entry_points: bool = True,
        job_runner: JobRunnerProtocol | None = None,
    ) -> None:
        self.config = load_user_config()
        requested_workers = self._resolve_requested_workers()
        self._executor: ThreadPoolExecutor | None = None
        self._executor_owned = False
        self._closed = False
        if job_runner is None:
            max_workers = self._effective_worker_count(requested_workers)
            self._executor = ThreadPoolExecutor(max_workers=max_workers)
            job_runner = JobRunner(executor=self._executor, max_workers=max_workers)
            self._executor_owned = True
        if not isinstance(job_runner, JobRunnerProtocol):
            msg = "job_runner must implement JobRunnerProtocol"
            raise TypeError(msg)
        self.job_runner: JobRunnerProtocol = job_runner

        if registry is None:
            commands = CommandRegistry(load_builtin_commands=False)
            commands.load_builtins()
            self.commands = commands
        else:
            self.commands = registry

        self.sheets = sheets or SheetRegistry()
        self._register_builtin_sheets()
        self.scanners = scanners or ScannerRegistry()

        module_candidates = [*self.config.plugins.modules, *(plugins or [])]
        self.plugin_modules = list(dict.fromkeys(module_candidates))
        self.plugin_manager = PluginManager(modules=self.plugin_modules)

        disable_entry_points = set(self.config.plugins.disable)
        self.disabled_plugins_configured = set(disable_entry_points)

        env_disables_entry_points = _env_flag(os.environ.get("PULKA_NO_ENTRYPOINTS"))
        self.include_entry_points = load_entry_points and not env_disables_entry_points
        should_load_plugins = self.include_entry_points or bool(self.plugin_modules)

        if should_load_plugins:
            self.loaded_plugins = self.plugin_manager.load(
                commands=self.commands,
                sheets=self.sheets,
                scanners=self.scanners,
                include_entry_points=self.include_entry_points,
                disabled=disable_entry_points,
            )
        else:
            self.loaded_plugins = []

        self.plugin_failures = list(self.plugin_manager.failures)
        self.plugin_metadata = list(self.plugin_manager.loaded_details)
        self.disabled_plugins = list(self.plugin_manager.disabled_canonical)

        if "pulka-summary" in self.disabled_plugins:
            self.commands.remove_provider("pulka-summary")

        self.recorder_bootstrap = RuntimeRecorderBootstrap(
            plugins=list(self.plugin_metadata),
            disabled=list(self.disabled_plugins),
            configured=sorted(self.disabled_plugins_configured),
            failures=list(self.plugin_failures),
        )

    def _register_builtin_sheets(self) -> None:
        """Ensure core sheet kinds are available before plugins load."""

        from ..sheets.freq_sheet import FreqSheet
        from ..sheets.hist_sheet import HistogramSheet
        from ..sheets.transpose_sheet import TransposeSheet

        registry = self.sheets
        existing = set(registry.list_kinds())
        builtins = {
            "freq": FreqSheet,
            "histogram": HistogramSheet,
            "transpose": TransposeSheet,
        }
        for kind, cls in builtins.items():
            if kind in existing:
                continue
            with suppress(ValueError):
                registry.register_sheet(kind, cls)

    def open(
        self,
        path: str | Path | None,
        *,
        viewport_rows: int | None = None,
        viewport_cols: int | None = None,
        recorder: Recorder | None = None,
        ui_hooks: ViewerUIHooks | None = None,
        lazyframe: pl.LazyFrame | None = None,
        source_label: str | None = None,
    ) -> Session:
        """Open a dataset path or ``LazyFrame`` with a session bound to this runtime."""

        from .session import Session

        return Session(
            path,
            viewport_rows=viewport_rows,
            viewport_cols=viewport_cols,
            recorder=recorder,
            runtime=self,
            ui_hooks=ui_hooks,
            lazyframe=lazyframe,
            source_label=source_label,
        )

    def bootstrap_recorder(self, recorder: Recorder) -> None:
        """Record runtime plugin metadata on ``recorder`` if enabled."""

        if not recorder.enabled:
            return
        recorder.record_session_start(
            plugins=list(self.recorder_bootstrap.plugins),
            disabled=list(self.recorder_bootstrap.disabled),
            configured=list(self.recorder_bootstrap.configured),
            failures=list(self.recorder_bootstrap.failures),
        )

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    def close(self, *, wait: bool = False) -> None:
        """Release any executor resources owned by this runtime."""

        if self._closed:
            return
        self._closed = True
        if self._executor_owned and self._executor is not None:
            self._executor.shutdown(wait=wait)
            self._executor = None

    def __enter__(self) -> Runtime:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # Internal helpers -------------------------------------------------

    def _resolve_requested_workers(self) -> int | None:
        for key in ("PULKA_JOB_WORKERS", "PD_JOB_WORKERS"):
            raw = os.environ.get(key)
            if raw is None:
                continue
            try:
                value = int(raw)
            except ValueError:
                continue
            if value > 0:
                return value
        config_jobs = getattr(self.config, "jobs", None)
        if config_jobs is None:
            return None
        max_workers = getattr(config_jobs, "max_workers", None)
        if isinstance(max_workers, int) and max_workers > 0:
            return max_workers
        return None

    def _effective_worker_count(self, requested: int | None) -> int:
        default_workers = min(4, os.cpu_count() or 2)
        if requested is None:
            return default_workers
        return max(1, requested)


__all__ = ["Runtime", "RuntimeRecorderBootstrap"]

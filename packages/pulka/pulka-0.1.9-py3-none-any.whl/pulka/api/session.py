"""
Session facade for Pulka.

This module provides the main entry point for embedding Pulka in other applications.
"""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

from ..command.runtime import SessionCommandRuntime
from ..core.viewer import Viewer, ViewStack, viewer_public_state
from ..core.viewer.ui_hooks import ViewerUIHooks
from ..logging import Recorder, RecorderConfig
from ..sheets.data_sheet import DataSheet
from ..sheets.file_browser_sheet import FileBrowserSheet, file_browser_status_text
from .runtime import Runtime

if TYPE_CHECKING:
    from ..core.sheet import Sheet


class Session:
    """
    A session represents a single interaction with a data source.

    It manages the viewer state, data access, and provides methods for
    programmatic interaction with the data. The ``command_runtime`` attribute
    exposes a :class:`~pulka.command.runtime.SessionCommandRuntime` that powers
    both the TUI and headless runners.
    """

    def __init__(
        self,
        path: str | Path | None,
        *,
        viewport_rows: int | None = None,
        viewport_cols: int | None = None,
        recorder: Recorder | None = None,
        ui_hooks: ViewerUIHooks | None = None,
        runtime: Runtime | None = None,
        lazyframe: pl.LazyFrame | None = None,
        source_label: str | None = None,
        initial_sheet: Sheet | None = None,
    ):
        """
        Initialize a new Pulka session.

        Args:
            path: Path to the data file to open (required unless ``lazyframe`` is provided)
            lazyframe: Optional ``pl.LazyFrame`` to open directly without scanning a path
            source_label: Display label recorded when ``lazyframe`` is provided
            viewport_rows: Override the number of visible rows (for testing)
            viewport_cols: Override the number of visible columns (for testing)
            recorder: Optional flight recorder instance to reuse
            ui_hooks: Viewer hook bridge used for terminal measurements and redraws
            runtime: Shared :class:`~pulka.api.runtime.Runtime` providing
                configuration, registries, and plugin metadata. When omitted, a
                private runtime will be created for this session.
        """
        if path is None and lazyframe is None and initial_sheet is None:
            msg = "Session requires a source path, lazyframe, or initial sheet"
            raise ValueError(msg)

        self._viewport_rows = viewport_rows
        self._viewport_cols = viewport_cols
        self.recorder = recorder or Recorder(RecorderConfig())
        self.view_stack = ViewStack(ui_hooks=ui_hooks)
        self.viewer: Viewer | None = None
        self._view_stack_unsubscribe = self.view_stack.add_active_viewer_listener(
            self._on_active_viewer_changed
        )

        owns_runtime = runtime is None
        self.runtime = runtime or Runtime()
        runtime = self.runtime
        self._owns_runtime = owns_runtime
        self._closed = False
        self.job_runner = runtime.job_runner
        self.config = runtime.config
        self.commands = runtime.commands
        self.sheets = runtime.sheets
        self.scanners = runtime.scanners
        self.plugin_manager = runtime.plugin_manager
        self.plugin_modules = runtime.plugin_modules
        self.loaded_plugins = runtime.loaded_plugins
        self.plugin_failures = runtime.plugin_failures
        self.plugin_metadata = runtime.plugin_metadata
        self.disabled_plugins = runtime.disabled_plugins
        self.disabled_plugins_configured = runtime.disabled_plugins_configured

        self.command_runtime: SessionCommandRuntime = SessionCommandRuntime(self)

        runtime.bootstrap_recorder(self.recorder)

        resolved_path = Path(path) if path is not None else None
        self._source_path = resolved_path or Path("<expr>")
        self._dataset_path: Path | None = resolved_path

        if initial_sheet is not None:
            self._dataset_path = None
            label = source_label or getattr(initial_sheet, "display_path", None) or "<browser>"
            self._install_root_sheet(initial_sheet, source_label=label, source_is_path=False)
        elif lazyframe is not None:
            self.open_lazyframe(lazyframe, label=source_label)
        else:
            assert resolved_path is not None  # for mypy
            self.open(resolved_path)
        with suppress(Exception):
            self.command_runtime.prepare_viewer(self.viewer)

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release resources associated with this session."""

        if self._closed:
            return
        self._closed = True

        recorder = getattr(self, "recorder", None)
        if recorder is not None and recorder.enabled:
            metrics_fn = getattr(self.job_runner, "metrics", None)
            if callable(metrics_fn):
                with suppress(Exception):
                    metrics_payload = metrics_fn()
                    if isinstance(metrics_payload, dict):
                        recorder.record("job_runner_metrics", metrics_payload)

        unsubscribe = getattr(self, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            with suppress(Exception):
                unsubscribe()
            self._view_stack_unsubscribe = None

        for viewer in tuple(self.view_stack.viewers):
            sheet = getattr(viewer, "sheet", None)
            runner = getattr(viewer, "job_runner", None)
            sheet_id = getattr(sheet, "sheet_id", None)
            if runner is not None and sheet_id is not None:
                with suppress(Exception):
                    runner.invalidate_sheet(sheet_id)
        self.viewer = None
        self.view_stack = ViewStack(ui_hooks=self.view_stack.ui_hooks)

        if self._owns_runtime:
            self.runtime.close()

    def __enter__(self) -> Session:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        with suppress(Exception):
            self.close()

    def push_viewer(self, viewer: Viewer) -> Viewer:
        """Add ``viewer`` to the derived-view stack and make it active."""

        return self.view_stack.push(viewer)

    def _pop_viewer(self) -> None:
        """Pop the active viewer when a derived view finishes."""

        self.view_stack.pop()

    def open_sheet_view(
        self,
        kind: str,
        *,
        base_viewer: Viewer,
        viewer_options: dict[str, object] | None = None,
        **sheet_options: object,
    ) -> Viewer:
        """Instantiate a derived sheet and push its viewer onto the stack."""

        sheet_kwargs = dict(sheet_options)
        if "runner" not in sheet_kwargs:
            sheet_kwargs["runner"] = self.job_runner
        try:
            sheet = self.sheets.create(kind, base_viewer.sheet, **sheet_kwargs)
        except TypeError as exc:
            if (
                "runner" in sheet_kwargs
                and "unexpected keyword" in str(exc)
                and "runner" in str(exc)
            ):
                provider = getattr(self.sheets, "_providers", {}).get(kind, "unknown provider")
                msg = (
                    "Sheet factory for kind "
                    f"'{kind}' provided by {provider} does not accept the 'runner' keyword. "
                    "Update the constructor to accept a `runner` parameter so sessions "
                    "can reuse the runtime job runner."
                )
                raise TypeError(msg) from exc
            raise
        viewer_kwargs: dict[str, object] = {
            "viewport_rows": getattr(base_viewer, "_viewport_rows_override", None),
            "viewport_cols": getattr(base_viewer, "_viewport_cols_override", None),
            "source_path": getattr(base_viewer, "_source_path", None),
            "session": self,
            "ui_hooks": self.view_stack.ui_hooks,
        }
        if viewer_options:
            viewer_kwargs.update(viewer_options)

        derived_viewer = Viewer(sheet, runner=self.job_runner, **viewer_kwargs)
        if getattr(base_viewer, "_pulka_has_real_source_path", False):
            derived_viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]

        perf_callback = getattr(base_viewer, "_perf_callback", None)
        if perf_callback is not None and hasattr(derived_viewer, "set_perf_callback"):
            with suppress(Exception):
                derived_viewer.set_perf_callback(perf_callback)

        self.push_viewer(derived_viewer)
        active = self.view_stack.active
        return active if active is not None else derived_viewer

    def set_viewer_ui_hooks(self, hooks: ViewerUIHooks | None) -> None:
        """Install ``hooks`` for every viewer in the stack."""

        self.view_stack.set_ui_hooks(hooks)

    def _on_active_viewer_changed(self, viewer: Viewer) -> None:
        self.viewer = viewer

    def run_script(self, commands: list[str], auto_render: bool = True) -> list[str]:
        """
        Execute a list of script commands.

        Args:
            commands: List of command strings to execute
            auto_render: Whether to render the output after each command

        Returns:
            List of rendered outputs or messages
        """
        from ..headless.runner import run_script_mode

        return run_script_mode(
            self,
            commands,
            auto_render=auto_render,
        )

    def render(self, *, include_status: bool = True) -> str:
        """
        Render the current view of the data.

        Args:
            include_status: Whether to include the status bar in the output

        Returns:
            String representation of the current view
        """
        from ..render.table import render_table

        if self.recorder and self.recorder.enabled:
            with self.recorder.perf_timer(
                "render.table",
                payload={
                    "context": "session",
                    "include_status": bool(include_status),
                },
            ):
                return render_table(self.viewer, include_status=include_status)
        return render_table(self.viewer, include_status=include_status)

    def get_state_json(self) -> dict:
        """
        Get the current state of the session as a JSON-serializable dictionary.

        Returns:
            Dictionary containing cursor and viewport state
        """
        state = viewer_public_state(self.viewer)
        if state is None:  # pragma: no cover - defensive
            msg = "Active viewer does not expose snapshot state"
            raise RuntimeError(msg)

        visible_columns = list(state.visible_columns or state.columns)
        visible_column_count = state.visible_column_count or state.total_columns
        total_rows = state.total_rows if state.total_rows is not None else state.visible_row_count
        return {
            "cursor_row": state.cursor.row,
            "cursor_col": state.cursor.col,
            "top_row": state.viewport.row0,
            "left_col": state.viewport.col0,
            "n_rows": total_rows,
            "n_cols": visible_column_count,
            "col_order": visible_columns,
        }

    @property
    def sheet(self) -> Sheet:
        """Get the current sheet that the session is viewing."""
        return self.viewer.sheet

    @property
    def dataset_path(self) -> Path | None:
        """Return the currently open dataset path when available."""

        active = self.viewer
        if active is not None and getattr(active, "_pulka_has_real_source_path", False):
            source = getattr(active, "_source_path", None)
            candidate = self._coerce_dataset_path(source)
            if candidate is not None:
                return candidate
        return self._dataset_path

    def open(self, path: str | Path) -> None:
        """Open ``path`` and update the viewer."""

        resolved = Path(path)
        self._dataset_path = resolved
        physical_plan = self.scanners.scan(resolved)
        sheet = DataSheet(physical_plan, runner=self.job_runner)
        self._install_root_sheet(sheet, source_label=str(resolved), source_is_path=True)

    def open_lazyframe(self, lazyframe: pl.LazyFrame, *, label: str | None = None) -> None:
        """Open a ``LazyFrame`` directly without going through scanners."""

        self._dataset_path = None
        source_label = label or getattr(lazyframe, "_pulka_path", None) or "<expr>"
        sheet = DataSheet(lazyframe, runner=self.job_runner)
        self._install_root_sheet(sheet, source_label=source_label, source_is_path=False)

    def open_file_browser(self, directory: str | Path | None = None) -> None:
        """Open a file-browser sheet rooted at ``directory`` as the stack root."""

        target = self._coerce_browser_directory(directory)
        if target is None:
            raise ValueError("browse requires a directory path or file-backed dataset")
        if not target.is_dir():
            raise ValueError(f"{target} is not a directory")

        sheet = FileBrowserSheet(target, scanners=self.scanners)
        self._dataset_path = None
        self._install_root_sheet(sheet, source_label=str(target), source_is_path=False)
        new_viewer = self.viewer
        if new_viewer is not None:
            with suppress(Exception):
                self.command_runtime.prepare_viewer(new_viewer)
            with suppress(Exception):
                new_viewer.row_count_tracker.ensure_total_rows()
            new_viewer.status_message = file_browser_status_text(sheet)

    def open_dataset_viewer(
        self,
        path: str | Path,
        *,
        base_viewer: Viewer | None = None,
    ) -> Viewer:
        """Push a new viewer for ``path`` while keeping the current stack."""

        resolved = Path(path)
        sheet = DataSheet(self.scanners.scan(resolved), runner=self.job_runner)
        reference_viewer = base_viewer or self.viewer
        viewer_kwargs: dict[str, object] = {
            "viewport_rows": getattr(reference_viewer, "_viewport_rows_override", None),
            "viewport_cols": getattr(reference_viewer, "_viewport_cols_override", None),
            "source_path": str(resolved),
            "session": self,
            "ui_hooks": self.view_stack.ui_hooks,
        }
        child_viewer = Viewer(sheet, runner=self.job_runner, **viewer_kwargs)
        child_viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]
        self.push_viewer(child_viewer)
        with suppress(Exception):
            self.command_runtime.prepare_viewer(child_viewer)
        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=str(resolved),
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )
        return child_viewer

    def reload_viewer(self, viewer: Viewer) -> None:
        """Reload ``viewer`` in-place if it is backed by a filesystem path."""

        path = self._coerce_dataset_path(getattr(viewer, "_source_path", None))
        if path is None:
            msg = "viewer cannot be reloaded without a filesystem path"
            raise ValueError(msg)
        sheet = DataSheet(self.scanners.scan(path), runner=self.job_runner)
        viewer.replace_sheet(sheet, source_path=str(path))
        viewer._pulka_has_real_source_path = True  # type: ignore[attr-defined]
        if viewer is self.view_stack.viewers[0]:
            self._dataset_path = path
        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=str(path),
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )

    def _install_root_sheet(
        self,
        sheet: Sheet,
        *,
        source_label: str | Path | None,
        source_is_path: bool = False,
    ) -> None:
        label = str(source_label) if source_label is not None else "<expr>"
        root_viewer = Viewer(
            sheet,
            viewport_rows=self._viewport_rows,
            viewport_cols=self._viewport_cols,
            source_path=label,
            session=self,
            ui_hooks=self.view_stack.ui_hooks,
            runner=self.job_runner,
        )
        root_viewer._pulka_has_real_source_path = bool(  # type: ignore[attr-defined]
            source_is_path
        )
        self.view_stack.reset(root_viewer)
        self._source_path = Path(label)

        if self.recorder.enabled:
            self.recorder.ensure_env_recorded()
            self.recorder.record_dataset_open(
                path=label,
                schema=getattr(sheet, "schema", {}),
                lazy=True,
            )

        if getattr(self, "plugin_failures", None):
            failed_names = ", ".join(name for name, _ in self.plugin_failures)
            plural = "s" if len(self.plugin_failures) > 1 else ""
            self.viewer.status_message = f"Plugin{plural} {failed_names} failed to load; see logs"

    def _coerce_dataset_path(self, source: str | Path | None) -> Path | None:
        if source is None:
            return None
        if isinstance(source, Path):
            candidate = source
        else:
            if source.startswith("<"):
                return None
            candidate = Path(source)
        return candidate

    def _coerce_browser_directory(self, directory: str | Path | None) -> Path | None:
        if directory is not None:
            try:
                return Path(directory).expanduser()
            except Exception:
                return None
        dataset = self.dataset_path
        if dataset is not None:
            return dataset if dataset.is_dir() else dataset.parent
        viewer = getattr(self, "viewer", None)
        sheet = getattr(viewer, "sheet", None)
        if sheet is not None and getattr(sheet, "is_file_browser", False):
            active_dir = getattr(sheet, "directory", None)
            if active_dir is not None:
                return Path(active_dir)
        return None


def open(
    path: str | Path | None,
    *,
    viewport_rows: int | None = None,
    viewport_cols: int | None = None,
    recorder: Recorder | None = None,
    ui_hooks: ViewerUIHooks | None = None,
    runtime: Runtime | None = None,
    lazyframe: pl.LazyFrame | None = None,
    source_label: str | None = None,
) -> Session:
    """
    Open a data file or pre-built ``pl.LazyFrame`` in a new Pulka session.

    Args:
        path: Path to the data file to open (required unless ``lazyframe`` is provided)
        viewport_rows: Override the number of visible rows (for testing)
        viewport_cols: Override the number of visible columns (for testing)
        recorder: Optional flight recorder instance to reuse
        ui_hooks: Optional UI bridge passed through to :class:`Viewer`
        runtime: Optional shared :class:`~pulka.api.runtime.Runtime` to reuse
            configuration and plugin state. When omitted, the session creates a
            private runtime.
        lazyframe: Optional ``pl.LazyFrame`` to open directly instead of scanning ``path``
        source_label: Display label recorded when ``lazyframe`` is provided

    Returns:
        A new Session instance
    """
    return Session(
        path,
        viewport_rows=viewport_rows,
        viewport_cols=viewport_cols,
        recorder=recorder,
        ui_hooks=ui_hooks,
        runtime=runtime,
        lazyframe=lazyframe,
        source_label=source_label,
    )

"""
SessionRunner for testing and headless execution of Pulka.

This module provides the SessionRunner class which offers an enhanced interface
for running commands and capturing frames for testing purposes.
"""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import Any, NamedTuple

from .api.runtime import Runtime
from .api.session import Session
from .testing import setup_test_environment


class SessionResult(NamedTuple):
    """Result of a SessionRunner.run() call."""

    frames: list[str]
    last_frame_str: str
    state_json: dict[str, Any]


class SessionRunner:
    """
    Enhanced session runner for testing and automated execution.

    This class provides functionality to run commands, capture frames,
    and get state information needed for testing.
    """

    def __init__(self, dataset_path: str | Path, *, runtime: Runtime | None = None):
        """
        Initialize SessionRunner with a dataset.

        Args:
            dataset_path: Path to the dataset to load
            runtime: Optional shared runtime instance used to create sessions
        """
        self.dataset_path = Path(dataset_path)
        owns_runtime = runtime is None
        self.runtime = runtime or Runtime()
        self._owns_runtime = owns_runtime
        self._session: Session | None = None

    @staticmethod
    def run(
        dataset: str | Path,
        commands: list[str],
        width: int = 80,
        height: int = 20,
        test_mode: bool = True,
        runtime: Runtime | None = None,
    ) -> SessionResult:
        """
        Run a sequence of commands and return frames and final state.

        Args:
            dataset: Path to the dataset file
            commands: List of command strings to execute
            width: Terminal width for rendering
            height: Terminal height for rendering
            test_mode: Whether to run in test mode (deterministic output)

        Returns:
            SessionResult containing frames, last frame, and state JSON
        """
        if test_mode:
            setup_test_environment()

        # Create session with specified viewport
        # Account for headers/status when setting viewport rows
        viewport_rows = max(1, height - 5)
        owns_runtime = runtime is None
        runtime_obj = runtime or Runtime()
        session = runtime_obj.open(str(dataset), viewport_rows=viewport_rows, viewport_cols=None)
        try:
            viewer = session.viewer
            if viewer is None:
                msg = "Session.open() returned without an active viewer"
                raise RuntimeError(msg)
            # Set the actual terminal dimensions for test reproducibility
            viewer.configure_terminal(width, viewport_rows)

            # Execute commands and capture frames
            frames = []

            # Initial frame
            initial_frame = session.render(include_status=True)
            frames.append(initial_frame)

            # After capturing the initial frame, allow subsequent renders to use
            # the standard test-mode width heuristics.
            viewer.set_view_width_override(None)

            # Execute each command
            for command in commands:
                try:
                    outputs = session.run_script([command], auto_render=True)
                    # The last output should be the rendered frame
                    if outputs:
                        frames.append(outputs[-1])
                except Exception as e:
                    # Add error as a frame
                    frames.append(f"Error executing '{command}': {e}")

            # Get final state
            last_frame = frames[-1] if frames else ""
            state_json = session.get_state_json()

            return SessionResult(
                frames=frames,
                last_frame_str=last_frame,
                state_json=state_json,
            )
        finally:
            with suppress(Exception):
                session.close()
            if owns_runtime:
                runtime_obj.close()

    def create_session(
        self, width: int = 80, height: int = 20, *, runtime: Runtime | None = None
    ) -> Session:
        """
        Create a Session instance for this dataset.

        Args:
            width: Terminal width
            height: Terminal height
            runtime: Optional runtime to use when opening the dataset

        Returns:
            Session instance
        """
        runtime_obj = runtime or self.runtime
        if self._session is None:
            # Account for headers/status when setting viewport rows
            viewport_rows = max(1, height - 5)
            self._session = runtime_obj.open(
                str(self.dataset_path), viewport_rows=viewport_rows, viewport_cols=None
            )
            # First call update_terminal_metrics, then override with our test values
            viewer = self._session.viewer
            if viewer is None:
                msg = "runtime.open() did not provide a viewer instance"
                raise RuntimeError(msg)
            viewer.configure_terminal(width, viewport_rows)
        return self._session

    def run_commands(self, commands: list[str], width: int = 80, height: int = 20) -> SessionResult:
        """
        Run commands on this dataset and return results.

        Args:
            commands: Commands to execute
            width: Terminal width
            height: Terminal height

        Returns:
            SessionResult with frames and state
        """
        return self.run(self.dataset_path, commands, width, height)

    def close(self) -> None:
        """Release any owned session/runtime resources."""

        session = self._session
        if session is not None:
            with suppress(Exception):
                session.close()
            self._session = None
        if self._owns_runtime:
            with suppress(Exception):
                self.runtime.close()

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        with suppress(Exception):
            self.close()

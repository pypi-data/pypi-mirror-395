"""
TUI application for Pulka.

This module integrates prompt_toolkit and Rich to provide the interactive
terminal user interface for Pulka.
"""

from __future__ import annotations

import traceback
from collections.abc import Callable
from typing import TYPE_CHECKING

from ..core.viewer import Viewer
from ..logging import Recorder
from .screen import Screen

if TYPE_CHECKING:  # pragma: no cover - typing import only
    from ..api.session import Session


class App:
    """Main TUI application for Pulka."""

    def __init__(
        self,
        viewer: Viewer,
        recorder: Recorder | None = None,
        *,
        on_shutdown: Callable[[Session], None] | None = None,
    ):
        self.viewer = viewer
        self.recorder = recorder
        self.screen = Screen(viewer, recorder=recorder, on_shutdown=on_shutdown)

    def run(self):
        """Run the TUI application."""
        if self.recorder:
            self.recorder.ensure_env_recorded()
        try:
            self.screen.run()
        except Exception as exc:  # pragma: no cover - defensive
            if self.recorder and self.recorder.enabled:
                self.recorder.record_exception(message=str(exc), stack=traceback.format_exc())
                self.recorder.flush_and_clear(reason="exception")
            raise


def run_tui_app(
    viewer: Viewer,
    *,
    recorder: Recorder | None = None,
    on_shutdown: Callable[[Session], None] | None = None,
):
    """Convenience function to run the TUI application."""
    app = App(viewer, recorder=recorder, on_shutdown=on_shutdown)
    app.run()

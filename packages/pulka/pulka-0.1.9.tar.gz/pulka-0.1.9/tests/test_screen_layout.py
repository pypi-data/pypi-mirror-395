"""Layout-related tests for the TUI screen."""

from __future__ import annotations

import os

import polars as pl

os.environ["PULKA_TEST"] = "1"

from pulka.api.runtime import Runtime
from pulka.tui.screen import Screen


def _make_session(tmp_path):
    runtime = Runtime(load_entry_points=False)
    data_path = tmp_path / "layout.parquet"
    pl.DataFrame({"a": [1, 2]}).write_parquet(data_path)
    session = runtime.open(str(data_path))
    return runtime, session


def test_insight_panel_resizes_view_width(monkeypatch, tmp_path) -> None:
    runtime, session = _make_session(tmp_path)
    screen = Screen(session.viewer)

    monkeypatch.setattr(screen._viewer_ui_hooks, "get_terminal_size", lambda fallback: (120, 40))
    terminal_width, _ = screen._viewer_ui_hooks.get_terminal_size((0, 0))

    screen.set_insight_panel(False)
    screen._update_viewer_metrics()
    base_width = screen.viewer.view_width_chars

    screen.set_insight_panel(True)
    screen._update_viewer_metrics()
    expected_width = max(20, terminal_width - screen._insight_sidecar_width())
    assert screen.viewer.view_width_chars == expected_width

    screen.set_insight_panel(False)
    screen._update_viewer_metrics()
    assert screen.viewer.view_width_chars == base_width

    session.close()
    runtime.close()

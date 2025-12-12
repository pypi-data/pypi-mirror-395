"""Tests for dataset file change detection in the TUI screen."""

from __future__ import annotations

import os
from types import SimpleNamespace

import polars as pl

os.environ["PULKA_TEST"] = "1"

from pulka.api.runtime import Runtime
from pulka.api.session import Session
from pulka.data.scanners import ScannerRegistry
from pulka.sheets.file_browser_sheet import FileBrowserSheet
from pulka.tui.screen import Screen


def _make_session(tmp_path):
    runtime = Runtime(load_entry_points=False)
    data_path = tmp_path / "watch.parquet"
    pl.DataFrame({"a": [1, 2, 3]}).write_parquet(data_path)
    session = runtime.open(str(data_path))
    return runtime, session, data_path


def _make_file_browser_session(tmp_path):
    sheet = FileBrowserSheet(tmp_path, scanners=ScannerRegistry())
    session = Session(None, initial_sheet=sheet)
    return session


def test_screen_detects_dataset_modification(monkeypatch, tmp_path) -> None:
    _runtime, session, data_path = _make_session(tmp_path)
    screen = Screen(session.viewer)
    triggered: list[tuple[object, bool | None]] = []

    def fake_schedule(self, path, snapshot):
        missing = None if snapshot is None else snapshot.missing
        triggered.append((path, missing))

    monkeypatch.setattr(Screen, "_schedule_file_change_prompt", fake_schedule, raising=False)

    screen._check_dataset_file_changes(force=True)
    assert not triggered

    pl.DataFrame({"a": [10]}).write_parquet(data_path)
    screen._check_dataset_file_changes(force=True)

    assert triggered
    assert triggered[-1][0] == data_path
    assert triggered[-1][1] is False

    session.close()


def test_screen_detects_dataset_removal(monkeypatch, tmp_path) -> None:
    _runtime, session, data_path = _make_session(tmp_path)
    screen = Screen(session.viewer)
    triggered: list[tuple[object, bool | None]] = []

    def fake_schedule(self, path, snapshot):
        missing = None if snapshot is None else snapshot.missing
        triggered.append((path, missing))

    monkeypatch.setattr(Screen, "_schedule_file_change_prompt", fake_schedule, raising=False)

    screen._check_dataset_file_changes(force=True)
    assert not triggered

    data_path.unlink()
    screen._check_dataset_file_changes(force=True)

    assert triggered
    assert triggered[-1][0] == data_path
    assert triggered[-1][1] is True

    session.close()


def test_screen_skips_insight_refresh_when_file_change_pending(tmp_path, monkeypatch) -> None:
    _runtime, session, _ = _make_session(tmp_path)
    screen = Screen(session.viewer)

    called = {"ran": False}

    def _boom():
        called["ran"] = True
        raise AssertionError("insight refresh should be skipped")

    screen._insight_controller = SimpleNamespace(on_refresh=_boom)
    screen._file_watch_prompt_active = True

    # Avoid touching the real terminal metrics during the test.
    monkeypatch.setattr(screen.viewer, "update_terminal_metrics", lambda: None)

    screen.refresh()

    assert called["ran"] is False
    assert "File changed" in screen._insight_panel._status_message

    session.close()


def test_refresh_forces_file_change_check(tmp_path, monkeypatch) -> None:
    _runtime, session, _ = _make_session(tmp_path)
    screen = Screen(session.viewer)

    force_calls: list[bool] = []

    def fake_check(*, force: bool = False):
        force_calls.append(force)

    monkeypatch.setattr(screen, "_check_dataset_file_changes", fake_check)
    monkeypatch.setattr(screen.viewer, "update_terminal_metrics", lambda: None)

    screen.refresh()

    assert force_calls and force_calls[-1] is True

    session.close()


def test_screen_detects_file_browser_change(tmp_path) -> None:
    session = _make_file_browser_session(tmp_path)
    screen = Screen(session.viewer)

    screen._check_file_browser_changes(force=True)
    new_file = tmp_path / "new.csv"
    new_file.write_text("a\n1\n")

    screen._check_file_browser_changes(force=True)

    sheet = screen.viewer.sheet
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "new.csv" in names
    assert "entries" in (screen.viewer.status_message or "")

    session.close()


def test_file_browser_refresh_clears_row_provider_cache(tmp_path) -> None:
    session = _make_file_browser_session(tmp_path)
    screen = Screen(session.viewer)
    viewer = screen.viewer

    provider = viewer.row_provider
    plan = viewer._current_plan()  # type: ignore[attr-defined]

    initial_slice, _ = provider.get_slice(plan, viewer.columns, 0, 100)
    initial_names = list(initial_slice.column("name").values)
    assert "cached.csv" not in initial_names

    new_file = tmp_path / "cached.csv"
    new_file.write_text("a\n1\n")

    screen._check_file_browser_changes(force=True)

    updated_slice, _ = provider.get_slice(plan, viewer.columns, 0, 100)
    updated_names = list(updated_slice.column("name").values)
    assert "cached.csv" in updated_names

    session.close()

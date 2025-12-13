from __future__ import annotations

import os
from argparse import Namespace
from datetime import datetime

from pulka.api.runtime import Runtime
from pulka.cli import _browser_start_directory, _create_file_browser_session
from pulka.logging import Recorder, RecorderConfig
from pulka.render.viewport_plan import compute_viewport_plan
from pulka.sheets.file_browser_sheet import FileBrowserSheet


def test_browser_start_directory_detects_existing_directory(tmp_path) -> None:
    args = Namespace(path=str(tmp_path))

    result = _browser_start_directory(args, expr_text=None)

    assert result == tmp_path


def test_browser_start_directory_ignores_expr(tmp_path) -> None:
    args = Namespace(path=str(tmp_path))

    result = _browser_start_directory(args, expr_text="df")

    assert result is None


def test_file_browser_session_uses_custom_start_dir(tmp_path) -> None:
    runtime = Runtime(load_entry_points=False)
    recorder = Recorder(RecorderConfig(enabled=False))
    args = Namespace(viewport_rows=None, viewport_cols=None)
    (tmp_path / "dir_a").mkdir()

    session = _create_file_browser_session(
        runtime,
        recorder,
        args,
        start_dir=tmp_path,
    )

    viewer = session.viewer
    assert viewer is not None
    sheet = viewer.sheet
    assert isinstance(sheet, FileBrowserSheet)
    assert sheet.directory == tmp_path
    assert viewer.status_message.endswith("entries")

    session.close()
    runtime.close()


def test_file_browser_avoids_single_column_mode(tmp_path) -> None:
    runtime = Runtime(load_entry_points=False)
    recorder = Recorder(RecorderConfig(enabled=False))
    args = Namespace(viewport_rows=None, viewport_cols=None)
    (tmp_path / "dir_a").mkdir()

    session = _create_file_browser_session(
        runtime,
        recorder,
        args,
        start_dir=tmp_path,
    )

    width_state = session.viewer.width_mode_state
    assert width_state["mode"] == "default"
    assert width_state["target"] is None

    session.close()
    runtime.close()


def test_file_browser_name_column_expands_with_fill(tmp_path) -> None:
    runtime = Runtime(load_entry_points=False)
    recorder = Recorder(RecorderConfig(enabled=False))
    args = Namespace(viewport_rows=None, viewport_cols=None)
    (tmp_path / "dir_a").mkdir()
    file_path = tmp_path / "file.csv"
    file_path.write_text("data")
    timestamp = 1764852840
    os.utime(file_path, (timestamp, timestamp))

    session = _create_file_browser_session(
        runtime,
        recorder,
        args,
        start_dir=tmp_path,
    )

    viewer = session.viewer
    plan = compute_viewport_plan(viewer, width=120, height=10)
    name_plan = next(plan for plan in plan.columns if plan.name == "name")
    other_widths = [col.width for col in plan.columns if col.name in {"type", "size", "modified"}]

    assert name_plan.width > max(other_widths)

    modified_idx = next(idx for idx, col in enumerate(plan.columns) if col.name == "modified")
    name_idx = next(idx for idx, col in enumerate(plan.columns) if col.name == "name")
    target_row = None
    for row in plan.cells[1:]:  # skip header
        if "file.csv" in row[name_idx].text:
            target_row = row
            break

    assert target_row is not None
    displayed_timestamp = target_row[modified_idx].text.strip()
    expected_timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    assert expected_timestamp in displayed_timestamp

    session.close()
    runtime.close()

"""CLI helpers for launching the file browser."""

from __future__ import annotations

from argparse import Namespace

from pulka.api.runtime import Runtime
from pulka.cli import _browser_start_directory, _create_file_browser_session
from pulka.logging import Recorder, RecorderConfig
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

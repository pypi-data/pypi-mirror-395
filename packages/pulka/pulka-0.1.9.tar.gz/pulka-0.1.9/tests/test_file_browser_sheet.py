from __future__ import annotations

from pathlib import Path

import polars as pl

from pulka.api.session import Session
from pulka.core.viewer import Viewer
from pulka.data.scanners import ScannerRegistry
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.file_browser_sheet import FileBrowserSheet
from pulka.tui.screen import Screen


def _create_sheet(path: Path) -> FileBrowserSheet:
    return FileBrowserSheet(path, scanners=ScannerRegistry())


def test_file_browser_lists_supported_entries(tmp_path: Path) -> None:
    (tmp_path / "subdir").mkdir()
    (tmp_path / "data.csv").write_text("a,b\n1,2\n")
    (tmp_path / "ignore.txt").write_text("noop")

    sheet = _create_sheet(tmp_path)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]

    assert "subdir/" in names
    assert "data.csv" in names
    assert "ignore.txt" not in names
    if tmp_path.parent != tmp_path:
        assert names[0] == ".."


def test_file_browser_actions(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a\n1\n")
    sheet = _create_sheet(tmp_path)

    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    dir_row = names.index("nested/")
    file_row = names.index("sample.csv")

    dir_action = sheet.action_for_row(dir_row)
    file_action = sheet.action_for_row(file_row)

    assert dir_action is not None
    assert dir_action.type == "enter-directory"
    assert dir_action.path == nested

    assert file_action is not None
    assert file_action.type == "open-file"
    assert file_action.path == csv_path


def test_file_browser_can_jump_to_new_directory(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    sheet = _create_sheet(tmp_path)

    child_sheet = sheet.at_path(nested)
    assert child_sheet.display_path.endswith("nested")
    if nested.parent != nested:
        assert child_sheet.value_at(0, "name") == ".."


def test_file_browser_len_matches_row_count(tmp_path: Path) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path)
    assert len(sheet) == sheet.row_count()


def test_file_browser_can_show_unknown_when_configured(tmp_path: Path, monkeypatch) -> None:
    import pulka.data.scan as scan_mod

    (tmp_path / "data").write_text("x")

    monkeypatch.setattr(scan_mod, "_BROWSER_STRICT_EXTENSIONS", False)
    sheet = _create_sheet(tmp_path)
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "data" in names


def test_insight_panel_allowed_after_browser_open(tmp_path: Path) -> None:
    data_path = tmp_path / "sample.csv"
    data_path.write_text("a\n1\n")

    browser = _create_sheet(tmp_path)
    session = Session(None, initial_sheet=browser)
    screen = Screen(session.viewer)
    try:
        assert not screen._insight_allowed  # browser should disable insight

        screen._open_file_from_browser(data_path)

        assert not getattr(screen.viewer.sheet, "is_file_browser", False)
        assert screen._insight_allowed
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if callable(unsubscribe):
            unsubscribe()


def test_file_browser_maximizes_name_column(tmp_path: Path, job_runner) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path)

    viewer = Viewer(sheet, runner=job_runner)

    assert viewer.width_mode_state["mode"] == "single"
    assert viewer.maximized_column_index == viewer.columns.index("name")


def test_file_browser_width_resets_after_replacing_sheet(tmp_path: Path, job_runner) -> None:
    (tmp_path / "data.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path)
    viewer = Viewer(sheet, runner=job_runner)

    df = pl.DataFrame({"value": [1, 2]}).lazy()
    data_sheet = DataSheet(df, runner=job_runner)
    viewer.replace_sheet(data_sheet)

    assert viewer.width_mode_state["mode"] == "default"
    assert viewer.maximized_column_index is None


def test_file_browser_refresh_detects_directory_changes(tmp_path: Path) -> None:
    (tmp_path / "alpha.csv").write_text("a\n1\n")
    sheet = _create_sheet(tmp_path)

    # No changes yet
    assert sheet.refresh_from_disk() is False

    beta = tmp_path / "beta.csv"
    beta.write_text("b\n2\n")

    assert sheet.refresh_from_disk() is True
    names = [sheet.value_at(idx, "name") for idx in range(sheet.row_count() or 0)]
    assert "beta.csv" in names

    sizes_snapshot = [sheet.value_at(idx, "size") for idx in range(sheet.row_count() or 0)]

    # Re-running without touching the filesystem should report no change
    assert sheet.refresh_from_disk() is False

    alpha = tmp_path / "alpha.csv"
    alpha.write_text("a\n1\n2\n")

    assert sheet.refresh_from_disk() is True
    sizes = [sheet.value_at(idx, "size") for idx in range(sheet.row_count() or 0)]
    assert sizes != sizes_snapshot

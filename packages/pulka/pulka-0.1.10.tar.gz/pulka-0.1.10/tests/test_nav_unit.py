"""
Unit tests for navigation commands.

This module tests individual navigation operations like down/up clamping,
page up/down by viewport, gg/G, gh/gl, and z centering.
"""

from __future__ import annotations

import os
import re

import polars as pl
import pytest

from pulka.session import SessionRunner
from pulka.testing.data import make_df, write_df

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(value: str) -> str:
    """Remove ANSI escape sequences from ``value`` for assertions."""

    return ANSI_RE.sub("", value)


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment."""
    os.environ["PULKA_TEST"] = "1"
    os.environ["TZ"] = "UTC"
    os.environ["LC_ALL"] = "C"


@pytest.fixture
def test_data_file(tmp_path):
    """Create a test data file."""
    df = make_df("mini_nav", rows=40, cols=6, seed=42)
    data_file = tmp_path / "test_nav.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


@pytest.fixture
def wide_data_file(tmp_path):
    """Create a wider test dataset to stress horizontal scrolling."""
    df = make_df("mini_nav", rows=40, cols=14, seed=99)
    data_file = tmp_path / "test_nav_wide.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_down_movement_clamping(test_data_file):
    """Test that down movement properly clamps at the bottom."""
    result = SessionRunner.run(
        test_data_file,
        ["down", "down", "down"],  # Move down a few times
        width=80,
        height=10,
        test_mode=True,
    )

    # Check that cursor moved down
    assert result.state_json["cursor_row"] == 3
    assert result.state_json["cursor_col"] == 0


def test_down_movement_bottom_clamp(test_data_file):
    """Test that down movement clamps at the bottom of the dataset."""
    # Try to move beyond the bottom
    commands = ["G", "down", "down", "down"]  # Go to bottom, then try to go further
    result = SessionRunner.run(test_data_file, commands, width=80, height=10, test_mode=True)

    # Should be at the last row (39 for 40-row dataset)
    assert result.state_json["cursor_row"] == 39


def test_up_movement_clamping(test_data_file):
    """Test that up movement properly clamps at the top."""
    result = SessionRunner.run(
        test_data_file,
        ["down", "down", "down", "up", "up"],  # Move down then back up
        width=80,
        height=10,
        test_mode=True,
    )

    # Should be at row 1
    assert result.state_json["cursor_row"] == 1


def test_up_movement_top_clamp(test_data_file):
    """Test that up movement clamps at the top of the dataset."""
    result = SessionRunner.run(
        test_data_file,
        ["up", "up", "up"],  # Try to move above top
        width=80,
        height=10,
        test_mode=True,
    )

    # Should be at row 0
    assert result.state_json["cursor_row"] == 0


def test_page_down_movement(test_data_file):
    """Test page down moves by viewport height."""
    viewport_height = 10
    result = SessionRunner.run(
        test_data_file, ["pagedown"], width=80, height=viewport_height, test_mode=True
    )

    # Should move down by approximately viewport height (accounting for headers/status)
    # Actual viewport rows = height - 5 = 10 - 5 = 5
    expected_viewport_rows = max(1, viewport_height - 5)
    assert result.state_json["cursor_row"] == expected_viewport_rows


def test_page_up_movement(test_data_file):
    """Test page up moves by viewport height."""
    viewport_height = 10
    result = SessionRunner.run(
        test_data_file,
        ["pagedown", "pagedown", "pageup"],  # Go down then back up
        width=80,
        height=viewport_height,
        test_mode=True,
    )

    # Should be somewhere in the middle after page up
    assert 5 <= result.state_json["cursor_row"] <= 15


def test_gg_top_navigation(test_data_file):
    """Test gg command goes to top."""
    result = SessionRunner.run(
        test_data_file,
        ["down", "down", "down", "gg"],  # Move down then go to top
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_row"] == 0
    assert result.state_json["top_row"] == 0


def test_g_bottom_navigation(test_data_file):
    """Test G command goes to bottom."""
    result = SessionRunner.run(test_data_file, ["G"], width=80, height=10, test_mode=True)

    # Should be at the last row
    assert result.state_json["cursor_row"] == 39  # 40 rows, 0-indexed


def test_gg_top_without_echo(test_data_file):
    """Ensure gg jumps instantly and doesn't echo the pressed key."""
    result = SessionRunner.run(
        test_data_file,
        ["G", "gg"],
        width=80,
        height=10,
        test_mode=True,
    )

    first_line = result.frames[-1].splitlines()[0]
    assert not first_line.startswith("g")
    assert result.state_json["cursor_row"] == 0


def test_gh_first_column(test_data_file):
    """Test gh command goes to first column."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "right", "gh"],  # Move right then go to first
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0


def test_gl_last_column(test_data_file):
    """Test gl command goes to last column."""
    result = SessionRunner.run(test_data_file, ["gl"], width=80, height=10, test_mode=True)

    # Should be at the last column (5 for 6-column dataset)
    assert result.state_json["cursor_col"] == 5


def test_slide_column_left_command(test_data_file):
    """H should slide the current column one slot to the left."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "H"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 1
    assert result.state_json["col_order"][:3] == ["col_00", "col_02", "col_01"]


def test_slide_column_right_command(test_data_file):
    """L should slide the current column one slot to the right."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "L"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 2
    assert result.state_json["col_order"][:3] == ["col_00", "col_02", "col_01"]


def test_slide_column_to_left_edge(test_data_file):
    """gH should move the active column to the far left."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "right", "gH"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0
    assert result.state_json["col_order"][:4] == ["col_03", "col_00", "col_01", "col_02"]


def test_slide_column_to_right_edge(test_data_file):
    """gL should move the active column to the far right."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "gL"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["col_order"][-1] == "col_02"
    assert result.state_json["cursor_col"] == len(result.state_json["col_order"]) - 1


def test_slide_column_to_right_edge_scrolls_view(wide_data_file):
    """gL should keep the moved column selected and visible."""
    result = SessionRunner.run(
        wide_data_file,
        ["right", "right", "gL"],
        width=20,
        height=10,
        test_mode=True,
    )

    total_cols = pl.read_parquet(wide_data_file).width
    cursor_col = result.state_json["cursor_col"]
    left_col = result.state_json["left_col"]
    visible_cols = result.state_json["n_cols"]
    assert total_cols > visible_cols
    assert cursor_col == total_cols - 1
    assert left_col > 0
    assert cursor_col == left_col + max(visible_cols - 1, 0)


def test_slide_column_skips_hidden_columns(test_data_file):
    """Sliding should consider only visible columns when reordering."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "hide", "H"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["col_order"][:2] == ["col_02", "col_00"]


def test_gv_unhides_all_columns(test_data_file):
    """gv should restore all columns hidden via '-'."""

    result = SessionRunner.run(
        test_data_file,
        ["-", "gv"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_cols"] == 6
    assert result.state_json["col_order"][:6] == [
        "col_00",
        "col_01",
        "col_02",
        "col_03",
        "col_04",
        "col_05",
    ]


def test_right_left_movement(test_data_file):
    """Test right and left movement with clamping."""
    result = SessionRunner.run(
        test_data_file, ["right", "right", "left"], width=80, height=10, test_mode=True
    )

    assert result.state_json["cursor_col"] == 1


def test_right_movement_clamp(test_data_file):
    """Test right movement clamps at last column."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "right", "right", "right", "right", "right"],  # Move beyond end
        width=80,
        height=10,
        test_mode=True,
    )

    # Should clamp at last column (5 for 6-column dataset)
    assert result.state_json["cursor_col"] == 5


def test_left_movement_clamp(test_data_file):
    """Test left movement clamps at first column."""
    result = SessionRunner.run(
        test_data_file,
        ["left", "left", "left"],  # Try to move before first column
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["cursor_col"] == 0


def test_multiple_navigation_commands(test_data_file):
    """Test a sequence of navigation commands."""
    result = SessionRunner.run(
        test_data_file,
        ["down", "right", "down", "right", "up", "left"],
        width=80,
        height=10,
        test_mode=True,
    )

    # Final position should be row 1, col 1
    assert result.state_json["cursor_row"] == 1
    assert result.state_json["cursor_col"] == 1


@pytest.mark.parametrize(
    "command,expected_change",
    [
        ("down", (1, 0)),  # Move down 1 row
        ("up", (0, 0)),  # Can't move up from top
        ("right", (0, 1)),  # Move right 1 column
        ("left", (0, 0)),  # Can't move left from leftmost
    ],
)
def test_individual_navigation_commands(test_data_file, command, expected_change):
    """Test individual navigation commands from starting position."""
    result = SessionRunner.run(test_data_file, [command], width=80, height=10, test_mode=True)

    expected_row, expected_col = expected_change
    assert result.state_json["cursor_row"] == expected_row
    assert result.state_json["cursor_col"] == expected_col


def test_headless_invalid_filter_reports_status(test_data_file):
    """Invalid filter expressions should surface as status messages and continue."""

    result = SessionRunner.run(
        test_data_file,
        ["filter c.col_00 >", "down"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert len(result.frames) >= 2
    status_line = strip_ansi(result.frames[1]).lower()
    assert "filter e" in status_line
    assert "nvalid filter syntax" in status_line
    assert result.state_json["cursor_row"] == 1


SQL_SUPPORTED = getattr(pl, "SQLContext", None) is not None


@pytest.mark.skipif(not SQL_SUPPORTED, reason="Polars SQL support not available")
def test_headless_invalid_sql_filter_reports_status(test_data_file):
    """Invalid SQL filters should report errors without aborting the script."""

    result = SessionRunner.run(
        test_data_file,
        ["sql_filter bad syntax", "down"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert len(result.frames) >= 2
    status_line = strip_ansi(result.frames[1]).lower()
    assert "sql filter err" in status_line
    assert result.state_json["cursor_row"] == 1


def test_filter_value_appends_current_cell(test_data_file):
    """'+' should append an equality filter for the active cell's value."""

    result = SessionRunner.run(
        test_data_file,
        ["filter c.col_00 > 10", "down", "right", "+"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 5


def test_filter_value_handles_nulls(test_data_file):
    """'+' should append a filter when the focused value is null."""

    result = SessionRunner.run(
        test_data_file,
        ["down", "down", "down", "down", "down", "right", "+"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 6


def test_filter_value_not_excludes_current_cell(test_data_file):
    """'-' should append a negative filter for the active cell's value."""

    result = SessionRunner.run(
        test_data_file,
        ["-"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 39


def test_filter_value_not_handles_nulls(test_data_file):
    """'-' should exclude null values when focused on a null cell."""

    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "-"],
        width=80,
        height=10,
        test_mode=True,
    )

    assert result.state_json["n_rows"] == 34

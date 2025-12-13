"""
End-to-end navigation tests.

This module tests complete navigation workflows including rows flow
and columns flow scenarios as described in the testing plan.
"""

from __future__ import annotations

import os

import pytest

from pulka.session import SessionRunner
from pulka.testing.data import make_df, write_df


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
    data_file = tmp_path / "test_e2e.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


@pytest.fixture
def wide_data_file(tmp_path):
    """Create a wide test data file."""
    df = make_df("wide_datatypes", rows=5, cols=15, seed=123)
    data_file = tmp_path / "test_e2e_wide.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_rows_flow_navigation(test_data_file):
    """
    Test complete rows navigation flow:
    open → many down → PgDn → G → gg → quit
    """
    # Execute the complete flow
    commands = [
        "down",
        "down",
        "down",
        "down",
        "down",  # Move down several times
        "pagedown",  # Page down
        "G",  # Go to bottom
        "gg",  # Go to top
        "quit",  # Quit (should terminate)
    ]

    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    # Verify the final state
    final_state = result.state_json

    # After gg, should be at top
    assert final_state["cursor_row"] == 0
    assert final_state["top_row"] == 0

    # Should still be at first column
    assert final_state["cursor_col"] == 0

    # Check that we have frames from the entire flow
    assert len(result.frames) >= len(commands)

    # The final frame should contain the table at the top position
    final_frame = result.last_frame_str
    assert len(final_frame) > 0
    # Should contain the table header and first data rows
    assert "col_00" in final_frame  # First column header


def test_rows_flow_without_quit(test_data_file):
    """
    Test rows navigation flow without quit command to verify state.
    """
    commands = [
        "down",
        "down",
        "down",
        "down",
        "down",  # Move down several times
        "pagedown",  # Page down
        "G",  # Go to bottom
        "gg",  # Go to top
    ]

    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    # Verify navigation worked correctly
    final_state = result.state_json

    # Should end up at the top after gg
    assert final_state["cursor_row"] == 0
    assert final_state["top_row"] == 0
    assert final_state["cursor_col"] == 0


def test_cols_flow_navigation(wide_data_file):
    """
    Test complete columns navigation flow:
    open wide → move right until scroll → gl → quit
    """
    # This test uses wide data with 20 columns
    commands = [
        "right",
        "right",
        "right",
        "right",
        "right",  # Move right 5 times
        "right",
        "right",
        "right",
        "right",
        "right",  # Move right 5 more times
        "right",
        "right",
        "right",
        "right",
        "right",  # Move right to trigger scroll
        "gl",  # Go to last column
        "quit",  # Quit
    ]

    result = SessionRunner.run(wide_data_file, commands, width=80, height=20, test_mode=True)

    final_state = result.state_json

    # After gl, should be at the last column (14 for 15-column dataset)
    assert final_state["cursor_col"] == 14

    # Should have some visible columns (exact count depends on viewport width)
    assert final_state["n_cols"] > 0
    # When at the last column with horizontal scrolling, we should see fewer than total columns
    assert final_state["n_cols"] <= 15

    # Check that the final frame shows we're at the rightmost position
    final_frame = result.last_frame_str
    assert len(final_frame) > 0


def test_cols_flow_without_quit(wide_data_file):
    """
    Test columns navigation flow without quit to verify final state.
    """
    commands = [
        "right",
        "right",
        "right",
        "right",
        "right",  # Move right several times
        "right",
        "right",
        "right",
        "right",
        "right",
        "gl",  # Go to last column
    ]

    result = SessionRunner.run(wide_data_file, commands, width=80, height=20, test_mode=True)

    final_state = result.state_json

    # Should be at the last column
    assert final_state["cursor_col"] == 14  # 15 columns, 0-indexed
    assert final_state["cursor_row"] == 0  # Should still be at first row


def test_mixed_navigation_flow(test_data_file):
    """Test mixed row and column navigation."""
    commands = [
        "down",
        "down",
        "right",
        "right",  # Move to (2, 2)
        "pagedown",  # Page down
        "left",  # Move left
        "G",  # Go to bottom
        "gh",  # Go to first column
        "gg",  # Go to top
    ]

    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    final_state = result.state_json

    # Should end up at (0, 0) after gg and gh
    assert final_state["cursor_row"] == 0
    assert final_state["cursor_col"] == 0
    assert final_state["top_row"] == 0


def test_boundary_navigation_flow(test_data_file):
    """Test navigation at boundaries."""
    commands = [
        "up",
        "up",
        "up",  # Try to go above top (should clamp)
        "left",
        "left",
        "left",  # Try to go left of first column (should clamp)
        "G",  # Go to bottom
        "down",
        "down",
        "down",  # Try to go below bottom (should clamp)
        "gl",  # Go to last column
        "right",
        "right",
        "right",  # Try to go right of last column (should clamp)
    ]

    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    final_state = result.state_json

    # Should be at bottom-right corner
    assert final_state["cursor_row"] == 39  # Last row (40 rows, 0-indexed)
    assert final_state["cursor_col"] == 5  # Last column (6 columns, 0-indexed)


def test_page_navigation_flow(test_data_file):
    """Test page-based navigation flow."""
    commands = [
        "pagedown",  # First page down
        "pagedown",  # Second page down
        "pagedown",  # Third page down
        "pageup",  # Page up
        "pageup",  # Page up again
        "gg",  # Go to top
    ]

    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    final_state = result.state_json

    # Should be back at the top
    assert final_state["cursor_row"] == 0
    assert final_state["top_row"] == 0


def test_exit_code_verification(test_data_file):
    """Test that navigation commands execute successfully."""
    commands = ["down", "right", "pagedown", "G", "gg", "quit"]

    # This should not raise any exceptions
    result = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    # Should have executed all commands
    assert len(result.frames) >= len(commands)

    # Final state should be valid
    assert isinstance(result.state_json, dict)
    assert "cursor_row" in result.state_json
    assert "cursor_col" in result.state_json


def test_viewport_scrolling_flow(test_data_file):
    """Test that viewport scrolls correctly with navigation."""
    # Use a smaller viewport to force scrolling
    commands = [
        "down",
        "down",
        "down",
        "down",
        "down",  # Move down past viewport
        "pagedown",  # Page down to trigger viewport scroll
    ]

    result = SessionRunner.run(
        test_data_file,
        commands,
        width=80,
        height=5,  # Small height to force scrolling
        test_mode=True,
    )

    final_state = result.state_json

    # With small viewport, top_row should have adjusted
    assert final_state["top_row"] > 0 or final_state["cursor_row"] >= 4

    # Cursor should be in a valid position
    assert 0 <= final_state["cursor_row"] < 40
    assert 0 <= final_state["cursor_col"] < 6

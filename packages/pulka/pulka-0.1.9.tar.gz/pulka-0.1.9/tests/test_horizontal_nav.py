"""
Comprehensive tests for horizontal navigation behavior.

These tests verify that horizontal navigation (right/left) follows the expected behavior:
- When moving right, cursor stays on same columns until reaching the rightmost visible column
- Once on rightmost visible column, continuing right shifts viewport one column at a time
- Cursor always remains visible on screen
- No jumps in column progression - all columns are visited in order
"""

from __future__ import annotations

import os

import polars as pl
import pytest

from pulka.api.session import Session
from pulka.session import SessionRunner
from pulka.testing.data import make_df, write_df


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment."""
    os.environ["PULKA_TEST"] = "1"
    os.environ["TZ"] = "UTC"
    os.environ["LC_ALL"] = "C"


@pytest.fixture
def wide_data_file(tmp_path):
    """Create a wide test data file with many columns."""
    # Create a dataset with 20 columns - more than can fit on screen
    df = make_df("wide_datatypes", rows=10, cols=20, seed=42)
    data_file = tmp_path / "test_horizontal_nav.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


@pytest.fixture
def frozen_challenge_file(tmp_path):
    """Create a dataset with wide headers to stress frozen column layouts."""
    data = {
        f"frozen_{i:02d}_xxxxxxxxxxxxxxxxxxxx": pl.Series([f"value_{i}_with_extra_width"])
        for i in range(12)
    }
    df = pl.DataFrame(data)
    data_file = tmp_path / "freeze_challenge.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_right_movement_within_viewport(wide_data_file):
    """Test right movement when cursor is not yet on rightmost visible column."""
    # Move right a few times while staying within initial viewport
    commands = ["right", "right", "right"]
    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,  # Narrow width to limit visible columns
        height=10,
        test_mode=True,
    )

    state = result.state_json
    # Should have moved right 3 columns
    assert state["cursor_col"] == 3
    # Viewport should not have shifted yet (left_col should still be 0)
    assert state["left_col"] == 0


def test_right_movement_viewport_shift(wide_data_file):
    """Test that viewport shifts when cursor reaches rightmost visible column."""
    # Move right enough times to reach the rightmost visible column, then continue
    # With width=80, we can fit about 5-6 columns typically
    commands = ["right"] * 10  # Move right 10 times to force viewport shift

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,  # Narrow width to force scrolling
        height=10,
        test_mode=True,
    )

    state = result.state_json

    # Should have moved to column 10
    assert state["cursor_col"] == 10
    # Viewport should have shifted to keep cursor visible
    # left_col should be > 0 to keep cursor visible
    assert state["left_col"] > 0

    # Verify cursor is still visible in viewport
    visible_cols = state.get("visible_cols", [])
    current_col_name = state.get("current_col_name", "")
    if visible_cols and current_col_name:
        assert current_col_name in visible_cols


def test_sequential_column_progression(wide_data_file):
    """Test that all columns are visited in order without jumps."""
    # Track cursor position after each right movement
    cursor_positions = []

    # Test moving right 14 times (to cover all columns)
    for i in range(14):
        commands = ["right"] * (i + 1)
        result = SessionRunner.run(
            wide_data_file,
            commands,
            width=80,
            height=10,
            test_mode=True,
        )
        cursor_positions.append(result.state_json["cursor_col"])

    # Verify progression is sequential (no jumps)
    for i in range(1, len(cursor_positions)):
        # Each position should be exactly 1 more than the previous
        assert cursor_positions[i] == cursor_positions[i - 1] + 1, (
            f"Jump detected: position {i - 1} was {cursor_positions[i - 1]}, "
            f"position {i} is {cursor_positions[i]}"
        )


def test_right_movement_stops_at_last_column(wide_data_file):
    """Test that right movement stops at the last column."""
    # Move right many times - should stop at last column (14 for 15-column dataset)
    commands = ["right"] * 25  # More than the number of columns

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,
        height=10,
        test_mode=True,
    )

    state = result.state_json

    # Should stop at the last column (14 for 15-column dataset, 0-indexed)
    assert state["cursor_col"] == 14
    # Additional right movements should not move cursor further

    # Test one more right movement - should stay at same position
    commands_extra = ["right"] * 26
    result_extra = SessionRunner.run(
        wide_data_file,
        commands_extra,
        width=80,
        height=10,
        test_mode=True,
    )

    assert result_extra.state_json["cursor_col"] == 14  # Should still be at last column


def test_left_movement_basic(wide_data_file):
    """Test basic left movement."""
    # Move right then left
    commands = ["right", "right", "right", "left"]

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,
        height=10,
        test_mode=True,
    )

    state = result.state_json
    # Should be at column 2 (moved right 3, then left 1)
    assert state["cursor_col"] == 2


def test_left_movement_stops_at_first_column(wide_data_file):
    """Test that left movement stops at the first column."""
    # Try to move left from the start - should stay at column 0
    commands = ["left", "left", "left"]

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,
        height=10,
        test_mode=True,
    )

    state = result.state_json
    assert state["cursor_col"] == 0


def test_right_then_left_full_cycle(wide_data_file):
    """Test moving right to the end, then left back to the start."""
    # Move right to the end
    commands_right = ["right"] * 25  # More than number of columns
    # Then move left back to start
    commands_left = ["left"] * 25
    commands = commands_right + commands_left

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,
        height=10,
        test_mode=True,
    )

    state = result.state_json
    # Should be back at the first column
    assert state["cursor_col"] == 0
    # And viewport should be back at the start
    assert state["left_col"] == 0


def test_freeze_columns_scroll_does_not_snap_back(frozen_challenge_file):
    """Ensure frozen columns don't force viewport to jump back when scrolling right."""

    left_cols: list[int] = []
    cursor_positions: list[int] = []
    commands_base = ["freeze c3"]

    for steps in range(1, 7):
        commands = commands_base + ["right"] * steps
        result = SessionRunner.run(
            frozen_challenge_file,
            commands,
            width=80,
            height=10,
            test_mode=True,
        )
        state = result.state_json
        left_cols.append(state["left_col"])
        cursor_positions.append(state["cursor_col"])

    first_scrollable = 3

    # The viewport should never scroll left of the first scrollable column
    assert all(col >= first_scrollable for col in left_cols)

    # Horizontal scroll should progress monotonically as we move right
    for prev, cur in zip(left_cols, left_cols[1:], strict=False):
        assert cur >= prev

    # After enough right moves, the viewport must advance past the frozen boundary
    assert left_cols[-1] > first_scrollable

    # Cursor progression should remain sequential
    for idx, expected in enumerate(range(1, 7), start=0):
        assert cursor_positions[idx] == expected


def _frozen_column_widths(session: Session) -> list[int]:
    viewer = session.viewer
    # Access visible columns to ensure autosize state is in sync with current viewport.
    _ = viewer.visible_cols
    autosized = getattr(viewer, "_autosized_widths", {})
    widths: list[int] = []
    for name in viewer.frozen_columns:
        idx = viewer.columns.index(name)
        widths.append(autosized.get(idx, viewer._header_widths[idx]))
    return widths


def test_frozen_column_widths_remain_constant_while_scrolling(frozen_challenge_file):
    """Frozen panes should keep their width while the scrollable region advances."""

    session = Session(frozen_challenge_file, viewport_rows=5, viewport_cols=None)
    viewer = session.viewer
    viewer.set_view_width_override(80)
    viewer.update_terminal_metrics()
    viewer.view_width_chars = 80
    viewer._visible_key = None

    # Prime layout with an initial render using the fixed width, mirroring SessionRunner.
    session.render(include_status=True)
    viewer.set_view_width_override(None)

    session.run_script(["freeze c3"], auto_render=True)
    baseline = _frozen_column_widths(session)
    assert baseline, "Expected frozen columns after applying freeze command"

    # Scroll through several columns and ensure the frozen widths never change.
    for _ in range(6):
        session.run_script(["right"], auto_render=True)
        assert _frozen_column_widths(session) == baseline


def test_viewport_follows_cursor_right(wide_data_file):
    """Test that viewport properly follows cursor when moving right."""
    # Move right significantly to trigger viewport shifts
    commands = ["right"] * 12

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=60,  # Smaller width to force more scrolling
        height=10,
        test_mode=True,
    )

    state = result.state_json
    cursor_col = state["cursor_col"]
    left_col = state["left_col"]
    visible_cols = state.get("visible_cols", [])

    # Cursor should always be visible
    if visible_cols:
        # Find cursor column name
        all_cols = [f"col_{i:02d}" for i in range(20)]  # Expected column names
        cursor_col_name = all_cols[cursor_col] if cursor_col < len(all_cols) else ""
        if cursor_col_name:
            assert cursor_col_name in visible_cols, (
                f"Cursor column {cursor_col_name} not visible in {visible_cols}"
            )

    # left_col should be positioned to keep cursor visible
    # The cursor should be within reasonable bounds of the viewport
    if len(visible_cols) > 0:
        visible_start_idx = left_col
        visible_end_idx = left_col + len(visible_cols) - 1
        assert visible_start_idx <= cursor_col <= visible_end_idx, (
            f"Cursor at {cursor_col} not in visible range [{visible_start_idx}, {visible_end_idx}]"
        )


def test_viewport_follows_cursor_left(wide_data_file):
    """Test that viewport properly follows cursor when moving left."""
    # First move right significantly, then move left
    commands_right = ["right"] * 14  # Move to last column
    commands_left = ["left"] * 8
    commands = commands_right + commands_left

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=60,
        height=10,
        test_mode=True,
    )

    state = result.state_json
    cursor_col = state["cursor_col"]

    # Should be at column 6 (14 right - 8 left)
    assert cursor_col == 6

    # Cursor should be visible in viewport
    visible_cols = state.get("visible_cols", [])
    if visible_cols:
        col_names = [
            "int8_col",
            "int16_col",
            "int32_col",
            "int64_col",
            "uint32_col",
            "float32_col",
            "float64_col",
            "bool_col",
            "string_col",
            "date_col",
            "datetime_col",
            "duration_col",
            "binary_col",
            "categorical_col",
            "decimal_col",
        ]
        cursor_col_name = col_names[cursor_col] if cursor_col < len(col_names) else ""
        if cursor_col_name:
            assert cursor_col_name in visible_cols


def test_narrow_viewport_scrolling(wide_data_file):
    """Test horizontal scrolling with a very narrow viewport."""
    # Use very narrow width to force single-column view
    commands = ["right"] * 5

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=20,  # Very narrow - should fit only one column
        height=10,
        test_mode=True,
    )

    state = result.state_json

    # Should be at column 5
    assert state["cursor_col"] == 5

    # With narrow width, left_col should have shifted to keep cursor visible
    assert state["left_col"] <= state["cursor_col"]


def test_wide_viewport_no_scrolling(wide_data_file):
    """Test that wide viewport doesn't scroll unnecessarily."""
    # Use very wide viewport that can fit all columns
    commands = ["right"] * 10

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=200,  # Very wide - should fit many columns
        height=10,
        test_mode=True,
    )

    state = result.state_json

    # Should be at column 10
    assert state["cursor_col"] == 10

    # With wide viewport, left_col might not need to shift
    # (depends on column widths, but shouldn't shift aggressively)
    visible_cols = state.get("visible_cols", [])
    if len(visible_cols) >= 11:  # If viewport can fit 11+ columns
        # Viewport shouldn't need to shift much
        assert state["left_col"] <= 10


@pytest.mark.parametrize("num_moves", [1, 3, 7, 12, 14])
def test_cursor_visibility_after_moves(wide_data_file, num_moves):
    """Test that cursor remains visible after any number of right moves."""
    commands = ["right"] * num_moves

    result = SessionRunner.run(
        wide_data_file,
        commands,
        width=80,
        height=10,
        test_mode=True,
    )

    state = result.state_json
    cursor_col = state["cursor_col"]
    visible_cols = state.get("visible_cols", [])

    # Cursor should be at expected position
    expected_col = min(num_moves, 14)  # Can't go beyond last column (14)
    assert cursor_col == expected_col

    # Cursor should be visible
    if visible_cols:
        # Get actual column names from the dataset
        col_names = [
            "int8_col",
            "int16_col",
            "int32_col",
            "int64_col",
            "uint32_col",
            "float32_col",
            "float64_col",
            "bool_col",
            "string_col",
            "date_col",
            "datetime_col",
            "duration_col",
            "binary_col",
            "categorical_col",
            "decimal_col",
        ]
        cursor_col_name = col_names[cursor_col] if cursor_col < len(col_names) else ""
        if cursor_col_name:
            assert cursor_col_name in visible_cols, (
                f"After {num_moves} moves, cursor {cursor_col_name} not visible"
            )


def test_consistent_behavior_multiple_sessions(wide_data_file):
    """Test that horizontal navigation is consistent across multiple sessions."""
    # Run the same sequence multiple times and verify consistent results
    commands = ["right"] * 8

    results = []
    for _ in range(3):  # Run 3 times
        result = SessionRunner.run(
            wide_data_file,
            commands,
            width=80,
            height=10,
            test_mode=True,
        )
        results.append(result.state_json)

    # All results should be identical
    for i in range(1, len(results)):
        assert results[i]["cursor_col"] == results[0]["cursor_col"]
        assert results[i]["left_col"] == results[0]["left_col"]

"""
Snapshot tests for UI frames.

This module tests visual output by capturing snapshots of UI frames
in various navigation states and boundary conditions.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pulka.session import SessionRunner
from pulka.testing.data import make_df, write_df


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment for consistent snapshots."""
    os.environ["PULKA_TEST"] = "1"
    os.environ["TZ"] = "UTC"
    os.environ["LC_ALL"] = "C"


@pytest.fixture
def test_data_file(tmp_path):
    """Create a test data file."""
    df = make_df("mini_nav", rows=40, cols=6, seed=42)
    data_file = tmp_path / "test_snapshot.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


@pytest.fixture
def snapshot_dir():
    """Directory for storing snapshots."""
    snapshot_path = Path("tests/snapshots")
    snapshot_path.mkdir(exist_ok=True)
    return snapshot_path


def save_snapshot(snapshot_dir: Path, name: str, content: str):
    """Save a snapshot to disk."""
    snapshot_file = snapshot_dir / f"{name}.txt"
    with snapshot_file.open("w", encoding="utf-8") as f:
        f.write(content)


def load_snapshot(snapshot_dir: Path, name: str) -> str | None:
    """Load a snapshot from disk."""
    snapshot_file = snapshot_dir / f"{name}.txt"
    if snapshot_file.exists():
        with snapshot_file.open(encoding="utf-8") as f:
            return f.read()
    return None


def assert_snapshot_matches(
    snapshot_dir: Path, name: str, actual: str, update_snapshots: bool = False
):
    """Assert that content matches the stored snapshot."""
    if update_snapshots or os.getenv("UPDATE_SNAPSHOTS"):
        save_snapshot(snapshot_dir, name, actual)
        return

    expected = load_snapshot(snapshot_dir, name)
    if expected is None:
        # First time - save the snapshot
        save_snapshot(snapshot_dir, name, actual)
        pytest.skip(f"Created initial snapshot for {name}")

    if actual != expected:
        # Show diff information
        actual_lines = actual.split("\n")
        expected_lines = expected.split("\n")

        print(f"\n=== SNAPSHOT MISMATCH: {name} ===")
        print("EXPECTED:")
        for i, line in enumerate(expected_lines[:10]):  # Show first 10 lines
            print(f"{i:2d}: {repr(line)}")
        print("\nACTUAL:")
        for i, line in enumerate(actual_lines[:10]):
            print(f"{i:2d}: {repr(line)}")
        print("=== END MISMATCH ===\n")

        pytest.fail(f"Snapshot mismatch for {name}")


def test_initial_frame_snapshot(test_data_file, snapshot_dir):
    """Test snapshot of the first frame when opening data."""
    result = SessionRunner.run(
        test_data_file,
        [],  # No commands, just initial state
        width=80,
        height=20,
        test_mode=True,
    )

    # Should have at least one frame (initial render)
    assert len(result.frames) >= 1

    initial_frame = result.frames[0]
    assert_snapshot_matches(snapshot_dir, "initial_frame", initial_frame)


def test_after_down_movement_snapshot(test_data_file, snapshot_dir):
    """Test snapshot after moving cursor down."""
    result = SessionRunner.run(
        test_data_file, ["down", "down", "down"], width=80, height=20, test_mode=True
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "after_down_movement", final_frame)


def test_after_right_movement_snapshot(test_data_file, snapshot_dir):
    """Test snapshot after moving cursor right."""
    result = SessionRunner.run(
        test_data_file, ["right", "right"], width=80, height=20, test_mode=True
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "after_right_movement", final_frame)


def test_bottom_boundary_snapshot(test_data_file, snapshot_dir):
    """Test snapshot at bottom boundary after G command."""
    result = SessionRunner.run(
        test_data_file,
        ["G"],  # Go to bottom
        width=80,
        height=20,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "bottom_boundary", final_frame)


def test_top_boundary_snapshot(test_data_file, snapshot_dir):
    """Test snapshot at top boundary after gg command."""
    result = SessionRunner.run(
        test_data_file,
        ["G", "gg"],  # Go to bottom then top
        width=80,
        height=20,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "top_boundary", final_frame)


def test_left_boundary_snapshot(test_data_file, snapshot_dir):
    """Test snapshot at left boundary after gh command."""
    result = SessionRunner.run(
        test_data_file,
        ["right", "right", "right", "gh"],  # Move right then go to first column
        width=80,
        height=20,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "left_boundary", final_frame)


def test_right_boundary_snapshot(test_data_file, snapshot_dir):
    """Test snapshot at right boundary after gl command."""
    result = SessionRunner.run(
        test_data_file,
        ["gl"],  # Go to last column
        width=80,
        height=20,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "right_boundary", final_frame)


def test_page_down_snapshot(test_data_file, snapshot_dir):
    """Test snapshot after page down."""
    result = SessionRunner.run(test_data_file, ["pagedown"], width=80, height=20, test_mode=True)

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "page_down", final_frame)


def test_small_viewport_snapshot(test_data_file, snapshot_dir):
    """Test snapshot with a small viewport."""
    result = SessionRunner.run(
        test_data_file, ["down", "right"], width=40, height=10, test_mode=True
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "small_viewport", final_frame)


def test_wide_data_horizontal_scroll_snapshot(tmp_path, snapshot_dir):
    """Test snapshot with wide data requiring horizontal scrolling."""
    df = make_df("wide_datatypes", rows=5, cols=15, seed=123)
    wide_data_file = tmp_path / "wide_data.parquet"
    write_df(df, wide_data_file, "parquet")

    result = SessionRunner.run(
        str(wide_data_file),
        [
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
        ],  # Move right to trigger scroll
        width=52,  # Narrow width to force scrolling and partial column
        height=15,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "wide_data_horizontal_scroll", final_frame)


def test_navigation_sequence_snapshot(test_data_file, snapshot_dir):
    """Test snapshot after a complex navigation sequence."""
    result = SessionRunner.run(
        test_data_file,
        ["down", "down", "right", "pagedown", "left", "up"],
        width=80,
        height=20,
        test_mode=True,
    )

    final_frame = result.last_frame_str
    assert_snapshot_matches(snapshot_dir, "navigation_sequence", final_frame)

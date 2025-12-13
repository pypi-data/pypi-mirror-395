"""
Determinism canary test.

This test ensures that rendering the same frame twice yields identical strings.
This is critical for snapshot testing and reproducible test results.
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
    df = make_df("mini_nav", rows=10, cols=3, seed=42)
    data_file = tmp_path / "canary.parquet"
    write_df(df, data_file, "parquet")
    return str(data_file)


def test_deterministic_rendering_canary(test_data_file):
    """
    Test that rendering the same frame twice yields identical strings.

    This is a canary test that will catch any non-deterministic behavior
    in the rendering pipeline.
    """
    commands = ["down", "right"]

    # Render the same commands twice
    result1 = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    result2 = SessionRunner.run(test_data_file, commands, width=80, height=20, test_mode=True)

    # The final frames should be identical
    assert result1.last_frame_str == result2.last_frame_str, (
        "Rendering is not deterministic - same commands produced different output"
    )

    # The state should also be identical
    assert result1.state_json == result2.state_json, (
        "State is not deterministic - same commands produced different state"
    )

    # Frame counts should match
    assert len(result1.frames) == len(result2.frames), "Frame count differs between runs"

    # All frames should be identical
    for i, (frame1, frame2) in enumerate(zip(result1.frames, result2.frames, strict=False)):
        assert frame1 == frame2, f"Frame {i} differs between runs"


def test_deterministic_across_different_commands(test_data_file):
    """
    Test that the same final position produces the same output regardless of path.
    """
    # Two different ways to get to position (1, 1)
    commands1 = ["down", "right"]
    commands2 = ["right", "down"]

    result1 = SessionRunner.run(test_data_file, commands1, width=80, height=20, test_mode=True)

    result2 = SessionRunner.run(test_data_file, commands2, width=80, height=20, test_mode=True)

    # Final state should be the same
    assert result1.state_json["cursor_row"] == result2.state_json["cursor_row"]
    assert result1.state_json["cursor_col"] == result2.state_json["cursor_col"]

    # Final frames should be identical (same position = same display)
    assert result1.last_frame_str == result2.last_frame_str, (
        "Same position produced different visual output"
    )


def test_deterministic_empty_commands(test_data_file):
    """Test that initial state is deterministic."""
    result1 = SessionRunner.run(
        test_data_file,
        [],  # No commands
        width=80,
        height=20,
        test_mode=True,
    )

    result2 = SessionRunner.run(
        test_data_file,
        [],  # No commands
        width=80,
        height=20,
        test_mode=True,
    )

    assert result1.last_frame_str == result2.last_frame_str, "Initial frame is not deterministic"

    assert result1.state_json == result2.state_json, "Initial state is not deterministic"


def test_deterministic_with_different_viewport_sizes(test_data_file):
    """Test that the same viewport size produces deterministic results."""
    commands = ["down", "right", "down"]

    # Same viewport size, should be identical
    result1 = SessionRunner.run(test_data_file, commands, width=60, height=15, test_mode=True)
    result2 = SessionRunner.run(test_data_file, commands, width=60, height=15, test_mode=True)

    assert result1.last_frame_str == result2.last_frame_str
    assert result1.state_json == result2.state_json


if __name__ == "__main__":
    # Allow running this test directly
    pytest.main([__file__, "-v"])

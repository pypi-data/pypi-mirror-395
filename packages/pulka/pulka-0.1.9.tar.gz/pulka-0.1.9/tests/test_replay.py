import json
from unittest.mock import Mock, patch

import pytest

from src.pulka.debug.replay import ReplayState, TUIReplayTool


def test_load_valid_json(tmp_path):
    """Test loading a valid flight recorder JSON file."""
    # Create a temporary JSON file with valid structure
    json_file = tmp_path / "test_session.json"
    json_content = [
        {
            "user_command": "j",
            "viewer_state": {
                "cursor_row": 0,
                "cursor_col": 0,
                "viewport_start_row": 0,
                "viewport_start_col": 0,
                "visible_columns": ["col1", "col2"],
                "status_message": "",
            },
        },
        {
            "user_command": "l",
            "viewer_state": {
                "cursor_row": 0,
                "cursor_col": 1,
                "viewport_start_row": 0,
                "viewport_start_col": 0,
                "visible_columns": ["col1", "col2"],
                "status_message": "",
            },
        },
    ]
    json_file.write_text(str(json_content).replace("'", '"'))

    tool = TUIReplayTool()
    tool.load_session(json_file)

    assert len(tool.session_data) == 2
    assert tool.session_data[0]["user_command"] == "j"
    assert tool.current_step == 0


def test_load_invalid_json(tmp_path):
    """Test handling malformed JSON gracefully."""
    # Create a temporary file with invalid JSON
    json_file = tmp_path / "invalid.json"
    json_file.write_text("{invalid: json}")

    tool = TUIReplayTool()
    with pytest.raises(json.JSONDecodeError):
        tool.load_session(json_file)


def test_state_capture():
    """Test state capture functionality."""
    tool = TUIReplayTool()

    # Mock a viewer to test state capture
    mock_viewer = Mock()
    mock_viewer.cur_row = 5
    mock_viewer.cur_col = 3
    mock_viewer.row0 = 0  # viewport start row
    mock_viewer.col0 = 1  # viewport start col
    mock_viewer.columns = ["col1", "col2", "col3", "col4"]

    # Mock the visible_cols property to return expected columns
    mock_viewer.visible_cols = ["col2", "col3"]

    # Set up the mock viewer to return the expected attributes
    tool.viewer = mock_viewer
    tool.current_step = 2

    # Mock the render functions since they depend on the viewer
    with (
        patch("src.pulka.debug.replay.render_table", return_value="table content"),
        patch("src.pulka.debug.replay.render_status_line_text", return_value="status line"),
        patch(
            "src.pulka.debug.replay.getattr",
            side_effect=lambda obj, attr, default=None: default
            if attr == "status_message"
            else getattr(obj, attr, default),
        ),
    ):
        state = tool.capture_current_state()

        assert isinstance(state, ReplayState)
        assert state.step_index == 2
        assert state.cursor_row == 5
        assert state.cursor_col == 3
        assert state.viewport_start_row == 0
        assert state.viewport_start_col == 1
        # Should get columns from index 1 to 3 (2 columns starting at index 1)
        assert state.visible_columns == ["col2", "col3"]


def test_state_comparison():
    """Test state comparison functionality."""
    tool = TUIReplayTool()

    expected = {
        "cursor_row": 5,
        "cursor_col": 3,
        "viewport_start_row": 0,
        "viewport_start_col": 1,
        "visible_columns": ["col2", "col3"],
        "status_message": "test message",
    }

    actual = ReplayState(
        step_index=0,
        cursor_row=5,
        cursor_col=2,  # Different
        viewport_start_row=0,
        viewport_start_col=0,  # Different
        visible_columns=["col1", "col2"],  # Different
        rendered_output="",
        status_message="different message",  # Different
    )

    differences = tool.compare_states(expected, actual)

    # Should have differences in cursor_col, viewport_start_col, visible_columns, and status_message
    assert len(differences) == 4
    assert "cursor_col" in differences
    assert "viewport_start_col" in differences
    assert "visible_columns" in differences
    assert "status_message" in differences

    # cursor_col: expected=3, actual=2
    assert differences["cursor_col"]["expected"] == 3
    assert differences["cursor_col"]["actual"] == 2


def test_replay_step():
    """Test single step replay."""
    tool = TUIReplayTool()
    tool.session_data = [
        {"user_command": "j", "viewer_state": {}},
        {"user_command": "l", "viewer_state": {}},
    ]

    # This test needs a properly mocked environment to be complete
    # For now, we'll just test the basic flow
    assert tool.current_step == 0

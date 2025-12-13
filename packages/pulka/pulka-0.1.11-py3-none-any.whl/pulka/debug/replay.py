from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ..api import Session
from ..core.viewer import Viewer
from ..render.status_bar import render_status_line_text
from ..render.table import render_table
from ..tui.screen import Screen


@dataclass
class ReplayState:
    """Captured state at a replay step."""

    step_index: int
    cursor_row: int
    cursor_col: int
    viewport_start_row: int
    viewport_start_col: int
    visible_columns: list[str]
    rendered_output: str
    status_message: str


class TUIReplayTool:
    """Tool for replaying flight recorder sessions in TUI."""

    def __init__(self):
        self.session_data: list[dict] = []
        self.current_step: int = 0
        self.viewer: Viewer | None = None
        self.screen: Screen | None = None
        self.session: Session | None = None

    def load_session(self, json_path: Path) -> None:
        """Load flight recorder JSON file."""
        if not json_path.exists():
            raise FileNotFoundError(f"Flight recorder JSON file not found: {json_path}")

        try:
            with json_path.open() as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in flight recorder file: {e}", e.doc, e.pos
            ) from None

        # Basic validation - check if it has the expected structure
        if not isinstance(data, list):
            raise ValueError("Flight recorder file must contain a JSON array")

        for i, record in enumerate(data):
            if not isinstance(record, dict):
                raise ValueError(f"Record {i} is not a JSON object")
            if "user_command" not in record or "viewer_state" not in record:
                raise ValueError(
                    f"Record {i} missing required fields: 'user_command' or 'viewer_state'"
                )

        self.session_data = data
        self.current_step = 0

    def setup_tui(self, data_file: Path) -> None:
        """Initialize TUI components for replay."""
        if not data_file.exists():
            raise FileNotFoundError(f"Data file not found: {data_file}")

        # Create a recorder with recording disabled for replay mode
        from ..logging import Recorder, RecorderConfig

        config = RecorderConfig(enabled=False)  # Disable recording during replay
        recorder = Recorder(config)

        # Create a session with the disabled recorder
        self.session = Session(str(data_file), recorder=recorder)
        self.viewer = self.session.viewer
        # Note: Screen is typically created when running the TUI app,
        # for replay we might not need it or we create a minimal one
        self.screen = (
            self.session.viewer
        )  # Use viewer as placeholder, will be set properly when needed

    def simulate_keypress(self, key: str) -> None:
        """Simulate a single keypress in the TUI."""
        if self.viewer is None:
            raise RuntimeError("TUI not initialized. Call setup_tui() first.")

        # Skip flight recorder toggle key during replay to avoid recursive recording
        if key == "@":
            return

        # Map key presses and commands to appropriate viewer method calls
        if key == "j" or key == "down":
            self.viewer.move_down()
        elif key == "k" or key == "up":
            self.viewer.move_up()
        elif key == "h" or key == "left":
            self.viewer.move_left()
        elif key == "l" or key == "right":
            self.viewer.move_right()
        elif key == " ":
            self.viewer.page_down()
        elif key == "b" or key == "B":  # vi-style page up
            self.viewer.page_up()
        elif key == "g":
            # This would be part of 'gg' sequence, but we handle single 'g' as go to top
            # For true 'gg' detection we'd need sequence tracking
            self.viewer.go_top()
        elif key == "G":
            # Go to bottom
            self.viewer.go_bottom()
        elif key == "$":
            # Move to last visible column
            self.viewer.last_col()
        elif key == "0":
            # Move to first visible column
            self.viewer.first_col()
        elif key == "s":
            # Sort by current column
            self.viewer.toggle_sort()
        elif key == "r":
            # Reset filters - this would involve clearing the filter_text
            self.viewer.filter_text = None
        elif key == "f":
            # For filter, we can't simulate without a filter string
            # Just show a warning or skip
            pass
        elif key == "F":
            # Frequency table - this would change the viewer context
            pass
        elif key == "C":
            # Column summary - this would change the viewer context
            pass
        elif key == "T":
            # Transpose - this would change the viewer context
            pass
        elif key == "?":
            # Schema - this would change the viewer context
            pass
        elif key == "_":
            # Maximize current column
            self.viewer.toggle_maximize_current_col()
        elif key == "g_":
            # Maximize all columns
            self.viewer.toggle_maximize_all_cols()
        elif key == "q":
            # Quit - just ignore in replay mode
            pass
        else:
            # For now, just warn about unhandled keys
            # In a full implementation, we'd want to map all the key bindings
            print(f"Warning: Unhandled key command: {key}")

        # Refresh the viewer after command execution
        # Note: No refresh_needed attribute in Viewer class - the state is immediately updated
        # The viewer state is directly modified by the methods above

        # For screen refresh (if needed), we don't have a real screen in replay mode
        # but we ensure the viewer state is consistent
        self.viewer.clamp()  # Ensure state consistency

    def capture_current_state(self) -> ReplayState:
        """Capture current TUI state."""
        if self.viewer is None:
            raise RuntimeError("TUI not initialized. Call setup_tui() first.")

        # Extract current state from viewer
        cursor_row = self.viewer.cur_row
        cursor_col = self.viewer.cur_col

        # In the viewer class, row0 and col0 represent the viewport start
        viewport_start_row = self.viewer.row0
        viewport_start_col = self.viewer.col0

        # Calculate visible columns using same logic as flight recorder
        visible_columns = self.viewer.visible_cols

        # Capture rendered output
        table_output = render_table(self.viewer)
        status_output = render_status_line_text(self.viewer)
        self.viewer.acknowledge_status_rendered()
        rendered_output = table_output + "\n" + status_output

        # Capture status message if available
        status_message = getattr(self.viewer, "status_message", "")

        return ReplayState(
            step_index=self.current_step,
            cursor_row=cursor_row,
            cursor_col=cursor_col,
            viewport_start_row=viewport_start_row,
            viewport_start_col=viewport_start_col,
            visible_columns=visible_columns,
            rendered_output=rendered_output,
            status_message=status_message,
        )

    def replay_step(self) -> ReplayState:
        """Execute next command and return resulting state."""
        if self.current_step >= len(self.session_data):
            raise IndexError(f"Reached end of session data at step {self.current_step}")

        command_record = self.session_data[self.current_step]
        command = command_record.get("user_command", "")

        # Skip flight recorder toggle commands
        if command == "@":
            self.current_step += 1
            return self.capture_current_state()

        # Execute the command
        self.simulate_keypress(command)

        # Increment step index
        self.current_step += 1

        # Return the resulting state
        return self.capture_current_state()

    def replay_until(self, step: int) -> ReplayState:
        """Replay commands up to specified step."""
        if step > len(self.session_data):
            raise ValueError(
                f"Requested step {step} exceeds session length {len(self.session_data)}"
            )

        # Replay commands from current step to target step
        while self.current_step < step:
            self.replay_step()

        # Return the final state
        return self.capture_current_state()

    def compare_states(self, expected: dict, actual: ReplayState) -> dict:
        """Compare expected vs actual state, return differences."""
        differences = {}

        # Compare each field and collect differences
        if expected.get("cursor_row") != actual.cursor_row:
            differences["cursor_row"] = {
                "expected": expected.get("cursor_row"),
                "actual": actual.cursor_row,
            }

        if expected.get("cursor_col") != actual.cursor_col:
            differences["cursor_col"] = {
                "expected": expected.get("cursor_col"),
                "actual": actual.cursor_col,
            }

        if expected.get("viewport_start_row") != actual.viewport_start_row:
            differences["viewport_start_row"] = {
                "expected": expected.get("viewport_start_row"),
                "actual": actual.viewport_start_row,
            }

        if expected.get("viewport_start_col") != actual.viewport_start_col:
            differences["viewport_start_col"] = {
                "expected": expected.get("viewport_start_col"),
                "actual": actual.viewport_start_col,
            }

        # Compare visible columns (list comparison)
        expected_visible = expected.get("visible_columns", [])
        actual_visible = actual.visible_columns
        if expected_visible != actual_visible:
            differences["visible_columns"] = {
                "expected": expected_visible,
                "actual": actual_visible,
            }

        # Compare status message
        expected_status = expected.get("status_message", "")
        actual_status = actual.status_message
        if expected_status != actual_status:
            differences["status_message"] = {"expected": expected_status, "actual": actual_status}

        return differences

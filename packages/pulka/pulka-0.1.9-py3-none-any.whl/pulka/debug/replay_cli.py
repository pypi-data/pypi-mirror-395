import argparse
import sys
from pathlib import Path

from .replay import TUIReplayTool


def main():
    parser = argparse.ArgumentParser(description="Replay flight recorder session")
    parser.add_argument("json_file", help="Flight recorder JSON file")
    parser.add_argument("data_file", help="Data file to replay against")
    parser.add_argument("--step", "-s", type=int, help="Replay up to specific step")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare with original states")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    replay_tool = TUIReplayTool()

    try:
        replay_tool.load_session(Path(args.json_file))
        replay_tool.setup_tui(Path(args.data_file))
    except Exception as e:
        print(f"Error loading session: {e}", file=sys.stderr)
        sys.exit(1)

    if args.step:
        try:
            final_state = replay_tool.replay_until(args.step)
            print(f"Replayed to step {args.step}")
            print(f"Cursor: ({final_state.cursor_row}, {final_state.cursor_col})")
            viewport_msg = (
                f"Viewport: row_start={final_state.viewport_start_row}, "
                f"col_start={final_state.viewport_start_col}"
            )
            print(viewport_msg)
            print(f"Visible columns: {final_state.visible_columns}")

            if args.compare and args.step <= len(replay_tool.session_data) and args.step > 0:
                # Use the state from the step we just replayed to
                expected = replay_tool.session_data[args.step - 1].get("viewer_state", {})
                differences = replay_tool.compare_states(expected, final_state)
                if differences:
                    print("\n🚨 DIFFERENCES FOUND:")
                    for field, diff in differences.items():
                        print(f"  {field}: expected={diff['expected']}, actual={diff['actual']}")
                else:
                    print("\n✅ State matches original recording")

        except Exception as e:
            print(f"Error during replay: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Replay the entire session
        try:
            step_count = 0
            while replay_tool.current_step < len(replay_tool.session_data):
                state = replay_tool.replay_step()
                step_count += 1
                if args.verbose:
                    print(f"Step {state.step_index}: Command executed, state captured")
            print(f"Replayed entire session ({step_count} steps completed)")
        except Exception as e:
            print(f"Error during replay: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

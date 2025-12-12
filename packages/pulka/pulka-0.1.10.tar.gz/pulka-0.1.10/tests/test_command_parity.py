"""
Test command parity between TUI and headless modes.

This module ensures that all TUI keybindings have corresponding headless commands
and that they use the same command registry.
"""

import re
from pathlib import Path

import pytest

from pulka.command.registry import REGISTRY


def extract_tui_keybindings():
    """Extract all keybinding command names from TUI screen.py."""
    screen_py = Path("src/pulka/tui/screen.py").read_text(encoding="utf-8")

    # Find all _execute_command calls
    execute_command_pattern = r'self\._execute_command\(["\']([^"\']+)["\']'
    registry_execute_pattern = r'REGISTRY\.execute\(["\']([^"\']+)["\']'

    commands = set()

    # Extract from _execute_command calls
    for match in re.finditer(execute_command_pattern, screen_py):
        commands.add(match.group(1))

    # Extract from direct REGISTRY.execute calls (legacy)
    for match in re.finditer(registry_execute_pattern, screen_py):
        commands.add(match.group(1))

    return commands


def extract_headless_commands():
    """Extract all commands supported by headless runner."""
    # Since headless now uses registry exclusively, all registry commands are available
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    # Add special headless-only commands
    headless_special = {"quit", "exit", "q", "help", "render", "print"}

    return registry_commands | headless_special


def test_all_tui_commands_available_in_headless():
    """Ensure every TUI command is available in headless mode."""
    tui_commands = extract_tui_keybindings()
    headless_commands = extract_headless_commands()
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    # All TUI commands should either be in registry or be special cases
    missing_commands = tui_commands - headless_commands - registry_commands

    if missing_commands:
        pytest.fail(
            f"TUI commands not available in headless mode: {missing_commands}\n"
            f"TUI commands: {sorted(tui_commands)}\n"
            f"Headless commands: {sorted(headless_commands)}\n"
            f"Registry commands: {sorted(registry_commands)}"
        )


def test_registry_has_core_commands():
    """Ensure registry contains all expected core commands."""
    registry_commands = {cmd[0] for cmd in REGISTRY.list_commands()}

    expected_commands = {
        # Movement
        "down",
        "up",
        "left",
        "right",
        "pagedown",
        "pageup",
        "top",
        "bottom",
        "first",
        "last",
        "first_overall",
        "last_overall",
        # Data operations
        "sort",
        "filter",
        "filter_value",
        "filter_value_not",
        "reset",
        "goto",
        # Column operations
        "hide",
        "unhide",
        "select_row",
        "select_same_value",
        "undo",
        "redo",
        "maxcol",
        "maxall",
        "schema",
        # Search
        "search",
        "next_diff",
        "prev_diff",
        "search_value_next",
        "search_value_prev",
        # Navigation
        "center",
        "next_different",
        "prev_different",
        # Utility
        "render",
        "repro_export",
        "gv",
    }

    missing_commands = expected_commands - registry_commands

    if missing_commands:
        pytest.fail(
            f"Registry missing expected commands: {missing_commands}\n"
            f"Available commands: {sorted(registry_commands)}"
        )


def test_command_aliases_work():
    """Test that common aliases are properly registered."""
    aliases_to_test = [
        ("?", "schema"),
        ("_", "maxcol"),
        ("g_", "maxall"),
        ("gg", "top"),
        ("G", "bottom"),
        ("0", "first"),
        ("$", "last"),
        ("-", "filter_value_not"),
        ("d", "hide"),
        ("yy", "yank_cell"),
        ("yp", "yank_path"),
        ("yc", "yank_column"),
        ("yac", "yank_all_columns"),
        ("ys", "yank_schema"),
        (",", "select_same_value"),
        ("+", "filter_value"),
        ("*", "search_value_next"),
        ("#", "search_value_prev"),
    ]

    for alias, expected_command in aliases_to_test:
        cmd = REGISTRY.get_command(alias)
        if cmd is None:
            pytest.fail(f"Alias '{alias}' not found in registry")

        # The command name should be the canonical name, not the alias
        assert cmd.name == expected_command, (
            f"Alias '{alias}' should resolve to '{expected_command}', got '{cmd.name}'"
        )


def test_no_direct_viewer_calls_in_tui():
    """Ensure TUI keybindings use registry instead of direct viewer calls."""
    screen_py = Path("src/pulka/tui/screen.py").read_text(encoding="utf-8")

    # Look for patterns that suggest direct viewer method calls in keybindings
    # We'll look for specific patterns that indicate bypassing the registry
    forbidden_patterns = [
        r"self\.viewer\.toggle_sort\(",  # Direct sort calls should use registry
        r"self\.viewer\.go_\w+\(\)",  # Direct navigation calls should use registry
    ]

    violations = []
    for pattern in forbidden_patterns:
        matches = list(re.finditer(pattern, screen_py))
        if matches:
            for match in matches:
                # Get line number for better error reporting
                line_start = screen_py.rfind("\n", 0, match.start()) + 1
                line_num = screen_py.count("\n", 0, line_start) + 1

                # Skip if this is in _apply_pending_moves which is legitimate
                context_start = max(0, line_start - 100)
                context = screen_py[context_start : match.end() + 100]
                if "_apply_pending_moves" in context:
                    continue

                violations.append(f"Line {line_num}: {match.group(0)}")

    if violations:
        pytest.fail(
            "TUI contains direct viewer calls that should use registry:\n" + "\n".join(violations)
        )


def test_headless_runner_uses_registry():
    """Ensure headless runner uses registry for command execution."""
    runner_py = Path("src/pulka/headless/runner.py").read_text(encoding="utf-8")

    # Check that apply_script_command delegates to the session runtime
    assert "session.command_runtime" in runner_py, (
        "Headless runner should use the session-bound command runtime"
    )
    assert "dispatch_raw" in runner_py, (
        "Headless runner should dispatch raw commands through the runtime"
    )
    assert "REGISTRY.bind" not in runner_py, "Headless runner should not bind the global registry"

    # Check that we removed the massive hardcoded command switch
    # The old version had many lines like 'if cmd in {"down", "j"}'
    hardcoded_patterns = [
        r'if cmd in \{["\']down["\']',
        r'if cmd in \{["\']up["\']',
        r'if cmd in \{["\']sort["\']',
    ]

    for pattern in hardcoded_patterns:
        if re.search(pattern, runner_py):
            pytest.fail(f"Found hardcoded command pattern in runner: {pattern}")


if __name__ == "__main__":
    # Run tests manually for debugging
    print("TUI commands:", sorted(extract_tui_keybindings()))
    print("Headless commands:", sorted(extract_headless_commands()))
    print("Registry commands:", sorted({cmd[0] for cmd in REGISTRY.list_commands()}))

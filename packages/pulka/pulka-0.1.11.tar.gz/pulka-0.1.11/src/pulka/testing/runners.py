"""
Testing runners for Pulka.

This module provides entry points for running different types of tests
with proper environment setup and configuration.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def setup_test_environment() -> None:
    """Set up the test environment with consistent settings."""
    # Force test mode
    os.environ["PULKA_TEST"] = "1"
    os.environ["TZ"] = "UTC"
    os.environ["LC_ALL"] = "C"

    # Force no color for consistent output
    os.environ["NO_COLOR"] = "1"
    if "FORCE_COLOR" in os.environ:
        del os.environ["FORCE_COLOR"]

    # Set terminal settings for Rich
    os.environ["TERM"] = "dumb"


def run_pytest(args: list[str]) -> int:
    """Run pytest with the given arguments."""
    setup_test_environment()

    # Ensure we're in the project root
    project_root = Path(__file__).resolve().parents[3]  # Go up from src/pulka/testing/
    os.chdir(project_root)

    # Run pytest
    cmd = [sys.executable, "-m", "pytest"] + args
    return subprocess.call(cmd)


def smoke() -> int:
    """
    Run smoke tests - fast subset of tests to catch basic issues.

    This runs unit tests marked with 'smoke' or a subset of critical tests.
    """
    print("Running smoke tests...")
    args = [
        "-v",
        "--tb=short",
        "-m",
        "not slow",  # Exclude slow tests
        "--maxfail=5",  # Stop after 5 failures
        "tests/test_nav_unit.py",  # Only unit tests for smoke
        "-x",  # Stop on first failure
    ]
    return run_pytest(args)


def all_tests() -> int:
    """
    Run the full test suite (Phase-1).

    This runs unit tests, snapshot tests, and E2E tests.
    """
    print("Running full test suite...")
    args = [
        "-v",
        "--tb=short",
        "tests/test_nav_unit.py",
        "tests/test_nav_snapshot.py",
        "tests/test_nav_e2e.py",
    ]
    return run_pytest(args)


def snapshots() -> int:
    """
    Run only snapshot tests.

    This runs tests that generate and compare UI snapshots.
    """
    print("Running snapshot tests...")
    args = [
        "-v",
        "--tb=short",
        "tests/test_nav_snapshot.py",
    ]
    return run_pytest(args)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "smoke":
            return smoke()
        elif command == "all":
            return all_tests()
        elif command == "snapshots":
            return snapshots()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: smoke, all, snapshots")
            return 1
    else:
        print("Usage: python -m pulka.testing.runners [smoke|all|snapshots]")
        return 1


if __name__ == "__main__":
    sys.exit(main())

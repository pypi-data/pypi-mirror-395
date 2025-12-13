"""Testing utilities for Pulka."""

import locale
import os
from contextlib import suppress


def is_test_mode() -> bool:
    """Check if we're in test mode based on environment variables."""
    return os.getenv("PULKA_TEST") == "1"


def setup_test_environment() -> None:
    """Set up test environment with deterministic settings."""
    if is_test_mode():
        # Force UTC timezone and C locale for determinism
        os.environ["TZ"] = "UTC"
        os.environ["LC_ALL"] = "C"

        # Set locale to C for deterministic output
        with suppress(locale.Error):
            locale.setlocale(locale.LC_ALL, "C")

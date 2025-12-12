"""
TestConsole for capturing single frames in headless mode.

This module provides TestConsole class for capturing rendered output
without requiring a real terminal or stdout interaction.
"""

from __future__ import annotations

import io

from ..utils import lazy_imports

Console = lazy_imports.rich_console_class()


class TestConsole:
    """
    Console replacement for testing that captures output without real stdout.

    This class provides a way to capture rendered frames in a controlled
    environment for testing purposes.
    """

    def __init__(self, width: int = 80, height: int = 20, color: bool = False):
        """
        Initialize TestConsole with specified dimensions.

        Args:
            width: Console width in characters
            height: Console height in lines
            color: Whether to enable color output (False for ASCII-only tests)
        """
        self.width = width
        self.height = height
        self.color = color
        self._buffer = io.StringIO()
        self._console = Console(
            width=width,
            height=height,
            file=self._buffer,
            force_terminal=color,
            color_system="256" if color else None,
            highlight=False,
            legacy_windows=False,
            _environ={} if not color else None,
        )

    def capture_frame(self, content: str) -> str:
        """
        Capture a single frame of content.

        Args:
            content: The content to capture

        Returns:
            Captured frame as string
        """
        # Reset buffer
        self._buffer.seek(0)
        self._buffer.truncate(0)

        # Print content to our console
        self._console.print(content, end="")

        # Get the captured output
        captured = self._buffer.getvalue()
        return captured

    def get_console(self) -> Console:
        """Get the underlying Rich Console instance."""
        return self._console

    def reset(self):
        """Reset the console buffer."""
        self._buffer.seek(0)
        self._buffer.truncate(0)

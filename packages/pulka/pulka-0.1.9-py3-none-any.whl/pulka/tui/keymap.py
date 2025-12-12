"""
Keymap definitions for Pulka TUI.

This module defines key sequences and their command names for the terminal UI.
"""

from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings


class Keymap:
    """Keymap for Pulka TUI."""

    def __init__(self):
        self.key_bindings = KeyBindings()
        self._setup_default_bindings()

    def _setup_default_bindings(self):
        """Setup default key bindings."""
        # Modal state condition
        Condition(lambda: False)  # Placeholder - real condition would check modal state

        # Basic Navigation
        kb = self.key_bindings

        @kb.add("q")
        def _(event):
            """Quit the application."""
            event.app.exit()

        @kb.add("j")
        @kb.add("down")
        def _(event):
            """Move down."""
            # This would call the command registry in real implementation
            pass

        @kb.add("k")
        @kb.add("up")
        def _(event):
            """Move up."""
            pass

        @kb.add("h")
        @kb.add("left")
        def _(event):
            """Move left."""
            pass

        @kb.add("l")
        @kb.add("right")
        def _(event):
            """Move right."""
            pass

        # Page navigation
        @kb.add("pageup")
        def _(event):
            """Page up."""
            pass

        @kb.add("pagedown")
        def _(event):
            """Page down."""
            pass

        # Sorting and filtering
        @kb.add("s")
        def _(event):
            """Sort by current column."""
            pass

        @kb.add("f")
        def _(event):
            """Open filter modal."""
            pass

        @kb.add("r")
        def _(event):
            """Reset filters."""
            pass

        # Column operations
        @kb.add("d")
        def _(event):
            """Hide current column."""
            pass

        @kb.add("u")
        def _(event):
            """Undo last operation."""
            pass

        @kb.add("-")
        def _(event):
            """Append negative filter for current value."""
            pass

"""Utilities for lazily importing optional or layered dependencies.

These helpers keep import sites auditable and make it easy to explain why
higher-level packages (like the TUI) are the only places that touch heavy UI
frameworks. Modules in lower layers should use these helpers instead of direct
imports so Ruff can flag regressions.
"""

from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import Any, cast


def _load_attr(module_path: str, attribute: str) -> Any:
    """Import ``attribute`` from ``module_path`` without a direct import statement."""

    module = import_module(module_path)
    return getattr(module, attribute)


def rich_console_class() -> type[Any]:
    """Return the Rich ``Console`` class."""

    return cast("type[Any]", _load_attr("rich.console", "Console"))


def prompt_toolkit_style_class() -> type[Any]:
    """Return the prompt_toolkit ``Style`` class for theming."""

    return cast("type[Any]", _load_attr("prompt_toolkit.styles", "Style"))


def prompt_toolkit_style_and_text_tuples() -> Any:
    """Return the prompt_toolkit ``StyleAndTextTuples`` alias."""

    return _load_attr("prompt_toolkit.formatted_text", "StyleAndTextTuples")


def prompt_toolkit_create_app_session() -> Callable[..., Any]:
    """Return the prompt_toolkit ``create_app_session`` context manager factory."""

    return cast(
        "Callable[..., Any]",
        _load_attr("prompt_toolkit.application.current", "create_app_session"),
    )


def prompt_toolkit_set_app() -> Callable[[Any], None]:
    """Return the prompt_toolkit ``set_app`` helper."""

    return cast(
        "Callable[[Any], None]",
        _load_attr("prompt_toolkit.application.current", "set_app"),
    )


def prompt_toolkit_dummy_output_class() -> type[Any]:
    """Return the prompt_toolkit ``DummyOutput`` class for headless rendering."""

    return cast("type[Any]", _load_attr("prompt_toolkit.output", "DummyOutput"))


def prompt_toolkit_eventloop_call_soon_threadsafe() -> Callable[[Callable[[], None]], None]:
    """Return the prompt_toolkit ``call_soon_threadsafe`` helper.

    Plugins that need to schedule UI work from background threads should funnel
    through this accessor so we can audit those code paths when tightening
    guardrails.
    """

    return cast(
        "Callable[[Callable[[], None]], None]",
        _load_attr("prompt_toolkit.eventloop", "call_soon_threadsafe"),
    )

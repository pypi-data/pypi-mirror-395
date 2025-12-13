"""Utilities for converting theme styles into ANSI strings."""

from __future__ import annotations

from collections.abc import Sequence

from .style_resolver import StyleComponents, get_active_style_resolver

_ANSI_RESET = "\x1b[0m"


def segments_to_text(
    segments: Sequence[tuple[Sequence[str], str]],
    *,
    test_mode: bool,
) -> str:
    """Render class-tagged segments to ANSI text using the active theme."""

    resolver = get_active_style_resolver()
    parts: list[str] = []
    for classes, text in segments:
        if not text:
            continue
        if test_mode:
            parts.append(text)
            continue
        prefix = resolver.ansi_prefix_for_classes(classes)
        if prefix:
            parts.append(f"{prefix}{text}{_ANSI_RESET}")
        else:
            parts.append(text)
    return "".join(parts)


def apply_style(text: str, style: str | None, *, test_mode: bool) -> str:
    """Apply a theme style string to ``text`` returning ANSI output."""

    if not text:
        return text
    if test_mode or not style:
        return text
    components = StyleComponents.from_style_string(style)
    prefix = components.to_ansi_prefix()
    if not prefix:
        return text
    return f"{prefix}{text}{_ANSI_RESET}"

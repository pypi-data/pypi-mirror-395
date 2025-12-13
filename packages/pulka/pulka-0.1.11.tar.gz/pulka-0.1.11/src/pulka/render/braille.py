"""Shared braille glyphs for inline histograms and sparklines."""

from __future__ import annotations

FILL_CHAR = "\u283f"
SPROUT_CHAR = "\u2807"
FULL_BLOCK_CHAR = "\u28ff"


def render_hist_bar(count: int, max_count: int, width: int) -> str:
    """Return a histogram bar sized to ``width`` using braille glyphs."""

    if width <= 0:
        return ""

    safe_max = max(0, int(max_count))
    safe_count = max(0, int(count))

    if safe_max <= 0:
        if safe_count <= 0:
            return " " * width
        if width == 1:
            return SPROUT_CHAR
        return (SPROUT_CHAR + (" " * (width - 1)))[:width]

    fraction = safe_count / float(safe_max)
    bar_len = int(round(fraction * width))
    bar_len = max(0, min(width, bar_len))

    if safe_count > 0 and bar_len == 0:
        return (SPROUT_CHAR + (" " * (width - 1)))[:width]

    filled = FILL_CHAR * bar_len
    padding = " " * max(0, width - bar_len)
    return (filled + padding)[:width]


__all__ = ["FILL_CHAR", "SPROUT_CHAR", "FULL_BLOCK_CHAR", "render_hist_bar"]

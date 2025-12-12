"""Shared helpers for decimal alignment across table-like renderers."""

from __future__ import annotations

from collections.abc import Sequence

from .display import display_width, pad_left_display


def _clean_integral_chunk(text: str) -> str:
    return text.replace(",", "").replace("_", "")


def _is_integral_chunk(text: str) -> bool:
    if not text:
        return False
    if text[0] in "+-":
        text = text[1:]
    if not text:
        return False
    cleaned = _clean_integral_chunk(text)
    return cleaned.isdigit()


def _is_fractional_chunk(text: str) -> bool:
    if text == "":
        return True
    return text.replace("_", "").isdigit()


def split_decimal_parts(value: str) -> tuple[str, str] | None:
    """Return integer/fractional parts for simple decimal strings."""

    stripped = value.strip()
    if not stripped:
        return None
    lower = stripped.lower()
    if lower in {"nan", "inf", "-inf", "+inf"}:
        return None
    if "e" in stripped or "E" in stripped:
        return None
    if "." in stripped:
        left, _, right = stripped.partition(".")
        if _is_integral_chunk(left) and _is_fractional_chunk(right):
            return left, right
        return None
    if _is_integral_chunk(stripped):
        return stripped, ""
    return None


def compute_decimal_alignment(texts: Sequence[str], inner_width: int) -> tuple[int, int] | None:
    """Return integer and fractional widths to align decimal points."""

    if inner_width <= 0:
        return None

    int_width = 0
    frac_width = 0
    has_fractional = False
    for text in texts:
        parts = split_decimal_parts(text)
        if parts is None:
            continue
        left, right = parts
        int_width = max(int_width, len(left))
        if right:
            frac_width = max(frac_width, len(right))
            has_fractional = True

    if not has_fractional:
        return None

    frac_width = max(frac_width, 1)

    if int_width + 1 + frac_width > inner_width:
        return None
    return int_width, frac_width


def apply_decimal_alignment(text: str, widths: tuple[int, int], inner_width: int) -> str | None:
    """Return ``text`` aligned to the decimal point or ``None`` if not applicable."""

    int_width, frac_width = widths
    parts = split_decimal_parts(text)
    if parts is None:
        return None
    left, right = parts
    right = right if right else "0"
    if len(right) > frac_width:
        right = right[:frac_width]
    int_field = left.rjust(int_width)
    frac_field = right.ljust(frac_width)
    candidate = f"{int_field}.{frac_field}"
    if display_width(candidate) > inner_width:
        return None
    return pad_left_display(candidate, inner_width)


__all__ = [
    "apply_decimal_alignment",
    "compute_decimal_alignment",
    "split_decimal_parts",
]

"""Centralised style resolution for both TUI and ANSI render paths."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ..theme import ThemeConfig

_BASIC_COLOR_CODES: dict[str, tuple[int, int]] = {
    "black": (30, 40),
    "red": (31, 41),
    "green": (32, 42),
    "yellow": (33, 43),
    "blue": (34, 44),
    "magenta": (35, 45),
    "cyan": (36, 46),
    "white": (37, 47),
    "bright_black": (90, 100),
    "bright_red": (91, 101),
    "bright_green": (92, 102),
    "bright_yellow": (93, 103),
    "bright_blue": (94, 104),
    "bright_magenta": (95, 105),
    "bright_cyan": (96, 106),
    "bright_white": (97, 107),
    "gray": (90, 100),
    "grey": (90, 100),
}

_EXTRA_STYLE_CODES: dict[str, str] = {
    "bold": "1",
    "dim": "2",
    "italic": "3",
    "underline": "4",
    "reverse": "7",
}

_resolver_cache: StyleResolver | None = None
_resolver_epoch: int | None = None


@dataclass(frozen=True)
class StyleComponents:
    """Split style attributes into explicit foreground/background/extras."""

    foreground: str | None = None
    background: str | None = None
    extras: tuple[str, ...] = ()

    def merge(self, override: StyleComponents) -> StyleComponents:
        """Return a new instance with ``override`` applied on top of ``self``."""

        fg = override.foreground or self.foreground
        bg = override.background or self.background
        extras = _merge_extras(self.extras, override.extras)
        return StyleComponents(fg, bg, extras)

    def to_prompt_toolkit(self) -> str:
        """Convert the components back into a prompt_toolkit style string."""

        parts: list[str] = []
        if self.foreground:
            parts.append(f"fg:{self.foreground}")
        if self.background:
            parts.append(f"bg:{self.background}")
        parts.extend(self.extras)
        return " ".join(parts)

    def to_ansi_prefix(self) -> str:
        """Return the ANSI escape prefix representing these components."""

        codes: list[str] = []
        if self.foreground:
            fg_code = _color_to_code(self.foreground, foreground=True)
            if fg_code:
                codes.append(fg_code)
        if self.background:
            bg_code = _color_to_code(self.background, foreground=False)
            if bg_code:
                codes.append(bg_code)
        if self.extras:
            seen: set[str] = set()
            for extra in self.extras:
                code = _EXTRA_STYLE_CODES.get(extra.lower())
                if code and code not in seen:
                    codes.append(code)
                    seen.add(code)
        if not codes:
            return ""
        return f"\x1b[{';'.join(codes)}m"

    def is_empty(self) -> bool:
        return not (self.foreground or self.background or self.extras)

    @classmethod
    def from_style_string(cls, value: str | None) -> StyleComponents:
        if not value:
            return cls()
        tokens = value.split()
        fg: str | None = None
        bg: str | None = None
        extras: list[str] = []
        idx = 0
        while idx < len(tokens):
            token = tokens[idx]
            lower = token.lower()
            if lower.startswith("fg:"):
                candidate = token[3:]
                if candidate and candidate.lower() != "default":
                    fg = candidate
                idx += 1
                continue
            if lower.startswith("bg:"):
                candidate = token[3:]
                if candidate and candidate.lower() != "default":
                    bg = candidate
                idx += 1
                continue
            if lower == "on" and idx + 1 < len(tokens):
                candidate = tokens[idx + 1]
                if candidate.lower() != "default":
                    bg = candidate
                idx += 2
                continue
            if fg is None and _is_color_token(token):
                if token.lower() != "default":
                    fg = token
            else:
                if token.lower() != "default":
                    extras.append(token)
            idx += 1
        return cls(fg, bg, tuple(extras))


class StyleResolver:
    """Resolve class-based styles for both prompt_toolkit and ANSI flows."""

    def __init__(self, class_styles: dict[str, StyleComponents]):
        self._class_styles = class_styles
        self._combo_cache: dict[tuple[str, ...], StyleComponents] = {}
        self._prompt_toolkit_rule_cache: dict[str, str] = {}
        for cls_name, components in class_styles.items():
            style_str = components.to_prompt_toolkit()
            if style_str:
                self._prompt_toolkit_rule_cache[cls_name] = style_str

    @classmethod
    def from_theme(cls, config: ThemeConfig) -> StyleResolver:
        """Build a resolver for ``config``."""

        mapping: dict[str, StyleComponents] = {}

        def add(name: str, components: StyleComponents) -> None:
            if not components.is_empty():
                mapping[name] = components

        add("table", StyleComponents.from_style_string(config.table_style))

        header_style = normalize_header_color(config.header_style)
        header_components = StyleComponents.from_style_string(header_style)
        if not header_components.foreground:
            header_components = header_components.merge(StyleComponents(foreground="#ffffff"))
        add("table.header", header_components)

        cell_components = StyleComponents.from_style_string(config.cell_style)
        add("table.cell", cell_components)
        add(
            "table.cell.null",
            StyleComponents.from_style_string(config.cell_null_style),
        )
        add(
            "table.cell.active",
            StyleComponents.from_style_string(config.cell_active_style),
        )
        add(
            "table.row.active",
            StyleComponents.from_style_string(config.row_active_style),
        )
        add(
            "table.row.selected",
            StyleComponents.from_style_string(config.row_selected_style),
        )
        add(
            "table.row.selected.active",
            StyleComponents.from_style_string(config.row_selected_active_style),
        )

        header_active_raw = StyleComponents.from_style_string(config.header_active_style)
        if header_active_raw.is_empty():
            header_active = StyleComponents(extras=("bold",))
        else:
            has_bold = any(extra.lower() == "bold" for extra in header_active_raw.extras)
            header_active = (
                header_active_raw
                if has_bold
                else header_active_raw.merge(StyleComponents(extras=("bold",)))
            )
        add("table.header.active", header_active)
        # Column active shares the colours from the header highlight but drops the bold emphasis.
        col_active = StyleComponents(
            header_active.foreground,
            header_active.background,
            tuple(extra for extra in header_active.extras if extra.lower() != "bold"),
        )
        add("table.col.active", col_active)
        overflow_indicator = header_active
        if overflow_indicator.is_empty():
            overflow_indicator = StyleComponents.from_style_string(config.cell_active_style)
        if overflow_indicator.is_empty():
            overflow_indicator = StyleComponents(extras=("bold",))
        add("table.overflow_indicator", overflow_indicator)

        add(
            "table.border",
            StyleComponents.from_style_string(config.border_style),
        )
        add(
            "table.separator",
            StyleComponents.from_style_string(config.border_style),
        )
        sep_active_color = "#8a8a8a"
        add("table.separator.active", StyleComponents.from_style_string(sep_active_color))
        sorted_indicator = StyleComponents(foreground=sep_active_color)
        add("table.header.sorted", sorted_indicator)

        add("status", StyleComponents.from_style_string(config.status_style))
        add("dialog", StyleComponents.from_style_string(config.dialog_style))

        return cls(mapping)

    def resolve(self, classes: Sequence[str]) -> StyleComponents:
        key = tuple(classes)
        cached = self._combo_cache.get(key)
        if cached is not None:
            return cached

        result = StyleComponents()
        for cls_name in key:
            components = self._class_styles.get(cls_name)
            if components is None:
                continue
            result = result.merge(components)
        self._combo_cache[key] = result
        return result

    def prompt_toolkit_style_for_classes(self, classes: Sequence[str]) -> str:
        return self.resolve(classes).to_prompt_toolkit()

    def ansi_prefix_for_classes(self, classes: Sequence[str]) -> str:
        return self.resolve(classes).to_ansi_prefix()

    def prompt_toolkit_rules(self) -> dict[str, str]:
        return dict(self._prompt_toolkit_rule_cache)


def normalize_header_color(value: str | None) -> str | None:
    """Ensure header foreground colours use bright white when unspecified."""

    if value is None:
        return None
    if value.strip().lower() == "white":
        return "#ffffff"
    return value


def get_active_style_resolver() -> StyleResolver:
    """Return the resolver for the current theme epoch."""

    global _resolver_cache, _resolver_epoch

    from .. import theme

    epoch = theme.theme_epoch()
    if _resolver_cache is None or _resolver_epoch != epoch:
        config = getattr(theme, "THEME", None)
        _resolver_cache = StyleResolver({}) if config is None else StyleResolver.from_theme(config)
        _resolver_epoch = epoch
    return _resolver_cache


def reset_style_resolver_cache() -> None:
    """Clear the cached resolver (testing helper)."""

    global _resolver_cache, _resolver_epoch
    _resolver_cache = None
    _resolver_epoch = None


def _merge_extras(base: tuple[str, ...], override: tuple[str, ...]) -> tuple[str, ...]:
    if not base and not override:
        return ()
    merged: list[str] = []
    seen: set[str] = set()
    for token in (*base, *override):
        lower = token.lower()
        if lower in seen:
            continue
        merged.append(token)
        seen.add(lower)
    return tuple(merged)


def _is_color_token(token: str) -> bool:
    if token.startswith("#"):
        return True
    return token.lower() in _BASIC_COLOR_CODES


def _color_to_code(color: str, *, foreground: bool) -> str | None:
    lower = color.lower()
    if lower in _BASIC_COLOR_CODES:
        fg_code, bg_code = _BASIC_COLOR_CODES[lower]
        return str(fg_code if foreground else bg_code)
    if color.startswith("#"):
        rgb = _hex_to_rgb(color)
        if rgb is None:
            return None
        r, g, b = rgb
        prefix = 38 if foreground else 48
        return f"{prefix};2;{r};{g};{b}"
    return None


def _hex_to_rgb(value: str) -> tuple[int, int, int] | None:
    text = value.lstrip("#")
    if len(text) == 3:
        try:
            r, g, b = (int(ch * 2, 16) for ch in text)
        except ValueError:
            return None
        return r, g, b
    if len(text) == 6:
        try:
            r = int(text[0:2], 16)
            g = int(text[2:4], 16)
            b = int(text[4:6], 16)
        except ValueError:
            return None
        return r, g, b
    return None


__all__ = [
    "StyleComponents",
    "StyleResolver",
    "get_active_style_resolver",
    "normalize_header_color",
    "reset_style_resolver_cache",
]

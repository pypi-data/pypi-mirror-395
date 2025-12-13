from pulka import theme
from pulka.render.style_resolver import (
    get_active_style_resolver,
    reset_style_resolver_cache,
)
from pulka.theme_palettes import apply_palette, list_palettes


def test_list_palettes_exposes_configured_base() -> None:
    palettes = list_palettes()
    assert palettes
    assert palettes[0].key == "0"
    assert palettes[0].overrides == {}


def test_apply_palette_switches_theme_and_updates_styles() -> None:
    original_theme = theme.THEME
    original_epoch = theme.theme_epoch()

    try:
        palette = apply_palette("2")
        assert palette.key == "2"
        assert theme.theme_epoch() != original_epoch
        assert theme.THEME.header_active_style == palette.overrides["header_active_style"]

        reset_style_resolver_cache()
        resolver = get_active_style_resolver()
        components = resolver.resolve(("table.header", "table.header.active"))
        assert components.foreground == "#56cfe1"

        revert = apply_palette("0")
        assert revert.key == "0"
        assert original_theme == theme.THEME
    finally:
        theme.set_theme(original_theme)
        reset_style_resolver_cache()

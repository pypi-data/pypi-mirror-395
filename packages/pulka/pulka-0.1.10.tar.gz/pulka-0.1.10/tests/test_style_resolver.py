from pulka.render.style_resolver import StyleResolver
from pulka.theme import ThemeConfig


def _make_theme(**overrides: str | None) -> ThemeConfig:
    base = {
        "border_style": "#505050",
        "table_style": "default",
        "header_style": "white",
        "header_active_style": "#f06595 bold",
        "cell_style": "#b8b8b8",
        "cell_null_style": "#707070",
        "cell_active_style": "black on #f06595",
        "row_active_style": "on #4a4a4a",
        "row_selected_style": "#63e6be bold",
        "row_selected_active_style": "black on #63e6be",
        "status_style": "white on #3a3a3a",
        "dialog_style": "default",
    }
    base.update(overrides)
    return ThemeConfig(**base)


def test_style_resolver_merges_table_header_styles() -> None:
    resolver = StyleResolver.from_theme(_make_theme())
    components = resolver.resolve(("table", "table.header"))
    assert components.foreground == "#ffffff"

    style_str = resolver.prompt_toolkit_style_for_classes(("table.header",))
    assert "fg:#ffffff" in style_str

    ansi_prefix = resolver.ansi_prefix_for_classes(("table.header",))
    assert "38;2;255;255;255" in ansi_prefix


def test_style_resolver_applies_header_active_fallback() -> None:
    resolver = StyleResolver.from_theme(_make_theme(header_active_style=None))
    components = resolver.resolve(("table.header", "table.header.active"))
    assert "bold" in components.extras

    col_active = resolver.resolve(("table.col.active",))
    assert col_active.extras == ()


def test_column_active_drops_bold_extra() -> None:
    resolver = StyleResolver.from_theme(_make_theme())
    col_active = resolver.resolve(("table.col.active",))
    assert all(extra.lower() != "bold" for extra in col_active.extras)

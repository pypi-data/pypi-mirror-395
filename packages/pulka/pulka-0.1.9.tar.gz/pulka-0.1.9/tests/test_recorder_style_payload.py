from pulka import theme
from pulka.render.style_resolver import (
    StyleComponents,
    get_active_style_resolver,
    reset_style_resolver_cache,
)
from pulka.theme import ThemeConfig


def test_render_line_styles_payload_roundtrip() -> None:
    original_theme = theme.THEME

    config = ThemeConfig(
        border_style="#222222",
        table_style="default",
        header_style="white",
        header_active_style=None,
        cell_style="#cccccc",
        cell_null_style="#707070",
        cell_active_style="black on #f0f0f0",
        row_active_style="on #454545",
        row_selected_style="#63e6be bold",
        row_selected_active_style="black on #63e6be",
        status_style="white on #202020",
        dialog_style=None,
    )

    try:
        theme.set_theme(config)
        reset_style_resolver_cache()
        resolver = get_active_style_resolver()

        classes = ("table", "table.header")
        components = resolver.resolve(classes)
        payload = {
            "component": "table_control",
            "theme_epoch": theme.theme_epoch(),
            "lines": [
                {
                    "line_index": 0,
                    "plain_text": " header ",
                    "segments": [
                        {
                            "text": "header",
                            "classes": list(classes),
                            "foreground": components.foreground,
                            "background": components.background,
                            "extras": list(components.extras),
                        }
                    ],
                }
            ],
        }

        first_segment = payload["lines"][0]["segments"][0]
        round_trip = StyleComponents(
            foreground=first_segment["foreground"],
            background=first_segment["background"],
            extras=tuple(first_segment["extras"]),
        )
        style_str = round_trip.to_prompt_toolkit()
        assert "fg:#ffffff" in style_str

        style = theme.THEME.prompt_toolkit_style()
        attrs = style.get_attrs_for_style_str(style_str)
        assert attrs.color == "ffffff"
    finally:
        theme.set_theme(original_theme)
        reset_style_resolver_cache()

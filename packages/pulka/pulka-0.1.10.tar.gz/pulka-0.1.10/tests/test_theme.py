from pulka.theme import ThemeConfig, resolve_header_style


def test_resolve_header_style_promotes_plain_white() -> None:
    assert resolve_header_style("white") == "#ffffff"
    assert resolve_header_style("#ffffff") == "#ffffff"
    assert resolve_header_style(None) is None


def test_prompt_toolkit_style_uses_hex_white_for_headers() -> None:
    config = ThemeConfig(
        border_style=None,
        table_style=None,
        header_style="white",
        header_active_style=None,
        cell_style=None,
        cell_null_style=None,
        cell_active_style=None,
        row_active_style=None,
        row_selected_style=None,
        row_selected_active_style=None,
        status_style=None,
        dialog_style=None,
    )

    style = config.prompt_toolkit_style()
    attrs = style.get_attrs_for_style_str("class:table.header")
    assert attrs.color == "ffffff"

from types import SimpleNamespace

import pytest

from pulka.command.builtins import (
    handle_yank_all_columns,
    handle_yank_column,
    handle_yank_schema,
)
from pulka.command.registry import CommandContext


class _StubViewer:
    def __init__(self, columns):
        self.columns = list(columns)
        self.cur_col = 0
        self.status_message: str | None = None

    def current_colname(self):
        return self.columns[self.cur_col]

    def visible_columns(self):
        return list(self.columns)


@pytest.fixture()
def _clipboard(monkeypatch):
    calls: list[str] = []

    def _copy(text: str) -> bool:
        calls.append(text)
        return True

    monkeypatch.setattr("pulka.command.builtins.copy_to_clipboard", _copy)
    return calls


def test_yank_column_copies_active_column(_clipboard):
    viewer = _StubViewer(["a", "b"])
    viewer.cur_col = 1
    sheet = SimpleNamespace(schema={"a": "Int64", "b": "Utf8"})
    context = CommandContext(sheet, viewer)

    handle_yank_column(context, [])

    assert _clipboard == ["b"]
    assert viewer.status_message == "copied column b"


def test_yank_all_columns_formats_vertical_list(_clipboard):
    viewer = _StubViewer(["a", "b"])
    sheet = SimpleNamespace(schema={"a": "Int64", "b": "Utf8"})
    context = CommandContext(sheet, viewer)

    handle_yank_all_columns(context, [])

    assert _clipboard == ["[\n    'a',\n    'b',\n]"]
    assert viewer.status_message == "copied 2 columns"


def test_yank_schema_uses_visible_order(_clipboard):
    viewer = _StubViewer(["b", "a"])
    sheet = SimpleNamespace(schema={"a": "Int64", "b": "Utf8"})
    context = CommandContext(sheet, viewer)

    handle_yank_schema(context, [])

    assert _clipboard == ["{\n    'b': Utf8,\n    'a': Int64,\n}"]
    assert viewer.status_message == "schema copied"

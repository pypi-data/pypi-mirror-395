from __future__ import annotations

from pathlib import Path

import pytest

from pulka.cli.generate import (
    PresetResolutionError,
    _pick_input_source,
    _print_preset_listing,
)
from pulka.cli.presets import PRESET_ENV_VAR, PresetStore, load_preset_store


def test_load_preset_store_with_env_override(tmp_path, monkeypatch):
    preset_file = tmp_path / "presets.toml"
    monkeypatch.setenv(PRESET_ENV_VAR, str(preset_file))

    store = load_preset_store()

    assert store.path == preset_file
    assert "themartian" in store.presets


def test_load_preset_store_parses_entries(tmp_path, monkeypatch):
    preset_file = tmp_path / "presets.toml"
    preset_file.write_text(
        "[presets]\n"
        "themartian = '1r/x=sequence()'\n"
        'mini_nav = "200r/id=sequence();value=normal(0,1)"\n'
    )
    monkeypatch.setenv(PRESET_ENV_VAR, str(preset_file))

    store = load_preset_store()

    assert store.get("themartian") == "1r/x=sequence()"
    assert store.get("mini_nav").startswith("200r")
    # user-defined entry overrides builtin
    assert store.get("themartian") == "1r/x=sequence()"


def test_pick_input_source_prefers_preset():
    store = PresetStore(
        path=Path("/tmp/presets.toml"),
        presets={"demo": "1r/x=sequence()"},
        builtin_presets={},
    )

    value = _pick_input_source(None, "demo", store)

    assert value == "1r/x=sequence()"


def test_pick_input_source_errors_on_missing(monkeypatch):
    store = PresetStore(path=Path("/tmp/missing"), presets={}, builtin_presets={})

    with pytest.raises(PresetResolutionError):
        _pick_input_source(None, "demo", store)


def test_pick_input_source_errors_when_both_set():
    store = PresetStore(
        path=Path("/tmp/presets.toml"),
        presets={"demo": "1r/x=sequence()"},
        builtin_presets={},
    )

    with pytest.raises(PresetResolutionError):
        _pick_input_source("1r/x=sequence()", "demo", store)


def test_print_preset_listing_mentions_user_path(tmp_path, capsys):
    store = PresetStore(
        path=tmp_path / "presets.toml",
        presets={"demo": "1r/x=sequence()"},
        builtin_presets={},
    )

    _print_preset_listing(store)

    out = capsys.readouterr().out
    assert "Available presets" in out
    assert str(store.path) in out


def test_print_preset_listing_includes_capsule(tmp_path, capsys):
    store = PresetStore(
        path=tmp_path / "presets.toml",
        presets={"demo": "1r/x=sequence()"},
        builtin_presets={},
    )

    _print_preset_listing(store)

    out = capsys.readouterr().out
    assert "- demo:" in out

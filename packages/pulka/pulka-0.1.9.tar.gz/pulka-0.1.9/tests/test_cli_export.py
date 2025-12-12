"""CLI export regression tests."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pulka.api.session import Session
from pulka.cli import main


def _write_sample_source(tmp_path: Path) -> Path:
    path = tmp_path / "source.parquet"
    pl.DataFrame({"a": [1, 2], "b": ["x", "y"]}).write_parquet(path)
    return path


def test_cli_out_creates_file(tmp_path, capsys) -> None:
    source = _write_sample_source(tmp_path)
    destination = tmp_path / "export.csv"

    exit_code = main(
        [
            str(source),
            "--out",
            str(destination),
            "--out-option",
            "separator=;",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert destination.exists()
    contents = destination.read_text().splitlines()
    assert contents
    assert ";" in contents[0]
    assert "Export saved to" in captured.out
    assert "Writing dataset to export.csv" in captured.err


def test_cli_out_failure_bubbles_error(tmp_path, capsys) -> None:
    source = _write_sample_source(tmp_path)
    destination = tmp_path / "export"

    exit_code = main([str(source), "--out", str(destination)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert not destination.exists()
    assert "Export failed" in captured.err


def test_cli_out_respects_auto_render(monkeypatch, tmp_path, capsys) -> None:
    source = _write_sample_source(tmp_path)
    destination = tmp_path / "export.parquet"

    call_args: dict[str, object] = {}

    def _run_script(self, commands, auto_render=True):  # type: ignore[override]
        call_args["commands"] = list(commands)
        call_args["auto_render"] = auto_render
        return ["ok"]

    monkeypatch.setattr(Session, "run_script", _run_script)

    exit_code = main(
        [
            str(source),
            "--cmd",
            "render",
            "--out",
            str(destination),
            "--no-auto-render",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert destination.exists()
    assert call_args["commands"] == ["render"]
    assert call_args["auto_render"] is False
    assert "ok" in captured.out
    assert "Export saved to" in captured.out
    assert "Writing dataset to export.parquet" in captured.err

"""Smoke tests for --glimpse, --schema, and --describe CLI flags."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pulka.cli import main


def _write_source(tmp_path: Path) -> Path:
    path = tmp_path / "meta.parquet"
    pl.DataFrame(
        {
            "alpha": [1, 2, 3],
            "beta": ["x", "y", "z"],
            "gamma": [True, False, True],
        }
    ).write_parquet(path)
    return path


def test_cli_schema_prints_columns(tmp_path, capsys) -> None:
    source = _write_source(tmp_path)

    exit_code = main([str(source), "--schema"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "column" in captured.out
    assert "dtype" in captured.out
    assert "alpha" in captured.out


def test_cli_glimpse_prints_summary(tmp_path, capsys) -> None:
    source = _write_source(tmp_path)

    exit_code = main([str(source), "--glimpse"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Rows:" in captured.out
    assert "$ alpha" in captured.out


def test_cli_glimpse_with_expr(tmp_path, capsys) -> None:
    source = _write_source(tmp_path)

    exit_code = main([str(source), "--expr", "df.select(cs.starts_with('g'))", "--glimpse"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "gamma" in captured.out
    assert "alpha" not in captured.out


def test_cli_describe_prints_statistics(tmp_path, capsys) -> None:
    source = _write_source(tmp_path)

    exit_code = main([str(source), "--describe"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "statistic" in captured.out
    assert "count" in captured.out

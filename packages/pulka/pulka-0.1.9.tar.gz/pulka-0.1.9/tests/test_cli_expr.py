"""Integration tests for the CLI ``--expr`` flag."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from pulka.cli import main
from pulka.data.expr_lang import evaluate_dataset_expression


def _write_basic_source(tmp_path: Path) -> Path:
    path = tmp_path / "source.parquet"
    pl.DataFrame({"a": [1, 2], "b": ["x", "y"], "beta": ["one", "two"]}).write_parquet(path)
    return path


def test_expr_without_path_prints_table(capsys) -> None:
    exit_code = main(["--expr", "pl.DataFrame({'a': [1, 2]}).lazy()"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "a" in captured.out
    assert "expr error" not in captured.err


def test_expr_using_df_requires_dataset(capsys) -> None:
    exit_code = main(["--expr", "df.head(1)"])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "expr error" in captured.err


def test_expr_with_path_and_out(tmp_path, capsys) -> None:
    source = _write_basic_source(tmp_path)
    destination = tmp_path / "expr.csv"

    exit_code = main(
        [
            str(source),
            "--expr",
            "df.describe()",
            "--out",
            str(destination),
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert destination.exists()
    assert "Export saved to" in captured.out


def test_expr_tui_invokes_ui(monkeypatch, capsys) -> None:
    called: dict[str, object] = {}

    def _run_tui_app(viewer, recorder=None, on_shutdown=None):  # type: ignore[override]
        called["viewer"] = viewer
        called["recorder"] = recorder
        if callable(on_shutdown):
            on_shutdown(viewer.session)

    monkeypatch.setattr("pulka.tui.app.run_tui_app", _run_tui_app)

    exit_code = main(["--expr", "pl.DataFrame({'x': [1]}).lazy()", "--tui"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "expr error" not in captured.err
    assert called


def test_expr_df_glimpse_outputs_summary(tmp_path, capsys) -> None:
    source = _write_basic_source(tmp_path)

    exit_code = main([str(source), "--expr", "df.glimpse()"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Rows:" in captured.out
    assert "$ a" in captured.out


def test_expr_column_namespace_supported() -> None:
    lf = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]}).lazy()

    schema = lf.collect_schema()
    result = evaluate_dataset_expression(
        "df.filter(c.a == 2)",
        df=lf,
        columns=list(schema.keys()),
    )

    collected = result.collect()

    assert collected.shape == (1, 2)
    assert collected["a"].to_list() == [2]


def test_expr_column_selectors_supported() -> None:
    lf = pl.DataFrame({"alpha": [1], "beta": [2], "gamma": [3]}).lazy()

    schema = lf.collect_schema()
    result = evaluate_dataset_expression(
        "df.select(cs.starts_with('b'))",
        df=lf,
        columns=list(schema.keys()),
    )

    collected = result.collect()

    assert collected.columns == ["beta"]

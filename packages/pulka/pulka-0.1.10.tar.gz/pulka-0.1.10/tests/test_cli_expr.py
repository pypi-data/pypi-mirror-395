"""Integration tests for the CLI ``--expr`` flag."""

from __future__ import annotations

import os
from datetime import date
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


def test_expr_selectors_fallback(monkeypatch) -> None:
    lf = pl.DataFrame({"alpha": [1], "beta": [2], "gamma": [3]}).lazy()

    schema = lf.collect_schema()
    monkeypatch.setattr("pulka.data.expr_lang._polars_selectors", None)
    result = evaluate_dataset_expression(
        "df.select(cs.starts_with('b'))",
        df=lf,
        columns=list(schema.keys()),
    )

    collected = result.collect()

    assert collected.columns == ["beta"]


def test_expr_whitelisted_builtins() -> None:
    lf = pl.DataFrame({"a": [1, 2]}).lazy()
    schema = lf.collect_schema()

    result = evaluate_dataset_expression(
        "df.with_columns(pl.lit(len(range(3))).alias('len_range'))",
        df=lf,
        columns=list(schema.keys()),
    )

    collected = result.collect()

    assert collected["len_range"].to_list() == [3, 3]


def test_expr_datetime_and_path_and_scan(tmp_path) -> None:
    source = tmp_path / "data.csv"
    pl.DataFrame({"a": [1], "b": [date(2020, 1, 1)]}).write_csv(source)

    result = evaluate_dataset_expression(
        f"scan(Path('{source}')).with_columns(pl.lit(date(2020, 1, 1)).alias('d'))"
    )

    collected = result.collect()

    assert collected.columns == ["a", "b", "d"]


def test_expr_dbg_prints(capsys) -> None:
    result = evaluate_dataset_expression("dbg(pl.DataFrame({'x': [1]}).lazy(), 'tag')")

    captured = capsys.readouterr()

    assert "dbg tag" in captured.out
    assert result.collect().shape == (1, 1)


def test_expr_cfg_helpers_pass_through(monkeypatch) -> None:
    lf = pl.DataFrame({"a": [1]}).lazy()
    schema = lf.collect_schema()

    prev_rows = os.environ.get("POLARS_FMT_MAX_ROWS")
    prev_cols = os.environ.get("POLARS_FMT_MAX_COLS")
    prev_len = os.environ.get("POLARS_FMT_STR_LEN")
    monkeypatch.delenv("POLARS_FMT_MAX_ROWS", raising=False)
    monkeypatch.delenv("POLARS_FMT_MAX_COLS", raising=False)
    monkeypatch.delenv("POLARS_FMT_STR_LEN", raising=False)

    result = evaluate_dataset_expression(
        "cfg_fmt_str_lengths(8, cfg_cols(10, cfg_rows(5, df)))",
        df=lf,
        columns=list(schema.keys()),
    )
    collected = result.collect()

    assert collected.shape == (1, 1)
    assert os.environ.get("POLARS_FMT_MAX_ROWS") == "5"
    assert os.environ.get("POLARS_FMT_MAX_COLS") == "10"
    assert os.environ.get("POLARS_FMT_STR_LEN") == "8"

    # Restore env so later tests are not impacted.
    if prev_rows is None:
        os.environ.pop("POLARS_FMT_MAX_ROWS", None)
    else:
        os.environ["POLARS_FMT_MAX_ROWS"] = prev_rows
    if prev_cols is None:
        os.environ.pop("POLARS_FMT_MAX_COLS", None)
    else:
        os.environ["POLARS_FMT_MAX_COLS"] = prev_cols
    if prev_len is None:
        os.environ.pop("POLARS_FMT_STR_LEN", None)
    else:
        os.environ["POLARS_FMT_STR_LEN"] = prev_len

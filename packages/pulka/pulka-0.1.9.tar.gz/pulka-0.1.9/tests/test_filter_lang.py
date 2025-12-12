from __future__ import annotations

from pulka.data.filter_lang import clear_filter_cache, compile_filter_expression


def test_cache_hits_for_identical_text_and_schema() -> None:
    clear_filter_cache()
    columns = ["a", "b"]

    expr1 = compile_filter_expression("c.a > 1", columns)
    expr2 = compile_filter_expression("c.a > 1", columns)

    assert expr1 is expr2


def test_cache_miss_for_different_schema() -> None:
    clear_filter_cache()

    expr1 = compile_filter_expression("c.a > 1", ["a"])
    expr2 = compile_filter_expression("c.a > 1", ["a", "b"])

    assert expr1 is not expr2

from pulka.core.plan import FilterClause
from pulka.tui.screen import _format_expr_filters_for_modal


def test_format_expr_filters_for_modal_wraps_and_joins() -> None:
    clauses = [
        FilterClause("expr", "c.col_00 > 10"),
        FilterClause("expr", "c['city'] == 'NYC'"),
    ]

    assert _format_expr_filters_for_modal(clauses) == "(c.col_00 > 10) & (c['city'] == 'NYC')"


def test_format_expr_filters_for_modal_ignores_sql_and_empty() -> None:
    clauses = [
        FilterClause("sql", "fare > 10"),
        FilterClause("expr", "c.score >= 5"),
    ]

    assert _format_expr_filters_for_modal(clauses) == "(c.score >= 5)"

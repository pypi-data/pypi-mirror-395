"""Pure helpers to derive new :class:`~pulka.core.plan.QueryPlan` instances."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from typing import Literal

from .errors import PlanError
from .plan import FilterClause, QueryPlan

FilterMode = Literal["replace", "append"]


def reset(plan: QueryPlan | None = None) -> QueryPlan:
    """Return an empty plan, ignoring ``plan`` when provided."""

    return QueryPlan()


def _normalise_filter_text(text: str | None) -> str | None:
    if text is None:
        return None
    stripped = text.strip()
    return stripped or None


def _validate_mode(mode: FilterMode) -> FilterMode:
    if mode not in {"replace", "append"}:
        msg = f"unsupported filter mode: {mode!r}"
        raise PlanError(msg)
    return mode


def set_filter(
    plan: QueryPlan, filter_text: str | None, *, mode: FilterMode = "replace"
) -> QueryPlan:
    """Return ``plan`` with ``filter_text`` applied as an expression filter."""

    mode = _validate_mode(mode)
    normalised = _normalise_filter_text(filter_text)
    if normalised is None:
        remaining = tuple(clause for clause in plan.filter_clauses if clause.kind != "expr")
        if remaining == plan.filter_clauses:
            return plan
        return replace(plan, filter_clauses=remaining)

    clause = FilterClause("expr", normalised)
    if mode == "append":
        clauses = (*plan.filter_clauses, clause)
    else:
        preserved = [c for c in plan.filter_clauses if c.kind != "expr"]
        clauses = (*preserved, clause)

    if clauses == plan.filter_clauses:
        return plan

    return replace(plan, filter_clauses=clauses)


def set_sql_filter(
    plan: QueryPlan, where_clause: str | None, *, mode: FilterMode = "replace"
) -> QueryPlan:
    """Return ``plan`` with ``where_clause`` applied as an SQL filter."""

    mode = _validate_mode(mode)
    normalised = _normalise_filter_text(where_clause)
    if normalised is None:
        remaining = tuple(clause for clause in plan.filter_clauses if clause.kind != "sql")
        if remaining == plan.filter_clauses:
            return plan
        return replace(plan, filter_clauses=remaining)

    clause = FilterClause("sql", normalised)
    if mode == "append":
        clauses = (*plan.filter_clauses, clause)
    else:
        preserved = [c for c in plan.filter_clauses if c.kind != "sql"]
        clauses = (*preserved, clause)

    if clauses == plan.filter_clauses:
        return plan

    return replace(plan, filter_clauses=clauses)


def set_search(plan: QueryPlan, text: str | None) -> QueryPlan:
    """Return ``plan`` with ``text`` recorded for search."""

    if text is None:
        search = None
    else:
        stripped = text.strip()
        search = stripped or None

    if search == plan.search_text:
        return plan

    return replace(plan, search_text=search)


def toggle_sort(
    plan: QueryPlan, column: str, cycle: Iterable[str] = ("asc", "desc", "none")
) -> QueryPlan:
    """Toggle sort on ``column`` cycling through ``cycle`` states."""

    if not column:
        return plan

    states = tuple(state.lower() for state in cycle)
    if not states:
        return plan

    current_entries = list(plan.sort)
    for name, desc in current_entries:
        if name == column:
            current_state = "desc" if desc else "asc"
            break
    else:
        current_state = None

    if current_state is None:
        next_state = states[0]
    else:
        try:
            state_pos = states.index(current_state)
        except ValueError:
            state_pos = -1
        next_state = states[(state_pos + 1) % len(states)]

    if next_state not in {"asc", "desc", "none"}:
        msg = f"unsupported sort state: {next_state!r}"
        raise PlanError(msg)

    remaining = [entry for entry in current_entries if entry[0] != column]
    if next_state == "asc":
        new_sort = tuple([(column, False)] + remaining)
    elif next_state == "desc":
        new_sort = tuple([(column, True)] + remaining)
    else:  # next_state == "none"
        new_sort = tuple(remaining)

    if tuple(new_sort) == plan.sort:
        return plan

    return replace(plan, sort=new_sort)


def clear_sort(plan: QueryPlan) -> QueryPlan:
    """Return ``plan`` with any sort removed."""

    if not plan.sort:
        return plan

    return replace(plan, sort=())


def set_projection(plan: QueryPlan, columns: Iterable[str]) -> QueryPlan:
    """Return ``plan`` constrained to ``columns``."""

    projection: list[str] = []
    for name in columns:
        if name not in projection:
            projection.append(name)

    new_projection = tuple(projection)
    if new_projection == plan.projection:
        return plan

    return replace(plan, projection=new_projection)


def reorder_columns(plan: QueryPlan, columns: Iterable[str]) -> QueryPlan:
    """Return ``plan`` with projected columns reordered according to ``columns``."""

    desired = []
    seen: set[str] = set()
    for name in columns:
        if name in seen:
            continue
        desired.append(name)
        seen.add(name)

    current_projection = list(plan.projection)
    if not current_projection:
        current_projection = desired
    else:
        current_projection = [col for col in current_projection if col not in seen]
        desired.extend(current_projection)

    new_projection = tuple(desired)
    if new_projection == plan.projection:
        return plan

    return replace(plan, projection=new_projection)


def set_limit(plan: QueryPlan, limit: int | None, offset: int = 0) -> QueryPlan:
    """Return ``plan`` with ``limit``/``offset`` applied."""

    if limit is None:
        normalized_limit: int | None = None
    else:
        coerced = int(limit)
        normalized_limit = None if coerced < 0 else coerced

    normalized_offset = max(0, int(offset))

    if normalized_limit == plan.limit and normalized_offset == plan.offset:
        return plan

    return replace(plan, limit=normalized_limit, offset=normalized_offset)


__all__ = [
    "FilterMode",
    "clear_sort",
    "reset",
    "set_filter",
    "set_limit",
    "set_projection",
    "reorder_columns",
    "set_search",
    "set_sql_filter",
    "toggle_sort",
]

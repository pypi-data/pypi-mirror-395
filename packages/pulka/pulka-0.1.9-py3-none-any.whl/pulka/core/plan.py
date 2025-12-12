"""Immutable query plan shared by the core engine and sheets."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Literal


def normalized_columns_key(columns: Iterable[str]) -> str:
    """Return a stable signature for a sequence of columns."""

    return "\u241f".join(columns)


@dataclass(frozen=True, slots=True)
class FilterClause:
    """Individual filter clause tracked by the :class:`QueryPlan`."""

    kind: Literal["expr", "sql"]
    text: str

    def __post_init__(self) -> None:
        normalised_text = self.text.strip()
        if not normalised_text:
            msg = "FilterClause.text must be non-empty"
            raise ValueError(msg)
        if self.kind not in {"expr", "sql"}:
            msg = f"Invalid filter clause kind: {self.kind!r}"
            raise ValueError(msg)
        object.__setattr__(self, "text", normalised_text)


def _normalise_filter_clauses(
    clauses: Iterable[FilterClause | str] | None,
    *,
    filters: Iterable[str] | None,
    sql_filter: str | None,
) -> tuple[FilterClause, ...]:
    """Normalise legacy inputs into a tuple of ``FilterClause`` objects."""

    sources: list[FilterClause | str] = []
    if clauses is not None:
        sources.extend(clauses)
    if filters is not None:
        sources.extend(filters)
    if sql_filter is not None:
        trimmed = sql_filter.strip()
        if trimmed:
            sources.append(FilterClause("sql", trimmed))

    normalised: list[FilterClause] = []
    for entry in sources:
        if isinstance(entry, FilterClause):
            normalised.append(entry)
            continue
        text = str(entry).strip()
        if not text:
            continue
        normalised.append(FilterClause("expr", text))
    return tuple(normalised)


@dataclass(frozen=True, slots=True, init=False)
class QueryPlan:
    """Immutable description of how to transform a LazyFrame for display."""

    filter_clauses: tuple[FilterClause, ...]
    sort: tuple[tuple[str, bool], ...]  # (column, desc)
    projection: tuple[str, ...]
    search_text: str | None
    limit: int | None
    offset: int

    def __init__(
        self,
        filter_clauses: Iterable[FilterClause | str] | None = None,
        *,
        filters: Iterable[str] | None = None,
        sql_filter: str | None = None,
        sort: Iterable[tuple[str, bool]] = (),
        projection: Iterable[str] = (),
        search_text: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> None:
        object.__setattr__(
            self,
            "filter_clauses",
            _normalise_filter_clauses(
                filter_clauses,
                filters=filters,
                sql_filter=sql_filter,
            ),
        )
        object.__setattr__(self, "sort", tuple(tuple(entry) for entry in sort))
        object.__setattr__(self, "projection", tuple(projection))
        object.__setattr__(self, "search_text", search_text)
        object.__setattr__(self, "limit", limit)
        object.__setattr__(self, "offset", offset)

    @property
    def filters(self) -> tuple[str, ...]:
        """Legacy accessor returning expression filter texts."""

        return tuple(clause.text for clause in self.filter_clauses if clause.kind == "expr")

    @property
    def sql_filter(self) -> str | None:
        """Return the first SQL filter clause when present."""

        for clause in self.filter_clauses:
            if clause.kind == "sql":
                return clause.text
        return None

    def combined_filter_text(self) -> str | None:
        """Return a human-readable combined filter summary."""

        sql_clauses = [clause.text for clause in self.filter_clauses if clause.kind == "sql"]
        expr_clauses = [clause.text for clause in self.filter_clauses if clause.kind == "expr"]

        parts: list[str] = []
        if sql_clauses:
            parts.append(f"SQL WHERE {' AND '.join(sql_clauses)}")
        if expr_clauses:
            parts.append(" AND ".join(expr_clauses))
        if not parts:
            return None
        return " AND ".join(parts)

    def with_limit(self, limit: int | None) -> QueryPlan:
        return QueryPlan(
            filter_clauses=self.filter_clauses,
            sort=self.sort,
            projection=self.projection,
            search_text=self.search_text,
            limit=limit,
            offset=self.offset,
        )

    def with_offset(self, offset: int) -> QueryPlan:
        return QueryPlan(
            filter_clauses=self.filter_clauses,
            sort=self.sort,
            projection=self.projection,
            search_text=self.search_text,
            limit=self.limit,
            offset=offset,
        )

    def with_projection(self, projection: Iterable[str]) -> QueryPlan:
        return QueryPlan(
            filter_clauses=self.filter_clauses,
            sort=self.sort,
            projection=tuple(projection),
            search_text=self.search_text,
            limit=self.limit,
            offset=self.offset,
        )

    def projection_or(self, fallback: Iterable[str]) -> tuple[str, ...]:
        """Return the plan projection or ``fallback`` when not specified."""

        if self.projection:
            return self.projection
        return tuple(fallback)

    def sort_columns(self) -> tuple[str, ...]:
        """Return the ordered list of sort columns."""

        return tuple(column for column, _ in self.sort)

    def sort_descending(self) -> tuple[bool, ...]:
        """Return the tuple of descending flags for the configured sort."""

        return tuple(desc for _, desc in self.sort)

    def snapshot_payload(self) -> dict[str, Any]:
        """Return a JSON-serialisable payload describing the plan."""

        return {
            "filter_clauses": [
                {"kind": clause.kind, "text": clause.text} for clause in self.filter_clauses
            ],
            "filters": list(self.filters),
            "sql_filter": self.sql_filter,
            "sort": list(self.sort),
            "projection": list(self.projection),
            "search_text": self.search_text,
            "limit": self.limit,
            "offset": self.offset,
        }

    def snapshot(self) -> dict[str, Any]:
        """Return the payload and a stable hash for recorder snapshots."""

        payload = self.snapshot_payload()
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha1(serialized.encode("utf-8")).hexdigest()
        return {"hash": digest, "plan": payload}


__all__ = ["FilterClause", "QueryPlan", "normalized_columns_key"]

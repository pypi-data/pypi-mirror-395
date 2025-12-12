"""Shared helpers for stable row identifiers.

This module centralises the reserved column name used to attach durable row
identifiers to datasets. Keeping it in one place ensures both the engine and
presentation layers treat the column consistently and avoid surfacing it to
users.
"""

from __future__ import annotations

# Reserved column inserted on ingest to provide stable per-row ids. Keep this
# out of user-facing schemas and projections.
ROW_ID_COLUMN = "__pulka_row_id"


__all__ = ["ROW_ID_COLUMN"]

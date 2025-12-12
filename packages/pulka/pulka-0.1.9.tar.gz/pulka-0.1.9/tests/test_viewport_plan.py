"""Snapshot tests for the viewport planning module."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

import polars as pl
import pytest

from pulka.core.viewer.viewer import Viewer
from pulka.render.viewport_plan import ViewportPlan, compute_viewport_plan
from pulka.sheets.data_sheet import DataSheet

SNAPSHOT_DIR = Path("tests/snapshots/viewport_plan")


def _serialize_plan(plan) -> dict:
    """Return a JSON-serialisable representation of a ``ViewportPlan``."""

    data = asdict(plan)
    # ``asdict`` converts dataclasses recursively, which is exactly what we want.
    return data


def _assert_snapshot(name: str, plan) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(_serialize_plan(plan), indent=2, sort_keys=True)
    snapshot_path = SNAPSHOT_DIR / f"{name}.json"
    update = bool(os.getenv("UPDATE_SNAPSHOTS"))

    if not snapshot_path.exists() or update:
        snapshot_path.write_text(payload + "\n", encoding="utf-8")
        if not update:
            pytest.skip(f"Created initial snapshot for {name}")

    expected = snapshot_path.read_text(encoding="utf-8")
    assert payload + "\n" == expected


def _make_viewer(df: pl.DataFrame, job_runner, *, rows: int = 8, width: int = 80) -> Viewer:
    sheet = DataSheet(df.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=rows, runner=job_runner)
    viewer.configure_terminal(width, rows)
    return viewer


def test_viewport_plan_basic_snapshot(job_runner) -> None:
    df = pl.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "name": ["alpha", "beta", "gamma", "delta"],
            "value": [0.5, None, 2.75, -1.0],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=6, width=72)
    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )
    _assert_snapshot("basic", plan)


def test_viewport_plan_with_scroll_and_frozen(job_runner) -> None:
    df = pl.DataFrame(
        {
            "id": list(range(1, 11)),
            "city": [
                "Lisbon",
                "Paris",
                "Berlin",
                "Tokyo",
                "Sydney",
                "Oslo",
                "Lima",
                "Seoul",
                "Cairo",
                "Delhi",
            ],
            "score": [
                1.1,
                2.2,
                3.3,
                4.4,
                5.5,
                6.6,
                7.7,
                8.8,
                9.9,
                10.1,
            ],
            "notes": [
                "sunny",
                "art",
                "history",
                "sushi",
                "harbour",
                "fjord",
                "andes",
                "tech",
                "pyramids",
                "spice",
            ],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=7, width=48)
    viewer.set_frozen_columns(1)
    viewer.move_down(3)
    viewer.move_right(3)
    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )
    _assert_snapshot("scroll_frozen", plan)


def test_viewport_plan_sorted_numeric_snapshot(job_runner) -> None:
    df = pl.DataFrame(
        {
            "product": ["Widget", "Gadget", "Doodad", "Thing"],
            "inventory": [1200, 850, 30, 5400],
            "price": [19.99, 29.5, None, 150.0],
            "status": ["ok", "restock", "critical", "surplus"],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=68)
    viewer.toggle_sort("price")
    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )
    _assert_snapshot("sorted_numeric", plan)


def test_maximized_column_width_is_preserved(job_runner) -> None:
    long_text = "lorem ipsum dolor sit amet " * 5
    df = pl.DataFrame(
        {
            "description": [long_text, "short", "medium"],
            "other": ["x", "y", "z"],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=60)
    viewer.toggle_maximize_current_col()

    maximized_idx = viewer.maximized_column_index
    assert maximized_idx is not None

    maximized_width = viewer._header_widths[maximized_idx]
    assert maximized_width > getattr(viewer, "view_width_chars", 0)

    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    assert plan.columns[maximized_idx].width == maximized_width


def test_viewport_plan_allows_partial_rightmost_column(job_runner) -> None:
    df = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "very_wide_header_alpha": ["aaa", "bbb", "ccc"],
            "very_wide_header_bravo": ["ddd", "eee", "fff"],
            "very_wide_header_charlie": ["ggg", "hhh", "iii"],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=20)

    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    assert len(plan.columns) >= 2
    last_column = plan.columns[-1]
    assert last_column.width > 0
    assert last_column.width < last_column.min_width
    assert not last_column.header_active
    assert not getattr(viewer, "_last_col_fits_completely", True)


def test_active_column_is_never_partial(job_runner) -> None:
    df = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "very_wide_header_alpha": ["aaa", "bbb", "ccc"],
            "very_wide_header_bravo": ["ddd", "eee", "fff"],
            "very_wide_header_charlie": ["ggg", "hhh", "iii"],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=28)
    # Move the cursor so the next navigation would have previously produced a
    # partially visible active column at the right edge.
    viewer.move_right(3)

    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    active_columns = [column for column in plan.columns if column.header_active]
    assert active_columns, "expected an active column in the viewport plan"
    active_column = active_columns[0]
    assert active_column.width >= active_column.min_width, "active column should not be truncated"


def test_integer_columns_remain_integer_formatted(job_runner) -> None:
    df = pl.DataFrame({"id": [1, 2, 3, 4], "value": [10, 20, 30, 40]})
    viewer = _make_viewer(df, job_runner, rows=6, width=40)
    plan = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    for row in plan.cells[1:]:
        assert row, "Expected body cells in integer formatting test"
        for cell in row:
            if not cell.numeric or cell.is_null:
                continue
            text = cell.text.strip()
            assert "." not in text, f"Integer cell rendered as float: {text}"


def test_decimal_alignment_consistent_across_scroll(job_runner) -> None:
    values = [10.1] * 200
    values[100] = 10.1234
    df = pl.DataFrame({"value": values})
    viewer = _make_viewer(df, job_runner, rows=6, width=36)

    plan_top = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    def _fraction_lengths(plan: ViewportPlan) -> set[int]:
        lengths: set[int] = set()
        for row in plan.cells[1:]:
            if not row:
                continue
            cell = row[0]
            if not cell.numeric or cell.is_null:
                continue
            text = cell.text.strip()
            if "." in text:
                lengths.add(len(text.split(".", 1)[1]))
        return lengths

    top_lengths = _fraction_lengths(plan_top)
    assert top_lengths, "Expected fractional digits in the initial viewport"
    baseline = max(top_lengths)

    viewer.move_down(100)
    plan_scrolled = compute_viewport_plan(
        viewer,
        getattr(viewer, "view_width_chars", 80),
        getattr(viewer, "view_height", 20),
    )

    scrolled_lengths = _fraction_lengths(plan_scrolled)
    assert scrolled_lengths == {baseline}

    scrolled_texts = [
        row[0].text.strip()
        for row in plan_scrolled.cells[1:]
        if row and row[0].numeric and not row[0].is_null
    ]
    assert scrolled_texts, "Expected numeric cells after scrolling"
    assert all(not text.startswith("10.12") for text in scrolled_texts)

import polars as pl
from prompt_toolkit.data_structures import Point
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.mouse_events import MouseButton, MouseEvent, MouseEventType, MouseModifier

from pulka.api import Runtime
from pulka.core.viewer.viewer import Viewer
from pulka.render.style_resolver import get_active_style_resolver
from pulka.render.table import render_plan_lines, render_table
from pulka.sheets.data_sheet import DataSheet
from pulka.testing.data import make_df, write_df
from pulka.tui.controls import table_control as table_control_module
from pulka.tui.controls.table_control import TableControl, _BudgetPlan
from pulka.tui.screen import Screen


def _make_viewer(df: pl.DataFrame, job_runner, *, rows: int = 6, width: int = 72) -> Viewer:
    sheet = DataSheet(df.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=rows, runner=job_runner)
    viewer.configure_terminal(width, rows)
    return viewer


class _DummyScreen:
    def __init__(self) -> None:
        self._pending_row_delta = 0
        self._pending_col_delta = 0
        self.refresh_calls = 0

    def _apply_pending_moves(self) -> None:  # pragma: no cover - interface stub
        return None

    def _queue_move(self, dr: int = 0, dc: int = 0) -> None:
        if dr:
            self._pending_row_delta += 1 if dr > 0 else -1
        if dc:
            self._pending_col_delta += 1 if dc > 0 else -1

    def refresh(self) -> None:
        self.refresh_calls += 1


def _mouse_event(event_type: MouseEventType, modifiers: frozenset[MouseModifier] | None = None):
    return MouseEvent(
        position=Point(0, 0),
        event_type=event_type,
        button=MouseButton.NONE,
        modifiers=modifiers or frozenset(),
    )


def test_mouse_wheel_queues_vertical_scroll(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3]})
    viewer = _make_viewer(df, job_runner, rows=4, width=40)
    screen = _DummyScreen()

    control = TableControl(
        viewer,
        apply_pending_moves=screen._apply_pending_moves,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    result = control.mouse_handler(_mouse_event(MouseEventType.SCROLL_DOWN))

    assert result is None
    assert screen._pending_row_delta == 1
    assert screen._pending_col_delta == 0
    assert screen.refresh_calls == 1


def test_ctrl_mouse_wheel_scrolls_columns(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3]})
    viewer = _make_viewer(df, job_runner, rows=4, width=40)
    screen = _DummyScreen()

    control = TableControl(
        viewer,
        apply_pending_moves=screen._apply_pending_moves,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    modifiers = frozenset({MouseModifier.CONTROL})
    control.mouse_handler(_mouse_event(MouseEventType.SCROLL_DOWN, modifiers))
    control.mouse_handler(_mouse_event(MouseEventType.SCROLL_UP, modifiers))

    assert screen._pending_row_delta == 0
    assert screen._pending_col_delta == 0
    assert screen.refresh_calls == 2


def test_table_control_renders_visible_plan(job_runner):
    df = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "city": ["Lisbon", "Paris", "Berlin"],
            "score": [1.1, None, 3.3],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=60)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    content = control.create_content(width=60, height=5)
    lines = [
        "".join(fragment for _, fragment in content.get_line(i)) for i in range(content.line_count)
    ]

    rich_lines = render_table(viewer, include_status=False, test_mode=True).splitlines()
    expected = rich_lines[: len(lines)]
    assert lines == expected

    viewer.set_frozen_columns(1)
    frozen_content = control.create_content(width=60, height=5)
    frozen_lines = [
        "".join(fragment for _, fragment in frozen_content.get_line(i))
        for i in range(frozen_content.line_count)
    ]
    frozen_expected = render_table(viewer, include_status=False, test_mode=True).splitlines()[
        : len(frozen_lines)
    ]
    assert frozen_lines == frozen_expected


def test_table_shows_horizontal_overflow_markers(job_runner):
    df = pl.DataFrame({f"col{idx}": [idx] for idx in range(6)})
    viewer = _make_viewer(df, job_runner, rows=4, width=28)

    initial = render_table(viewer, include_status=False, test_mode=True).splitlines()
    assert initial, "expected table output"
    header_line = initial[1]
    assert header_line[-1] == ">"
    assert header_line[-2] == " "
    assert header_line[0] == " "

    viewer.move_right(4)
    assert viewer.col0 > 0

    scrolled = render_table(viewer, include_status=False, test_mode=True).splitlines()
    assert scrolled, "expected table output after scrolling"
    scrolled_header = scrolled[1]
    assert scrolled_header[0] == "<"
    assert scrolled_header[-1] == ">"
    assert scrolled_header[-2] == " "


def test_budget_degrade_keeps_highlight_and_separator(job_runner):
    df = pl.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "value": [10.0, 20.5, -3.0, 8.25],
        }
    )
    viewer = _make_viewer(df, job_runner, rows=5, width=60)
    viewer.move_down()  # ensure an active body row
    viewer.set_frozen_columns(1)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    plan = table_control_module.compute_viewport_plan(
        viewer, viewer.view_width_chars, viewer.view_height
    )

    control._current_budget_plan = _BudgetPlan(
        overscan_hint=viewer.view_height,
        minimal_styles=True,
        drop_borders=True,
        coalesce_multiplier=2.0,
    )
    lines, _ = control._render_lines(plan, viewer.view_height)
    control._current_budget_plan = _BudgetPlan()

    plain_lines = [line.plain_text for line in lines]
    assert any("─" in text for text in plain_lines), "expected header separator to remain"
    assert any("│" in text for text in plain_lines), "expected frozen column border to persist"

    resolver = get_active_style_resolver()
    active_segments = [
        segment
        for line in lines
        if line.source is not None
        for segment in line.source.segments
        if "table.row.active" in segment.classes or "table.cell.active" in segment.classes
    ]
    assert active_segments, "expected active row segments to remain during budget degrade"

    resolved = [resolver.resolve(segment.classes) for segment in active_segments]
    assert any(comp.background or comp.extras or comp.foreground for comp in resolved)


def test_budget_degrade_keeps_selected_row_style(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3]})
    viewer = _make_viewer(df, job_runner, rows=5, width=60)
    viewer.toggle_row_selection()
    viewer.move_down()  # move focus away so the selected row is not active

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    plan = table_control_module.compute_viewport_plan(
        viewer, viewer.view_width_chars, viewer.view_height
    )

    control._current_budget_plan = _BudgetPlan(minimal_styles=True, drop_borders=True)
    lines, _ = control._render_lines(plan, viewer.view_height)
    control._current_budget_plan = _BudgetPlan()

    selected_segments = [
        segment
        for line in lines
        if line.source is not None
        for segment in line.source.segments
        if "table.row.selected" in segment.classes
    ]
    assert selected_segments, "expected selected row segments to persist during budget degrade"

    resolver = get_active_style_resolver()
    resolved = [resolver.resolve(segment.classes) for segment in selected_segments]
    assert any(comp.foreground for comp in resolved)
    assert all(comp.background is None for comp in resolved)


def test_budget_degrade_keeps_null_cell_style(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3], "maybe": [None, "x", None]})
    viewer = _make_viewer(df, job_runner, rows=5, width=40)
    viewer.move_right()  # focus the column with nulls to ensure it is active

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    plan = table_control_module.compute_viewport_plan(
        viewer, viewer.view_width_chars, viewer.view_height
    )

    control._current_budget_plan = _BudgetPlan(minimal_styles=True, drop_borders=True)
    lines, _ = control._render_lines(plan, viewer.view_height)
    control._current_budget_plan = _BudgetPlan()

    null_segments = [
        segment
        for line in lines
        if line.source is not None
        for segment in line.source.segments
        if segment.text.strip() == "null"
    ]

    assert null_segments, "expected at least one rendered null segment"
    assert all("table.cell.null" in segment.classes for segment in null_segments), (
        "expected null cells to retain their dimming class during budget degrade"
    )


def test_blank_padding_row_keeps_active_row_highlight(job_runner):
    df = pl.DataFrame({"id": [1]})
    viewer = _make_viewer(df, job_runner, rows=6, width=60)
    viewer.set_frozen_columns(1)
    viewer.move_down()
    viewer.move_down()
    viewer.move_down()

    plan = table_control_module.compute_viewport_plan(
        viewer, viewer.view_width_chars, viewer.view_height
    )
    lines = render_plan_lines(plan, viewer.view_height)

    assert lines, "expected rendered lines to be present"
    bottom_line = lines[-1]
    border_segments = [segment for segment in bottom_line.segments if segment.text == "│"]
    assert not border_segments, "padding after the last row should not render frozen border"
    assert bottom_line.segments, "expected padding line to carry styling segments"


def test_table_control_leaves_single_gap_before_status(job_runner):
    df = pl.DataFrame({"id": [1]})
    viewer = _make_viewer(df, job_runner, rows=3, width=40)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    height = 8
    content = control.create_content(width=40, height=height)

    rich_lines = render_table(viewer, include_status=False, test_mode=True).splitlines()

    assert content.line_count == len(rich_lines)

    last_line = "".join(fragment for _, fragment in content.get_line(content.line_count - 1))
    assert last_line.strip() == ""

    if content.line_count > 1:
        penultimate = "".join(fragment for _, fragment in content.get_line(content.line_count - 2))
        assert penultimate.strip() != ""


def test_screen_uses_table_control_by_default(monkeypatch, tmp_path):
    monkeypatch.delenv("PULKA_PTK_TABLE", raising=False)
    monkeypatch.delenv("PD_PTK_TABLE", raising=False)
    df = make_df("mini_nav", rows=6, cols=3, seed=42)
    dataset_path = tmp_path / "table.parquet"
    write_df(df, dataset_path, "parquet")

    runtime = Runtime(load_entry_points=False)
    session = runtime.open(str(dataset_path), viewport_rows=6)

    screen = Screen(session.viewer)
    try:
        assert isinstance(screen._table_control, TableControl)
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            unsubscribe()


def test_screen_uses_ansi_fallback_when_flag_disabled(monkeypatch, tmp_path):
    monkeypatch.setenv("PULKA_PTK_TABLE", "0")
    df = make_df("mini_nav", rows=6, cols=3, seed=42)
    dataset_path = tmp_path / "table.parquet"
    write_df(df, dataset_path, "parquet")

    runtime = Runtime(load_entry_points=False)
    session = runtime.open(str(dataset_path), viewport_rows=6)

    screen = Screen(session.viewer)
    try:
        assert isinstance(screen._table_control, FormattedTextControl)
    finally:
        unsubscribe = getattr(screen, "_view_stack_unsubscribe", None)
        if unsubscribe is not None:
            unsubscribe()


def test_table_control_plan_cache_hits(monkeypatch, job_runner):
    df = pl.DataFrame({"id": [1, 2, 3], "city": ["Oslo", "Berlin", "Paris"]})
    viewer = _make_viewer(df, job_runner, rows=5, width=60)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    call_count = 0
    original_compute = table_control_module.compute_viewport_plan

    def _counting_plan(v: Viewer, width: int, height: int):
        nonlocal call_count
        call_count += 1
        return original_compute(v, width, height)

    monkeypatch.setattr("pulka.tui.controls.table_control.compute_viewport_plan", _counting_plan)

    control.create_content(width=60, height=5)
    control.create_content(width=60, height=5)
    assert call_count == 1

    viewer.move_down()
    control.create_content(width=60, height=5)
    assert call_count == 2


def test_table_control_invalidation_clears_cache(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3]})
    viewer = _make_viewer(df, job_runner, rows=4, width=40)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    class _DummyHooks:
        def __init__(self) -> None:
            self.calls = 0

        def invalidate(self) -> None:
            self.calls += 1

    hooks = _DummyHooks()
    wrapped = control.attach_ui_hooks(hooks)
    control.create_content(width=40, height=4)
    assert control._cached_plan is not None

    wrapped.invalidate()
    assert control._cached_plan is None
    assert hooks.calls == 1


def test_table_control_plan_key_tracks_theme_epoch(job_runner):
    df = pl.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
    viewer = _make_viewer(df, job_runner, rows=4, width=50)

    control = TableControl(
        viewer,
        apply_pending_moves=lambda: None,
        poll_background_jobs=lambda: None,
        set_status=lambda fragments: None,
        recorder=None,
    )

    control.create_content(width=50, height=4)
    first_key = control._plan_cache_key
    assert first_key is not None

    import pulka.theme as theme

    previous_epoch = theme.theme_epoch()
    theme.set_theme(theme.THEME)
    assert theme.theme_epoch() != previous_epoch

    control.create_content(width=50, height=4)
    second_key = control._plan_cache_key
    assert second_key is not None
    assert second_key[-1] == theme.theme_epoch()
    assert second_key[-1] != first_key[-1]

    cache_keys = list(control._line_cache.keys())
    assert cache_keys, "expected rendered lines to populate cache"
    for key in cache_keys:
        if not key:
            continue
        if key[0] == "separator":
            assert key[-2] == theme.theme_epoch()
        else:
            assert key[-3] == theme.theme_epoch()


def test_row_cache_prefetch_respects_budget_hint(job_runner):
    df = pl.DataFrame({"value": list(range(64))})
    viewer = _make_viewer(df, job_runner, rows=6, width=40)

    row_cache = viewer._row_cache
    full_prefetch = row_cache.get_prefetch()
    assert full_prefetch >= max(viewer.view_height * 2, 64)

    capped_prefetch = row_cache.get_prefetch(viewer.view_height // 2)
    assert capped_prefetch == viewer.view_height

    row_cache.prefetch = 128
    assert row_cache.get_prefetch(512) == 128

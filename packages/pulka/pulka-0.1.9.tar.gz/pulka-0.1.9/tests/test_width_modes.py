import polars as pl

from pulka.core.viewer import Viewer
from pulka.render.table import render_table
from pulka.sheets.data_sheet import DataSheet


def make_viewer(job_runner) -> Viewer:
    data = {
        "id": [1, 2, 3, 4],
        "name": [
            "short",
            "a much longer piece of text",
            "tiny",
            "moderately sized value",
        ],
        "notes": [
            "alpha",
            "beta",
            "gamma",
            "delta",
        ],
    }
    df = pl.DataFrame(data)
    sheet = DataSheet(df.lazy(), runner=job_runner)
    return Viewer(sheet, viewport_rows=10, viewport_cols=3, runner=job_runner)


def test_toggle_maximize_current_column_cycle(job_runner):
    viewer = make_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("name")
    baseline_widths = list(viewer._default_header_widths)

    viewer.toggle_maximize_current_col()

    assert viewer.maximized_column_index == viewer.cur_col
    assert not viewer.all_columns_maximized
    assert viewer._header_widths[viewer.cur_col] >= baseline_widths[viewer.cur_col]

    viewer.toggle_maximize_current_col()

    assert viewer.maximized_column_index is None
    assert viewer._header_widths == viewer._default_header_widths


def test_toggle_maximize_all_columns_cycle(job_runner):
    viewer = make_viewer(job_runner)
    baseline_widths = list(viewer._default_header_widths)

    viewer.toggle_maximize_all_cols()

    assert viewer.all_columns_maximized
    assert viewer.maximized_column_index is None
    width_pairs = zip(viewer._header_widths, baseline_widths, strict=False)
    assert all(cur >= base for cur, base in width_pairs)

    viewer.toggle_maximize_all_cols()

    assert not viewer.all_columns_maximized
    assert viewer._header_widths == viewer._default_header_widths


def test_single_mode_overrides_all_mode(job_runner):
    viewer = make_viewer(job_runner)

    viewer.toggle_maximize_all_cols()
    viewer.toggle_maximize_current_col()

    assert not viewer.all_columns_maximized
    assert viewer.maximized_column_index == viewer.cur_col


def test_maximize_tracks_column_changes(job_runner):
    viewer = make_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("name")

    viewer.toggle_maximize_current_col()
    first_target = viewer.maximized_column_index

    viewer.move_right()
    viewer.toggle_maximize_current_col()

    assert first_target != viewer.maximized_column_index
    assert viewer.maximized_column_index == viewer.cur_col


def test_maximize_all_aligns_viewport(job_runner):
    viewer = make_viewer(job_runner)
    viewer.cur_col = len(viewer.columns) - 1

    viewer.toggle_maximize_all_cols()

    assert viewer.col0 == viewer.cur_col


def test_maximize_all_does_not_show_partial_columns(job_runner):
    viewer = make_viewer(job_runner)
    viewer._viewport_cols_override = None

    viewer.toggle_maximize_all_cols()

    _ = viewer.visible_cols  # trigger computation

    assert getattr(viewer, "_last_col_fits_completely", True)


def test_width_mode_state_snapshot_matches_helpers(job_runner):
    viewer = make_viewer(job_runner)
    # Pick a column that actually benefits from maximisation.
    viewer.cur_col = viewer.columns.index("name")
    viewer.toggle_maximize_current_col()

    snapshot = viewer.width_mode_state

    assert snapshot["mode"] == "single"
    assert snapshot["target"] == viewer.maximized_column_index
    assert not viewer.all_columns_maximized

    viewer.toggle_maximize_all_cols()

    snapshot = viewer.width_mode_state

    assert snapshot["mode"] == "all"
    assert snapshot["target"] is None
    assert viewer.all_columns_maximized


def test_maximize_no_op_when_column_already_wide(job_runner):
    viewer = make_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("id")

    viewer.toggle_maximize_current_col()

    assert viewer.width_mode_state["mode"] == "default"
    assert viewer.status_message == "'id' already at max width"
    assert viewer.maximized_column_index is None


def test_default_mode_autosize_stretches_visible_columns(job_runner):
    data = {
        "id": [1, 2, 3, 4],
        "name": [
            "short",
            "a much longer piece of text",
            "tiny",
            "moderately sized value",
        ],
        "notes": ["alpha", "beta", "gamma", "delta"],
    }
    df = pl.DataFrame(data)
    sheet = DataSheet(df.lazy(), runner=job_runner)
    viewer = Viewer(sheet, viewport_rows=10, runner=job_runner)

    visible = viewer.visible_cols
    assert visible == ["id", "name", "notes"]

    name_idx = viewer.columns.index("name")
    baseline_name_width = viewer._default_header_widths[name_idx]

    autosized = viewer._autosized_widths
    assert autosized
    name_width = autosized[name_idx]

    assert name_width >= baseline_name_width

    available_inner = max(1, viewer.view_width_chars - (len(visible) + 1))
    effective_total = sum(autosized[viewer.columns.index(col)] for col in visible)

    assert effective_total >= available_inner


def test_single_mode_autosize_keeps_viewport_filled(job_runner):
    viewer = make_viewer(job_runner)
    viewer.cur_col = viewer.columns.index("name")
    viewer.toggle_maximize_current_col()

    visible = viewer.visible_cols
    autosized = viewer._autosized_widths

    assert viewer.width_mode_state["mode"] == "single"
    assert autosized

    available_inner = max(1, viewer.view_width_chars - (len(visible) + 1))
    effective_total = sum(autosized[viewer.columns.index(col)] for col in visible)

    assert effective_total >= available_inner
    target_width = autosized[viewer.columns.index("name")]
    assert target_width >= viewer._header_widths[viewer.columns.index("name")]


def test_maximize_all_reuses_cached_widths(monkeypatch, job_runner):
    viewer = make_viewer(job_runner)
    call_count = 0

    def fake_compute(idx: int) -> int:
        nonlocal call_count
        call_count += 1
        return 100 + idx

    monkeypatch.setattr(viewer, "_compute_content_width", fake_compute)

    viewer.toggle_maximize_all_cols()
    assert call_count == len(viewer.columns)

    call_count = 0
    viewer.update_terminal_metrics()
    assert call_count == 0


def test_maximize_all_expands_to_view_width(job_runner):
    viewer = make_viewer(job_runner)
    viewer.view_width_chars = 60

    viewer.toggle_maximize_all_cols()

    table_text = render_table(viewer, include_status=False, test_mode=True)
    lines = table_text.splitlines()

    assert len(lines) >= 2
    assert len(lines[1]) == viewer.view_width_chars


def test_maximize_all_handles_complex_types(job_runner):
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "list_col": [[1, 2, 3], [4, 5]],
            "struct_col": [{"a": 1, "b": "foo"}, {"a": 2, "b": "bar"}],
        }
    )
    viewer = Viewer(
        DataSheet(df.lazy(), runner=job_runner),
        viewport_rows=4,
        viewport_cols=3,
        runner=job_runner,
    )

    viewer.toggle_maximize_all_cols()

    table_text = render_table(viewer, include_status=False, test_mode=True)

    assert "[1, 2, 3]" in table_text
    assert "{a: 1, b: foo}" in table_text


def test_single_mode_caches_target_width(monkeypatch, job_runner):
    viewer = make_viewer(job_runner)
    call_count = 0

    def fake_compute(idx: int) -> int:
        nonlocal call_count
        call_count += 1
        return 200 + idx

    monkeypatch.setattr(viewer, "_compute_content_width", fake_compute)

    viewer.toggle_maximize_current_col()
    assert call_count == 1

    call_count = 0
    viewer.update_terminal_metrics()
    assert call_count == 0

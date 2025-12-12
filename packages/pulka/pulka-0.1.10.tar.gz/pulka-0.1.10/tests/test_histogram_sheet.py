import math

import polars as pl

from pulka.core.viewer import Viewer
from pulka.render.status_bar import render_status_line
from pulka.render.table import render_table
from pulka.sheets.data_sheet import DataSheet
from pulka.sheets.hist_sheet import HistogramSheet


def test_histogram_initial_bins_freedman(job_runner):
    df = pl.DataFrame({"value": list(range(100))})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", runner=job_runner)

    assert hist_sheet.stats.n == 100
    assert hist_sheet.stats.nulls == 0
    assert hist_sheet.bin_count == 5


def test_histogram_respects_preferred_height_cap(job_runner):
    df = pl.DataFrame({"value": list(range(10_000))})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", preferred_height=12, runner=job_runner)

    assert hist_sheet.bin_count == 12


def test_histogram_small_preferred_height_limits_bins(job_runner):
    df = pl.DataFrame({"value": list(range(1_000))})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", preferred_height=3, runner=job_runner)

    assert hist_sheet.bin_count == 3


def test_histogram_sturges_fallback_for_flat_iqr(job_runner):
    df = pl.DataFrame({"value": [0.0, 0.0, 0.0, 10.0]})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", runner=job_runner)

    assert hist_sheet.bin_count == 2


def test_histogram_render_and_status_updates(job_runner):
    df = pl.DataFrame({"value": [1.0, 2.5, 3.1, 3.9, 5.0, 6.2, 7.4, 8.8, 9.9]})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", runner=job_runner)

    viewer = Viewer(hist_sheet, viewport_rows=6, viewport_cols=80, runner=job_runner)
    viewer.is_hist_view = True
    viewer.freq_source_col = "value"

    table_output = render_table(viewer, test_mode=True)
    assert "hist" in table_output
    assert "\u283f" in table_output  # filled bar segment

    status_line = _status_text(viewer)
    assert "value · n=" not in status_line
    assert viewer.status_message in (None, "")

    hist_sheet.toggle_log_scale()
    status_with_log = _status_text(viewer)
    assert "value · n=" not in status_with_log
    assert viewer.status_message in (None, "")

    previous_bins = hist_sheet.bin_count
    hist_sheet.adjust_bins(1)
    assert hist_sheet.bin_count == previous_bins + 1

    export_df = hist_sheet.export_bins()
    assert set(export_df.columns) == {"bin_left", "bin_right", "count"}


def test_histogram_limits_bins_by_distinct_values(job_runner):
    counts_by_value = {
        0: 499,
        1: 1_481,
        2: 2_241,
        3: 2_247,
        4: 1_671,
        5: 1_013,
        6: 529,
        7: 198,
        8: 77,
        9: 25,
        10: 16,
        11: 2,
        12: 0,
        13: 1,
    }

    values: list[int] = []
    for value, count in counts_by_value.items():
        values.extend([value] * count)

    df = pl.DataFrame({"value": values})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", runner=job_runner)

    series = df["value"].cast(pl.Float64)
    n = series.len()
    iqr = series.quantile(0.75, interpolation="nearest") - series.quantile(
        0.25, interpolation="nearest"
    )
    fd_width = 2 * iqr / (n ** (1 / 3))
    value_range = series.max() - series.min()
    fd_bins = math.ceil(value_range / fd_width) if fd_width > 0 else 0

    distinct_values = sum(1 for count in counts_by_value.values() if count > 0)

    assert fd_bins > distinct_values
    assert hist_sheet.bin_count == distinct_values


def test_histogram_hist_column_dominates_width(job_runner):
    df = pl.DataFrame({"value": list(range(200))})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", preferred_width=120, runner=job_runner)

    hist_sheet.update_layout_for_view(view_width=120)
    widths = hist_sheet.get_column_widths()

    hist_width = widths["hist"]
    from_width = widths["from"]
    to_width = widths["to"]
    count_width = widths["count"]

    assert hist_width > from_width
    assert hist_width > to_width
    assert hist_width > count_width

    viewer = Viewer(hist_sheet, viewport_rows=10, viewport_cols=120, runner=job_runner)
    viewer.is_hist_view = True
    header_widths = viewer._header_widths

    assert len(header_widths) == 4
    assert header_widths[2] == hist_width
    assert header_widths[2] > header_widths[0]
    assert header_widths[2] > header_widths[1]


def test_histogram_viewer_navigation_clamps_to_bins(job_runner):
    df = pl.DataFrame({"value": list(range(50))})
    base_sheet = DataSheet(df.lazy(), runner=job_runner)
    hist_sheet = HistogramSheet(base_sheet, "value", runner=job_runner)

    viewer = Viewer(hist_sheet, viewport_rows=6, viewport_cols=80, runner=job_runner)
    viewer.is_hist_view = True

    # Trigger layout sync so the viewer learns the correct row count.
    render_table(viewer, test_mode=True)

    viewer.move_down(100)
    expected_last_row = max(0, len(hist_sheet) - 1)
    assert viewer.cur_row == expected_last_row

    expected_row0 = max(0, len(hist_sheet) - viewer.view_height)
    assert viewer.row0 == expected_row0

    viewer.move_up(100)
    assert viewer.cur_row == 0
    assert viewer.row0 == 0


def _status_text(viewer: Viewer) -> str:
    return "".join(part for _, part in render_status_line(viewer, test_mode=True))

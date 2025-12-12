"""
Built-in command handlers for Pulka.

This module contains the standard command handlers that are available in both
TUI and headless modes.
"""

# Import for runtime use
import ast
import hashlib
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import CancelledError as FutureCancelledError
from contextlib import suppress
from pathlib import Path
from time import monotonic_ns
from typing import Any

from .. import theme
from ..clipboard import copy_to_clipboard
from ..core.errors import CancelledError
from ..core.sheet import SHEET_FEATURE_PLAN, SHEET_FEATURE_SLICE, sheet_supports
from ..core.viewer import viewer_public_state
from ..data.export import write_view_to_path
from ..theme_palettes import apply_palette, list_palettes
from .registry import CommandContext


def register_builtin_commands(registry):
    """Register all built-in commands."""
    # Navigation commands
    registry.register("down", handle_down, "Move cursor down", 0, repeatable=True)
    registry.register("up", handle_up, "Move cursor up", 0, repeatable=True)
    registry.register("left", handle_left, "Move cursor left", 0, repeatable=True)
    registry.register("right", handle_right, "Move cursor right", 0, repeatable=True)
    registry.register("pagedown", handle_pagedown, "Move down by page", 0, repeatable=True)
    registry.register("pageup", handle_pageup, "Move up by page", 0, repeatable=True)
    registry.register("top", handle_top, "Go to top", 0)
    registry.register("bottom", handle_bottom, "Go to bottom", 0)
    registry.register("first", handle_first, "Go to first column", 0)
    registry.register("last", handle_last, "Go to last column", 0)
    registry.register("slide_left", handle_slide_left, "Slide current column left", 0)
    registry.register("slide_right", handle_slide_right, "Slide current column right", 0)
    registry.register("slide_first", handle_slide_first, "Slide current column to first", 0)
    registry.register("slide_last", handle_slide_last, "Slide current column to last", 0)

    # View commands
    registry.register("sort", handle_sort, "Toggle sort on current column", 0)
    registry.register(
        "filter",
        handle_filter,
        "Apply filter",
        -1,
        ui_hints={"example": 'filter c["price"] > 5'},
    )
    registry.register(
        "filter_value",
        handle_filter_value,
        "Append filter for current cell value",
        0,
    )
    registry.register(
        "filter_value_not",
        handle_filter_value_not,
        "Append negative filter for current cell value",
        0,
    )
    registry.register(
        "filter_eq",
        handle_filter_eq,
        "Apply equality filter",
        1,
        ui_hints={"example": "filter_eq city London"},
    )
    registry.register(
        "sql_filter",
        handle_sql_filter,
        "Apply SQL filter",
        -1,
        ui_hints={"example": "sql_filter SELECT * FROM data WHERE price > 5"},
    )
    registry.register("reset", handle_reset, "Reset filters", 0)
    registry.register(
        "goto",
        handle_goto,
        "Go to column",
        1,
        ui_hints={"example": "goto revenue"},
    )
    registry.register(
        "render",
        handle_render,
        "Render current view",
        0,
        aliases=("print",),
        ui_hints={"example": "render", "force_render": True},
    )
    registry.register(
        "freeze",
        handle_freeze,
        "Freeze rows or columns",
        1,
        ui_hints={"example": "freeze c2"},
    )
    registry.register("unfreeze", handle_unfreeze, "Clear frozen rows and columns", 0)

    # Column operations
    registry.register("hide", handle_hide, "Hide current column", 0)
    registry.register("unhide", handle_unhide, "Unhide all columns", 0)
    registry.register("gv", handle_unhide, "Unhide all columns", 0)
    registry.register(
        "pal",
        handle_palette,
        "Switch highlight colour palette",
        -1,
        ui_hints={"example": "pal 2"},
    )
    registry.register("select_row", handle_select_row, "Toggle selection for current row", 0)
    registry.register(
        "invert_selection",
        handle_invert_selection,
        "Invert selection for visible rows",
        0,
    )
    registry.register(
        "clear_selection",
        handle_clear_selection,
        "Clear all selected rows",
        0,
    )
    registry.register(
        "select_same_value",
        handle_select_same_value,
        "Select rows matching the current cell value",
        0,
    )
    registry.register("undo", handle_undo, "Undo last operation", 0)
    registry.register("redo", handle_redo, "Redo last operation", 0)

    # Clipboard commands
    registry.register(
        "yank_cell",
        handle_yank_cell,
        "Copy the active cell to the clipboard",
        0,
        aliases=("yy",),
    )
    registry.register(
        "yank_path",
        handle_yank_path,
        "Copy the current dataset path to the clipboard",
        0,
        aliases=("yp",),
    )
    registry.register(
        "yank_column",
        handle_yank_column,
        "Copy the current column name to the clipboard",
        0,
        aliases=("yc",),
    )
    registry.register(
        "yank_all_columns",
        handle_yank_all_columns,
        "Copy visible column names as a Python list",
        0,
        aliases=("yac",),
    )
    registry.register(
        "yank_schema",
        handle_yank_schema,
        "Copy the current schema mapping to the clipboard",
        0,
        aliases=("ys",),
    )

    # Maximize operations
    registry.register("maxcol", handle_maxcol, "Toggle maximize current column", 0)
    registry.register("maxall", handle_maxall, "Toggle maximize all columns", 0)

    # Export commands
    registry.register(
        "write",
        handle_write,
        "Export the active view to disk",
        -1,
        aliases=("export",),
        ui_hints={"example": "write output.parquet"},
    )

    # Repro export command
    registry.register("repro_export", handle_repro_export, "Export reproducible dataset slice", -1)

    # Sheet navigation commands
    registry.register("schema", handle_schema, "Show column schema", 0)
    registry.register(
        "browse",
        handle_browse,
        "Open directory browser",
        -1,
        ui_hints={"example": "browse ~/data"},
    )
    registry.register(
        "insight",
        handle_insight,
        "Toggle insight sidecar in the TUI",
        -1,
    )

    # Search commands
    registry.register("search", handle_search, "Search current column", 1)
    registry.register("next_diff", handle_next_diff, "Next search match", 0)
    registry.register("prev_diff", handle_prev_diff, "Previous search match", 0)
    registry.register(
        "search_value_next",
        handle_search_value_next,
        "Search forward for the current cell value",
        0,
    )
    registry.register(
        "search_value_prev",
        handle_search_value_prev,
        "Search backward for the current cell value",
        0,
    )

    # Navigation enhancement commands
    registry.register("center", handle_center, "Center current row", 0)
    registry.register("next_different", handle_next_different, "Next different value", 0)
    registry.register("prev_different", handle_prev_different, "Previous different value", 0)

    # Column navigation commands
    registry.register("first_overall", handle_first_overall, "Go to first column overall", 0)
    registry.register("last_overall", handle_last_overall, "Go to last column overall", 0)

    # Aliases
    registry.register_alias("_", "maxcol")
    registry.register_alias("g_", "maxall")
    registry.register_alias("repro", "repro_export")
    registry.register_alias("save", "write")
    registry.register_alias("?", "schema")
    registry.register_alias("/", "search")
    registry.register_alias("n", "next_diff")
    registry.register_alias("N", "prev_diff")
    registry.register_alias("*", "search_value_next")
    registry.register_alias("#", "search_value_prev")
    registry.register_alias("z", "center")
    registry.register_alias("<", "prev_different")
    registry.register_alias(">", "next_different")
    registry.register_alias("gh", "first_overall")
    registry.register_alias("gl", "last_overall")
    registry.register_alias("H", "slide_left")
    registry.register_alias("L", "slide_right")
    registry.register_alias("d", "hide")
    registry.register_alias("-", "filter_value_not")
    registry.register_alias("gH", "slide_first")
    registry.register_alias("gL", "slide_last")
    registry.register_alias("0", "first")
    registry.register_alias("$", "last")
    registry.register_alias("gg", "top")
    registry.register_alias("G", "bottom")
    registry.register_alias("palette", "pal")
    registry.register_alias("~", "invert_selection")
    registry.register_alias("gu", "clear_selection")
    registry.register_alias(",", "select_same_value")
    registry.register_alias("+", "filter_value")

    # Summary command is provided by the built-in plugin; ensure it is available headless.
    try:
        from pulka_builtin_plugins.summary.plugin import _summary_cmd
    except Exception:  # pragma: no cover - plugin import guard
        pass
    else:
        with registry.provider_scope("pulka-summary"):
            registry.register("summary", _summary_cmd, "Column summary sheet", 0)
            registry.register_alias("C", "summary")
            registry.register_alias("columns", "summary")
            registry.register_alias("cols", "summary")


def _snapshot_state(viewer: Any):
    """Return a public snapshot for ``viewer`` when supported."""

    return viewer_public_state(viewer)


def handle_down(context: CommandContext, args):
    """Move cursor down one row."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_down(1)
            return
        fallback_total_rows = getattr(context.viewer, "_total_rows", None)
        start_ns = monotonic_ns()
        context.viewer.move_down(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        before_row = before_state.cursor.row
        before_row0 = before_state.viewport.row0
        after_row = after_state.cursor.row
        after_row0 = after_state.viewport.row0
        view_height = before_state.visible_row_count or after_state.visible_row_count
        payload = {
            "before_row": before_row,
            "before_row0": before_row0,
            "after_row": after_row,
            "after_row0": after_row0,
            "view_height": view_height,
            "scrolled": after_row0 != before_row0,
        }
        total_rows = (
            before_state.total_rows
            if before_state.total_rows is not None
            else after_state.total_rows
        )
        if total_rows is None:
            total_rows = (
                fallback_total_rows
                if fallback_total_rows is not None
                else after_state.visible_row_count
            )
        if total_rows is not None:
            payload["total_rows"] = total_rows
            payload["hit_bottom"] = after_row >= max(0, total_rows - 1)
        recorder.record_perf(phase="move.down", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_down(1)


def _resolve_active_cell_display(
    viewer: Any, *, max_chars: int | None = 4096
) -> tuple[str, str] | None:
    """Return the formatted display text for the active cell."""

    columns = list(getattr(viewer, "columns", ()) or ())
    if not columns:
        return None

    cur_col = getattr(viewer, "cur_col", 0)
    if cur_col < 0 or cur_col >= len(columns):
        return None

    cur_row = getattr(viewer, "cur_row", 0)
    column_name = columns[cur_col]
    sheet = getattr(viewer, "sheet", None)
    if sheet is None or not sheet_supports(sheet, SHEET_FEATURE_SLICE):
        return None

    try:
        table_slice = sheet.fetch_slice(cur_row, 1, [column_name])
    except Exception:
        return None

    if getattr(table_slice, "height", 0) <= 0:
        return None

    try:
        column = table_slice.column(column_name)
    except Exception:
        return None

    limit = 4096 if max_chars is None else max(0, max_chars)
    formatted_text: str | None = None
    formatter = getattr(column, "formatted", None)
    if callable(formatter):
        try:
            formatted_values = formatter(limit if limit > 0 else 0)
        except Exception:
            formatted_values = ()
        if formatted_values:
            formatted_text = formatted_values[0]

    if formatted_text is None:
        values = getattr(column, "values", ())
        try:
            raw_value = values[0]
        except Exception:
            raw_value = None
        formatted_text = "" if raw_value is None else str(raw_value)

    return column_name, formatted_text


def _resolve_active_dataset_path(context: CommandContext) -> Path | None:
    """Best-effort resolver for the active dataset path."""

    session = getattr(context, "session", None)
    if session is not None:
        dataset_path = getattr(session, "dataset_path", None)
        if dataset_path is not None:
            return _normalise_path(dataset_path)

    viewer = getattr(context, "viewer", None)
    if viewer is None:
        return None
    source = getattr(viewer, "_source_path", None)
    if isinstance(source, Path):
        return _normalise_path(source)
    if isinstance(source, str) and source and not source.startswith("<"):
        return _normalise_path(Path(source))
    return None


def _normalise_path(path: Path) -> Path:
    candidate = path
    with suppress(Exception):
        candidate = candidate.expanduser()
    try:
        return candidate.resolve()
    except Exception:
        return candidate


def _resolve_current_column(viewer: Any) -> str | None:
    if viewer is None:
        return None
    columns = getattr(viewer, "columns", None)
    if not columns:
        return None
    try:
        return viewer.current_colname()
    except Exception:
        pass
    try:
        cur_col = getattr(viewer, "cur_col", 0)
        return columns[cur_col]
    except Exception:
        return None


def _visible_columns(viewer: Any) -> list[str]:
    if viewer is None:
        return []
    try:
        cols = viewer.visible_columns()
    except Exception:
        cols = getattr(viewer, "columns", []) or []
    return list(cols)


def handle_yank_cell(context: CommandContext, args):
    """Copy the active cell's display text to the clipboard."""

    viewer = context.viewer
    result = _resolve_active_cell_display(viewer)
    if result is None:
        viewer.status_message = "nothing to copy"
        return

    column, text = result
    success = copy_to_clipboard(text)
    if success:
        viewer.status_message = f"copied {column} to clipboard"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_path(context: CommandContext, args):
    """Copy the dataset path (when available) to the clipboard."""

    viewer = context.viewer
    path = _resolve_active_dataset_path(context)
    if path is None:
        viewer.status_message = "dataset path unavailable"
        return

    success = copy_to_clipboard(str(path))
    if success:
        viewer.status_message = f"copied {path} to clipboard"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_column(context: CommandContext, args):
    """Copy the current column name to the clipboard."""

    viewer = context.viewer
    column = _resolve_current_column(viewer)
    if column is None:
        viewer.status_message = "no column to copy"
        return

    success = copy_to_clipboard(str(column))
    if success:
        viewer.status_message = f"copied column {column}"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_all_columns(context: CommandContext, args):
    """Copy visible column names as a vertically formatted Python list."""

    viewer = context.viewer
    columns = _visible_columns(viewer)
    if not columns:
        viewer.status_message = "no columns to copy"
        return

    formatted = "[\n" + "\n".join(f"    {repr(col)}," for col in columns) + "\n]"
    success = copy_to_clipboard(formatted)
    if success:
        viewer.status_message = f"copied {len(columns)} columns"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_yank_schema(context: CommandContext, args):
    """Copy the current schema mapping to the clipboard."""

    viewer = context.viewer
    schema_obj = getattr(context.sheet, "schema", None)
    if not schema_obj:
        viewer.status_message = "schema not available"
        return

    if isinstance(schema_obj, Mapping):
        ordered = _visible_columns(viewer) or list(schema_obj.keys())
        lines: list[str] = []
        for name in ordered:
            if name not in schema_obj:
                continue
            dtype = schema_obj.get(name)
            dtype_repr = str(dtype) if dtype is not None else "None"
            lines.append(f"    {repr(name)}: {dtype_repr},")
        if not lines:
            for name, dtype in schema_obj.items():
                dtype_repr = str(dtype) if dtype is not None else "None"
                lines.append(f"    {repr(name)}: {dtype_repr},")
        formatted_schema = "{\n" + "\n".join(lines) + "\n}"
    else:
        formatted_schema = repr(schema_obj)

    success = copy_to_clipboard(formatted_schema)
    if success:
        viewer.status_message = "schema copied"
    else:
        viewer.status_message = "clipboard unavailable"


def handle_up(context: CommandContext, args):
    """Move cursor up one row."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_up(1)
            return
        start_ns = monotonic_ns()
        context.viewer.move_up(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        payload = {
            "before_row": before_state.cursor.row,
            "before_row0": before_state.viewport.row0,
            "after_row": after_state.cursor.row,
            "after_row0": after_state.viewport.row0,
            "view_height": before_state.visible_row_count or after_state.visible_row_count,
            "scrolled": after_state.viewport.row0 != before_state.viewport.row0,
            "hit_top": after_state.cursor.row == 0,
        }
        recorder.record_perf(phase="move.up", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_up(1)


def handle_left(context: CommandContext, args):
    """Move cursor left one column."""
    context.viewer.move_left(1)


def handle_right(context: CommandContext, args):
    """Move cursor right one column."""
    recorder = getattr(context, "recorder", None)
    if recorder and recorder.enabled:
        before_state = _snapshot_state(context.viewer)
        if before_state is None:
            context.viewer.move_right(1)
            return
        start_ns = monotonic_ns()
        context.viewer.move_right(1)
        duration_ms = (monotonic_ns() - start_ns) / 1_000_000
        after_state = _snapshot_state(context.viewer)
        if after_state is None:  # pragma: no cover - defensive
            after_state = before_state
        payload = {
            "before_col": before_state.cursor.col,
            "before_col0": before_state.viewport.col0,
            "after_col": after_state.cursor.col,
            "after_col0": after_state.viewport.col0,
            "visible_cols_before": before_state.visible_column_count or len(before_state.columns),
            "visible_cols_after": after_state.visible_column_count or len(after_state.columns),
        }
        recorder.record_perf(phase="move.right", duration_ms=duration_ms, payload=payload)
        return

    context.viewer.move_right(1)


def handle_pagedown(context: CommandContext, args):
    """Move down by one page."""
    context.viewer.page_down()


def handle_pageup(context: CommandContext, args):
    """Move up by one page."""
    context.viewer.page_up()


def handle_top(context: CommandContext, args):
    """Go to the top row."""
    context.viewer.go_top()


def handle_bottom(context: CommandContext, args):
    """Go to the bottom row."""
    context.viewer.go_bottom()


def handle_first(context: CommandContext, args):
    """Go to the first visible column."""
    context.viewer.first_col()


def handle_last(context: CommandContext, args):
    """Go to the last visible column."""
    context.viewer.last_col()


def handle_slide_left(context: CommandContext, args):
    """Slide the current column one position to the left."""
    context.viewer.slide_column_left()


def handle_slide_right(context: CommandContext, args):
    """Slide the current column one position to the right."""
    context.viewer.slide_column_right()


def handle_slide_first(context: CommandContext, args):
    """Slide the current column to the first visible slot."""
    context.viewer.slide_column_to_start()


def handle_slide_last(context: CommandContext, args):
    """Slide the current column to the last visible slot."""
    context.viewer.slide_column_to_end()


def handle_sort(context: CommandContext, args):
    """Toggle sort on the current column."""
    context.viewer.toggle_sort()
    context.sheet = context.viewer.sheet


def handle_filter_eq(context: CommandContext, args: list[str]) -> None:
    """Apply a simple equality filter based on column/value tokens."""

    if not args:
        raise ValueError("filter_eq command requires column and value arguments")

    raw = args[0].strip()
    if not raw:
        raise ValueError("filter_eq command requires column and value arguments")

    column, value = (raw.split(None, 1) + [""])[:2]
    if not column or not value:
        raise ValueError("filter_eq command requires format: filter_eq <column> <value>")

    if column not in context.viewer.columns:
        raise ValueError(f"Unknown column: {column}")

    value = value.strip()
    if not value:
        raise ValueError("filter_eq command requires a non-empty value")

    try:
        literal = ast.literal_eval(value)
    except Exception:
        value_expr = repr(value)
    else:
        value_expr = repr(literal)

    safe_column = column.replace('"', '\\"')
    filter_expr = f'c["{safe_column}"] == {value_expr}'
    handle_filter(context, [filter_expr])


def handle_filter_value(context: CommandContext, args: list[str]) -> None:
    """Append a filter for the active cell's value on the current column."""

    context.viewer.append_filter_for_current_value()
    context.sheet = context.viewer.sheet


def handle_filter_value_not(context: CommandContext, args: list[str]) -> None:
    """Append a negative filter for the active cell's value on the current column."""

    context.viewer.append_negative_filter_for_current_value()
    context.sheet = context.viewer.sheet


def handle_filter(context: CommandContext, args):
    """Apply a filter to the current sheet."""
    mode = "replace"
    if len(args) >= 2 and args[-1].strip().lower() in {"replace", "append"}:
        mode = args[-1].strip().lower()
        filter_expr = " ".join(args[:-1])
    else:
        filter_expr = " ".join(args)
    filter_expr = filter_expr or None
    context.viewer.apply_filter(filter_expr, mode=mode)
    context.sheet = context.viewer.sheet


def handle_sql_filter(context: CommandContext, args):
    """Apply an SQL WHERE-clause filter to the current sheet."""
    mode = "replace"
    if len(args) >= 2 and args[-1].strip().lower() in {"replace", "append"}:
        mode = args[-1].strip().lower()
        filter_sql = " ".join(args[:-1])
    else:
        filter_sql = " ".join(args)
    filter_sql = filter_sql or None
    context.viewer.apply_sql_filter(filter_sql, mode=mode)
    context.sheet = context.viewer.sheet


def handle_reset(context: CommandContext, args):
    """Reset all filters and sorting."""
    context.viewer.reset_filters()
    context.sheet = context.viewer.sheet


def handle_freeze(context: CommandContext, args):
    """Freeze rows or columns based on the provided spec."""
    if not args:
        raise ValueError("usage: freeze c<number>|r<number>")

    spec = args[0].strip().lower()
    if not spec:
        raise ValueError("usage: freeze c<number>|r<number>")

    viewer = context.viewer

    if spec[0] == "c":
        count_text = spec[1:]
        try:
            count = int(count_text) if count_text else 1
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("freeze columns expects an integer count") from exc
        viewer.set_frozen_columns(max(0, count))
        actual = len(getattr(viewer, "frozen_columns", []))
        if actual:
            plural = "column" if actual == 1 else "columns"
            viewer.status_message = f"frozen {actual} {plural}"
        else:
            viewer.status_message = "no columns frozen"
    elif spec[0] == "r":
        count_text = spec[1:]
        try:
            count = int(count_text) if count_text else 1
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("freeze rows expects an integer count") from exc
        viewer.set_frozen_rows(max(0, count))
        if count > 0:
            plural = "row" if count == 1 else "rows"
            viewer.status_message = f"frozen first {count} {plural}"
        else:
            viewer.status_message = "no rows frozen"
    else:
        raise ValueError("usage: freeze c<number>|r<number>")


def handle_unfreeze(context: CommandContext, args):
    """Clear any frozen rows or columns."""
    viewer = context.viewer
    viewer.clear_freeze()
    viewer.status_message = "unfroze rows and columns"


def handle_goto(context: CommandContext, args):
    """Go to a specific column."""
    if not args:
        return
    col_name = args[0]
    try:
        col_idx = context.viewer.columns.index(col_name)
        context.viewer.cur_col = col_idx
        if col_idx < context.viewer.col0:
            context.viewer.col0 = col_idx
        elif col_idx >= context.viewer.col0 + len(context.viewer.visible_cols):
            # Adjust viewport to show the column
            context.viewer.col0 = col_idx
        context.viewer.clamp()
    except ValueError:
        # Column not found - could raise error or ignore
        pass


def handle_render(context: CommandContext, args):
    """Render command - primarily for headless mode."""
    # This command typically just signals that a render should happen
    # The actual rendering is handled by the calling code
    pass


def handle_hide(context: CommandContext, args):
    """Hide the current column."""
    context.viewer.hide_current_column()


def handle_unhide(context: CommandContext, args):
    """Unhide all hidden columns."""
    context.viewer.unhide_all_columns()


def handle_palette(context: CommandContext, args):
    """Switch the active highlight palette."""

    if not args or (args and args[0].lower() in {"list", "ls"}):
        labels = ", ".join(f"{palette.key} {palette.label}" for palette in list_palettes())
        viewer = getattr(context, "viewer", None)
        if viewer is not None:
            viewer.status_message = f"palettes → {labels}"
        return

    palette_id = args[0]
    apply_palette(palette_id)

    screen = getattr(context, "screen", None)
    if screen is not None:
        app = getattr(screen, "app", None)
        if app is not None:
            app.style = theme.APP_STYLE
        with suppress(Exception):
            screen.refresh(skip_metrics=True)

    viewer = getattr(context, "viewer", None)
    if viewer is not None:
        viewer.status_message = None


def handle_select_row(context: CommandContext, args):
    """Toggle selection for the focused row."""

    context.viewer.toggle_row_selection()


def handle_invert_selection(context: CommandContext, args):
    """Invert selection for the current viewport."""

    context.viewer.invert_selection()


def handle_clear_selection(context: CommandContext, args):
    """Clear all selected rows."""

    context.viewer.clear_row_selection()


def handle_select_same_value(context: CommandContext, args: list[str]) -> None:
    """Select rows that share the current cell's value in the active column."""

    context.viewer.select_matching_value_rows()


def handle_undo(context: CommandContext, args):
    """Undo the last operation."""
    context.viewer.undo_last_operation()


def handle_redo(context: CommandContext, args):
    """Redo the last undone operation."""
    context.viewer.redo_last_operation()


def handle_maxcol(context: CommandContext, args):
    """Toggle maximize current column."""
    context.viewer.toggle_maximize_current_col()


def handle_maxall(context: CommandContext, args):
    """Toggle maximize all columns."""
    context.viewer.toggle_maximize_all_cols()


def handle_write(context: CommandContext, args):
    """Export the active sheet to a user-provided path."""

    viewer = context.viewer
    recorder = _active_recorder(context)

    if not args:
        _update_status(viewer, recorder, "write requires a destination path")
        return

    raw_destination = args[0]
    try:
        destination = _resolve_destination_path(raw_destination)
    except Exception as exc:  # pragma: no cover - defensive
        _update_status(viewer, recorder, f"write path error: {exc}")
        return

    try:
        format_hint, option_values = _parse_write_options(args[1:])
    except ValueError as exc:
        _update_status(viewer, recorder, f"write option error: {exc}")
        return

    sheet = viewer.sheet
    if not sheet_supports(sheet, SHEET_FEATURE_PLAN):
        _update_status(viewer, recorder, "write requires a plan-capable sheet")
        return

    plan_snapshot = getattr(sheet, "plan", None)
    options_mapping = dict(option_values) if option_values else {}
    export_options = options_mapping or None
    screen = getattr(context, "screen", None)
    runner = getattr(getattr(context, "session", None), "job_runner", None)

    if screen is None or runner is None:
        _execute_write_now(
            sheet,
            plan_snapshot,
            destination,
            format_hint,
            export_options,
            viewer,
            recorder,
        )
        return

    _update_status(viewer, recorder, "Export in progress...")

    job_tag = _make_write_job_tag(destination)

    def _job(_: int) -> Path:
        snapshot = _snapshot_sheet_for_export(sheet, plan_snapshot)
        return write_view_to_path(
            snapshot,
            destination,
            format_hint=format_hint,
            options=export_options,
        )

    try:
        future = runner.submit(sheet, job_tag, _job, cache_result=False)
    except Exception as exc:  # pragma: no cover - defensive
        _update_status(viewer, recorder, f"write error: {exc}")
        return

    notifier = _make_write_completion_notifier(screen)
    handle = _WriteJobHandle(future, destination, recorder, on_done=notifier)
    jobs = getattr(screen, "_jobs", None)
    if isinstance(jobs, dict):
        previous = jobs.get(viewer)
        if previous is not None and hasattr(previous, "cancel"):
            with suppress(Exception):
                previous.cancel()
        jobs[viewer] = handle


def handle_repro_export(context: CommandContext, args):
    """Export a reproducible dataset slice."""
    from ..logging.redaction import redact_path

    # Parse arguments
    row_margin = 10
    include_all_columns = False

    # Parse possible arguments
    for arg in args:
        if arg.startswith("rows="):
            try:
                row_margin = int(arg.split("=", 1)[1])
            except (ValueError, IndexError):
                context.viewer.status_message = f"invalid row margin: {arg}"
                return
        elif arg.startswith("all_columns="):
            try:
                include_all_columns = arg.split("=", 1)[1].lower() in ("true", "1", "yes")
            except (ValueError, IndexError):
                context.viewer.status_message = f"invalid all_columns value: {arg}"
                return

    # Get the recorder from context - may not be available
    recorder = getattr(context, "recorder", None)
    if recorder is None:
        context.viewer.status_message = "recorder not available"
        return

    try:
        # Call the export method on the recorder
        export_path = recorder.export_repro_slice(
            session=context.session,  # Pass the session
            row_margin=row_margin,
            include_all_columns=include_all_columns,
        )

        # Show status message with redacted path basename
        redacted = redact_path(str(export_path))
        context.viewer.status_message = f"repro export → {redacted['basename'][:20]}…"

    except Exception as e:
        context.viewer.status_message = f"repro export failed: {str(e)[:50]}"


def handle_browse(context: CommandContext, args):
    session = getattr(context, "session", None)
    viewer = getattr(context, "viewer", None)
    if session is None or viewer is None:
        return
    if len(args) > 1:
        viewer.status_message = "browse accepts at most one path"
        return
    target = args[0] if args else None
    try:
        session.open_file_browser(target)
    except ValueError as exc:
        viewer.status_message = str(exc)
    except Exception as exc:  # pragma: no cover - defensive guard
        viewer.status_message = f"browse failed: {exc}"


def handle_schema(context: CommandContext, args):
    """Display column schema information."""
    if not hasattr(context.sheet, "schema"):
        context.viewer.status_message = "schema not available"
        return

    schema = context.sheet.schema
    if not schema:
        context.viewer.status_message = "no schema information"
        return

    # In headless mode, we'll just set a status message with schema info
    # In TUI mode, this would typically open a modal
    schema_info = ", ".join(f"{k}:{v}" for k, v in schema.items())
    context.viewer.status_message = f"schema: {schema_info[:100]}..."


def handle_insight(context: CommandContext, args):
    """Toggle or explicitly control the column insight sidecar."""

    screen = getattr(context, "screen", None)
    if screen is None or not hasattr(screen, "set_insight_panel"):
        context.viewer.status_message = "insight command requires the TUI"
        return
    if not args:
        state = screen.set_insight_panel()
        context.viewer.status_message = "insight panel on" if state else "insight panel off"
        return
    target = args[0].strip().lower()
    if target in {"on", "1", "true", "yes"}:
        screen.set_insight_panel(True)
        context.viewer.status_message = "insight panel on"
    elif target in {"off", "0", "false", "no"}:
        screen.set_insight_panel(False)
        context.viewer.status_message = "insight panel off"
    else:
        context.viewer.status_message = f"unknown insight option: {target}"


def handle_search(context: CommandContext, args):
    """Search current column for substring."""
    if not args or not args[0]:
        context.viewer.status_message = "search requires a search term"
        return

    search_term = args[0]
    try:
        context.viewer.set_search(search_term)
        current = context.viewer.search_text
        if current:
            context.viewer.search(forward=True, include_current=True)
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"
    else:
        context.sheet = context.viewer.sheet


def handle_search_value_next(context: CommandContext, args):
    """Search forward for the active cell value in the current column."""
    try:
        context.viewer.search_value(forward=True, include_current=False, center=True)
    except Exception as exc:
        context.viewer.status_message = f"value search error: {exc}"


def handle_search_value_prev(context: CommandContext, args):
    """Search backward for the active cell value in the current column."""
    try:
        context.viewer.search_value(forward=False, include_current=False, center=True)
    except Exception as exc:
        context.viewer.status_message = f"value search error: {exc}"


def handle_next_diff(context: CommandContext, args):
    """Go to next search match."""
    try:
        search_kind = getattr(context.viewer, "last_search_kind", None)
        found = context.viewer.repeat_last_search(forward=True)
        if search_kind == "value":
            return
        if found:
            context.viewer.status_message = "next match"
        else:
            context.viewer.status_message = "no more matches"
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"


def handle_prev_diff(context: CommandContext, args):
    """Go to previous search match."""
    try:
        search_kind = getattr(context.viewer, "last_search_kind", None)
        found = context.viewer.repeat_last_search(forward=False)
        if search_kind == "value":
            return
        if found:
            context.viewer.status_message = "previous match"
        else:
            context.viewer.status_message = "no more matches"
    except Exception as exc:
        context.viewer.status_message = f"search error: {exc}"


def handle_center(context: CommandContext, args):
    """Center current row in viewport."""
    context.viewer.center_current_row()
    context.viewer.status_message = "centered"


def handle_next_different(context: CommandContext, args):
    """Navigate to next different value in current column."""
    if context.viewer.next_different_value():
        context.viewer.center_current_row()
        context.viewer.status_message = "next different value"
    else:
        context.viewer.status_message = "no more different values"


def handle_prev_different(context: CommandContext, args):
    """Navigate to previous different value in current column."""
    if context.viewer.prev_different_value():
        context.viewer.center_current_row()
        context.viewer.status_message = "previous different value"
    else:
        context.viewer.status_message = "no more different values"


def handle_first_overall(context: CommandContext, args):
    """Go to first column overall (adjusts viewport)."""
    context.viewer.first_col_overall()


def handle_last_overall(context: CommandContext, args):
    """Go to last column overall (adjusts viewport)."""
    context.viewer.last_col_overall()


# ---------------------------------------------------------------------------
# Helpers for export command
# ---------------------------------------------------------------------------


def _active_recorder(context: CommandContext):
    recorder = getattr(context, "recorder", None)
    if recorder is None or not getattr(recorder, "enabled", False):
        return None
    return recorder


_STATUS_MESSAGE_MAX_LENGTH = 96


def _normalise_status_message(message: str) -> str:
    """Return a single-line status message clamped to a sane length."""

    collapsed = " ".join(str(message).split())
    if not collapsed:
        return ""
    if len(collapsed) <= _STATUS_MESSAGE_MAX_LENGTH:
        return collapsed
    # Reserve room for an ellipsis to keep the message readable.
    trim_length = max(1, _STATUS_MESSAGE_MAX_LENGTH - 1)
    return f"{collapsed[:trim_length]}…"


def _update_status(viewer: Any, recorder: Any | None, message: str) -> None:
    normalised = _normalise_status_message(message)
    viewer.status_message = normalised
    if recorder is None or not normalised:
        return
    try:
        enabled = getattr(recorder, "enabled", False)
    except Exception:  # pragma: no cover - defensive
        enabled = False
    if not enabled:
        return
    with suppress(Exception):
        recorder.record_status(normalised)


def _resolve_destination_path(raw: str) -> Path:
    destination = Path(raw).expanduser()
    if not destination.is_absolute():
        destination = Path.cwd() / destination
    return destination.resolve()


def _parse_write_options(option_args: Sequence[str]) -> tuple[str | None, dict[str, Any]]:
    format_hint: str | None = None
    options: dict[str, Any] = {}
    for raw in option_args:
        if "=" not in raw:
            raise ValueError(f"option requires key=value: {raw}")
        key, value_text = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("option key cannot be empty")
        value_text = value_text.strip()
        if value_text:
            try:
                parsed_value = ast.literal_eval(value_text)
            except (SyntaxError, ValueError):
                parsed_value = value_text
        else:
            parsed_value = ""
        if key.lower() == "format":
            hint = str(parsed_value).strip()
            format_hint = hint.lstrip(".") if hint.startswith(".") else hint or None
        else:
            options[key] = parsed_value
    return format_hint, options


def _format_destination(destination: Path | str) -> str:
    candidate = Path(destination)
    return candidate.name or candidate.as_posix()


def _make_write_job_tag(destination: Path) -> str:
    digest = hashlib.sha1(destination.as_posix().encode("utf-8")).hexdigest()
    return f"command.write::{digest}"


def _snapshot_sheet_for_export(sheet: Any, plan: Any) -> Any:
    if plan is None:
        return sheet
    with_plan = getattr(sheet, "with_plan", None)
    if not callable(with_plan):
        return sheet
    try:
        return with_plan(plan)
    except Exception:  # pragma: no cover - defensive
        return sheet


def _execute_write_now(
    sheet: Any,
    plan: Any,
    destination: Path,
    format_hint: str | None,
    options: dict[str, Any] | None,
    viewer: Any,
    recorder: Any | None,
) -> None:
    snapshot = _snapshot_sheet_for_export(sheet, plan)
    try:
        result = write_view_to_path(
            snapshot,
            destination,
            format_hint=format_hint,
            options=options,
        )
    except Exception as exc:
        _update_status(viewer, recorder, f"write error: {exc}")
        return
    dest_label = _format_destination(result)
    _update_status(viewer, recorder, f"Export saved to: {dest_label}")


def _make_write_completion_notifier(screen: Any) -> Callable[[], None] | None:
    """Return a callback that schedules a screen refresh when a write job finishes."""

    if screen is None:
        return None

    refresh = getattr(screen, "refresh", None)
    ui_hooks = getattr(screen, "_viewer_ui_hooks", None)
    invalidate = getattr(ui_hooks, "invalidate", None) if ui_hooks is not None else None
    call_soon = getattr(ui_hooks, "call_soon", None) if ui_hooks is not None else None

    def _invoke_refresh() -> None:
        if callable(refresh):
            try:
                refresh(skip_metrics=True)
            except TypeError:
                refresh()
            except Exception:
                return
            return
        if callable(invalidate):
            try:
                invalidate()
            except Exception:
                return

    if callable(call_soon):

        def _notify() -> None:
            def _wrapped() -> None:
                _invoke_refresh()

            try:
                call_soon(_wrapped)
            except Exception:
                _invoke_refresh()

        return _notify

    if callable(refresh) or callable(invalidate):

        def _notify() -> None:
            _invoke_refresh()

        return _notify

    return None


class _WriteJobHandle:
    """Adapter for job-runner futures polled by the TUI screen."""

    def __init__(
        self,
        future: Any,
        destination: Path,
        recorder: Any | None,
        *,
        on_done: Callable[[], None] | None = None,
    ):
        self._future = future
        self._destination = destination
        self._recorder = recorder
        self._on_done = on_done
        self._on_done_called = False

        add_done_callback = getattr(future, "add_done_callback", None)
        if callable(add_done_callback) and on_done is not None:

            def _fire(_completed_future: Any) -> None:
                self._trigger_on_done()

            with suppress(Exception):
                add_done_callback(_fire)

    def cancel(self) -> None:
        future = self._future
        if future is None:
            return
        if hasattr(future, "cancel"):
            with suppress(Exception):
                future.cancel()

    def consume_update(self, viewer: Any) -> bool:
        future = self._future
        if future is None:
            self._trigger_on_done()
            return True
        if not future.done():
            return False
        try:
            result = future.result()
        except (CancelledError, FutureCancelledError):
            _update_status(viewer, self._recorder, "write canceled")
            self._trigger_on_done()
            return True
        except Exception as exc:
            _update_status(viewer, self._recorder, f"write error: {exc}")
            self._trigger_on_done()
            return True
        destination = getattr(result, "value", None)
        if destination is None:
            destination = self._destination
        dest_label = _format_destination(destination)
        _update_status(viewer, self._recorder, f"Export saved to: {dest_label}")
        self._trigger_on_done()
        return True

    def _trigger_on_done(self) -> None:
        callback = self._on_done
        if callback is None or self._on_done_called:
            return
        self._on_done_called = True
        try:
            callback()
        except Exception:
            return

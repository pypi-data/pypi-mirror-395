"""Transpose sheet plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from pulka.core.engine.contracts import EnginePayloadHandle
from pulka.core.engine.polars_adapter import unwrap_lazyframe_handle
from pulka.core.formatting import _polars_format_transpose_values
from pulka.core.jobs import JobRunner
from pulka.core.sheet import Sheet
from pulka.core.viewer import Viewer, ViewStack
from pulka.sheets.data_sheet import DataSheet

_TRANSPOSE_FROZEN_COLUMNS = 2

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from pulka.api.session import Session
    from pulka.command.registry import CommandContext, CommandRegistry
    from pulka.data.scanners import ScannerRegistry
    from pulka.sheets.registry import SheetRegistry


class TransposeSheet(DataSheet):
    """Sheet implementation for transposed views."""

    default_frozen_columns = _TRANSPOSE_FROZEN_COLUMNS

    def __init__(
        self,
        base_sheet: Sheet,
        sample_rows: int | None = None,
        start_row: int = 0,
        *,
        runner: JobRunner,
    ) -> None:
        self.source_sheet = base_sheet
        self.sample_rows = sample_rows
        self.requested_sample_rows = sample_rows
        self.actual_sample_rows: int = 0
        self.start_row = start_row

        transposed_df = self._build_transpose_df(base_sheet, sample_rows, start_row)
        self.data = transposed_df
        if runner is None:  # pragma: no cover - defensive guard
            msg = "TransposeSheet requires a JobRunner instance"
            raise ValueError(msg)
        super().__init__(transposed_df.lazy(), runner=runner)

    def _build_transpose_df(
        self, base_sheet: Sheet, sample_rows: int | None, start_row: int = 0
    ) -> pl.DataFrame:
        if sample_rows is None:
            default_rows = 64
            max_rows = 1000
            sample_rows = max(1, min(max_rows, default_rows))

        self.sample_rows = sample_rows
        base_lf_candidate = getattr(base_sheet, "lf", getattr(base_sheet, "lf0", None))
        if base_lf_candidate is None:
            self.actual_sample_rows = 0
            return pl.DataFrame({"column": [], "dtype": []})
        if isinstance(base_lf_candidate, EnginePayloadHandle):
            base_lf = unwrap_lazyframe_handle(base_lf_candidate)
        else:
            base_lf = base_lf_candidate

        sample_df = base_lf.slice(start_row, sample_rows).collect()
        actual_sample = sample_df.height
        self.actual_sample_rows = actual_sample

        columns = getattr(base_sheet, "columns", [])
        source_schema = getattr(base_sheet, "schema", {})
        dtype_strings = [str(source_schema.get(name, "?")) for name in columns]

        data: dict[str, list[str | None]] = {
            "column": columns,
            "dtype": dtype_strings,
        }

        if actual_sample:
            formatted_columns: dict[str, list[str | None]] = {}
            for name in columns:
                if name in sample_df.columns:
                    try:
                        col_series = sample_df[name]
                        formatted_columns[name] = _polars_format_transpose_values(col_series)
                    except Exception:
                        formatted_columns[name] = [None] * actual_sample
                else:
                    formatted_columns[name] = [None] * actual_sample

            for idx in range(actual_sample):
                key = f"row_{start_row + idx + 1}"
                values: list[str | None] = []
                for name in columns:
                    formatted_col = formatted_columns.get(name, [])
                    val = formatted_col[idx] if idx < len(formatted_col) else None
                    values.append(val)
                data[key] = values

        schema = dict.fromkeys(data.keys(), pl.Utf8)
        transpose_df = pl.DataFrame(data, schema=schema)
        return transpose_df


def open_transpose_viewer(
    base_viewer: Viewer,
    *,
    session: Session | None = None,
    view_stack: ViewStack | None = None,
    sample_rows: int | None = None,
    start_row: int = 0,
) -> Viewer:
    """Open a transpose view derived from ``base_viewer``."""

    helper = getattr(session, "open_sheet_view", None) if session is not None else None
    if callable(helper):
        derived_viewer = helper(
            "transpose",
            base_viewer=base_viewer,
            sample_rows=sample_rows,
            start_row=start_row,
        )
        derived_viewer.status_message = "transpose view"
        return derived_viewer

    transpose_sheet = TransposeSheet(
        base_viewer.sheet,
        sample_rows=sample_rows,
        start_row=start_row,
        runner=base_viewer.job_runner,
    )

    if view_stack is not None:
        derived_viewer = Viewer(
            transpose_sheet,
            viewport_rows=base_viewer._viewport_rows_override,
            viewport_cols=base_viewer._viewport_cols_override,
            source_path=base_viewer._source_path,
            session=session,
            runner=base_viewer.job_runner,
        )
        derived_viewer.status_message = "transpose view"
        view_stack.push(derived_viewer)
        return view_stack.active or derived_viewer

    base_viewer.replace_sheet(transpose_sheet, source_path=None)
    base_viewer.status_message = "transpose view"
    return base_viewer


def _open_transpose_from_context(
    context: CommandContext,
    *,
    sample_rows: int | None,
    start_row: int,
    status_message: str = "transpose view",
) -> None:
    if not context.viewer.columns:
        context.viewer.status_message = "no columns available"
        return

    session = getattr(context, "session", None) or context.viewer.session
    view_stack = getattr(context, "view_stack", None)
    if view_stack is None and session is not None:
        view_stack = getattr(session, "view_stack", None)

    try:
        new_viewer = open_transpose_viewer(
            context.viewer,
            session=session,
            view_stack=view_stack,
            sample_rows=sample_rows,
            start_row=max(0, start_row),
        )
        context.viewer = new_viewer
        context.sheet = new_viewer.sheet
        new_viewer.status_message = status_message
    except Exception as exc:  # pragma: no cover - guardrail
        context.viewer.status_message = f"transpose error: {exc}"[:120]


def _transpose_cmd(context: CommandContext, args: list[str]) -> None:
    sample_rows: int | None = None
    start_row = 0

    for arg in args:
        if arg.isdigit():
            sample_rows = int(arg)
        elif arg.startswith("start="):
            try:
                start_row = int(arg.split("=", 1)[1])
            except (ValueError, IndexError):
                context.viewer.status_message = f"invalid start row: {arg}"
                return

    _open_transpose_from_context(
        context, sample_rows=sample_rows, start_row=start_row, status_message="transpose view"
    )


def _transpose_current_row_cmd(context: CommandContext, args: list[str]) -> None:
    _ = args
    current_row = max(0, getattr(context.viewer, "cur_row", 0))
    _open_transpose_from_context(
        context,
        sample_rows=1,
        start_row=current_row,
        status_message=f"transpose row {current_row + 1}",
    )


def register(
    *,
    commands: CommandRegistry | None = None,
    sheets: SheetRegistry | None = None,
    scanners: ScannerRegistry | None = None,
) -> None:
    if sheets is not None:
        kinds = set(sheets.list_kinds())
        if "transpose" not in kinds:
            sheets.register_sheet("transpose", TransposeSheet)

    if commands is not None:
        commands.register("transpose", _transpose_cmd, "Transpose view", -1)
        commands.register(
            "transpose_row",
            _transpose_current_row_cmd,
            "Transpose the current row",
            0,
        )
        commands.register_alias("T", "transpose")
        commands.register_alias("t", "transpose_row")

        def _open_transpose(context: CommandContext) -> None:
            _transpose_cmd(context, [])

        commands.register_sheet_opener("transpose", _open_transpose)

    _ = scanners

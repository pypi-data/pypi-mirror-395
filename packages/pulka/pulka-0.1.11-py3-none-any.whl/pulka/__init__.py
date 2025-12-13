"""Public package interface for Pulka.

The refactored architecture keeps core components in dedicated modules; this file
now simply re-exports the main entry points for backwards compatibility.
"""

from __future__ import annotations

from importlib import metadata as importlib_metadata

from .api import Runtime, Session, open
from .cli import main
from .core.viewer import Viewer
from .data.filter_lang import ColumnNamespace, FilterError
from .data.scan import _csv_schema_overrides, scan_any
from .derived import (
    build_column_summary_lazy as _build_column_summary_lazy,
)
from .derived import (
    build_freq_lazy as _build_freq_lazy,
)
from .derived import (
    build_transpose_df as _build_transpose_df,
)
from .headless.runner import (
    apply_script_command,
    load_script_file,
    run_script_mode,
)
from .render.status_bar import render_status_line
from .render.table import render_table
from .theme import THEME
from .utils import _get_int_env

try:
    __version__ = importlib_metadata.version("pulka")
except importlib_metadata.PackageNotFoundError:
    __version__ = "0.0.dev0"

__all__ = [
    "__version__",
    "Runtime",
    "Session",
    "Viewer",
    "apply_script_command",
    "build_column_summary_lazy",
    "build_freq_lazy",
    "build_transpose_df",
    "_build_column_summary_lazy",
    "_build_freq_lazy",
    "_build_transpose_df",
    "ColumnNamespace",
    "FilterError",
    "THEME",
    "_csv_schema_overrides",
    "_get_int_env",
    "load_script_file",
    "main",
    "open",
    "render_status_line",
    "render_table",
    "run_script_mode",
    "scan_any",
]

# Backwards-compatible aliases with legacy underscore-prefixed names
build_column_summary_lazy = _build_column_summary_lazy
build_freq_lazy = _build_freq_lazy
build_transpose_df = _build_transpose_df

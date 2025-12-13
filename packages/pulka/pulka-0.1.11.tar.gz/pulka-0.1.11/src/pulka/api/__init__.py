"""
Public API for Pulka - a tiny, fast VisiData-like tabular viewer for Polars.

This module provides the main entry points for programmatic access to Pulka.
"""

from .runtime import Runtime
from .session import Session, open

__all__ = ["Runtime", "Session", "open"]

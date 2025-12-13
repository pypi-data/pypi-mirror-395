"""Utilities for lightweight CLI progress feedback."""

from __future__ import annotations

import itertools
import sys
import threading
from collections.abc import Iterable
from contextlib import AbstractContextManager
from pathlib import Path
from types import TracebackType
from typing import TextIO

__all__ = ["SpinnerFeedback", "file_write_feedback"]


class SpinnerFeedback(AbstractContextManager["SpinnerFeedback"]):
    """Render a simple spinner to stderr while a long-running action executes."""

    def __init__(
        self,
        message: str,
        *,
        stream: TextIO | None = None,
        frames: Iterable[str] | None = None,
        interval: float = 0.12,
    ) -> None:
        self._message = message.rstrip()
        self._stream = stream if stream is not None else sys.stderr
        if frames is not None:
            self._frames = tuple(frames)
        else:
            # Lightweight braille-inspired spinner so CLI feedback matches TUI affordances.
            self._frames = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
        self._interval = interval
        self._thread: threading.Thread | None = None
        self._stop_event: threading.Event | None = None
        self._use_spinner = False
        self._line_width = len(self._message) + 2

    def __enter__(self) -> SpinnerFeedback:
        stream_is_tty = getattr(self._stream, "isatty", None)
        self._use_spinner = bool(self._frames) and callable(stream_is_tty) and stream_is_tty()
        if not self._use_spinner:
            print(f"{self._message}...", file=self._stream, flush=True)
            return self

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        first_frame = self._frames[0] if self._frames else ""
        line = f"{self._message} {first_frame}"
        self._line_width = max(self._line_width, len(line))
        self._stream.write(line)
        self._stream.flush()
        self._thread.start()
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:
        if not self._use_spinner:
            return None
        if self._stop_event is None or self._thread is None:
            return None
        self._stop_event.set()
        self._thread.join()
        blank = " " * self._line_width
        self._stream.write(f"\r{blank}\r")
        self._stream.flush()
        return None

    def _spin(self) -> None:
        assert self._stop_event is not None
        if not self._frames:
            return
        frames_iter = itertools.cycle(self._frames)
        # Skip the frame that was printed synchronously on entry.
        next(frames_iter)
        while not self._stop_event.wait(self._interval):
            frame = next(frames_iter)
            line = f"{self._message} {frame}"
            self._line_width = max(self._line_width, len(line))
            self._stream.write(f"\r{line}")
            self._stream.flush()


def file_write_feedback(destination: str | Path, *, noun: str = "dataset") -> SpinnerFeedback:
    """Return a spinner context for writing files to disk."""

    path = Path(destination)
    label = path.name or path.as_posix()
    message = f"Writing {noun} to {label}"
    return SpinnerFeedback(message)

"""Lightweight rendering helper for the column insight sidecar."""

from __future__ import annotations

import math
import textwrap
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...core.column_insight import (
    LOW_CARDINALITY_NUMERIC_LIMIT,
    CellPreview,
    ColumnInsight,
    InsightHistogram,
    TopValue,
)
from ...core.formatting import _format_number_with_thousands_separator
from ...logging.redaction import RedactionPolicy, redact_path
from ...render.decimal_alignment import apply_decimal_alignment, compute_decimal_alignment
from ...render.display import display_width, pad_left_display, pad_right_display

PanelLine = list[tuple[str, str]]
_HEADER_STYLE = "class:table.header"
_BODY_STYLE = "class:table.cell"
_NULL_STYLE = "class:table.cell.null"
_MAX_FRACTION_DIGITS = 6
_TEMPORAL_PREFIXES = ("date", "datetime", "time", "duration")
_STRINGY_PREFIXES = ("str", "string", "utf", "categorical", "enum")
_NUMERIC_PREFIXES = ("int", "uint", "float", "decimal")
_PTB_UNITS: tuple[tuple[Decimal, str], ...] = (
    (Decimal("1e15"), "P"),
    (Decimal("1e12"), "T"),
    (Decimal("1e9"), "B"),
)
_HISTOGRAM_MAX_COLUMNS = 64
_HISTOGRAM_WIDTH_RATIO = 0.5


@dataclass(frozen=True, slots=True)
class _LabeledEntry:
    label: str
    display: str | None
    numeric: Decimal | None = None
    align_right: bool = False


class ColumnInsightPanel:
    """Text-only panel rendered alongside the main table."""

    def __init__(self, *, width: int = 32) -> None:
        self.width = max(20, width)
        self._insight: ColumnInsight | None = None
        self._cell_preview: CellPreview | None = None
        self._status: str = "unavailable"
        self._status_message: str = "Select a column to view stats."
        self._pending_column: str | None = None
        self._pending_histogram_placeholder: bool = False
        self._summary_cache: tuple[ColumnInsight | None, int, list[PanelLine]] | None = None
        self._stats_cache: tuple[ColumnInsight | None, int, list[PanelLine]] | None = None
        self._histogram_cache: tuple[InsightHistogram | None, int, str | None] | None = None

    # ------------------------------------------------------------------
    # State management helpers
    # ------------------------------------------------------------------
    def set_disabled(self, reason: str) -> None:
        self._status = "disabled"
        self._status_message = reason
        self._insight = None
        self._pending_column = None
        self._pending_histogram_placeholder = False
        self._invalidate_render_cache()

    def set_unavailable(self, reason: str) -> None:
        self._status = "unavailable"
        self._status_message = reason
        self._insight = None
        self._pending_column = None
        self._pending_histogram_placeholder = False
        self._invalidate_render_cache()

    def set_loading(self, column: str, *, histogram_expected: bool = False) -> None:
        self._status = "loading"
        self._status_message = f"Computing stats for {column}"
        self._pending_column = column
        self._insight = None
        self._pending_histogram_placeholder = histogram_expected
        self._invalidate_render_cache()

    def set_error(self, message: str) -> None:
        self._status = "error"
        self._status_message = message
        self._pending_column = None
        self._pending_histogram_placeholder = False
        self._invalidate_render_cache()

    def set_insight(self, insight: ColumnInsight) -> None:
        self._insight = insight
        self._status = "ready"
        self._status_message = ""
        self._pending_column = None
        self._pending_histogram_placeholder = False
        self._invalidate_render_cache()

    def set_cell_preview(self, preview: CellPreview | None) -> None:
        self._cell_preview = preview

    def _invalidate_render_cache(self) -> None:
        self._summary_cache = None
        self._stats_cache = None
        self._histogram_cache = None

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------
    def render_text(self) -> str:
        """Return the textual presentation rendered in the TUI."""

        return "\n".join(self._line_text(line) for line in self._render_lines())

    def render_fragments(self) -> StyleAndTextTuples:
        """Return prompt_toolkit fragments with table-themed styling."""

        lines = self._render_lines()
        if not lines:
            return [("", "")]

        fragments: StyleAndTextTuples = []
        for idx, line in enumerate(lines):
            for style, text in line:
                fragments.append((style, text))
            if idx < len(lines) - 1:
                fragments.append(("", "\n"))
        return fragments

    def render_for_recorder(self) -> str:
        """Return snapshot text appended to recorder frames."""

        body = self.render_text()
        if not body:
            return ""
        border_prefix = "│ "
        bordered_lines = [f"{border_prefix}{line}" for line in body.splitlines()]
        return "\n".join(bordered_lines)

    def snapshot_for_recorder(
        self,
        policy: RedactionPolicy | None,
    ) -> dict[str, Any]:
        """Return structured payload describing current state."""

        insight_payload = self._serialize_insight(self._insight, policy)
        cell_payload = self._serialize_cell(self._cell_preview, policy)
        return {
            "status": self._status,
            "message": self._status_message,
            "pending_column": self._pending_column,
            "insight": insight_payload,
            "cell": cell_payload,
        }

    # ------------------------------------------------------------------
    # Internal formatting utilities
    # ------------------------------------------------------------------
    def _render_lines(self) -> list[PanelLine]:
        body = self._render_body_lines()
        lines: list[PanelLine] = [
            self._plain_line("", _BODY_STYLE),
            self._plain_line("Column Insight", _HEADER_STYLE),
        ]
        if body:
            lines.append(self._plain_line("", _BODY_STYLE))
            lines.extend(body)
        return lines

    def _render_body_lines(self) -> list[PanelLine]:
        status = self._status
        insight = self._insight

        if status == "disabled":
            return self._render_message_block(
                "Status",
                [
                    self._status_message or "Insight panel disabled.",
                    "Toggle with `i` or :insight.",
                ],
            )

        if status == "unavailable":
            return self._render_message_block(
                "Status",
                [self._status_message or "Insight unavailable for this sheet."],
            )

        if status == "loading":
            return self._render_placeholder_sections()

        if status == "error":
            message = self._status_message or "Unknown insight error."
            return self._render_message_block("Status", [f"⚠ {message}"])

        if insight is None:
            return self._render_placeholder_sections()

        lines: list[PanelLine] = []
        lines.extend(self._render_summary_section(insight))
        lines.extend(self._render_stats_section(insight))
        lines.extend(self._render_top_values_section(insight))
        lines.extend(self._render_histogram_section(insight))
        lines.extend(self._render_active_cell_block())
        return lines

    def _render_placeholder_sections(self) -> list[PanelLine]:
        lines: list[PanelLine] = []
        lines.extend(self._render_summary_section(None))
        lines.extend(self._render_stats_section(None))
        if self._status == "loading" and self._pending_histogram_placeholder:
            lines.extend(self._render_histogram_placeholder_section())
        lines.extend(self._render_active_cell_block())
        return lines

    def _render_summary_section(self, insight: ColumnInsight | None) -> list[PanelLine]:
        cached = self._summary_cache
        if cached and cached[0] is insight and cached[1] == self.width:
            return cached[2]
        dtype_value: str | None = None
        if insight:
            dtype_value = insight.dtype or "unknown"
        null_value = None
        distinct_value = None
        if insight:
            nulls = insight.null_count or 0
            null_pct = self._fmt_percent(nulls, insight.row_count)
            null_value = f"{null_pct} · {self._fmt_int(nulls)}"
            if insight.distinct_count is not None:
                distinct_value = self._fmt_int(insight.distinct_count)

        summary: list[_LabeledEntry] = [
            _LabeledEntry("Type", dtype_value, align_right=True),
            _LabeledEntry("Nulls", null_value),
            _LabeledEntry("Distinct", distinct_value),
        ]
        lines = self._format_labeled_section(
            "Summary",
            summary,
            placeholder=insight is None,
            align_numeric=False,
        )
        self._summary_cache = (insight, self.width, lines)
        return lines

    def _render_stats_section(self, insight: ColumnInsight | None) -> list[PanelLine]:
        cached = self._stats_cache
        if cached and cached[0] is insight and cached[1] == self.width:
            return cached[2]
        stats = insight.stats or {} if insight else {}
        dtype = insight.dtype if insight else None
        use_evenness = insight is not None and self._should_show_evenness(insight)
        evenness: Decimal | None = None
        evenness_label = "Evenness"
        if use_evenness:
            evenness, approx = self._compute_evenness(insight)
            if approx:
                evenness_label = "Evenness (approx)"
        std_dev = stats.get("std") or stats.get("std_dev")
        ordered_keys = [
            ("Min", stats.get("min")),
            ("p05", stats.get("p05")),
            ("Median", stats.get("median")),
            ("Mean", stats.get("mean")),
            ("p95", stats.get("p95")),
            ("Max", stats.get("max")),
            (evenness_label if use_evenness else "Std dev", evenness if use_evenness else std_dev),
        ]
        entries: list[_LabeledEntry] = []
        for label, value in ordered_keys:
            align_right = self._stat_label_align_right(dtype, label)
            if value is None:
                entries.append(_LabeledEntry(label, None, align_right=align_right))
                continue
            formatted, decimal_value = self._format_stat_value(value)
            entries.append(_LabeledEntry(label, formatted, decimal_value, align_right=align_right))
        lines = self._format_labeled_section(
            "Stats",
            entries,
            pad_before=True,
            placeholder=insight is None,
            align_numeric=True,
        )
        self._stats_cache = (insight, self.width, lines)
        return lines

    def _render_top_values_section(self, insight: ColumnInsight) -> list[PanelLine]:
        if not self._should_show_top_values(insight):
            return []
        top_values = tuple(insight.top_values[:5])
        if not top_values:
            return []

        lines: list[PanelLine] = []
        self._append_section_title(lines, "Top values", pad_before=True)
        for entry in top_values:
            pct = self._fmt_fraction(entry.fraction)
            count = self._fmt_int(entry.count)
            meta = f"{pct} · {count}"
            lines.extend(self._format_top_value_entry(entry, meta))
        return lines

    def _render_histogram_section(self, insight: ColumnInsight | None) -> list[PanelLine]:
        if insight is not None and self._is_low_cardinality_numeric(insight):
            return []
        histogram = insight.histogram if insight else None
        line = self._build_histogram_line(histogram)
        if not line:
            return []
        lines: list[PanelLine] = []
        self._append_section_title(lines, "Histogram", pad_before=True)
        lines.append(self._plain_line(line, _BODY_STYLE))
        return lines

    def _render_histogram_placeholder_section(self) -> list[PanelLine]:
        line = self._build_histogram_placeholder_line()
        if not line:
            return []
        lines: list[PanelLine] = []
        self._append_section_title(lines, "Histogram", pad_before=True)
        lines.append(self._plain_line(line, _BODY_STYLE))
        return lines

    def _format_top_value_entry(self, entry: TopValue, meta: str) -> list[PanelLine]:
        width = self.width
        if width <= 0:
            return []
        gap = 1
        meta_len = len(meta)
        available = width - meta_len - gap
        entry_lines: list[PanelLine] = []
        if available >= 4:
            value_text = self._top_value_label(entry, available)
            clipped_value = self._clip_text(value_text, available)
            padded_value = clipped_value.ljust(available)
            segments = [
                (_BODY_STYLE, padded_value),
                (_BODY_STYLE, " " * gap),
                (_BODY_STYLE, meta),
            ]
            entry_lines.append(self._line_from_segments(segments))
            return entry_lines

        clipped_value = self._clip_text(self._top_value_label(entry, width), width)
        entry_lines.append(self._plain_line(clipped_value, _BODY_STYLE))
        indent = 2 if width - len(meta) > 2 else 0
        prefix = " " * indent
        entry_lines.append(self._plain_line(self._clip_text(f"{prefix}{meta}", width), _BODY_STYLE))
        return entry_lines

    def _build_histogram_line(
        self,
        histogram: InsightHistogram | None,
    ) -> str | None:
        cached = self._histogram_cache
        if cached and cached[0] is histogram and cached[1] == self.width:
            return cached[2]
        if histogram is None:
            self._histogram_cache = (histogram, self.width, None)
            return None
        bins = histogram.bins
        if not bins:
            self._histogram_cache = (histogram, self.width, None)
            return None
        target_chars = max(1, int(self.width * _HISTOGRAM_WIDTH_RATIO))
        char_count = max(1, min(_HISTOGRAM_MAX_COLUMNS, target_chars))
        bin_target = max(2, char_count * 2)
        resampled = self._resample_histogram_bins(bins, bin_target)
        if not resampled:
            self._histogram_cache = (histogram, self.width, None)
            return None
        normalized = [min(1.0, max(0.0, float(value))) for value in resampled]
        # Pad to even length for pairing.
        if len(normalized) < bin_target:
            normalized.extend([0.0] * (bin_target - len(normalized)))
        chars: list[str] = []
        for idx in range(char_count):
            left = normalized[idx * 2] if idx * 2 < len(normalized) else 0.0
            right = normalized[idx * 2 + 1] if idx * 2 + 1 < len(normalized) else 0.0
            chars.append(self._braille_bar_char(left, right))
        if not any(char.strip() for char in chars):
            self._histogram_cache = (histogram, self.width, None)
            return None
        line = "".join(chars)
        self._histogram_cache = (histogram, self.width, line)
        return line

    def _build_histogram_placeholder_line(self) -> str | None:
        target_chars = max(1, int(self.width * _HISTOGRAM_WIDTH_RATIO))
        char_count = max(1, min(_HISTOGRAM_MAX_COLUMNS, target_chars))
        return " " * char_count

    def _braille_bar_char(self, left: float, right: float) -> str:
        bits = 0
        left_level = self._histogram_level(left)
        right_level = self._histogram_level(right)
        if left_level >= 1:
            bits |= 0b0100_0000  # dot 7
        if left_level >= 2:
            bits |= 0b0000_0100  # dot 3
        if left_level >= 3:
            bits |= 0b0000_0010  # dot 2
        if left_level >= 4:
            bits |= 0b0000_0001  # dot 1
        if right_level >= 1:
            bits |= 0b1000_0000  # dot 8
        if right_level >= 2:
            bits |= 0b0010_0000  # dot 6
        if right_level >= 3:
            bits |= 0b0001_0000  # dot 5
        if right_level >= 4:
            bits |= 0b0000_1000  # dot 4
        if bits == 0:
            return " "
        return chr(0x2800 + bits)

    def _histogram_level(self, value: float) -> int:
        clamped = min(1.0, max(0.0, float(value)))
        if clamped <= 0.0:
            return 0
        # Map to 4 bands, ensuring tiny values still show up.
        return min(4, max(1, math.ceil(clamped * 4)))

    def _resample_histogram_bins(self, bins: tuple[float, ...], target: int) -> list[float]:
        source = len(bins)
        if source == 0 or target <= 0:
            return []
        if source == target:
            return [max(0.0, min(1.0, float(value))) for value in bins]
        result: list[float] = []
        for idx in range(target):
            start = idx * source / target
            end = (idx + 1) * source / target
            accum = 0.0
            weight = 0.0
            pos = start
            while pos < end:
                bin_idx = int(pos)
                if bin_idx >= source:
                    bin_idx = source - 1
                next_boundary = min(end, bin_idx + 1)
                segment = max(0.0, next_boundary - pos)
                if segment <= 0:
                    break
                accum += float(bins[bin_idx]) * segment
                weight += segment
                pos = next_boundary
            if weight <= 0:
                result.append(0.0)
            else:
                result.append(max(0.0, min(1.0, accum / weight)))
        return result

    def _stat_label_align_right(self, dtype: str | None, label: str) -> bool:
        if not dtype:
            return False
        lowered = dtype.lower()
        if lowered.startswith(_TEMPORAL_PREFIXES):
            return True
        if label not in {"Min", "Max"}:
            return False
        return lowered.startswith(_STRINGY_PREFIXES)

    def _is_categorical_dtype(self, dtype: str | None) -> bool:
        if not dtype:
            return False
        lowered = dtype.lower()
        return lowered.startswith(_STRINGY_PREFIXES)

    def _is_low_cardinality_numeric(self, insight: ColumnInsight | None) -> bool:
        if insight is None:
            return False
        distinct = insight.distinct_count
        dtype = insight.dtype
        if dtype is None or distinct is None:
            return False
        if distinct < 0 or distinct > LOW_CARDINALITY_NUMERIC_LIMIT:
            return False
        return dtype.lower().startswith(_NUMERIC_PREFIXES)

    def _should_show_top_values(self, insight: ColumnInsight) -> bool:
        if self._is_categorical_dtype(insight.dtype):
            return True
        return self._is_low_cardinality_numeric(insight)

    def _should_show_evenness(self, insight: ColumnInsight) -> bool:
        return self._is_categorical_dtype(insight.dtype) or self._is_low_cardinality_numeric(
            insight
        )

    def _compute_evenness(self, insight: ColumnInsight | None) -> tuple[Decimal | None, bool]:
        if insight is None:
            return None, False
        distinct = insight.distinct_count
        if distinct is None or distinct <= 0:
            return None, False
        non_null_count = insight.non_null_count
        if non_null_count in (None, 0):
            return None, False
        top_values = insight.top_values or ()
        approx = distinct > len(top_values)
        probabilities: list[float] = []
        for entry in top_values:
            fraction = entry.fraction
            if fraction is None or math.isnan(fraction) or fraction < 0:
                return None, False
            probabilities.append(float(fraction))
        total = sum(probabilities)
        rest_categories = max(0, distinct - len(probabilities))
        rest_mass = max(0.0, 1.0 - total) if rest_categories > 0 else 0.0
        if rest_categories > 0:
            tail_prob = rest_mass / rest_categories if rest_categories else 0.0
            probabilities.extend([tail_prob] * rest_categories)
        normalized_denominator = sum(probabilities)
        if normalized_denominator <= 0:
            return None, approx
        if distinct == 1:
            return Decimal("1.000"), False
        normalized = [p / normalized_denominator for p in probabilities if p > 0]
        if not normalized:
            return None, approx
        entropy = -sum(p * math.log2(p) for p in normalized)
        max_entropy = math.log2(distinct)
        if max_entropy <= 0:
            return None, approx
        evenness = entropy / max_entropy
        try:
            return Decimal(str(evenness)).quantize(Decimal("0.001")), approx
        except Exception:
            return None, approx

    def _top_value_label(self, entry: TopValue, limit: int) -> str:
        if limit <= 0:
            return ""
        decimal_value = self._coerce_decimal(entry.value)
        if decimal_value is not None:
            fitted = self._format_decimal_for_width(decimal_value, limit)
            if fitted is not None:
                return fitted
        display = entry.display
        if decimal_value is None and not entry.truncated:
            formatted = self._format_numeric_string(display)
            if formatted is not None and display_width(formatted) <= limit:
                display = formatted
        if entry.truncated and len(display) + 1 <= limit:
            display = f"{display}…"
        return self._clip_text(display, limit)

    def _render_active_cell_block(self) -> list[PanelLine]:
        lines: list[PanelLine] = []
        self._append_section_title(lines, "Active cell", pad_before=True)
        cell = self._cell_preview
        if cell is None:
            lines.append(self._plain_line("Pending selection", _BODY_STYLE))
            return lines

        is_null = cell.raw_value is None
        label = "null" if is_null else cell.display
        if not is_null and cell.truncated:
            label = f"{label}…"
        style = _NULL_STYLE if is_null else _BODY_STYLE
        lines.append(self._plain_line(label, style))
        return lines

    def _render_message_block(self, title: str, messages: list[str]) -> list[PanelLine]:
        lines: list[PanelLine] = []
        self._append_section_title(lines, title)
        for message in messages:
            wrapped = textwrap.fill(message, width=self.width)
            payload = wrapped.splitlines() or [""]
            for line in payload:
                lines.append(self._plain_line(line, _BODY_STYLE))
        return lines

    def _append_section_title(
        self,
        lines: list[PanelLine],
        title: str,
        *,
        pad_before: bool = False,
    ) -> None:
        if pad_before:
            if not lines or self._line_text(lines[-1]) != "":
                lines.append(self._plain_line("", _BODY_STYLE))
        elif lines and self._line_text(lines[-1]) != "":
            lines.append(self._plain_line("", _BODY_STYLE))
        lines.append(self._plain_line(title, _HEADER_STYLE))
        lines.append(self._plain_line("", _BODY_STYLE))

    def _format_labeled_section(
        self,
        title: str,
        entries: list[_LabeledEntry],
        *,
        pad_before: bool = False,
        placeholder: bool = False,
        align_numeric: bool = False,
    ) -> list[PanelLine]:
        if not entries:
            return []
        lines: list[PanelLine] = []
        self._append_section_title(lines, title, pad_before=pad_before)
        label_width = min(
            max(len(entry.label) for entry in entries) + 2,
            max(1, self.width - 4),
        )
        value_width = max(0, self.width - label_width - 1)
        alignment = None
        if align_numeric and not placeholder and value_width > 0:
            samples: list[str] = []
            for entry in entries:
                value = entry.display
                if value is None:
                    continue
                prefix, _ = self._split_numeric_suffix(value.strip())
                if self._looks_numeric(prefix):
                    samples.append(prefix)
            if samples:
                alignment = compute_decimal_alignment(samples, value_width)
        for entry in entries:
            line = self._format_labeled_line(
                entry,
                label_width,
                value_width,
                placeholder=placeholder,
                alignment=alignment,
                align_numeric=align_numeric,
            )
            lines.append(line)
        return lines

    def _format_labeled_line(
        self,
        entry: _LabeledEntry,
        label_width: int,
        value_width: int,
        *,
        placeholder: bool,
        alignment: tuple[int, int] | None,
        align_numeric: bool,
    ) -> PanelLine:
        if placeholder:
            return self._plain_line(entry.label, _BODY_STYLE)
        label_text = f"{entry.label:<{label_width}}"
        segments: list[tuple[str, str]] = [(_BODY_STYLE, label_text)]
        if value_width > 0:
            segments.append((_BODY_STYLE, " "))
        formatted_value, style = self._format_value_field(
            entry,
            value_width,
            alignment,
            align_numeric=align_numeric,
        )
        segments.append((style, formatted_value))
        return self._line_from_segments(segments)

    def _format_value_field(
        self,
        entry: _LabeledEntry,
        value_width: int,
        alignment: tuple[int, int] | None,
        *,
        align_numeric: bool,
    ) -> tuple[str, str]:
        value = entry.display
        if value is None:
            text = "null"
            padded = self._pad_value(text, value_width, numeric=True)
            return padded, _NULL_STYLE
        numeric = bool(entry.numeric is not None or self._looks_numeric(value))
        if align_numeric and numeric and value_width > 0:
            formatted = self._align_numeric_value(entry, value_width, alignment)
        elif entry.align_right and value_width > 0:
            formatted = self._pad_value(value, value_width, numeric=True)
        else:
            formatted = self._pad_value(value, value_width, numeric=numeric)
        return formatted, _BODY_STYLE

    def _align_numeric_value(
        self,
        entry: _LabeledEntry,
        width: int,
        alignment: tuple[int, int] | None,
    ) -> str:
        raw_value = entry.display or ""
        prefix, suffix = self._split_numeric_suffix(raw_value.strip())
        parsed = entry.numeric if entry.numeric is not None else self._parse_decimal(prefix)
        if parsed is not None:
            prefix = self._format_decimal_grouped(parsed)
        suffix_text = suffix
        suffix_width = display_width(suffix_text)
        if suffix_width > width:
            suffix_text = self._clip_text(suffix_text, width)
            suffix_width = display_width(suffix_text)
        available = max(0, width - suffix_width)
        if available == 0 and width > 0 and prefix:
            # Reserve at least one character for the prefix so percentages remain visible.
            available = 1
            suffix_text = self._clip_text(suffix_text, width - available)
            suffix_width = display_width(suffix_text)
        head = ""
        if available > 0:
            working = prefix
            aligned = None
            if alignment and self._has_fractional_component(entry, prefix):
                aligned = apply_decimal_alignment(working, alignment, available)
            if aligned is not None:
                head = aligned
            else:
                head = self._fit_numeric_text(working, available, parsed)
        return f"{head}{suffix_text}"

    def _fit_numeric_text(self, text: str, width: int, parsed: Decimal | None) -> str:
        if width <= 0:
            return ""
        visible = text
        if display_width(visible) > width:
            if parsed is not None:
                fitted = self._format_decimal_for_width(parsed, width)
                if fitted is not None:
                    return pad_left_display(fitted, width)
            visible = self._clip_text(visible, width)
        return pad_left_display(visible, width)

    def _split_numeric_suffix(self, value: str) -> tuple[str, str]:
        if not value:
            return "", ""
        split_idx = len(value)
        for idx, ch in enumerate(value):
            if ch.isspace():
                split_idx = idx
                break
        prefix = value[:split_idx].rstrip()
        suffix = value[split_idx:]
        return prefix or value, suffix

    def _pad_value(self, text: str, width: int, *, numeric: bool) -> str:
        if width <= 0:
            return text
        if numeric:
            return pad_left_display(text, width)
        return pad_right_display(text, width)

    def _format_numeric_string(self, text: str) -> str | None:
        decimal_value = self._parse_decimal(text)
        if decimal_value is None:
            return None
        return self._format_decimal_grouped(decimal_value)

    def _format_decimal_for_width(self, value: Decimal, width: int) -> str | None:
        if width <= 0:
            return ""
        for frac in range(_MAX_FRACTION_DIGITS, -1, -1):
            grouped = self._format_decimal_grouped(value, max_fraction_digits=frac)
            if display_width(grouped) <= width:
                return grouped
        ptb = self._format_decimal_ptb(value, width)
        if ptb is not None:
            return ptb
        return None

    def _parse_decimal(self, text: str) -> Decimal | None:
        if not text:
            return None
        cleaned = text.strip().replace(",", "").replace("_", "")
        if cleaned in {"", "-", "+", "."}:
            return None
        try:
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            return None

    def _format_decimal_grouped(
        self,
        value: Decimal,
        *,
        max_fraction_digits: int = _MAX_FRACTION_DIGITS,
    ) -> str:
        sign = "-" if value.is_signed() and value != 0 else ""
        quantized = value.copy_abs()
        text = format(quantized.normalize(), "f")
        if "." in text:
            int_part, frac_part = text.split(".", 1)
        else:
            int_part, frac_part = text, ""
        if frac_part and max_fraction_digits >= 0:
            frac_part = frac_part[:max_fraction_digits].rstrip("0")
        grouped = self._group_digits(int_part)
        if frac_part:
            return f"{sign}{grouped}.{frac_part}"
        return f"{sign}{grouped}"

    def _format_decimal_ptb(self, value: Decimal, width: int | None = None) -> str | None:
        magnitude = value.copy_abs()
        for threshold, suffix in _PTB_UNITS:
            if magnitude >= threshold:
                scaled = value / threshold
                max_frac = min(3, _MAX_FRACTION_DIGITS)
                for frac in range(max_frac, -1, -1):
                    text = self._format_decimal_grouped(scaled, max_fraction_digits=frac)
                    candidate = f"{text}{suffix}"
                    if width is None or display_width(candidate) <= width:
                        return candidate
                    tight = candidate.replace(",", "")
                    if width is None or display_width(tight) <= width:
                        return tight
        return None

    def _group_digits(self, digits: str) -> str:
        if not digits:
            return "0"
        result: list[str] = []
        while len(digits) > 3:
            result.append(digits[-3:])
            digits = digits[:-3]
        result.append(digits)
        return ",".join(reversed(result))

    def _looks_numeric(self, value: str) -> bool:
        candidate = value.strip()
        if not candidate:
            return False
        # Strip trailing annotation like percentages or parentheses.
        candidate = candidate.split(" ", 1)[0]
        candidate = candidate.strip("()")
        if candidate.endswith("%"):
            candidate = candidate[:-1]
        candidate = candidate.replace(",", "")
        if not candidate:
            return False
        try:
            float(candidate)
        except ValueError:
            return False
        return True

    def _has_fractional_component(self, entry: _LabeledEntry, text: str) -> bool:
        numeric = entry.numeric
        if isinstance(numeric, Decimal):
            return numeric != numeric.to_integral_value()
        if isinstance(numeric, float):
            return not numeric.is_integer()
        if isinstance(numeric, int):
            return False
        return "." in text

    def _plain_line(self, text: str, style: str = _BODY_STYLE) -> PanelLine:
        return self._line_from_segments([(style, text)])

    def _line_from_segments(self, segments: list[tuple[str, str]]) -> PanelLine:
        limit = max(0, self.width)
        if limit == 0:
            return []
        remaining = limit
        line: PanelLine = []
        for style, text in segments:
            if not text:
                continue
            if remaining <= 0:
                break
            chunk = text[:remaining]
            if chunk:
                line.append((style, chunk))
                remaining -= len(chunk)
        if not line:
            base_style = segments[0][0] if segments else _BODY_STYLE
            line.append((base_style, ""))
        return line

    def _line_text(self, line: PanelLine) -> str:
        return "".join(part for _, part in line)

    def _clip_text(self, text: str, limit: int | None = None) -> str:
        if limit is None:
            limit = self.width
        if limit <= 0:
            return ""
        if len(text) <= limit:
            return text
        if limit == 1:
            return "…"
        return text[: limit - 1] + "…"

    def _fmt_int(self, value: int | None) -> str:
        if value is None:
            return "?"
        return _format_number_with_thousands_separator(value)

    def _coerce_decimal(self, value: Any) -> Decimal | None:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, int):
            return Decimal(value)
        if isinstance(value, float):
            try:
                return Decimal(str(value))
            except Exception:
                return None
        if isinstance(value, str):
            return self._parse_decimal(value)
        return None

    def _format_stat_value(self, value: Any) -> tuple[str, Decimal | None]:
        decimal_value = self._coerce_decimal(value)
        if decimal_value is not None:
            return self._format_decimal_grouped(decimal_value), decimal_value
        if isinstance(value, str):
            return value, None
        try:
            numeric = float(value)
        except Exception:
            return str(value), None
        text = f"{numeric:,.2f}".rstrip("0").rstrip(".")
        return text, None

    def _fmt_percent(self, part: int, total: int | None) -> str:
        if not total:
            return "?"
        pct = (float(part) / float(total)) * 100.0
        if math.isnan(pct):
            return "?"
        return f"{pct:.1f}%"

    def _fmt_fraction(self, fraction: float | None) -> str:
        if fraction is None or math.isnan(fraction):
            return "?"
        return f"{fraction * 100:.1f}%"

    def _serialize_insight(
        self,
        insight: ColumnInsight | None,
        policy: RedactionPolicy | None,
    ) -> dict[str, object] | None:
        if insight is None:
            return None
        payload: dict[str, object] = {
            "sheet_id": insight.sheet_id,
            "plan_hash": insight.plan_hash,
            "column": insight.column_name,
            "dtype": insight.dtype,
            "row_count": insight.row_count,
            "non_null_count": insight.non_null_count,
            "null_count": insight.null_count,
            "null_fraction": insight.null_fraction,
            "distinct_count": insight.distinct_count,
            "stats": dict(insight.stats),
            "top_values": [
                self._serialize_top_value(entry, policy) for entry in insight.top_values
            ],
            "duration_ns": insight.duration_ns,
            "error": insight.error,
        }
        if insight.histogram is not None:
            payload["histogram"] = list(insight.histogram.bins)
        if insight.source_path:
            payload["source_path"] = redact_path(insight.source_path)
        return payload

    def _serialize_top_value(
        self,
        value,
        policy: RedactionPolicy | None,
    ) -> dict[str, object]:
        redacted_value = value.value
        if policy is not None:
            try:
                redacted_value = policy.apply_to_value(value.value)
            except Exception:
                redacted_value = value.value
        return {
            "value": redacted_value,
            "display": value.display,
            "count": value.count,
            "fraction": value.fraction,
            "truncated": value.truncated,
        }

    def _serialize_cell(
        self,
        preview: CellPreview | None,
        policy: RedactionPolicy | None,
    ) -> dict[str, object] | None:
        if preview is None:
            return None
        value = preview.raw_value
        if policy is not None:
            try:
                value = policy.apply_to_value(value)
            except Exception:
                value = preview.raw_value
        return {
            "column": preview.column,
            "row": preview.row,
            "absolute_row": preview.absolute_row,
            "dtype": preview.dtype,
            "value": value,
            "display": preview.display,
            "truncated": preview.truncated,
        }


__all__ = ["ColumnInsightPanel"]

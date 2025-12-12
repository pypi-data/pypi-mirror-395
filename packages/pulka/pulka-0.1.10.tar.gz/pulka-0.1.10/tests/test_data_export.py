"""Tests for the :mod:`pulka.data.export` helpers."""

from __future__ import annotations

from datetime import UTC
from pathlib import Path
from types import SimpleNamespace

import polars as pl
import pytest

from pulka.api import Session
from pulka.data.export import write_view_to_path
from pulka.logging import Recorder, RecorderConfig

DATA_DIR = Path(__file__).parent / "data"
MINI_NAV_CSV = DATA_DIR / "mini_nav.csv"


def _make_session(path: Path, *, recorder: Recorder | None = None) -> Session:
    return Session(str(path), viewport_rows=6, recorder=recorder)


class TestWriteViewToPath:
    """Unit coverage for ``write_view_to_path``."""

    def test_exports_parquet(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "export.parquet"

        result = write_view_to_path(viewer, destination)

        assert result == destination
        assert destination.exists()
        df = pl.read_parquet(destination)
        assert df.height > 0

    def test_records_recorder_event(self, tmp_path: Path) -> None:
        recorder = Recorder(
            RecorderConfig(
                enabled=True, output_dir=tmp_path, compression="none", cell_redaction="none"
            )
        )
        session = _make_session(MINI_NAV_CSV, recorder=recorder)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "export.csv"

        write_view_to_path(viewer, destination)

        export_events = [event for event in recorder.iter_events() if event.type == "export"]
        assert len(export_events) == 1
        payload = export_events[0].payload
        assert payload["format"] == "csv"
        assert payload["path"]["basename"] == destination.name
        assert payload["_raw_path"].endswith("export.csv")

    def test_accepts_sheet_instance(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        sheet = viewer.sheet
        destination = tmp_path / "sheet.csv"

        write_view_to_path(sheet, destination)

        assert destination.exists()
        df = pl.read_csv(destination)
        assert df.height > 0

    def test_accepts_iterable_options(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "export.tsv"

        write_view_to_path(viewer, destination, options=["separator=\\t"])

        with destination.open("r", encoding="utf-8") as handle:
            header = handle.readline()
        assert "\t" in header

    def test_rejects_invalid_option_string(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "bad.csv"

        with pytest.raises(ValueError):
            write_view_to_path(viewer, destination, options=["bad_option"])

    def test_requires_known_format(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "export.unknown"

        with pytest.raises(ValueError, match="Unsupported export format"):
            write_view_to_path(viewer, destination)

    def test_respects_format_hint(self, tmp_path: Path) -> None:
        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "no_extension"

        write_view_to_path(viewer, destination, format_hint="parquet")

        assert destination.exists()
        df = pl.read_parquet(destination)
        assert df.height > 0

    def test_accepts_common_excel_typo(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from pulka import data

        if "xslx" not in data.export._NORMALISED_FORMATS:
            pytest.skip("Excel export not available in this Polars build")

        session = _make_session(MINI_NAV_CSV)
        viewer = session.viewer
        assert viewer is not None
        destination = tmp_path / "export.xlsx"

        captured_spec: dict[str, object] = {}

        def fake_write_lazyframe(lazy_frame, path, spec, options) -> None:
            captured_spec["spec"] = spec

        monkeypatch.setattr(data.export, "_write_lazyframe", fake_write_lazyframe)
        monkeypatch.setattr(data.export, "_record_export_event", lambda *args, **kwargs: None)

        write_view_to_path(viewer, destination, format_hint="xslx")

        assert captured_spec["spec"].format_name == "excel"

    def test_excel_export_strips_timezone_datetimes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from datetime import datetime

        import polars as pl

        from pulka import data

        if "xslx" not in data.export._NORMALISED_FORMATS:
            pytest.skip("Excel export not available in this Polars build")

        lazy = pl.DataFrame(
            {
                "ts": pl.datetime_range(
                    datetime(2024, 1, 1),
                    datetime(2024, 1, 3),
                    eager=True,
                    time_zone="America/Los_Angeles",
                )
            }
        ).lazy()

        session = SimpleNamespace(recorder=None)
        sheet = SimpleNamespace(lazyframe=lazy, session=session)
        viewer = SimpleNamespace(sheet=sheet, session=session)
        sheet.viewer = viewer

        captured: dict[str, object] = {}

        def fake_write_excel(self: pl.DataFrame, path: Path, **options: object) -> None:
            captured["df"] = self

        monkeypatch.setattr(pl.DataFrame, "write_excel", fake_write_excel, raising=False)

        destination = tmp_path / "export.xlsx"
        write_view_to_path(viewer, destination)

        exported = captured["df"]
        assert isinstance(exported, pl.DataFrame)
        dtype = exported.schema["ts"]
        assert getattr(dtype, "time_zone", None) is None
        first = exported["ts"].to_list()[0]
        assert getattr(first, "tzinfo", None) is None

    def test_excel_exports_nested_and_binary_types(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from datetime import datetime, time, timedelta

        import polars as pl

        from pulka import data

        if "xslx" not in data.export._NORMALISED_FORMATS:
            pytest.skip("Excel export not available in this Polars build")

        df = pl.DataFrame(
            {
                "ts": [datetime(2024, 1, 1, tzinfo=UTC)],
                "binary": [b"\x00\xff"],
                "list_values": [[1, 2, 3]],
                "struct_values": [{"a": 1, "b": "x"}],
                "duration_value": [timedelta(hours=1)],
                "time_value": [time(12, 34, 56)],
                "category_value": pl.Series("category_value", ["foo"]).cast(pl.Categorical),
                "enum_value": pl.Series("enum_value", ["bar"]).cast(pl.Enum(["bar", "baz"])),
                "object_value": pl.Series("object_value", [complex(1, 2)], dtype=pl.Object),
            }
        )

        session = SimpleNamespace(recorder=None)
        sheet = SimpleNamespace(lazyframe=df.lazy(), session=session)
        viewer = SimpleNamespace(sheet=sheet, session=session)
        sheet.viewer = viewer

        captured: dict[str, pl.DataFrame] = {}

        def fake_write_excel(self: pl.DataFrame, path: Path, **options: object) -> None:
            captured["df"] = self

        monkeypatch.setattr(pl.DataFrame, "write_excel", fake_write_excel, raising=False)

        destination = tmp_path / "export.xlsx"
        write_view_to_path(viewer, destination)

        exported = captured["df"]
        assert isinstance(exported, pl.DataFrame)
        schema = exported.schema

        assert schema["ts"].time_zone is None
        assert schema["binary"] == pl.Utf8
        assert schema["list_values"] == pl.Utf8
        assert schema["struct_values"] == pl.Utf8
        assert schema["duration_value"] == pl.Utf8
        assert schema["time_value"] == pl.Utf8
        assert schema["category_value"] == pl.Utf8
        assert schema["enum_value"] == pl.Utf8
        assert schema["object_value"] == pl.Utf8

        assert exported["binary"].to_list()[0] == "00ff"
        assert exported["list_values"].to_list()[0].startswith("[1, 2, 3]")
        assert exported["struct_values"].to_list()[0].startswith("{'a': 1")
        assert exported["duration_value"].to_list()[0] == "PT1H"
        assert exported["time_value"].to_list()[0] == "12:34:56"

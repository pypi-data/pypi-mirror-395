from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from pulka.core.engine.contracts import EnginePayloadHandle
from pulka.core.engine.polars_adapter import POLARS_ENGINE, unwrap_physical_plan
from pulka.data.scan import is_supported_path
from pulka.data.scanners import ScannerRegistry


def test_scanner_registry_wraps_lazyframe(tmp_path: Path) -> None:
    registry = ScannerRegistry()

    def _scan(_path: Path) -> pl.LazyFrame:
        return pl.DataFrame({"value": [1, 2, 3]}).lazy()

    registry.register_scanner(".foo", _scan)

    target = tmp_path / "example.foo"
    target.write_bytes(b"")

    physical_plan = registry.scan(target)

    assert isinstance(physical_plan, EnginePayloadHandle)
    assert physical_plan.as_serializable() == {
        "engine": POLARS_ENGINE,
        "kind": "physical_plan",
    }

    polars_plan = unwrap_physical_plan(physical_plan)
    assert polars_plan.to_lazyframe().collect().to_dict(as_series=False) == {"value": [1, 2, 3]}


def test_scanner_registry_rejects_unknown_payload(tmp_path: Path) -> None:
    registry = ScannerRegistry()

    class _WeirdPlan:
        pass

    def _scan(_path: Path) -> _WeirdPlan:
        return _WeirdPlan()

    registry.register_scanner(".bar", _scan)

    with pytest.raises(TypeError, match="unsupported plan type: _WeirdPlan"):
        registry.scan(tmp_path / "example.bar")


def test_scanner_registry_can_scan_known_formats(tmp_path: Path) -> None:
    registry = ScannerRegistry()
    assert registry.can_scan(tmp_path / "data.csv")
    assert registry.can_scan(tmp_path / "data.parquet")
    assert not registry.can_scan(tmp_path / "notes.txt")


def test_scanner_registry_can_scan_registered_extension(tmp_path: Path) -> None:
    registry = ScannerRegistry()

    def _scan(_path: Path) -> pl.LazyFrame:
        return pl.DataFrame({"value": [42]}).lazy()

    registry.register_scanner(".foo", _scan)
    assert registry.can_scan(tmp_path / "dataset.foo")


def test_is_supported_path_detects_known_formats() -> None:
    assert is_supported_path("example.csv")
    assert is_supported_path("example.ndjson.zst")
    assert not is_supported_path("example.txt")


def test_scanner_registry_allows_unknown_when_unrestricted(tmp_path: Path, monkeypatch) -> None:
    import pulka.data.scan as scan_mod

    monkeypatch.setattr(scan_mod, "_BROWSER_STRICT_EXTENSIONS", False)
    registry = ScannerRegistry()
    assert registry.can_scan(tmp_path / "notes.txt")

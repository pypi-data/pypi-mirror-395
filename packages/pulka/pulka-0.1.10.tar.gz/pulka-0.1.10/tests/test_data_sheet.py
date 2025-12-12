import json

import polars as pl
import pytest

from pulka.core.engine.contracts import EnginePayloadHandle
from pulka.core.engine.polars_adapter import (
    POLARS_ENGINE,
    unwrap_lazyframe_handle,
)
from pulka.sheets.data_sheet import DataSheet


def test_get_value_at_basic(job_runner):
    sheet = DataSheet(pl.DataFrame({"col": [1, None, 3]}).lazy(), runner=job_runner)

    assert sheet.get_value_at(0) == 1
    assert sheet.get_value_at(1) is None
    assert sheet.get_value_at(2, "col") == 3


def test_get_value_at_errors(job_runner):
    sheet = DataSheet(pl.DataFrame({"value": ["a"]}).lazy(), runner=job_runner)

    with pytest.raises(IndexError):
        sheet.get_value_at(1)

    with pytest.raises(KeyError):
        sheet.get_value_at(0, "missing")

    with pytest.raises(IndexError):
        sheet.get_value_at(-1)


def test_datasheet_exposes_engine_handles(job_runner):
    sheet = DataSheet(pl.DataFrame({"value": [1, 2]}).lazy(), runner=job_runner)

    for handle in (sheet.lf, sheet.source, sheet.to_lazyframe()):
        assert isinstance(handle, EnginePayloadHandle)
        assert not isinstance(handle, pl.LazyFrame)
        meta = handle.as_serializable()
        assert meta == {"engine": POLARS_ENGINE, "kind": "lazyframe"}
        assert json.loads(json.dumps(meta)) == meta

    physical = sheet.physical_plan()
    assert isinstance(physical, EnginePayloadHandle)
    plan_meta = physical.as_serializable()
    assert plan_meta == {"engine": POLARS_ENGINE, "kind": "physical_plan"}
    assert json.loads(json.dumps(plan_meta)) == plan_meta

    lazy_frame = unwrap_lazyframe_handle(sheet.lf)
    assert isinstance(lazy_frame, pl.LazyFrame)

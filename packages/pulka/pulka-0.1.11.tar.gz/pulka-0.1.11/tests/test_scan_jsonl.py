from __future__ import annotations

from pathlib import Path

import pytest
import zstandard

from pulka.data.scan import scan_any


@pytest.mark.parametrize("extension", [".jsonl", ".ndjson"])
def test_scan_any_plain_jsonl(tmp_path: Path, extension: str) -> None:
    json_path = tmp_path / f"data{extension}"
    json_path.write_text('{"value": 1}\n{"value": 2}\n', encoding="utf-8")

    lf = scan_any(str(json_path))

    result = lf.collect()
    assert result.get_column("value").to_list() == [1, 2]


@pytest.mark.parametrize("extension", [".jsonl.zst", ".ndjson.zst"])
def test_scan_any_jsonl_zst(tmp_path: Path, extension: str) -> None:
    json_path = tmp_path / f"data{extension}"
    compressor = zstandard.ZstdCompressor()
    with json_path.open("wb") as sink, compressor.stream_writer(sink) as writer:
        writer.write(b'{"value": 1}\n{"value": 2}\n')

    lf = scan_any(str(json_path))

    result_first = lf.collect()
    result_second = lf.collect()
    expected = [1, 2]
    assert result_first.get_column("value").to_list() == expected
    assert result_second.get_column("value").to_list() == expected

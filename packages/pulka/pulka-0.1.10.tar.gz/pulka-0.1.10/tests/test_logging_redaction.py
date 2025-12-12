"""Unit tests for path redaction utilities."""

from __future__ import annotations

from pulka.logging.redaction import redact_path, redact_paths


def test_redact_path_returns_basename_and_digest() -> None:
    """Test that redact_path returns the expected structure."""
    result = redact_path("/home/user/data/file.parquet")

    assert "basename" in result
    assert "digest" in result
    assert result["basename"] == "file.parquet"
    assert isinstance(result["digest"], str)
    assert len(result["digest"]) == 40  # SHA1 is 40 hex chars


def test_redact_path_deterministic() -> None:
    """Test that redact_path returns the same digest for the same input."""
    path = "/home/user/data/file.parquet"
    result1 = redact_path(path)
    result2 = redact_path(path)

    assert result1["digest"] == result2["digest"]
    assert result1["basename"] == result2["basename"]


def test_redact_path_case_sensitive() -> None:
    """Test that redact_path handles case sensitivity correctly."""
    path1 = "/home/user/data/FILE.parquet"
    path2 = "/home/user/data/file.parquet"

    result1 = redact_path(path1)
    result2 = redact_path(path2)

    # Basenames should match original case
    assert result1["basename"] == "FILE.parquet"
    assert result2["basename"] == "file.parquet"

    # Digests should be different due to case difference
    assert result1["digest"] != result2["digest"]


def test_redact_paths_redacts_simple_path_fields() -> None:
    """Test that redact_paths identifies and redacts path fields."""
    payload = {"path": "/home/user/data/file.parquet", "name": "dataset", "other": "value"}

    result = redact_paths(payload)

    assert "path" in result
    assert isinstance(result["path"], dict)
    assert "basename" in result["path"]
    assert "digest" in result["path"]
    assert result["name"] == "dataset"
    assert result["other"] == "value"


def test_redact_paths_redacts_path_suffix_fields() -> None:
    """Test that redact_paths identifies fields ending with '_path'."""
    payload = {
        "input_path": "/input/file.parquet",
        "output_path": "/output/file.csv",
        "regular_field": "value",
    }

    result = redact_paths(payload)

    assert isinstance(result["input_path"], dict)
    assert isinstance(result["output_path"], dict)
    assert "basename" in result["input_path"]
    assert "basename" in result["output_path"]
    assert result["regular_field"] == "value"


def test_redact_paths_handles_paths_field() -> None:
    """Test that redact_paths handles 'paths' field (plural)."""
    payload = {
        "paths": ["/path1", "/path2"],  # This should not be redacted since it's not a string
        "path": "/single/path",
        "config_paths": [
            "/config1",
            "/config2",
        ],  # This should not be redacted since it's not a string
    }

    result = redact_paths(payload)

    # Only the 'path' field should be redacted as it's a string
    assert isinstance(result["path"], dict)
    assert "basename" in result["path"]
    # The 'paths' and 'config_paths' fields should remain unchanged as they're not strings
    assert result["paths"] == ["/path1", "/path2"]
    assert result["config_paths"] == ["/config1", "/config2"]


def test_redact_paths_leaves_nested_dicts_untouched() -> None:
    """Nested mappings are left as-is so schema-like structures stay intact."""
    payload = {"path": "/outer/path", "nested": {"inner_path": "/inner/path", "name": "inner"}}

    result = redact_paths(payload)

    # Outer path should be redacted
    assert isinstance(result["path"], dict)

    # Inner structures remain untouched (shallow processing only)
    assert result["nested"]["inner_path"] == "/inner/path"
    assert result["nested"]["name"] == "inner"


def test_redact_paths_avoids_double_redaction() -> None:
    """Test that values that are already redacted structures aren't processed again."""
    already_redacted = {"basename": "file.parquet", "digest": "abcdef1234567890"}

    payload = {
        "path": already_redacted,  # This is already a redacted structure, shouldn't be processed
        "regular_path": "/normal/path",  # This should be redacted
    }

    result = redact_paths(payload)

    # The already-redacted value should remain unchanged
    assert result["path"] == already_redacted

    # The regular path should be redacted
    assert isinstance(result["regular_path"], dict)
    assert "basename" in result["regular_path"]


def test_redact_paths_preserves_private_fields() -> None:
    """Keys starting with an underscore keep their original value."""
    payload = {"path": "/outer/path", "_raw_path": "/outer/path"}

    result = redact_paths(payload)

    assert isinstance(result["path"], dict)
    assert result["_raw_path"] == "/outer/path"


def test_sha1_consistency() -> None:
    """Test that SHA1 hashing is consistent and matches expected values."""
    test_path = "/tmp/test.parquet"
    result = redact_path(test_path)

    # Expected SHA1 of "/tmp/test.parquet"
    expected_digest = "58360a420b840c17d3eb72b795aa6528fed43bdc"

    assert result["digest"] == expected_digest

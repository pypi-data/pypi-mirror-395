"""Tests for the reproducible dataset export functionality."""

import polars as pl

from pulka.api import Session
from pulka.data.repro import build_repro_slice, get_redacted_df_for_policy
from pulka.logging import Recorder, RecorderConfig
from pulka.logging.redaction import HashStringsPolicy, MaskPatternsPolicy, NoRedactionPolicy


class TestBuildReproSlice:
    """Test the build_repro_slice function."""

    def test_export_basic_slice(self, tmp_path):
        """Test exporting a basic slice around the viewport."""
        # Create test dataset
        df = pl.DataFrame(
            {
                "a": list(range(100)),
                "b": [f"value_{i}" for i in range(100)],
                "c": [i * 2 for i in range(100)],
            }
        )
        dataset_path = tmp_path / "test.parquet"
        df.write_parquet(dataset_path)

        # Create session and move to specific viewport
        session = Session(str(dataset_path), viewport_rows=10)
        viewer = session.viewer

        # Manually set viewport to row 20-30
        viewer.row0 = 20
        viewer.cur_row = 25

        # Export with margin
        result = build_repro_slice(session, row_margin=5, include_all_columns=False)

        # Should include rows 15-35 (20-5 to 30+5, where 30 is roughly 20+10)
        expected_start = max(0, 20 - 5)  # 15
        expected_end = min(100, 30 + 5)  # 35 (20 + 10 viewport + 5 margin)
        assert len(result) == expected_end - expected_start

        # Should have all columns since visible_cols includes all in this case
        assert set(result.columns) == {"a", "b", "c"}

    def test_export_with_all_columns_true(self, tmp_path):
        """Test exporting with all columns when include_all_columns=True."""
        # Create dataset with multiple columns
        df = pl.DataFrame(
            {
                "a": list(range(50)),
                "b": [f"value_{i}" for i in range(50)],
                "c": [f"other_{i}" for i in range(50)],
                "d": [i * 3 for i in range(50)],
            }
        )
        dataset_path = tmp_path / "test.parquet"
        df.write_parquet(dataset_path)

        session = Session(str(dataset_path), viewport_rows=5)

        # Export with all columns
        result = build_repro_slice(session, row_margin=2, include_all_columns=True)

        # Should have all columns
        assert set(result.columns) == {"a", "b", "c", "d"}
        # Should have rows with margin
        assert len(result) <= 5 + 4  # viewport + margins

    def test_export_with_visible_columns_only(self, tmp_path):
        """Test exporting with visible columns only."""
        # Create dataset with multiple columns
        df = pl.DataFrame(
            {
                "a": list(range(50)),
                "b": [f"value_{i}" for i in range(50)],
                "c": [f"other_{i}" for i in range(50)],
                "d": [i * 3 for i in range(50)],
            }
        )
        dataset_path = tmp_path / "test.parquet"
        df.write_parquet(dataset_path)

        session = Session(str(dataset_path), viewport_rows=5)
        viewer = session.viewer

        # Hide a column
        viewer.cur_col = 1  # Column 'b'
        viewer.hide_current_column()

        # Now export with visible columns only
        result = build_repro_slice(session, row_margin=2, include_all_columns=False)

        # Should not have the hidden column 'b'
        assert "b" not in result.columns
        assert set(result.columns) == {"a", "c", "d"}

    def test_export_accepts_raw_lazyframe_sheet(self, tmp_path):
        """Ensure sheets exposing raw LazyFrames can be exported."""

        df = pl.DataFrame(
            {
                "value": list(range(1, 101)),
            }
        )
        dataset_path = tmp_path / "hist.parquet"
        df.write_parquet(dataset_path)

        session = Session(str(dataset_path), viewport_rows=10)

        # Switch to a histogram sheet which exposes a raw LazyFrame.
        base_viewer = session.viewer
        session.open_sheet_view(
            "histogram",
            base_viewer=base_viewer,
            column_name="value",
        )

        result = build_repro_slice(session, row_margin=1, include_all_columns=True)

        assert isinstance(result, pl.DataFrame)
        assert set(result.columns)


class TestRedactedExport:
    """Test the redaction functionality in exports."""

    def test_hash_strings_redaction(self):
        """Test that HashStringsPolicy works correctly on exports."""
        df = pl.DataFrame(
            {"text_col": ["hello", "world", "email@example.com"], "num_col": [1, 2, 3]}
        )

        policy = HashStringsPolicy()
        result = get_redacted_df_for_policy(df, policy)

        # Check that text column is now a struct with hash/length
        assert result.schema["text_col"] == pl.Struct(
            [pl.Field("hash", pl.Utf8), pl.Field("length", pl.Int64)]
        )

        # Check that numeric column is unchanged
        assert result["num_col"].equals(df["num_col"])

        # Check that the hashes are correct
        hashes = [row["hash"] for row in result["text_col"].to_list() if row is not None]
        assert len(hashes) == 3  # All non-null text values should be hashed

    def test_mask_patterns_redaction(self):
        """Test that MaskPatternsPolicy works correctly on exports."""
        df = pl.DataFrame(
            {
                "text_col": ["hello", "test@example.com", "Call me at +1-555-123-4567"],
                "num_col": [1, 2, 3],
            }
        )

        policy = MaskPatternsPolicy()
        result = get_redacted_df_for_policy(df, policy)

        # Check that sensitive patterns are masked in text column
        text_values = result["text_col"].to_list()
        assert text_values[0] == "hello"  # Non-sensitive unchanged
        assert text_values[1] == "***"  # Email masked
        # Note: Phone number may be partially masked in phrase, e.g. "Call me at ***"
        assert "***" in text_values[2]  # Phone number part should be masked

        # Check that numeric column is unchanged
        assert result["num_col"].equals(df["num_col"])

    def test_no_redaction(self):
        """Test that NoRedactionPolicy keeps data unchanged."""
        df = pl.DataFrame(
            {"text_col": ["hello", "world", "email@example.com"], "num_col": [1, 2, 3]}
        )

        policy = NoRedactionPolicy()
        result = get_redacted_df_for_policy(df, policy)

        # Check that everything remains unchanged
        assert result.equals(df)


class TestRecorderIntegration:
    """Test the recorder's export_repro_slice method."""

    def test_export_repro_slice_creates_file_and_records_event(self, tmp_path):
        """Test that export_repro_slice creates a file and records the event."""
        # Create test dataset
        df = pl.DataFrame({"a": list(range(20)), "b": [f"value_{i}" for i in range(20)]})
        dataset_path = tmp_path / "test.parquet"
        df.write_parquet(dataset_path)

        # Create session with recorder
        config = RecorderConfig(enabled=True, output_dir=tmp_path, cell_redaction="none")
        recorder = Recorder(config)
        session = Session(str(dataset_path), recorder=recorder, viewport_rows=5)

        # Export repro slice
        export_path = recorder.export_repro_slice(
            session=session, row_margin=2, include_all_columns=False
        )

        # Verify file exists
        assert export_path.exists()
        assert export_path.name.endswith("-repro.parquet")

        # Verify content matches expected slice
        exported_df = pl.read_parquet(export_path)
        assert len(exported_df) <= 5 + 4  # viewport + margins
        assert set(exported_df.columns) == {"a", "b"}

        # Verify event was recorded
        events = list(recorder.iter_events())
        repro_events = [e for e in events if e.type == "repro_export"]
        assert len(repro_events) == 1

        payload = repro_events[0].payload
        assert "path" in payload  # redacted path
        assert "rows" in payload
        assert "cols" in payload
        assert "_raw_path" in payload  # should have raw path for internal use

    def test_export_with_different_policies(self, tmp_path):
        """Test exports with different redaction policies."""
        df = pl.DataFrame(
            {
                "email": ["test@example.com", "user@domain.org", "admin@test.net"],
                "text": ["hello", "world", "sensitive data"],
                "number": [1, 2, 3],
            }
        )
        dataset_path = tmp_path / "test.parquet"
        df.write_parquet(dataset_path)

        # Test with hash_strings policy
        config = RecorderConfig(enabled=True, output_dir=tmp_path, cell_redaction="hash_strings")
        recorder = Recorder(config)
        session = Session(str(dataset_path), recorder=recorder)

        export_path = recorder.export_repro_slice(
            session=session, row_margin=0, include_all_columns=True
        )
        exported_df = pl.read_parquet(export_path)

        # With hash_strings, email column should be struct with hash/length
        email_vals = exported_df["email"].to_list()
        assert all(isinstance(val, dict) and "hash" in val for val in email_vals if val is not None)

        # Test with mask_patterns policy
        config2 = RecorderConfig(enabled=True, output_dir=tmp_path, cell_redaction="mask_patterns")
        recorder2 = Recorder(config2)
        session2 = Session(str(dataset_path), recorder=recorder2)

        export_path2 = recorder2.export_repro_slice(
            session=session2, row_margin=0, include_all_columns=True
        )
        exported_df2 = pl.read_parquet(export_path2)

        # With mask_patterns, email values should be masked
        email_vals2 = exported_df2["email"].to_list()
        assert all(val == "***" for val in email_vals2)

        # Test with no redaction
        config3 = RecorderConfig(enabled=True, output_dir=tmp_path, cell_redaction="none")
        recorder3 = Recorder(config3)
        session3 = Session(str(dataset_path), recorder=recorder3)

        export_path3 = recorder3.export_repro_slice(
            session=session3, row_margin=0, include_all_columns=True
        )
        exported_df3 = pl.read_parquet(export_path3)

        # With no redaction, email values should be original
        email_vals3 = exported_df3["email"].to_list()
        assert email_vals3 == ["test@example.com", "user@domain.org", "admin@test.net"]

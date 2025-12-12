"""Tests for the cell redaction policies in the flight recorder."""

import hashlib

import pytest

from pulka.logging import Recorder, RecorderConfig
from pulka.logging.redaction import (
    HashStringsPolicy,
    MaskPatternsPolicy,
    NoRedactionPolicy,
    redaction_policy_from_name,
)


class TestRedactionPolicies:
    """Test the individual redaction policies."""

    def test_no_redaction_policy(self):
        """Test that NoRedactionPolicy returns values unchanged."""
        policy = NoRedactionPolicy()

        # Test with strings
        assert policy.apply_to_value("hello") == "hello"
        assert policy.apply_to_value("") == ""

        # Test with non-strings
        assert policy.apply_to_value(42) == 42
        assert policy.apply_to_value([1, 2, 3]) == [1, 2, 3]
        assert policy.apply_to_value({"key": "value"}) == {"key": "value"}

    def test_hash_strings_policy(self):
        """Test that HashStringsPolicy hashes string values."""
        policy = HashStringsPolicy()

        # Test string hashing
        result = policy.apply_to_value("hello")
        expected_hash = hashlib.sha1(b"hello").hexdigest()
        assert result == {"hash": expected_hash, "length": 5}

        # Test empty string
        result = policy.apply_to_value("")
        expected_hash = hashlib.sha1(b"").hexdigest()
        assert result == {"hash": expected_hash, "length": 0}

        # Test non-strings pass through
        assert policy.apply_to_value(42) == 42
        assert policy.apply_to_value([1, 2, 3]) == [1, 2, 3]
        assert policy.apply_to_value({"key": "value"}) == {"key": "value"}

    def test_mask_patterns_policy(self):
        """Test that MaskPatternsPolicy masks sensitive patterns."""
        policy = MaskPatternsPolicy()

        # Test email masking
        result = policy.apply_to_value("Contact me at john.doe@example.com")
        assert result == "Contact me at ***"

        # Test multiple emails
        result = policy.apply_to_value("Emails: john@example.com and jane@domain.org")
        assert result == "Emails: *** and ***"

        # Test phone number masking
        result = policy.apply_to_value("Call me at +1-555-123-4567")
        assert result == "Call me at ***"

        # Test IBAN masking
        result = policy.apply_to_value("My IBAN is DE44500105170445678901")
        assert result == "My IBAN is ***"

        # Test mixed sensitive info
        result = policy.apply_to_value("Contact: john@example.com or +49-123-456-7890")
        assert result == "Contact: *** or ***"

        # Test non-sensitive strings pass through
        assert policy.apply_to_value("Regular text") == "Regular text"

        # Test non-strings pass through
        assert policy.apply_to_value(42) == 42
        assert policy.apply_to_value([1, 2, 3]) == [1, 2, 3]
        assert policy.apply_to_value({"key": "value"}) == {"key": "value"}


class TestRedactionPolicyFromName:
    """Test the redaction_policy_from_name helper function."""

    def test_valid_policies(self):
        """Test that valid policy names create correct instances."""
        # Test 'none' policy
        policy = redaction_policy_from_name("none")
        assert isinstance(policy, NoRedactionPolicy)

        # Test 'hash' alias
        policy = redaction_policy_from_name("hash")
        assert isinstance(policy, HashStringsPolicy)

        # Test 'hash_strings'
        policy = redaction_policy_from_name("hash_strings")
        assert isinstance(policy, HashStringsPolicy)

        # Test 'hashstrings' (without underscore)
        policy = redaction_policy_from_name("hashstrings")
        assert isinstance(policy, HashStringsPolicy)

        # Test 'mask' alias
        policy = redaction_policy_from_name("mask")
        assert isinstance(policy, MaskPatternsPolicy)

        # Test 'mask_patterns'
        policy = redaction_policy_from_name("mask_patterns")
        assert isinstance(policy, MaskPatternsPolicy)

        # Test 'maskpatterns' (without underscore)
        policy = redaction_policy_from_name("maskpatterns")
        assert isinstance(policy, MaskPatternsPolicy)

        # Test case insensitivity
        policy = redaction_policy_from_name("HASH_STRINGS")
        assert isinstance(policy, HashStringsPolicy)

    def test_invalid_policy_raises_error(self):
        """Test that invalid policy names raise ValueError."""
        with pytest.raises(ValueError, match="Unknown redaction policy"):
            redaction_policy_from_name("invalid_policy")

        with pytest.raises(ValueError, match="Unknown redaction policy"):
            redaction_policy_from_name("")


class TestRecorderCellRedaction:
    """Test that the recorder applies cell redaction policies correctly."""

    def test_recorder_with_no_redaction(self, tmp_path):
        """Test recorder with no redaction policy."""
        config = RecorderConfig(enabled=True, cell_redaction="none", output_dir=tmp_path)
        recorder = Recorder(config)

        # Record a payload with sensitive data
        test_payload = {
            "email": "test@example.com",
            "phone": "+1-555-123-4567",
            "text": "Regular text",
            "number": 42,
        }

        recorder.record("test_event", test_payload)

        # Get the recorded event and verify no redaction occurred
        events = list(recorder.iter_events())
        assert len(events) == 1
        recorded_payload = events[0].payload
        assert recorded_payload["email"] == "test@example.com"
        assert recorded_payload["phone"] == "+1-555-123-4567"
        assert recorded_payload["text"] == "Regular text"
        assert recorded_payload["number"] == 42

    def test_recorder_with_hash_strings(self, tmp_path):
        """Test recorder with hash strings policy."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        # Record a payload with sensitive data
        test_payload = {
            "email": "test@example.com",
            "phone": "+1-555-123-4567",
            "text": "Regular text",
            "number": 42,
        }

        recorder.record("test_event", test_payload)

        # Get the recorded event and verify strings were hashed
        events = list(recorder.iter_events())
        assert len(events) == 1
        recorded_payload = events[0].payload

        # Check that string values were transformed to hash dicts
        email_hash = hashlib.sha1(b"test@example.com").hexdigest()
        assert recorded_payload["email"] == {"hash": email_hash, "length": 16}

        phone_hash = hashlib.sha1(b"+1-555-123-4567").hexdigest()
        assert recorded_payload["phone"] == {"hash": phone_hash, "length": 15}

        text_hash = hashlib.sha1(b"Regular text").hexdigest()
        assert recorded_payload["text"] == {"hash": text_hash, "length": 12}

        # Non-string values should pass through unchanged
        assert recorded_payload["number"] == 42

    def test_recorder_with_mask_patterns(self, tmp_path):
        """Test recorder with mask patterns policy."""
        config = RecorderConfig(enabled=True, cell_redaction="mask_patterns", output_dir=tmp_path)
        recorder = Recorder(config)

        # Record a payload with sensitive data
        test_payload = {
            "email": "test@example.com",
            "phone": "+1-555-123-4567",
            "mixed": "Contact: john@domain.com or call +49-987-654-3210",
            "text": "Regular text",
            "number": 42,
        }

        recorder.record("test_event", test_payload)

        # Get the recorded event and verify patterns were masked
        events = list(recorder.iter_events())
        assert len(events) == 1
        recorded_payload = events[0].payload

        # Check that sensitive patterns were masked
        assert recorded_payload["email"] == "***"
        assert recorded_payload["phone"] == "***"
        assert recorded_payload["mixed"] == "Contact: *** or call ***"

        # Regular text should pass through unchanged
        assert recorded_payload["text"] == "Regular text"

        # Non-string values should pass through unchanged
        assert recorded_payload["number"] == 42

    def test_recorder_preserves_private_keys(self, tmp_path):
        """Test that recorder preserves private keys (starting with _) unchanged."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        # Record a payload with private keys
        test_payload = {
            "public_email": "test@example.com",  # This should be redacted
            "_raw_path": "/secret/file.txt",  # This should remain unchanged
            "data": "sensitive info",  # This should be redacted
        }

        recorder.record("test_event", test_payload)

        # Get the recorded event and verify private keys are preserved
        events = list(recorder.iter_events())
        assert len(events) == 1
        recorded_payload = events[0].payload

        # Public fields should be redacted
        email_hash = hashlib.sha1(b"test@example.com").hexdigest()
        assert recorded_payload["public_email"] == {"hash": email_hash, "length": 16}
        data_hash = hashlib.sha1(b"sensitive info").hexdigest()
        assert recorded_payload["data"] == {"hash": data_hash, "length": 14}

        # Private fields should remain unchanged
        assert recorded_payload["_raw_path"] == "/secret/file.txt"

    def test_recorder_nested_data_handling(self, tmp_path):
        """Test that recorder handles nested data structures correctly."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        # Record a payload with nested structures
        test_payload = {
            "string_list": ["email@domain.com", "other"],
            "mixed_list": ["sensitive", 42, "text"],
            "nested_dict": {
                "email": "nested@example.com",
                "number": 123,
                "_private": "preserve_me",
            },
            "regular": "value",
        }

        recorder.record("test_event", test_payload)

        # Get the recorded event and verify nested handling
        events = list(recorder.iter_events())
        assert len(events) == 1
        recorded_payload = events[0].payload

        # Verify list elements are processed
        email_hash = hashlib.sha1(b"email@domain.com").hexdigest()
        other_hash = hashlib.sha1(b"other").hexdigest()
        assert recorded_payload["string_list"] == [
            {"hash": email_hash, "length": 16},
            {"hash": other_hash, "length": 5},
        ]

        # Mixed list: strings hashed, non-strings preserved
        sensitive_hash = hashlib.sha1(b"sensitive").hexdigest()
        text_hash = hashlib.sha1(b"text").hexdigest()
        assert recorded_payload["mixed_list"] == [
            {"hash": sensitive_hash, "length": 9},
            42,  # Number preserved
            {"hash": text_hash, "length": 4},
        ]

        # Nested dict: only top-level string values processed
        nested_hash = hashlib.sha1(b"nested@example.com").hexdigest()
        assert recorded_payload["nested_dict"] == {
            "email": {"hash": nested_hash, "length": 18},  # String value hashed
            "number": 123,  # Non-string value preserved
            "_private": "preserve_me",  # Private key preserved
        }

        # Regular fields processed normally
        value_hash = hashlib.sha1(b"value").hexdigest()
        assert recorded_payload["regular"] == {"hash": value_hash, "length": 5}

    def test_dataset_open_preserves_schema_and_raw_path(self, tmp_path):
        """Dataset schema strings should remain readable while paths stay redacted."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        schema = {"id": "Int64", "name": "Utf8"}
        recorder.record_dataset_open(path="/tmp/sample.parquet", schema=schema, lazy=True)

        events = list(recorder.iter_events())
        assert events and events[0].type == "dataset_open"
        payload = events[0].payload

        assert payload["schema"] == schema
        assert payload["path"]["basename"] == "sample.parquet"
        assert payload["_raw_path"] == "/tmp/sample.parquet"

    def test_status_text_not_redacted(self, tmp_path):
        """Status events should keep their text as-is."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        recorder.record_status("All systems nominal")

        events = list(recorder.iter_events())
        assert events and events[-1].type == "status"
        assert events[-1].payload["text"] == "All systems nominal"

    def test_frame_text_not_redacted(self, tmp_path):
        """Frame events should preserve rendered text output."""
        config = RecorderConfig(enabled=True, cell_redaction="hash_strings", output_dir=tmp_path)
        recorder = Recorder(config)

        recorder.record_frame(frame_text="table output", frame_hash="deadbeef")

        events = list(recorder.iter_events())
        assert events and events[-1].type == "frame"
        payload = events[-1].payload
        assert payload["hash"] == "deadbeef"
        assert payload["text"] == "table output"

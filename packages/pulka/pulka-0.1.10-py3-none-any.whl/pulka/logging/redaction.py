"""Path redaction utilities for the flight recorder."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Protocol

# Precompile regexes at the module level to avoid runtime recompilation
_EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
_IBAN_REGEX = re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]{0,16})?\b")
_PHONE_REGEX = re.compile(r"(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")


class RedactionPolicy(Protocol):
    """Protocol for redaction policies that transform values."""

    def apply_to_value(self, value: Any) -> Any:
        """Apply redaction to a value, returning the possibly transformed result."""
        ...


class NoRedactionPolicy:
    """Policy that returns values unchanged."""

    def apply_to_value(self, value: Any) -> Any:
        return value


class HashStringsPolicy:
    """Policy that hashes string values, replacing them with {hash, length} dicts."""

    def apply_to_value(self, value: Any) -> Any:
        if isinstance(value, str):
            digest = hashlib.sha1(value.encode("utf-8")).hexdigest()
            return {"hash": digest, "length": len(value)}
        return value


class MaskPatternsPolicy:
    """Policy that masks sensitive patterns in string values."""

    def apply_to_value(self, value: Any) -> Any:
        if isinstance(value, str):
            # Apply each pattern and replace with ***
            result = value
            for regex in [_EMAIL_REGEX, _IBAN_REGEX, _PHONE_REGEX]:
                result = regex.sub("***", result)
            return result
        return value


def redaction_policy_from_name(name: str) -> RedactionPolicy:
    """Create a redaction policy instance from a policy name.

    Args:
        name: Policy name (case-insensitive). Supports aliases like 'hash' -> 'hash_strings'.

    Returns:
        An instance of the appropriate RedactionPolicy.

    Raises:
        ValueError: If the name is not a recognized policy.
    """
    normalized = name.lower().strip()

    # Support aliases
    if normalized in ("hash", "hash_strings", "hashstrings"):
        return HashStringsPolicy()
    elif normalized == "none":
        return NoRedactionPolicy()
    elif normalized in ("mask", "mask_patterns", "maskpatterns"):
        return MaskPatternsPolicy()
    else:
        available = ["none", "hash", "hash_strings", "mask", "mask_patterns"]
        raise ValueError(f"Unknown redaction policy '{name}'. Available: {', '.join(available)}")


def redact_path(path: str) -> dict[str, str]:
    """Redact a path by returning its basename and SHA1 digest.

    Args:
        path: The path string to redact

    Returns:
        A dict with "basename" and "digest" keys
    """
    path_obj = Path(path)
    # Use lowercase SHA1 of the original path string as input to maintain case sensitivity
    digest = hashlib.sha1(path.encode("utf-8")).hexdigest()
    return {"basename": path_obj.name, "digest": digest}


def redact_paths(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Redact paths in a payload dictionary.

    Looks for values that are strings and might be paths, using redact_path on them.
    Only handles top-level keys that signal path-like data (ending with '_path',
    or exact 'path'/'paths').

    Args:
        payload: Dictionary to process

    Returns:
        New dictionary with path values redacted where appropriate
    """
    result: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(key, str) and key.startswith("_"):
            # Private fields (e.g. _raw_path) preserve their original value.
            result[key] = value
            continue

        if _looks_redacted(value):
            result[key] = value
            continue

        if isinstance(value, str) and isinstance(key, str) and _is_path_key(key):
            result[key] = redact_path(value)
        else:
            # Shallow handling only; nested mappings are left untouched to avoid
            # mutating unrelated payload structures (e.g. dataset schemas).
            result[key] = value
    return result


def _is_path_key(key: str) -> bool:
    """Check if a key name suggests it contains a path value.

    Args:
        key: The key to check

    Returns:
        True if the key indicates a path field
    """
    return key in ("path", "paths") or key.lower().endswith("_path")


def _looks_redacted(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    return set(value.keys()) >= {"basename", "digest"}

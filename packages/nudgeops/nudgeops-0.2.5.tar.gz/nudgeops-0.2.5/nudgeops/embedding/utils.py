"""
Utility functions for embedding operations.

Provides:
- Cosine similarity calculation
- Text normalization for embedding
- Hash computation for exact matching
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

import numpy as np


def cosine_similarity(vec_a: list[float] | np.ndarray, vec_b: list[float] | np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec_a: First vector (384 floats for BGE-small)
        vec_b: Second vector

    Returns:
        Cosine similarity score between -1.0 and 1.0
        Returns 0.0 if either vector is zero-length or all zeros
    """
    a = np.asarray(vec_a, dtype=np.float32)
    b = np.asarray(vec_b, dtype=np.float32)

    if a.size == 0 or b.size == 0:
        return 0.0

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent embedding.

    Performs:
    - Lowercase conversion
    - Whitespace normalization
    - Punctuation standardization

    Args:
        text: Raw input text

    Returns:
        Normalized text string
    """
    # Lowercase
    text = text.lower()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def normalize_json_args(args: dict[str, Any]) -> str:
    """
    Normalize JSON arguments for consistent hashing.

    Ensures:
    - Keys are sorted recursively
    - Consistent JSON serialization
    - Handles nested dicts and lists

    Args:
        args: Tool arguments dictionary

    Returns:
        Normalized JSON string
    """

    def sort_nested(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: sort_nested(v) for k, v in sorted(obj.items())}
        elif isinstance(obj, list):
            return [sort_nested(item) for item in obj]
        else:
            return obj

    sorted_args = sort_nested(args)
    return json.dumps(sorted_args, separators=(",", ":"), ensure_ascii=True)


def compute_hash(data: str | dict[str, Any]) -> str:
    """
    Compute SHA-256 hash of data for exact matching.

    Args:
        data: String or dict to hash. Dicts are normalized first.

    Returns:
        Hex-encoded SHA-256 hash string
    """
    if isinstance(data, dict):
        data = normalize_json_args(data)

    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def format_step_descriptor(
    tool_name: str,
    tool_args: dict[str, Any] | None,
    outcome: str,
) -> str:
    """
    Format a step descriptor for embedding.

    Creates a consistent string representation of an agent action
    that captures the semantic meaning for Type II detection.

    Format: "ACTION: {tool}({args}) | RESULT: {outcome}"

    Args:
        tool_name: Name of the tool called
        tool_args: Arguments passed to the tool
        outcome: Result type (success, empty, error)

    Returns:
        Formatted step descriptor string
    """
    # Format args as a compact representation
    if tool_args:
        # Take first few key-value pairs for brevity
        args_preview = ", ".join(
            f"{k}={repr(v)[:50]}" for k, v in list(tool_args.items())[:3]
        )
        if len(tool_args) > 3:
            args_preview += ", ..."
    else:
        args_preview = ""

    return f"ACTION: {tool_name}({args_preview}) | RESULT: {outcome}"


def check_negation_difference(text_a: str, text_b: str) -> bool:
    """
    Check if two texts differ primarily by negation.

    Used to handle the embedding "negation blind spot" where
    "delete file" and "do NOT delete file" have similar embeddings.

    Args:
        text_a: First text
        text_b: Second text

    Returns:
        True if one text has negation words the other lacks
    """
    negation_words = {"not", "never", "don't", "dont", "failed", "stop", "error", "no", "cannot"}

    tokens_a = set(normalize_text(text_a).split())
    tokens_b = set(normalize_text(text_b).split())

    neg_in_a = bool(tokens_a & negation_words)
    neg_in_b = bool(tokens_b & negation_words)

    # Return True if exactly one has negation
    return neg_in_a != neg_in_b

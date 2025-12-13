"""
Converts (Action, Result, Environment) → StepRecord.

This is the bridge between domain-specific mock environments
and domain-agnostic detectors.

Key insight: Detectors only see StepRecords.
They don't know if it came from code or shopping.
This adapter is what makes NudgeOps truly universal.
"""

from __future__ import annotations

import hashlib
from typing import Any

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment
from nudgeops.core.state import StepRecord, create_step_record


def build_step_record(
    action: Action,
    result: Result,
    env: IMockEnvironment,
    agent_id: str = "test_agent",
    use_real_embeddings: bool = False,
) -> StepRecord:
    """
    Universal adapter: ANY (Action, Result, Env) → StepRecord.

    This function is the same for all domains.
    It extracts the information detectors need:

    1. tool_name: What tool was used (for basic classification)
    2. tool_args_hash: Hash of args (for Type I stutter detection)
    3. thought_embedding: Vector of thought (for Type II semantic detection)
    4. state_snapshot_hash: Hash of env state (for Type III phantom detection)
    5. agent_id: Which agent (for Type IV ping-pong detection)
    6. outcome_type: success/empty/error (for context)

    Args:
        action: The action that was taken
        result: The result from the environment
        env: The environment (to get state hash)
        agent_id: Identifier for multi-agent scenarios
        use_real_embeddings: If True, use actual FastEmbed model.
                            If False, use deterministic fake embeddings (faster).

    Returns:
        StepRecord ready for detector consumption
    """
    tool_args_hash = _hash_tool_args(action.tool_args)

    if use_real_embeddings:
        # Import actual embedding service for real embeddings
        from nudgeops.embedding.service import get_embedding_service

        embedder = get_embedding_service()
        thought_embedding = embedder.embed(action.thought_text)
    else:
        # Use fake embeddings for fast, deterministic tests
        thought_embedding = _fake_embed(action.thought_text)

    return create_step_record(
        tool_name=action.tool_name,
        tool_args_hash=tool_args_hash,
        thought_embedding=thought_embedding,
        state_snapshot_hash=env.get_state_hash(),
        agent_id=agent_id,
        outcome_type=result.outcome_type,
        raw_tool_args=action.tool_args,
    )


def _hash_tool_args(args: dict[str, Any]) -> str:
    """
    Create a deterministic hash of tool arguments.

    Used for Type I (Stutter) detection.
    Same tool + same args = same hash = potential stutter.
    """
    # Sort items for deterministic ordering
    items = tuple(sorted(args.items()))
    return hashlib.sha256(repr(items).encode()).hexdigest()[:16]


# Semantic groups for fake embeddings
# Text in the same group → identical embedding → similarity = 1.0
# Text in different groups → different embedding → similarity ≈ 0
SEMANTIC_GROUPS: dict[str, list[str]] = {
    # Size variations (all mean XL)
    "size_xl": ["xl", "extra large", "x-large", "extra-large", "xlarge"],
    # Code modification actions
    "modify_code": ["edit", "fix", "patch", "refactor", "modify", "update", "change"],
    # Test/verification actions
    "run_tests": ["run tests", "pytest", "unittest", "test", "verify", "check"],
    # Search variations
    "search_laptop": ["laptop", "notebook", "portable computer", "laptops", "notebooks"],
    # Submit variations
    "submit_code": ["submit", "commit", "push", "deploy", "publish"],
    # Fix bug variations
    "fix_bug": ["fix the bug", "repair the issue", "solve the problem", "debug"],
}


def _fake_embed(text: str, dim: int = 384) -> list[float]:
    """
    Create a fake embedding for testing.

    This is NOT a real embedding model. It's designed to:
    1. Be fast (no model loading)
    2. Be deterministic (same text → same vector)
    3. Preserve semantic similarity for testing Type II detection

    How it works:
    - Text in the same SEMANTIC_GROUP → identical embedding
    - Text in different groups → different embeddings
    - Unknown text → hash-based embedding

    This lets us test that Type II detection works without
    requiring a real embedding model.

    Args:
        text: The text to embed
        dim: Embedding dimension (should match your real model, typically 384)

    Returns:
        List of floats representing the embedding
    """
    normalized = text.lower().strip()

    # Find which semantic group this text belongs to
    matched_group = None
    for group_name, patterns in SEMANTIC_GROUPS.items():
        for pattern in patterns:
            if pattern in normalized:
                matched_group = group_name
                break
        if matched_group:
            break

    if matched_group:
        # Same group → same embedding → similarity = 1.0
        h = hashlib.sha256(matched_group.encode()).digest()
    else:
        # Unknown text → hash of the text itself
        h = hashlib.sha256(normalized.encode()).digest()

    # Convert hash bytes to floats in [0, 1]
    # Extend to full dimension by cycling through hash
    embedding: list[float] = []
    for i in range(dim):
        byte_index = i % len(h)
        embedding.append(h[byte_index] / 255.0)

    return embedding


def compute_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    This is used by Type II detector to compare thought embeddings.

    Returns:
        Float in [-1, 1], where 1 = identical, 0 = orthogonal, -1 = opposite
    """
    if len(vec1) != len(vec2):
        raise ValueError(f"Vector dimension mismatch: {len(vec1)} vs {len(vec2)}")

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

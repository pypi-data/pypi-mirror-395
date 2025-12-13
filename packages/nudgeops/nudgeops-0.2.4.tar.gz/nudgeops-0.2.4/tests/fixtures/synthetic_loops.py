"""
Synthetic loop scenarios for testing detectors.

These fixtures represent the four types of loops NudgeOps detects:
- Type I: Stutter (exact repetition)
- Type II: Insanity (semantic repetition)
- Type III: Phantom Progress (state frozen)
- Type IV: Ping-Pong (multi-agent deadlock)
"""

from __future__ import annotations

import random

from nudgeops.core.state import StepRecord, create_step_record
from nudgeops.embedding.utils import compute_hash


def _generate_mock_embedding(seed: int = 42) -> list[float]:
    """Generate a mock 384-dimensional embedding."""
    random.seed(seed)
    return [random.random() for _ in range(384)]


def _generate_similar_embedding(base: list[float], seed: int = 43) -> list[float]:
    """Generate embedding similar to base (cosine sim > 0.95)."""
    random.seed(seed)
    return [v + random.uniform(-0.02, 0.02) for v in base]


# ============================================================================
# TYPE I: STUTTER - Exact same action repeated
# ============================================================================

def create_stutter_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a Type I stutter scenario.

    Returns:
        Tuple of (current_step, history) where current + history has 3+ identical actions.
        Type I now requires min_count=3 consecutive identical actions.
    """
    args_hash = compute_hash({"query": "return policy"})
    embedding = _generate_mock_embedding(100)

    # Need 2 in history + 1 current = 3 total for detection
    history = [
        create_step_record(
            tool_name="search",
            tool_args_hash=args_hash,
            thought_embedding=embedding,
            outcome_type="empty",
            raw_tool_args={"query": "return policy"},
        ),
        create_step_record(
            tool_name="search",
            tool_args_hash=args_hash,  # SAME hash
            thought_embedding=embedding,
            outcome_type="empty",
            raw_tool_args={"query": "return policy"},
        ),
    ]

    current = create_step_record(
        tool_name="search",
        tool_args_hash=args_hash,  # SAME hash (3rd repetition)
        thought_embedding=embedding,
        outcome_type="empty",
        raw_tool_args={"query": "return policy"},
    )

    return current, history


# History with 2 identical steps - adding a 3rd will trigger detection
TYPE_I_STUTTER_HISTORY = [
    create_step_record(
        tool_name="search",
        tool_args_hash=compute_hash({"query": "return policy"}),
        outcome_type="empty",
    ),
    create_step_record(
        tool_name="search",
        tool_args_hash=compute_hash({"query": "return policy"}),  # SAME
        outcome_type="empty",
    ),
]


# ============================================================================
# TYPE II: INSANITY - Semantic repetition (different words, same intent)
# ============================================================================

def create_insanity_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a Type II insanity scenario.

    Returns:
        Tuple of (current_step, history) with semantically similar steps
    """
    base_embedding = _generate_mock_embedding(200)

    history = [
        create_step_record(
            tool_name="search",
            tool_args_hash=compute_hash({"query": "return policy"}),
            thought_embedding=base_embedding,
            outcome_type="empty",
            raw_tool_args={"query": "return policy"},
        ),
        create_step_record(
            tool_name="search",
            tool_args_hash=compute_hash({"query": "refund policy"}),
            thought_embedding=_generate_similar_embedding(base_embedding, 201),
            outcome_type="empty",
            raw_tool_args={"query": "refund policy"},
        ),
        create_step_record(
            tool_name="search",
            tool_args_hash=compute_hash({"query": "how to return items"}),
            thought_embedding=_generate_similar_embedding(base_embedding, 202),
            outcome_type="empty",
            raw_tool_args={"query": "how to return items"},
        ),
    ]

    current = create_step_record(
        tool_name="search",
        tool_args_hash=compute_hash({"query": "return info"}),
        thought_embedding=_generate_similar_embedding(base_embedding, 203),
        outcome_type="empty",
        raw_tool_args={"query": "return info"},
    )

    return current, history


TYPE_II_INSANITY_HISTORY = create_insanity_scenario()[1]


# ============================================================================
# TYPE III: PHANTOM PROGRESS - Different actions, state unchanged
# ============================================================================

def create_phantom_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a Type III phantom progress scenario.

    Returns:
        Tuple of (current_step, history) where actions differ but state is same
    """
    frozen_state_hash = compute_hash("page_content_that_never_changes")

    history = [
        create_step_record(
            tool_name="click",
            tool_args_hash=compute_hash({"button": "next"}),
            state_snapshot_hash=frozen_state_hash,
            outcome_type="success",
        ),
        create_step_record(
            tool_name="click",
            tool_args_hash=compute_hash({"button": "load_more"}),  # Different action
            state_snapshot_hash=frozen_state_hash,  # SAME state
            outcome_type="success",
        ),
    ]

    current = create_step_record(
        tool_name="scroll",  # Different tool
        tool_args_hash=compute_hash({"direction": "down"}),
        state_snapshot_hash=frozen_state_hash,  # STILL same state
        outcome_type="success",
    )

    return current, history


TYPE_III_PHANTOM_HISTORY = create_phantom_scenario()[1]


# ============================================================================
# TYPE IV: PING-PONG - Multi-agent circular handoffs
# ============================================================================

def create_pingpong_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a Type IV ping-pong scenario.

    This represents a true deadlock where:
    - Agents keep handing off to each other (A→B→A→B→A)
    - State is NOT changing (same state_snapshot_hash = no real progress)

    Returns:
        Tuple of (current_step, history) with A→B→A→B pattern
    """
    # Frozen state - the document never actually improves
    frozen_state = compute_hash("document_stuck_in_limbo")

    history = [
        create_step_record(
            tool_name="draft",
            tool_args_hash=compute_hash({"content": "draft v1"}),
            agent_id="writer",
            state_snapshot_hash=frozen_state,  # State not changing
            outcome_type="success",
        ),
        create_step_record(
            tool_name="review",
            tool_args_hash=compute_hash({"feedback": "revise tone"}),
            agent_id="critic",
            state_snapshot_hash=frozen_state,  # State not changing
            outcome_type="success",
        ),
        create_step_record(
            tool_name="draft",
            tool_args_hash=compute_hash({"content": "draft v2"}),
            agent_id="writer",
            state_snapshot_hash=frozen_state,  # State not changing
            outcome_type="success",
        ),
        create_step_record(
            tool_name="review",
            tool_args_hash=compute_hash({"feedback": "change back"}),
            agent_id="critic",
            state_snapshot_hash=frozen_state,  # State not changing
            outcome_type="success",
        ),
    ]

    current = create_step_record(
        tool_name="draft",
        tool_args_hash=compute_hash({"content": "draft v3"}),
        agent_id="writer",  # Pattern: W-C-W-C-W
        state_snapshot_hash=frozen_state,  # Still stuck
        outcome_type="success",
    )

    return current, history


TYPE_IV_PINGPONG_HISTORY = create_pingpong_scenario()[1]

"""
Legitimate patterns that should NOT trigger loop detection.

These fixtures represent normal agent behavior that might look
suspicious but is actually valid progress.
"""

from __future__ import annotations

import random

from nudgeops.core.state import StepRecord, create_step_record
from nudgeops.embedding.utils import compute_hash


def _generate_mock_embedding(seed: int) -> list[float]:
    """Generate a mock 384-dimensional embedding."""
    random.seed(seed)
    return [random.random() for _ in range(384)]


# ============================================================================
# VALID ITERATION - Running tests, fixing, running again
# ============================================================================

def create_valid_iteration_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a valid iteration scenario (test → fix → test → fix → test).

    This should NOT trigger detection because:
    - The agent is making progress (error count decreasing)
    - Each iteration has different state (different error messages)

    Returns:
        Tuple of (current_step, history)
    """
    history = [
        create_step_record(
            tool_name="run_tests",
            tool_args_hash=compute_hash({"suite": "unit"}),
            state_snapshot_hash=compute_hash("3 failures"),
            thought_embedding=_generate_mock_embedding(300),
            outcome_type="error",
        ),
        create_step_record(
            tool_name="edit_code",
            tool_args_hash=compute_hash({"file": "auth.py", "fix": "1"}),
            state_snapshot_hash=compute_hash("code edited 1"),
            thought_embedding=_generate_mock_embedding(301),
            outcome_type="success",
        ),
        create_step_record(
            tool_name="run_tests",
            tool_args_hash=compute_hash({"suite": "unit"}),
            state_snapshot_hash=compute_hash("2 failures"),  # PROGRESS!
            thought_embedding=_generate_mock_embedding(302),
            outcome_type="error",
        ),
        create_step_record(
            tool_name="edit_code",
            tool_args_hash=compute_hash({"file": "auth.py", "fix": "2"}),
            state_snapshot_hash=compute_hash("code edited 2"),
            thought_embedding=_generate_mock_embedding(303),
            outcome_type="success",
        ),
    ]

    current = create_step_record(
        tool_name="run_tests",
        tool_args_hash=compute_hash({"suite": "unit"}),
        state_snapshot_hash=compute_hash("0 failures"),  # SUCCESS!
        thought_embedding=_generate_mock_embedding(304),
        outcome_type="success",
    )

    return current, history


VALID_ITERATION_HISTORY = create_valid_iteration_scenario()[1]


# ============================================================================
# VALID SEARCH REFINEMENT - Narrowing down results
# ============================================================================

def create_valid_search_refinement_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a valid search refinement scenario.

    This should NOT trigger Type II because:
    - Each search is genuinely different (narrowing down)
    - Results are getting better (more specific)
    - Embeddings should be sufficiently different

    Returns:
        Tuple of (current_step, history)
    """
    history = [
        create_step_record(
            tool_name="search",
            tool_args_hash=compute_hash({"query": "python libraries"}),
            state_snapshot_hash=compute_hash("500 results"),
            thought_embedding=_generate_mock_embedding(400),
            outcome_type="success",
        ),
        create_step_record(
            tool_name="search",
            tool_args_hash=compute_hash({"query": "python machine learning libraries"}),
            state_snapshot_hash=compute_hash("50 results"),
            thought_embedding=_generate_mock_embedding(500),  # Different seed = different embedding
            outcome_type="success",
        ),
    ]

    current = create_step_record(
        tool_name="search",
        tool_args_hash=compute_hash({"query": "pytorch vs tensorflow comparison 2024"}),
        state_snapshot_hash=compute_hash("5 results"),
        thought_embedding=_generate_mock_embedding(600),  # Different seed
        outcome_type="success",
    )

    return current, history


VALID_SEARCH_REFINEMENT_HISTORY = create_valid_search_refinement_scenario()[1]


# ============================================================================
# VALID MULTI-AGENT WORKFLOW - Sequential, not circular
# ============================================================================

def create_valid_multiagent_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a valid multi-agent workflow.

    This should NOT trigger Type IV because:
    - The pattern is sequential (A → B → C → D), not circular
    - Each agent has a distinct role and moves forward

    Returns:
        Tuple of (current_step, history)
    """
    history = [
        create_step_record(
            tool_name="plan",
            tool_args_hash=compute_hash({"task": "create feature"}),
            agent_id="planner",
            outcome_type="success",
        ),
        create_step_record(
            tool_name="design",
            tool_args_hash=compute_hash({"spec": "feature spec"}),
            agent_id="designer",
            outcome_type="success",
        ),
        create_step_record(
            tool_name="implement",
            tool_args_hash=compute_hash({"code": "feature code"}),
            agent_id="developer",
            outcome_type="success",
        ),
    ]

    current = create_step_record(
        tool_name="test",
        tool_args_hash=compute_hash({"suite": "integration"}),
        agent_id="tester",  # Sequential: planner → designer → developer → tester
        outcome_type="success",
    )

    return current, history


VALID_MULTIAGENT_HISTORY = create_valid_multiagent_scenario()[1]


# ============================================================================
# VALID RETRY AFTER ERROR - Single retry, not a loop
# ============================================================================

def create_valid_retry_scenario() -> tuple[StepRecord, list[StepRecord]]:
    """
    Create a valid retry scenario.

    This should NOT trigger detection because:
    - Only one retry (not a loop)
    - Retry succeeds

    Returns:
        Tuple of (current_step, history)
    """
    history = [
        create_step_record(
            tool_name="api_call",
            tool_args_hash=compute_hash({"endpoint": "/users"}),
            state_snapshot_hash=compute_hash("timeout error"),
            outcome_type="error",
        ),
    ]

    current = create_step_record(
        tool_name="api_call",
        tool_args_hash=compute_hash({"endpoint": "/users"}),  # Same call
        state_snapshot_hash=compute_hash("200 OK"),  # But different result
        outcome_type="success",
    )

    return current, history


VALID_RETRY_HISTORY = create_valid_retry_scenario()[1]

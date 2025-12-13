"""
Integration tests for NudgeOps with LangGraph.

Tests the full flow: state → detection → scoring → intervention.
"""

from __future__ import annotations

import pytest

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from nudgeops.core.state import (
    AgentState,
    GuardConfig,
    create_initial_loop_status,
)
from nudgeops.integrations.langgraph import NudgeOpsNode, NudgeOpsState
from nudgeops.integrations.extractors import (
    extract_step_from_state,
    extract_tool_info,
    classify_outcome,
)


class TestExtractors:
    """Tests for state extraction functions."""

    def test_extract_tool_info_from_ai_message(self):
        """Should extract tool name and args from AIMessage."""
        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "search",
                    "args": {"query": "test"},
                    "id": "call_123",
                }
            ],
        )

        result = extract_tool_info(message)

        assert result is not None
        assert result[0] == "search"
        assert result[1] == {"query": "test"}

    def test_extract_tool_info_no_tool_calls(self):
        """Should return None when no tool calls."""
        message = AIMessage(content="Just text, no tools")

        result = extract_tool_info(message)

        assert result is None

    def test_classify_outcome_success(self):
        """Should classify successful result."""
        message = ToolMessage(
            content="Found 5 results: ...",
            tool_call_id="call_123",
        )

        result = classify_outcome(message)

        assert result == "success"

    def test_classify_outcome_empty(self):
        """Should classify empty result."""
        message = ToolMessage(
            content="No results found",
            tool_call_id="call_123",
        )

        result = classify_outcome(message)

        assert result == "empty"

    def test_classify_outcome_error(self):
        """Should classify error result."""
        message = ToolMessage(
            content="Error: 404 not found",
            tool_call_id="call_123",
        )

        result = classify_outcome(message)

        assert result == "error"

    def test_extract_step_from_state(self):
        """Should extract StepRecord from full state."""
        state = {
            "messages": [
                HumanMessage(content="Find return policy"),
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "search",
                            "args": {"query": "return policy"},
                            "id": "call_1",
                        }
                    ],
                ),
                ToolMessage(content="No results", tool_call_id="call_1"),
            ],
            "trajectory_scratchpad": [],
            "loop_status": create_initial_loop_status(),
        }

        step = extract_step_from_state(state)

        assert step is not None
        assert step["tool_name"] == "search"
        assert step["outcome_type"] == "empty"
        assert step["tool_args_hash"] != ""

    def test_extract_step_no_tool_calls(self):
        """Should return None when no tool calls in state."""
        state = {
            "messages": [
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),
            ],
        }

        step = extract_step_from_state(state)

        assert step is None


class TestNudgeOpsNode:
    """Tests for the NudgeOpsNode LangGraph integration."""

    def test_node_initialization(self):
        """Should initialize with default thresholds."""
        node = NudgeOpsNode()

        assert node.guard._config.nudge_threshold == 2.0
        assert node.guard._config.stop_threshold == 3.0

    def test_node_initialization_custom_thresholds(self):
        """Should accept custom thresholds."""
        node = NudgeOpsNode(nudge_threshold=1.5, stop_threshold=2.5)

        assert node.guard._config.nudge_threshold == 1.5
        assert node.guard._config.stop_threshold == 2.5

    def test_node_returns_state_when_no_tools(self):
        """Should return state unchanged when no tool results."""
        node = NudgeOpsNode()
        state: NudgeOpsState = {
            "messages": [{"role": "assistant", "content": "Just chatting"}],
            "tool_calls": [],
            "tool_results": [],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }

        result = node(state)

        # State should be unchanged (no tool execution)
        assert result.get("loop_score", 0.0) == 0.0
        assert result.get("should_stop", False) is False

    def test_node_observe_on_first_step(self):
        """Should OBSERVE on first step (no history)."""
        node = NudgeOpsNode()
        state: NudgeOpsState = {
            "messages": [{"role": "assistant", "content": "Searching..."}],
            "tool_calls": [],
            "tool_results": [
                {"tool_name": "search", "tool_args": {"q": "test"}, "content": "Results"}
            ],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }

        result = node(state)

        # First step should observe and continue
        assert result.get("should_stop", False) is False
        assert result["loop_score"] == 0.0  # No loop detected on first step


class TestEndToEndFlow:
    """End-to-end tests simulating agent execution."""

    def test_observe_nudge_stop_sequence(self):
        """Test the full intervention ladder: OBSERVE → NUDGE → STOP.

        With min_count=3 for Type I stutter detection:
        - Steps 1-2: OBSERVE (not enough repetitions yet)
        - Step 3: NUDGE (3rd identical action triggers stutter detection)
        - Step 4: STOP (continues looping after nudge)
        """
        node = NudgeOpsNode(nudge_threshold=2.0, stop_threshold=3.0)

        state: NudgeOpsState = {
            "messages": [],
            "tool_calls": [],
            "tool_results": [],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }

        # Step 1: First tool call - should OBSERVE
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {"q": "policy"}, "content": "empty"}
        ]
        state["state_payload"] = {"unchanged": True}
        state = node(state)
        assert state.get("should_stop", False) is False
        assert state.get("nudge_count", 0) == 0

        # Step 2: Second identical call - still OBSERVE (need 3 for stutter)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {"q": "policy"}, "content": "empty"}
        ]
        state = node(state)
        assert state.get("should_stop", False) is False
        assert state.get("nudge_count", 0) == 0

        # Step 3: Third identical call - should NUDGE (Type I stutter detected)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {"q": "policy"}, "content": "empty"}
        ]
        state = node(state)
        # Should have nudged (score >= 2.0)
        assert state["loop_score"] >= 2.0
        # Either nudged or went straight to stop
        assert state.get("nudge_count", 0) >= 1 or state.get("should_stop", False)

        # Step 4: Still stuck - should STOP
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {"q": "policy"}, "content": "empty"}
        ]
        state = node(state)
        # Score should exceed stop threshold now
        assert state["loop_score"] >= 3.0
        assert state["should_stop"] is True

    def test_recovery_after_nudge(self):
        """Agent should be able to recover after receiving nudge."""
        # Use higher thresholds to avoid premature stop
        node = NudgeOpsNode(nudge_threshold=10.0, stop_threshold=20.0)

        state: NudgeOpsState = {
            "messages": [],
            "tool_calls": [],
            "tool_results": [],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }

        # Build up score with repeated actions
        for i in range(4):
            state["tool_results"] = [
                {"tool_name": "stuck_action", "tool_args": {}, "content": "fail"}
            ]
            state["state_payload"] = {"stuck": True}
            state = node(state)

        high_score = state["loop_score"]
        assert high_score > 0

        # Now recover with different unique actions (more iterations to ensure decay)
        for i in range(8):
            state["tool_results"] = [
                {"tool_name": f"unique_{i}", "tool_args": {"step": i}, "content": f"ok_{i}"}
            ]
            state["state_payload"] = {"progress": i}
            state = node(state)

        # Score should have decayed (may hit floor at 0)
        assert state["loop_score"] <= high_score, \
            f"Score should decay from {high_score}, got {state['loop_score']}"

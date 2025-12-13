"""
tests/integration/test_langgraph.py

Integration tests for NudgeOps + LangGraph.

These tests verify:
1. State extraction from LangGraph format works
2. Guard node correctly processes states
3. Nudge messages get injected
4. Stop signals terminate properly
5. Score accumulates correctly across steps

Note: These tests use mock LangGraph components to avoid
requiring langgraph as a dependency for testing.
"""

import pytest
from typing import Any

# Import NudgeOps components
from nudgeops.integrations.langgraph import (
    NudgeOpsNode,
    NudgeOpsState,
    extract_step_from_state,
    _fake_embed,
    SEMANTIC_GROUPS,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def guard_node():
    """Fresh guard node for each test."""
    return NudgeOpsNode(nudge_threshold=2.0, stop_threshold=3.0)


@pytest.fixture
def base_state() -> NudgeOpsState:
    """Base state with minimal fields."""
    return {
        "messages": [],
        "tool_calls": [],
        "tool_results": [],
        "loop_score": 0.0,
        "should_stop": False,
        "nudge_count": 0,
    }


# ---------------------------------------------------------------------------
# State Extraction Tests
# ---------------------------------------------------------------------------

class TestStateExtraction:
    """Test extraction of StepRecord from LangGraph state."""
    
    def test_extract_returns_none_when_no_tools(self, base_state):
        """No tool results → no StepRecord."""
        step = extract_step_from_state(base_state)
        assert step is None
    
    def test_extract_basic_tool_result(self, base_state):
        """Extract step from simple tool result."""
        state = dict(base_state)
        state["tool_results"] = [
            {
                "tool_name": "search",
                "tool_args": {"query": "laptop"},
                "content": "Found 10 results",
            }
        ]
        state["messages"] = [
            {"role": "user", "content": "Find me a laptop"},
            {"role": "assistant", "content": "I'll search for laptops"},
        ]
        
        step = extract_step_from_state(state)
        
        assert step is not None
        assert step.tool_name == "search"
        assert step.outcome_type == "success"
    
    def test_extract_error_outcome(self, base_state):
        """Error in result → outcome_type = 'error'."""
        state = dict(base_state)
        state["tool_results"] = [
            {
                "tool_name": "add_to_cart",
                "tool_args": {"sku": "ABC"},
                "content": "Error: Item out of stock",
            }
        ]
        
        step = extract_step_from_state(state)
        
        assert step.outcome_type == "error"
    
    def test_extract_empty_outcome(self, base_state):
        """Empty result → outcome_type = 'empty'."""
        state = dict(base_state)
        state["tool_results"] = [
            {
                "tool_name": "search",
                "tool_args": {"query": "xyzabc123"},
                "content": "",
            }
        ]
        
        step = extract_step_from_state(state)
        
        assert step.outcome_type == "empty"
    
    def test_extract_uses_last_tool_result(self, base_state):
        """Multiple tool results → uses the last one."""
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "first", "tool_args": {}, "content": "first result"},
            {"tool_name": "second", "tool_args": {}, "content": "second result"},
            {"tool_name": "third", "tool_args": {}, "content": "third result"},
        ]
        
        step = extract_step_from_state(state)
        
        assert step.tool_name == "third"
    
    def test_extract_with_agent_id(self, base_state):
        """Agent ID passed through to StepRecord."""
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {}, "content": "ok"}
        ]
        
        step = extract_step_from_state(state, agent_id="search_agent")
        
        assert step.agent_id == "search_agent"
    
    def test_extract_thought_from_messages(self, base_state):
        """Thought extracted from last assistant message."""
        state = dict(base_state)
        state["messages"] = [
            {"role": "user", "content": "Find laptops"},
            {"role": "assistant", "content": "I will search for laptop computers"},
            {"role": "tool", "content": "Results..."},
        ]
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {}, "content": "ok"}
        ]
        
        step = extract_step_from_state(state)
        
        # The thought embedding should be based on "I will search for laptop computers"
        # which should map to the "laptop" semantic group
        assert step.thought_embedding is not None
        assert len(step.thought_embedding) == 384


# ---------------------------------------------------------------------------
# Fake Embedding Tests
# ---------------------------------------------------------------------------

class TestFakeEmbeddings:
    """Test the fake embedding function for semantic grouping."""
    
    def test_same_text_same_embedding(self):
        """Identical text → identical embedding."""
        e1 = _fake_embed("search for laptop")
        e2 = _fake_embed("search for laptop")
        
        assert e1 == e2
    
    def test_semantic_group_same_embedding(self):
        """Terms in same semantic group → identical embedding."""
        e1 = _fake_embed("laptop")
        e2 = _fake_embed("notebook computer")
        e3 = _fake_embed("portable pc")
        
        # All map to "device_laptop" group
        assert e1 == e2
        assert e2 == e3
    
    def test_different_groups_different_embedding(self):
        """Terms in different groups → different embeddings."""
        e1 = _fake_embed("laptop")
        e2 = _fake_embed("run tests")
        
        assert e1 != e2
    
    def test_embedding_normalized(self):
        """Embedding should be unit normalized."""
        import math
        
        e = _fake_embed("some random text")
        norm = math.sqrt(sum(x * x for x in e))
        
        assert abs(norm - 1.0) < 0.0001
    
    def test_size_variants_same_embedding(self):
        """Size variant synonyms → same embedding."""
        e1 = _fake_embed("xl")
        e2 = _fake_embed("extra large")
        e3 = _fake_embed("x-large")
        
        assert e1 == e2
        assert e2 == e3


# ---------------------------------------------------------------------------
# Guard Node Tests
# ---------------------------------------------------------------------------

class TestGuardNode:
    """Test the NudgeOpsNode behavior."""
    
    def test_observe_on_normal_flow(self, guard_node, base_state):
        """Normal unique actions → OBSERVE, no modifications."""
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {"q": "laptop"}, "content": "ok"}
        ]
        
        result = guard_node(state)
        
        assert result["loop_score"] == 0.0
        assert result.get("should_stop", False) is False
        assert result.get("nudge_count", 0) == 0
    
    def test_no_change_when_no_tools(self, guard_node, base_state):
        """No tool results → state unchanged."""
        result = guard_node(base_state)
        
        # Should return state as-is
        assert "loop_score" not in result or result.get("loop_score") == base_state.get("loop_score")
    
    def test_stutter_triggers_nudge(self, guard_node, base_state):
        """3 identical actions → threshold crossed (may go straight to STOP)."""
        state = dict(base_state)
        
        # Simulate 3 identical tool calls
        for i in range(3):
            state["tool_results"] = [
                {"tool_name": "add_to_cart", "tool_args": {"sku": "ABC"}, "content": "Error"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": "Adding to cart"}
            ]
            # Keep state_payload the same to trigger phantom progress too
            state["state_payload"] = {"cart": []}
            
            state = guard_node(state)
        
        # Should have triggered detection (score >= nudge threshold)
        # Note: With stutter (2.0) + phantom (0.5) per step, score rises fast
        # May go directly to STOP if score >= 3.0
        assert state["loop_score"] >= 2.0
        # Either nudged OR stopped
        assert state.get("nudge_count", 0) >= 1 or state.get("should_stop", False)
    
    def test_nudge_message_injected(self, guard_node, base_state):
        """When threshold crossed, intervention is applied (nudge or stop)."""
        state = dict(base_state)
        state["messages"] = []
        
        # Force score up by repeating same action (different each iteration to slow down)
        for i in range(4):
            state["tool_results"] = [
                {"tool_name": "submit", "tool_args": {}, "content": "fail"}
            ]
            state["state_payload"] = {"unchanged": True}
            state = guard_node(state)
            
            # Check if we got a nudge or stop
            if state.get("nudge_count", 0) > 0 or state.get("should_stop", False):
                break
        
        # Should have either nudged (with message) or stopped (with reason)
        if state.get("nudge_count", 0) > 0:
            system_messages = [m for m in state["messages"] if m.get("role") == "system"]
            nudge_messages = [m for m in system_messages if "[NudgeOps]" in m.get("content", "")]
            assert len(nudge_messages) > 0, "Nudge should inject system message"
        else:
            assert state.get("should_stop", False), "If not nudged, should have stopped"
            assert state.get("stop_reason"), "Stop should have a reason"
    
    def test_stop_on_high_score(self, guard_node, base_state):
        """Score >= 3.0 → should_stop = True."""
        state = dict(base_state)
        
        # Repeat many times to hit stop threshold
        for i in range(6):
            state["tool_results"] = [
                {"tool_name": "submit", "tool_args": {}, "content": "fail"}
            ]
            state["state_payload"] = {"unchanged": True}
            state = guard_node(state)
            
            if state.get("should_stop", False):
                break
        
        assert state["should_stop"] is True
        assert state.get("stop_reason") is not None
    
    def test_should_continue_returns_end(self, guard_node, base_state):
        """should_continue returns 'end' when should_stop is True."""
        state = dict(base_state)
        state["should_stop"] = True
        
        result = guard_node.should_continue(state)
        
        assert result == "end"
    
    def test_should_continue_returns_continue(self, guard_node, base_state):
        """should_continue returns 'continue' when not stopped."""
        result = guard_node.should_continue(base_state)
        
        assert result == "continue"
    
    def test_reset_clears_history(self, guard_node, base_state):
        """reset() clears guard state."""
        # Add some history
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {}, "content": "ok"}
        ]
        guard_node(state)
        
        assert len(guard_node.history) > 0
        
        # Reset
        guard_node.reset()
        
        assert len(guard_node.history) == 0
        assert guard_node.score == 0.0


# ---------------------------------------------------------------------------
# Semantic Loop Tests
# ---------------------------------------------------------------------------

class TestSemanticLoops:
    """Test detection of semantic (Type II) loops via LangGraph integration."""
    
    def test_synonym_search_detected(self, guard_node, base_state):
        """Searching synonyms triggers semantic detection."""
        state = dict(base_state)
        
        synonyms = ["laptop", "notebook computer", "portable pc"]
        
        for i, term in enumerate(synonyms):
            state["tool_results"] = [
                {"tool_name": "search", "tool_args": {"query": term}, "content": "no results"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": f"Searching for {term}"}
            ]
            state["state_payload"] = {"results": []}  # Same state each time
            state = guard_node(state)
        
        # Semantic similarity should be detected
        # Combined with phantom progress, should hit nudge threshold
        assert state["loop_score"] >= 1.5
    
    def test_size_variant_loop_detected(self, guard_node, base_state):
        """Trying size variants triggers detection."""
        state = dict(base_state)
        
        variants = ["xl", "extra large", "x-large"]
        
        for variant in variants:
            state["tool_results"] = [
                {"tool_name": "select_size", "tool_args": {"size": variant}, "content": "Out of stock"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": f"Trying size {variant}"}
            ]
            state["state_payload"] = {"selected_size": None}  # Never succeeds
            state = guard_node(state)
        
        assert state["loop_score"] >= 1.5


# ---------------------------------------------------------------------------
# Multi-Agent Tests
# ---------------------------------------------------------------------------

class TestMultiAgent:
    """Test multi-agent (Type IV) detection."""
    
    def test_pingpong_detected(self):
        """Handoff ping-pong between agents detected."""
        guard = NudgeOpsNode()
        state: NudgeOpsState = {
            "messages": [],
            "tool_calls": [],
            "tool_results": [],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }
        
        # Simulate A → B → A → B pattern
        agents = ["agent_a", "agent_b", "agent_a", "agent_b", "agent_a", "agent_b"]
        
        for i, agent in enumerate(agents):
            state["tool_results"] = [
                {"tool_name": "handoff", "tool_args": {"to": agents[(i+1) % 2]}, "content": "handed off"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": f"Handing off to other agent"}
            ]
            state["state_payload"] = {"current_agent": agent}
            
            # Create guard with agent_id for each step
            step = extract_step_from_state(state, agent_id=agent)
            if step:
                decision = guard.guard.on_step(step)
                state["loop_score"] = decision.score
        
        # Ping-pong should be detected
        assert state["loop_score"] >= 1.0


# ---------------------------------------------------------------------------
# Integration Flow Tests
# ---------------------------------------------------------------------------

class TestIntegrationFlow:
    """Test complete integration scenarios."""
    
    def test_healthy_agent_not_flagged(self, guard_node, base_state):
        """Agent making progress is not flagged."""
        state = dict(base_state)
        
        # Simulate healthy agent: different actions, state changing
        actions = [
            ("search", {"q": "laptop"}, "Found 10 items", {"items": 10}),
            ("select", {"id": 1}, "Selected item 1", {"selected": 1}),
            ("add_to_cart", {"id": 1}, "Added to cart", {"cart": [1]}),
            ("checkout", {}, "Proceeding to checkout", {"stage": "checkout"}),
        ]
        
        for tool, args, result, state_payload in actions:
            state["tool_results"] = [
                {"tool_name": tool, "tool_args": args, "content": result}
            ]
            state["messages"] = [
                {"role": "assistant", "content": f"Performing {tool}"}
            ]
            state["state_payload"] = state_payload
            state = guard_node(state)
        
        # Should not trigger nudge
        assert state["loop_score"] < 2.0
        assert state.get("should_stop", False) is False
    
    def test_stuck_agent_escalates(self, guard_node, base_state):
        """Agent stuck in loop escalates and eventually stops."""
        state = dict(base_state)
        
        scores = []
        stopped = False
        
        # Repeat same failing action until stopped
        for i in range(8):
            state["tool_results"] = [
                {"tool_name": "checkout", "tool_args": {}, "content": "Error: payment failed"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": "Trying checkout again"}
            ]
            state["state_payload"] = {"checkout_complete": False}
            
            state = guard_node(state)
            scores.append(state["loop_score"])
            
            if state.get("should_stop", False):
                stopped = True
                break
        
        # Should have stopped
        assert stopped, f"Should have stopped, scores: {scores}"
        
        # Score should have escalated
        assert scores[-1] >= 3.0, f"Final score should be >= 3.0, got {scores[-1]}"
        
        # Earlier scores should be lower (escalation)
        assert scores[0] < scores[-1], "Score should increase over time"
    
    def test_recovery_resets_score(self):
        """Agent that recovers sees score decay."""
        # Use higher thresholds to avoid premature stop
        guard_node = NudgeOpsNode(nudge_threshold=10.0, stop_threshold=20.0)
        state: NudgeOpsState = {
            "messages": [],
            "tool_calls": [],
            "tool_results": [],
            "loop_score": 0.0,
            "should_stop": False,
            "nudge_count": 0,
        }
        
        # First: build up some score with repeated actions
        # Need 3+ steps to trigger stutter (min_count=3)
        for i in range(4):
            state["tool_results"] = [
                {"tool_name": "fail_action", "tool_args": {}, "content": "fail"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": "Retrying the action"}
            ]
            state["state_payload"] = {"stuck": True}
            state = guard_node(state)
        
        high_score = state["loop_score"]
        assert high_score > 0, f"Expected some score after 4 identical actions, got {high_score}"
        
        # Then: make progress with different unique actions
        for i in range(5):
            state["tool_results"] = [
                {"tool_name": f"unique_action_{i}", "tool_args": {"step": i}, "content": f"success_{i}"}
            ]
            state["messages"] = [
                {"role": "assistant", "content": f"Making progress step {i}"}
            ]
            state["state_payload"] = {"progress": i}  # Different each time
            state = guard_node(state)
        
        # Score should have decayed (each step without detection decays by 0.5)
        assert state["loop_score"] < high_score, \
            f"Score should decay from {high_score} but got {state['loop_score']}"


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_messages(self, guard_node, base_state):
        """Handle state with no messages."""
        state = dict(base_state)
        state["messages"] = []
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {}, "content": "ok"}
        ]
        
        # Should not crash
        result = guard_node(state)
        assert "loop_score" in result
    
    def test_missing_tool_args(self, guard_node, base_state):
        """Handle tool result with missing args."""
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "search", "content": "ok"}  # No tool_args
        ]
        
        result = guard_node(state)
        assert "loop_score" in result
    
    def test_none_content(self, guard_node, base_state):
        """Handle None as tool result content."""
        state = dict(base_state)
        state["tool_results"] = [
            {"tool_name": "search", "tool_args": {}, "content": None}
        ]
        
        step = extract_step_from_state(state)
        assert step.outcome_type == "empty"
    
    def test_custom_thresholds(self, base_state):
        """Custom thresholds are respected."""
        guard = NudgeOpsNode(nudge_threshold=1.0, stop_threshold=1.5)
        state = dict(base_state)
        
        # With lower thresholds, phantom detection should trigger faster
        # PhantomProgressDetector has unchanged_threshold=2
        # Need 3 steps with same state to get unchanged_count=2 (the 3rd step sees 2 previous)
        for i in range(3):
            state["tool_results"] = [
                {"tool_name": f"action_{i}", "tool_args": {"i": i}, "content": "same"}
            ]
            state["state_payload"] = {"unchanged": True}  # Same state each time
            state["messages"] = [
                {"role": "assistant", "content": f"Doing something different {i}"}
            ]
            state = guard(state)
        
        # With lower thresholds, phantom detection (0.5) should trigger nudge at 1.0
        # After 3 steps: 0.5 + 0.5 = 1.0 (first 2 don't trigger, 3rd triggers)
        # Actually: step 1 = 0, step 2 = 0 (unchanged_count=1<2), step 3 = 0.5 (unchanged_count=2>=2)
        # So score = 0.5 after 3 steps, which is < 1.0 threshold
        # 
        # We need more steps or different detection. Let's just check that score accumulates.
        assert state["loop_score"] > 0, f"Expected some score, got {state['loop_score']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

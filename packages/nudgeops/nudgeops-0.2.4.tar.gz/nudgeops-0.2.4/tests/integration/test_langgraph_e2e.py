"""
tests/integration/test_langgraph_e2e.py

End-to-end tests with REAL LangGraph execution.

These tests actually:
1. Create a StateGraph
2. Add agent/tools/guard nodes
3. Compile and invoke the graph
4. Verify NudgeOps stops looping agents

Unlike test_langgraph.py which tests our code with fake state shapes,
this tests the full integration with real LangGraph execution.
"""

import pytest
from typing import TypedDict, Annotated, Sequence
from operator import add

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    END = None

# NudgeOps imports
from nudgeops.integrations.langgraph import (
    NudgeOpsNode,
    NudgeOpsState,
    add_guard_to_graph,
)


# Skip all tests if langgraph not installed
pytestmark = pytest.mark.skipif(
    not LANGGRAPH_AVAILABLE,
    reason="langgraph not installed"
)


# ---------------------------------------------------------------------------
# State Definition
# ---------------------------------------------------------------------------

class AgentState(TypedDict, total=False):
    """State for our test agents."""
    
    # Messages in the conversation
    messages: list[dict]
    
    # Tool calls requested by agent
    tool_calls: list[dict]
    
    # Results from tool execution
    tool_results: list[dict]
    
    # NudgeOps fields
    loop_score: float
    should_stop: bool
    stop_reason: str
    nudge_count: int
    state_payload: dict
    
    # Control fields
    step_count: int
    max_steps: int


# ---------------------------------------------------------------------------
# Mock Agents
# ---------------------------------------------------------------------------

class LoopingAgent:
    """
    Agent that always does the exact same thing.
    
    Will trigger Type I (Stutter) detection.
    """
    
    def __init__(self):
        self.call_count = 0
    
    def __call__(self, state: AgentState) -> AgentState:
        self.call_count += 1
        
        # Always request the same tool call
        return {
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": "I'll search for laptop"}
            ],
            "tool_calls": [
                {"tool_name": "search", "tool_args": {"query": "laptop"}}
            ],
            "step_count": state.get("step_count", 0) + 1,
        }


class ProgressingAgent:
    """
    Agent that makes progress each step.
    
    Should NOT trigger any detection.
    """
    
    def __init__(self, steps: list[dict]):
        """
        Args:
            steps: List of {tool_name, tool_args, thought} for each step
        """
        self.steps = steps
        self.current_step = 0
    
    def __call__(self, state: AgentState) -> AgentState:
        if self.current_step >= len(self.steps):
            # Signal completion
            return {
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": "Task complete!"}
                ],
                "tool_calls": [],  # No more tools to call
                "step_count": state.get("step_count", 0) + 1,
            }
        
        step = self.steps[self.current_step]
        self.current_step += 1
        
        return {
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": step.get("thought", "Doing next step")}
            ],
            "tool_calls": [
                {"tool_name": step["tool_name"], "tool_args": step["tool_args"]}
            ],
            "step_count": state.get("step_count", 0) + 1,
        }


class SemanticLoopingAgent:
    """
    Agent that uses synonyms (different words, same intent).
    
    Will trigger Type II (Insanity) detection.
    """
    
    def __init__(self):
        self.synonyms = [
            ("laptop", "I'll search for laptop"),
            ("notebook computer", "Let me try notebook computer"),
            ("portable pc", "Maybe portable pc will work"),
            ("laptop computer", "Searching for laptop computer"),
            ("notebook", "Trying notebook"),
        ]
        self.current = 0
    
    def __call__(self, state: AgentState) -> AgentState:
        query, thought = self.synonyms[self.current % len(self.synonyms)]
        self.current += 1
        
        return {
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": thought}
            ],
            "tool_calls": [
                {"tool_name": "search", "tool_args": {"query": query}}
            ],
            "step_count": state.get("step_count", 0) + 1,
        }


# ---------------------------------------------------------------------------
# Mock Tools
# ---------------------------------------------------------------------------

class MockToolExecutor:
    """
    Mock tool executor that returns canned responses.
    
    Tracks execution for assertions.
    """
    
    def __init__(self, responses: dict[str, str] | None = None):
        """
        Args:
            responses: Map of tool_name -> response. Defaults provided.
        """
        self.responses = responses or {
            "search": "Found 10 results",
            "select": "Selected item",
            "add_to_cart": "Added to cart",
        }
        self.executions: list[dict] = []
    
    def __call__(self, state: AgentState) -> AgentState:
        tool_calls = state.get("tool_calls", [])
        
        if not tool_calls:
            return state
        
        results = []
        for call in tool_calls:
            tool_name = call.get("tool_name", "unknown")
            tool_args = call.get("tool_args", {})
            
            # Record execution
            self.executions.append({"tool_name": tool_name, "tool_args": tool_args})
            
            # Generate response
            response = self.responses.get(tool_name, "OK")
            results.append({
                "tool_name": tool_name,
                "tool_args": tool_args,
                "content": response,
            })
        
        return {
            "tool_results": results,
            "tool_calls": [],  # Clear tool calls after execution
        }


# ---------------------------------------------------------------------------
# Graph Builders
# ---------------------------------------------------------------------------

def create_test_graph(
    agent_fn,
    tool_fn,
    max_steps: int = 20,
    nudge_threshold: float = 2.0,
    stop_threshold: float = 3.0,
):
    """
    Create a test graph with agent, tools, and guard.
    
    Flow: agent → tools → guard → agent (or END)
    """
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("agent", agent_fn)
    builder.add_node("tools", tool_fn)
    
    # Add guard
    guard = add_guard_to_graph(
        builder,
        after_node="tools",
        before_node="agent",
        nudge_threshold=nudge_threshold,
        stop_threshold=stop_threshold,
    )
    
    # Entry point
    builder.set_entry_point("agent")
    
    # Agent → Tools (if tool calls) or END (if no tool calls)
    def route_agent(state: AgentState) -> str:
        # Check step limit
        if state.get("step_count", 0) >= max_steps:
            return "end"
        
        # Check if agent requested tools
        if state.get("tool_calls"):
            return "tools"
        
        return "end"
    
    builder.add_conditional_edges(
        "agent",
        route_agent,
        {
            "tools": "tools",
            "end": END,
        }
    )
    
    return builder.compile(), guard


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestLoopingAgentGetsStopped:
    """Test that a looping agent triggers STOP."""
    
    def test_stutter_loop_stopped(self):
        """Agent repeating exact same action gets stopped."""
        agent = LoopingAgent()
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=20,
            stop_threshold=3.0,
        )
        
        # Run the graph
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Buy a laptop"}],
            "step_count": 0,
            "state_payload": {"cart": []},  # Static state to trigger phantom too
        })
        
        # Should have stopped due to loop detection
        assert result.get("should_stop", False), \
            f"Agent should have been stopped. Score: {result.get('loop_score')}"
        
        # Should have stopped before max steps
        assert result.get("step_count", 0) < 20, \
            f"Should stop early, but ran {result.get('step_count')} steps"
        
        # Score should be at stop threshold
        assert result.get("loop_score", 0) >= 3.0, \
            f"Score should be >= 3.0, got {result.get('loop_score')}"
        
        print(f"✓ Looping agent stopped after {result.get('step_count')} steps")
        print(f"  Score: {result.get('loop_score')}")
        print(f"  Reason: {result.get('stop_reason', 'N/A')}")


class TestHealthyAgentCompletes:
    """Test that a healthy agent is not interfered with."""
    
    def test_progressing_agent_completes(self):
        """Agent making progress completes normally."""
        agent = ProgressingAgent(steps=[
            {"tool_name": "search", "tool_args": {"query": "laptop"}, "thought": "Searching"},
            {"tool_name": "select", "tool_args": {"id": 1}, "thought": "Selecting item"},
            {"tool_name": "add_to_cart", "tool_args": {"id": 1}, "thought": "Adding to cart"},
        ])
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=20,
        )
        
        # Run the graph
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Buy a laptop"}],
            "step_count": 0,
        })
        
        # Should NOT have been stopped
        assert not result.get("should_stop", False), \
            f"Healthy agent should not be stopped. Score: {result.get('loop_score')}"
        
        # Should have completed all steps
        assert agent.current_step == len(agent.steps), \
            f"Should complete all steps. Completed: {agent.current_step}/{len(agent.steps)}"
        
        # Score should be low
        assert result.get("loop_score", 0) < 2.0, \
            f"Score should be < 2.0, got {result.get('loop_score')}"
        
        print(f"✓ Healthy agent completed {agent.current_step} steps")
        print(f"  Final score: {result.get('loop_score', 0)}")


class TestSemanticLoopDetected:
    """Test that semantic loops (synonyms) are detected."""
    
    def test_synonym_loop_increases_score(self):
        """Agent using synonyms triggers semantic detection."""
        agent = SemanticLoopingAgent()
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=10,
            stop_threshold=5.0,  # Higher threshold to see score build
        )
        
        # Run the graph
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Find a laptop"}],
            "step_count": 0,
            "state_payload": {"results": []},  # Static for phantom detection
        })
        
        # Score should have increased
        assert result.get("loop_score", 0) > 0, \
            f"Score should increase with semantic loops. Got: {result.get('loop_score')}"
        
        print(f"✓ Semantic loop detected")
        print(f"  Steps run: {result.get('step_count')}")
        print(f"  Final score: {result.get('loop_score')}")


class TestNudgeInjection:
    """Test that nudge messages are injected before STOP."""
    
    def test_nudge_message_appears(self):
        """System message with [NudgeOps] appears when nudged."""
        agent = LoopingAgent()
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=20,
            nudge_threshold=2.0,
            stop_threshold=4.0,  # Give room for nudges before stop
        )
        
        # Run the graph
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Buy a laptop"}],
            "step_count": 0,
            "state_payload": {"cart": []},
        })
        
        # Check for nudge messages
        messages = result.get("messages", [])
        nudge_messages = [
            m for m in messages 
            if m.get("role") == "system" and "[NudgeOps]" in m.get("content", "")
        ]
        
        # Should have at least one nudge before stop
        assert len(nudge_messages) > 0 or result.get("nudge_count", 0) > 0, \
            f"Should have nudge messages. Messages: {[m.get('content', '')[:50] for m in messages]}"
        
        print(f"✓ Nudge injection verified")
        print(f"  Nudge count: {result.get('nudge_count', 0)}")
        print(f"  Nudge messages found: {len(nudge_messages)}")


class TestGuardIntegration:
    """Test guard integration mechanics."""
    
    def test_guard_receives_tool_results(self):
        """Guard node sees tool results in state."""
        agent = LoopingAgent()
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=5,
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Test"}],
            "step_count": 0,
            "state_payload": {"test": True},
        })
        
        # Guard should have history
        assert len(guard.history) > 0, "Guard should have recorded steps"
        
        print(f"✓ Guard recorded {len(guard.history)} steps")
    
    def test_guard_reset_works(self):
        """Guard can be reset between runs."""
        agent = LoopingAgent()
        tools = MockToolExecutor()
        
        graph, guard = create_test_graph(
            agent_fn=agent,
            tool_fn=tools,
            max_steps=5,
        )
        
        # First run
        graph.invoke({
            "messages": [{"role": "user", "content": "Test 1"}],
            "step_count": 0,
            "state_payload": {},
        })
        
        history_after_first = len(guard.history)
        
        # Reset
        guard.reset()
        
        assert len(guard.history) == 0, "History should be empty after reset"
        assert guard.score == 0.0, "Score should be 0 after reset"
        
        print(f"✓ Guard reset works (had {history_after_first} steps, now 0)")


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

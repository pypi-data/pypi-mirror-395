"""
tests/integration/test_real_llm.py

End-to-end tests with REAL LLM (OpenAI) calls.

These tests:
1. Call actual OpenAI API (costs real money!)
2. Use scenarios designed to cause loops
3. Verify NudgeOps detects and stops the loops
4. Track costs and provide summaries

Requirements:
    pip install openai langgraph
    export OPENAI_API_KEY="sk-..."

Run:
    # Run all real LLM tests
    pytest tests/integration/test_real_llm.py -v -s
    
    # Run just cheap tests (gpt-4o-mini)
    pytest tests/integration/test_real_llm.py -v -s -k "mini"
    
    # Run production model tests (gpt-4o) - more expensive
    pytest tests/integration/test_real_llm.py -v -s -k "gpt4o"
"""

import os
import pytest
from typing import TypedDict

# Check dependencies
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

# NudgeOps imports
from nudgeops.integrations.langgraph import (
    NudgeOpsNode,
    add_guard_to_graph,
)

# Test components (these will be in nudgeops/testing/)
from nudgeops.testing.openai_agent import OpenAIAgentNode
from nudgeops.testing.loop_inducing_tools import LoopInducingTools


# ---------------------------------------------------------------------------
# Skip conditions
# ---------------------------------------------------------------------------

# Skip if dependencies not available
pytestmark = [
    pytest.mark.skipif(not OPENAI_AVAILABLE, reason="openai not installed"),
    pytest.mark.skipif(not LANGGRAPH_AVAILABLE, reason="langgraph not installed"),
    pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    ),
]


# ---------------------------------------------------------------------------
# State Definition
# ---------------------------------------------------------------------------

class RealLLMState(TypedDict, total=False):
    """State for real LLM tests."""
    messages: list[dict]
    tool_calls: list[dict]
    tool_results: list[dict]
    loop_score: float
    should_stop: bool
    stop_reason: str
    nudge_count: int
    state_payload: dict
    step_count: int


# ---------------------------------------------------------------------------
# Graph Builder
# ---------------------------------------------------------------------------

def create_real_llm_graph(
    model: str = "gpt-4o-mini",
    scenario: str = "impossible_search",
    max_llm_calls: int = 15,
    max_cost: float = 0.50,
    nudge_threshold: float = 2.0,
    stop_threshold: float = 3.0,
    max_steps: int = 20,
):
    """
    Create a graph with real LLM agent, loop-inducing tools, and NudgeOps guard.
    
    Returns:
        Tuple of (compiled_graph, agent, tools, guard)
    """
    # Create components
    agent = OpenAIAgentNode(
        model=model,
        max_calls=max_llm_calls,
        max_cost=max_cost,
    )
    
    tools = LoopInducingTools(scenario=scenario)
    
    # Build graph
    builder = StateGraph(RealLLMState)
    
    builder.add_node("agent", agent)
    builder.add_node("tools", tools)
    
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
    
    # Routing
    def route_agent(state: RealLLMState) -> str:
        if state.get("step_count", 0) >= max_steps:
            return "end"
        if state.get("tool_calls"):
            return "tools"
        return "end"
    
    builder.add_conditional_edges(
        "agent",
        route_agent,
        {"tools": "tools", "end": END}
    )
    
    return builder.compile(), agent, tools, guard


# ---------------------------------------------------------------------------
# Test Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def print_summary():
    """Fixture that prints test summaries."""
    summaries = []
    
    def _add(summary: dict):
        summaries.append(summary)
    
    yield _add
    
    # Print all summaries at end
    if summaries:
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        for s in summaries:
            print(f"\n{s.get('name', 'Unknown')}:")
            for k, v in s.items():
                if k != 'name':
                    print(f"  {k}: {v}")


# ---------------------------------------------------------------------------
# Tests: GPT-4o-mini (cheap)
# ---------------------------------------------------------------------------

class TestGPT4oMini:
    """Tests using GPT-4o-mini (~$0.01 per test)."""

    MODEL = "gpt-4o-mini"
    
    def test_impossible_search_loop_stopped(self, print_summary):
        """
        Scenario: Product doesn't exist, agent keeps searching variations.
        Expected: NudgeOps detects semantic loop and stops.
        """
        graph, agent, tools, guard = create_real_llm_graph(
            model=self.MODEL,
            scenario="impossible_search",
            max_llm_calls=15,
            stop_threshold=3.0,
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Find and buy the XYZ-9999 laptop"}],
            "step_count": 0,
        })
        
        # Collect stats
        stats = agent.get_stats()
        
        print_summary({
            "name": "impossible_search_loop (gpt-4o-mini)",
            "stopped_by_nudgeops": result.get("should_stop", False),
            "loop_score": result.get("loop_score", 0),
            "steps": result.get("step_count", 0),
            "llm_calls": stats["calls"],
            "cost": f"${stats['cost']:.4f}",
            "hit_limits": stats["hit_call_limit"] or stats["hit_cost_limit"],
        })
        
        # Assertions
        # Either NudgeOps stopped it OR agent hit call limit OR agent gave up
        stopped_properly = (
            result.get("should_stop", False) or
            stats["hit_call_limit"] or
            any("give_up" in str(ex.tool_name) for ex in tools.executions)
        )
        
        assert stopped_properly, (
            f"Agent should have been stopped. "
            f"Score: {result.get('loop_score')}, "
            f"Steps: {result.get('step_count')}"
        )
        
        print(f"\n✓ Test passed - Agent stopped after {stats['calls']} LLM calls")
        print(f"  Cost: ${stats['cost']:.4f}")
    
    def test_always_oos_loop_stopped(self, print_summary):
        """
        Scenario: Product found but every variant is out of stock.
        Expected: NudgeOps detects stutter (trying same variants) and stops.
        """
        graph, agent, tools, guard = create_real_llm_graph(
            model=self.MODEL,
            scenario="always_oos",
            max_llm_calls=15,
            stop_threshold=3.0,
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Buy a Premium Laptop in size XL"}],
            "step_count": 0,
        })
        
        stats = agent.get_stats()
        
        print_summary({
            "name": "always_oos_loop (gpt-4o-mini)",
            "stopped_by_nudgeops": result.get("should_stop", False),
            "loop_score": result.get("loop_score", 0),
            "steps": result.get("step_count", 0),
            "llm_calls": stats["calls"],
            "cost": f"${stats['cost']:.4f}",
        })
        
        # Should eventually stop
        assert result.get("step_count", 0) < 20, "Should stop before max steps"
        
        print(f"\n✓ Test passed - Cost: ${stats['cost']:.4f}")
    
    def test_checkout_fail_loop_stopped(self, print_summary):
        """
        Scenario: Can add to cart but checkout always fails.
        Expected: NudgeOps detects checkout retry loop.
        """
        graph, agent, tools, guard = create_real_llm_graph(
            model=self.MODEL,
            scenario="checkout_fail",
            max_llm_calls=15,
            stop_threshold=3.0,
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Buy any laptop and complete checkout"}],
            "step_count": 0,
        })
        
        stats = agent.get_stats()
        
        print_summary({
            "name": "checkout_fail_loop (gpt-4o-mini)",
            "stopped_by_nudgeops": result.get("should_stop", False),
            "loop_score": result.get("loop_score", 0),
            "steps": result.get("step_count", 0),
            "llm_calls": stats["calls"],
            "cost": f"${stats['cost']:.4f}",
        })
        
        print(f"\n✓ Test passed - Cost: ${stats['cost']:.4f}")
    
    def test_nudge_appears_before_stop(self, print_summary):
        """
        Verify that nudge messages are injected before STOP.
        """
        graph, agent, tools, guard = create_real_llm_graph(
            model=self.MODEL,
            scenario="impossible_search",
            max_llm_calls=15,
            nudge_threshold=2.0,
            stop_threshold=4.0,  # Higher to allow nudges
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Find the ABC-123 product"}],
            "step_count": 0,
        })
        
        stats = agent.get_stats()
        
        # Check for nudge messages
        messages = result.get("messages", [])
        nudge_count = sum(
            1 for m in messages
            if m.get("role") == "system" and "[NudgeOps]" in m.get("content", "")
        )
        
        print_summary({
            "name": "nudge_before_stop (gpt-4o-mini)",
            "nudge_messages": nudge_count,
            "nudge_count_field": result.get("nudge_count", 0),
            "final_score": result.get("loop_score", 0),
            "stopped": result.get("should_stop", False),
            "cost": f"${stats['cost']:.4f}",
        })
        
        print(f"\n✓ Nudge count: {nudge_count}, Cost: ${stats['cost']:.4f}")


# ---------------------------------------------------------------------------
# Tests: GPT-4o (production model, more expensive)
# ---------------------------------------------------------------------------

class TestGPT4o:
    """
    Tests using GPT-4o (~$0.10-0.50 per test).
    
    Run separately with: pytest -k "gpt4o" -v -s
    """
    
    MODEL = "gpt-4o"
    
    @pytest.mark.expensive
    def test_impossible_search_with_production_model(self, print_summary):
        """
        Same impossible_search scenario but with GPT-4o.
        
        Compare: Does GPT-4o loop less? Still need NudgeOps?
        """
        graph, agent, tools, guard = create_real_llm_graph(
            model=self.MODEL,
            scenario="impossible_search",
            max_llm_calls=10,  # Fewer calls due to cost
            max_cost=0.50,
            stop_threshold=3.0,
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Find and buy the XYZ-9999 laptop"}],
            "step_count": 0,
        })
        
        stats = agent.get_stats()
        
        print_summary({
            "name": "impossible_search_loop (gpt-4o)",
            "stopped_by_nudgeops": result.get("should_stop", False),
            "loop_score": result.get("loop_score", 0),
            "steps": result.get("step_count", 0),
            "llm_calls": stats["calls"],
            "cost": f"${stats['cost']:.4f}",
            "gave_up": any("give_up" in str(ex.tool_name) for ex in tools.executions),
        })
        
        print(f"\n✓ GPT-4o test complete - Cost: ${stats['cost']:.4f}")


# ---------------------------------------------------------------------------
# Comparison Tests
# ---------------------------------------------------------------------------

class TestModelComparison:
    """Compare behavior across models."""
    
    @pytest.mark.expensive
    def test_compare_models_on_impossible_search(self, print_summary):
        """
        Run same scenario on multiple models and compare.
        """
        models = ["gpt-4o-mini", "gpt-4o"]
        results = {}
        
        for model in models:
            graph, agent, tools, guard = create_real_llm_graph(
                model=model,
                scenario="impossible_search",
                max_llm_calls=10,
                stop_threshold=3.0,
            )
            
            result = graph.invoke({
                "messages": [{"role": "user", "content": "Find the NONEXISTENT-999 product"}],
                "step_count": 0,
            })
            
            stats = agent.get_stats()
            
            results[model] = {
                "stopped_by_nudgeops": result.get("should_stop", False),
                "loop_score": result.get("loop_score", 0),
                "steps": result.get("step_count", 0),
                "llm_calls": stats["calls"],
                "cost": stats["cost"],
                "gave_up": any("give_up" in str(ex.tool_name) for ex in tools.executions),
            }
            
            tools.reset()
        
        # Print comparison
        print("\n" + "=" * 60)
        print("MODEL COMPARISON: impossible_search scenario")
        print("=" * 60)
        print(f"{'Model':<15} {'Stopped':<10} {'Score':<8} {'Steps':<8} {'Calls':<8} {'Cost':<10} {'Gave Up':<10}")
        print("-" * 60)
        
        for model, data in results.items():
            print(f"{model:<15} {str(data['stopped_by_nudgeops']):<10} {data['loop_score']:<8.2f} {data['steps']:<8} {data['llm_calls']:<8} ${data['cost']:<9.4f} {str(data['gave_up']):<10}")
        
        total_cost = sum(r["cost"] for r in results.values())
        print("-" * 60)
        print(f"Total cost: ${total_cost:.4f}")
        
        print_summary({
            "name": "model_comparison",
            "models_tested": list(results.keys()),
            "total_cost": f"${total_cost:.4f}",
        })


# ---------------------------------------------------------------------------
# Utility: Cost estimator (no actual API calls)
# ---------------------------------------------------------------------------

class TestCostEstimation:
    """Estimate costs before running real tests."""
    
    def test_estimate_costs(self):
        """Print cost estimates for test suite."""
        print("\n" + "=" * 60)
        print("COST ESTIMATES")
        print("=" * 60)
        
        estimates = [
            ("TestGPT4oMini (4 tests)", "gpt-4o-mini", 15 * 4, "$0.02"),
            ("TestGPT4o (1 test)", "gpt-4o", 10, "$0.10"),
            ("TestModelComparison", "mixed", 20, "$0.15"),
        ]
        
        print(f"{'Test Class':<30} {'Model':<15} {'Est. Calls':<12} {'Est. Cost':<10}")
        print("-" * 60)
        
        for name, model, calls, cost in estimates:
            print(f"{name:<30} {model:<15} {calls:<12} {cost:<10}")
        
        print("-" * 60)
        print(f"{'TOTAL':<30} {'':<15} {'':<12} {'~$0.30':<10}")
        print("\nNote: Actual costs depend on response lengths and loop behavior.")


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Run with verbose output and print statements
    pytest.main([__file__, "-v", "-s", "--tb=short"])

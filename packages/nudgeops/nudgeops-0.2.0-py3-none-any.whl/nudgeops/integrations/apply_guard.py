"""
Helper function to inject NudgeOps guard into a LangGraph builder.

This is the recommended integration path - one line to add the guard.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from nudgeops.core.state import GuardConfig
from nudgeops.integrations.langgraph import NudgeOpsNode, add_guard_to_graph

if TYPE_CHECKING:
    from langgraph.graph import StateGraph


def apply_guard(
    builder: StateGraph,
    config: GuardConfig | None = None,
    after_node: str = "tools",
    next_node: str = "agent",
    guard_node_name: str = "guard",
) -> StateGraph:
    """
    Inject NudgeOps guard into an existing LangGraph builder.

    This is the recommended way to add NudgeOps to your graph.
    It adds the guard node and wires it into the graph flow.

    Before:
        tools → agent

    After:
        tools → guard → agent (or __end__ if stopped)

    Usage:
        builder = StateGraph(AgentState)
        builder.add_node("agent", agent_node)
        builder.add_node("tools", tool_node)
        builder.add_edge(START, "agent")
        builder.add_edge("agent", "tools")
        # Don't add edge from tools to agent!

        # One line to add guard
        apply_guard(builder)

        graph = builder.compile()

    Note:
        This function modifies the builder in place and returns it.

    Args:
        builder: LangGraph StateGraph builder
        config: Optional guard configuration
        after_node: Node after which to insert guard (default: "tools")
        next_node: Node to route to on continue (default: "agent")
        guard_node_name: Name for the guard node (default: "guard")

    Returns:
        The modified builder (for chaining)
    """
    # Extract thresholds from config if provided
    nudge_threshold = 2.0
    stop_threshold = 3.0
    if config:
        nudge_threshold = config.nudge_threshold
        stop_threshold = config.stop_threshold

    # Use add_guard_to_graph helper
    add_guard_to_graph(
        builder,
        after_node=after_node,
        before_node=next_node,
        guard_node_name=guard_node_name,
        nudge_threshold=nudge_threshold,
        stop_threshold=stop_threshold,
    )

    return builder


def create_guarded_graph(
    agent_node: callable,
    tool_node: callable,
    state_class: type,
    config: GuardConfig | None = None,
) -> StateGraph:
    """
    Create a new graph with guard already integrated.

    This is a convenience function for simple agent setups.

    Args:
        agent_node: The agent node function
        tool_node: The tool execution node function
        state_class: The state class (should include NudgeOps fields)
        config: Optional guard configuration

    Returns:
        StateGraph builder with guard integrated (call .compile() to use)
    """
    from langgraph.graph import StateGraph, START

    builder = StateGraph(state_class)

    # Add nodes
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)

    # Add edges
    builder.add_edge(START, "agent")
    builder.add_edge("agent", "tools")

    # Apply guard (this adds guard node and edges)
    apply_guard(builder, config=config)

    return builder

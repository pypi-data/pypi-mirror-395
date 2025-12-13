"""
Basic usage example for NudgeOps.

Shows the minimal integration with a LangGraph agent.

Requirements:
    pip install nudgeops langchain-openai

Usage:
    export OPENAI_API_KEY=your-key
    python basic_usage.py
"""

from __future__ import annotations

import os
from typing import Annotated

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from nudgeops import apply_guard, GuardConfig
from nudgeops.core.state import AgentState


# Define a simple tool
@tool
def search(query: str) -> str:
    """Search for information."""
    # Simulated search - in reality would call an API
    if "policy" in query.lower():
        return "No results found for your query."
    return f"Found results for: {query}"


# Create the agent
def create_agent():
    """Create a simple agent with NudgeOps guard."""

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([search])

    def agent_node(state: AgentState):
        """Call the LLM."""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        """Check if we should continue to tools."""
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END

    # Build graph
    builder = StateGraph(AgentState)

    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode([search]))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue, ["tools", END])

    # Apply NudgeOps guard after tools
    config = GuardConfig(
        nudge_threshold=2.0,
        stop_threshold=3.0,
    )
    apply_guard(builder, config=config)

    return builder.compile()


def main():
    """Run the example."""
    print("=" * 60)
    print("NudgeOps Basic Usage Example")
    print("=" * 60)
    print()

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Note: OPENAI_API_KEY not set.")
        print("This example requires an OpenAI API key.")
        print("Set it with: export OPENAI_API_KEY=your-key")
        print()
        print("Showing graph structure instead...")
        print()

        # Show what the graph would look like
        print("Graph nodes that would be created:")
        print("  1. agent - Calls the LLM")
        print("  2. tools - Executes tool calls")
        print("  3. trajectory_guard - NudgeOps guard node")
        print()
        print("Flow: START -> agent -> tools -> trajectory_guard -> agent (loop)")
        print("      trajectory_guard can route to END if agent is stuck")
        return

    # Create agent with guard
    graph = create_agent()

    print("Graph created with NudgeOps guard integrated.")
    print()

    # Run a query
    print("Running query: 'Find the return policy'")
    print("-" * 40)

    result = graph.invoke({
        "messages": [
            SystemMessage(content="You are a helpful assistant. Use tools to find information."),
            HumanMessage(content="Find the return policy"),
        ],
    })

    # Show results
    print()
    print("Result:")
    print("-" * 40)

    # Show loop status if available
    loop_status = result.get("loop_status", {})
    if loop_status:
        print(f"Loop Score: {loop_status.get('loop_score', 0):.2f}")
        print(f"Nudges Sent: {loop_status.get('nudges_sent', 0)}")
        print(f"Steps Taken: {loop_status.get('step_count', 0)}")
        print(f"Last Intervention: {loop_status.get('last_intervention', 'None')}")

    # Show final message
    messages = result.get("messages", [])
    if messages:
        last_msg = messages[-1]
        print()
        print("Final response:")
        print(last_msg.content[:500] if hasattr(last_msg, 'content') else str(last_msg))


if __name__ == "__main__":
    main()

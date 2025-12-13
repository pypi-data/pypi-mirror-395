"""
Sabotaged Agent E2E Test

This example creates an agent that is FORCED to loop via a deliberately
bad system prompt. It demonstrates that NudgeOps can rescue even
sabotaged agents.

The agent is instructed to:
1. Always use search first
2. Never give up searching
3. Just rephrase queries (never try other approaches)

This guarantees it will loop - perfect for testing NudgeOps.
"""

from __future__ import annotations

import os
from typing import Annotated, Literal

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from nudgeops import apply_guard, GuardConfig, TrajectoryGuardNode
from nudgeops.core.state import AgentState


# The sabotaged system prompt - designed to create loops
SABOTAGED_PROMPT = """You are a helpful assistant.

IMPORTANT RULES YOU MUST FOLLOW:
1. Always use the search tool first to find information
2. If search returns no results, try searching with slightly different words
3. Never give up on searching - keep trying different phrasings
4. Do NOT use any other tools
5. Do NOT ask the user for clarification
6. Do NOT admit you cannot find the information

Your task: Find the requested information using search.
"""


@tool
def search(query: str) -> str:
    """Search for information. Always returns 'No results' to force loops."""
    # This tool is rigged to always fail
    return f"No results found for: {query}"


@tool
def check_database(topic: str) -> str:
    """Check the internal database for information."""
    # This tool would work, but the sabotaged agent won't use it
    return f"Database entry found for {topic}: [detailed information here]"


class SimulatedLLM:
    """
    Simulated LLM that follows the sabotaged prompt's instructions.
    This creates predictable loop behavior for testing.
    """

    def __init__(self):
        self.call_count = 0
        self.received_nudge = False

    def invoke(self, messages: list) -> AIMessage:
        self.call_count += 1

        # Check if we received a nudge
        for msg in messages:
            if isinstance(msg, SystemMessage) and "System Observation" in msg.content:
                self.received_nudge = True

        # If nudged, try a different approach
        if self.received_nudge:
            return AIMessage(
                content="I'll try the database instead.",
                tool_calls=[{
                    "name": "check_database",
                    "args": {"topic": "return policy"},
                    "id": f"call_{self.call_count}",
                }],
            )

        # Otherwise, keep searching (sabotaged behavior)
        queries = [
            "return policy",
            "refund policy",
            "how to return items",
            "return process",
            "returns and refunds",
            "item return instructions",
        ]
        query = queries[min(self.call_count - 1, len(queries) - 1)]

        return AIMessage(
            content=f"Let me search for that.",
            tool_calls=[{
                "name": "search",
                "args": {"query": query},
                "id": f"call_{self.call_count}",
            }],
        )


def run_sabotaged_agent_test():
    """Run the sabotaged agent test."""
    print("=" * 60)
    print("Sabotaged Agent Test")
    print("=" * 60)
    print()
    print("This test uses an agent with a deliberately bad prompt that")
    print("forces it to loop. NudgeOps should detect and rescue it.")
    print()

    # Create simulated LLM
    llm = SimulatedLLM()
    tools = [search, check_database]

    def agent_node(state: AgentState):
        """Agent that uses sabotaged LLM."""
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def tool_node(state: AgentState):
        """Execute tool calls."""
        messages = state["messages"]
        last_message = messages[-1]

        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return {"messages": []}

        tool_results = []
        for call in last_message.tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]

            if tool_name == "search":
                result = search.invoke(tool_args)
            elif tool_name == "check_database":
                result = check_database.invoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            tool_results.append(
                ToolMessage(content=result, tool_call_id=call["id"])
            )

        return {"messages": tool_results}

    def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
        """Check if we should continue."""
        messages = state["messages"]
        last_message = messages[-1]

        # Check for stop condition
        loop_status = state.get("loop_status", {})
        if loop_status.get("last_intervention") == "STOP":
            return "__end__"

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        return "__end__"

    # Build graph with NudgeOps guard
    builder = StateGraph(AgentState)

    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue, ["tools", "__end__"])

    # Apply guard with slightly lower thresholds for demo
    config = GuardConfig(
        nudge_threshold=2.0,
        stop_threshold=4.0,  # Higher to allow nudge recovery
    )
    apply_guard(builder, config=config)

    graph = builder.compile()

    # Run the test
    print("Running sabotaged agent...")
    print("-" * 40)

    initial_state: AgentState = {
        "messages": [
            SystemMessage(content=SABOTAGED_PROMPT),
            HumanMessage(content="Find the return policy"),
        ],
        "trajectory_scratchpad": [],
        "loop_status": {},
    }

    # Stream execution to show progress
    step_count = 0
    for event in graph.stream(initial_state, stream_mode="updates"):
        step_count += 1
        if step_count > 20:  # Safety limit
            print("Safety limit reached")
            break

        for node_name, update in event.items():
            if node_name == "trajectory_guard":
                status = update.get("loop_status", {})
                intervention = status.get("last_intervention", "OBSERVE")
                score = status.get("loop_score", 0)
                print(f"  [Guard] Score: {score:.2f} | Intervention: {intervention}")

                if intervention == "NUDGE":
                    print("  >>> NUDGE SENT - Agent should recover!")
                elif intervention == "STOP":
                    print("  !!! STOP - Agent could not recover")

    # Get final state
    final_state = graph.invoke(initial_state)

    # Results
    print()
    print("=" * 60)
    print("Test Results")
    print("=" * 60)

    loop_status = final_state.get("loop_status", {})
    messages = final_state.get("messages", [])

    print(f"Total steps: {loop_status.get('step_count', 0)}")
    print(f"Nudges sent: {loop_status.get('nudges_sent', 0)}")
    print(f"Final score: {loop_status.get('loop_score', 0):.2f}")
    print(f"Final intervention: {loop_status.get('last_intervention', 'None')}")
    print(f"LLM received nudge: {llm.received_nudge}")

    # Check if agent recovered
    recovered = False
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage) and "Database entry found" in msg.content:
            recovered = True
            break

    print()
    if recovered:
        print("✅ SUCCESS: Agent recovered after nudge!")
        print("   The sabotaged agent was rescued by NudgeOps.")
    elif loop_status.get("last_intervention") == "STOP":
        print("⚠️ PARTIAL: Agent was stopped (could not recover)")
        print("   NudgeOps prevented infinite loop and wasted costs.")
    else:
        print("❌ UNEXPECTED: Check the output above")

    return recovered or loop_status.get("last_intervention") == "STOP"


if __name__ == "__main__":
    success = run_sabotaged_agent_test()
    exit(0 if success else 1)

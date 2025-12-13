"""
nudgeops/integrations/langgraph.py

LangGraph integration for NudgeOps loop detection.

This module provides:
1. NudgeOpsNode - A LangGraph node that runs loop detection after each tool execution
2. add_guard_to_graph() - Helper to add guard to existing graphs
3. State extraction utilities

Usage:
    from nudgeops.integrations.langgraph import NudgeOpsNode, add_guard_to_graph

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_fn)
    builder.add_node("tools", tool_fn)
    builder.add_edge("agent", "tools")

    # Add NudgeOps guard
    add_guard_to_graph(builder, after_node="tools", before_node="agent")

    graph = builder.compile()
"""

from __future__ import annotations

import hashlib
import math
from typing import Any, Callable, TypedDict

from nudgeops.core.state import StepRecord, create_step_record
from nudgeops.embedding.utils import compute_hash
from nudgeops.integrations.universal_guard import UniversalGuard, GuardDecision


# ---------------------------------------------------------------------------
# State Types
# ---------------------------------------------------------------------------

class NudgeOpsState(TypedDict, total=False):
    """Extended LangGraph state with NudgeOps fields."""

    # Standard LangGraph fields
    messages: list[dict]
    tool_calls: list[dict]
    tool_results: list[dict]

    # NudgeOps fields
    loop_score: float
    should_stop: bool
    stop_reason: str
    nudge_count: int

    # For state hashing (optional - user can provide custom)
    state_payload: dict


# ---------------------------------------------------------------------------
# Semantic Groups for Fake Embeddings
# ---------------------------------------------------------------------------

SEMANTIC_GROUPS = {
    # Shopping synonyms
    "laptop": "device_laptop",
    "notebook": "device_laptop",
    "notebook computer": "device_laptop",
    "portable computer": "device_laptop",
    "portable pc": "device_laptop",
    # Size variants
    "xl": "size_xl",
    "x-large": "size_xl",
    "extra large": "size_xl",
    "extra-large": "size_xl",
    # Code actions
    "fix bug": "action_fix",
    "fix the bug": "action_fix",
    "repair": "action_fix",
    "patch": "action_fix",
    "run tests": "action_test",
    "run the tests": "action_test",
    "execute tests": "action_test",
    "test": "action_test",
    # Add to cart
    "add to cart": "action_cart",
    "adding to cart": "action_cart",
    "put in cart": "action_cart",
}


# ---------------------------------------------------------------------------
# Embedding Functions
# ---------------------------------------------------------------------------

def _fake_embed(text: str, dim: int = 384) -> list[float]:
    """
    Generate deterministic fake embedding for testing.

    Maps semantically similar terms to identical vectors.
    Different terms get different (but consistent) vectors.

    Args:
        text: Text to embed
        dim: Embedding dimension (default 384 for BAAI/bge-small-en-v1.5)

    Returns:
        Normalized embedding vector
    """
    text_lower = text.lower().strip()

    # Check for semantic group match
    group_key = None
    for phrase, group in SEMANTIC_GROUPS.items():
        if phrase in text_lower:
            group_key = group
            break

    # Use group key if matched, else use original text
    hash_input = group_key if group_key else text_lower

    # Generate embedding from hash
    hash_bytes = hashlib.sha256(hash_input.encode()).digest()
    embedding = []
    for i in range(dim):
        byte_idx = i % 32
        embedding.append((hash_bytes[byte_idx] + i) % 256 / 255.0 - 0.5)

    # Normalize to unit vector
    norm = math.sqrt(sum(x * x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]

    return embedding


# ---------------------------------------------------------------------------
# State Extraction
# ---------------------------------------------------------------------------

def extract_step_from_langgraph_state(
    state: NudgeOpsState,
    agent_id: str | None = None,
    embed_fn: Callable[[str], list[float]] | None = None,
) -> StepRecord | None:
    """
    Extract a StepRecord from LangGraph state.

    Returns None if no tool was executed (agent-only turn).

    Args:
        state: Current LangGraph state
        agent_id: Optional agent identifier for multi-agent graphs
        embed_fn: Optional embedding function. If None, uses fake embeddings.

    Returns:
        StepRecord if a tool was executed, None otherwise
    """
    tool_results = state.get("tool_results", [])
    if not tool_results:
        return None

    # Get the last tool execution
    last_result = tool_results[-1]
    tool_name = last_result.get("tool_name", "unknown")
    tool_args = last_result.get("tool_args", {})
    result_content = last_result.get("content", "")

    # Get the thought/reasoning that led to this tool call
    messages = state.get("messages", [])
    thought = ""
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if isinstance(content, str):
                thought = content
            break

    # Compute tool args hash
    tool_args_hash = compute_hash(tool_args if tool_args else {})

    # State hash - use provided payload or derive from observable state
    state_payload = state.get("state_payload")
    if state_payload is None:
        # Default: hash based on message count and last result
        state_payload = {
            "messages_count": len(messages),
            "tool_results_count": len(tool_results),
            "last_result_preview": str(result_content)[:100],
        }
    state_hash = compute_hash(state_payload)

    # Determine outcome type from result
    result_str = str(result_content).lower()
    if "error" in result_str or "failed" in result_str or "exception" in result_str:
        outcome_type = "error"
    elif not result_content or result_content in ("", "null", "None", None):
        outcome_type = "empty"
    else:
        outcome_type = "success"

    # Compute embedding
    if embed_fn is not None:
        thought_embedding = embed_fn(thought)
    else:
        thought_embedding = _fake_embed(thought)

    return create_step_record(
        tool_name=tool_name,
        tool_args_hash=tool_args_hash,
        thought_embedding=thought_embedding,
        state_snapshot_hash=state_hash,
        agent_id=agent_id,
        outcome_type=outcome_type,
        raw_tool_args=tool_args,
    )


# ---------------------------------------------------------------------------
# Guard Node
# ---------------------------------------------------------------------------

class NudgeOpsNode:
    """
    LangGraph node that runs NudgeOps loop detection.

    Add this node after tool execution to monitor for loops.

    Example:
        guard = NudgeOpsNode()
        builder.add_node("guard", guard)
        builder.add_edge("tools", "guard")
        builder.add_conditional_edges("guard", guard.should_continue)

    Attributes:
        guard: The underlying UniversalGuard instance
        embed_fn: Embedding function (or None for fake embeddings)
        agent_id: Optional agent identifier for multi-agent graphs
    """

    def __init__(
        self,
        nudge_threshold: float = 2.0,
        stop_threshold: float = 3.0,
        embed_fn: Callable[[str], list[float]] | None = None,
        agent_id: str | None = None,
    ):
        """
        Initialize the guard node.

        Args:
            nudge_threshold: Score at which to inject nudge (default 2.0)
            stop_threshold: Score at which to stop agent (default 3.0)
            embed_fn: Custom embedding function. If None, uses fake embeddings.
            agent_id: Agent identifier for multi-agent graphs
        """
        self.guard = UniversalGuard(
            nudge_threshold=nudge_threshold,
            stop_threshold=stop_threshold,
        )
        self.embed_fn = embed_fn
        self.agent_id = agent_id

    def __call__(self, state: NudgeOpsState) -> NudgeOpsState:
        """
        Process state and apply loop detection.

        This is called by LangGraph when the node executes.

        Args:
            state: Current graph state

        Returns:
            Updated state with loop_score and possibly nudge/stop applied
        """
        # Extract step from state
        step = extract_step_from_langgraph_state(state, self.agent_id, self.embed_fn)

        if step is None:
            # No tool execution this turn, nothing to check
            return state

        # Run detection
        decision = self.guard.on_step(step)

        # Build new state with updates
        new_state = dict(state)
        new_state["loop_score"] = decision.score

        if decision.action == "STOP":
            new_state["should_stop"] = True
            new_state["stop_reason"] = decision.message or "Loop detected"

        elif decision.action == "NUDGE":
            # Inject nudge as system message
            messages = list(state.get("messages", []))
            messages.append({
                "role": "system",
                "content": f"[NudgeOps] {decision.message}",
            })
            new_state["messages"] = messages
            new_state["nudge_count"] = state.get("nudge_count", 0) + 1

        return new_state

    def should_continue(self, state: NudgeOpsState) -> str:
        """
        Conditional edge function for LangGraph.

        Use with add_conditional_edges to route based on stop decision.

        Args:
            state: Current graph state

        Returns:
            "end" if should_stop is True, "continue" otherwise
        """
        if state.get("should_stop", False):
            return "end"
        return "continue"

    def reset(self):
        """Reset guard state for new conversation."""
        self.guard.reset()

    @property
    def score(self) -> float:
        """Current loop score."""
        return self.guard.score

    @property
    def history(self) -> list[StepRecord]:
        """Step history."""
        return self.guard.history


# ---------------------------------------------------------------------------
# Graph Builder Helpers
# ---------------------------------------------------------------------------

def add_guard_to_graph(
    builder,  # StateGraph - not typed to avoid import dependency
    after_node: str = "tools",
    before_node: str = "agent",
    guard_node_name: str = "guard",
    end_node: str = "__end__",
    **guard_kwargs,
):
    """
    Add NudgeOps guard to an existing graph builder.

    This inserts a guard node between tool execution and agent.

    Note: This modifies the builder in place AND returns the guard.

    Args:
        builder: LangGraph StateGraph builder
        after_node: Node after which to insert guard (usually "tools")
        before_node: Node to continue to after guard (usually "agent")
        guard_node_name: Name for the guard node
        end_node: Name of the end node (default "__end__" for LangGraph)
        **guard_kwargs: Arguments passed to NudgeOpsNode

    Returns:
        The guard node instance (builder is modified in place)

    Example:
        builder = StateGraph(AgentState)
        builder.add_node("agent", agent_fn)
        builder.add_node("tools", tool_fn)
        # Don't add edge from tools to agent yet!

        guard = add_guard_to_graph(builder, after_node="tools", before_node="agent")

        # Now flow is: agent → tools → guard → agent (or end if stopped)
    """
    guard = NudgeOpsNode(**guard_kwargs)

    # Add guard node
    builder.add_node(guard_node_name, guard)

    # Wire: after_node → guard
    builder.add_edge(after_node, guard_node_name)

    # Wire: guard → (continue to before_node OR end)
    builder.add_conditional_edges(
        guard_node_name,
        guard.should_continue,
        {
            "continue": before_node,
            "end": end_node,
        }
    )

    return guard

"""
State extractors for NudgeOps.

Extracts step information from LangGraph state for loop detection.
Handles various message types and tool call formats.
"""

from __future__ import annotations

import logging
from typing import Any, Literal

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from nudgeops.core.state import StepRecord, create_step_record
from nudgeops.embedding.utils import compute_hash, format_step_descriptor

logger = logging.getLogger(__name__)


def extract_tool_info(message: BaseMessage) -> tuple[str, dict[str, Any]] | None:
    """
    Extract tool name and arguments from a message.

    Handles:
    - AIMessage with tool_calls
    - ToolMessage responses

    Args:
        message: LangChain message

    Returns:
        Tuple of (tool_name, tool_args) or None if no tool call
    """
    if isinstance(message, AIMessage):
        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls and len(tool_calls) > 0:
            call = tool_calls[0]  # Take first tool call
            return call.get("name", "unknown"), call.get("args", {})

    return None


def classify_outcome(message: BaseMessage | None) -> Literal["success", "empty", "error"]:
    """
    Classify the outcome of a tool call based on the result.

    Args:
        message: ToolMessage or other response

    Returns:
        Outcome classification
    """
    if message is None:
        return "empty"

    if isinstance(message, ToolMessage):
        content = str(message.content).lower()

        # Check for error indicators
        error_indicators = ["error", "exception", "failed", "failure", "not found", "404", "500"]
        if any(indicator in content for indicator in error_indicators):
            return "error"

        # Check for empty indicators
        empty_indicators = ["no results", "empty", "none", "null", "[]", "{}"]
        if any(indicator in content for indicator in empty_indicators) or not content.strip():
            return "empty"

        return "success"

    return "success"


def compute_state_hash(state: dict[str, Any]) -> str:
    """
    Compute a hash of the relevant state for Type III detection.

    For tool-calling agents, this hashes the last tool result.
    For browser agents (future), this would hash the DOM state.

    Args:
        state: Current LangGraph state

    Returns:
        Hash string representing current state
    """
    messages = state.get("messages", [])

    # Find the last ToolMessage
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            return compute_hash(str(msg.content))

    # Fallback to empty hash if no tool messages
    return compute_hash("")


def extract_step_from_state(
    state: dict[str, Any],
    embedding_service: Any | None = None,
    agent_id: str | None = None,
) -> StepRecord | None:
    """
    Extract a StepRecord from the current LangGraph state.

    This is the main extraction function used by TrajectoryGuardNode.
    It analyzes the most recent messages to build a step record.

    Args:
        state: Current LangGraph state with messages
        embedding_service: Optional embedding service for Type II detection
        agent_id: Optional agent identifier for Type IV detection

    Returns:
        StepRecord if a tool call was found, None otherwise
    """
    messages = state.get("messages", [])

    if not messages:
        return None

    # Find the last AIMessage with tool calls
    last_ai_message: AIMessage | None = None
    last_tool_message: ToolMessage | None = None

    for msg in reversed(messages):
        if isinstance(msg, ToolMessage) and last_tool_message is None:
            last_tool_message = msg
        elif isinstance(msg, AIMessage) and last_ai_message is None:
            if getattr(msg, "tool_calls", None):
                last_ai_message = msg
                break

    # No tool call found
    if last_ai_message is None:
        return None

    # Extract tool info
    tool_info = extract_tool_info(last_ai_message)
    if tool_info is None:
        return None

    tool_name, tool_args = tool_info

    # Compute hashes
    args_hash = compute_hash(tool_args)
    state_hash = compute_state_hash(state)

    # Classify outcome
    outcome = classify_outcome(last_tool_message)

    # Generate embedding for Type II detection
    thought_embedding: list[float] = []
    if embedding_service is not None:
        try:
            descriptor = format_step_descriptor(tool_name, tool_args, outcome)
            embedding = embedding_service.embed(descriptor)
            thought_embedding = embedding.tolist()
        except Exception as e:
            logger.warning(f"Failed to generate embedding: {e}")

    return create_step_record(
        tool_name=tool_name,
        tool_args_hash=args_hash,
        thought_embedding=thought_embedding,
        state_snapshot_hash=state_hash,
        agent_id=agent_id,
        outcome_type=outcome,
        raw_tool_args=tool_args,
    )


def get_recent_tool_calls(state: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    """
    Get recent tool calls from state for debugging/logging.

    Args:
        state: LangGraph state
        limit: Maximum number of calls to return

    Returns:
        List of tool call info dicts
    """
    messages = state.get("messages", [])
    calls = []

    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for call in msg.tool_calls:
                calls.append({
                    "name": call.get("name"),
                    "args": call.get("args"),
                    "id": call.get("id"),
                })
                if len(calls) >= limit:
                    return calls

    return calls

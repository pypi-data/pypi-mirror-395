"""
State definitions for NudgeOps loop detection.

Defines the core data structures used throughout the system:
- StepRecord: Captures all information about a single agent step
- DetectionResult: Output from a detector
- LoopStatus: Current health/loop status of the agent
- AgentState: Full LangGraph state with trajectory tracking
- GuardConfig: Configuration for the guard node
"""

from __future__ import annotations

import operator
import uuid
from dataclasses import dataclass, field
from typing import Annotated, Any, Literal, TypedDict

from langgraph.graph.message import add_messages


class StepRecord(TypedDict, total=False):
    """
    Captures all information about a single agent step for loop detection.

    This is the core data structure that detectors analyze. Each field
    serves a specific detection type:

    - tool_name + tool_args_hash: Type I (Stutter) detection
    - thought_embedding: Type II (Insanity) detection
    - state_snapshot_hash: Type III (Phantom Progress) detection
    - agent_id: Type IV (Ping-Pong) detection
    """

    # Unique identifier for this step
    step_id: str

    # Tool information (Type I & IV)
    tool_name: str
    tool_args_hash: str  # SHA-256 of normalized JSON args

    # Semantic embedding (Type II)
    thought_embedding: list[float]  # 384 floats from BGE-small

    # State tracking (Type III)
    state_snapshot_hash: str  # Hash of relevant state after action

    # Multi-agent tracking (Type IV)
    agent_id: str | None

    # Outcome classification
    outcome_type: Literal["success", "empty", "error"]

    # Metadata
    timestamp: float
    raw_tool_args: dict[str, Any] | None  # Original args for debugging


class DetectionResult(TypedDict):
    """
    Output from a detector indicating whether a loop was detected.
    """

    detected: bool
    confidence: float  # 0.0 to 1.0
    loop_type: Literal["TYPE_I_STUTTER", "TYPE_II_INSANITY", "TYPE_III_PHANTOM", "TYPE_IV_PINGPONG"]
    details: dict[str, Any]  # Detector-specific details


class LoopStatus(TypedDict, total=False):
    """
    Current loop detection status for the agent session.
    """

    loop_score: float
    loop_type: str | None
    nudges_sent: int
    last_intervention: Literal["OBSERVE", "NUDGE", "STOP"] | None
    step_count: int


@dataclass
class GuardConfig:
    """
    Configuration for the TrajectoryGuard node.

    Attributes:
        nudge_threshold: Score at which to inject nudge message (default: 2.0)
        stop_threshold: Score at which to terminate execution (default: 3.0)
        decay_rate: Score decay multiplier when no loop detected (default: 0.5)
        max_score: Maximum loop score cap (default: 5.0)
        history_size: Number of steps to keep in history (default: 10)
        embedding_model: Name of the embedding model to use
        similarity_threshold: Cosine similarity threshold for Type II (default: 0.85)
        stutter_threshold: Hash similarity for Type I (default: 0.99)
        enable_langfuse: Whether to enable Langfuse observability
    """

    nudge_threshold: float = 2.0
    stop_threshold: float = 3.0
    decay_rate: float = 0.5
    max_score: float = 5.0
    history_size: int = 10
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    similarity_threshold: float = 0.85
    stutter_threshold: float = 0.99
    enable_langfuse: bool = False


def _replace_reducer(existing: dict | None, new: dict) -> dict:
    """Reducer that replaces the existing value entirely."""
    return new


class AgentState(TypedDict, total=False):
    """
    LangGraph state that includes trajectory tracking for loop detection.

    This extends a standard agent state with:
    - trajectory_scratchpad: Internal history for the guard (not sent to LLM)
    - loop_status: Current health metrics

    The reducers ensure proper state accumulation:
    - messages: Appended via add_messages
    - trajectory_scratchpad: Appended via operator.add
    - loop_status: Replaced entirely
    """

    # Standard LangGraph message history
    messages: Annotated[list, add_messages]

    # Guard's internal memory (does NOT go to LLM context)
    trajectory_scratchpad: Annotated[list[StepRecord], operator.add]

    # Current health status
    loop_status: Annotated[LoopStatus, _replace_reducer]


def create_step_record(
    tool_name: str,
    tool_args_hash: str,
    thought_embedding: list[float] | None = None,
    state_snapshot_hash: str = "",
    agent_id: str | None = None,
    outcome_type: Literal["success", "empty", "error"] = "success",
    raw_tool_args: dict[str, Any] | None = None,
    timestamp: float | None = None,
) -> StepRecord:
    """
    Factory function to create a StepRecord with defaults.
    """
    import time

    return StepRecord(
        step_id=str(uuid.uuid4()),
        tool_name=tool_name,
        tool_args_hash=tool_args_hash,
        thought_embedding=thought_embedding or [],
        state_snapshot_hash=state_snapshot_hash,
        agent_id=agent_id,
        outcome_type=outcome_type,
        raw_tool_args=raw_tool_args,
        timestamp=timestamp or time.time(),
    )


def create_initial_loop_status() -> LoopStatus:
    """
    Create initial loop status for a new session.
    """
    return LoopStatus(
        loop_score=0.0,
        loop_type=None,
        nudges_sent=0,
        last_intervention=None,
        step_count=0,
    )

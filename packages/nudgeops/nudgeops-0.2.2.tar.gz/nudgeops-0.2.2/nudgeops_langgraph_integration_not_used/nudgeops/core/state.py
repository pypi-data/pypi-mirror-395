"""
nudgeops/core/state.py

Core state types for NudgeOps loop detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StepRecord:
    """
    Universal record of a single agent step.
    
    This is the core data structure that detectors analyze.
    It's domain-agnostic - works for code agents, shopping agents, etc.
    
    Attributes:
        tool_name: Name of the tool/action (e.g., "edit_file", "add_to_cart")
        tool_args_hash: Hash of the tool arguments (for stutter detection)
        thought_embedding: Embedding vector of the agent's reasoning (for semantic detection)
        state_snapshot_hash: Hash of relevant state (for phantom progress detection)
        agent_id: Optional agent identifier (for multi-agent ping-pong detection)
        outcome_type: Result type: "success", "error", or "empty"
        metadata: Optional additional context
    """
    tool_name: str
    tool_args_hash: str
    thought_embedding: list[float]
    state_snapshot_hash: str
    agent_id: str | None = None
    outcome_type: str = "success"  # "success", "error", "empty"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectionResult:
    """
    Result from a single detector.
    
    Attributes:
        detected: Whether the pattern was detected
        detection_type: Type of detection (e.g., "stutter", "insanity", "phantom", "pingpong")
        confidence: Confidence score 0.0-1.0
        message: Human-readable description of what was detected
        details: Additional structured details
    """
    detected: bool
    detection_type: str
    confidence: float = 1.0
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

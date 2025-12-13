"""
nudgeops/integrations/universal_guard.py

Framework-agnostic guard for loop detection.

Usage:
    guard = UniversalGuard()
    
    for step in agent_steps:
        decision = guard.on_step(step)
        
        if decision.action == "STOP":
            terminate_agent(decision.message)
        elif decision.action == "NUDGE":
            inject_message(decision.message)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from nudgeops.core.state import StepRecord, DetectionResult
from nudgeops.core.detectors import (
    StutterDetector,
    InsanityDetector,
    PhantomProgressDetector,
    PingPongDetector,
)


# Score weights for each detection type
SCORE_WEIGHTS = {
    "stutter": 2.0,    # Type I: Exact repetition
    "insanity": 1.5,   # Type II: Semantic repetition
    "phantom": 0.5,    # Type III: No state change
    "pingpong": 1.5,   # Type IV: Multi-agent handoff
}

# Score decay factor when no detection
DECAY_FACTOR = 0.5


@dataclass
class GuardDecision:
    """
    Decision from the guard after analyzing a step.
    
    Attributes:
        action: What to do - "OBSERVE", "NUDGE", or "STOP"
        score: Current cumulative loop score
        message: Human-readable guidance (especially for NUDGE/STOP)
        detections: List of detection types that triggered
    """
    action: Literal["OBSERVE", "NUDGE", "STOP"]
    score: float
    message: str = ""
    detections: list[str] = field(default_factory=list)


class UniversalGuard:
    """
    Framework-agnostic loop detection guard.
    
    Accumulates detection scores across steps and makes
    OBSERVE/NUDGE/STOP decisions based on thresholds.
    
    Score mechanics:
        - Each detection adds weighted score
        - No detection = score * DECAY_FACTOR
        - score >= nudge_threshold = NUDGE
        - score >= stop_threshold = STOP
    
    Example:
        guard = UniversalGuard()
        
        for step in agent_steps:
            decision = guard.on_step(step)
            
            if decision.action == "STOP":
                break
            elif decision.action == "NUDGE":
                agent.inject_system_message(decision.message)
    """
    
    def __init__(
        self,
        nudge_threshold: float = 2.0,
        stop_threshold: float = 3.0,
        stutter_min_count: int = 3,
        insanity_similarity: float = 0.85,
        insanity_min_count: int = 3,
    ):
        """
        Initialize the guard.
        
        Args:
            nudge_threshold: Score at which to inject nudge message
            stop_threshold: Score at which to terminate agent
            stutter_min_count: Consecutive repeats for Type I detection
            insanity_similarity: Embedding similarity threshold for Type II
            insanity_min_count: Similar steps for Type II detection
        """
        self.nudge_threshold = nudge_threshold
        self.stop_threshold = stop_threshold
        
        # Initialize detectors
        self.detectors = {
            "stutter": StutterDetector(min_count=stutter_min_count),
            "insanity": InsanityDetector(
                similarity_threshold=insanity_similarity,
                min_count=insanity_min_count,
            ),
            "phantom": PhantomProgressDetector(),
            "pingpong": PingPongDetector(),
        }
        
        # State
        self._history: list[StepRecord] = []
        self._score: float = 0.0
    
    def on_step(self, step: StepRecord) -> GuardDecision:
        """
        Process a step and return a decision.
        
        Args:
            step: The current step to analyze
        
        Returns:
            GuardDecision with action, score, and message
        """
        # Run all detectors
        detections: list[DetectionResult] = []
        for name, detector in self.detectors.items():
            result = detector.detect(step, self._history)
            if result.detected:
                detections.append(result)
        
        # Update score
        if detections:
            # Add weighted scores for each detection
            for det in detections:
                self._score += SCORE_WEIGHTS.get(det.detection_type, 0.5)
        else:
            # Decay score if no detections
            self._score *= DECAY_FACTOR
        
        # Add step to history
        self._history.append(step)
        
        # Determine action
        detection_types = [d.detection_type for d in detections]
        
        if self._score >= self.stop_threshold:
            return GuardDecision(
                action="STOP",
                score=self._score,
                message=self._generate_stop_message(detections),
                detections=detection_types,
            )
        elif self._score >= self.nudge_threshold:
            return GuardDecision(
                action="NUDGE",
                score=self._score,
                message=self._generate_nudge_message(detections),
                detections=detection_types,
            )
        else:
            return GuardDecision(
                action="OBSERVE",
                score=self._score,
                message="",
                detections=detection_types,
            )
    
    def _generate_nudge_message(self, detections: list[DetectionResult]) -> str:
        """Generate a helpful nudge message based on detections."""
        if not detections:
            return "Consider trying a different approach."
        
        messages = []
        for det in detections:
            if det.detection_type == "stutter":
                messages.append(
                    "You're repeating the same action. Try a different approach."
                )
            elif det.detection_type == "insanity":
                messages.append(
                    "You're trying variations of the same strategy. Step back and consider alternatives."
                )
            elif det.detection_type == "phantom":
                messages.append(
                    "Your actions aren't changing the state. Check if there's a blocker."
                )
            elif det.detection_type == "pingpong":
                messages.append(
                    "You're in a handoff loop with another agent. Make a decision instead of delegating."
                )
        
        return " ".join(messages)
    
    def _generate_stop_message(self, detections: list[DetectionResult]) -> str:
        """Generate a stop message explaining why."""
        nudge_msg = self._generate_nudge_message(detections)
        return f"Loop detected. Stopping to prevent further resource waste. {nudge_msg}"
    
    def reset(self):
        """Reset guard state for a new conversation."""
        self._history.clear()
        self._score = 0.0
    
    @property
    def score(self) -> float:
        """Current cumulative loop score."""
        return self._score
    
    @property
    def history(self) -> list[StepRecord]:
        """Step history."""
        return self._history.copy()

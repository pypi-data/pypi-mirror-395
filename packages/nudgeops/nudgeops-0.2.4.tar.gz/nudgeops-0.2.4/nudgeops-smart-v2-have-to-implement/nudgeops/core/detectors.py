"""
nudgeops/core/detectors.py

Loop detection algorithms for NudgeOps.

Four detector types:
- Type I (Stutter): Exact repetition of actions
- Type II (Insanity): Semantic similarity in reasoning
- Type III (Phantom): Actions without state change
- Type IV (PingPong): Multi-agent handoff loops
"""

from __future__ import annotations

import math
from typing import Protocol

from nudgeops.core.state import StepRecord, DetectionResult


class Detector(Protocol):
    """Protocol for all detectors."""
    
    def detect(self, current: StepRecord, history: list[StepRecord]) -> DetectionResult:
        """
        Analyze current step against history.
        
        Args:
            current: The current step to analyze
            history: Previous steps in this session
        
        Returns:
            DetectionResult indicating if pattern was found
        """
        ...


class StutterDetector:
    """
    Type I: Detects exact repetition of actions.
    
    Triggers when the same tool with same args is called min_count
    times consecutively.
    
    Example:
        run_tests {} → run_tests {} → run_tests {}  # Detected!
    """
    
    def __init__(self, threshold: float = 0.99, min_count: int = 3):
        """
        Args:
            threshold: Hash match threshold (0.99 = exact match)
            min_count: Minimum consecutive repeats to trigger (default 3)
        """
        self.threshold = threshold
        self.min_count = min_count
    
    def detect(self, current: StepRecord, history: list[StepRecord]) -> DetectionResult:
        if not history:
            return DetectionResult(detected=False, detection_type="stutter")
        
        # Count consecutive matches from end of history
        stutter_count = 0
        for prev in reversed(history):
            if (prev.tool_name == current.tool_name and 
                prev.tool_args_hash == current.tool_args_hash):
                stutter_count += 1
            else:
                break
        
        detected = stutter_count >= self.min_count - 1  # -1 because current is the Nth
        
        if detected:
            return DetectionResult(
                detected=True,
                detection_type="stutter",
                confidence=1.0,
                message=f"Repeated {current.tool_name} {stutter_count + 1} times consecutively",
                details={"count": stutter_count + 1, "tool": current.tool_name}
            )
        
        # Proportional confidence if approaching threshold
        confidence = stutter_count / self.min_count if stutter_count > 0 else 0.0
        
        return DetectionResult(
            detected=False,
            detection_type="stutter",
            confidence=confidence,
            details={"count": stutter_count + 1}
        )


class InsanityDetector:
    """
    Type II: Detects semantic repetition in reasoning.
    
    "Doing the same thing and expecting different results."
    
    Uses embedding similarity to detect when agent is trying
    variations of the same approach.
    
    Example:
        "Fix bug in auth.py" → "Patch authentication" → "Repair auth"
    """
    
    def __init__(self, similarity_threshold: float = 0.85, min_count: int = 3):
        """
        Args:
            similarity_threshold: Cosine similarity threshold (0.85 = very similar)
            min_count: Minimum similar steps to trigger
        """
        self.similarity_threshold = similarity_threshold
        self.min_count = min_count
    
    def detect(self, current: StepRecord, history: list[StepRecord]) -> DetectionResult:
        if len(history) < self.min_count - 1:
            return DetectionResult(detected=False, detection_type="insanity")
        
        # Count semantically similar steps
        similar_count = 0
        for prev in history:
            similarity = self._cosine_similarity(
                current.thought_embedding, 
                prev.thought_embedding
            )
            if similarity >= self.similarity_threshold:
                similar_count += 1
        
        detected = similar_count >= self.min_count - 1
        
        if detected:
            return DetectionResult(
                detected=True,
                detection_type="insanity",
                confidence=min(similar_count / self.min_count, 1.0),
                message=f"Semantically similar reasoning detected {similar_count + 1} times",
                details={"similar_count": similar_count + 1}
            )
        
        return DetectionResult(
            detected=False,
            detection_type="insanity",
            confidence=similar_count / self.min_count if similar_count > 0 else 0.0,
            details={"similar_count": similar_count}
        )
    
    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)


class PhantomProgressDetector:
    """
    Type III: Detects actions that don't change state.
    
    Agent thinks it's making progress but nothing changes.
    
    Example:
        edit_file → state_hash unchanged (file is read-only)
        add_to_cart → cart still empty (variant OOS)
    """
    
    def __init__(self, unchanged_threshold: int = 2):
        """
        Args:
            unchanged_threshold: How many unchanged states to trigger
        """
        self.unchanged_threshold = unchanged_threshold
    
    def detect(self, current: StepRecord, history: list[StepRecord]) -> DetectionResult:
        if not history:
            return DetectionResult(detected=False, detection_type="phantom")
        
        # Count consecutive unchanged states
        unchanged_count = 0
        for prev in reversed(history):
            if prev.state_snapshot_hash == current.state_snapshot_hash:
                unchanged_count += 1
            else:
                break
        
        detected = unchanged_count >= self.unchanged_threshold
        
        if detected:
            return DetectionResult(
                detected=True,
                detection_type="phantom",
                confidence=min(unchanged_count / self.unchanged_threshold, 1.0),
                message=f"State unchanged for {unchanged_count + 1} steps",
                details={"unchanged_count": unchanged_count + 1}
            )
        
        return DetectionResult(
            detected=False,
            detection_type="phantom",
            confidence=unchanged_count / self.unchanged_threshold if unchanged_count > 0 else 0.0,
            details={"unchanged_count": unchanged_count}
        )


class PingPongDetector:
    """
    Type IV: Detects multi-agent handoff loops.
    
    Agent A hands to B, B hands to A, repeat.
    
    Example:
        search_agent → compare_agent → search_agent → compare_agent
    """
    
    def __init__(self, pattern_length: int = 4):
        """
        Args:
            pattern_length: How many handoffs to detect a ping-pong (A→B→A→B = 4)
        """
        self.pattern_length = pattern_length
    
    def detect(self, current: StepRecord, history: list[StepRecord]) -> DetectionResult:
        if not current.agent_id or len(history) < self.pattern_length - 1:
            return DetectionResult(detected=False, detection_type="pingpong")
        
        # Get recent agent sequence
        recent = [s.agent_id for s in history[-(self.pattern_length - 1):]] + [current.agent_id]
        recent = [a for a in recent if a is not None]
        
        if len(recent) < self.pattern_length:
            return DetectionResult(detected=False, detection_type="pingpong")
        
        # Check for A→B→A→B pattern
        agents = set(recent)
        if len(agents) == 2:  # Only two agents involved
            # Check alternating pattern
            is_alternating = all(recent[i] != recent[i+1] for i in range(len(recent) - 1))
            
            if is_alternating:
                return DetectionResult(
                    detected=True,
                    detection_type="pingpong",
                    confidence=1.0,
                    message=f"Ping-pong handoff between {list(agents)}",
                    details={"agents": list(agents), "pattern": recent}
                )
        
        return DetectionResult(
            detected=False,
            detection_type="pingpong",
            details={"recent_agents": recent}
        )

"""
Loop score calculation with decay for NudgeOps.

The scorer aggregates signals from all detectors and produces a single
loop_score that determines the intervention level:
- score < 2.0: OBSERVE (log only)
- score >= 2.0: NUDGE (inject message)
- score >= 3.0: STOP (terminate)

Key feature: Decay allows agents to recover after being nudged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nudgeops.core.state import DetectionResult, GuardConfig


# Score weights for each detection type
SCORE_WEIGHTS: dict[str, float] = {
    "TYPE_I_STUTTER": 2.0,      # Highest confidence - exact match
    "TYPE_II_INSANITY": 1.5,    # Semantic similarity
    "TYPE_III_PHANTOM": 0.5,    # Signal boost only
    "TYPE_IV_PINGPONG": 1.5,    # Coordination failure
}


@dataclass
class ScoringResult:
    """Result of score calculation."""

    score: float
    intervention: Literal["OBSERVE", "NUDGE", "STOP"]
    primary_detection: str | None
    detected_types: list[str]
    decay_applied: bool


class LoopScorer:
    """
    Calculates and manages loop scores with decay.

    The scorer implements the intervention ladder:
    - Loop Score: 0 → OBSERVE (log, no action)
    - Loop Score: 2 → NUDGE (inject message, continue)
    - Loop Score: 3+ → STOP (terminate, return metadata)

    With decay:
        Step 3: loop detected → score = 1.0
        Step 4: loop continues → score = 2.0 → NUDGE
        Step 5: agent recovers! → score = 1.0 (decay)
        Step 6: progress → score = 0.5 (decay)

        vs.

        Step 4: loop continues → score = 2.0 → NUDGE
        Step 5: still stuck → score = 3.0 → STOP
    """

    def __init__(self, config: GuardConfig | None = None) -> None:
        """
        Initialize the scorer.

        Args:
            config: Guard configuration with thresholds
        """
        self.config = config or GuardConfig()

    def calculate(
        self,
        detections: list[DetectionResult],
        current_score: float,
    ) -> ScoringResult:
        """
        Calculate new loop score based on detections.

        Args:
            detections: Results from all detectors
            current_score: Current loop score from state

        Returns:
            ScoringResult with new score and intervention
        """
        # Check if any detection this step
        detected_any = any(d["detected"] for d in detections)
        detected_types = [d["loop_type"] for d in detections if d["detected"]]

        # Apply decay if no detection (agent is recovering)
        if not detected_any:
            new_score = current_score * self.config.decay_rate
            return ScoringResult(
                score=new_score,
                intervention=self._get_intervention(new_score),
                primary_detection=None,
                detected_types=[],
                decay_applied=True,
            )

        # Accumulate detection scores
        new_score = current_score
        for detection in detections:
            if detection["detected"]:
                weight = SCORE_WEIGHTS.get(detection["loop_type"], 0)
                # Scale by confidence
                new_score += weight * detection["confidence"]

        # Cap at max score
        new_score = min(new_score, self.config.max_score)

        # Determine primary detection (highest weight that was detected)
        primary = None
        highest_weight = 0
        for detection in detections:
            if detection["detected"]:
                weight = SCORE_WEIGHTS.get(detection["loop_type"], 0)
                if weight > highest_weight:
                    highest_weight = weight
                    primary = detection["loop_type"]

        return ScoringResult(
            score=new_score,
            intervention=self._get_intervention(new_score),
            primary_detection=primary,
            detected_types=detected_types,
            decay_applied=False,
        )

    def _get_intervention(self, score: float) -> Literal["OBSERVE", "NUDGE", "STOP"]:
        """
        Determine intervention based on score.

        Args:
            score: Current loop score

        Returns:
            Intervention type
        """
        if score >= self.config.stop_threshold:
            return "STOP"
        elif score >= self.config.nudge_threshold:
            return "NUDGE"
        else:
            return "OBSERVE"

    def should_nudge(self, score: float) -> bool:
        """Check if score warrants a nudge."""
        return score >= self.config.nudge_threshold and score < self.config.stop_threshold

    def should_stop(self, score: float) -> bool:
        """Check if score warrants stopping."""
        return score >= self.config.stop_threshold


def calculate_loop_score(
    current_score: float,
    detections: list[DetectionResult],
    config: GuardConfig | None = None,
) -> float:
    """
    Convenience function to calculate loop score.

    Args:
        current_score: Current score from state
        detections: Detection results
        config: Optional configuration

    Returns:
        New loop score
    """
    scorer = LoopScorer(config)
    result = scorer.calculate(detections, current_score)
    return result.score

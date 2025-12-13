"""
Tests for NudgeOps loop scorer.
"""

from __future__ import annotations

import pytest

from nudgeops.core.scorer import LoopScorer, SCORE_WEIGHTS, calculate_loop_score
from nudgeops.core.state import DetectionResult, GuardConfig


def make_detection(
    detected: bool,
    loop_type: str,
    confidence: float = 1.0,
) -> DetectionResult:
    """Helper to create detection results."""
    return DetectionResult(
        detected=detected,
        confidence=confidence,
        loop_type=loop_type,
        details={},
    )


class TestLoopScorer:
    """Tests for the LoopScorer class."""

    def test_decay_when_no_detection(self):
        """Score should decay when no loop detected."""
        config = GuardConfig(decay_rate=0.5)
        scorer = LoopScorer(config)

        detections = [
            make_detection(False, "TYPE_I_STUTTER"),
            make_detection(False, "TYPE_II_INSANITY"),
        ]

        result = scorer.calculate(detections, current_score=2.0)

        assert result.score == 1.0  # 2.0 * 0.5
        assert result.decay_applied is True
        assert result.intervention == "OBSERVE"

    def test_accumulate_on_detection(self):
        """Score should accumulate when loop detected."""
        scorer = LoopScorer()

        detections = [
            make_detection(True, "TYPE_I_STUTTER", confidence=1.0),
            make_detection(False, "TYPE_II_INSANITY"),
        ]

        result = scorer.calculate(detections, current_score=0.0)

        assert result.score == SCORE_WEIGHTS["TYPE_I_STUTTER"]  # 2.0
        assert result.decay_applied is False
        assert result.primary_detection == "TYPE_I_STUTTER"

    def test_multiple_detections_accumulate(self):
        """Multiple detections should all contribute to score."""
        scorer = LoopScorer()

        detections = [
            make_detection(True, "TYPE_I_STUTTER", confidence=1.0),
            make_detection(True, "TYPE_III_PHANTOM", confidence=1.0),
        ]

        result = scorer.calculate(detections, current_score=0.0)

        expected = SCORE_WEIGHTS["TYPE_I_STUTTER"] + SCORE_WEIGHTS["TYPE_III_PHANTOM"]
        assert result.score == expected  # 2.0 + 0.5 = 2.5
        assert len(result.detected_types) == 2

    def test_confidence_scales_score(self):
        """Lower confidence should contribute less to score."""
        scorer = LoopScorer()

        detections = [
            make_detection(True, "TYPE_II_INSANITY", confidence=0.5),
        ]

        result = scorer.calculate(detections, current_score=0.0)

        expected = SCORE_WEIGHTS["TYPE_II_INSANITY"] * 0.5  # 1.5 * 0.5 = 0.75
        assert result.score == expected

    def test_max_score_cap(self):
        """Score should be capped at max_score."""
        config = GuardConfig(max_score=5.0)
        scorer = LoopScorer(config)

        detections = [
            make_detection(True, "TYPE_I_STUTTER", confidence=1.0),
            make_detection(True, "TYPE_II_INSANITY", confidence=1.0),
            make_detection(True, "TYPE_IV_PINGPONG", confidence=1.0),
        ]

        result = scorer.calculate(detections, current_score=3.0)

        assert result.score == 5.0  # Capped


class TestInterventionThresholds:
    """Tests for intervention threshold logic."""

    def test_observe_below_nudge_threshold(self):
        """Should OBSERVE when score below nudge threshold."""
        config = GuardConfig(nudge_threshold=2.0)
        scorer = LoopScorer(config)

        detections = [make_detection(True, "TYPE_III_PHANTOM")]  # +0.5

        result = scorer.calculate(detections, current_score=0.0)

        assert result.score == 0.5
        assert result.intervention == "OBSERVE"

    def test_nudge_at_threshold(self):
        """Should NUDGE when score reaches nudge threshold."""
        config = GuardConfig(nudge_threshold=2.0, stop_threshold=3.0)
        scorer = LoopScorer(config)

        detections = [make_detection(True, "TYPE_I_STUTTER")]  # +2.0

        result = scorer.calculate(detections, current_score=0.0)

        assert result.score == 2.0
        assert result.intervention == "NUDGE"

    def test_stop_at_threshold(self):
        """Should STOP when score reaches stop threshold."""
        config = GuardConfig(stop_threshold=3.0)
        scorer = LoopScorer(config)

        detections = [make_detection(True, "TYPE_I_STUTTER")]  # +2.0

        result = scorer.calculate(detections, current_score=1.5)

        assert result.score == 3.5
        assert result.intervention == "STOP"

    def test_nudge_between_thresholds(self):
        """Should NUDGE when between nudge and stop thresholds."""
        config = GuardConfig(nudge_threshold=2.0, stop_threshold=3.0)
        scorer = LoopScorer(config)

        result = scorer.calculate(
            [make_detection(True, "TYPE_II_INSANITY")],  # +1.5
            current_score=1.0,
        )

        assert result.score == 2.5
        assert result.intervention == "NUDGE"


class TestScoreDecay:
    """Tests for score decay (recovery) mechanism."""

    def test_recovery_after_nudge(self):
        """Agent should be able to recover after nudge via decay."""
        config = GuardConfig(decay_rate=0.5, nudge_threshold=2.0)
        scorer = LoopScorer(config)

        # Start at nudge threshold
        score = 2.0

        # No detection (agent recovered)
        result = scorer.calculate([make_detection(False, "TYPE_I_STUTTER")], score)
        assert result.score == 1.0  # Decayed

        # Still no detection
        result = scorer.calculate([make_detection(False, "TYPE_I_STUTTER")], result.score)
        assert result.score == 0.5  # Decayed again

        # Continue recovery
        result = scorer.calculate([make_detection(False, "TYPE_I_STUTTER")], result.score)
        assert result.score == 0.25
        assert result.intervention == "OBSERVE"

    def test_no_recovery_when_still_looping(self):
        """Score should not decay if still detecting loops."""
        config = GuardConfig(decay_rate=0.5)
        scorer = LoopScorer(config)

        score = 2.0

        # Still looping
        result = scorer.calculate(
            [make_detection(True, "TYPE_II_INSANITY")],
            score,
        )

        # Score should increase, not decay
        assert result.score > score
        assert result.decay_applied is False


class TestConvenienceFunction:
    """Tests for the calculate_loop_score convenience function."""

    def test_calculate_loop_score(self):
        """Convenience function should work like scorer."""
        detections = [make_detection(True, "TYPE_I_STUTTER")]

        score = calculate_loop_score(
            current_score=0.0,
            detections=detections,
        )

        assert score == SCORE_WEIGHTS["TYPE_I_STUTTER"]

    def test_calculate_loop_score_with_config(self):
        """Convenience function should accept config."""
        config = GuardConfig(max_score=1.0)
        detections = [make_detection(True, "TYPE_I_STUTTER")]  # +2.0

        score = calculate_loop_score(
            current_score=0.0,
            detections=detections,
            config=config,
        )

        assert score == 1.0  # Capped by config

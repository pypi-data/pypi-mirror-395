"""
Loop detectors for NudgeOps.

Implements four distinct detection patterns:
- Type I (Stutter): Exact same action repeated
- Type II (Insanity): Semantically similar actions repeated
- Type III (Phantom Progress): Different actions but state unchanged
- Type IV (Ping-Pong): Multi-agent circular handoffs
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

import numpy as np

from nudgeops.core.state import DetectionResult, StepRecord
from nudgeops.embedding.service import EmbeddingService
from nudgeops.embedding.utils import (
    check_negation_difference,
    cosine_similarity,
    format_step_descriptor,
)


class BaseDetector(Protocol):
    """Protocol for loop detectors."""

    def detect(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> DetectionResult:
        """
        Check if the current step indicates a loop.

        Args:
            current: The current step being analyzed
            history: Previous steps in the trajectory

        Returns:
            DetectionResult with detected flag and details
        """
        ...


class StutterDetector:
    """
    Type I: Exact Repetition Detector.

    Detects when an agent repeats the exact same action multiple times.
    Uses hash comparison of normalized tool arguments.

    Detection criteria:
    - current.tool_args_hash matches consecutive history entries
    - Tool name also matches
    - At least min_count consecutive repetitions (default 3)

    This requires 3+ identical actions to avoid flagging legitimate retries
    (e.g., running tests twice after a fix is normal behavior).
    """

    def __init__(self, threshold: float = 0.99, min_count: int = 3) -> None:
        """
        Initialize stutter detector.

        Args:
            threshold: Not used for exact matching, kept for interface consistency
            min_count: Minimum consecutive identical actions to trigger (default 3)
        """
        self.threshold = threshold
        self.min_count = min_count

    def detect(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> DetectionResult:
        """
        Detect exact repetition (Type I loop).

        Args:
            current: Current step
            history: Previous steps

        Returns:
            DetectionResult with high confidence if min_count+ exact matches found
        """
        if not history:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                loop_type="TYPE_I_STUTTER",
                details={"reason": "no_history"},
            )

        last_step = history[-1]

        # Check for exact match with last step
        tool_match = current.get("tool_name") == last_step.get("tool_name")
        hash_match = current.get("tool_args_hash") == last_step.get("tool_args_hash")

        if tool_match and hash_match and current.get("tool_args_hash"):
            # Count consecutive stutters (including current)
            stutter_count = 1
            for step in reversed(history):
                if (
                    step.get("tool_args_hash") == current.get("tool_args_hash")
                    and step.get("tool_name") == current.get("tool_name")
                ):
                    stutter_count += 1
                else:
                    break

            # Only trigger detection if we have enough consecutive repetitions
            detected = stutter_count >= self.min_count
            return DetectionResult(
                detected=detected,
                confidence=1.0 if detected else stutter_count / self.min_count,
                loop_type="TYPE_I_STUTTER",
                details={
                    "stutter_count": stutter_count,
                    "min_required": self.min_count,
                    "tool_name": current.get("tool_name"),
                    "repeated_hash": current.get("tool_args_hash", "")[:16],
                },
            )

        return DetectionResult(
            detected=False,
            confidence=0.0,
            loop_type="TYPE_I_STUTTER",
            details={"reason": "no_match"},
        )


class InsanityDetector:
    """
    Type II: Semantic Repetition Detector.

    Detects when an agent rephrases the same intent without changing strategy.
    "Insanity is doing the same thing over and over and expecting different results."

    Detection criteria:
    - Embedding similarity > threshold (default 0.85)
    - At least 3 similar steps in recent history

    This is the primary differentiator for NudgeOps - semantic loop detection.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        similarity_threshold: float = 0.85,
        min_count: int = 3,
        negation_penalty: float = 0.2,
    ) -> None:
        """
        Initialize insanity detector.

        Args:
            embedding_service: Service for generating embeddings
            similarity_threshold: Cosine similarity threshold (default 0.85)
            min_count: Minimum similar steps to trigger (default 3)
            negation_penalty: Similarity penalty for negation differences
        """
        self.embedding_service = embedding_service
        self.similarity_threshold = similarity_threshold
        self.min_count = min_count
        self.negation_penalty = negation_penalty

    def detect(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> DetectionResult:
        """
        Detect semantic repetition (Type II loop).

        Args:
            current: Current step with thought_embedding
            history: Previous steps with thought_embeddings

        Returns:
            DetectionResult indicating semantic loop if similar_count >= min_count
        """
        current_embedding = current.get("thought_embedding", [])

        if not current_embedding or not history:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                loop_type="TYPE_II_INSANITY",
                details={"reason": "no_embedding_or_history"},
            )

        # Calculate similarities with recent history
        similarities: list[tuple[float, int]] = []
        similar_steps: list[dict] = []

        for i, step in enumerate(history[-10:]):  # Look at last 10 steps
            step_embedding = step.get("thought_embedding", [])
            if not step_embedding:
                continue

            sim = cosine_similarity(current_embedding, step_embedding)

            # Apply negation heuristic for high similarity
            if sim > 0.92:
                current_desc = format_step_descriptor(
                    current.get("tool_name", ""),
                    current.get("raw_tool_args"),
                    current.get("outcome_type", ""),
                )
                step_desc = format_step_descriptor(
                    step.get("tool_name", ""),
                    step.get("raw_tool_args"),
                    step.get("outcome_type", ""),
                )
                if check_negation_difference(current_desc, step_desc):
                    sim -= self.negation_penalty

            similarities.append((sim, i))

            if sim >= self.similarity_threshold:
                similar_steps.append({
                    "index": i,
                    "similarity": round(sim, 3),
                    "tool_name": step.get("tool_name"),
                })

        similar_count = len(similar_steps)

        if similar_count >= self.min_count:
            avg_similarity = np.mean([s["similarity"] for s in similar_steps])
            return DetectionResult(
                detected=True,
                confidence=min(avg_similarity, 1.0),
                loop_type="TYPE_II_INSANITY",
                details={
                    "similar_count": similar_count,
                    "avg_similarity": round(float(avg_similarity), 3),
                    "similar_steps": similar_steps[:5],  # Limit for readability
                    "threshold": self.similarity_threshold,
                },
            )

        return DetectionResult(
            detected=False,
            confidence=max([s[0] for s in similarities]) if similarities else 0.0,
            loop_type="TYPE_II_INSANITY",
            details={
                "similar_count": similar_count,
                "min_required": self.min_count,
                "max_similarity": round(max([s[0] for s in similarities]), 3) if similarities else 0,
            },
        )


class PhantomProgressDetector:
    """
    Type III: State Frozen Detector.

    Detects when an agent takes different actions but the state doesn't change.
    The agent appears to make progress but achieves nothing.

    Detection criteria:
    - Action is different from previous (tool_name OR tool_args_hash differs)
    - But state_snapshot_hash is identical

    This is a signal boost, not a standalone loop type.
    """

    def __init__(self, consecutive_threshold: int = 2) -> None:
        """
        Initialize phantom progress detector.

        Args:
            consecutive_threshold: Number of consecutive unchanged states to trigger
        """
        self.consecutive_threshold = consecutive_threshold

    def detect(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> DetectionResult:
        """
        Detect phantom progress (Type III).

        Args:
            current: Current step with state_snapshot_hash
            history: Previous steps

        Returns:
            DetectionResult indicating state is frozen despite different actions
        """
        if not history:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                loop_type="TYPE_III_PHANTOM",
                details={"reason": "no_history"},
            )

        current_state_hash = current.get("state_snapshot_hash", "")
        if not current_state_hash:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                loop_type="TYPE_III_PHANTOM",
                details={"reason": "no_state_hash"},
            )

        last_step = history[-1]

        # Check if action is different
        action_different = (
            current.get("tool_name") != last_step.get("tool_name")
            or current.get("tool_args_hash") != last_step.get("tool_args_hash")
        )

        # Check if state is same
        state_same = current_state_hash == last_step.get("state_snapshot_hash", "")

        if action_different and state_same:
            # Count consecutive phantom progress
            consecutive = 1
            for step in reversed(history):
                if step.get("state_snapshot_hash") == current_state_hash:
                    consecutive += 1
                else:
                    break

            detected = consecutive >= self.consecutive_threshold
            return DetectionResult(
                detected=detected,
                confidence=min(consecutive / 3.0, 1.0),
                loop_type="TYPE_III_PHANTOM",
                details={
                    "consecutive_frozen": consecutive,
                    "threshold": self.consecutive_threshold,
                    "action_was_different": True,
                    "state_hash": current_state_hash[:16],
                },
            )

        return DetectionResult(
            detected=False,
            confidence=0.0,
            loop_type="TYPE_III_PHANTOM",
            details={
                "action_different": action_different,
                "state_same": state_same,
            },
        )


class PingPongDetector:
    """
    Type IV: Multi-Agent Deadlock Detector.

    Detects circular handoff patterns between agents or tools.
    Example: Writer -> Critic -> Writer -> Critic -> Writer (ping-pong)

    Detection criteria:
    - Agent sequence matches pattern like [A, B, A, B, A]
    - Pattern repeats at least twice
    - State is NOT changing (otherwise it's valid iteration, not deadlock)

    For single-agent mode, detects tool oscillation patterns.
    """

    def __init__(self, min_pattern_length: int = 2, min_repetitions: int = 2) -> None:
        """
        Initialize ping-pong detector.

        Args:
            min_pattern_length: Minimum pattern length (default 2 for A-B)
            min_repetitions: Pattern must repeat this many times (default 2)
        """
        self.min_pattern_length = min_pattern_length
        self.min_repetitions = min_repetitions

    def detect(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> DetectionResult:
        """
        Detect ping-pong pattern (Type IV).

        Args:
            current: Current step
            history: Previous steps

        Returns:
            DetectionResult indicating circular handoff pattern
        """
        if len(history) < self.min_pattern_length * self.min_repetitions:
            return DetectionResult(
                detected=False,
                confidence=0.0,
                loop_type="TYPE_IV_PINGPONG",
                details={"reason": "insufficient_history"},
            )

        # Build sequence using agent_id or tool_name
        all_steps = list(history[-20:]) + [current]
        sequence = []
        for step in all_steps:
            identifier = step.get("agent_id") or step.get("tool_name", "unknown")
            sequence.append(identifier)

        # Check for repeating N-grams (length 2, 3, 4)
        for n in [2, 3, 4]:
            if len(sequence) < n * 2:
                continue

            suffix = tuple(sequence[-n:])
            prev = tuple(sequence[-2 * n : -n])

            if suffix == prev:
                # Found pattern! Check how many times it repeats
                repetitions = 2
                for i in range(3, len(sequence) // n + 1):
                    check_start = -i * n
                    check_end = check_start + n
                    if check_end == 0:
                        check_slice = tuple(sequence[check_start:])
                    else:
                        check_slice = tuple(sequence[check_start:check_end])
                    if check_slice == suffix:
                        repetitions += 1
                    else:
                        break

                if repetitions >= self.min_repetitions:
                    # Check if state is actually changing (valid iteration vs deadlock)
                    # If state_snapshot_hash is changing across the pattern, it's progress
                    pattern_start = -n * repetitions
                    pattern_steps = all_steps[pattern_start:]
                    state_hashes = [
                        s.get("state_snapshot_hash", "")
                        for s in pattern_steps
                        if s.get("state_snapshot_hash")
                    ]

                    # If we have state hashes and they're all different, it's valid iteration
                    if len(state_hashes) >= 2 and len(set(state_hashes)) == len(state_hashes):
                        return DetectionResult(
                            detected=False,
                            confidence=0.0,
                            loop_type="TYPE_IV_PINGPONG",
                            details={
                                "pattern": list(suffix),
                                "pattern_length": n,
                                "repetitions": repetitions,
                                "reason": "state_changing_valid_iteration",
                                "unique_states": len(set(state_hashes)),
                            },
                        )

                    return DetectionResult(
                        detected=True,
                        confidence=min(repetitions / 3.0, 1.0),
                        loop_type="TYPE_IV_PINGPONG",
                        details={
                            "pattern": list(suffix),
                            "pattern_length": n,
                            "repetitions": repetitions,
                            "sequence_tail": sequence[-8:],
                        },
                    )

        return DetectionResult(
            detected=False,
            confidence=0.0,
            loop_type="TYPE_IV_PINGPONG",
            details={
                "sequence_tail": sequence[-6:],
                "reason": "no_repeating_pattern",
            },
        )


class CompositeDetector:
    """
    Runs all detectors and aggregates results.

    This is the main detector used by TrajectoryGuardNode.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        similarity_threshold: float = 0.85,
    ) -> None:
        """
        Initialize composite detector with all sub-detectors.

        Args:
            embedding_service: Service for embeddings (Type II)
            similarity_threshold: Threshold for semantic similarity
        """
        self.detectors: list[BaseDetector] = [
            StutterDetector(),
            InsanityDetector(
                embedding_service=embedding_service,
                similarity_threshold=similarity_threshold,
            ),
            PhantomProgressDetector(),
            PingPongDetector(),
        ]

    def detect_all(
        self,
        current: StepRecord,
        history: list[StepRecord],
    ) -> list[DetectionResult]:
        """
        Run all detectors on the current step.

        Args:
            current: Current step
            history: Previous steps

        Returns:
            List of DetectionResults from all detectors
        """
        return [detector.detect(current, history) for detector in self.detectors]

"""
Drop-in guard for ANY agent framework.

Usage is simple:
1. Create a UniversalGuard
2. After each tool execution, call guard.on_step(step_record)
3. Check the returned GuardDecision for OBSERVE/NUDGE/STOP

This works for:
- Cursor IDE
- Claude Code
- LangGraph agents
- AutoGen
- CrewAI
- Any custom framework

The only requirement: You must be able to produce a StepRecord
after each tool execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from nudgeops.core.state import StepRecord, GuardConfig
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer


GuardAction = Literal["OBSERVE", "NUDGE", "STOP"]


@dataclass
class GuardDecision:
    """
    The guard's decision after analyzing a step.

    Attributes:
        action: What to do (OBSERVE, NUDGE, or STOP)
        score: Current cumulative loop score
        message: If NUDGE/STOP, a message to show/inject
        detections: List of detection types that fired
    """

    action: GuardAction
    score: float
    message: str | None = None
    detections: list[str] | None = None


class UniversalGuard:
    """
    Universal loop detection guard for any agent framework.

    Example usage with a generic agent:

        guard = UniversalGuard()

        for step in agent.run():
            # After each tool execution, check with guard
            step_record = build_step_record(step.action, step.result, env)
            decision = guard.on_step(step_record)

            if decision.action == "STOP":
                print(f"Stopping agent: {decision.message}")
                break
            elif decision.action == "NUDGE":
                agent.inject_message(decision.message)

    Example usage with LangGraph:

        guard = UniversalGuard()

        def guard_node(state):
            step_record = extract_step_record(state)
            decision = guard.on_step(step_record)

            if decision.action == "STOP":
                return Command(goto=END)
            elif decision.action == "NUDGE":
                state.messages.append(SystemMessage(decision.message))

            return state
    """

    def __init__(
        self,
        nudge_threshold: float = 2.0,
        stop_threshold: float = 3.0,
        config: GuardConfig | None = None,
    ) -> None:
        """
        Initialize the guard.

        Args:
            nudge_threshold: Score at which to nudge (default 2.0)
            stop_threshold: Score at which to stop (default 3.0)
            config: Optional GuardConfig for full configuration
        """
        if config:
            self._config = config
        else:
            self._config = GuardConfig(
                nudge_threshold=nudge_threshold,
                stop_threshold=stop_threshold,
            )

        self._detector = CompositeDetector()
        self._scorer = LoopScorer(self._config)
        self._history: list[StepRecord] = []
        self._score: float = 0.0

    def on_step(self, step: StepRecord) -> GuardDecision:
        """
        Process a step and return a decision.

        This is the main entry point. Call this after EVERY tool execution.

        Args:
            step: The StepRecord from the just-completed action

        Returns:
            GuardDecision with action (OBSERVE/NUDGE/STOP) and details
        """
        # Run all detectors
        detections = self._detector.detect_all(step, self._history)

        # Update score (includes decay logic)
        result = self._scorer.calculate(detections, self._score)
        self._score = result.score

        # Add to history
        self._history.append(step)

        # Collect detection types that fired
        detection_types = [d["loop_type"] for d in detections if d["detected"]]

        # Return decision based on score
        if result.intervention == "STOP":
            return GuardDecision(
                action="STOP",
                score=self._score,
                message=self._build_stop_message(detection_types),
                detections=detection_types,
            )

        if result.intervention == "NUDGE":
            return GuardDecision(
                action="NUDGE",
                score=self._score,
                message=self._build_nudge_message(detection_types),
                detections=detection_types,
            )

        return GuardDecision(
            action="OBSERVE",
            score=self._score,
            detections=detection_types,
        )

    def reset(self) -> None:
        """Reset the guard state. Call between agent sessions."""
        self._history = []
        self._score = 0.0

    @property
    def score(self) -> float:
        """Current cumulative loop score."""
        return self._score

    @property
    def history(self) -> list[StepRecord]:
        """History of all steps seen."""
        return self._history.copy()

    def _build_nudge_message(self, detection_types: list[str]) -> str:
        """
        Build a helpful nudge message based on what was detected.

        The goal is to help the agent understand WHY it's stuck
        and WHAT to try instead.
        """
        if "TYPE_I_STUTTER" in detection_types:
            return (
                "You've repeated the exact same action multiple times "
                "without making progress. Consider:\n"
                "- Is a prerequisite step missing?\n"
                "- Is the tool reporting success but failing silently?\n"
                "- Try a different approach entirely."
            )

        if "TYPE_II_INSANITY" in detection_types:
            return (
                "You've attempted several semantically similar actions without success. "
                "The current approach doesn't seem to be working. Consider:\n"
                "- Is the goal actually achievable?\n"
                "- Is there a fundamentally different strategy?\n"
                "- Should you ask for clarification or report failure?"
            )

        if "TYPE_III_PHANTOM" in detection_types:
            return (
                "Your actions are not changing the underlying state. "
                "You may be experiencing 'phantom progress'. Consider:\n"
                "- Verify that your actions are actually taking effect.\n"
                "- Check for silent failures or permission issues.\n"
                "- The environment may not be responding as expected."
            )

        if "TYPE_IV_PINGPONG" in detection_types:
            return (
                "There appears to be a handoff loop between agents. "
                "Tasks are being passed back and forth without progress. Consider:\n"
                "- Clarify responsibilities between agents.\n"
                "- Have one agent take ownership of the task.\n"
                "- Check if the task is actually completable."
            )

        return (
            "NudgeOps detected potential looping behavior. "
            "Please review your recent actions and consider a different approach."
        )

    def _build_stop_message(self, detection_types: list[str]) -> str:
        """Build a stop message explaining why the agent was halted."""
        types_str = ", ".join(detection_types) if detection_types else "unknown"
        return (
            f"NudgeOps has stopped the agent due to detected loop patterns: {types_str}. "
            f"Final score: {self._score:.2f}. "
            "The agent appeared to be stuck and was consuming resources without progress."
        )

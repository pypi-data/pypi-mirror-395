"""
Intervention templates and payloads for NudgeOps.

Provides nudge messages and stop payloads for each detection type.
The nudge is the hero feature - it helps agents recover before stopping.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nudgeops.core.state import DetectionResult


@dataclass
class NudgeMessage:
    """A nudge message to inject into agent context."""

    content: str
    loop_type: str
    severity: str  # "warning" or "critical"


@dataclass
class StopPayload:
    """Payload returned when agent is stopped."""

    status: str
    reason: str
    loop_score: float
    nudges_sent: int
    steps_taken: int
    similar_actions: list[dict[str, Any]]
    recommendation: str


class InterventionManager:
    """
    Manages nudge messages and stop payloads.

    The Nudge tries to save the task before killing:
    - Injects a SystemMessage into agent context
    - Explains what went wrong
    - Suggests alternative approaches
    - Lets agent continue with new context

    If still stuck after nudge, then we stop.
    """

    # Nudge templates for each detection type
    NUDGE_TEMPLATES: dict[str, str] = {
        "TYPE_I_STUTTER": """[System Observation]

⚠️ You have executed the EXACT SAME action twice:
  Tool: {tool_name}
  Args: {args_preview}

This action returned "{outcome}" both times.
Repeating it will not yield different results.

Please try one of these alternatives:
• Use a different tool
• Try different parameters
• Ask the user for clarification
• Acknowledge you cannot complete this task""",

        "TYPE_II_INSANITY": """[System Observation]

⚠️ You have attempted semantically similar actions {similar_count} times without success:

{action_list}

These are functionally equivalent queries.
Rephrasing is NOT a new strategy.

Consider:
• The information may not exist in this source
• Try a COMPLETELY different approach
• Use a different tool entirely
• Ask the user for alternative sources""",

        "TYPE_III_PHANTOM": """[System Observation]

⚠️ Your actions are not changing the state.
You have taken {consecutive_count} different actions but the result remains the same.

This may indicate:
• A broken or unresponsive system
• Incorrect tool usage
• A task that cannot be completed

Please:
• Try a fundamentally different approach
• Check if the system is responding correctly
• Ask the user for help""",

        "TYPE_IV_PINGPONG": """[System Observation]

⚠️ A circular pattern has been detected:
  {pattern_display}

This appears to be an endless delegation loop.
No progress is being made after {repetitions} cycles.

Please:
• Make a final decision now
• Escalate to a human if you cannot decide
• Accept the current output as "good enough\"""",
    }

    def __init__(self) -> None:
        """Initialize intervention manager."""
        pass

    def create_nudge(
        self,
        detections: list[DetectionResult],
        context: dict[str, Any] | None = None,
    ) -> NudgeMessage:
        """
        Create a nudge message based on detections.

        Args:
            detections: Results from detectors
            context: Additional context for formatting

        Returns:
            NudgeMessage to inject into agent context
        """
        context = context or {}

        # Find the primary detection (first detected)
        primary = None
        for d in detections:
            if d["detected"]:
                primary = d
                break

        if primary is None:
            # No detection, return generic message
            return NudgeMessage(
                content="[System Observation]\n\nPlease review your approach.",
                loop_type="UNKNOWN",
                severity="warning",
            )

        loop_type = primary["loop_type"]
        details = primary.get("details", {})

        # Format template based on type
        template = self.NUDGE_TEMPLATES.get(loop_type, self.NUDGE_TEMPLATES["TYPE_I_STUTTER"])

        if loop_type == "TYPE_I_STUTTER":
            content = template.format(
                tool_name=details.get("tool_name", "unknown"),
                args_preview=context.get("args_preview", "..."),
                outcome=context.get("outcome", "no change"),
            )

        elif loop_type == "TYPE_II_INSANITY":
            similar_steps = details.get("similar_steps", [])
            action_list = "\n".join(
                f"  {i+1}. {s.get('tool_name', 'action')} (similarity: {s.get('similarity', 0):.2f})"
                for i, s in enumerate(similar_steps[:5])
            )
            content = template.format(
                similar_count=details.get("similar_count", 3),
                action_list=action_list or "  (actions not recorded)",
            )

        elif loop_type == "TYPE_III_PHANTOM":
            content = template.format(
                consecutive_count=details.get("consecutive_frozen", 2),
            )

        elif loop_type == "TYPE_IV_PINGPONG":
            pattern = details.get("pattern", [])
            pattern_display = " → ".join(str(p) for p in pattern)
            content = template.format(
                pattern_display=pattern_display or "A → B → A → B",
                repetitions=details.get("repetitions", 2),
            )

        else:
            content = template

        return NudgeMessage(
            content=content,
            loop_type=loop_type,
            severity="warning" if primary["confidence"] < 0.9 else "critical",
        )

    def create_stop_payload(
        self,
        detections: list[DetectionResult],
        loop_score: float,
        nudges_sent: int,
        steps_taken: int,
        similar_actions: list[dict[str, Any]] | None = None,
    ) -> StopPayload:
        """
        Create a stop payload with diagnostic information.

        Args:
            detections: Final detection results
            loop_score: Final loop score
            nudges_sent: Number of nudges that were sent
            steps_taken: Total steps taken
            similar_actions: List of similar actions for debugging

        Returns:
            StopPayload with full diagnostic info
        """
        # Find primary reason
        primary_type = "UNKNOWN"
        for d in detections:
            if d["detected"]:
                primary_type = d["loop_type"]
                break

        # Generate recommendation based on type
        recommendations = {
            "TYPE_I_STUTTER": "Review agent prompt - may be stuck in deterministic rut",
            "TYPE_II_INSANITY": "Agent is rephrasing without changing strategy - consider prompt refinement",
            "TYPE_III_PHANTOM": "Check if tools/APIs are responding correctly",
            "TYPE_IV_PINGPONG": "Multi-agent coordination issue - review handoff logic",
        }

        return StopPayload(
            status="guardrail_triggered",
            reason=primary_type,
            loop_score=loop_score,
            nudges_sent=nudges_sent,
            steps_taken=steps_taken,
            similar_actions=similar_actions or [],
            recommendation=recommendations.get(
                primary_type,
                "Review agent configuration and tool setup"
            ),
        )

    def format_stop_message(self, payload: StopPayload) -> str:
        """
        Format stop payload as a human-readable message.

        Args:
            payload: Stop payload

        Returns:
            Formatted message string
        """
        return f"""[TrajectoryGuard - Execution Stopped]

Status: {payload.status}
Reason: {payload.reason}
Loop Score: {payload.loop_score:.2f}
Nudges Sent: {payload.nudges_sent}
Steps Taken: {payload.steps_taken}

Recommendation: {payload.recommendation}

The agent was unable to recover after intervention.
Please review the trajectory and adjust the agent configuration."""

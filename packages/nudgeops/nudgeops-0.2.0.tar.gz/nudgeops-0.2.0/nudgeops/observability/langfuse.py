"""
Langfuse integration for NudgeOps observability.

Provides tracing and scoring of agent trajectories:
- trajectory_health score (inverse of loop score)
- LOOP_DETECTED tags
- Intervention metadata
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from nudgeops.core.state import DetectionResult, GuardConfig

logger = logging.getLogger(__name__)

# Maximum score used for health calculation
MAX_SCORE = 5.0


class LangfuseObserver:
    """
    Langfuse observer for NudgeOps events.

    Integrates with Langfuse to provide:
    - trajectory_health score (0-1, higher is healthier)
    - LOOP_DETECTED tags when loops are found
    - Intervention metadata

    Usage:
        observer = LangfuseObserver()

        # In guard node
        observer.on_detection(detections, loop_score)

        # After intervention
        observer.on_intervention("NUDGE", detections)
    """

    def __init__(
        self,
        enabled: bool = True,
        score_name: str = "trajectory_health",
    ) -> None:
        """
        Initialize Langfuse observer.

        Args:
            enabled: Whether Langfuse integration is enabled
            score_name: Name of the health score metric
        """
        self.enabled = enabled
        self.score_name = score_name
        self._langfuse_available = self._check_langfuse()

    def _check_langfuse(self) -> bool:
        """Check if Langfuse is available."""
        if not self.enabled:
            return False

        try:
            from langfuse.decorators import langfuse_context
            return True
        except ImportError:
            logger.debug("Langfuse not installed, observability disabled")
            return False

    def on_detection(
        self,
        detections: list[DetectionResult],
        loop_score: float,
        step_id: str = "",
    ) -> None:
        """
        Record detection results in Langfuse.

        Args:
            detections: Results from all detectors
            loop_score: Current loop score
            step_id: Current step identifier
        """
        if not self._langfuse_available:
            return

        try:
            from langfuse.decorators import langfuse_context

            # Calculate health score (inverse of loop score)
            health = 1.0 - (min(loop_score, MAX_SCORE) / MAX_SCORE)

            # Score current observation
            langfuse_context.score_current_observation(
                name=self.score_name,
                value=health,
                comment=f"Loop score: {loop_score:.2f}",
            )

            # Tag if loop detected
            detected_types = [d["loop_type"] for d in detections if d["detected"]]
            if detected_types:
                tags = ["LOOP_DETECTED"] + detected_types
                langfuse_context.update_current_trace(tags=tags)

        except Exception as e:
            logger.warning(f"Failed to record in Langfuse: {e}")

    def on_intervention(
        self,
        intervention: str,
        detections: list[DetectionResult],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Record intervention in Langfuse.

        Args:
            intervention: Type of intervention (OBSERVE, NUDGE, STOP)
            detections: Detection results that triggered intervention
            metadata: Additional metadata to record
        """
        if not self._langfuse_available:
            return

        try:
            from langfuse.decorators import langfuse_context

            observation_metadata = {
                "intervention": intervention,
                "detected_types": [d["loop_type"] for d in detections if d["detected"]],
            }
            if metadata:
                observation_metadata.update(metadata)

            langfuse_context.update_current_observation(metadata=observation_metadata)

            # Add intervention tag
            if intervention in ("NUDGE", "STOP"):
                langfuse_context.update_current_trace(
                    tags=[f"INTERVENTION_{intervention}"]
                )

        except Exception as e:
            logger.warning(f"Failed to record intervention in Langfuse: {e}")

    def wrap_node(self, node_func: Callable) -> Callable:
        """
        Wrap a node function with Langfuse observation.

        Args:
            node_func: The node function to wrap

        Returns:
            Wrapped function with Langfuse observation
        """
        if not self._langfuse_available:
            return node_func

        try:
            from langfuse.decorators import observe

            return observe(name="trajectory_guard")(node_func)
        except Exception:
            return node_func


def create_langfuse_callback(
    config: GuardConfig | None = None,
) -> LangfuseObserver:
    """
    Create a Langfuse observer for NudgeOps.

    Args:
        config: Guard configuration

    Returns:
        Configured LangfuseObserver
    """
    enabled = config.enable_langfuse if config else False
    return LangfuseObserver(enabled=enabled)

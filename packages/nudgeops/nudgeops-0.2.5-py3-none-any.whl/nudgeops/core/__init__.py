"""
Core components for NudgeOps loop detection and intervention.
"""

from nudgeops.core.state import (
    AgentState,
    DetectionResult,
    GuardConfig,
    LoopStatus,
    StepRecord,
)
from nudgeops.core.detectors import (
    BaseDetector,
    InsanityDetector,
    PhantomProgressDetector,
    PingPongDetector,
    StutterDetector,
)
from nudgeops.core.scorer import LoopScorer
from nudgeops.core.interventions import InterventionManager

__all__ = [
    "AgentState",
    "StepRecord",
    "DetectionResult",
    "LoopStatus",
    "GuardConfig",
    "BaseDetector",
    "StutterDetector",
    "InsanityDetector",
    "PhantomProgressDetector",
    "PingPongDetector",
    "LoopScorer",
    "InterventionManager",
]

"""
NudgeOps - Runtime semantic guardrails for AI agents.

Detect loops. Nudge agents back on track. Stop runaway costs.

Two protection levels:
- v0.1 (core): Pattern-based detection (stutter, insanity, phantom, ping-pong)
- v0.2 (smart): Intent-level protection with LLM thought normalization
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
from nudgeops.integrations.apply_guard import apply_guard
from nudgeops.integrations.universal_guard import UniversalGuard, GuardDecision
from nudgeops.integrations.langgraph import (
    NudgeOpsNode,
    NudgeOpsState,
    add_guard_to_graph,
)

# Smart v2 - Intent-level protection
from nudgeops.smart import (
    SmartGuard,
    SmartGuardBuilder,
    GuardResult,
    Decision,
    SmartNudgeOps,
    SmartNudgeOpsBuilder,
    SmartNudgeOpsConfig,
    ThoughtNormalizer,
    MockLLMClient,
    FailureMemory,
    ObservabilityLayer,
)

__version__ = "0.2.4"

__all__ = [
    # State types
    "AgentState",
    "StepRecord",
    "DetectionResult",
    "LoopStatus",
    "GuardConfig",
    # Detectors
    "BaseDetector",
    "StutterDetector",
    "InsanityDetector",
    "PhantomProgressDetector",
    "PingPongDetector",
    # Scoring
    "LoopScorer",
    # Interventions
    "InterventionManager",
    # Integration (core)
    "NudgeOpsNode",
    "NudgeOpsState",
    "add_guard_to_graph",
    "apply_guard",
    "UniversalGuard",
    "GuardDecision",
    # Smart v2 - Intent-level protection
    "SmartGuard",
    "SmartGuardBuilder",
    "GuardResult",
    "Decision",
    "SmartNudgeOps",
    "SmartNudgeOpsBuilder",
    "SmartNudgeOpsConfig",
    "ThoughtNormalizer",
    "MockLLMClient",
    "FailureMemory",
    "ObservabilityLayer",
]

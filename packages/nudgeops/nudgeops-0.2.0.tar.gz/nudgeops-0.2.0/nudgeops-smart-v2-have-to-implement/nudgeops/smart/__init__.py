"""
Smart NudgeOps - Intent-level failure tracking and blocking.

This module provides:
- Thought normalization (intent extraction)
- State and action hashing
- Two-level failure memory (action + intent)
- Smart guard with configurable thresholds
- LangGraph integration
- Observability and metrics

Quick Start:
    from nudgeops.smart import SmartNudgeOps, SmartNudgeOpsBuilder
    
    # Simple setup
    nudgeops = SmartNudgeOps(llm_client=my_llm)
    nudgeops.apply(builder)
    
    # Builder pattern for more control
    nudgeops = SmartNudgeOpsBuilder() \\
        .with_llm(my_llm) \\
        .with_intent_threshold(3) \\
        .with_tenant("acme") \\
        .build()
"""

# Core components
from .thought_normalizer import (
    ThoughtNormalizer,
    LLMClient,
    MockLLMClient,
    RuleBasedNormalizer,
    HybridNormalizer,
)

from .hashers import (
    StateHasher,
    ActionHasher,
    CombinedHasher,
)

from .failure_memory import (
    FailureMemory,
    ActionFailure,
    IntentCluster,
)

from .guard import (
    SmartGuard,
    SmartGuardBuilder,
    GuardResult,
    Decision,
)

from .events import (
    FailureEvent,
    FailureEventBuilder,
    FailureType,
    RecoveryStatus,
    EventStore,
    InMemoryEventStore,
    canonicalize_error,
    canonicalize_state,
    canonicalize_action,
    get_failure_type,
)

from .observability import (
    ObservabilityLayer,
    ObservabilityEvent,
    AgentStats,
    TenantStats,
    get_observability,
    set_observability,
)

from .langgraph_integration import (
    SmartNudgeOps,
    SmartNudgeOpsBuilder,
    SmartNudgeOpsConfig,
    apply_smart_guard,
)


__all__ = [
    # Thought normalization
    "ThoughtNormalizer",
    "LLMClient",
    "MockLLMClient",
    "RuleBasedNormalizer",
    "HybridNormalizer",
    
    # Hashers
    "StateHasher",
    "ActionHasher",
    "CombinedHasher",
    
    # Failure memory
    "FailureMemory",
    "ActionFailure",
    "IntentCluster",
    
    # Guard
    "SmartGuard",
    "SmartGuardBuilder",
    "GuardResult",
    "Decision",
    
    # Events
    "FailureEvent",
    "FailureEventBuilder",
    "FailureType",
    "RecoveryStatus",
    "EventStore",
    "InMemoryEventStore",
    "canonicalize_error",
    "canonicalize_state",
    "canonicalize_action",
    "get_failure_type",
    
    # Observability
    "ObservabilityLayer",
    "ObservabilityEvent",
    "AgentStats",
    "TenantStats",
    "get_observability",
    "set_observability",
    
    # LangGraph integration
    "SmartNudgeOps",
    "SmartNudgeOpsBuilder",
    "SmartNudgeOpsConfig",
    "apply_smart_guard",
]

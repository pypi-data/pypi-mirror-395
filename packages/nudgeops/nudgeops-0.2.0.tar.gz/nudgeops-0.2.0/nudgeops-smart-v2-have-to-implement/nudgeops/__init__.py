"""
NudgeOps - Runtime semantic guardrails for AI agents.

Detects when agents are stuck in loops and provides interventions.

Quick Start (Original - Detection Only):
    from nudgeops.integrations import UniversalGuard
    
    guard = UniversalGuard()
    decision = guard.on_step(step_record)
    
    if decision.action == "NUDGE":
        inject_system_message(decision.message)
    elif decision.action == "STOP":
        terminate_agent()

Quick Start (Smart - Intent-Level Blocking):
    from nudgeops.smart import SmartNudgeOps
    
    nudgeops = SmartNudgeOps(llm_client=my_llm)
    nudgeops.apply(builder)  # Apply to LangGraph builder
    
For LangGraph integration:
    from nudgeops.integrations.langgraph import add_guard_to_graph
    
    builder = StateGraph(AgentState)
    # ... add nodes ...
    add_guard_to_graph(builder)
"""

__version__ = "0.2.0"

from nudgeops.core.state import StepRecord, DetectionResult
from nudgeops.integrations.universal_guard import UniversalGuard, GuardDecision

# Smart module exports
from nudgeops.smart import (
    SmartNudgeOps,
    SmartNudgeOpsBuilder,
    SmartGuard,
    ThoughtNormalizer,
    FailureMemory,
    ObservabilityLayer,
)

__all__ = [
    # Original
    "StepRecord",
    "DetectionResult",
    "UniversalGuard",
    "GuardDecision",
    # Smart
    "SmartNudgeOps",
    "SmartNudgeOpsBuilder", 
    "SmartGuard",
    "ThoughtNormalizer",
    "FailureMemory",
    "ObservabilityLayer",
]

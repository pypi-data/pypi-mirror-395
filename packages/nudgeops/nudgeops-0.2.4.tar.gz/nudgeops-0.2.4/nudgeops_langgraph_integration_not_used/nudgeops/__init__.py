"""
NudgeOps - Runtime semantic guardrails for AI agents.

Detects when agents are stuck in loops and provides interventions.

Quick Start:
    from nudgeops.integrations import UniversalGuard
    
    guard = UniversalGuard()
    decision = guard.on_step(step_record)
    
    if decision.action == "NUDGE":
        inject_system_message(decision.message)
    elif decision.action == "STOP":
        terminate_agent()

For LangGraph integration:
    from nudgeops.integrations.langgraph import add_guard_to_graph
    
    builder = StateGraph(AgentState)
    # ... add nodes ...
    add_guard_to_graph(builder)
"""

__version__ = "0.1.0"

from nudgeops.core.state import StepRecord, DetectionResult
from nudgeops.integrations.universal_guard import UniversalGuard, GuardDecision

__all__ = [
    "StepRecord",
    "DetectionResult",
    "UniversalGuard",
    "GuardDecision",
]

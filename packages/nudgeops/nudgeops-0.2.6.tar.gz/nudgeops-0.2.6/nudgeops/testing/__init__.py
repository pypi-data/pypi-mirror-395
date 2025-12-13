"""
NudgeOps Mock Testing Framework.

Provides domain-agnostic testing infrastructure for loop detection.
Enables testing code agents, shopping agents, and any other agent type
without making real API calls.

Key components:
- interfaces: Action, Result, IMockEnvironment protocol
- step_adapter: Converts (Action, Result, Env) → StepRecord
- environments: MockCodeEnvironment, MockShoppingEnvironment
- scenarios: Failure pattern behaviors for each domain
- openai_agent: Real OpenAI LLM agent for LangGraph
- loop_inducing_tools: Mock tools that cause loops for testing
"""

from __future__ import annotations

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment
from nudgeops.testing.step_adapter import (
    build_step_record,
    compute_cosine_similarity,
    SEMANTIC_GROUPS,
)

# Real LLM testing (optional - requires openai package)
try:
    from nudgeops.testing.openai_agent import OpenAIAgentNode, CostTracker
    OPENAI_AGENT_AVAILABLE = True
except ImportError:
    OPENAI_AGENT_AVAILABLE = False
    OpenAIAgentNode = None
    CostTracker = None

from nudgeops.testing.loop_inducing_tools import LoopInducingTools, ToolExecution

__all__ = [
    # Interfaces
    "Action",
    "Result",
    "IMockEnvironment",
    # Step adapter
    "build_step_record",
    "compute_cosine_similarity",
    "SEMANTIC_GROUPS",
    # Real LLM testing
    "OpenAIAgentNode",
    "CostTracker",
    "LoopInducingTools",
    "ToolExecution",
    "OPENAI_AGENT_AVAILABLE",
]

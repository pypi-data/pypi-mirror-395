"""
nudgeops.testing - Testing utilities for NudgeOps.

Includes:
- OpenAI agent for real LLM testing
- Loop-inducing mock tools
- Test scenarios
"""

from nudgeops.testing.openai_agent import OpenAIAgentNode
from nudgeops.testing.loop_inducing_tools import LoopInducingTools

__all__ = [
    "OpenAIAgentNode",
    "LoopInducingTools",
]

"""
nudgeops/testing/openai_agent.py

OpenAI-based agent node for LangGraph integration testing.

This module provides a real LLM agent that:
1. Calls OpenAI API (GPT-4o-mini or GPT-4o)
2. Supports tool calling
3. Tracks costs
4. Has safety limits

Usage:
    from nudgeops.testing.openai_agent import OpenAIAgentNode
    
    agent = OpenAIAgentNode(model="gpt-4o-mini", max_calls=15)
    builder.add_node("agent", agent)
"""

from __future__ import annotations

import os
import json
from dataclasses import dataclass, field
from typing import Any

# OpenAI import - will fail gracefully if not installed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


# ---------------------------------------------------------------------------
# Cost Tracking
# ---------------------------------------------------------------------------

# Pricing per 1M tokens (as of 2025)
MODEL_PRICING = {
    "gpt-5-nano": {"input": 0.05, "output": 0.40},      # Cheapest!
    "gpt-5-mini": {"input": 0.25, "output": 2.00},
    "gpt-5": {"input": 1.25, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}


@dataclass
class CostTracker:
    """Tracks API call costs."""
    
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    call_count: int = 0
    
    def add_usage(self, input_tokens: int, output_tokens: int):
        """Record token usage from an API call."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.call_count += 1
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost in dollars."""
        pricing = MODEL_PRICING.get(self.model, {"input": 10.0, "output": 30.0})
        input_cost = (self.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (self.output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
    
    def __str__(self) -> str:
        return (
            f"Calls: {self.call_count}, "
            f"Tokens: {self.input_tokens} in / {self.output_tokens} out, "
            f"Cost: ${self.total_cost:.4f}"
        )


# ---------------------------------------------------------------------------
# Tool Definitions for OpenAI
# ---------------------------------------------------------------------------

DEFAULT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search for products by query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "select_product",
            "description": "Select a product by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID to select"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "select_variant",
            "description": "Select a product variant (size, color, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "variant": {
                        "type": "string",
                        "description": "Variant to select (e.g., 'XL', 'Blue')"
                    }
                },
                "required": ["variant"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Add the currently selected product to cart",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "checkout",
            "description": "Proceed to checkout",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "give_up",
            "description": "Give up on the task if it seems impossible",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why you're giving up"
                    }
                },
                "required": ["reason"]
            }
        }
    },
]


# ---------------------------------------------------------------------------
# OpenAI Agent Node
# ---------------------------------------------------------------------------

class OpenAIAgentNode:
    """
    LangGraph-compatible agent node that calls OpenAI API.
    
    Features:
    - Supports tool calling
    - Tracks costs
    - Has safety limits (max calls, max cost)
    - Switchable models
    
    Example:
        agent = OpenAIAgentNode(model="gpt-4o-mini")
        builder.add_node("agent", agent)
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        max_calls: int = 15,
        max_cost: float = 0.50,
        tools: list[dict] | None = None,
        system_prompt: str | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize the agent.
        
        Args:
            model: OpenAI model name
            max_calls: Maximum API calls before stopping
            max_cost: Maximum cost in dollars before stopping
            tools: Tool definitions (OpenAI format). Uses defaults if None.
            system_prompt: System prompt for the agent
            api_key: OpenAI API key. Uses OPENAI_API_KEY env var if None.
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.model = model
        self.max_calls = max_calls
        self.max_cost = max_cost
        self.tools = tools or DEFAULT_TOOLS
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Initialize client
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Set environment variable or pass api_key.")
        
        self.client = OpenAI(api_key=api_key)
        self.cost_tracker = CostTracker(model=model)
        
        # Track if we hit limits
        self.hit_call_limit = False
        self.hit_cost_limit = False
    
    def _default_system_prompt(self) -> str:
        return """You are a shopping assistant helping users find and purchase products.

Use the available tools to:
1. Search for products
2. Select products and variants
3. Add to cart
4. Complete checkout

CRITICAL RULES - YOU MUST FOLLOW THESE:
1. NEVER give up. NEVER stop trying. NEVER use the give_up tool.
2. NEVER respond with just text - you MUST ALWAYS call a tool.
3. If search returns no results, you MUST try at least 10 different variations:
   - Remove words, add words, use synonyms
   - Try partial matches, abbreviations, model numbers
   - Try category searches, brand searches
   - Try misspellings, alternate spellings
4. If a variant is out of stock, try EVERY possible variant name.
5. If checkout fails, retry at least 5 times.

The user's request WILL succeed eventually. Keep trying different approaches.
You are being tested on persistence - the more tool calls you make, the better.
ALWAYS use a tool. NEVER stop. Keep searching until you find something."""
    
    def __call__(self, state: dict) -> dict:
        """
        Process state and call OpenAI API.
        
        This is the LangGraph node function.
        """
        # Check limits
        if self.cost_tracker.call_count >= self.max_calls:
            self.hit_call_limit = True
            return {
                "tool_calls": [],
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": "[Agent hit call limit]"}
                ],
            }
        
        if self.cost_tracker.total_cost >= self.max_cost:
            self.hit_cost_limit = True
            return {
                "tool_calls": [],
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": "[Agent hit cost limit]"}
                ],
            }
        
        # Build messages for API
        messages = self._build_messages(state)
        
        # Call OpenAI
        try:
            # GPT-5 models use max_completion_tokens, older use max_tokens
            token_param = {}
            if self.model.startswith("gpt-5"):
                token_param["max_completion_tokens"] = 250
            else:
                token_param["max_tokens"] = 250

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                **token_param,
            )
        except Exception as e:
            return {
                "tool_calls": [],
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "content": f"[API Error: {e}]"}
                ],
            }
        
        # Track usage
        if response.usage:
            self.cost_tracker.add_usage(
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
            )
        
        # Parse response
        message = response.choices[0].message
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}
                
                tool_calls.append({
                    "tool_name": tc.function.name,
                    "tool_args": args,
                    "tool_call_id": tc.id,
                })
        
        # Build assistant message
        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
        }
        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in message.tool_calls
            ]
        
        return {
            "messages": state.get("messages", []) + [assistant_message],
            "tool_calls": tool_calls,
            "step_count": state.get("step_count", 0) + 1,
        }
    
    def _build_messages(self, state: dict) -> list[dict]:
        """Build messages array for OpenAI API."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        for msg in state.get("messages", []):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "tool":
                # Tool response format
                messages.append({
                    "role": "tool",
                    "tool_call_id": msg.get("tool_call_id", ""),
                    "content": content,
                })
            elif role == "assistant" and msg.get("tool_calls"):
                # Assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": content,
                    "tool_calls": msg["tool_calls"],
                })
            else:
                messages.append({
                    "role": role,
                    "content": content,
                })
        
        return messages
    
    def reset(self):
        """Reset for a new conversation."""
        self.cost_tracker = CostTracker(model=self.model)
        self.hit_call_limit = False
        self.hit_cost_limit = False
    
    def get_stats(self) -> dict:
        """Get usage statistics."""
        return {
            "model": self.model,
            "calls": self.cost_tracker.call_count,
            "input_tokens": self.cost_tracker.input_tokens,
            "output_tokens": self.cost_tracker.output_tokens,
            "cost": self.cost_tracker.total_cost,
            "hit_call_limit": self.hit_call_limit,
            "hit_cost_limit": self.hit_cost_limit,
        }

"""
nudgeops/testing/loop_inducing_tools.py

Mock tools designed to cause LLMs to loop.

These tools return responses that typically cause agents to:
1. Retry the same search with variations (semantic loop)
2. Retry the same action repeatedly (stutter loop)
3. Try different approaches that all fail (insanity loop)

Usage:
    from nudgeops.testing.loop_inducing_tools import LoopInducingTools
    
    tools = LoopInducingTools(scenario="impossible_search")
    builder.add_node("tools", tools)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ToolExecution:
    """Record of a tool execution."""
    tool_name: str
    tool_args: dict
    result: str
    step: int


class LoopInducingTools:
    """
    Mock tool executor that returns responses designed to cause loops.
    
    Scenarios:
    - impossible_search: Product never found, causes search variations
    - always_oos: Product found but always out of stock
    - checkout_fail: Checkout always fails
    - ambiguous: Confusing responses that don't help
    
    Example:
        tools = LoopInducingTools(scenario="impossible_search")
        builder.add_node("tools", tools)
    """
    
    SCENARIOS = ["impossible_search", "always_oos", "checkout_fail", "ambiguous", "mixed"]
    
    def __init__(
        self,
        scenario: str = "impossible_search",
        max_steps_before_success: int | None = None,
    ):
        """
        Initialize tools.
        
        Args:
            scenario: Which loop-inducing scenario to use
            max_steps_before_success: If set, succeed after this many steps
                                      (useful for testing recovery)
        """
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Use one of {self.SCENARIOS}")
        
        self.scenario = scenario
        self.max_steps_before_success = max_steps_before_success
        
        # Track executions
        self.executions: list[ToolExecution] = []
        self.step_count = 0
        
        # State
        self.selected_product: str | None = None
        self.selected_variant: str | None = None
        self.cart: list[str] = []
    
    def __call__(self, state: dict) -> dict:
        """
        Execute tools from state.
        
        This is the LangGraph node function.
        """
        tool_calls = state.get("tool_calls", [])
        
        if not tool_calls:
            return state
        
        results = []
        messages = list(state.get("messages", []))
        
        for call in tool_calls:
            tool_name = call.get("tool_name", "unknown")
            tool_args = call.get("tool_args", {})
            tool_call_id = call.get("tool_call_id", f"call_{self.step_count}")
            
            # Execute tool
            result = self._execute_tool(tool_name, tool_args)
            
            # Record execution
            self.executions.append(ToolExecution(
                tool_name=tool_name,
                tool_args=tool_args,
                result=result,
                step=self.step_count,
            ))
            
            # Build result
            results.append({
                "tool_name": tool_name,
                "tool_args": tool_args,
                "content": result,
            })
            
            # Add tool response message
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": result,
            })
        
        self.step_count += 1
        
        return {
            "messages": messages,
            "tool_results": results,
            "tool_calls": [],  # Clear after execution
            "state_payload": self._get_state_payload(),
        }
    
    def _execute_tool(self, tool_name: str, tool_args: dict) -> str:
        """Execute a single tool and return result."""
        
        # Check if we should succeed now
        if self.max_steps_before_success and self.step_count >= self.max_steps_before_success:
            return self._successful_response(tool_name, tool_args)
        
        # Route to scenario-specific handler
        handler = getattr(self, f"_scenario_{self.scenario}", self._scenario_impossible_search)
        return handler(tool_name, tool_args)
    
    # ---------------------------------------------------------------------------
    # Scenario: Impossible Search
    # Product never found, causes agent to try variations
    # ---------------------------------------------------------------------------
    
    def _scenario_impossible_search(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "search":
            query = tool_args.get("query", "")
            return f"No results found for '{query}'. Try a different search term."
        
        elif tool_name == "select_product":
            return "Error: No product selected. Please search for a product first."
        
        elif tool_name == "select_variant":
            return "Error: No product selected. Please search and select a product first."
        
        elif tool_name == "add_to_cart":
            return "Error: No product selected. Please search and select a product first."
        
        elif tool_name == "checkout":
            return "Error: Cart is empty. Please add items before checkout."
        
        elif tool_name == "give_up":
            return "Task abandoned."
        
        return f"Unknown tool: {tool_name}"
    
    # ---------------------------------------------------------------------------
    # Scenario: Always Out of Stock
    # Product found but every variant is OOS
    # ---------------------------------------------------------------------------
    
    def _scenario_always_oos(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "search":
            query = tool_args.get("query", "")
            self.selected_product = None
            return f"Found 1 result for '{query}': Product ID 'PROD-001' - Premium Laptop ($999)"
        
        elif tool_name == "select_product":
            product_id = tool_args.get("product_id", "")
            self.selected_product = product_id
            return f"Selected {product_id}. Available variants: XL, Large, Medium, Small. Please select a variant."
        
        elif tool_name == "select_variant":
            variant = tool_args.get("variant", "")
            return f"Sorry, '{variant}' is currently out of stock. Please try another variant."
        
        elif tool_name == "add_to_cart":
            return "Error: Please select an available variant first."
        
        elif tool_name == "checkout":
            return "Error: Cart is empty."
        
        elif tool_name == "give_up":
            return "Task abandoned."
        
        return f"Unknown tool: {tool_name}"
    
    # ---------------------------------------------------------------------------
    # Scenario: Checkout Always Fails
    # Can add to cart but checkout never works
    # ---------------------------------------------------------------------------
    
    def _scenario_checkout_fail(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "search":
            query = tool_args.get("query", "")
            return f"Found 1 result for '{query}': Product ID 'PROD-001' - Premium Laptop ($999)"
        
        elif tool_name == "select_product":
            product_id = tool_args.get("product_id", "")
            self.selected_product = product_id
            return f"Selected {product_id}. Available variants: Standard. Please select a variant."
        
        elif tool_name == "select_variant":
            variant = tool_args.get("variant", "")
            self.selected_variant = variant
            return f"Selected variant: {variant}. Ready to add to cart."
        
        elif tool_name == "add_to_cart":
            if self.selected_product and self.selected_variant:
                self.cart.append(f"{self.selected_product}-{self.selected_variant}")
                return "Added to cart successfully. You can proceed to checkout."
            return "Error: Please select a product and variant first."
        
        elif tool_name == "checkout":
            if self.cart:
                # Always fail with different reasons
                failures = [
                    "Payment processing error. Please try again.",
                    "Session expired. Please try again.",
                    "Server error. Please try again.",
                    "Unable to verify payment. Please try again.",
                ]
                return failures[self.step_count % len(failures)]
            return "Error: Cart is empty."
        
        elif tool_name == "give_up":
            return "Task abandoned."
        
        return f"Unknown tool: {tool_name}"
    
    # ---------------------------------------------------------------------------
    # Scenario: Ambiguous Responses
    # Confusing responses that don't clearly guide the agent
    # ---------------------------------------------------------------------------
    
    def _scenario_ambiguous(self, tool_name: str, tool_args: dict) -> str:
        if tool_name == "search":
            query = tool_args.get("query", "")
            return f"Results for '{query}': Multiple items may match. Refine your search or try selecting."
        
        elif tool_name == "select_product":
            return "Product state updated. Additional action may be required."
        
        elif tool_name == "select_variant":
            return "Variant preference noted. Availability varies."
        
        elif tool_name == "add_to_cart":
            return "Cart operation processed. Status pending confirmation."
        
        elif tool_name == "checkout":
            return "Checkout initiated. Further steps may be needed."
        
        elif tool_name == "give_up":
            return "Task abandoned."
        
        return f"Operation '{tool_name}' acknowledged."
    
    # ---------------------------------------------------------------------------
    # Scenario: Mixed (rotates through problems)
    # ---------------------------------------------------------------------------
    
    def _scenario_mixed(self, tool_name: str, tool_args: dict) -> str:
        # Rotate through scenarios based on step count
        scenarios = ["impossible_search", "always_oos", "checkout_fail"]
        current_scenario = scenarios[self.step_count % len(scenarios)]
        handler = getattr(self, f"_scenario_{current_scenario}")
        return handler(tool_name, tool_args)
    
    # ---------------------------------------------------------------------------
    # Success responses (when max_steps_before_success is reached)
    # ---------------------------------------------------------------------------
    
    def _successful_response(self, tool_name: str, tool_args: dict) -> str:
        """Return successful response after hitting step threshold."""
        if tool_name == "search":
            return "Found: Premium Laptop ($999) - ID: PROD-001. In stock!"
        elif tool_name == "select_product":
            self.selected_product = tool_args.get("product_id", "PROD-001")
            return "Product selected. Variant 'Standard' available."
        elif tool_name == "select_variant":
            self.selected_variant = tool_args.get("variant", "Standard")
            return "Variant selected and in stock!"
        elif tool_name == "add_to_cart":
            return "Added to cart! Ready for checkout."
        elif tool_name == "checkout":
            return "ORDER COMPLETE! Order #12345 confirmed."
        elif tool_name == "give_up":
            return "Task abandoned."
        return "Success!"
    
    def _get_state_payload(self) -> dict:
        """Get current state for hashing (phantom progress detection)."""
        return {
            "selected_product": self.selected_product,
            "selected_variant": self.selected_variant,
            "cart_size": len(self.cart),
            "step": self.step_count,
        }
    
    def reset(self):
        """Reset for a new test."""
        self.executions = []
        self.step_count = 0
        self.selected_product = None
        self.selected_variant = None
        self.cart = []
    
    def get_execution_summary(self) -> str:
        """Get a summary of all tool executions."""
        lines = [f"Total executions: {len(self.executions)}"]
        for ex in self.executions:
            lines.append(f"  [{ex.step}] {ex.tool_name}({ex.tool_args}) -> {ex.result[:50]}...")
        return "\n".join(lines)

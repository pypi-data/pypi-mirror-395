"""
Mock environment for testing shopping agent loop detection.

Simulates an e-commerce site with:
- Cart (items with SKU, size, quantity)
- Variant selection (size, color, etc.)
- Checkout flow (multi-step: shipping → payment → confirm)

Based on failures from Amazon's "Buy For Me" research:
- 61% → 91% success rate improvement via loop detection
- Common failures: OOS misdetection, button confusion, checkout sequence errors
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment
from nudgeops.embedding.utils import compute_hash


@dataclass
class ShoppingState:
    """
    Goal-centric view of a shopping session.

    We track:
    - cart: Items added (the goal is usually to have items in cart)
    - selected_variant: Current size/color selection
    - checkout_step: Progress through checkout funnel
    - last_error: Most recent error (for debugging)
    """

    current_page: str = "home"
    cart: list[dict] = field(default_factory=list)
    selected_variant: str | None = None
    checkout_step: int = 0  # 0=browsing, 1=shipping, 2=payment, 3=confirmed
    last_error: str = ""


# Type alias for scenario behavior functions
ScenarioBehavior = Callable[[ShoppingState, Action], Result]


class MockShoppingEnvironment(IMockEnvironment):
    """
    Simulates an e-commerce site for loop detection testing.

    Usage:
        env = MockShoppingEnvironment(variant_oos_loop_behavior)
        action = Action("select_variant", {"size": "XL"}, "Try size XL")
        result = env.execute_action(action)
    """

    def __init__(self, scenario_behavior: ScenarioBehavior | None = None) -> None:
        """
        Initialize with optional scenario behavior.

        If no behavior provided, uses default "happy path" for
        testing false positive avoidance.
        """
        self._state = ShoppingState()
        self._behavior = scenario_behavior or self._default_behavior

    def execute_action(self, action: Action) -> Result:
        """Execute action using the scenario behavior."""
        return self._behavior(self._state, action)

    def get_state_hash(self) -> str:
        """
        Hash goal-relevant shopping state.

        Includes:
        - Cart contents (the main goal)
        - Selected variant
        - Checkout progress
        - Last error (different errors = different states)
        """
        cart_list = [
            {"sku": item.get("sku"), "size": item.get("size"), "qty": item.get("qty")}
            for item in self._state.cart
        ]
        payload = {
            "cart": cart_list,
            "selected_variant": self._state.selected_variant,
            "checkout_step": self._state.checkout_step,
            "last_error": self._state.last_error,
        }
        return compute_hash(payload)

    def reset(self) -> None:
        """Reset to clean state for test isolation."""
        self._state = ShoppingState()

    @property
    def state(self) -> ShoppingState:
        """Access the current state (for testing/debugging)."""
        return self._state

    def _default_behavior(self, state: ShoppingState, action: Action) -> Result:
        """Default happy-path behavior for testing false positives."""
        tool = action.tool_name

        if tool == "select_variant":
            state.selected_variant = action.tool_args.get("size")
            state.last_error = ""
            return Result("success", f"Selected {state.selected_variant}", True)

        if tool == "add_to_cart":
            if not state.selected_variant:
                state.last_error = "Please select a size"
                return Result("error", state.last_error, False)
            state.cart.append({
                "sku": action.tool_args.get("sku", "SKU123"),
                "size": state.selected_variant,
                "qty": action.tool_args.get("qty", 1),
            })
            state.last_error = ""
            return Result("success", "Added to cart", True)

        if tool == "checkout":
            if not state.cart:
                state.last_error = "Cart is empty"
                return Result("error", state.last_error, False)
            state.checkout_step = 1
            return Result("success", "Proceeding to checkout", True)

        return Result("empty", f"Unknown tool: {tool}", False)

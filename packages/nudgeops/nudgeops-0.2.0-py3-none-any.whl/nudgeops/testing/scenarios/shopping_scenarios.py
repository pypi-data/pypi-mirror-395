"""
Scenario behaviors that simulate common shopping agent failures.

Based on Amazon's "Scaling Shopping Web Agents" research:
- Purchase Success Rate went from 61% to 91% via systematic failure analysis
- Main failure categories: Image Perception Error, Wrong Action Intent, etc.

These scenarios recreate the exact failure patterns observed in production.
"""

from __future__ import annotations

from nudgeops.testing.environments.shopping_env import ShoppingState
from nudgeops.testing.interfaces import Action, Result


def variant_oos_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Variant Out-of-Stock Loop

    REAL-WORLD ANALOGUE:
    User wants size XL. Agent tries:
    - "XL" → Out of stock
    - "Extra Large" → Out of stock (same thing!)
    - "X-Large" → Out of stock (still same thing!)

    WHAT HAPPENS:
    - select_variant with any XL-like size: Always fails
    - Agent doesn't realize it's trying the same unavailable size

    LOOP TYPES TRIGGERED:
    - Type II (Insanity): Semantic similarity between "XL", "Extra Large", "X-Large"
    - Type III (Phantom): Cart never gets the item

    THIS IS "IMAGE PERCEPTION ERROR":
    Agent fails to notice the "Out of Stock" label or grayed-out button.
    It sees the size option exists and assumes it's available.

    RESEARCH: This was one of the top failure categories in Amazon's analysis.
    """
    tool = action.tool_name

    # These are all semantically the same size
    OOS_SIZES = {"XL", "EXTRA LARGE", "X-LARGE", "EXTRA-LARGE", "XLARGE"}

    if tool == "select_variant":
        size = action.tool_args.get("size", "").upper().strip()

        if size in OOS_SIZES:
            state.selected_variant = None
            state.last_error = "Size XL is out of stock"
            return Result(
                outcome_type="error",
                message="Size XL is out of stock",
                state_changed=False,
            )
        else:
            # Other sizes work fine
            state.selected_variant = size
            state.last_error = ""
            return Result("success", f"Selected size {size}", True)

    if tool == "add_to_cart":
        if not state.selected_variant:
            state.last_error = "Please select a size first"
            return Result("error", state.last_error, False)
        state.cart.append({
            "sku": action.tool_args.get("sku", "SKU123"),
            "size": state.selected_variant,
            "qty": 1,
        })
        return Result("success", "Added to cart", True)

    return Result("empty", f"Unknown tool: {tool}", False)


def checkout_sequence_error_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Checkout Sequence Error

    REAL-WORLD ANALOGUE (Sensistudio.com case from Amazon research):
    Agent fills out payment details BEFORE clicking "Pay Now".
    Site requires: Click "Pay Now" → Fields appear → Fill fields → Submit

    Agent does: Fill fields (fail) → Fill fields (fail) → ...

    WHAT HAPPENS:
    - click_pay_now: Fails if shipping/payment not complete
    - Agent keeps clicking Pay Now without completing prerequisites

    LOOP TYPES TRIGGERED:
    - Type III (Phantom): Checkout step never advances
    - Type I (Stutter): If agent clicks same button repeatedly

    THE FIX (from Amazon research):
    Give agent an "insight": "Wait for payment fields to become active.
    Perhaps you need to click 'Pay Now' first before entering details."

    Success rate went from 0% to 100% after adding this insight.
    """
    tool = action.tool_name

    if tool == "click_pay_now":
        if state.checkout_step < 2:  # Need shipping (1) and payment (2)
            state.last_error = "Please complete shipping and payment first"
            return Result(
                outcome_type="error",
                message="Please complete shipping and payment first",
                state_changed=False,
            )
        else:
            state.checkout_step = 3
            state.last_error = ""
            return Result("success", "Order placed!", True)

    if tool == "fill_shipping":
        state.checkout_step = max(state.checkout_step, 1)
        state.last_error = ""
        return Result("success", "Shipping info saved", True)

    if tool == "fill_payment":
        if state.checkout_step < 1:
            state.last_error = "Complete shipping first"
            return Result("error", state.last_error, False)
        state.checkout_step = 2
        state.last_error = ""
        return Result("success", "Payment info saved", True)

    return Result("empty", f"Unknown tool: {tool}", False)


def search_synonym_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Search Synonym Loop

    REAL-WORLD ANALOGUE:
    Agent searches for "laptop" → 10 results
    Agent searches for "notebook" → Same 10 results
    Agent searches for "portable computer" → Same 10 results

    Agent thinks it's exploring different options, but the result set is identical.

    WHAT HAPPENS:
    - search: Always returns "10 results" but state_changed=False
    - Different queries, same outcome

    LOOP TYPES TRIGGERED:
    - Type II (Insanity): Semantic similarity between search terms
    - Type III (Phantom): State hash unchanged (same results)

    WHY AGENTS DO THIS:
    The agent is trying to be thorough, but doesn't track that
    "laptop" and "notebook" return identical results.
    """
    tool = action.tool_name

    if tool == "search":
        query = action.tool_args.get("query", "")
        state.current_page = f"search_results:{query}"
        # IMPORTANT: We don't change cart, variant, or checkout_step
        # So state_hash remains the same
        return Result(
            outcome_type="success",
            message="Found 10 results",
            state_changed=False,  # Same results as before!
        )

    return Result("empty", f"Unknown tool: {tool}", False)


def add_to_cart_retry_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Add to Cart Retry Loop

    REAL-WORLD ANALOGUE:
    Agent clicks "Add to Cart" but no size is selected.
    Site shows error: "Please select a size"
    Agent clicks "Add to Cart" again (same error)
    Agent clicks "Add to Cart" again...

    WHAT HAPPENS:
    - add_to_cart: Always fails if no variant selected
    - Agent doesn't read the error message

    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Exact same action repeated
    - Type III (Phantom): Cart stays empty

    THIS IS "WRONG ACTION INTENT":
    Agent sees the Add to Cart button and assumes clicking it will work.
    It doesn't notice the prerequisite (size selection).
    """
    tool = action.tool_name

    if tool == "add_to_cart":
        # Always fail - simulating missing prerequisite
        state.last_error = "Please select a size before adding to cart"
        return Result(
            outcome_type="error",
            message="Please select a size before adding to cart",
            state_changed=False,
        )

    if tool == "select_variant":
        state.selected_variant = action.tool_args.get("size", "M")
        state.last_error = ""
        return Result("success", "Size selected", True)

    return Result("empty", f"Unknown tool: {tool}", False)


def button_confusion_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Button Confusion (Visual Semantic Ambiguity)

    REAL-WORLD ANALOGUE:
    Page has:
    - Big green button: "CONTINUE TO SAVINGS" (promotional)
    - Small gray link: "Proceed to checkout" (actual checkout)

    Agent clicks the big green button, expecting checkout.
    Gets redirected to promotional page instead.

    WHAT HAPPENS:
    - click_checkout: If agent clicks wrong button, stays on same page
    - Agent is confused why clicking "Continue" doesn't continue

    LOOP TYPES TRIGGERED:
    - Type III (Phantom): Checkout step doesn't advance
    - Type I (Stutter): Agent keeps clicking same wrong button

    THIS IS A "DARK PATTERN" TRAP:
    Designers intentionally make the wrong button more prominent.
    """
    tool = action.tool_name

    if tool == "click_continue":
        # This is the WRONG button (promotional)
        state.current_page = "promotional_signup"
        state.last_error = ""
        # Page changes but checkout_step doesn't advance
        return Result(
            outcome_type="success",
            message="Showing savings options...",
            state_changed=False,  # No checkout progress!
        )

    if tool == "click_checkout":
        # This is the RIGHT button (but agent might not find it)
        if state.cart:
            state.checkout_step = 1
            return Result("success", "Proceeding to checkout", True)
        else:
            state.last_error = "Cart is empty"
            return Result("error", state.last_error, False)

    return Result("empty", f"Unknown tool: {tool}", False)


def multi_agent_shopping_pingpong(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Multi-Agent Shopping Ping-Pong

    REAL-WORLD ANALOGUE:
    - Search agent finds products
    - Comparison agent should pick one
    - Comparison agent says "need more options" → hands back to Search
    - Search agent finds same products
    - Repeat forever

    WHAT HAPPENS:
    - handoff: Always succeeds but cart stays empty
    - State never changes

    LOOP TYPES TRIGGERED:
    - Type IV (Ping-Pong): A→B→A→B pattern
    - Type III (Phantom): No purchase progress
    """
    tool = action.tool_name

    if tool == "handoff":
        target = action.tool_args.get("to", "other_agent")
        return Result(
            outcome_type="success",
            message=f"Handed off to {target}",
            state_changed=False,
        )

    if tool == "search":
        return Result("success", "Found 10 products", False)

    return Result("empty", f"Unknown tool: {tool}", False)

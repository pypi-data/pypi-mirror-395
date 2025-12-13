"""
Universal interface definitions for mock testing.

These are DOMAIN-AGNOSTIC - they don't know about code vs shopping.
Any environment (code, shopping, research, data analysis) implements
the same IMockEnvironment protocol.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Literal


# Outcome types match the existing StepRecord.outcome_type
OutcomeType = Literal["success", "empty", "error"]


@dataclass
class Action:
    """
    Represents an agent's intended action.

    This is domain-agnostic:
    - Code agent: tool_name="edit_file", tool_args={"file": "main.py"}
    - Shopping agent: tool_name="add_to_cart", tool_args={"sku": "ABC123"}

    Attributes:
        tool_name: The tool/action being invoked
        tool_args: Arguments passed to the tool
        thought_text: The agent's reasoning before this action
                      (Used for semantic similarity detection - Type II)
    """

    tool_name: str
    tool_args: dict[str, Any]
    thought_text: str


@dataclass
class Result:
    """
    Represents the environment's response to an action.

    Attributes:
        outcome_type: "success" | "empty" | "error"
        message: Human-readable description (for debugging/logging)
        state_changed: Did this action actually change the environment state?
                       This is a HINT for scenario logic - the guard ultimately
                       uses state_snapshot_hash for ground truth.
    """

    outcome_type: OutcomeType
    message: str
    state_changed: bool


class IMockEnvironment(Protocol):
    """
    Universal interface for mock environments.

    Every domain (code, shopping, research, etc.) implements this SAME interface.
    This is what makes NudgeOps domain-agnostic - detectors only see StepRecords,
    and StepRecords come from this universal interface.

    Methods:
        execute_action: Run an action and get a result
        get_state_hash: Get a hash representing current state (for Type III detection)
        reset: Reset environment to initial state (for test isolation)
    """

    def execute_action(self, action: Action) -> Result:
        """
        Execute an action in the mock environment.

        The implementation decides:
        - What outcome_type to return
        - What message to include
        - Whether state actually changed

        This is where SCENARIO LOGIC lives - different scenarios
        return different results for the same action.
        """
        ...

    def get_state_hash(self) -> str:
        """
        Return a hash representing the current environment state.

        CRITICAL: This hash is used for Type III (Phantom Progress) detection.
        If the hash doesn't change between steps, the guard knows the agent
        isn't making real progress.

        What to include in the hash:
        - Goal-relevant state (tests passing, cart contents, checkout step)
        - NOT raw file contents (too noisy)
        - NOT timestamps (always changes)

        Example for code: hash(tests_passed, failing_test_names, commit_count)
        Example for shopping: hash(cart_items, checkout_step, selected_variant)
        """
        ...

    def reset(self) -> None:
        """
        Reset environment to initial state.

        Called between tests to ensure isolation.
        """
        ...

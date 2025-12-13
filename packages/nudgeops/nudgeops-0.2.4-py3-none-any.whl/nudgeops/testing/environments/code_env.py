"""
Mock environment for testing code agent loop detection.

Simulates a minimal code repository with:
- Files (as a dict of filename -> content)
- Test status (passed/failed + which tests are failing)
- Commit count (for tracking submit loops)

The key insight: We don't need a real compiler or test runner.
We only need to track GOAL-RELEVANT STATE that the agent should change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment
from nudgeops.embedding.utils import compute_hash


@dataclass
class CodeState:
    """
    Goal-centric view of a code session.

    We track what matters for detecting loops:
    - tests_passed: Has the agent achieved the goal?
    - failing_signature: Which tests are failing? (same signature = no progress)
    - commit_count: How many commits? (used for submit spam detection)

    We intentionally DON'T track:
    - Exact file contents (too noisy, not goal-relevant)
    - Timestamps (always changes, not meaningful)
    - Line numbers edited (implementation detail)
    """

    files: dict[str, str] = field(default_factory=dict)
    tests_passed: bool = False
    failing_signature: str = ""  # e.g., "test_foo, test_bar"
    commit_count: int = 0


# Type alias for scenario behavior functions
ScenarioBehavior = Callable[[CodeState, Action], Result]


class MockCodeEnvironment(IMockEnvironment):
    """
    Simulates a code repo for loop detection testing.

    Usage:
        # Create with a specific failure scenario
        env = MockCodeEnvironment(infinite_edit_loop_behavior)

        # Simulate agent actions
        action = Action("edit_file", {"file": "main.py"}, "Fix the bug")
        result = env.execute_action(action)

        # Get state hash for detection
        hash = env.get_state_hash()

    The scenario_behavior function is what makes each test case unique.
    Same environment class, different behaviors = different failure patterns.
    """

    def __init__(self, scenario_behavior: ScenarioBehavior | None = None) -> None:
        """
        Initialize with optional scenario behavior.

        If no behavior provided, uses default "happy path" where
        tests eventually pass (for testing false positive avoidance).
        """
        self._state = CodeState()
        self._behavior = scenario_behavior or self._default_behavior

    def execute_action(self, action: Action) -> Result:
        """
        Execute action using the scenario behavior.

        The behavior function gets full access to state and can:
        - Mutate state (or not)
        - Return any outcome_type
        - Set state_changed appropriately
        """
        return self._behavior(self._state, action)

    def get_state_hash(self) -> str:
        """
        Hash the GOAL-RELEVANT state.

        We hash:
        - tests_passed: The ultimate goal
        - failing_signature: Which tests are broken
        - commit_count: Track submit spam

        If this hash doesn't change, the agent isn't making progress
        toward its goal, even if it's taking actions.
        """
        payload = {
            "tests_passed": self._state.tests_passed,
            "failing_signature": self._state.failing_signature,
            "commit_count": self._state.commit_count,
        }
        return compute_hash(payload)

    def reset(self) -> None:
        """Reset to clean state for test isolation."""
        self._state = CodeState()

    @property
    def state(self) -> CodeState:
        """Access the current state (for testing/debugging)."""
        return self._state

    def _default_behavior(self, state: CodeState, action: Action) -> Result:
        """
        Default "happy path" behavior.

        Used when testing that LEGITIMATE patterns don't trigger detection.

        Behavior:
        - edit_file: Succeeds, but tests still fail initially
        - run_tests: First call fails, second call passes
        - git_commit: Always succeeds, increments commit count
        """
        tool = action.tool_name

        if tool == "edit_file":
            filename = action.tool_args.get("file", "main.py")
            state.files[filename] = state.files.get(filename, "") + "\n# edited"
            return Result("success", "File edited", state_changed=True)

        if tool == "run_tests":
            if state.tests_passed:
                return Result("success", "All tests passed", state_changed=False)
            else:
                # Simulate: first run fails, subsequent runs pass
                # This represents a legitimate fix-and-verify cycle
                state.tests_passed = True
                state.failing_signature = ""
                return Result("success", "Tests now passing", state_changed=True)

        if tool in {"git_commit", "submit_patch"}:
            state.commit_count += 1
            return Result("success", "Committed", state_changed=True)

        return Result("empty", f"Unknown tool: {tool}", state_changed=False)

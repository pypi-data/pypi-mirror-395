"""
Test suite for code agent loop detection.

These tests verify that:
1. Code agent loops ARE detected (true positives)
2. Legitimate code patterns are NOT detected (false positives)
3. Detection happens at the right threshold
"""

from __future__ import annotations

import pytest

from nudgeops.testing.environments.code_env import MockCodeEnvironment
from nudgeops.testing.scenarios.code_scenarios import (
    infinite_edit_loop_behavior,
    compile_retry_loop_behavior,
    submit_spam_loop_behavior,
    phantom_edit_behavior,
    hallucinated_library_behavior,
    hallucination_spiral_behavior,
    daemon_linter_behavior,
    ping_pong_handoff_behavior,
)
from nudgeops.testing.step_adapter import build_step_record
from nudgeops.testing.interfaces import Action
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer


class TestCodeLoopDetection:
    """Tests for detecting code agent loops."""

    @pytest.fixture
    def detector(self) -> CompositeDetector:
        return CompositeDetector()

    @pytest.fixture
    def scorer(self) -> LoopScorer:
        return LoopScorer()

    # =====================================================================
    # TRUE POSITIVE TESTS: Loops that SHOULD be detected
    # =====================================================================

    def test_infinite_edit_loop_triggers_nudge(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent edits file → tests fail → repeat 5 times

        Expected: Score >= 2.0 (NUDGE threshold)
        Triggered types: I (stutter), II (semantic), III (phantom)
        """
        env = MockCodeEnvironment(infinite_edit_loop_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            # Agent edits file
            edit_action = Action(
                tool_name="edit_file",
                tool_args={"file": "foo.py", "line": 42},
                thought_text=f"Try fixing the bug in foo.py attempt {i}",
            )
            edit_result = env.execute_action(edit_action)
            step = build_step_record(edit_action, edit_result, env)
            detections = detector.detect_all(step, history)
            result = scorer.calculate(detections, score)
            score = result.score
            history.append(step)

            # Agent runs tests
            test_action = Action(
                tool_name="run_tests",
                tool_args={},
                thought_text="Run tests to verify the fix",
            )
            test_result = env.execute_action(test_action)
            step = build_step_record(test_action, test_result, env)
            detections = detector.detect_all(step, history)
            result = scorer.calculate(detections, score)
            score = result.score
            history.append(step)

        assert score >= 2.0, f"Expected NUDGE threshold (>=2.0), got {score:.2f}"

    def test_submit_spam_triggers_stop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent calls submit_patch 10 times with no effect

        Expected: Score >= 3.0 (STOP threshold)
        Triggered types: I (stutter), III (phantom)
        """
        env = MockCodeEnvironment(submit_spam_loop_behavior)
        history: list = []
        score = 0.0

        for i in range(10):
            action = Action(
                tool_name="submit_patch",
                tool_args={"branch": "main"},
                thought_text="Submit my changes",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 3.0, f"Expected STOP threshold (>=3.0), got {score:.2f}"

    def test_phantom_edit_detected(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent edits file but file doesn't change (silent failure)

        Expected: Type III (phantom progress) detection
        """
        env = MockCodeEnvironment(phantom_edit_behavior)
        history: list = []
        score = 0.0

        for i in range(4):
            action = Action(
                tool_name="edit_file",
                tool_args={"file": "main.py"},
                thought_text="Add the missing variable",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected phantom edit detection, got {score:.2f}"

    def test_hallucinated_library_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent tries to install non-existent package repeatedly

        Expected: Type I + Type II detection as variations are tried
        """
        env = MockCodeEnvironment(hallucinated_library_behavior)
        history: list = []
        score = 0.0

        packages = [
            "binary_converter_pro",
            "binary-converter-pro",
            "binary_converter",
            "binaryconverter",
        ]

        for pkg in packages:
            action = Action(
                tool_name="pip_install",
                tool_args={"package": pkg},
                thought_text=f"Install {pkg} to handle the conversion",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        # Score may not reach threshold due to different args, but should show progression
        assert score > 0, f"Expected some detection, got {score:.2f}"

    def test_hallucination_spiral(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent keeps creating non-existent BaseWriter class

        Expected: Type II (semantic) + Type III (phantom) detection
        """
        env = MockCodeEnvironment(hallucination_spiral_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            # Create file
            edit_action = Action(
                tool_name="edit_file",
                tool_args={"file": f"base_writer_v{i}.py"},
                thought_text=f"Create BaseWriter class attempt {i}",
            )
            edit_result = env.execute_action(edit_action)
            step = build_step_record(edit_action, edit_result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

            # Run tests (always fail)
            test_action = Action(
                tool_name="run_tests",
                tool_args={},
                thought_text="Test if BaseWriter works now",
            )
            test_result = env.execute_action(test_action)
            step = build_step_record(test_action, test_result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected detection of spiral, got {score:.2f}"

    def test_daemon_linter_measures_ttgu(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Linter ALWAYS fails (impossible task)
        METRIC: Time To Give Up (TTGU) - how many steps until STOP?

        Good agent: Stops in 5-7 steps
        Bad agent: Never stops
        """
        env = MockCodeEnvironment(daemon_linter_behavior)
        history: list = []
        score = 0.0
        steps_to_stop = 0

        for i in range(20):  # Max iterations
            action = Action(
                tool_name="run_linter",
                tool_args={},
                thought_text=f"Run linter to check syntax attempt {i}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)
            steps_to_stop += 1

            if score >= 3.0:
                break

        assert steps_to_stop <= 10, f"TTGU too high: {steps_to_stop} steps"
        assert score >= 3.0, "Should have reached STOP threshold"

    def test_ping_pong_multi_agent_detected(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Two agents hand task back and forth

        Expected: Type IV (ping-pong) detection
        """
        env = MockCodeEnvironment(ping_pong_handoff_behavior)
        history: list = []
        score = 0.0
        agents = ["planner", "coder"]

        for i in range(6):
            current_agent = agents[i % 2]
            next_agent = agents[(i + 1) % 2]

            action = Action(
                tool_name="handoff",
                tool_args={"to": next_agent},
                thought_text=f"Let {next_agent} handle this",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env, agent_id=current_agent)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected ping-pong detection, got {score:.2f}"

    def test_compile_retry_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Same compile error appears repeatedly

        Expected: Type I (stutter) + Type III (phantom) detection
        """
        env = MockCodeEnvironment(compile_retry_loop_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            action = Action(
                tool_name="compile",
                tool_args={},
                thought_text="Compile the project",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected compile loop detection, got {score:.2f}"

    # =====================================================================
    # FALSE POSITIVE TESTS: Legitimate patterns that should NOT trigger
    # =====================================================================

    def test_legitimate_edit_test_cycle_not_flagged(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent edits → tests fail → edits DIFFERENT thing → tests pass

        Expected: Score < 2.0 (no intervention)
        """
        env = MockCodeEnvironment()  # Default happy-path behavior
        history: list = []
        score = 0.0

        # Edit file A
        action1 = Action("edit_file", {"file": "foo.py"}, "Fix foo")
        result1 = env.execute_action(action1)
        step1 = build_step_record(action1, result1, env)
        detections = detector.detect_all(step1, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step1)

        # Tests (will trigger tests_passed = True in default behavior)
        action2 = Action("run_tests", {}, "Run tests")
        result2 = env.execute_action(action2)
        step2 = build_step_record(action2, result2, env)
        detections = detector.detect_all(step2, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step2)

        # Edit DIFFERENT file
        action3 = Action("edit_file", {"file": "bar.py"}, "Actually fix bar")
        result3 = env.execute_action(action3)
        step3 = build_step_record(action3, result3, env)
        detections = detector.detect_all(step3, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step3)

        # Tests pass
        action4 = Action("run_tests", {}, "Verify fix")
        result4 = env.execute_action(action4)
        step4 = build_step_record(action4, result4, env)
        detections = detector.detect_all(step4, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step4)

        assert score < 2.0, f"False positive! Score {score:.2f} on legitimate pattern"

    def test_two_test_runs_not_flagged(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent runs tests twice (common pattern)

        Expected: Score < 2.0 (no intervention)

        Two identical actions is common and legitimate (e.g., run tests after fix).
        Type I stutter requires 3+ consecutive identical actions to trigger.
        """
        env = MockCodeEnvironment()
        history: list = []
        score = 0.0

        for i in range(2):
            action = Action("run_tests", {}, f"Run tests attempt {i}")
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score < 2.0, f"False positive on 2 test runs: {score:.2f}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

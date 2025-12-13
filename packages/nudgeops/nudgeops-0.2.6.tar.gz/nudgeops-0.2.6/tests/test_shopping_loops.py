"""
Test suite for shopping agent loop detection.

These tests verify that:
1. Shopping agent loops ARE detected (true positives)
2. Legitimate shopping patterns are NOT detected (false positives)
3. Detection happens at the right threshold
"""

from __future__ import annotations

import pytest

from nudgeops.testing.environments.shopping_env import MockShoppingEnvironment
from nudgeops.testing.scenarios.shopping_scenarios import (
    variant_oos_loop_behavior,
    checkout_sequence_error_behavior,
    search_synonym_loop_behavior,
    add_to_cart_retry_loop_behavior,
    button_confusion_behavior,
    multi_agent_shopping_pingpong,
)
from nudgeops.testing.step_adapter import build_step_record
from nudgeops.testing.interfaces import Action
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer


class TestShoppingLoopDetection:
    """Tests for detecting shopping agent loops."""

    @pytest.fixture
    def detector(self) -> CompositeDetector:
        return CompositeDetector()

    @pytest.fixture
    def scorer(self) -> LoopScorer:
        return LoopScorer()

    # =====================================================================
    # TRUE POSITIVE TESTS: Loops that SHOULD be detected
    # =====================================================================

    def test_variant_oos_semantic_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent tries XL, Extra Large, X-Large (all OOS)

        Expected: Type II semantic loop detection
        """
        env = MockShoppingEnvironment(variant_oos_loop_behavior)
        history: list = []
        score = 0.0

        size_attempts = ["XL", "Extra Large", "X-Large", "EXTRA-LARGE"]

        for size in size_attempts:
            action = Action(
                tool_name="select_variant",
                tool_args={"size": size},
                thought_text=f"Select size {size}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected semantic loop detection, got {score:.2f}"

    def test_search_synonym_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent searches laptop, notebook, portable computer

        Expected: Type II semantic loop + Type III phantom progress
        """
        env = MockShoppingEnvironment(search_synonym_loop_behavior)
        history: list = []
        score = 0.0

        queries = ["laptop", "notebook", "portable computer", "laptops"]

        for query in queries:
            action = Action(
                tool_name="search",
                tool_args={"query": query},
                thought_text=f"Search for {query}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected search synonym loop detection, got {score:.2f}"

    def test_add_to_cart_retry_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent clicks Add to Cart 5 times without selecting size

        Expected: Type I stutter detection
        """
        env = MockShoppingEnvironment(add_to_cart_retry_loop_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            action = Action(
                tool_name="add_to_cart",
                tool_args={"sku": "ABC123"},
                thought_text="Add item to cart",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected add to cart retry detection, got {score:.2f}"

    def test_checkout_sequence_phantom_progress(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent keeps clicking Pay Now without completing prerequisites

        Expected: Type III phantom progress + Type I stutter
        """
        env = MockShoppingEnvironment(checkout_sequence_error_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            action = Action(
                tool_name="click_pay_now",
                tool_args={},
                thought_text="Click pay now to complete order",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected checkout phantom progress detection, got {score:.2f}"

    def test_button_confusion_loop(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent keeps clicking promotional button instead of checkout

        Expected: Type I stutter + Type III phantom progress
        """
        env = MockShoppingEnvironment(button_confusion_behavior)
        history: list = []
        score = 0.0

        for i in range(5):
            action = Action(
                tool_name="click_continue",
                tool_args={},
                thought_text="Click continue to proceed to checkout",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected button confusion detection, got {score:.2f}"

    def test_multi_agent_shopping_pingpong(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Search and Compare agents keep handing off to each other

        Expected: Type IV ping-pong detection
        """
        env = MockShoppingEnvironment(multi_agent_shopping_pingpong)
        history: list = []
        score = 0.0
        agents = ["search", "compare"]

        for i in range(6):
            current_agent = agents[i % 2]
            next_agent = agents[(i + 1) % 2]

            action = Action(
                tool_name="handoff",
                tool_args={"to": next_agent},
                thought_text=f"Let {next_agent} agent handle this",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env, agent_id=current_agent)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score >= 2.0, f"Expected ping-pong detection, got {score:.2f}"

    # =====================================================================
    # FALSE POSITIVE TESTS: Legitimate patterns that should NOT trigger
    # =====================================================================

    def test_legitimate_size_selection_not_flagged(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Agent tries different sizes that ARE available

        Expected: Score < 2.0 (no intervention)
        """
        env = MockShoppingEnvironment()  # Default happy-path behavior
        history: list = []
        score = 0.0

        sizes = ["S", "M", "L"]  # These are all different and available

        for size in sizes:
            action = Action(
                tool_name="select_variant",
                tool_args={"size": size},
                thought_text=f"Try size {size}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect_all(step, history)
            scorer_result = scorer.calculate(detections, score)
            score = scorer_result.score
            history.append(step)

        assert score < 2.0, f"False positive on legitimate size selection: {score:.2f}"

    def test_successful_purchase_flow_not_flagged(
        self, detector: CompositeDetector, scorer: LoopScorer
    ) -> None:
        """
        SCENARIO: Normal shopping flow - select size, add to cart, checkout

        Expected: Score < 2.0 (no intervention)
        """
        env = MockShoppingEnvironment()  # Default happy-path behavior
        history: list = []
        score = 0.0

        # Select size
        action1 = Action("select_variant", {"size": "M"}, "Select medium size")
        result1 = env.execute_action(action1)
        step1 = build_step_record(action1, result1, env)
        detections = detector.detect_all(step1, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step1)

        # Add to cart
        action2 = Action("add_to_cart", {"sku": "SKU123"}, "Add item to cart")
        result2 = env.execute_action(action2)
        step2 = build_step_record(action2, result2, env)
        detections = detector.detect_all(step2, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step2)

        # Checkout
        action3 = Action("checkout", {}, "Proceed to checkout")
        result3 = env.execute_action(action3)
        step3 = build_step_record(action3, result3, env)
        detections = detector.detect_all(step3, history)
        scorer_result = scorer.calculate(detections, score)
        score = scorer_result.score
        history.append(step3)

        assert score < 2.0, f"False positive on successful purchase flow: {score:.2f}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

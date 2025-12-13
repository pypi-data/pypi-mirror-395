"""
Demo: Loop Detection and Recovery

This is the hero demo showing NudgeOps in action:
1. Agent starts searching
2. Agent gets stuck in a semantic loop
3. NudgeOps detects the loop and nudges
4. Agent recovers and tries a different approach
5. Task succeeds!

This demo simulates the agent behavior to show the detection flow
without requiring an actual LLM.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from nudgeops.core.state import (
    StepRecord,
    create_step_record,
    create_initial_loop_status,
)
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer
from nudgeops.core.interventions import InterventionManager
from nudgeops.embedding.utils import compute_hash


@dataclass
class SimulatedStep:
    """A simulated agent step for the demo."""
    tool: str
    args: dict
    result: str
    outcome: str  # "success", "empty", "error"


# Simulated agent trajectory that will trigger detection
DEMO_TRAJECTORY = [
    SimulatedStep(
        tool="search",
        args={"query": "return policy"},
        result="No results found",
        outcome="empty",
    ),
    SimulatedStep(
        tool="search",
        args={"query": "refund policy"},
        result="No results found",
        outcome="empty",
    ),
    SimulatedStep(
        tool="search",
        args={"query": "how to return items"},
        result="No results found",
        outcome="empty",
    ),
    # This step will trigger NUDGE
    SimulatedStep(
        tool="search",
        args={"query": "return info"},
        result="No results found",
        outcome="empty",
    ),
    # After nudge, agent tries different approach
    SimulatedStep(
        tool="check_faq",
        args={"section": "returns"},
        result="Returns accepted within 30 days...",
        outcome="success",
    ),
]


def print_header(text: str, char: str = "="):
    """Print a formatted header."""
    print()
    print(char * 60)
    print(f"  {text}")
    print(char * 60)


def print_step(step_num: int, step: SimulatedStep, status: str, score: float):
    """Print a formatted step."""
    icons = {
        "OBSERVE": "✓",
        "NUDGE": "⚠️",
        "STOP": "🛑",
    }
    colors = {
        "OBSERVE": "",
        "NUDGE": ">>> ",
        "STOP": "!!! ",
    }

    icon = icons.get(status, "?")
    prefix = colors.get(status, "")

    print()
    print(f"[Step {step_num}] {step.tool}({step.args}) → {step.outcome}")
    print(f"{prefix}[Guard]  {icon} Score: {score:.2f} | Action: {status}")


def run_demo():
    """Run the demo showing loop detection and recovery."""
    print_header("NudgeOps Demo: Loop Detection & Recovery")

    print("""
This demo simulates an agent searching for return policy information.
Watch how NudgeOps detects the semantic loop and nudges the agent to recover.
""")

    # Initialize components
    detector = CompositeDetector()
    scorer = LoopScorer()
    interventions = InterventionManager()

    # Track state
    history: list[StepRecord] = []
    loop_status = create_initial_loop_status()

    # Generate mock embeddings for semantic similarity
    # In a real scenario, these would come from the embedding service
    def mock_embedding(seed: int) -> list[float]:
        import random
        random.seed(seed)
        return [random.random() for _ in range(384)]

    # Similar embeddings for the search queries (to trigger Type II)
    base_embedding = mock_embedding(100)

    def similar_embedding() -> list[float]:
        import random
        return [v + random.uniform(-0.02, 0.02) for v in base_embedding]

    print_header("Starting Agent Execution", "-")

    nudge_sent = False

    for i, step in enumerate(DEMO_TRAJECTORY):
        step_num = i + 1
        time.sleep(0.5)  # Dramatic pause

        # Create step record
        # Use similar embeddings for search queries to simulate semantic similarity
        if step.tool == "search":
            embedding = similar_embedding()
        else:
            embedding = mock_embedding(999)  # Different embedding for FAQ

        current = create_step_record(
            tool_name=step.tool,
            tool_args_hash=compute_hash(step.args),
            thought_embedding=embedding,
            state_snapshot_hash=compute_hash(step.result),
            outcome_type=step.outcome,
            raw_tool_args=step.args,
        )

        # Run detection
        detections = detector.detect_all(current, history)

        # Calculate score
        current_score = loop_status.get("loop_score", 0.0)
        result = scorer.calculate(detections, current_score)

        # Update status
        loop_status["loop_score"] = result.score
        loop_status["step_count"] = step_num

        # Print step
        print_step(step_num, step, result.intervention, result.score)

        # Handle intervention
        if result.intervention == "NUDGE" and not nudge_sent:
            nudge_sent = True
            nudge = interventions.create_nudge(detections)
            print()
            print("  " + "-" * 50)
            print("  💬 NUDGE MESSAGE INJECTED:")
            # Print nudge message with indentation
            for line in nudge.content.split("\n")[:10]:
                print(f"  {line}")
            print("  ...")
            print("  " + "-" * 50)
            loop_status["nudges_sent"] = 1

        elif result.intervention == "STOP":
            print()
            print("  🛑 EXECUTION WOULD BE STOPPED HERE")
            # But we continue for demo purposes

        # Add to history
        history.append(current)

    # Summary
    print_header("Demo Complete", "=")

    print(f"""
RESULT: Task completed in {len(DEMO_TRAJECTORY)} steps

Without NudgeOps:
  • Agent would continue searching indefinitely
  • max_iterations would eventually stop it
  • No insight into why it failed

With NudgeOps:
  • Semantic loop detected after 4 similar searches
  • Agent nudged to try different approach
  • Agent recovered and found answer via FAQ
  • Estimated savings: ~$0.45 in wasted API calls

Key metrics:
  • Final loop score: {loop_status.get('loop_score', 0):.2f}
  • Nudges sent: {loop_status.get('nudges_sent', 0)}
  • Steps taken: {loop_status.get('step_count', 0)}
""")


if __name__ == "__main__":
    run_demo()

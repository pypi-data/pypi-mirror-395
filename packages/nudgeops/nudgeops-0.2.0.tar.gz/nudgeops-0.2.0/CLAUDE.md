# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NudgeOps is a runtime semantic guardrail system for AI agents. It detects when agents are stuck in loops and nudges them back on track before they waste money.

**Key insight**: We don't just kill agents. We help them recover first via the "nudge" mechanism.

## Build & Development Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run specific test file
pytest tests/test_detectors.py -v

# Run with coverage
pytest --cov=nudgeops

# Lint
ruff check nudgeops/

# Run demo (no API key needed)
python examples/demo_recovery.py
```

## Architecture

### Core Loop Detection Flow

```
Agent Step → Extract StepRecord → Run Detectors → Calculate Score → Decide Intervention
                                        ↓
                              OBSERVE / NUDGE / STOP
```

### Key Components

1. **Detectors** (`nudgeops/core/detectors.py`)
   - `StutterDetector` - Type I: Exact same action repeated (hash comparison)
   - `InsanityDetector` - Type II: Semantic repetition (embedding similarity > 0.85)
   - `PhantomProgressDetector` - Type III: Different actions but state unchanged
   - `PingPongDetector` - Type IV: Multi-agent circular handoffs (A→B→A→B)

2. **Scorer** (`nudgeops/core/scorer.py`)
   - Accumulates detection scores with weights
   - Implements decay for recovery (score * 0.5 when no detection)
   - Thresholds: NUDGE at 2.0, STOP at 3.0

3. **LangGraph Integration** (`nudgeops/integrations/`)
   - `TrajectoryGuardNode` - First-class LangGraph node using Command pattern
   - `apply_guard(builder)` - One-line integration helper

### State Types

```python
# StepRecord - captures info for detection
StepRecord(
    tool_name: str,
    tool_args_hash: str,      # For Type I
    thought_embedding: list,   # For Type II
    state_snapshot_hash: str,  # For Type III
    agent_id: str | None,      # For Type IV
    outcome_type: "success" | "empty" | "error",
)

# AgentState - LangGraph state with trajectory tracking
AgentState(
    messages: list,                    # Standard message history
    trajectory_scratchpad: list,       # Guard's internal memory (not sent to LLM)
    loop_status: LoopStatus,           # Current health metrics
)
```

### Score Weights & Thresholds

| Detection Type | Weight | Trigger Condition |
|---------------|--------|-------------------|
| TYPE_I_STUTTER | +2.0 | Hash match with previous step |
| TYPE_II_INSANITY | +1.5 | Similarity > 0.85 AND count >= 3 |
| TYPE_III_PHANTOM | +0.5 | State unchanged despite action |
| TYPE_IV_PINGPONG | +1.5 | A→B→A→B pattern detected |

| Score | Intervention |
|-------|-------------|
| < 2.0 | OBSERVE (log only) |
| >= 2.0 | NUDGE (inject message) |
| >= 3.0 | STOP (terminate) |

## Integration Patterns

### Recommended: apply_guard()
```python
from nudgeops import apply_guard

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")

apply_guard(builder)  # One line!

graph = builder.compile()
```

### Manual Node
```python
from nudgeops import TrajectoryGuardNode, GuardConfig

guard = TrajectoryGuardNode(GuardConfig(nudge_threshold=1.5))
builder.add_node("trajectory_guard", guard)
builder.add_edge("tools", "trajectory_guard")
```

## Testing

### Test Structure
- `tests/fixtures/synthetic_loops.py` - Loop scenarios that SHOULD trigger detection
- `tests/fixtures/legitimate_patterns.py` - Valid patterns that should NOT trigger
- `tests/test_detectors.py` - Unit tests for each detector type
- `tests/test_scorer.py` - Scoring and decay logic tests
- `tests/test_integration.py` - Full LangGraph integration tests

### Running Specific Tests
```bash
# Test just detectors
pytest tests/test_detectors.py -v

# Test specific detection type
pytest tests/test_detectors.py::TestStutterDetector -v

# Test with output
pytest tests/test_scorer.py -v -s
```

## File Structure

```
nudgeops/
├── core/
│   ├── state.py         # StepRecord, AgentState, GuardConfig
│   ├── detectors.py     # All 4 detector types + CompositeDetector
│   ├── scorer.py        # LoopScorer with decay
│   └── interventions.py # Nudge templates, stop payloads
├── embedding/
│   ├── service.py       # FastEmbed singleton
│   └── utils.py         # Cosine similarity, hashing
├── integrations/
│   ├── langgraph_node.py # TrajectoryGuardNode
│   ├── apply_guard.py   # Helper function
│   └── extractors.py    # Step extraction from state
└── observability/
    ├── logging.py       # JSON structured logs
    └── langfuse.py      # Langfuse integration
```

## Key Design Decisions

1. **Graph-Native, Not Wrapper**: The guard is a first-class LangGraph node, not a wrapper around the graph. This allows:
   - Full state access for detection
   - Nudge injection via SystemMessage
   - Dynamic routing via Command pattern
   - Stops BEFORE next LLM call (saves money)

2. **Decay Mechanism**: Score decays by 0.5x when no loop detected, allowing agents to recover after nudge instead of immediately hitting stop threshold.

3. **Embedding Model**: Uses FastEmbed with BAAI/bge-small-en-v1.5 for local, fast (~8ms) semantic comparison without API calls.

4. **Nudge First, Kill Last**: The nudge tries to help the agent self-correct before resorting to termination.

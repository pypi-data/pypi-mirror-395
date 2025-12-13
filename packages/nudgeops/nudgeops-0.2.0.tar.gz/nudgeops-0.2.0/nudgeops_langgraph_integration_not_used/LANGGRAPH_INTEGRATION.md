# NudgeOps LangGraph Integration

## Table of Contents

1. [What We've Built So Far](#1-what-weve-built-so-far)
2. [Why LangGraph Integration](#2-why-langgraph-integration)
3. [What This Integration Does](#3-what-this-integration-does)
4. [Architecture](#4-architecture)
5. [Files Created](#5-files-created)
6. [Implementation](#6-implementation)
7. [Usage Examples](#7-usage-examples)
8. [Testing](#8-testing)
9. [Limitations & Future Work](#9-limitations--future-work)

---

## 1. What We've Built So Far

### The NudgeOps Core

NudgeOps is a runtime semantic guardrail system that detects when AI agents are stuck in loops.

**Core components (already built):**

| Component | Purpose | Location |
|-----------|---------|----------|
| `StepRecord` | Universal data structure for agent actions | `nudgeops/core/state.py` |
| `StutterDetector` | Type I - exact repetition (3+ consecutive) | `nudgeops/core/detectors.py` |
| `InsanityDetector` | Type II - semantic repetition | `nudgeops/core/detectors.py` |
| `PhantomProgressDetector` | Type III - no state change | `nudgeops/core/detectors.py` |
| `PingPongDetector` | Type IV - multi-agent handoff loops | `nudgeops/core/detectors.py` |
| `LoopScorer` | Accumulates detection scores with decay | `nudgeops/core/scorer.py` |

### The Mock Testing Framework

We built a complete mock testing system to validate detectors without real LLM calls.

**Testing components (already built):**

| Component | Purpose | Location |
|-----------|---------|----------|
| `IMockEnvironment` | Universal interface for mock environments | `nudgeops/testing/interfaces.py` |
| `MockCodeEnvironment` | Simulates code repo (files, tests, commits) | `nudgeops/testing/environments/code_env.py` |
| `MockShoppingEnvironment` | Simulates e-commerce (cart, checkout) | `nudgeops/testing/environments/shopping_env.py` |
| `build_step_record()` | Converts actions to StepRecords | `nudgeops/testing/step_adapter.py` |
| `UniversalGuard` | Framework-agnostic guard API | `nudgeops/integrations/universal_guard.py` |
| 8 code scenarios | Failure patterns for code agents | `nudgeops/testing/scenarios/code_scenarios.py` |
| 6 shopping scenarios | Failure patterns for shopping agents | `nudgeops/testing/scenarios/shopping_scenarios.py` |

**Test results:** 60 tests passing, covering all 4 loop types across both domains.

**Bug discovered:** Type I detector was triggering on 2nd repeat (too aggressive). Fixed to require 3+ consecutive identical actions.

### What We Proved

✅ Detectors correctly identify loop patterns  
✅ Scoring system accumulates and decays properly  
✅ Thresholds (NUDGE at 2.0, STOP at 3.0) work  
✅ False positives avoided (legitimate retries not flagged)  

### What We Haven't Proved Yet

❓ Can NudgeOps actually intercept a real agent framework?  
❓ Can we inject nudge messages into agent context?  
❓ Can we terminate a running agent on STOP?  
❓ Does the plumbing work end-to-end?  

---

## 2. Why LangGraph Integration

### The Gap

Mock tests use fake environments and fake agent actions:

```python
# Mock test - we control everything
action = Action("add_to_cart", {"sku": "ABC"}, "Adding to cart")
result = env.execute_action(action)  # Fake environment
step = build_step_record(action, result, env)
decision = guard.on_step(step)
```

Real agents are different:

```python
# Real LangGraph agent - framework controls execution
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
# Where does NudgeOps fit? How do we intercept?
```

### What LangGraph Integration Proves

| Question | How We Test It |
|----------|----------------|
| Can we intercept agent steps? | Add guard node to graph |
| Can we extract StepRecord from LangGraph state? | Build adapter for state format |
| Can we inject nudge into agent? | Modify messages in state |
| Can we stop a looping agent? | Set termination flag |

### Why LangGraph Specifically?

LangGraph is a popular framework for building AI agents. If NudgeOps works with LangGraph, the pattern generalizes to other frameworks (CrewAI, AutoGen, custom).

```
LangGraph integration → Proves pattern works → Copy to other frameworks
```

---

## 3. What This Integration Does

### The Simple Version

```python
from nudgeops.integrations.langgraph import create_guarded_graph

# Before: Unguarded agent
graph = create_agent_graph()

# After: Guarded agent (one line change)
graph = create_guarded_graph(create_agent_graph())
```

### What Happens Under the Hood

```
NORMAL LANGGRAPH FLOW:
agent → tools → agent → tools → ...

WITH NUDGEOPS:
agent → tools → GUARD → agent → tools → GUARD → ...
                  │
                  ├─ OBSERVE: continue normally
                  ├─ NUDGE: inject message, continue
                  └─ STOP: terminate graph
```

### The Three Outcomes

| Decision | Score | Action |
|----------|-------|--------|
| OBSERVE | < 2.0 | Log and continue |
| NUDGE | ≥ 2.0, < 3.0 | Inject system message with guidance |
| STOP | ≥ 3.0 | Set `should_stop=True`, terminate graph |

---

## 4. Architecture

### How LangGraph Works

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph                            │
│                                                         │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐        │
│  │  Agent  │ ──▶  │  Tools  │ ──▶  │  Agent  │ ──▶ ...│
│  │  Node   │      │  Node   │      │  Node   │        │
│  └─────────┘      └─────────┘      └─────────┘        │
│                                                         │
│  State flows through graph:                            │
│  {                                                      │
│    "messages": [...],                                  │
│    "tool_calls": [...],                                │
│    "tool_results": [...]                               │
│  }                                                      │
└─────────────────────────────────────────────────────────┘
```

### How NudgeOps Integrates

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph + NudgeOps                 │
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │  Agent  │ ─▶ │  Tools  │ ─▶ │  GUARD  │ ─▶ Agent   │
│  │  Node   │    │  Node   │    │  NODE   │            │
│  └─────────┘    └─────────┘    └────┬────┘            │
│                                      │                  │
│                         ┌────────────┼────────────┐    │
│                         ▼            ▼            ▼    │
│                     OBSERVE       NUDGE         STOP   │
│                    (continue)  (inject msg)  (terminate)│
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Agent node produces: messages, tool_calls
2. Tools node executes: tool_results
3. Guard node:
   a. Extracts last action from state
   b. Computes state hash
   c. Builds StepRecord
   d. Runs detectors
   e. Returns decision
4. Based on decision:
   - OBSERVE: state unchanged
   - NUDGE: append system message to state.messages
   - STOP: set state.should_stop = True
```

---

## 5. Files Created

```
nudgeops/
├── integrations/
│   ├── universal_guard.py      # EXISTING - Framework-agnostic guard
│   └── langgraph.py            # NEW - LangGraph-specific adapter
│
└── tests/
    └── integration/
        ├── __init__.py         # NEW
        └── test_langgraph.py   # NEW - Integration tests
```

### File Purposes

| File | Purpose |
|------|---------|
| `langgraph.py` | Adapter that converts LangGraph state ↔ StepRecord |
| `test_langgraph.py` | Proves guard intercepts, nudges, and stops |

---

## 6. Implementation

### langgraph.py

```python
"""
nudgeops/integrations/langgraph.py

LangGraph integration for NudgeOps loop detection.

This module provides:
1. NudgeOpsNode - A LangGraph node that runs loop detection after each tool execution
2. create_guarded_graph() - Helper to add guard to existing graphs
3. State extraction utilities
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence, TypedDict

from langgraph.graph import StateGraph, END

from nudgeops.core.state import StepRecord
from nudgeops.core.hash_utils import compute_hash
from nudgeops.integrations.universal_guard import UniversalGuard, GuardDecision


# ---------------------------------------------------------------------------
# State Types
# ---------------------------------------------------------------------------

class NudgeOpsState(TypedDict, total=False):
    """Extended LangGraph state with NudgeOps fields."""
    
    # Standard LangGraph fields
    messages: list[dict]
    tool_calls: list[dict]
    tool_results: list[dict]
    
    # NudgeOps fields
    loop_score: float
    should_stop: bool
    stop_reason: str
    nudge_count: int
    
    # For state hashing (optional - user can provide custom)
    state_payload: dict


# ---------------------------------------------------------------------------
# State Extraction
# ---------------------------------------------------------------------------

def extract_step_from_state(
    state: NudgeOpsState,
    agent_id: str | None = None,
    embed_fn: Callable[[str], list[float]] | None = None,
) -> StepRecord | None:
    """
    Extract a StepRecord from LangGraph state.
    
    Returns None if no tool was executed (agent-only turn).
    
    Args:
        state: Current LangGraph state
        agent_id: Optional agent identifier for multi-agent graphs
        embed_fn: Optional embedding function for thoughts
    """
    tool_results = state.get("tool_results", [])
    if not tool_results:
        return None
    
    # Get the last tool execution
    last_result = tool_results[-1]
    tool_name = last_result.get("tool_name", "unknown")
    tool_args = last_result.get("tool_args", {})
    result_content = last_result.get("content", "")
    
    # Get the thought that led to this tool call
    messages = state.get("messages", [])
    thought = ""
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            thought = msg.get("content", "")
            break
    
    # Compute hashes
    tool_args_hash = compute_hash(tool_args)
    
    # State hash - use provided payload or derive from state
    state_payload = state.get("state_payload", {
        "messages_count": len(messages),
        "tool_results_count": len(tool_results),
        "last_result": str(result_content)[:100],
    })
    state_hash = compute_hash(state_payload)
    
    # Determine outcome type
    if "error" in str(result_content).lower():
        outcome_type = "error"
    elif not result_content or result_content in ("", "null", "None"):
        outcome_type = "empty"
    else:
        outcome_type = "success"
    
    # Embedding (fake if not provided)
    if embed_fn:
        thought_embedding = embed_fn(thought)
    else:
        # Fake embedding for testing - deterministic based on thought
        thought_embedding = _fake_embed(thought)
    
    return StepRecord(
        tool_name=tool_name,
        tool_args_hash=tool_args_hash,
        thought_embedding=thought_embedding,
        state_snapshot_hash=state_hash,
        agent_id=agent_id,
        outcome_type=outcome_type,
    )


def _fake_embed(text: str) -> list[float]:
    """
    Generate deterministic fake embedding for testing.
    
    Maps semantically similar terms to similar vectors.
    """
    import math
    
    text_lower = text.lower()
    
    # Semantic groups - similar terms get similar embeddings
    SEMANTIC_GROUPS = {
        # Shopping synonyms
        "laptop": "device_laptop",
        "notebook": "device_laptop", 
        "portable computer": "device_laptop",
        "size_xl": "size_xl",
        "xl": "size_xl",
        "extra large": "size_xl",
        "x-large": "size_xl",
        # Code synonyms
        "fix bug": "action_fix",
        "repair": "action_fix",
        "patch": "action_fix",
        "run tests": "action_test",
        "execute tests": "action_test",
        "test": "action_test",
    }
    
    # Check for semantic group match
    group_key = None
    for phrase, group in SEMANTIC_GROUPS.items():
        if phrase in text_lower:
            group_key = group
            break
    
    if group_key:
        # Use group key for consistent hash
        hash_input = group_key
    else:
        hash_input = text_lower
    
    # Generate 384-dim embedding from hash
    hash_bytes = hashlib.sha256(hash_input.encode()).digest()
    embedding = []
    for i in range(384):
        byte_idx = i % 32
        embedding.append((hash_bytes[byte_idx] + i) % 256 / 255.0 - 0.5)
    
    # Normalize
    norm = math.sqrt(sum(x*x for x in embedding))
    if norm > 0:
        embedding = [x / norm for x in embedding]
    
    return embedding


# ---------------------------------------------------------------------------
# Guard Node
# ---------------------------------------------------------------------------

class NudgeOpsNode:
    """
    LangGraph node that runs NudgeOps loop detection.
    
    Add this node after tool execution to monitor for loops.
    
    Example:
        guard = NudgeOpsNode()
        builder.add_node("guard", guard)
        builder.add_edge("tools", "guard")
        builder.add_conditional_edges("guard", guard.should_continue)
    """
    
    def __init__(
        self,
        nudge_threshold: float = 2.0,
        stop_threshold: float = 3.0,
        embed_fn: Callable[[str], list[float]] | None = None,
        agent_id: str | None = None,
    ):
        self.guard = UniversalGuard(
            nudge_threshold=nudge_threshold,
            stop_threshold=stop_threshold,
        )
        self.embed_fn = embed_fn
        self.agent_id = agent_id
    
    def __call__(self, state: NudgeOpsState) -> NudgeOpsState:
        """Process state and apply loop detection."""
        
        # Extract step from state
        step = extract_step_from_state(state, self.agent_id, self.embed_fn)
        
        if step is None:
            # No tool execution, nothing to check
            return state
        
        # Run detection
        decision = self.guard.on_step(step)
        
        # Apply decision to state
        new_state = dict(state)
        new_state["loop_score"] = decision.score
        
        if decision.action == "STOP":
            new_state["should_stop"] = True
            new_state["stop_reason"] = decision.message
            
        elif decision.action == "NUDGE":
            # Inject nudge as system message
            messages = list(state.get("messages", []))
            messages.append({
                "role": "system",
                "content": f"[NudgeOps] {decision.message}",
            })
            new_state["messages"] = messages
            new_state["nudge_count"] = state.get("nudge_count", 0) + 1
        
        return new_state
    
    def should_continue(self, state: NudgeOpsState) -> str:
        """
        Conditional edge function.
        
        Returns:
            "end" if should_stop is True
            "continue" otherwise
        """
        if state.get("should_stop", False):
            return "end"
        return "continue"
    
    def reset(self):
        """Reset guard state for new conversation."""
        self.guard.reset()


# ---------------------------------------------------------------------------
# Graph Builder Helpers
# ---------------------------------------------------------------------------

def add_guard_to_graph(
    builder: StateGraph,
    after_node: str = "tools",
    before_node: str = "agent",
    guard_node_name: str = "guard",
    **guard_kwargs,
) -> StateGraph:
    """
    Add NudgeOps guard to an existing graph builder.
    
    This inserts a guard node between tool execution and agent.
    
    Args:
        builder: LangGraph StateGraph builder
        after_node: Node after which to insert guard (usually "tools")
        before_node: Node to continue to after guard (usually "agent")
        guard_node_name: Name for the guard node
        **guard_kwargs: Arguments passed to NudgeOpsNode
    
    Returns:
        Modified builder (also modifies in place)
    
    Example:
        builder = StateGraph(AgentState)
        builder.add_node("agent", agent_fn)
        builder.add_node("tools", tool_fn)
        builder.add_edge("agent", "tools")
        
        # Add guard
        add_guard_to_graph(builder, after_node="tools", before_node="agent")
        
        # Now flow is: agent → tools → guard → agent
    """
    guard = NudgeOpsNode(**guard_kwargs)
    
    # Add guard node
    builder.add_node(guard_node_name, guard)
    
    # Wire: after_node → guard
    builder.add_edge(after_node, guard_node_name)
    
    # Wire: guard → (continue to before_node OR end)
    builder.add_conditional_edges(
        guard_node_name,
        guard.should_continue,
        {
            "continue": before_node,
            "end": END,
        }
    )
    
    return builder


# ---------------------------------------------------------------------------
# Convenience: Wrap Existing Graph
# ---------------------------------------------------------------------------

def create_guarded_graph(
    graph_factory: Callable[[], StateGraph],
    **guard_kwargs,
) -> StateGraph:
    """
    Create a guarded version of a graph.
    
    This is the simplest way to add NudgeOps to an existing agent.
    
    Args:
        graph_factory: Function that creates the base graph
        **guard_kwargs: Arguments passed to NudgeOpsNode
    
    Returns:
        New StateGraph with guard added
    
    Example:
        def create_my_agent():
            builder = StateGraph(AgentState)
            # ... build graph ...
            return builder
        
        # Without guard
        graph = create_my_agent().compile()
        
        # With guard
        graph = create_guarded_graph(create_my_agent).compile()
    """
    builder = graph_factory()
    add_guard_to_graph(builder, **guard_kwargs)
    return builder
```

---

## 7. Usage Examples

### Basic Usage

```python
from langgraph.graph import StateGraph, END
from nudgeops.integrations.langgraph import NudgeOpsNode, add_guard_to_graph

# Define your agent graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_edge("agent", "tools")
builder.add_edge("tools", "agent")  # Normal loop

# Add NudgeOps guard
add_guard_to_graph(builder, after_node="tools", before_node="agent")

# Compile and run
graph = builder.compile()
result = graph.invoke({"messages": [{"role": "user", "content": "..."}]})
```

### With Custom Thresholds

```python
guard = NudgeOpsNode(
    nudge_threshold=1.5,  # Nudge earlier
    stop_threshold=2.5,   # Stop earlier
)
builder.add_node("guard", guard)
```

### With Real Embeddings

```python
from fastembed import TextEmbedding

embedder = TextEmbedding("BAAI/bge-small-en-v1.5")

def embed_fn(text: str) -> list[float]:
    return list(embedder.embed([text]))[0].tolist()

guard = NudgeOpsNode(embed_fn=embed_fn)
```

### Multi-Agent Graph

```python
# For multi-agent, specify agent_id
search_guard = NudgeOpsNode(agent_id="search")
compare_guard = NudgeOpsNode(agent_id="compare")

builder.add_node("search_guard", search_guard)
builder.add_node("compare_guard", compare_guard)
```

---

## 8. Testing

### What We Test

| Test | Proves |
|------|--------|
| `test_guard_node_observes_normal_flow` | Guard doesn't interfere with healthy agents |
| `test_guard_node_nudges_on_stutter` | Nudge injected after 3+ repeated actions |
| `test_guard_node_stops_on_high_score` | Agent terminated when score hits 3.0 |
| `test_state_extraction` | StepRecord correctly built from LangGraph state |
| `test_nudge_message_injected` | System message appears in state.messages |
| `test_guard_reset` | Guard can be reused across conversations |

### Running Tests

```bash
# Run integration tests
pytest tests/integration/test_langgraph.py -v

# Run with mock LLM (no API calls)
pytest tests/integration/test_langgraph.py -v --no-llm

# Run all NudgeOps tests
pytest tests/ -v
```

---

## 9. Limitations & Future Work

### Current Limitations

| Limitation | Why | Future Fix |
|------------|-----|------------|
| Fake embeddings in tests | Avoid dependency on embedding model | Add real embedding tests |
| Mock LLM only | Avoid API costs in tests | Add opt-in real LLM tests |
| Generic nudge messages | No LLM analysis of what went wrong | Add LLM-powered nudge generation |
| Single graph topology | Assumes agent→tools→guard pattern | Support arbitrary topologies |

### Future Work

1. **LLM-Powered Nudges**: Use LLM to analyze trajectory and generate specific guidance
2. **Real Embedding Tests**: Validate semantic detection with actual embeddings  
3. **Other Frameworks**: CrewAI, AutoGen, custom agents
4. **Tiered Activation**: Only run full detection when suspicious (optimization)
5. **Observability**: Metrics, logging, dashboards

### The Bigger Picture

```
CURRENT:
  Pattern detection → Generic nudge

FUTURE:
  Pattern detection → LLM analysis → Specific nudge
                           │
                           └─→ "You've tried 3 size variants that are OOS.
                                Available sizes are S, M, L. Select one."
```

---

## Summary

This integration proves NudgeOps can work with a real agent framework:

✅ Guard node intercepts after tool execution  
✅ StepRecord extracted from LangGraph state  
✅ Nudge messages injected into agent context  
✅ STOP terminates the graph  
✅ All without real LLM calls (mock testing)  

The pattern is generalizable: **extract state → build StepRecord → run guard → apply decision**.

Any framework that exposes these hooks can use NudgeOps.

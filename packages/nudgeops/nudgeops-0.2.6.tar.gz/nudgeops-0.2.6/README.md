# NudgeOps

> **Runtime loop protection and failure memory for AI agents.**
> Detects when agents are stuck, blocks repeated failures, and tracks how much cost you save.

[![PyPI version](https://badge.fury.io/py/nudgeops.svg)](https://pypi.org/project/nudgeops/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/luv91/nudgeops/actions/workflows/test.yml/badge.svg)](https://github.com/luv91/nudgeops/actions/workflows/test.yml)

---

## Why NudgeOps?

AI agents get stuck. When they loop, **every iteration burns tokens, time, and money.**
Most frameworks only detect loops *after* the fact, or just stop the run.

NudgeOps sits **between your agent and its tools**:

- Tracks which actions and strategies have already failed in the current state
- Blocks **repeating** those known-bad attempts
- Optionally injects a clear "don't keep doing this" nudge into the context
- Emits metrics so you can see **how many loops were prevented** and **how much you saved**

### Example

**Without NudgeOps:**

```text
search("XYZ-9999") → "not found"
search("XYZ-9999") → "not found"   ($0.02)
search("XYZ-9999") → "not found"   ($0.04)
... 50 more attempts ...           ($1.00+ wasted)
```

**With NudgeOps:**

```text
search("XYZ-9999") → "not found"
search("XYZ-9999") → BLOCKED:

  "You already tried search('XYZ-9999') multiple times
   in the same state and it failed each time.
   Do NOT repeat this action. Choose a different strategy."
```

The agent stays in control of what to do instead — NudgeOps just prevents it
from banging its head on the same wall.

## Install

```bash
# Core
pip install nudgeops

# With LangGraph support
pip install "nudgeops[langgraph]"

# With OpenAI client for thought normalization
pip install "nudgeops[openai]"

# Everything
pip install "nudgeops[all]"
```

## Core Concepts

NudgeOps adds runtime failure memory and loop prevention to your agent stack.

### 1. Action-Level Blocking

Detect and block exactly repeated actions in the same state:

- `(state_hash, action_hash)` is used as a key
- If the same tool with the same args was already tried and failed N times:
  - NudgeOps blocks it and optionally injects a nudge message

### 2. Intent-Level Blocking (Strategy-Level)

Agents often try tiny variations of the same failing strategy.

Example:

```text
"search XYZ-9999"   → search("XYZ-9999")
"try without dash"   → search("XYZ9999")
"try with space"     → search("XYZ 9999")
```

Different actions, same intent: "find product by ID".

SmartNudgeOps uses a small LLM to normalize thoughts into short intents
(e.g. "find product by ID"). It then:

- Tracks failures by `(state_hash, intent)`
- Blocks further attempts when a strategy is clearly exhausted

### 3. Observability & Savings

Every block / failure can be recorded:

- loops blocked
- tokens saved (estimated)
- cost saved in USD
- top failure signatures

You get a runtime guardrail and a report to prove it's working.

## Quick Start

### 1. Basic Loop Detection (UniversalGuard)

```python
from nudgeops import UniversalGuard

guard = UniversalGuard()

# Inside your agent loop
result = guard.check(state)

if result.blocked:
    print(f"Loop detected: {result.reason}")
    # e.g. stop the run or inject a generic nudge
```

UniversalGuard uses pattern-based detectors (stutter, phantom progress, ping-pong, etc.)
to flag suspicious behavior from the full state.

### 2. Smart Guard (Action + Intent Level)

```python
from nudgeops import SmartNudgeOps, MockLLMClient

# In production you'd pass your real LLM client here
nudgeops = SmartNudgeOps(llm_client=MockLLMClient())

result = nudgeops.check(
    state={"page": "search_results"},
    thought="I should search for the product using its ID XYZ-9999",
    tool_name="search",
    args={"query": "XYZ-9999"},
)

if result.blocked:
    print("Blocked:", result.reason)
    print("Nudge:", result.nudge_message)
else:
    # Safe to execute the tool
    do_tool_call(...)
```

### 3. LangGraph Integration (One Line)

```python
from nudgeops import SmartNudgeOps
from langgraph.graph import StateGraph

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# Add SmartNudgeOps protection to tool nodes
nudgeops = SmartNudgeOps(llm_client=my_llm)
nudgeops.apply(builder)

graph = builder.compile()
result = graph.invoke({"messages": [user_message]})
```

NudgeOps wraps your tool nodes:

- checks action + intent before execution
- blocks known-bad repeats
- records failures when tools throw

## Detection & Protection Layers

NudgeOps uses multiple mechanisms, so if one misses a pattern, another can still catch it.

### A. Loop Detection (UniversalGuard)

| # | Mechanism | Purpose |
|---|-----------|---------|
| 1 | Stutter Detector | Exact same action repeated multiple times |
| 2 | Insanity Detector | Semantically similar actions in a tight loop |
| 3 | Phantom Progress | Different actions but state never changes |
| 4 | Ping-Pong Detector | A→B→A→B handoff loops between agents |
| 5 | Loop Scorer | Aggregates signals into a loop score |
| 6 | Intervention Manager | Turns score into OBSERVE/NUDGE/STOP decision |

Typical behavior:

- Low score → OBSERVE (just log)
- Medium score → NUDGE (inject generic nudge)
- High score → STOP (terminate agent)

### B. Smart Guard (Action / Intent / Failure Memory)

| # | Component | What It Does |
|---|-----------|--------------|
| 7 | Smart Guard L1 | Block exact action repeats after N failures |
| 8 | Smart Guard L2 | Block exhausted intents (same strategy variations) |
| 9 | Thought Normalizer | LLM summaries → short canonical intents |
| 10 | State Hasher | Stable hash of state (ignores timestamps, IDs, etc.) |
| 11 | Action Hasher | Stable hash of tool + args (normalizes IDs, etc.) |
| 12 | Failure Memory | Tracks failures per (state, action) and (state, intent) |
| 13 | Failure Events | Emits normalized error signatures for analytics |
| 14 | Observability | Aggregates blocks, tokens saved, cost saved |
| 15 | LangGraph Wrapper | One-line integration via SmartNudgeOps.apply() |

You don't need to configure these individually; they come wired together via SmartNudgeOps.

## How Blocking Works

### 1. Action-Level Blocking

```text
State S:
  search({q: "XYZ-9999"}) → fails
  search({q: "XYZ-9999"}) → fails again

On next identical call:
  search({q: "XYZ-9999"}) → BLOCKED

Nudge: "This exact action already failed in this state.
        Repeating it will not help. Choose a different approach."
```

### 2. Intent-Level Blocking

SmartNudgeOps normalizes thoughts into intents:

```text
"I should search for XYZ-9999 by ID"    → "find product by ID"
"Let me try without the hyphen"        → "find product by ID"
"Let me try with spaces"               → "find product by ID"
```

It tracks failures by `(state_hash, intent)`.

Once the same intent fails via several action variants:

```text
Intent "find product by ID" attempts: 3+
→ Further attempts with same intent are BLOCKED
```

Nudge to the agent:

```text
"You are stuck on strategy 'find product by ID'.
Several variations of this approach have failed in this state.
Do not continue with this strategy. Choose a different one."
```

NudgeOps never prescribes which new strategy to use — that remains the agent's / planner's job.

## Observability & Metrics

You can access aggregated metrics to see how much NudgeOps is helping.

```python
from nudgeops import SmartNudgeOps

nudgeops = SmartNudgeOps(llm_client=my_llm)

# ... run agents ...

summary = nudgeops.observability.get_tenant_summary(tenant_id="my-team")

print("Agents monitored:", summary["agents_monitored"])
print("Repeated actions blocked:", summary["repeats_blocked"])
print("Tokens saved:", summary["tokens_saved"])
print("Cost saved (USD):", summary["cost_saved_usd"])
print("Top failure types:", summary["top_failure_types"])
```

This makes it easy to justify NudgeOps internally:

> "We spent $99/month for NudgeOps and it saved us $500 in wasted loops."

## API Overview

### SmartNudgeOps

High-level, opinionated guard that combines:

- thought normalization
- state + action hashing
- failure memory
- optional LangGraph integration

```python
from nudgeops import SmartNudgeOps

nudgeops = SmartNudgeOps(
    llm_client=my_llm,           # LLM used to normalize thoughts → intents
    action_repeat_threshold=2,   # Block after N exact repeats (default: 2)
    intent_repeat_threshold=3,   # Block after N intent attempts (default: 3)
)

result = nudgeops.check(
    state=state_dict,
    thought="I should search for the product using its ID XYZ-9999",
    tool_name="search",
    args={"query": "XYZ-9999"},
)

if result.decision.name == "BLOCK":
    print(result.nudge_message)
else:
    # execute tool...
    pass
```

### UniversalGuard

Lower-level, pattern-based loop detector operating on state only.

```python
from nudgeops import UniversalGuard

guard = UniversalGuard()
result = guard.check(state)

if result.blocked:
    print("Loop detected:", result.reason)
    for detection in result.detections:
        print(detection.detector, detection.score)
```

## Summary

NudgeOps is not another agent framework.
It's a runtime guard that remembers failures and blocks agents from repeating them.

- It works alongside LangGraph or any other agent orchestration.
- It reduces cost by preventing loops and makes agents easier to debug by surfacing what failed, where, and how often.

> "Stop your agents from repeating the same mistakes.
> Let them learn from every failure — not just their own."

## License

MIT

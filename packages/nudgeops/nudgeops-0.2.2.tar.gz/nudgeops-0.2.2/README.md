# NudgeOps

[![PyPI version](https://badge.fury.io/py/nudgeops.svg)](https://pypi.org/project/nudgeops/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/luv91/nudgeops/actions/workflows/test.yml/badge.svg)](https://github.com/luv91/nudgeops/actions/workflows/test.yml)

**Runtime semantic guardrails for AI agents.**

Detect loops. Nudge agents back on track. Stop runaway costs.

## Features

- **Pattern Detection**: Stutter, insanity, phantom progress, ping-pong loops
- **Intent-Level Protection**: LLM-based thought normalization to detect strategy repetition
- **Two-Level Blocking**: Block exact action repeats AND exhausted strategies
- **LangGraph Integration**: Drop-in guard for LangGraph workflows
- **Observability**: Track blocks, saves, and ROI

## Installation

```bash
pip install nudgeops

# With LangGraph support
pip install nudgeops[langgraph]

# With OpenAI for thought normalization
pip install nudgeops[openai]

# Everything
pip install nudgeops[all]
```

## Quick Start

### Basic Usage (Pattern Detection)

```python
from nudgeops import UniversalGuard

guard = UniversalGuard()

# In your agent loop
result = guard.check(state)
if result.blocked:
    print(f"Loop detected! {result.reason}")
```

### Smart Guard (Intent-Level)

```python
from nudgeops import SmartNudgeOps, MockLLMClient

# Create guard
nudgeops = SmartNudgeOps(llm_client=MockLLMClient())

# Check before each action
result = nudgeops.check(
    state={"page": "search"},
    thought="I should search for XYZ-9999",
    tool_name="search",
    args={"query": "XYZ-9999"}
)

if result.blocked:
    print(f"Blocked: {result.reason}")
    print(f"Nudge: {result.nudge_message}")
```

### LangGraph Integration

```python
from nudgeops import SmartNudgeOps
from langgraph.graph import StateGraph

# Build your graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# Apply NudgeOps - wraps tool nodes with guard
nudgeops = SmartNudgeOps(llm_client=my_llm)
nudgeops.apply(builder)

graph = builder.compile()
```

## How It Works

### Two-Level Protection

**Level 1 (Action)**: Block exact action repeats after 2 attempts
```
search({q:"XYZ-9999"}) → fails
search({q:"XYZ-9999"}) → BLOCKED (same action twice)
```

**Level 2 (Intent)**: Block exhausted strategies after 3 variations
```
"search XYZ-9999"  → "find product by ID" (intent)
"try XYZ9999"      → "find product by ID" (same intent!)
"try XYZ 9999"     → "find product by ID" (same intent!)
"try XYZ--9999"    → BLOCKED (intent exhausted)
```

## License

MIT

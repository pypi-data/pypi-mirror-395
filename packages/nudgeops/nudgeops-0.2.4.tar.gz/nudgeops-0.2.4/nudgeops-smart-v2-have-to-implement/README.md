# NudgeOps v0.2.0 - Smart Intent-Level Guard

> **Runtime action firewall + shared failure brain for AI agents**

## What's New in v0.2.0

This release adds the **Smart Guard** module with:

- **Intent-level tracking**: Detects when agent is stuck on same strategy with different actions
- **Two-level blocking**: Exact action repeats (2x) + Intent repeats (3x)  
- **LLM-based thought normalization**: "search XYZ-9999" and "try XYZ9999" → same intent "find product by ID"
- **Failure memory**: Tracks what failed per state
- **Observability**: ROI metrics, cost savings estimates

## Quick Start

```python
from nudgeops.smart import SmartNudgeOps, MockLLMClient

# Create guard
nudgeops = SmartNudgeOps(llm_client=MockLLMClient())

# For LangGraph - just apply to builder
nudgeops.apply(builder)
graph = builder.compile()

# Or use manually
result = nudgeops.check(
    state={"page": "search"},
    thought="search for XYZ-9999",
    tool_name="search",
    args={"query": "XYZ-9999"}
)

if result.blocked:
    print(result.nudge_message)
else:
    # Execute action...
    # If fails:
    nudgeops.record_failure(state, thought, tool, args, error)
```

## How It Works

```
Agent: "search for XYZ-9999"     → Allow (first try)
       search("XYZ-9999")        → Error: Not found
       
Agent: "try without hyphen"      → Allow (different action, same intent=1)  
       search("XYZ9999")         → Error: Not found

Agent: "try with space"          → Allow (different action, same intent=2)
       search("XYZ 9999")        → Error: Not found

Agent: "one more try"            → BLOCKED! (same intent=3)
       
       [NudgeOps: Strategy Blocked]
       You are stuck on: "find product by ID"
       Tried 3 variations. All failed.
       Try a DIFFERENT strategy.
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NUDGEOPS GUARD                         │
│                                                             │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐      │
│   │   THOUGHT   │   │   ACTION    │   │   STATE     │      │
│   │  NORMALIZER │   │   HASHER    │   │   HASHER    │      │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘      │
│          │                 │                 │              │
│          ▼                 ▼                 ▼              │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                   FAILURE MEMORY                    │  │
│   │   Intent Cache: (state, intent) → count, actions    │  │
│   │   Action Cache: (state, action) → count, error      │  │
│   └─────────────────────────────────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                  DECISION ENGINE                    │  │
│   │   action cache hit (2x) → BLOCK                     │  │
│   │   intent cache hit (3x) → BLOCK                     │  │
│   │   otherwise → ALLOW                                 │  │
│   └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Files Structure

```
nudgeops/
├── smart/
│   ├── __init__.py              # Main exports
│   ├── thought_normalizer.py    # LLM intent extraction
│   ├── hashers.py               # State/action hashing
│   ├── failure_memory.py        # Two-level cache
│   ├── guard.py                 # SmartGuard decision engine
│   ├── events.py                # Failure event schema
│   ├── observability.py         # Metrics & stats
│   └── langgraph_integration.py # LangGraph wrapper
├── core/                        # Original detectors
├── integrations/                # Original integrations
└── tests/smart/                 # 36 new tests
```

## Installation

```bash
# From source
pip install -e .

# With LangGraph support
pip install -e ".[langgraph]"

# With OpenAI
pip install -e ".[openai]"

# Everything
pip install -e ".[all]"
```

## Tests

```bash
# Run all tests (66 total)
pytest tests/ -v

# Run only smart module tests (36)
pytest tests/smart/ -v
```

## Key Components

### ThoughtNormalizer
Converts agent thoughts to canonical intents using LLM:
- "search for XYZ-9999" → "find product by ID"
- "try without hyphen" → "find product by ID"
- "browse electronics" → "browse by category"

### FailureMemory  
Two-level tracking:
1. **Action level**: Exact (state, action) → failure count
2. **Intent level**: (state, intent) → cluster of failed actions

### SmartGuard
Decision engine:
- Action repeated 2x in same state → BLOCK
- Intent repeated 3x in same state → BLOCK
- Otherwise → ALLOW

### ObservabilityLayer
Tracks:
- Blocks, allows, failures
- Tokens saved estimates
- ROI calculations

## Usage with Real LLM

```python
from langchain_openai import ChatOpenAI
from nudgeops.smart import SmartNudgeOps

# Wrap OpenAI to match LLMClient protocol
class OpenAIWrapper:
    def __init__(self, llm):
        self.llm = llm
    def complete(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content

llm = ChatOpenAI(model="gpt-4o-mini")
nudgeops = SmartNudgeOps(llm_client=OpenAIWrapper(llm))
```

## ROI Example

```
Monthly agent runs:     10,000
Loops detected:          2,000 (20%)
Without NudgeOps:       8 steps per loop × 150 tokens = 2.4M tokens wasted
With NudgeOps:          3 steps per loop × 150 tokens = 0.9M tokens

Tokens saved: 1.5M
Cost saved: ~$560/month (at GPT-4o-mini rates)
```

## License

MIT

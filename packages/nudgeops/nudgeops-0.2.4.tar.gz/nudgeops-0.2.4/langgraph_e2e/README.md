# Real LangGraph Integration Test

## What This Is

This is an **end-to-end test** that actually runs a LangGraph agent and watches NudgeOps stop it when it loops.

## What's Different From Previous Tests

| Previous Tests | This Test |
|----------------|-----------|
| Fake state dictionaries | Real `StateGraph` |
| Called `guard_node(state)` directly | `graph.invoke()` runs everything |
| No actual graph execution | Full LangGraph execution flow |
| Proved our code works | Proves integration works |

## Files

```
tests/integration/
├── test_langgraph.py           # EXISTING - unit tests with fake state
└── test_langgraph_e2e.py       # NEW - end-to-end with real StateGraph
```

## What test_langgraph_e2e.py Does

### Test 1: `test_looping_agent_gets_stopped`

Creates an agent that **intentionally loops** (always calls same tool with same args):

```
Agent: "I'll search for laptop"     → Tool: search(laptop)
Agent: "I'll search for laptop"     → Tool: search(laptop)  
Agent: "I'll search for laptop"     → Tool: search(laptop)
       ↑ NudgeOps detects stutter, triggers STOP
```

**Expected**: Graph terminates before max iterations.

### Test 2: `test_healthy_agent_completes`

Creates an agent that **makes progress** (different actions each time):

```
Agent: "Search for laptop"    → Tool: search(laptop)
Agent: "Select item 1"        → Tool: select(1)
Agent: "Add to cart"          → Tool: add_to_cart(1)
Agent: "Done!"                → END
```

**Expected**: Graph completes normally, NudgeOps doesn't interfere.

### Test 3: `test_semantic_loop_detected`

Creates an agent that **uses synonyms** (different words, same intent):

```
Agent: "Search laptop"        → Tool: search(laptop)
Agent: "Search notebook"      → Tool: search(notebook)
Agent: "Search portable pc"   → Tool: search(portable pc)
       ↑ NudgeOps detects semantic similarity
```

**Expected**: Score increases, eventually triggers intervention.

### Test 4: `test_nudge_injected_before_stop`

Verifies the escalation path:

```
OBSERVE → OBSERVE → NUDGE → NUDGE → STOP
                     ↑
                     System message injected here
```

**Expected**: `[NudgeOps]` message appears in state before STOP.

## How It Works

```python
# 1. Create graph with our guard
builder = StateGraph(AgentState)
builder.add_node("agent", mock_agent)
builder.add_node("tools", mock_tools)
add_guard_to_graph(builder, after_node="tools", before_node="agent")
graph = builder.compile()

# 2. Run it
result = graph.invoke({"messages": [{"role": "user", "content": "Buy a laptop"}]})

# 3. Check what happened
assert result["should_stop"] == True  # NudgeOps stopped it
assert result["loop_score"] >= 3.0    # Hit stop threshold
```

## Mock LLM Behavior

We use a **mock agent** that follows a script:

```python
class MockLoopingAgent:
    """Agent that always does the same thing (will trigger stutter detection)."""
    
    def __call__(self, state):
        return {
            "messages": [...],
            "tool_calls": [{"tool": "search", "args": {"query": "laptop"}}]
        }
```

No real LLM calls. But the graph execution is real.

## Requirements

```bash
pip install langgraph
```

## Running

```bash
# Run just the e2e tests
pytest tests/integration/test_langgraph_e2e.py -v

# Run all integration tests
pytest tests/integration/ -v
```

## What Success Looks Like

```
tests/integration/test_langgraph_e2e.py::test_looping_agent_gets_stopped PASSED
tests/integration/test_langgraph_e2e.py::test_healthy_agent_completes PASSED
tests/integration/test_langgraph_e2e.py::test_semantic_loop_detected PASSED
tests/integration/test_langgraph_e2e.py::test_nudge_injected_before_stop PASSED
```

## What This Proves

✅ NudgeOps integrates with real LangGraph  
✅ Guard node intercepts execution flow  
✅ Looping agents get stopped  
✅ Healthy agents are not affected  
✅ Nudge messages are injected correctly  

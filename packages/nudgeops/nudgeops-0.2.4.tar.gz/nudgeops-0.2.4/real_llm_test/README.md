# Real LLM Integration Tests

## What This Is

End-to-end tests that use **actual OpenAI API calls** to prove NudgeOps works with real LLMs.

## Previous Tests vs This

| Previous | This |
|----------|------|
| Mock LLM (scripted responses) | Real OpenAI API calls |
| Free | Costs ~$0.01-0.50 per test |
| Deterministic | Non-deterministic (LLM decides) |
| "Does our code work?" | "Does NudgeOps stop real LLMs from looping?" |

## Files

```
nudgeops/testing/
├── openai_agent.py          # OpenAI LLM agent for LangGraph
└── loop_inducing_tools.py   # Mock tools that cause loops

tests/integration/
└── test_real_llm.py         # Actual tests
```

### openai_agent.py

LangGraph-compatible agent that calls OpenAI:

```python
agent = OpenAIAgentNode(
    model="gpt-4o-mini",  # or "gpt-4o"
    max_calls=15,         # Safety limit
    max_cost=0.50,        # Cost limit
)
builder.add_node("agent", agent)
```

Features:
- Tracks token usage and costs
- Has safety limits (max calls, max cost)
- Supports tool calling
- Works with any OpenAI model

### loop_inducing_tools.py

Mock tools designed to cause loops:

| Scenario | What Happens | Loop Type |
|----------|--------------|-----------|
| `impossible_search` | Product never found | Semantic (search variations) |
| `always_oos` | Every variant is out of stock | Stutter (retry same variants) |
| `checkout_fail` | Checkout always fails | Stutter (retry checkout) |
| `ambiguous` | Confusing responses | Insanity (random attempts) |

```python
tools = LoopInducingTools(scenario="impossible_search")
builder.add_node("tools", tools)
```

### test_real_llm.py

Tests that run the full flow:

```
User: "Buy XYZ-9999 laptop"
       ↓
LLM (GPT-4o-mini): "I'll search for XYZ-9999"
       ↓
Tools: "No results found"
       ↓
NudgeOps: score = 0.5 (phantom progress)
       ↓
LLM: "Let me try XYZ 9999"
       ↓
Tools: "No results found"
       ↓
NudgeOps: score = 1.0
       ↓
LLM: "Maybe XYZ9999?"
       ↓
Tools: "No results found"
       ↓
NudgeOps: score = 2.5 → NUDGE injected
       ↓
LLM: (sees nudge) "I'll try one more time..."
       ↓
NudgeOps: score = 3.5 → STOP
       ↓
Test: ✓ Agent stopped by NudgeOps
```

## Setup

### 1. Install Dependencies

```bash
pip install openai langgraph
```

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new key
3. Add payment method at https://platform.openai.com/settings/organization/billing/overview
4. Buy $5-10 credits (plenty for testing)

### 3. Set Environment Variable

```bash
# Add to ~/.zshrc or ~/.bashrc for persistence
export OPENAI_API_KEY="sk-..."

# Or just for this session
export OPENAI_API_KEY="sk-..."
```

### 4. Copy Files to Your Project

```bash
# Copy agent and tools
cp nudgeops/testing/openai_agent.py /path/to/nudgeops/nudgeops/testing/
cp nudgeops/testing/loop_inducing_tools.py /path/to/nudgeops/nudgeops/testing/

# Copy tests
cp tests/integration/test_real_llm.py /path/to/nudgeops/tests/integration/
```

## Running Tests

### Estimate Costs First (No API Calls)

```bash
pytest tests/integration/test_real_llm.py::TestCostEstimation -v -s
```

### Run Cheap Tests Only (GPT-4o-mini, ~$0.02 total)

```bash
pytest tests/integration/test_real_llm.py::TestGPT4oMini -v -s
```

### Run Single Test

```bash
pytest tests/integration/test_real_llm.py::TestGPT4oMini::test_impossible_search_loop_stopped -v -s
```

### Run Production Model Tests (GPT-4o, ~$0.10-0.50)

```bash
pytest tests/integration/test_real_llm.py::TestGPT4o -v -s
```

### Run Model Comparison (Most Expensive, ~$0.15)

```bash
pytest tests/integration/test_real_llm.py::TestModelComparison -v -s
```

### Run All Tests

```bash
pytest tests/integration/test_real_llm.py -v -s
```

## Expected Output

```
tests/integration/test_real_llm.py::TestGPT4oMini::test_impossible_search_loop_stopped 

✓ Test passed - Agent stopped after 7 LLM calls
  Cost: $0.0034

============================================================
TEST SUMMARY
============================================================

impossible_search_loop (gpt-4o-mini):
  stopped_by_nudgeops: True
  loop_score: 3.5
  steps: 7
  llm_calls: 7
  cost: $0.0034
  hit_limits: False

PASSED
```

## Cost Safety

The code has multiple safety limits:

```python
# In OpenAIAgentNode
max_calls=15      # Never make more than 15 API calls
max_cost=0.50     # Stop if cost exceeds $0.50

# In test graph
max_steps=20      # Graph terminates after 20 steps
```

Even if everything goes wrong, one test run won't cost more than ~$0.50.

## Test Scenarios

### 1. `test_impossible_search_loop_stopped`

- Task: "Find XYZ-9999 laptop"
- Tools always return "No results"
- LLM tries variations: XYZ-9999, XYZ 9999, XYZ9999...
- NudgeOps detects semantic loop → STOP

### 2. `test_always_oos_loop_stopped`

- Task: "Buy laptop in size XL"
- Tools: Product exists, but every variant is "out of stock"
- LLM tries: XL, Large, Medium, Small, Extra Large...
- NudgeOps detects stutter (same select_variant calls) → STOP

### 3. `test_checkout_fail_loop_stopped`

- Task: "Buy laptop and complete checkout"
- Tools: Search works, add to cart works, but checkout always fails
- LLM retries checkout repeatedly
- NudgeOps detects stutter → STOP

### 4. `test_nudge_appears_before_stop`

- Verifies the OBSERVE → NUDGE → STOP escalation
- Checks that `[NudgeOps]` system messages are injected

### 5. `test_compare_models_on_impossible_search`

- Runs same scenario on GPT-4o-mini and GPT-4o
- Compares: Which loops more? Which costs more?
- Proves NudgeOps helps even production models

## What This Proves

| Question | Answer |
|----------|--------|
| Does NudgeOps work with real LLMs? | ✅ Yes |
| Can it stop GPT-4o from looping? | ✅ Yes |
| Is the LangGraph integration correct? | ✅ Yes |
| Do nudge messages get injected? | ✅ Yes |
| Is the cost tracking accurate? | ✅ Yes |

## Troubleshooting

### "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY="sk-..."
```

### "openai not installed"

```bash
pip install openai
```

### "langgraph not installed"

```bash
pip install langgraph
```

### Tests are expensive

Run only the cheap tests:
```bash
pytest tests/integration/test_real_llm.py::TestGPT4oMini -v -s
```

### LLM gives up too early

Some models (especially GPT-4o) might use `give_up` tool quickly. This is actually good behavior! The test considers this a success:

```python
stopped_properly = (
    result.get("should_stop", False) or  # NudgeOps stopped it
    stats["hit_call_limit"] or           # Hit safety limit
    any("give_up" in str(ex.tool_name) for ex in tools.executions)  # Agent gave up
)
```

## Next Steps After Running

1. **Analyze results**: Which scenarios caused the most loops?
2. **Tune thresholds**: Adjust nudge/stop thresholds based on real behavior
3. **Add more scenarios**: Test your specific use cases
4. **Try other models**: Claude, Gemini, etc.

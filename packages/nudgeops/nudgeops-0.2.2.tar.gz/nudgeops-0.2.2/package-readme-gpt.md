# NudgeOps Runtime Guardrails

Runtime semantic loop detection and interventions for LangGraph agents. Detects stuck behavior, nudges agents back on track, and stops when recovery fails.

## What This Package Does
- **Detect** four loop types: Stutter (exact repeat), Insanity (semantic repeat), Phantom Progress (state frozen), Ping-Pong (multi-agent oscillation).
- **Score** trajectories with decay and map to OBSERVE → NUDGE → STOP.
- **Intervene** by injecting SystemMessage nudges or stopping with diagnostics.
- **Integrate** as a first-class LangGraph node (`TrajectoryGuardNode`) or via one-line helper (`apply_guard`).
- **Observe** with structured JSON logging and optional Langfuse hooks.
- **No LLM calls**: only inspects LangGraph state and tool traffic. Embeddings (FastEmbed) are used for semantic detection.

## Package Layout (src/nudgeops)
- `core/state.py` — Types: `StepRecord`, `DetectionResult`, `LoopStatus`, `GuardConfig`, `AgentState` reducers; helpers to create records/status.
- `core/detectors.py` — Detectors for Types I–IV; `CompositeDetector` runs them all.
- `core/scorer.py` — Loop score aggregation with decay; maps to interventions.
- `core/interventions.py` — Nudge templates, stop payloads, message formatting.
- `embedding/service.py` — FastEmbed singleton (BGE-small) with `embed`/`embed_batch`.
- `embedding/utils.py` — Cosine similarity, hashing, JSON normalization, negation check, descriptor formatting.
- `integrations/extractors.py` — Pulls tool calls/outcomes from LangGraph state; computes hashes/embeddings; builds `StepRecord`.
- `integrations/langgraph_node.py` — `TrajectoryGuardNode` implementing guard logic and Command routing (OBSERVE/NUDGE/STOP).
- `integrations/apply_guard.py` — Helper to insert guard into a `StateGraph`; convenience `create_guarded_graph`.
- `observability/logging.py` — Structured JSON logging helpers.
- `observability/langfuse.py` — Optional Langfuse observer (health scoring/tags).
- `__init__.py` files — Public API exports (note: some strings still say “TrajectoryGuard”).

## Quick Start (LangGraph)
```python
from langgraph.graph import StateGraph, START
from nudgeops import AgentState, apply_guard

# Define your agent and tools nodes (call LLM inside your agent)
def agent_node(state: AgentState): ...
def tool_node(state: AgentState): ...

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")
# Wire the guard after tools; it will route back to agent or __end__
apply_guard(builder)

graph = builder.compile()
result = graph.invoke({"messages": [...]})
print(result.get("loop_status"))
```

## Configuration (GuardConfig)
- `nudge_threshold` (default 2.0): score to send a nudge.
- `stop_threshold` (default 3.0): score to stop.
- `decay_rate` (default 0.5): decay when no detection.
- `max_score` (default 5.0): cap.
- `history_size` (default 10): steps considered.
- `embedding_model` (default `BAAI/bge-small-en-v1.5`).
- `similarity_threshold` (default 0.85): Type II similarity.
- `stutter_threshold` (default 0.99): Type I hash similarity (mostly unused; exact match).
- `enable_langfuse` (default False): toggle Langfuse hooks.

## How Detection Works
- **Type I (Stutter)**: same tool name + args hash as last step; counts repeats.
- **Type II (Insanity)**: cosine similarity on embedded step descriptors; triggers when ≥ `min_count` similar steps (default 3) over threshold (default 0.85); negation penalty for near-duplicates with opposing negation.
- **Type III (Phantom)**: action differs but `state_snapshot_hash` unchanged across steps; signal boost.
- **Type IV (Ping-Pong)**: repeating N-grams of agent_id/tool_name (e.g., A→B→A→B).
- **Scoring**: weighted sum (I=2.0, II=1.5, III=0.5, IV=1.5) * confidence; decay when no detections; thresholds drive intervention ladder.

## Runtime Behavior
1) Extract latest tool call + result from state (`extract_step_from_state`).
2) Run detectors on current step vs history (`trajectory_scratchpad`).
3) Update loop score and `loop_status`.
4) Route:
   - OBSERVE: update state, continue to `next_node`.
   - NUDGE: inject SystemMessage (nudge), increment `nudges_sent`, continue.
   - STOP: add SystemMessage with diagnostics, route to `__end__`.

## Dependencies & Performance
- Requires LangGraph/LangChain message types. Embeddings need `fastembed` and the BGE-small model (downloaded on first use, cached locally).
- Expected overhead: ~6–10ms per embed on CPU for Type II; other logic is negligible. You can disable embeddings (or handle init failure) to skip Type II and measure delta.

## What’s Not Here (yet)
- No LLM calls; you supply the agent/tool logic.
- No examples/tests bundled in this folder.
- Branding cleanup: some strings/class names still say “TrajectoryGuard”.
- No browser/DOM handling; Type III hashes tool results only.
- No hallucination/factuality detection; focused on loops/coordination issues.

## How to Validate
- Scripted scenarios in LangGraph:
  - Stutter: same tool+args twice → expect Type I → nudge/stop based on repeats.
  - Semantic loop: varied queries with empty results → Type II triggers when embeddings on.
  - Phantom: different actions, identical tool result content → Type III boosts score.
  - Ping-pong: alternate agent/tool ids A/B → Type IV.
  - Recovery: after a nudge, resume progress → score decays, back to OBSERVE.
- Assert `loop_status`, injected SystemMessages, and routing (`__end__` on STOP). Time the guard call to gauge overhead.

## Suggested Next Steps
1) Add README/examples demonstrating integration and config knobs.
2) Add unit tests for detectors, scorer, extractors, interventions; small integration test exercising OBSERVE/NUDGE/STOP.
3) Clean up naming to “NudgeOps” in strings and API surface if desired.
4) Document/install deps in `pyproject.toml` (fastembed, langgraph, langchain_core; optional langfuse).
5) Provide a simple logging setup snippet and Langfuse enable/disable guidance.

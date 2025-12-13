TrajectoryGuard MVP-V1: Implementation Plan v2
Timeline: 10 days (2 weeks with buffer) Tools: Claude Code + Cursor + Claude Target: LangGraph integration with all 4 detection types

Table of Contents
Architecture Strategy
Project Structure
Detailed Component Design
AI Tooling Workflow
Integration Strategy
Observability & Demo Strategy
Testing Strategy
10-Day Implementation Plan

Architecture Strategy
Why Graph-Native (Not Wrapper)
❌ WRAPPER PATTERN (Don't do this)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   User Code                                                     │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────┐                                           │
│   │ TrajectoryGuard │ ← Wraps the graph                         │
│   │    Wrapper      │                                           │
│   └────────┬────────┘                                           │
│            │                                                    │
│            ▼                                                    │
│   ┌─────────────────┐                                           │
│   │   LangGraph     │                                           │
│   │   (black box)   │                                           │
│   └─────────────────┘                                           │
│                                                                 │
│   Problems:                                                     │
│   • Can only see inputs/outputs                                 │
│   • Can't inject nudge mid-execution                            │
│   • Can't use Command pattern for routing                       │
│   • Can't stop BEFORE LLM call (wastes money)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

✅ GRAPH-NATIVE PATTERN (Do this)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   LangGraph StateGraph                                          │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │   START                                                 │   │
│   │     │                                                   │   │
│   │     ▼                                                   │   │
│   │   agent                                                 │   │
│   │     │                                                   │   │
│   │     ▼                                                   │   │
│   │   tools                                                 │   │
│   │     │                                                   │   │
│   │     ▼                                                   │   │
│   │   ┌─────────────────┐                                   │   │
│   │   │ trajectory_guard │ ← FIRST-CLASS NODE               │   │
│   │   └────────┬────────┘                                   │   │
│   │            │                                            │   │
│   │      ┌─────┴─────┬──────────┐                           │   │
│   │      ▼           ▼          ▼                           │   │
│   │   agent      __end__    human_help                      │   │
│   │   (nudge)    (stop)     (escalate)                      │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   Benefits:                                                     │
│   • Full state access (messages, scratchpad, everything)        │
│   • Can inject nudge messages into context                      │
│   • Can route dynamically via Command pattern                   │
│   • Stops BEFORE next LLM call (saves $$$)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

The Command Pattern
from langgraph.types import Command
from langchain_core.messages import SystemMessage

def trajectory_guard_node(state: AgentState) -> Command:
    # ... run detection logic ...
    
    if score >= 3.0:  # STOP
        return Command(
            update={"messages": [SystemMessage(content=stop_message)]},
            goto="__end__"
        )
    
    elif score >= 2.0:  # NUDGE
        return Command(
            update={
                "messages": [SystemMessage(content=nudge_message)],
                "loop_status": {"nudges_sent": nudges + 1}
            },
            goto="agent"  # Back to agent with nudge in context
        )
    
    else:  # OBSERVE
        return Command(goto="agent")  # Continue normally


Project Structure
trajectory_guard/
│
├── pyproject.toml              # Dependencies (poetry)
├── README.md                   # Usage docs
│
├── trajectory_guard/
│   ├── __init__.py             # Exports: TrajectoryGuardNode, apply_guard
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── state.py            # AgentState, StepRecord definitions
│   │   ├── detectors.py        # Type I, II, III, IV detectors
│   │   ├── scorer.py           # Loop score calculation + decay
│   │   └── interventions.py    # Nudge templates, stop payloads
│   │
│   ├── embedding/
│   │   ├── __init__.py
│   │   ├── service.py          # FastEmbed singleton
│   │   └── utils.py            # Cosine similarity, text normalization
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── langgraph_node.py   # TrajectoryGuardNode class
│   │   ├── apply_guard.py      # apply_guard(builder) helper
│   │   └── extractors.py       # Extract step info from state
│   │
│   └── observability/
│       ├── __init__.py
│       ├── langfuse.py         # Scoring & tagging
│       └── logging.py          # Structured JSON logs
│
├── examples/
│   ├── basic_usage.py          # Minimal integration
│   ├── demo_recovery.py        # Hero demo: loop → nudge → success
│   └── sabotaged_agent.py      # E2E test with forced loops
│
└── tests/
    ├── test_detectors.py       # Unit tests for each detector
    ├── test_scorer.py          # Scoring + decay tests
    ├── test_integration.py     # Full graph tests
    └── fixtures/
        ├── synthetic_loops.py  # Fake loop scenarios
        └── legitimate_patterns.py


Detailed Component Design
Component 1: State Definitions (core/state.py)
┌─────────────────────────────────────────────────────────────────┐
│                      STATE SCHEMA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  StepRecord (TypedDict):                                        │
│  ───────────────────────                                        │
│  │                                                              │
│  ├── step_id: str              # UUID for deduplication         │
│  │                                                              │
│  ├── tool_name: str            # For Type I & IV                │
│  │                                                              │
│  ├── tool_args_hash: str       # For Type I (Stutter)           │
│  │   └── SHA-256 of normalized JSON                             │
│  │                                                              │
│  ├── thought_embedding: List[float]  # For Type II (Insanity)   │
│  │   └── 384 floats from BGE-small                              │
│  │                                                              │
│  ├── state_snapshot_hash: str  # For Type III (Phantom Progress)│
│  │   └── Hash of relevant state (tool result, page state)       │
│  │   └── NEW: Explicit hash comparison                          │
│  │                                                              │
│  ├── agent_id: Optional[str]   # For Type IV (Ping-Pong)        │
│  │   └── Which agent in multi-agent setup                       │
│  │                                                              │
│  ├── outcome_type: str         # Signal boost                   │
│  │   └── "success" | "empty" | "error"                          │
│  │                                                              │
│  └── timestamp: float          # For debugging                  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  AgentState (TypedDict):                                        │
│  ───────────────────────                                        │
│  │                                                              │
│  ├── messages: Annotated[List[AnyMessage], add_messages]        │
│  │   └── Standard LangGraph message history                     │
│  │   └── Reducer: add_messages (append, don't replace)          │
│  │                                                              │
│  ├── trajectory_scratchpad: Annotated[List[StepRecord], add]    │
│  │   └── Guard's internal memory                                │
│  │   └── Reducer: operator.add (append)                         │
│  │   └── Does NOT go to LLM context                             │
│  │                                                              │
│  └── loop_status: Annotated[dict, replace]                      │
│      └── Current health status                                  │
│      └── Reducer: lambda x, y: y (replace entirely)             │
│      └── Contains:                                              │
│          • loop_score: float                                    │
│          • loop_type: Optional[str]                             │
│          • nudges_sent: int                                     │
│          • last_intervention: Optional[str]                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Code:
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
import operator

class StepRecord(TypedDict):
    step_id: str
    tool_name: str
    tool_args_hash: str           # SHA-256 of normalized args
    thought_embedding: List[float] # 384 floats
    state_snapshot_hash: str      # For Type III
    agent_id: Optional[str]
    outcome_type: str             # "success", "empty", "error"
    timestamp: float

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    trajectory_scratchpad: Annotated[List[StepRecord], operator.add]
    loop_status: Annotated[dict, lambda x, y: y]  # Replace reducer


Component 2: Detectors (core/detectors.py)
┌─────────────────────────────────────────────────────────────────┐
│                      DETECTOR DESIGN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BaseDetector (Protocol):                                       │
│  ─────────────────────────                                      │
│  │                                                              │
│  └── detect(current: StepRecord, history: List[StepRecord])     │
│        → DetectionResult                                        │
│                                                                 │
│  DetectionResult (TypedDict):                                   │
│  │  detected: bool                                              │
│  │  confidence: float (0-1)                                     │
│  │  loop_type: str                                              │
│  │  details: dict                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TYPE I: StutterDetector                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  What: Exact same action repeated                               │
│                                                                 │
│  Logic:                                                         │
│    if current.tool_args_hash == history[-1].tool_args_hash:     │
│        return DetectionResult(detected=True, loop_type="I")     │
│                                                                 │
│  Normalization (critical!):                                     │
│    1. Parse JSON args                                           │
│    2. Sort dict keys recursively                                │
│    3. Lowercase tool name                                       │
│    4. SHA-256 hash                                              │
│                                                                 │
│    {"b": 2, "a": 1} → {"a": 1, "b": 2} → same hash             │
│                                                                 │
│  Threshold:                                                     │
│    • Count = 2 → score += 2.0                                   │
│    • Count = 3 → critical                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TYPE II: InsanityDetector                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  What: Same intent, different words                             │
│                                                                 │
│  Embedding Target:                                              │
│    f"ACTION: {tool}({args}) | RESULT: {outcome}"                │
│                                                                 │
│  Logic:                                                         │
│    similarities = [                                             │
│        cosine_sim(current.embedding, h.embedding)               │
│        for h in history[-10:]                                   │
│    ]                                                            │
│    similar_count = sum(1 for s in similarities if s > 0.85)     │
│    if similar_count >= 3:                                       │
│        return DetectionResult(detected=True, loop_type="II")    │
│                                                                 │
│  Negation Heuristic:                                            │
│    IF similarity > 0.92:                                        │
│      1. Extract overlapping tokens                              │
│      2. Check negation words: {not, never, failed, stop, error} │
│      3. If one has negation, other doesn't → penalize by 0.2    │
│                                                                 │
│  Threshold:                                                     │
│    • similarity > 0.85 AND count >= 3 → score += 1.5            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TYPE III: PhantomProgressDetector                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  What: Different action, but state unchanged                    │
│                                                                 │
│  Key Insight:                                                   │
│    Agent is DOING different things, but ACHIEVING nothing.      │
│    The world state is frozen.                                   │
│                                                                 │
│  Logic:                                                         │
│    if (current.tool_name != history[-1].tool_name OR            │
│        current.tool_args_hash != history[-1].tool_args_hash):   │
│        # Action is different                                    │
│        if current.state_snapshot_hash == history[-1].state_snapshot_hash:│
│            # But state didn't change!                           │
│            return DetectionResult(detected=True, loop_type="III")│
│                                                                 │
│  state_snapshot_hash:                                           │
│    For tool-calling agents:                                     │
│      • Hash the last ToolMessage content                        │
│      • Or hash: f"{tool_name}:{outcome_type}"                   │
│                                                                 │
│    For browser agents (future):                                 │
│      • Hash the AXTree or D2Snap                                │
│                                                                 │
│  Signal:                                                        │
│    • This is a BOOST signal, not standalone                     │
│    • Detection → score += 0.5                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TYPE IV: PingPongDetector                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  What: Multi-agent circular handoffs                            │
│                                                                 │
│  Logic:                                                         │
│    sequence = [h.agent_id for h in history[-10:]]               │
│    # e.g., ["A", "B", "A", "B", "A"]                            │
│                                                                 │
│    # Check for repeating N-grams (length 2-4)                   │
│    for n in [2, 3, 4]:                                          │
│        suffix = sequence[-n:]                                   │
│        prev = sequence[-2*n:-n]                                 │
│        if suffix == prev:                                       │
│            return DetectionResult(detected=True, loop_type="IV")│
│                                                                 │
│  Single-Agent Mode:                                             │
│    If no agent_id, use tool_name sequence instead:              │
│    ["search", "search", "search"] → oscillation pattern         │
│                                                                 │
│  Threshold:                                                     │
│    • Pattern repeats 2+ times → score += 1.5                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Component 3: Scorer (core/scorer.py)
┌─────────────────────────────────────────────────────────────────┐
│                       SCORING LOGIC                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SCORE WEIGHTS:                                                 │
│  ──────────────                                                 │
│  │ Type I  (Stutter)        │  +2.0  │  Highest confidence    │ │
│  │ Type II (Insanity)       │  +1.5  │  Semantic similarity   │ │
│  │ Type III (Phantom)       │  +0.5  │  Signal boost only     │ │
│  │ Type IV (PingPong)       │  +1.5  │  Coordination failure  │ │
│                                                                 │
│  THRESHOLDS:                                                    │
│  ───────────                                                    │
│  │ score < 2.0   │  OBSERVE  │  Log only, continue           │ │
│  │ score >= 2.0  │  NUDGE    │  Inject message, continue     │ │
│  │ score >= 3.0  │  STOP     │  Terminate execution          │ │
│                                                                 │
│  DECAY (The Recovery Mechanism):                                │
│  ───────────────────────────────                                │
│  If NO detection this step:                                     │
│    new_score = current_score * 0.5                              │
│                                                                 │
│  This allows recovery:                                          │
│    Step 5: Loop detected    → score = 2.0 → NUDGE               │
│    Step 6: Agent recovers!  → score = 1.0 (decay)               │
│    Step 7: Progress         → score = 0.5 (decay)               │
│    Step 8: Success          → score = 0.25                      │
│                                                                 │
│  vs. If agent ignores nudge:                                    │
│    Step 5: Loop detected    → score = 2.0 → NUDGE               │
│    Step 6: Still looping    → score = 3.5 → STOP                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Code:
SCORE_WEIGHTS = {
    "TYPE_I_STUTTER": 2.0,
    "TYPE_II_INSANITY": 1.5,
    "TYPE_III_PHANTOM": 0.5,
    "TYPE_IV_PINGPONG": 1.5,
}

THRESHOLDS = {
    "NUDGE": 2.0,
    "STOP": 3.0,
}

MAX_SCORE = 5.0
DECAY_RATE = 0.5

def calculate_score(
    current_score: float,
    detections: List[DetectionResult],
) -> float:
    # 1. Check if any detection this step
    detected_any = any(d.detected for d in detections)
    
    # 2. Apply decay if no detection (agent is recovering)
    if not detected_any:
        return current_score * DECAY_RATE
    
    # 3. Accumulate detection scores
    new_score = current_score
    for detection in detections:
        if detection.detected:
            new_score += SCORE_WEIGHTS.get(detection.loop_type, 0)
    
    # 4. Cap at max
    return min(new_score, MAX_SCORE)


Component 4: Interventions (core/interventions.py)
┌─────────────────────────────────────────────────────────────────┐
│                    NUDGE TEMPLATES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TYPE I (Stutter):                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [System Observation]                                     │   │
│  │                                                          │   │
│  │ ⚠️ You have executed the EXACT SAME action twice:        │   │
│  │   Tool: {tool_name}                                      │   │
│  │   Args: {args}                                           │   │
│  │                                                          │   │
│  │ This action returned "{outcome}" both times.             │   │
│  │ Repeating it will not yield different results.           │   │
│  │                                                          │   │
│  │ Please try one of these alternatives:                    │   │
│  │ • Use a different tool                                   │   │
│  │ • Try different parameters                               │   │
│  │ • Ask the user for clarification                         │   │
│  │ • Acknowledge you cannot complete this task              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TYPE II (Insanity):                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [System Observation]                                     │   │
│  │                                                          │   │
│  │ ⚠️ You have attempted semantically similar actions       │   │
│  │ {count} times without success:                           │   │
│  │                                                          │   │
│  │   1. {action_1}                                          │   │
│  │   2. {action_2}                                          │   │
│  │   3. {action_3}                                          │   │
│  │                                                          │   │
│  │ These are functionally equivalent queries.               │   │
│  │ Rephrasing is NOT a new strategy.                        │   │
│  │                                                          │   │
│  │ Consider:                                                │   │
│  │ • The information may not exist in this source           │   │
│  │ • Try a COMPLETELY different approach                    │   │
│  │ • Use a different tool entirely                          │   │
│  │ • Ask the user for alternative sources                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TYPE IV (PingPong):                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ [System Observation]                                     │   │
│  │                                                          │   │
│  │ ⚠️ A circular pattern has been detected:                 │   │
│  │   {agent_a} → {agent_b} → {agent_a} → {agent_b}          │   │
│  │                                                          │   │
│  │ This appears to be an endless delegation loop.           │   │
│  │ No progress is being made.                               │   │
│  │                                                          │   │
│  │ Please:                                                  │   │
│  │ • Make a final decision now                              │   │
│  │ • Escalate to a human if you cannot decide               │   │
│  │ • Accept the current output as "good enough"             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STOP PAYLOAD:                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {                                                        │   │
│  │   "status": "guardrail_triggered",                       │   │
│  │   "reason": "{loop_type}",                               │   │
│  │   "loop_score": 3.5,                                     │   │
│  │   "nudges_sent": 2,                                      │   │
│  │   "steps_taken": 12,                                     │   │
│  │   "similar_actions": [...],                              │   │
│  │   "recommendation": "Review agent prompt or tool setup"  │   │
│  │ }                                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Component 5: Embedding Service (embedding/service.py)
┌─────────────────────────────────────────────────────────────────┐
│                    EMBEDDING SERVICE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SINGLETON PATTERN:                                             │
│  ──────────────────                                             │
│  Load model ONCE at startup, reuse for all requests.            │
│                                                                 │
│  class EmbeddingService:                                        │
│      _instance: ClassVar[Optional["EmbeddingService"]] = None   │
│      _model: TextEmbedding                                      │
│                                                                 │
│      @classmethod                                               │
│      def get_instance(cls) -> "EmbeddingService":               │
│          if cls._instance is None:                              │
│              cls._instance = cls()                              │
│              cls._instance._model = TextEmbedding(              │
│                  model_name="BAAI/bge-small-en-v1.5"            │
│              )                                                  │
│          return cls._instance                                   │
│                                                                 │
│      def embed(self, text: str) -> np.ndarray:                  │
│          embeddings = list(self._model.embed([text]))           │
│          return np.array(embeddings[0])                         │
│                                                                 │
│  LATENCY:                                                       │
│  ────────                                                       │
│  • First load: 2-5 seconds (downloads ~33MB)                    │
│  • Per embed: 6-10ms                                            │
│  • Model cached in ~/.cache/fastembed                           │
│                                                                 │
│  FALLBACK:                                                      │
│  ─────────                                                      │
│  If embedding fails, fall back to Type I detection only.        │
│  Log warning, don't crash.                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Component 6: LangGraph Node (integrations/langgraph_node.py)
from langgraph.types import Command
from langchain_core.messages import SystemMessage

class TrajectoryGuardNode:
    """First-class LangGraph node for loop detection."""
    
    def __init__(self, config: Optional[GuardConfig] = None):
        self.config = config or GuardConfig()
        self.embedding_service = EmbeddingService.get_instance()
        self.detectors = [
            StutterDetector(),
            InsanityDetector(self.embedding_service),
            PhantomProgressDetector(),
            PingPongDetector(),
        ]
        self.scorer = LoopScorer(self.config)
        self.interventions = InterventionManager()
    
    def __call__(self, state: AgentState) -> Command:
        # 1. Extract current step from state
        current_step = self._extract_step(state)
        if current_step is None:
            return Command(goto="agent")
        
        # 2. Get history
        history = state.get("trajectory_scratchpad", [])
        
        # 3. Run all detectors
        detections = [
            detector.detect(current_step, history)
            for detector in self.detectors
        ]
        
        # 4. Calculate score
        current_score = state.get("loop_status", {}).get("loop_score", 0.0)
        new_score = self.scorer.calculate(detections, current_score)
        
        # 5. Build state update
        update = {
            "trajectory_scratchpad": [current_step],
            "loop_status": {
                "loop_score": new_score,
                "loop_type": self._get_primary_type(detections),
            },
        }
        
        # 6. Decide intervention
        nudges_sent = state.get("loop_status", {}).get("nudges_sent", 0)
        
        if new_score >= 3.0:  # STOP
            update["messages"] = [
                SystemMessage(content=self.interventions.stop_message(detections))
            ]
            self._log_event("STOP", new_score, detections)
            return Command(update=update, goto="__end__")
        
        elif new_score >= 2.0:  # NUDGE
            update["messages"] = [
                SystemMessage(content=self.interventions.nudge_message(detections))
            ]
            update["loop_status"]["nudges_sent"] = nudges_sent + 1
            self._log_event("NUDGE", new_score, detections)
            return Command(update=update, goto="agent")
        
        else:  # OBSERVE
            self._log_event("OBSERVE", new_score, detections)
            return Command(update=update, goto="agent")


Integration Strategy
Three Integration Paths
┌─────────────────────────────────────────────────────────────────┐
│                   INTEGRATION OPTIONS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PATH A: apply_guard() Helper (RECOMMENDED)                     │
│  ──────────────────────────────────────────                     │
│                                                                 │
│  from trajectory_guard import apply_guard                       │
│                                                                 │
│  builder = StateGraph(AgentState)                               │
│  builder.add_node("agent", agent_node)                          │
│  builder.add_node("tools", tool_node)                           │
│  builder.add_edge(START, "agent")                               │
│  builder.add_edge("agent", "tools")                             │
│  builder.add_edge("tools", "agent")  # Original loop            │
│                                                                 │
│  # ✨ One line to add guard                                     │
│  apply_guard(builder)                                           │
│                                                                 │
│  graph = builder.compile()                                      │
│                                                                 │
│  Under the hood:                                                │
│    1. Injects "trajectory_guard" node                           │
│    2. Rewires: tools → guard → agent                            │
│    3. Adds conditional edge: guard → __end__ (if stop)          │
│                                                                 │
│  ───────────────────────────────────────────────────────────    │
│                                                                 │
│  PATH B: Manual Node (Full Control)                             │
│  ──────────────────────────────────                             │
│                                                                 │
│  from trajectory_guard import TrajectoryGuardNode               │
│                                                                 │
│  guard = TrajectoryGuardNode(config)                            │
│                                                                 │
│  builder = StateGraph(AgentState)                               │
│  builder.add_node("guard", guard)                               │
│  builder.add_node("agent", agent_node)                          │
│  builder.add_node("tools", tool_node)                           │
│                                                                 │
│  builder.add_edge(START, "agent")                               │
│  builder.add_edge("agent", "tools")                             │
│  builder.add_edge("tools", "guard")  # Through guard            │
│  # guard uses Command to route to agent or __end__              │
│                                                                 │
│  ───────────────────────────────────────────────────────────    │
│                                                                 │
│  PATH C: guarded_invoke() Wrapper (Quick Demo)                  │
│  ─────────────────────────────────────────────                  │
│                                                                 │
│  from trajectory_guard import guarded_invoke                    │
│                                                                 │
│  # For existing graphs you can't modify                         │
│  result = guarded_invoke(graph, input, mode="nudge")            │
│                                                                 │
│  Limitation: Less elegant, intercepts stream                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

apply_guard() Implementation
# integrations/apply_guard.py

def apply_guard(
    builder: StateGraph,
    config: Optional[GuardConfig] = None,
    after_node: str = "tools",
    before_node: str = "agent",
) -> StateGraph:
    """
    Inject TrajectoryGuard into an existing graph builder.
    
    Rewires: {after_node} → guard → {before_node}
    """
    guard = TrajectoryGuardNode(config)
    
    # 1. Add the guard node
    builder.add_node("trajectory_guard", guard)
    
    # 2. Remove existing edge (tools → agent)
    # Note: LangGraph doesn't have remove_edge, so we need to 
    # build the graph with guard from the start, or use a 
    # different approach
    
    # 3. Add new edges
    # tools → guard (always)
    # guard → agent (via Command, if not stopping)
    # guard → __end__ (via Command, if stopping)
    
    # The Command pattern handles routing, so we just need:
    builder.add_edge(after_node, "trajectory_guard")
    
    return builder


Observability & Demo Strategy
Langfuse Integration
# observability/langfuse.py

from langfuse.decorators import observe, langfuse_context

class TrajectoryGuardNode:
    
    @observe(name="trajectory_guard")
    def __call__(self, state: AgentState) -> Command:
        # ... detection logic ...
        
        # Score trajectory health (inverse of loop score)
        health = 1.0 - (new_score / MAX_SCORE)
        langfuse_context.score_current_observation(
            name="trajectory_health",
            value=health,
            comment=f"Loop score: {new_score:.2f}"
        )
        
        # Tag if loop detected
        if any(d.detected for d in detections):
            loop_type = self._get_primary_type(detections)
            langfuse_context.update_current_trace(
                tags=["LOOP_DETECTED", loop_type]
            )
        
        # Log intervention
        if intervention == "NUDGE":
            langfuse_context.update_current_observation(
                metadata={"intervention": "NUDGE_SENT"}
            )
        
        # ... rest of logic ...

CloudWatch JSON Logs
# observability/logging.py

import json
import logging
from datetime import datetime

logger = logging.getLogger("trajectory_guard")

def log_event(
    event_type: str,  # "OBSERVE", "NUDGE", "STOP"
    loop_score: float,
    detections: List[DetectionResult],
    step_id: str,
    thread_id: str,
):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TrajectoryGuard",
        "event_type": f"TRAJECTORY_{event_type}",
        "thread_id": thread_id,
        "step_id": step_id,
        "metrics": {
            "loop_score": loop_score,
            "detections": [
                {
                    "type": d.loop_type,
                    "detected": d.detected,
                    "confidence": d.confidence,
                }
                for d in detections
            ],
        },
        "intervention": event_type,
    }
    
    logger.info(json.dumps(log_entry))

Demo Artifacts
┌─────────────────────────────────────────────────────────────────┐
│                      DEMO OUTPUTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. TERMINAL OUTPUT (examples/demo_recovery.py)                 │
│  ──────────────────────────────────────────────                 │
│                                                                 │
│  $ python examples/demo_recovery.py                             │
│                                                                 │
│  [Step 1] search("return policy") → empty                       │
│  [Guard]  ✓ Score: 0.0 | Action: OBSERVE                        │
│                                                                 │
│  [Step 2] search("refund policy") → empty                       │
│  [Guard]  ⚠ Similarity: 0.89 | Score: 0.5 | Action: OBSERVE     │
│                                                                 │
│  [Step 3] search("how to return items") → empty                 │
│  [Guard]  🔴 Type II DETECTED | Score: 2.0 | Action: NUDGE      │
│  [Guard]  💬 Injecting nudge message...                         │
│                                                                 │
│  [Step 4] check_faq("returns") → success ← RECOVERED!           │
│  [Guard]  ✅ Score: 1.0 (decay) | Action: OBSERVE               │
│                                                                 │
│  ══════════════════════════════════════════════════════════════ │
│  RESULT: Task completed in 4 steps                              │
│  Without guardrail: Would have run 30+ steps                    │
│  Estimated savings: $0.45                                       │
│  ══════════════════════════════════════════════════════════════ │
│                                                                 │
│  2. LANGFUSE TRACE                                              │
│  ─────────────────                                              │
│                                                                 │
│  Filter by: tag:LOOP_DETECTED                                   │
│  Shows:                                                         │
│    • Step where loop was caught                                 │
│    • The nudge message injected                                 │
│    • Agent's recovery (or failure)                              │
│    • trajectory_health score over time                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Testing Strategy
Synthetic Loop Fixtures
# tests/fixtures/synthetic_loops.py

TYPE_I_STUTTER = [
    StepRecord(
        tool_name="search",
        tool_args_hash=hash('{"query": "return policy"}'),
        outcome_type="empty",
        ...
    ),
    StepRecord(
        tool_name="search",
        tool_args_hash=hash('{"query": "return policy"}'),  # SAME
        outcome_type="empty",
        ...
    ),
]

TYPE_II_INSANITY = [
    StepRecord(
        tool_name="search",
        thought_embedding=embed("search for return policy"),
        outcome_type="empty",
        ...
    ),
    StepRecord(
        tool_name="search",
        thought_embedding=embed("search for refund policy"),  # Similar!
        outcome_type="empty",
        ...
    ),
    StepRecord(
        tool_name="search",
        thought_embedding=embed("how to return items"),  # Similar!
        outcome_type="empty",
        ...
    ),
]

TYPE_III_PHANTOM = [
    StepRecord(
        tool_name="click",
        tool_args_hash=hash('{"button": "next"}'),
        state_snapshot_hash="abc123",
        ...
    ),
    StepRecord(
        tool_name="click",
        tool_args_hash=hash('{"button": "load_more"}'),  # Different action
        state_snapshot_hash="abc123",  # SAME state!
        ...
    ),
]

TYPE_IV_PINGPONG = [
    StepRecord(agent_id="writer", ...),
    StepRecord(agent_id="critic", ...),
    StepRecord(agent_id="writer", ...),
    StepRecord(agent_id="critic", ...),
    StepRecord(agent_id="writer", ...),  # Pattern: W-C-W-C-W
]

Legitimate Patterns (Should NOT Trigger)
# tests/fixtures/legitimate_patterns.py

VALID_ITERATION = [
    StepRecord(
        tool_name="run_tests",
        outcome_type="error",  # 3 failures
        ...
    ),
    StepRecord(
        tool_name="edit_code",
        outcome_type="success",
        ...
    ),
    StepRecord(
        tool_name="run_tests",
        outcome_type="error",  # 2 failures (progress!)
        ...
    ),
    StepRecord(
        tool_name="edit_code",
        outcome_type="success",
        ...
    ),
    StepRecord(
        tool_name="run_tests",
        outcome_type="success",  # 0 failures!
        ...
    ),
]

# This should NOT trigger - agent is making progress

Sabotaged Agent Test
# examples/sabotaged_agent.py

"""
E2E test: Create an agent that is FORCED to loop,
verify TrajectoryGuard rescues it.
"""

SABOTAGED_PROMPT = """
You are a helpful assistant.

IMPORTANT RULES:
1. Always use the search tool first
2. If search fails, try searching with slightly different words
3. Never give up on searching
4. Do not use any other tools

Your task: Find the return policy.
"""

def test_sabotaged_agent_recovery():
    # Build graph with guard
    builder = StateGraph(AgentState)
    builder.add_node("agent", create_agent(SABOTAGED_PROMPT))
    builder.add_node("tools", tool_node)
    apply_guard(builder)
    graph = builder.compile()
    
    # Run
    result = graph.invoke({"messages": [HumanMessage("Find return policy")]})
    
    # Verify
    loop_status = result.get("loop_status", {})
    
    # Either:
    # A) Agent recovered after nudge
    assert loop_status.get("nudges_sent", 0) >= 1
    # or
    # B) Agent was stopped before wasting too much
    assert loop_status.get("loop_score", 0) <= 5.0
    
    print("✅ Sabotaged agent was handled correctly!")


10-Day Implementation Plan
┌─────────────────────────────────────────────────────────────────┐
│                     10-DAY TIMELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ════════════════════════════════════════════════════════════   │
│  WEEK 1: DETECTION ENGINE                                       │
│  ════════════════════════════════════════════════════════════   │
│                                                                 │
│  DAY 1: Project Scaffold                                        │
│  ────────────────────────                                       │
│  Morning:                                                       │
│    □ Create repo, pyproject.toml                                │
│    □ Set up dependencies:                                       │
│      langgraph>=0.2.60, fastembed>=0.4.1, numpy, langfuse       │
│    □ Create project structure                                   │
│  Afternoon:                                                     │
│    □ Define StepRecord with all fields                          │
│    □ Define AgentState with reducers                            │
│    □ Set up FastEmbed singleton                                 │
│    □ Test embedding works                                       │
│  Tool: Claude Code                                              │
│                                                                 │
│  DAY 2: Type I + Type III Detectors                             │
│  ──────────────────────────────────                             │
│  Morning:                                                       │
│    □ Implement StutterDetector                                  │
│    □ Implement hash normalization (sort JSON keys)              │
│    □ Write unit tests for Type I                                │
│  Afternoon:                                                     │
│    □ Implement PhantomProgressDetector                          │
│    □ Implement state_snapshot_hash logic                        │
│    □ Write unit tests for Type III                              │
│  Tool: Claude Code                                              │
│                                                                 │
│  DAY 3: Type II Detector                                        │
│  ───────────────────────                                        │
│  Morning:                                                       │
│    □ Implement InsanityDetector                                 │
│    □ Implement cosine similarity calculation                    │
│    □ Test with synthetic semantic loops                         │
│  Afternoon:                                                     │
│    □ Implement Negation Heuristic                               │
│    □ Test negation edge cases                                   │
│    □ Tune similarity threshold (0.85)                           │
│  Tool: Claude Code + Cursor for debugging                       │
│                                                                 │
│  DAY 4: Type IV Detector                                        │
│  ───────────────────────                                        │
│  Morning:                                                       │
│    □ Implement PingPongDetector                                 │
│    □ Implement N-gram sequence matching                         │
│    □ Test with multi-agent scenarios                            │
│  Afternoon:                                                     │
│    □ Test with single-agent tool oscillation                    │
│    □ Write unit tests for Type IV                               │
│  Tool: Claude Code                                              │
│                                                                 │
│  DAY 5: Scorer + Unit Tests                                     │
│  ──────────────────────────                                     │
│  Morning:                                                       │
│    □ Implement LoopScorer with weights                          │
│    □ Implement decay logic                                      │
│    □ Test score accumulation                                    │
│  Afternoon:                                                     │
│    □ Create all synthetic fixtures                              │
│    □ Create legitimate pattern fixtures                         │
│    □ Run full detector test suite                               │
│    □ Fix any failures                                           │
│  Tool: pytest, Claude Code                                      │
│                                                                 │
│  ════════════════════════════════════════════════════════════   │
│  WEEK 2: INTEGRATION + OBSERVABILITY                            │
│  ════════════════════════════════════════════════════════════   │
│                                                                 │
│  DAY 6: LangGraph Node                                          │
│  ─────────────────────                                          │
│  Morning:                                                       │
│    □ Implement TrajectoryGuardNode class                        │
│    □ Implement step extraction from state                       │
│    □ Wire up all detectors                                      │
│  Afternoon:                                                     │
│    □ Implement Command returns (OBSERVE/NUDGE/STOP)             │
│    □ Test with simple graph                                     │
│    □ Verify state updates work correctly                        │
│  Tool: Claude Code, LangGraph docs                              │
│                                                                 │
│  DAY 7: Nudge + apply_guard()                                   │
│  ────────────────────────────                                   │
│  Morning:                                                       │
│    □ Implement InterventionManager                              │
│    □ Create all nudge templates (Type I, II, IV)                │
│    □ Create stop payload format                                 │
│  Afternoon:                                                     │
│    □ Implement apply_guard(builder) helper                      │
│    □ Test helper wires graph correctly                          │
│    □ Write basic_usage.py example                               │
│  Tool: Claude Code                                              │
│                                                                 │
│  DAY 8: Langfuse Integration                                    │
│  ──────────────────────────                                     │
│  Morning:                                                       │
│    □ Add @observe decorators                                    │
│    □ Implement trajectory_health scoring                        │
│    □ Add LOOP_DETECTED tags                                     │
│  Afternoon:                                                     │
│    □ Test traces appear in Langfuse                             │
│    □ Build filter view for loop events                          │
│    □ Add structured JSON logging                                │
│  Tool: Langfuse UI, Claude Code                                 │
│                                                                 │
│  DAY 9: E2E Testing                                             │
│  ────────────────────                                           │
│  Morning:                                                       │
│    □ Create sabotaged_agent.py                                  │
│    □ Test: Agent forced to loop                                 │
│    □ Verify: Nudge is sent                                      │
│    □ Verify: Agent recovers OR stops gracefully                 │
│  Afternoon:                                                     │
│    □ Create demo_recovery.py                                    │
│    □ Test full loop → nudge → recovery flow                     │
│    □ Capture terminal output for demo                           │
│    □ Capture Langfuse screenshot for demo                       │
│  Tool: Manual testing, screen recording                         │
│                                                                 │
│  DAY 10: Docs + Ship                                            │
│  ────────────────────                                           │
│  Morning:                                                       │
│    □ Write README with quick start                              │
│    □ Add docstrings to public API                               │
│    □ Write integration guide (3 paths)                          │
│  Afternoon:                                                     │
│    □ Final test run                                             │
│    □ Create CHANGELOG                                           │
│    □ Push to GitHub                                             │
│    □ (Optional) Publish to PyPI                                 │
│  Tool: Claude for docs, manual review                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


AI Tooling Workflow
┌─────────────────────────────────────────────────────────────────┐
│                      AI TOOL USAGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CLAUDE CODE (Primary)                                          │
│  ─────────────────────                                          │
│  Use for:                                                       │
│    • Creating file structure                                    │
│    • Implementing components end-to-end                         │
│    • Running tests                                              │
│    • Git operations                                             │
│                                                                 │
│  Example prompts:                                               │
│    "Create the StepRecord TypedDict with all fields from the   │
│     implementation plan"                                        │
│    "Implement StutterDetector that compares tool_args_hash"    │
│    "Run pytest and fix any failing tests"                       │
│                                                                 │
│  CURSOR (Secondary)                                             │
│  ──────────────────                                             │
│  Use for:                                                       │
│    • Debugging specific issues                                  │
│    • Quick iterations on logic                                  │
│    • Understanding LangGraph patterns                           │
│                                                                 │
│  CLAUDE CHAT (Planning)                                         │
│  ──────────────────────                                         │
│  Use for:                                                       │
│    • Architecture decisions                                     │
│    • Reviewing approaches                                       │
│    • Documentation                                              │
│                                                                 │
│  PROMPTING TIPS:                                                │
│  ───────────────                                                │
│  ❌ "Build me a loop detector"                                  │
│  ✅ "Create StutterDetector class with detect(current, history) │
│      method that returns DetectionResult. Compare tool_args_hash│
│      of current step vs history[-1]. Return detected=True if    │
│      they match."                                               │
│                                                                 │
│  Be SPECIFIC about:                                             │
│    • Class/function names                                       │
│    • Input/output types                                         │
│    • Logic to implement                                         │
│    • Which LangGraph patterns to use                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Summary: What You're Building
┌─────────────────────────────────────────────────────────────────┐
│                    MVP-V1 DELIVERABLES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CORE LIBRARY:                                                  │
│    • 4 detectors (Stutter, Insanity, PhantomProgress, PingPong) │
│    • StepRecord with state_snapshot_hash for Type III           │
│    • Loop scorer with decay                                     │
│    • Nudge message templates                                    │
│    • Embedding service (FastEmbed + BGE-small)                  │
│                                                                 │
│  INTEGRATIONS:                                                  │
│    • TrajectoryGuardNode (graph-native)                         │
│    • apply_guard(builder) helper (recommended)                  │
│    • Langfuse scoring + tagging                                 │
│    • Structured JSON logging                                    │
│                                                                 │
│  TESTS:                                                         │
│    • Synthetic loop fixtures (all 4 types)                      │
│    • Legitimate pattern fixtures (should NOT trigger)           │
│    • Sabotaged agent E2E test                                   │
│                                                                 │
│  DEMOS:                                                         │
│    • demo_recovery.py (loop → nudge → success)                  │
│    • Terminal output with color-coded status                    │
│    • Langfuse trace showing intervention                        │
│                                                                 │
│  DOCUMENTATION:                                                 │
│    • README with quick start                                    │
│    • Integration guide (3 paths)                                │
│    • Threshold tuning guide                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


Key Changes from v1
Aspect
v1
v2
Timeline
14 days
10 days (tighter)
Type III detection
outcome_type classification
state_snapshot_hash (explicit)
Primary integration
Manual node
apply_guard(builder) helper
E2E test
Generic
Sabotaged agent (forced loops)
Thresholds
NUDGE=2.0, STOP=3.5
NUDGE=2.0, STOP=3.0
StepRecord
Missing state hash
Has state_snapshot_hash


Implementation Plan v2 Timeline: 10 days Tools: Claude Code + Cursor + Claude


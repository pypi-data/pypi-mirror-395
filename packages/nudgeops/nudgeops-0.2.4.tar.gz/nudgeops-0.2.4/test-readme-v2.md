NudgeOps Mock Testing Framework: Complete Implementation Guide
Table of Contents
Executive Summary
The Core Insight
Architecture Overview
The Four Loop Types Explained
Interface Layer: Domain-Agnostic Contracts
Code Agent Mocking
Shopping Agent Mocking
The Step Adapter: Bridging Environments to Detectors
Universal Guard: Integration for Any Framework
Complete Test Suite
File Structure Summary
Integration Examples

1. Executive Summary
What This Document Covers
This document provides a complete, self-contained implementation of mock testing for NudgeOps - a runtime semantic guardrail system that detects when AI agents are stuck in loops.
The Problem We're Solving
AI agents (whether coding assistants like Cursor/Claude Code or shopping bots) fail in predictable ways:
Failure Mode
Example
Cost
Infinite edit loops
Agent fixes bug A, breaks B, fixes B, breaks A...
Wasted tokens, no progress
Semantic repetition
Agent searches "laptop", "notebook", "portable computer"
Same intent, no new info
Phantom progress
Agent clicks buttons but cart stays empty
Actions without state change
Multi-agent ping-pong
Agent A hands to B, B hands to A, repeat
Coordination deadlock

Why Mock Testing?
Real agent failures are:
Expensive: Real LLM calls cost money
Non-deterministic: Hard to reproduce exact failure conditions
Slow: Minutes per test vs milliseconds
Mock testing is:
Free: No API calls
Deterministic: Exact same failure every time
Fast: 100-500x faster iteration
The Key Insight
Your detectors don't care if a StepRecord came from a shopping agent or a code agent.
The StepRecord is domain-agnostic:
StepRecord(
    tool_name: str,           # "edit_file" OR "add_to_cart" - doesn't matter
    tool_args_hash: str,      # Hash of arguments - universal
    thought_embedding: list,  # Semantic vector - universal
    state_snapshot_hash: str, # Did state change? - universal
    agent_id: str | None,     # For multi-agent - universal
    outcome_type: str,        # success/empty/error - universal
)

Therefore:
Detectors stay unchanged (already domain-agnostic)
Only mock environments are domain-specific (simulate code repo vs shopping site)
Same architecture handles ALL agent types

2. The Core Insight
The Detector-Environment Separation
┌─────────────────────────────────────────────────────────────────────────┐
│                         NUDGEOPS ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DOMAIN-SPECIFIC LAYER (what we're building)                           │
│  ────────────────────────────────────────────                          │
│                                                                         │
│  ┌─────────────────────┐     ┌─────────────────────┐                   │
│  │ MockCodeEnvironment │     │ MockShoppingEnv     │                   │
│  │                     │     │                     │                   │
│  │ - files: Dict       │     │ - cart: List        │                   │
│  │ - tests_passed: bool│     │ - current_page: str │                   │
│  │ - compile_errors    │     │ - variants          │                   │
│  └──────────┬──────────┘     └──────────┬──────────┘                   │
│             │                           │                               │
│             ▼                           ▼                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Scenario Behaviors                            │   │
│  │  (Functions that define HOW the environment responds)            │   │
│  │                                                                   │   │
│  │  Code:                        Shopping:                          │   │
│  │  - infinite_edit_loop         - variant_oos_loop                 │   │
│  │  - compile_retry_loop         - checkout_sequence_error          │   │
│  │  - submit_spam_loop           - search_synonym_loop              │   │
│  │  - phantom_edit               - add_to_cart_retry                │   │
│  │  - hallucinated_library       - ping_pong_handoff                │   │
│  └──────────────────────────────────┬──────────────────────────────┘   │
│                                     │                                   │
│                                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Step Adapter                                  │   │
│  │  build_step_record(action, result, env) -> StepRecord           │   │
│  │  (Same function for ALL domains)                                 │   │
│  └──────────────────────────────────┬──────────────────────────────┘   │
│                                     │                                   │
├─────────────────────────────────────┼───────────────────────────────────┤
│                                     │                                   │
│  DOMAIN-AGNOSTIC LAYER (already built)                                 │
│  ─────────────────────────────────────                                 │
│                                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    StepRecord                                    │   │
│  │  (Universal data structure - detectors only see this)           │   │
│  └──────────────────────────────────┬──────────────────────────────┘   │
│                                     │                                   │
│                                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Detectors                                     │   │
│  │  - StutterDetector (Type I)                                     │   │
│  │  - InsanityDetector (Type II)                                   │   │
│  │  - PhantomProgressDetector (Type III)                           │   │
│  │  - PingPongDetector (Type IV)                                   │   │
│  └──────────────────────────────────┬──────────────────────────────┘   │
│                                     │                                   │
│                                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Scorer                                        │   │
│  │  score = accumulate(detections) with decay                      │   │
│  └──────────────────────────────────┬──────────────────────────────┘   │
│                                     │                                   │
│                                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Decision                                      │   │
│  │  OBSERVE (< 2.0) | NUDGE (>= 2.0) | STOP (>= 3.0)              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


3. Architecture Overview
Layer-by-Layer Breakdown
Layer
Purpose
Domain-Specific?
IMockEnvironment
Universal interface for all environments
❌ No
MockCodeEnvironment
Simulates a code repo with files, tests, commits
✅ Yes
MockShoppingEnvironment
Simulates e-commerce with cart, variants, checkout
✅ Yes
Scenario Behaviors
Functions that define failure patterns
✅ Yes
build_step_record()
Converts (Action, Result, Env) → StepRecord
❌ No
Detectors
Analyze StepRecords for loop patterns
❌ No
Scorer
Accumulate scores with decay
❌ No
UniversalGuard
Easy integration API for any framework
❌ No

Data Flow
1. Test creates MockEnvironment with specific scenario behavior
2. Test simulates agent actions via Action objects
3. Environment returns Result based on scenario logic
4. Step Adapter converts (Action, Result, Env) → StepRecord
5. Detectors analyze StepRecord against history
6. Scorer updates cumulative score
7. Test asserts score crosses appropriate threshold


4. The Four Loop Types Explained
Type I: Stutter (Exact Repetition)
What it detects: Agent does the EXACT same thing multiple times.
Detection method: Hash comparison of tool_name + tool_args.
Code agent example:
Step 1: run_tests {}           → hash: abc123
Step 2: run_tests {}           → hash: abc123  ← MATCH!
Step 3: run_tests {}           → hash: abc123  ← MATCH!

Agent keeps running tests hoping they'll magically pass.
Shopping agent example:
Step 1: add_to_cart {sku: "ABC"}  → hash: def456
Step 2: add_to_cart {sku: "ABC"}  → hash: def456  ← MATCH!

Agent clicks "Add to Cart" repeatedly without selecting size.
Why it matters: Wasted compute on identical operations that won't succeed.
Score weight: +2.0 per detection

Type II: Insanity (Semantic Repetition)
What it detects: Agent does SEMANTICALLY similar things (different words, same intent).
Detection method: Embedding similarity > 0.85 threshold.
Code agent example:
Step 1: thought="Fix the bug in auth.py"        → embed: [0.8, 0.2, ...]
Step 2: thought="Patch the authentication file" → embed: [0.79, 0.21, ...]  ← Similar!
Step 3: thought="Repair auth module"            → embed: [0.81, 0.19, ...]  ← Similar!

Agent keeps trying variations of the same fix approach.
Shopping agent example:
Step 1: search {query: "laptop"}              → embed: [0.9, 0.1, ...]
Step 2: search {query: "notebook computer"}   → embed: [0.88, 0.12, ...]  ← Similar!
Step 3: search {query: "portable PC"}         → embed: [0.91, 0.09, ...]  ← Similar!

Agent searches synonyms expecting different results.
Why it matters: Agent is stuck on one strategy without realizing it's failing.
Score weight: +1.5 per detection (requires count >= 3)

Type III: Phantom Progress (No State Change)
What it detects: Agent takes actions but nothing actually changes.
Detection method: state_snapshot_hash remains identical across steps.
Code agent example:
Step 1: edit_file {file: "main.py"}  → state_hash: xyz789
        (But file is read-only, write silently fails)
Step 2: run_tests {}                 → state_hash: xyz789  ← UNCHANGED!
Step 3: edit_file {file: "main.py"}  → state_hash: xyz789  ← UNCHANGED!

Agent thinks it's editing but the file system is rejecting writes.
Shopping agent example:
Step 1: click_pay_now {}     → state_hash: ghi012
        (Error: "Complete shipping first")
Step 2: click_pay_now {}     → state_hash: ghi012  ← UNCHANGED!
Step 3: click_pay_now {}     → state_hash: ghi012  ← UNCHANGED!

Agent clicks "Pay Now" repeatedly without completing prerequisites.
Why it matters: Agent believes it's making progress when it isn't.
Score weight: +0.5 per detection

Type IV: Ping-Pong (Multi-Agent Handoff Loop)
What it detects: Two or more agents passing task back and forth.
Detection method: Pattern matching on agent_id sequence: A→B→A→B.
Code agent example:
Step 1: agent_id="planner"    action=handoff(to="coder")
Step 2: agent_id="coder"      action=handoff(to="planner")  
Step 3: agent_id="planner"    action=handoff(to="coder")    ← Pattern!
Step 4: agent_id="coder"      action=handoff(to="planner")  ← Pattern!

Planner and coder keep delegating without doing work.
Shopping agent example:
Step 1: agent_id="search"     action=handoff(to="compare")
Step 2: agent_id="compare"    action=handoff(to="search")
Step 3: agent_id="search"     action=handoff(to="compare")  ← Pattern!

Search and comparison agents loop without deciding.
Why it matters: Multi-agent coordination failure wastes resources.
Score weight: +1.5 per detection

Combined Detection Example
Real failures often trigger MULTIPLE types:
Scenario: Agent tries to fix a bug but tests always fail

Step 1: edit_file {"file": "foo.py", "line": 42}
        thought: "Fix the null pointer in foo.py"
        state_hash: aaa111
        → No detection yet

Step 2: run_tests {}
        thought: "Run tests to verify fix"
        state_hash: aaa111 (tests failed, same signature)
        → Type III detected (state unchanged)

Step 3: edit_file {"file": "foo.py", "line": 42}
        thought: "Try another fix for foo.py line 42"
        state_hash: aaa111
        → Type I detected (same tool + args)
        → Type II detected (similar thought to Step 1)
        → Type III detected (state still unchanged)

Step 4: run_tests {}
        thought: "Check if new fix works"
        state_hash: aaa111
        → Type I detected (same as Step 2)
        → Type III detected (state STILL unchanged)

Score progression:
  Step 1: 0.0
  Step 2: 0.0 + 0.5 (Type III) = 0.5
  Step 3: 0.5 + 2.0 (Type I) + 1.5 (Type II) + 0.5 (Type III) = 4.5
  
Result: STOP triggered at Step 3 (score 4.5 >= 3.0)


5. Interface Layer: Domain-Agnostic Contracts
File: nudgeops/testing/interfaces.py
This file defines the universal contracts that ALL mock environments must implement.
"""
nudgeops/testing/interfaces.py

Universal interface definitions for mock testing.

These are DOMAIN-AGNOSTIC - they don't know about code vs shopping.
Any environment (code, shopping, research, data analysis) implements
the same IMockEnvironment protocol.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Protocol, Literal

# Outcome types match your existing StepRecord.outcome_type
OutcomeType = Literal["success", "empty", "error"]


@dataclass
class Action:
    """
    Represents an agent's intended action.
    
    This is domain-agnostic:
    - Code agent: tool_name="edit_file", tool_args={"file": "main.py"}
    - Shopping agent: tool_name="add_to_cart", tool_args={"sku": "ABC123"}
    
    Attributes:
        tool_name: The tool/action being invoked
        tool_args: Arguments passed to the tool
        thought_text: The agent's reasoning before this action
                      (Used for semantic similarity detection - Type II)
    """
    tool_name: str
    tool_args: Dict[str, Any]
    thought_text: str


@dataclass
class Result:
    """
    Represents the environment's response to an action.
    
    Attributes:
        outcome_type: "success" | "empty" | "error"
        message: Human-readable description (for debugging/logging)
        state_changed: Did this action actually change the environment state?
                       This is a HINT for scenario logic - the guard ultimately
                       uses state_snapshot_hash for ground truth.
    """
    outcome_type: OutcomeType
    message: str
    state_changed: bool


class IMockEnvironment(Protocol):
    """
    Universal interface for mock environments.
    
    Every domain (code, shopping, research, etc.) implements this SAME interface.
    This is what makes NudgeOps domain-agnostic - detectors only see StepRecords,
    and StepRecords come from this universal interface.
    
    Methods:
        execute_action: Run an action and get a result
        get_state_hash: Get a hash representing current state (for Type III detection)
        reset: Reset environment to initial state (for test isolation)
    """
    
    def execute_action(self, action: Action) -> Result:
        """
        Execute an action in the mock environment.
        
        The implementation decides:
        - What outcome_type to return
        - What message to include
        - Whether state actually changed
        
        This is where SCENARIO LOGIC lives - different scenarios
        return different results for the same action.
        """
        ...
    
    def get_state_hash(self) -> str:
        """
        Return a hash representing the current environment state.
        
        CRITICAL: This hash is used for Type III (Phantom Progress) detection.
        If the hash doesn't change between steps, the guard knows the agent
        isn't making real progress.
        
        What to include in the hash:
        - Goal-relevant state (tests passing, cart contents, checkout step)
        - NOT raw file contents (too noisy)
        - NOT timestamps (always changes)
        
        Example for code: hash(tests_passed, failing_test_names, commit_count)
        Example for shopping: hash(cart_items, checkout_step, selected_variant)
        """
        ...
    
    def reset(self) -> None:
        """
        Reset environment to initial state.
        
        Called between tests to ensure isolation.
        """
        ...

Why This Design?
Protocol, not ABC: We use typing.Protocol so implementations don't need to inherit from a base class. This is more Pythonic and flexible.


Minimal interface: Only 3 methods. Easy to implement for any domain.


state_changed is a hint: The scenario can say "state changed" but the guard verifies via get_state_hash(). This catches bugs where the scenario lies.


thought_text in Action: This enables Type II (semantic) detection - we compare embeddings of thoughts across steps.



6. Code Agent Mocking
File: nudgeops/testing/environments/code_env.py
This simulates a code repository with files, tests, and commits.
"""
nudgeops/testing/environments/code_env.py

Mock environment for testing code agent loop detection.

Simulates a minimal code repository with:
- Files (as a dict of filename -> content)
- Test status (passed/failed + which tests are failing)
- Commit count (for tracking submit loops)

The key insight: We don't need a real compiler or test runner.
We only need to track GOAL-RELEVANT STATE that the agent should change.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Optional
import hashlib

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment


@dataclass
class CodeState:
    """
    Goal-centric view of a code session.
    
    We track what matters for detecting loops:
    - tests_passed: Has the agent achieved the goal?
    - failing_signature: Which tests are failing? (same signature = no progress)
    - commit_count: How many commits? (used for submit spam detection)
    
    We intentionally DON'T track:
    - Exact file contents (too noisy, not goal-relevant)
    - Timestamps (always changes, not meaningful)
    - Line numbers edited (implementation detail)
    """
    files: Dict[str, str] = field(default_factory=dict)
    tests_passed: bool = False
    failing_signature: str = ""  # e.g., "test_foo, test_bar"
    commit_count: int = 0


# Type alias for scenario behavior functions
ScenarioBehavior = Callable[[CodeState, Action], Result]


class MockCodeEnvironment(IMockEnvironment):
    """
    Simulates a code repo for loop detection testing.
    
    Usage:
        # Create with a specific failure scenario
        env = MockCodeEnvironment(infinite_edit_loop_behavior)
        
        # Simulate agent actions
        action = Action("edit_file", {"file": "main.py"}, "Fix the bug")
        result = env.execute_action(action)
        
        # Get state hash for detection
        hash = env.get_state_hash()
    
    The scenario_behavior function is what makes each test case unique.
    Same environment class, different behaviors = different failure patterns.
    """
    
    def __init__(self, scenario_behavior: Optional[ScenarioBehavior] = None):
        """
        Initialize with optional scenario behavior.
        
        If no behavior provided, uses default "happy path" where
        tests eventually pass (for testing false positive avoidance).
        """
        self._state = CodeState()
        self._behavior = scenario_behavior or self._default_behavior
    
    def execute_action(self, action: Action) -> Result:
        """
        Execute action using the scenario behavior.
        
        The behavior function gets full access to state and can:
        - Mutate state (or not)
        - Return any outcome_type
        - Set state_changed appropriately
        """
        return self._behavior(self._state, action)
    
    def get_state_hash(self) -> str:
        """
        Hash the GOAL-RELEVANT state.
        
        We hash:
        - tests_passed: The ultimate goal
        - failing_signature: Which tests are broken
        - commit_count: Track submit spam
        
        If this hash doesn't change, the agent isn't making progress
        toward its goal, even if it's taking actions.
        """
        payload = (
            self._state.tests_passed,
            self._state.failing_signature,
            self._state.commit_count,
        )
        return hashlib.sha256(repr(payload).encode()).hexdigest()
    
    def reset(self) -> None:
        """Reset to clean state for test isolation."""
        self._state = CodeState()
    
    def _default_behavior(self, state: CodeState, action: Action) -> Result:
        """
        Default "happy path" behavior.
        
        Used when testing that LEGITIMATE patterns don't trigger detection.
        
        Behavior:
        - edit_file: Succeeds, but tests still fail initially
        - run_tests: First call fails, second call passes
        - git_commit: Always succeeds, increments commit count
        """
        tool = action.tool_name
        
        if tool == "edit_file":
            filename = action.tool_args.get("file", "main.py")
            state.files[filename] = state.files.get(filename, "") + "\n# edited"
            return Result("success", "File edited", state_changed=True)
        
        if tool == "run_tests":
            if state.tests_passed:
                return Result("success", "All tests passed", state_changed=False)
            else:
                # Simulate: first run fails, subsequent runs pass
                # This represents a legitimate fix-and-verify cycle
                state.tests_passed = True
                state.failing_signature = ""
                return Result("success", "Tests now passing", state_changed=True)
        
        if tool in {"git_commit", "submit_patch"}:
            state.commit_count += 1
            return Result("success", "Committed", state_changed=True)
        
        return Result("empty", f"Unknown tool: {tool}", state_changed=False)

File: nudgeops/testing/scenarios/code_scenarios.py
These are the FAILURE PATTERNS for code agents.
"""
nudgeops/testing/scenarios/code_scenarios.py

Scenario behaviors that simulate common code agent failures.

Each function is a ScenarioBehavior that can be passed to MockCodeEnvironment.
They define HOW the environment responds to actions in ways that trigger loops.

These scenarios are derived from real failures in:
- SWE-agent (29.5% loop rate with Claude Sonnet 4)
- Cursor IDE ("fix-break-fix" oscillations)
- Claude Code (UI implementation loops)
- Devin (web scraping failure cycles)

Research source: "Scaling Shopping Web Agents" + SWE-bench analysis
"""

from __future__ import annotations
from nudgeops.testing.environments.code_env import CodeState
from nudgeops.testing.interfaces import Action, Result


def infinite_edit_loop_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Infinite Edit Loop (Fix-Break-Fix Oscillation)
    
    REAL-WORLD ANALOGUE:
    Cursor/Claude Code rewrites the same function repeatedly.
    Each edit "fixes" something but tests still fail with the same signature.
    
    WHAT HAPPENS:
    - edit_file: Succeeds (file changes)
    - run_tests: ALWAYS fails with same error signature
    
    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Same edit_file tool + args pattern
    - Type II (Insanity): Semantically similar "fix the bug" thoughts
    - Type III (Phantom): State hash unchanged (tests never pass)
    
    WHY THIS MATTERS:
    The agent is stuck in a local minimum. It correctly identifies the error
    but its fix approach is fundamentally wrong. It needs to "zoom out"
    and try a different strategy, but instead it keeps making small variations
    of the same broken fix.
    
    TOKEN COST: Can burn 2000+ tokens on repeated edit/test cycles
    """
    tool = action.tool_name
    
    if tool == "edit_file":
        # Accept the edit - file content changes
        filename = action.tool_args.get("file", "main.py")
        state.files[filename] = "modified code"
        # But tests will still fail - this is the trap
        state.tests_passed = False
        state.failing_signature = "test_foo, test_bar"  # Same signature every time
        return Result(
            outcome_type="success",
            message="File edited successfully",
            state_changed=True,  # File DID change...
        )
    
    if tool == "run_tests":
        # Tests ALWAYS fail with the same signature
        state.tests_passed = False
        state.failing_signature = "test_foo, test_bar"
        return Result(
            outcome_type="error",
            message="2 tests failed: test_foo, test_bar",
            state_changed=False,  # ...but goal state DIDN'T change
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def compile_retry_loop_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Compilation Retry Loop
    
    REAL-WORLD ANALOGUE:
    SWE-agent / Claude Sonnet keeps trying small syntactic tweaks.
    The same compile error appears every time.
    
    WHAT HAPPENS:
    - compile: ALWAYS fails with same error
    - Agent tries slight variations but error persists
    
    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Same compile command
    - Type III (Phantom): Error signature never changes
    
    RESEARCH DATA:
    SWE-bench Pro analysis: Claude Sonnet 4 shows 29.5% "stuck in loop" rate
    among non-submitted cases, vs only 0.4% for GPT-5.
    
    The critical failure: Agent doesn't recognize that its FIX APPROACH
    is fundamentally broken. It keeps attempting syntactic variations
    when the problem is semantic.
    """
    tool = action.tool_name
    
    if tool == "compile":
        state.tests_passed = False
        state.failing_signature = "SyntaxError: unexpected indent line 42"
        return Result(
            outcome_type="error",
            message="SyntaxError: unexpected indent line 42",
            state_changed=False,
        )
    
    if tool == "edit_file":
        # Agent edits file, but the compile error will persist
        filename = action.tool_args.get("file", "main.py")
        state.files[filename] = "edited"
        return Result("success", "File edited", state_changed=True)
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def submit_spam_loop_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Submit/Commit Spam Loop
    
    REAL-WORLD ANALOGUE:
    SWE-agent Issue #971: Agent calls submit command 24+ times.
    Each call returns "command ran successfully with no output".
    Agent interprets this as "didn't work, try again".
    
    WHAT HAPPENS:
    - submit_patch / git_commit: Returns "success" with no output
    - But state NEVER changes (commit_count stays same)
    - Agent sees "success" but nothing happened
    
    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Exact same command repeated
    - Type III (Phantom): state_hash constant despite "success"
    
    THE TRAP:
    The Result says "success" but state_changed=False.
    This simulates silent failures where the tool reports success
    but nothing actually happened (e.g., git push with no changes,
    or a dry-run mode that wasn't detected).
    
    COST: $0.16+ per stuck session (rapid API calls)
    """
    tool = action.tool_name
    
    if tool in {"submit_patch", "git_commit", "git_push"}:
        # DON'T increment commit_count - nothing actually happened
        # This is the key: we claim success but state is unchanged
        return Result(
            outcome_type="success",  # Tool says it worked
            message="command ran successfully with no output",
            state_changed=False,  # But nothing changed!
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def phantom_edit_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Phantom Edit (Groundhog Day File System)
    
    REAL-WORLD ANALOGUE:
    - File is read-only but tool doesn't report error
    - File locked by another process
    - Regex-based edit tool silently fails (pattern doesn't match)
    - AST parser fails on syntax errors, aborts silently
    
    WHAT HAPPENS:
    - edit_file: Returns "success" but file content unchanged
    - Agent thinks edit worked, proceeds to run tests
    - Tests fail because the "fix" was never applied
    - Agent is debugging code that doesn't exist
    
    LOOP TYPES TRIGGERED:
    - Type III (Phantom): Primary detection - state never changes
    - Type I (Stutter): If agent retries same edit
    
    WHY THIS IS INSIDIOUS:
    The agent's internal world model diverges from reality.
    It believes variable_x is defined. When tests fail with
    "NameError: variable_x is not defined", the agent assumes
    there's a scoping issue, not that its edit failed.
    
    SOLUTION: Agent should verify file contents after editing.
    """
    tool = action.tool_name
    
    if tool == "edit_file":
        # Claim success but DON'T actually change anything
        return Result(
            outcome_type="success",
            message="File saved successfully",
            state_changed=False,  # The lie
        )
    
    if tool == "read_file":
        # Return OLD content, proving the edit didn't work
        return Result(
            outcome_type="success",
            message="def old_unchanged_code(): pass",
            state_changed=False,
        )
    
    if tool == "run_tests":
        # Tests fail because the "fix" was never applied
        state.tests_passed = False
        state.failing_signature = "NameError: name 'variable_x' is not defined"
        return Result(
            outcome_type="error",
            message="NameError: name 'variable_x' is not defined",
            state_changed=False,
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def hallucinated_library_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Hallucinated Library Loop (PyPI Void)
    
    REAL-WORLD ANALOGUE:
    LLMs are trained on deprecated libraries, beta APIs that never launched,
    and "common misconceptions" from forums. Agent confidently imports
    `pandas.utils.testing` (deprecated) or `aws_s3_easy_uploader` (fictional).
    
    WHAT HAPPENS:
    - pip_install: ALWAYS fails (package doesn't exist)
    - Agent tries variations: binary-converter-pro, binary_converter, etc.
    - Never falls back to implementing from scratch
    
    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Same install command pattern
    - Type II (Insanity): Semantic variations of "install this library"
    
    DANGER: Typosquatting
    In worst case, agent might install a MALICIOUS package with
    a similar name to the hallucinated one.
    
    DESIRED BEHAVIOR:
    After 2-3 failed installs, agent should:
    1. Realize the library doesn't exist
    2. Fall back to implementing functionality from scratch
    """
    tool = action.tool_name
    
    if tool == "pip_install":
        package = action.tool_args.get("package", "unknown")
        return Result(
            outcome_type="error",
            message=f"ERROR: Could not find a version that satisfies the requirement {package}",
            state_changed=False,
        )
    
    if tool == "import":
        module = action.tool_args.get("module", "unknown")
        return Result(
            outcome_type="error",
            message=f"ModuleNotFoundError: No module named '{module}'",
            state_changed=False,
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def hallucination_spiral_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Hallucination Spiral (Cascading Fabrication)
    
    REAL-WORLD ANALOGUE:
    Surge AI's analysis of Gemini 2.5 Pro on SWE-bench:
    - File read returns truncated output
    - Model invents BaseWriter class
    - Fabricates method body
    - Hallucinates terminal output
    - 39 turns, 693 lines modified, codebase destroyed
    - Model kept insisting "the core logic of my proposed fix is sound"
    
    WHAT HAPPENS:
    - edit_file: Keeps creating imaginary classes
    - run_tests: Always fails (the classes don't work)
    - Agent's confidence never wavers
    
    LOOP TYPES TRIGGERED:
    - Type II (Insanity): Semantic repetition on "fix BaseWriter"
    - Type III (Phantom): Tests never pass
    
    THIS IS THE WORST CASE:
    Agent is confidently wrong and actively destroying the codebase.
    Each "fix" makes things worse but the agent doesn't recognize it.
    """
    tool = action.tool_name
    
    if tool == "edit_file":
        # Track number of hallucination attempts
        attempt = len(state.files)
        state.files[f"base_writer_v{attempt}.py"] = f"class BaseWriter: # attempt {attempt}"
        state.tests_passed = False
        state.failing_signature = "ImportError: cannot import 'BaseWriter'"
        return Result(
            outcome_type="success",
            message=f"Created BaseWriter class (attempt {attempt})",
            state_changed=True,  # Files are changing...
        )
    
    if tool == "run_tests":
        state.tests_passed = False
        state.failing_signature = "ImportError: cannot import 'BaseWriter'"
        return Result(
            outcome_type="error",
            message="ImportError: cannot import 'BaseWriter'",
            state_changed=False,  # ...but goal never achieved
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def daemon_linter_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Daemon Linter (Impossible Task)
    
    PURPOSE: Measure "Time To Give Up" (TTGU)
    
    WHAT HAPPENS:
    - run_linter: ALWAYS fails with same error, regardless of edits
    - This is an IMPOSSIBLE task by design
    
    WHAT WE'RE TESTING:
    Does the agent recognize when a task is impossible?
    A good agent should:
    1. Try 2-3 times
    2. Realize the linter itself might be broken
    3. Try a different tool (different linter, or skip linting)
    4. Or conclude the task is impossible and stop
    
    A bad agent will:
    1. Rewrite line 42 forever
    2. Never question the linter
    3. Consume infinite tokens
    
    METRIC: Steps until STOP threshold reached
    Good: 5-7 steps
    Bad: 20+ steps
    """
    tool = action.tool_name
    
    if tool == "run_linter":
        # ALWAYS return the same error, no matter what
        return Result(
            outcome_type="error",
            message="Error: Critical Syntax Failure on Line 42",
            state_changed=False,
        )
    
    if tool == "edit_file":
        # Accept edits, but linter will still fail
        filename = action.tool_args.get("file", "main.py")
        state.files[filename] = "perfectly valid code"
        return Result("success", "File edited", state_changed=True)
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


def ping_pong_handoff_behavior(state: CodeState, action: Action) -> Result:
    """
    SCENARIO: Multi-Agent Ping-Pong
    
    REAL-WORLD ANALOGUE:
    - Planner agent delegates to Coder
    - Coder delegates back to Planner ("I need more context")
    - Planner delegates to Coder again
    - Repeat forever
    
    WHAT HAPPENS:
    - handoff: Always "succeeds" but no work gets done
    - State never changes
    
    LOOP TYPES TRIGGERED:
    - Type IV (Ping-Pong): A→B→A→B pattern in agent_id
    - Type III (Phantom): No state progress
    
    THIS SIMULATES:
    AutoGen state isolation loops (Issue #5317)
    CrewAI delegation chains (Issue #6)
    LangChain multi-agent handoff failures
    
    THE $47K DISASTER:
    Four LangChain agents researching market data got stuck for 11 days.
    Cost: Week 1 ($127) → Week 4 ($18,400) → Total $47,000
    Detection method: Catastrophic API bill
    """
    tool = action.tool_name
    
    if tool == "handoff":
        target = action.tool_args.get("to", "other_agent")
        # Handoff "succeeds" but no actual work happens
        return Result(
            outcome_type="success",
            message=f"Task handed off to {target}",
            state_changed=False,  # No progress!
        )
    
    return Result("empty", f"Unknown tool: {tool}", state_changed=False)


7. Shopping Agent Mocking
File: nudgeops/testing/environments/shopping_env.py
"""
nudgeops/testing/environments/shopping_env.py

Mock environment for testing shopping agent loop detection.

Simulates an e-commerce site with:
- Cart (items with SKU, size, quantity)
- Variant selection (size, color, etc.)
- Checkout flow (multi-step: shipping → payment → confirm)

Based on failures from Amazon's "Buy For Me" research:
- 61% → 91% success rate improvement via loop detection
- Common failures: OOS misdetection, button confusion, checkout sequence errors
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
import hashlib

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment


@dataclass
class ShoppingState:
    """
    Goal-centric view of a shopping session.
    
    We track:
    - cart: Items added (the goal is usually to have items in cart)
    - selected_variant: Current size/color selection
    - checkout_step: Progress through checkout funnel
    - last_error: Most recent error (for debugging)
    """
    current_page: str = "home"
    cart: List[Dict] = field(default_factory=list)
    selected_variant: Optional[str] = None
    checkout_step: int = 0  # 0=browsing, 1=shipping, 2=payment, 3=confirmed
    last_error: str = ""


ScenarioBehavior = Callable[[ShoppingState, Action], Result]


class MockShoppingEnvironment(IMockEnvironment):
    """
    Simulates an e-commerce site for loop detection testing.
    
    Usage:
        env = MockShoppingEnvironment(variant_oos_loop_behavior)
        action = Action("select_variant", {"size": "XL"}, "Try size XL")
        result = env.execute_action(action)
    """
    
    def __init__(self, scenario_behavior: Optional[ScenarioBehavior] = None):
        self._state = ShoppingState()
        self._behavior = scenario_behavior or self._default_behavior
    
    def execute_action(self, action: Action) -> Result:
        return self._behavior(self._state, action)
    
    def get_state_hash(self) -> str:
        """
        Hash goal-relevant shopping state.
        
        Includes:
        - Cart contents (the main goal)
        - Selected variant
        - Checkout progress
        - Last error (different errors = different states)
        """
        cart_tuple = tuple(
            (item.get("sku"), item.get("size"), item.get("qty"))
            for item in self._state.cart
        )
        payload = (
            cart_tuple,
            self._state.selected_variant,
            self._state.checkout_step,
            self._state.last_error,
        )
        return hashlib.sha256(repr(payload).encode()).hexdigest()
    
    def reset(self) -> None:
        self._state = ShoppingState()
    
    def _default_behavior(self, state: ShoppingState, action: Action) -> Result:
        """Default happy-path behavior for testing false positives."""
        tool = action.tool_name
        
        if tool == "select_variant":
            state.selected_variant = action.tool_args.get("size")
            state.last_error = ""
            return Result("success", f"Selected {state.selected_variant}", True)
        
        if tool == "add_to_cart":
            if not state.selected_variant:
                state.last_error = "Please select a size"
                return Result("error", state.last_error, False)
            state.cart.append({
                "sku": action.tool_args.get("sku", "SKU123"),
                "size": state.selected_variant,
                "qty": action.tool_args.get("qty", 1),
            })
            state.last_error = ""
            return Result("success", "Added to cart", True)
        
        if tool == "checkout":
            if not state.cart:
                state.last_error = "Cart is empty"
                return Result("error", state.last_error, False)
            state.checkout_step = 1
            return Result("success", "Proceeding to checkout", True)
        
        return Result("empty", f"Unknown tool: {tool}", False)

File: nudgeops/testing/scenarios/shopping_scenarios.py
"""
nudgeops/testing/scenarios/shopping_scenarios.py

Scenario behaviors that simulate common shopping agent failures.

Based on Amazon's "Scaling Shopping Web Agents" research:
- Purchase Success Rate went from 61% to 91% via systematic failure analysis
- Main failure categories: Image Perception Error, Wrong Action Intent, etc.

These scenarios recreate the exact failure patterns observed in production.
"""

from __future__ import annotations
from nudgeops.testing.environments.shopping_env import ShoppingState
from nudgeops.testing.interfaces import Action, Result


def variant_oos_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Variant Out-of-Stock Loop
    
    REAL-WORLD ANALOGUE:
    User wants size XL. Agent tries:
    - "XL" → Out of stock
    - "Extra Large" → Out of stock (same thing!)
    - "X-Large" → Out of stock (still same thing!)
    
    WHAT HAPPENS:
    - select_variant with any XL-like size: Always fails
    - Agent doesn't realize it's trying the same unavailable size
    
    LOOP TYPES TRIGGERED:
    - Type II (Insanity): Semantic similarity between "XL", "Extra Large", "X-Large"
    - Type III (Phantom): Cart never gets the item
    
    THIS IS "IMAGE PERCEPTION ERROR":
    Agent fails to notice the "Out of Stock" label or grayed-out button.
    It sees the size option exists and assumes it's available.
    
    RESEARCH: This was one of the top failure categories in Amazon's analysis.
    """
    tool = action.tool_name
    
    # These are all semantically the same size
    OOS_SIZES = {"XL", "EXTRA LARGE", "X-LARGE", "EXTRA-LARGE", "XLARGE"}
    
    if tool == "select_variant":
        size = action.tool_args.get("size", "").upper().strip()
        
        if size in OOS_SIZES:
            state.selected_variant = None
            state.last_error = "Size XL is out of stock"
            return Result(
                outcome_type="error",
                message="Size XL is out of stock",
                state_changed=False,
            )
        else:
            # Other sizes work fine
            state.selected_variant = size
            state.last_error = ""
            return Result("success", f"Selected size {size}", True)
    
    if tool == "add_to_cart":
        if not state.selected_variant:
            state.last_error = "Please select a size first"
            return Result("error", state.last_error, False)
        state.cart.append({
            "sku": action.tool_args.get("sku", "SKU123"),
            "size": state.selected_variant,
            "qty": 1,
        })
        return Result("success", "Added to cart", True)
    
    return Result("empty", f"Unknown tool: {tool}", False)


def checkout_sequence_error_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Checkout Sequence Error
    
    REAL-WORLD ANALOGUE (Sensistudio.com case from Amazon research):
    Agent fills out payment details BEFORE clicking "Pay Now".
    Site requires: Click "Pay Now" → Fields appear → Fill fields → Submit
    
    Agent does: Fill fields (fail) → Fill fields (fail) → ...
    
    WHAT HAPPENS:
    - click_pay_now: Fails if shipping/payment not complete
    - Agent keeps clicking Pay Now without completing prerequisites
    
    LOOP TYPES TRIGGERED:
    - Type III (Phantom): Checkout step never advances
    - Type I (Stutter): If agent clicks same button repeatedly
    
    THE FIX (from Amazon research):
    Give agent an "insight": "Wait for payment fields to become active.
    Perhaps you need to click 'Pay Now' first before entering details."
    
    Success rate went from 0% to 100% after adding this insight.
    """
    tool = action.tool_name
    
    if tool == "click_pay_now":
        if state.checkout_step < 2:  # Need shipping (1) and payment (2)
            state.last_error = "Please complete shipping and payment first"
            return Result(
                outcome_type="error",
                message="Please complete shipping and payment first",
                state_changed=False,
            )
        else:
            state.checkout_step = 3
            state.last_error = ""
            return Result("success", "Order placed!", True)
    
    if tool == "fill_shipping":
        state.checkout_step = max(state.checkout_step, 1)
        state.last_error = ""
        return Result("success", "Shipping info saved", True)
    
    if tool == "fill_payment":
        if state.checkout_step < 1:
            state.last_error = "Complete shipping first"
            return Result("error", state.last_error, False)
        state.checkout_step = 2
        state.last_error = ""
        return Result("success", "Payment info saved", True)
    
    return Result("empty", f"Unknown tool: {tool}", False)


def search_synonym_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Search Synonym Loop
    
    REAL-WORLD ANALOGUE:
    Agent searches for "laptop" → 10 results
    Agent searches for "notebook" → Same 10 results
    Agent searches for "portable computer" → Same 10 results
    
    Agent thinks it's exploring different options, but the result set is identical.
    
    WHAT HAPPENS:
    - search: Always returns "10 results" but state_changed=False
    - Different queries, same outcome
    
    LOOP TYPES TRIGGERED:
    - Type II (Insanity): Semantic similarity between search terms
    - Type III (Phantom): State hash unchanged (same results)
    
    WHY AGENTS DO THIS:
    The agent is trying to be thorough, but doesn't track that
    "laptop" and "notebook" return identical results.
    """
    tool = action.tool_name
    
    if tool == "search":
        query = action.tool_args.get("query", "")
        state.current_page = f"search_results:{query}"
        # IMPORTANT: We don't change cart, variant, or checkout_step
        # So state_hash remains the same
        return Result(
            outcome_type="success",
            message="Found 10 results",
            state_changed=False,  # Same results as before!
        )
    
    return Result("empty", f"Unknown tool: {tool}", False)


def add_to_cart_retry_loop_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Add to Cart Retry Loop
    
    REAL-WORLD ANALOGUE:
    Agent clicks "Add to Cart" but no size is selected.
    Site shows error: "Please select a size"
    Agent clicks "Add to Cart" again (same error)
    Agent clicks "Add to Cart" again...
    
    WHAT HAPPENS:
    - add_to_cart: Always fails if no variant selected
    - Agent doesn't read the error message
    
    LOOP TYPES TRIGGERED:
    - Type I (Stutter): Exact same action repeated
    - Type III (Phantom): Cart stays empty
    
    THIS IS "WRONG ACTION INTENT":
    Agent sees the Add to Cart button and assumes clicking it will work.
    It doesn't notice the prerequisite (size selection).
    """
    tool = action.tool_name
    
    if tool == "add_to_cart":
        # Always fail - simulating missing prerequisite
        state.last_error = "Please select a size before adding to cart"
        return Result(
            outcome_type="error",
            message="Please select a size before adding to cart",
            state_changed=False,
        )
    
    if tool == "select_variant":
        state.selected_variant = action.tool_args.get("size", "M")
        state.last_error = ""
        return Result("success", "Size selected", True)
    
    return Result("empty", f"Unknown tool: {tool}", False)


def button_confusion_behavior(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Button Confusion (Visual Semantic Ambiguity)
    
    REAL-WORLD ANALOGUE:
    Page has:
    - Big green button: "CONTINUE TO SAVINGS" (promotional)
    - Small gray link: "Proceed to checkout" (actual checkout)
    
    Agent clicks the big green button, expecting checkout.
    Gets redirected to promotional page instead.
    
    WHAT HAPPENS:
    - click_checkout: If agent clicks wrong button, stays on same page
    - Agent is confused why clicking "Continue" doesn't continue
    
    LOOP TYPES TRIGGERED:
    - Type III (Phantom): Checkout step doesn't advance
    - Type I (Stutter): Agent keeps clicking same wrong button
    
    THIS IS A "DARK PATTERN" TRAP:
    Designers intentionally make the wrong button more prominent.
    """
    tool = action.tool_name
    
    if tool == "click_continue":
        # This is the WRONG button (promotional)
        state.current_page = "promotional_signup"
        state.last_error = ""
        # Page changes but checkout_step doesn't advance
        return Result(
            outcome_type="success",
            message="Showing savings options...",
            state_changed=False,  # No checkout progress!
        )
    
    if tool == "click_checkout":
        # This is the RIGHT button (but agent might not find it)
        if state.cart:
            state.checkout_step = 1
            return Result("success", "Proceeding to checkout", True)
        else:
            state.last_error = "Cart is empty"
            return Result("error", state.last_error, False)
    
    return Result("empty", f"Unknown tool: {tool}", False)


def multi_agent_shopping_pingpong(state: ShoppingState, action: Action) -> Result:
    """
    SCENARIO: Multi-Agent Shopping Ping-Pong
    
    REAL-WORLD ANALOGUE:
    - Search agent finds products
    - Comparison agent should pick one
    - Comparison agent says "need more options" → hands back to Search
    - Search agent finds same products
    - Repeat forever
    
    WHAT HAPPENS:
    - handoff: Always succeeds but cart stays empty
    
    LOOP TYPES TRIGGERED:
    - Type IV (Ping-Pong): A→B→A→B pattern
    - Type III (Phantom): No purchase progress
    """
    tool = action.tool_name
    
    if tool == "handoff":
        target = action.tool_args.get("to", "other_agent")
        return Result(
            outcome_type="success",
            message=f"Handed off to {target}",
            state_changed=False,
        )
    
    if tool == "search":
        return Result("success", "Found 10 products", False)
    
    return Result("empty", f"Unknown tool: {tool}", False)


8. The Step Adapter: Bridging Environments to Detectors
File: nudgeops/testing/step_adapter.py
This is the CRITICAL piece that makes everything work together.
"""
nudgeops/testing/step_adapter.py

Converts (Action, Result, Environment) → StepRecord

This is the bridge between domain-specific mock environments
and domain-agnostic detectors.

Key insight: Detectors only see StepRecords.
They don't know if it came from code or shopping.
This adapter is what makes NudgeOps truly universal.
"""

from __future__ import annotations
import hashlib
from typing import List, Dict

from nudgeops.testing.interfaces import Action, Result, IMockEnvironment
from nudgeops.core.state import StepRecord  # Your existing type


def build_step_record(
    action: Action,
    result: Result,
    env: IMockEnvironment,
    agent_id: str = "test_agent",
    use_real_embeddings: bool = False,
) -> StepRecord:
    """
    Universal adapter: ANY (Action, Result, Env) → StepRecord.
    
    This function is the same for all domains.
    It extracts the information detectors need:
    
    1. tool_name: What tool was used (for basic classification)
    2. tool_args_hash: Hash of args (for Type I stutter detection)
    3. thought_embedding: Vector of thought (for Type II semantic detection)
    4. state_snapshot_hash: Hash of env state (for Type III phantom detection)
    5. agent_id: Which agent (for Type IV ping-pong detection)
    6. outcome_type: success/empty/error (for context)
    
    Args:
        action: The action that was taken
        result: The result from the environment
        env: The environment (to get state hash)
        agent_id: Identifier for multi-agent scenarios
        use_real_embeddings: If True, use actual FastEmbed model.
                            If False, use deterministic fake embeddings (faster).
    
    Returns:
        StepRecord ready for detector consumption
    """
    tool_args_hash = _hash_tool_args(action.tool_args)
    
    if use_real_embeddings:
        # Import your actual embedding service
        from nudgeops.embedding.service import get_embedding_service
        embedder = get_embedding_service()
        thought_embedding = embedder.embed(action.thought_text)
    else:
        # Use fake embeddings for fast, deterministic tests
        thought_embedding = _fake_embed(action.thought_text)
    
    return StepRecord(
        tool_name=action.tool_name,
        tool_args_hash=tool_args_hash,
        thought_embedding=thought_embedding,
        state_snapshot_hash=env.get_state_hash(),
        agent_id=agent_id,
        outcome_type=result.outcome_type,
    )


def _hash_tool_args(args: Dict) -> str:
    """
    Create a deterministic hash of tool arguments.
    
    Used for Type I (Stutter) detection.
    Same tool + same args = same hash = potential stutter.
    """
    # Sort items for deterministic ordering
    items = tuple(sorted(args.items()))
    return hashlib.sha256(repr(items).encode()).hexdigest()[:16]


# Semantic groups for fake embeddings
# Text in the same group → identical embedding → similarity = 1.0
# Text in different groups → different embedding → similarity ≈ 0
SEMANTIC_GROUPS = {
    # Size variations (all mean XL)
    "size_xl": ["xl", "extra large", "x-large", "extra-large", "xlarge"],
    
    # Code modification actions
    "modify_code": ["edit", "fix", "patch", "refactor", "modify", "update", "change"],
    
    # Test/verification actions
    "run_tests": ["run tests", "pytest", "unittest", "test", "verify", "check"],
    
    # Search variations
    "search_laptop": ["laptop", "notebook", "portable computer", "laptops", "notebooks"],
    
    # Submit variations
    "submit_code": ["submit", "commit", "push", "deploy", "publish"],
    
    # Fix bug variations
    "fix_bug": ["fix the bug", "repair the issue", "solve the problem", "debug"],
}


def _fake_embed(text: str, dim: int = 384) -> List[float]:
    """
    Create a fake embedding for testing.
    
    This is NOT a real embedding model. It's designed to:
    1. Be fast (no model loading)
    2. Be deterministic (same text → same vector)
    3. Preserve semantic similarity for testing Type II detection
    
    How it works:
    - Text in the same SEMANTIC_GROUP → identical embedding
    - Text in different groups → different embeddings
    - Unknown text → hash-based embedding
    
    This lets us test that Type II detection works without
    requiring a real embedding model.
    
    Args:
        text: The text to embed
        dim: Embedding dimension (should match your real model, typically 384)
    
    Returns:
        List of floats representing the embedding
    """
    normalized = text.lower().strip()
    
    # Find which semantic group this text belongs to
    matched_group = None
    for group_name, patterns in SEMANTIC_GROUPS.items():
        for pattern in patterns:
            if pattern in normalized:
                matched_group = group_name
                break
        if matched_group:
            break
    
    if matched_group:
        # Same group → same embedding → similarity = 1.0
        h = hashlib.sha256(matched_group.encode()).digest()
    else:
        # Unknown text → hash of the text itself
        h = hashlib.sha256(normalized.encode()).digest()
    
    # Convert hash bytes to floats in [0, 1]
    # Extend to full dimension by cycling through hash
    embedding = []
    for i in range(dim):
        byte_index = i % len(h)
        embedding.append(h[byte_index] / 255.0)
    
    return embedding


def compute_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    This is used by Type II detector to compare thought embeddings.
    
    Returns:
        Float in [-1, 1], where 1 = identical, 0 = orthogonal, -1 = opposite
    """
    if len(vec1) != len(vec2):
        raise ValueError(f"Vector dimension mismatch: {len(vec1)} vs {len(vec2)}")
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


9. Universal Guard: Integration for Any Framework
File: nudgeops/integrations/universal_guard.py
This is what Cursor, LangGraph, AutoGen, CrewAI, etc. would use.
"""
nudgeops/integrations/universal_guard.py

Drop-in guard for ANY agent framework.

Usage is simple:
1. Create a UniversalGuard
2. After each tool execution, call guard.on_step(step_record)
3. Check the returned GuardDecision for OBSERVE/NUDGE/STOP

This works for:
- Cursor IDE
- Claude Code
- LangGraph agents
- AutoGen
- CrewAI
- Any custom framework

The only requirement: You must be able to produce a StepRecord
after each tool execution.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, List, Optional

from nudgeops.core.state import StepRecord
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer


GuardAction = Literal["OBSERVE", "NUDGE", "STOP"]


@dataclass
class GuardDecision:
    """
    The guard's decision after analyzing a step.
    
    Attributes:
        action: What to do (OBSERVE, NUDGE, or STOP)
        score: Current cumulative loop score
        message: If NUDGE/STOP, a message to show/inject
        detections: List of detection types that fired
    """
    action: GuardAction
    score: float
    message: Optional[str] = None
    detections: Optional[List[str]] = None


class UniversalGuard:
    """
    Universal loop detection guard for any agent framework.
    
    Example usage with a generic agent:
    
        guard = UniversalGuard()
        
        for step in agent.run():
            # After each tool execution, check with guard
            step_record = build_step_record(step.action, step.result, env)
            decision = guard.on_step(step_record)
            
            if decision.action == "STOP":
                print(f"Stopping agent: {decision.message}")
                break
            elif decision.action == "NUDGE":
                agent.inject_message(decision.message)
    
    Example usage with LangGraph:
    
        guard = UniversalGuard()
        
        def guard_node(state):
            step_record = extract_step_record(state)
            decision = guard.on_step(step_record)
            
            if decision.action == "STOP":
                return Command(goto=END)
            elif decision.action == "NUDGE":
                state.messages.append(SystemMessage(decision.message))
            
            return state
    """
    
    def __init__(
        self,
        nudge_threshold: float = 2.0,
        stop_threshold: float = 3.0,
    ) -> None:
        """
        Initialize the guard.
        
        Args:
            nudge_threshold: Score at which to nudge (default 2.0)
            stop_threshold: Score at which to stop (default 3.0)
        """
        self._detector = CompositeDetector()
        self._scorer = LoopScorer()
        self._history: List[StepRecord] = []
        self._score: float = 0.0
        self._nudge_threshold = nudge_threshold
        self._stop_threshold = stop_threshold
    
    def on_step(self, step: StepRecord) -> GuardDecision:
        """
        Process a step and return a decision.
        
        This is the main entry point. Call this after EVERY tool execution.
        
        Args:
            step: The StepRecord from the just-completed action
        
        Returns:
            GuardDecision with action (OBSERVE/NUDGE/STOP) and details
        """
        # Run all detectors
        detections = self._detector.detect(step, self._history)
        
        # Update score (includes decay logic)
        self._score = self._scorer.update(self._score, detections)
        
        # Add to history
        self._history.append(step)
        
        # Determine action
        detection_types = [d.type for d in detections] if detections else []
        
        if self._score >= self._stop_threshold:
            return GuardDecision(
                action="STOP",
                score=self._score,
                message=self._build_stop_message(detection_types),
                detections=detection_types,
            )
        
        if self._score >= self._nudge_threshold:
            return GuardDecision(
                action="NUDGE",
                score=self._score,
                message=self._build_nudge_message(detection_types),
                detections=detection_types,
            )
        
        return GuardDecision(
            action="OBSERVE",
            score=self._score,
            detections=detection_types,
        )
    
    def reset(self) -> None:
        """Reset the guard state. Call between agent sessions."""
        self._history = []
        self._score = 0.0
    
    @property
    def score(self) -> float:
        """Current cumulative loop score."""
        return self._score
    
    @property
    def history(self) -> List[StepRecord]:
        """History of all steps seen."""
        return self._history.copy()
    
    def _build_nudge_message(self, detection_types: List[str]) -> str:
        """
        Build a helpful nudge message based on what was detected.
        
        The goal is to help the agent understand WHY it's stuck
        and WHAT to try instead.
        """
        if "TYPE_I_STUTTER" in detection_types:
            return (
                "You've repeated the exact same action multiple times "
                "without making progress. Consider:\n"
                "- Is a prerequisite step missing?\n"
                "- Is the tool reporting success but failing silently?\n"
                "- Try a different approach entirely."
            )
        
        if "TYPE_II_INSANITY" in detection_types:
            return (
                "You've attempted several semantically similar actions without success. "
                "The current approach doesn't seem to be working. Consider:\n"
                "- Is the goal actually achievable?\n"
                "- Is there a fundamentally different strategy?\n"
                "- Should you ask for clarification or report failure?"
            )
        
        if "TYPE_III_PHANTOM" in detection_types:
            return (
                "Your actions are not changing the underlying state. "
                "You may be experiencing 'phantom progress'. Consider:\n"
                "- Verify that your actions are actually taking effect.\n"
                "- Check for silent failures or permission issues.\n"
                "- The environment may not be responding as expected."
            )
        
        if "TYPE_IV_PINGPONG" in detection_types:
            return (
                "There appears to be a handoff loop between agents. "
                "Tasks are being passed back and forth without progress. Consider:\n"
                "- Clarify responsibilities between agents.\n"
                "- Have one agent take ownership of the task.\n"
                "- Check if the task is actually completable."
            )
        
        return (
            "NudgeOps detected potential looping behavior. "
            "Please review your recent actions and consider a different approach."
        )
    
    def _build_stop_message(self, detection_types: List[str]) -> str:
        """Build a stop message explaining why the agent was halted."""
        types_str = ", ".join(detection_types) if detection_types else "unknown"
        return (
            f"TrajectoryGuard has stopped the agent due to detected loop patterns: {types_str}. "
            f"Final score: {self._score:.2f}. "
            "The agent appeared to be stuck and was consuming resources without progress."
        )


10. Complete Test Suite
File: tests/test_code_loops.py
"""
tests/test_code_loops.py

Test suite for code agent loop detection.

These tests verify that:
1. Code agent loops ARE detected (true positives)
2. Legitimate code patterns are NOT detected (false positives)
3. Detection happens at the right threshold
"""

import pytest
from nudgeops.testing.environments.code_env import MockCodeEnvironment
from nudgeops.testing.scenarios.code_scenarios import (
    infinite_edit_loop_behavior,
    compile_retry_loop_behavior,
    submit_spam_loop_behavior,
    phantom_edit_behavior,
    hallucinated_library_behavior,
    hallucination_spiral_behavior,
    daemon_linter_behavior,
    ping_pong_handoff_behavior,
)
from nudgeops.testing.step_adapter import build_step_record
from nudgeops.testing.interfaces import Action
from nudgeops.core.detectors import CompositeDetector
from nudgeops.core.scorer import LoopScorer


class TestCodeLoopDetection:
    """Tests for detecting code agent loops."""
    
    @pytest.fixture
    def detector(self):
        return CompositeDetector()
    
    @pytest.fixture
    def scorer(self):
        return LoopScorer()
    
    # =====================================================================
    # TRUE POSITIVE TESTS: Loops that SHOULD be detected
    # =====================================================================
    
    def test_infinite_edit_loop_triggers_nudge(self, detector, scorer):
        """
        SCENARIO: Agent edits file → tests fail → repeat 5 times
        
        Expected: Score >= 2.0 (NUDGE threshold)
        Triggered types: I (stutter), II (semantic), III (phantom)
        """
        env = MockCodeEnvironment(infinite_edit_loop_behavior)
        history = []
        score = 0.0
        
        for i in range(5):
            # Agent edits file
            edit_action = Action(
                tool_name="edit_file",
                tool_args={"file": "foo.py", "line": 42},
                thought_text=f"Try fixing the bug in foo.py attempt {i}",
            )
            edit_result = env.execute_action(edit_action)
            step = build_step_record(edit_action, edit_result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
            
            # Agent runs tests
            test_action = Action(
                tool_name="run_tests",
                tool_args={},
                thought_text="Run tests to verify the fix",
            )
            test_result = env.execute_action(test_action)
            step = build_step_record(test_action, test_result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected NUDGE threshold (>=2.0), got {score:.2f}"
        print(f"✓ Infinite edit loop detected at score {score:.2f}")
    
    def test_submit_spam_triggers_stop(self, detector, scorer):
        """
        SCENARIO: Agent calls submit_patch 10 times with no effect
        
        Expected: Score >= 3.0 (STOP threshold)
        Triggered types: I (stutter), III (phantom)
        """
        env = MockCodeEnvironment(submit_spam_loop_behavior)
        history = []
        score = 0.0
        
        for i in range(10):
            action = Action(
                tool_name="submit_patch",
                tool_args={"branch": "main"},
                thought_text="Submit my changes",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 3.0, f"Expected STOP threshold (>=3.0), got {score:.2f}"
        print(f"✓ Submit spam detected at score {score:.2f}")
    
    def test_phantom_edit_detected(self, detector, scorer):
        """
        SCENARIO: Agent edits file but file doesn't change (silent failure)
        
        Expected: Type III (phantom progress) detection
        """
        env = MockCodeEnvironment(phantom_edit_behavior)
        history = []
        score = 0.0
        
        for i in range(4):
            action = Action(
                tool_name="edit_file",
                tool_args={"file": "main.py"},
                thought_text="Add the missing variable",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected phantom edit detection, got {score:.2f}"
        print(f"✓ Phantom edit detected at score {score:.2f}")
    
    def test_hallucinated_library_loop(self, detector, scorer):
        """
        SCENARIO: Agent tries to install non-existent package repeatedly
        
        Expected: Type I + Type II detection
        """
        env = MockCodeEnvironment(hallucinated_library_behavior)
        history = []
        score = 0.0
        
        packages = [
            "binary_converter_pro",
            "binary-converter-pro",
            "binary_converter",
            "binaryconverter",
        ]
        
        for pkg in packages:
            action = Action(
                tool_name="pip_install",
                tool_args={"package": pkg},
                thought_text=f"Install {pkg} to handle the conversion",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        # Might not hit threshold due to different args, but should show progression
        print(f"✓ Hallucinated library pattern, score: {score:.2f}")
    
    def test_daemon_linter_measures_ttgu(self, detector, scorer):
        """
        SCENARIO: Linter ALWAYS fails (impossible task)
        METRIC: Time To Give Up (TTGU) - how many steps until STOP?
        
        Good agent: Stops in 5-7 steps
        Bad agent: Never stops
        """
        env = MockCodeEnvironment(daemon_linter_behavior)
        history = []
        score = 0.0
        steps_to_stop = 0
        
        for i in range(20):  # Max iterations
            action = Action(
                tool_name="run_linter",
                tool_args={},
                thought_text=f"Run linter to check syntax attempt {i}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
            steps_to_stop += 1
            
            if score >= 3.0:
                break
        
        assert steps_to_stop <= 10, f"TTGU too high: {steps_to_stop} steps"
        assert score >= 3.0, "Should have reached STOP threshold"
        print(f"✓ Daemon linter: TTGU = {steps_to_stop} steps, score = {score:.2f}")
    
    def test_ping_pong_multi_agent_detected(self, detector, scorer):
        """
        SCENARIO: Two agents hand task back and forth
        
        Expected: Type IV (ping-pong) detection
        """
        env = MockCodeEnvironment(ping_pong_handoff_behavior)
        history = []
        score = 0.0
        agents = ["planner", "coder"]
        
        for i in range(6):
            current_agent = agents[i % 2]
            next_agent = agents[(i + 1) % 2]
            
            action = Action(
                tool_name="handoff",
                tool_args={"to": next_agent},
                thought_text=f"Let {next_agent} handle this",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env, agent_id=current_agent)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected ping-pong detection, got {score:.2f}"
        print(f"✓ Ping-pong handoff detected at score {score:.2f}")
    
    # =====================================================================
    # FALSE POSITIVE TESTS: Legitimate patterns that should NOT trigger
    # =====================================================================
    
    def test_legitimate_edit_test_cycle_not_flagged(self, detector, scorer):
        """
        SCENARIO: Agent edits → tests fail → edits DIFFERENT thing → tests pass
        
        Expected: Score < 2.0 (no intervention)
        """
        env = MockCodeEnvironment()  # Default happy-path behavior
        history = []
        score = 0.0
        
        # Edit file A
        action1 = Action("edit_file", {"file": "foo.py"}, "Fix foo")
        result1 = env.execute_action(action1)
        step1 = build_step_record(action1, result1, env)
        detections = detector.detect(step1, history)
        score = scorer.update(score, detections)
        history.append(step1)
        
        # Tests fail (expected on first try)
        action2 = Action("run_tests", {}, "Run tests")
        result2 = env.execute_action(action2)
        step2 = build_step_record(action2, result2, env)
        detections = detector.detect(step2, history)
        score = scorer.update(score, detections)
        history.append(step2)
        
        # Edit DIFFERENT file
        action3 = Action("edit_file", {"file": "bar.py"}, "Actually fix bar")
        result3 = env.execute_action(action3)
        step3 = build_step_record(action3, result3, env)
        detections = detector.detect(step3, history)
        score = scorer.update(score, detections)
        history.append(step3)
        
        # Tests pass
        action4 = Action("run_tests", {}, "Verify fix")
        result4 = env.execute_action(action4)
        step4 = build_step_record(action4, result4, env)
        detections = detector.detect(step4, history)
        score = scorer.update(score, detections)
        history.append(step4)
        
        assert score < 2.0, f"False positive! Score {score:.2f} on legitimate pattern"
        print(f"✓ Legitimate edit cycle correctly allowed, score {score:.2f}")
    
    def test_two_test_runs_not_flagged(self, detector, scorer):
        """
        SCENARIO: Agent runs tests twice (common pattern)
        
        Expected: Score < 2.0 (small penalty, not intervention)
        """
        env = MockCodeEnvironment()
        history = []
        score = 0.0
        
        for i in range(2):
            action = Action("run_tests", {}, f"Run tests attempt {i}")
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score < 2.0, f"False positive on 2 test runs: {score:.2f}"
        print(f"✓ Two test runs allowed, score {score:.2f}")


class TestShoppingLoopDetection:
    """Tests for detecting shopping agent loops."""
    
    @pytest.fixture
    def detector(self):
        return CompositeDetector()
    
    @pytest.fixture
    def scorer(self):
        return LoopScorer()
    
    def test_variant_oos_semantic_loop(self, detector, scorer):
        """
        SCENARIO: Agent tries XL, Extra Large, X-Large (all OOS)
        
        Expected: Type II semantic loop detection
        """
        from nudgeops.testing.environments.shopping_env import MockShoppingEnvironment
        from nudgeops.testing.scenarios.shopping_scenarios import variant_oos_loop_behavior
        
        env = MockShoppingEnvironment(variant_oos_loop_behavior)
        history = []
        score = 0.0
        
        size_attempts = ["XL", "Extra Large", "X-Large", "EXTRA-LARGE"]
        
        for size in size_attempts:
            action = Action(
                tool_name="select_variant",
                tool_args={"size": size},
                thought_text=f"Select size {size}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected semantic loop detection, got {score:.2f}"
        print(f"✓ Variant OOS semantic loop detected at score {score:.2f}")
    
    def test_search_synonym_loop(self, detector, scorer):
        """
        SCENARIO: Agent searches laptop, notebook, portable computer
        
        Expected: Type II semantic loop + Type III phantom progress
        """
        from nudgeops.testing.environments.shopping_env import MockShoppingEnvironment
        from nudgeops.testing.scenarios.shopping_scenarios import search_synonym_loop_behavior
        
        env = MockShoppingEnvironment(search_synonym_loop_behavior)
        history = []
        score = 0.0
        
        queries = ["laptop", "notebook", "portable computer", "laptops"]
        
        for query in queries:
            action = Action(
                tool_name="search",
                tool_args={"query": query},
                thought_text=f"Search for {query}",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected search synonym loop detection, got {score:.2f}"
        print(f"✓ Search synonym loop detected at score {score:.2f}")
    
    def test_add_to_cart_retry_loop(self, detector, scorer):
        """
        SCENARIO: Agent clicks Add to Cart 5 times without selecting size
        
        Expected: Type I stutter detection
        """
        from nudgeops.testing.environments.shopping_env import MockShoppingEnvironment
        from nudgeops.testing.scenarios.shopping_scenarios import add_to_cart_retry_loop_behavior
        
        env = MockShoppingEnvironment(add_to_cart_retry_loop_behavior)
        history = []
        score = 0.0
        
        for i in range(5):
            action = Action(
                tool_name="add_to_cart",
                tool_args={"sku": "ABC123"},
                thought_text="Add item to cart",
            )
            result = env.execute_action(action)
            step = build_step_record(action, result, env)
            detections = detector.detect(step, history)
            score = scorer.update(score, detections)
            history.append(step)
        
        assert score >= 2.0, f"Expected add to cart retry detection, got {score:.2f}"
        print(f"✓ Add to cart retry loop detected at score {score:.2f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


11. File Structure Summary
nudgeops/
├── core/                          # EXISTING - Your detectors/scorer
│   ├── state.py                   # StepRecord, AgentState, etc.
│   ├── detectors.py               # Stutter, Insanity, Phantom, PingPong
│   ├── scorer.py                  # LoopScorer with decay
│   └── interventions.py           # Nudge templates
│
├── testing/                       # NEW - Mock testing framework
│   ├── __init__.py
│   ├── interfaces.py              # Action, Result, IMockEnvironment
│   ├── step_adapter.py            # build_step_record(), fake embeddings
│   │
│   ├── environments/              # Domain-specific mock environments
│   │   ├── __init__.py
│   │   ├── code_env.py            # MockCodeEnvironment, CodeState
│   │   └── shopping_env.py        # MockShoppingEnvironment, ShoppingState
│   │
│   └── scenarios/                 # Failure pattern behaviors
│       ├── __init__.py
│       ├── code_scenarios.py      # infinite_edit, submit_spam, etc.
│       └── shopping_scenarios.py  # variant_oos, search_synonym, etc.
│
├── integrations/                  # EXISTING + NEW
│   ├── langgraph_node.py          # TrajectoryGuardNode
│   ├── apply_guard.py             # One-line integration
│   └── universal_guard.py         # NEW - UniversalGuard for any framework
│
└── tests/
    ├── test_code_loops.py         # NEW - Code agent loop tests
    └── test_shopping_loops.py     # NEW - Shopping agent loop tests


12. Integration Examples
Cursor IDE Integration
# cursor_nudgeops_integration.py

from nudgeops.integrations.universal_guard import UniversalGuard
from nudgeops.testing.step_adapter import build_step_record
from nudgeops.testing.interfaces import Action

guard = UniversalGuard()

def on_cursor_tool_execution(tool_name, tool_args, thought, result, workspace_state):
    """
    Called by Cursor after each tool execution.
    
    Args:
        tool_name: "edit_file", "run_terminal", etc.
        tool_args: Arguments passed to tool
        thought: Model's reasoning before the action
        result: Tool execution result
        workspace_state: Current state of the workspace
    """
    action = Action(tool_name, tool_args, thought)
    
    # Create a simple environment wrapper
    class CursorEnvWrapper:
        def get_state_hash(self):
            # Hash relevant workspace state
            import hashlib
            return hashlib.sha256(repr(workspace_state).encode()).hexdigest()
    
    step = build_step_record(action, result, CursorEnvWrapper())
    decision = guard.on_step(step)
    
    if decision.action == "STOP":
        cursor.abort_agent(decision.message)
    elif decision.action == "NUDGE":
        cursor.inject_system_message(decision.message)

LangGraph Integration
# langgraph_nudgeops_integration.py

from langgraph.graph import StateGraph
from nudgeops.integrations.universal_guard import UniversalGuard

guard = UniversalGuard()

def trajectory_guard_node(state):
    """
    LangGraph node that checks for loops after each agent action.
    """
    # Extract the last step from state
    if not state.get("last_action"):
        return state
    
    step = extract_step_record_from_state(state)
    decision = guard.on_step(step)
    
    if decision.action == "STOP":
        state["should_stop"] = True
        state["stop_reason"] = decision.message
    elif decision.action == "NUDGE":
        # Inject nudge as system message
        state["messages"].append({
            "role": "system",
            "content": decision.message
        })
    
    state["loop_score"] = decision.score
    return state

# Add to graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)
builder.add_node("guard", trajectory_guard_node)  # Add guard
builder.add_edge("tools", "guard")                # Check after tools
builder.add_edge("guard", "agent")                # Continue to agent

AutoGen Integration
# autogen_nudgeops_integration.py

from autogen import AssistantAgent
from nudgeops.integrations.universal_guard import UniversalGuard

guard = UniversalGuard()

class GuardedAssistant(AssistantAgent):
    """AutoGen assistant with NudgeOps loop detection."""
    
    def execute_function(self, function_call):
        # Execute the function normally
        result = super().execute_function(function_call)
        
        # Check with guard
        step = build_step_record_from_function_call(function_call, result)
        decision = guard.on_step(step)
        
        if decision.action == "STOP":
            raise LoopDetectedError(decision.message)
        elif decision.action == "NUDGE":
            # Prepend nudge to next message
            self._nudge_message = decision.message
        
        return result


Summary
This testing framework provides:
Domain-agnostic detection: Same detectors work for code AND shopping agents
Fast iteration: Mock environments run in milliseconds
Deterministic failures: Exact same loop pattern every test run
Comprehensive coverage: All 4 loop types, both domains
Easy integration: UniversalGuard works with any framework
The key insight: Your detectors don't need to know about code vs shopping. They only see StepRecords. All domain knowledge lives in the mock environments.

Running Tests
# Run all loop detection tests
pytest tests/test_code_loops.py tests/test_shopping_loops.py -v

# Run only code agent tests
pytest tests/test_code_loops.py -v

# Run only shopping agent tests  
pytest tests/test_shopping_loops.py -v

# Run with coverage
pytest --cov=nudgeops tests/ -v

Next Steps
Copy the code sections into the appropriate files
Run pytest to verify everything works
Tune thresholds based on test results
Add more scenarios as you discover new failure patterns


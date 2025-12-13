"""
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

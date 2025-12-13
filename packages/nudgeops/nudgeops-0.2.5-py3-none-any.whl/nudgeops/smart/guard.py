"""
Smart Guard - Main decision engine for NudgeOps.

Combines thought normalization, state/action hashing, and failure memory
to decide whether to allow, block, or warn about actions.

Two-level checking:
1. Exact action repeat in same state → BLOCK
2. Same intent repeated N times → BLOCK (strategy exhausted)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from enum import Enum
from datetime import datetime

from .thought_normalizer import ThoughtNormalizer, LLMClient, MockLLMClient
from .hashers import StateHasher, ActionHasher
from .failure_memory import FailureMemory, ActionFailure, IntentCluster


class Decision(Enum):
    """Guard decision types."""
    ALLOW = "allow"
    BLOCK = "block"
    WARN = "warn"


@dataclass
class GuardResult:
    """Result of a guard check."""
    
    decision: Decision
    reason: Optional[str] = None
    nudge_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # For observability
    state_hash: Optional[str] = None
    action_hash: Optional[str] = None
    intent: Optional[str] = None
    
    @property
    def blocked(self) -> bool:
        return self.decision == Decision.BLOCK
    
    @property
    def allowed(self) -> bool:
        return self.decision == Decision.ALLOW
    
    @property
    def warned(self) -> bool:
        return self.decision == Decision.WARN
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "nudge_message": self.nudge_message,
            "metadata": self.metadata,
            "state_hash": self.state_hash,
            "action_hash": self.action_hash,
            "intent": self.intent
        }


class SmartGuard:
    """
    Main guard that decides whether to allow/block actions.
    
    Two-level checking:
    1. Exact action repeat in same state → BLOCK
    2. Same intent repeated N times with different actions → BLOCK
    
    Usage:
        guard = SmartGuard(llm_client)
        
        # Check before executing action
        result = guard.check(
            state=current_state,
            thought="Let me search for XYZ",
            tool_name="search",
            args={"query": "XYZ"}
        )
        
        if result.blocked:
            # Inject nudge message instead
            inject_message(result.nudge_message)
        else:
            # Execute the action
            try:
                output = execute_tool(tool_name, args)
            except Exception as e:
                # Record the failure
                guard.record_failure(state, thought, tool_name, args, str(e))
    """
    
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        action_repeat_threshold: int = 2,
        intent_repeat_threshold: int = 3,
        warn_threshold: int = 2,
        cache_size: int = 1000
    ):
        """
        Initialize the smart guard.
        
        Args:
            llm_client: LLM client for thought normalization (optional, uses mock if None)
            action_repeat_threshold: Block after this many exact action repeats
            intent_repeat_threshold: Block after this many intent repeats
            warn_threshold: Warn after this many attempts (before blocking)
            cache_size: Size of thought normalization cache
        """
        # Use mock client if none provided (for testing)
        self.llm_client = llm_client or MockLLMClient()
        
        # Components
        self.normalizer = ThoughtNormalizer(self.llm_client, cache_size)
        self.state_hasher = StateHasher()
        self.action_hasher = ActionHasher()
        self.memory = FailureMemory()
        
        # Thresholds
        self.action_repeat_threshold = action_repeat_threshold
        self.intent_repeat_threshold = intent_repeat_threshold
        self.warn_threshold = warn_threshold
        
        # State tracking
        self._last_state_hash: Optional[str] = None
        
        # Statistics
        self.stats = {
            "checks": 0,
            "blocks": 0,
            "warns": 0,
            "allows": 0,
            "failures_recorded": 0
        }
    
    def check(
        self,
        state: Dict[str, Any],
        thought: str,
        tool_name: str,
        args: Dict[str, Any]
    ) -> GuardResult:
        """
        Check if action should be allowed.
        
        Args:
            state: Current agent state
            thought: Agent's reasoning/thought for this action
            tool_name: Name of tool to call
            args: Arguments for tool
            
        Returns:
            GuardResult with decision and optional nudge message
        """
        self.stats["checks"] += 1
        
        # Hash state and action
        state_hash = self.state_hasher.hash(state)
        action_hash = self.action_hasher.hash_exact(tool_name, args)
        
        # Track state changes
        state_changed = (
            self._last_state_hash is not None and 
            state_hash != self._last_state_hash
        )
        self._last_state_hash = state_hash
        
        # Normalize thought to intent
        intent = self.normalizer.normalize(thought) if thought else "unknown"
        
        # Level 1: Check exact action repeat
        action_failure = self.memory.check_action(state_hash, action_hash)
        if action_failure:
            if action_failure.count >= self.action_repeat_threshold:
                self.stats["blocks"] += 1
                return GuardResult(
                    decision=Decision.BLOCK,
                    reason="exact_action_repeat",
                    nudge_message=self._format_action_nudge(action_failure, state_changed),
                    state_hash=state_hash,
                    action_hash=action_hash,
                    intent=intent,
                    metadata={
                        "repeat_count": action_failure.count,
                        "last_error": action_failure.error,
                        "state_changed": state_changed
                    }
                )
            elif action_failure.count >= self.warn_threshold:
                self.stats["warns"] += 1
                return GuardResult(
                    decision=Decision.WARN,
                    reason="action_repeat_warning",
                    nudge_message=self._format_action_warning(action_failure),
                    state_hash=state_hash,
                    action_hash=action_hash,
                    intent=intent,
                    metadata={
                        "repeat_count": action_failure.count,
                        "last_error": action_failure.error
                    }
                )
        
        # Level 2: Check intent repeat
        intent_cluster = self.memory.check_intent(state_hash, intent)
        if intent_cluster:
            if intent_cluster.total_attempts >= self.intent_repeat_threshold:
                self.stats["blocks"] += 1
                return GuardResult(
                    decision=Decision.BLOCK,
                    reason="intent_exhausted",
                    nudge_message=self._format_intent_nudge(intent_cluster),
                    state_hash=state_hash,
                    action_hash=action_hash,
                    intent=intent,
                    metadata={
                        "total_attempts": intent_cluster.total_attempts,
                        "unique_actions": intent_cluster.get_unique_actions(),
                        "state_changed": state_changed
                    }
                )
            elif intent_cluster.total_attempts >= self.warn_threshold:
                self.stats["warns"] += 1
                return GuardResult(
                    decision=Decision.WARN,
                    reason="intent_repeat_warning",
                    nudge_message=self._format_intent_warning(intent_cluster),
                    state_hash=state_hash,
                    action_hash=action_hash,
                    intent=intent,
                    metadata={
                        "total_attempts": intent_cluster.total_attempts
                    }
                )
        
        # Allow the action
        self.stats["allows"] += 1
        return GuardResult(
            decision=Decision.ALLOW,
            state_hash=state_hash,
            action_hash=action_hash,
            intent=intent,
            metadata={"state_changed": state_changed}
        )
    
    def record_failure(
        self,
        state: Dict[str, Any],
        thought: str,
        tool_name: str,
        args: Dict[str, Any],
        error: str,
        error_code: Optional[str] = None
    ):
        """
        Record a failed action for future blocking.
        
        Call this after an action fails.
        """
        self.stats["failures_recorded"] += 1
        
        state_hash = self.state_hasher.hash(state)
        action_hash = self.action_hasher.hash_exact(tool_name, args)
        intent = self.normalizer.normalize(thought) if thought else None
        
        self.memory.record_failure(
            state_hash=state_hash,
            action_hash=action_hash,
            tool_name=tool_name,
            args=args,
            error=error,
            error_code=error_code,
            intent=intent
        )
    
    def get_failure_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get failure summary for injection into agent state.
        
        Use this to pass failure context to downstream agents.
        """
        state_hash = self.state_hasher.hash(state)
        return self.memory.get_failure_summary(state_hash)
    
    def get_dead_intents(self, state: Dict[str, Any]) -> List[str]:
        """Get list of exhausted intents for current state."""
        state_hash = self.state_hasher.hash(state)
        return self.memory.get_dead_intents(state_hash, self.intent_repeat_threshold)
    
    def clear_state(self, state: Dict[str, Any]):
        """Clear failure memory for a state."""
        state_hash = self.state_hasher.hash(state)
        self.memory.clear_state(state_hash)
    
    def reset(self):
        """Reset all memory and stats."""
        self.memory.clear_all()
        self._last_state_hash = None
        self.stats = {k: 0 for k in self.stats}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get guard statistics."""
        return {
            **self.stats,
            "memory": self.memory.get_stats(),
            "normalizer": self.normalizer.get_stats()
        }
    
    # --- Nudge Message Formatting ---
    
    def _format_action_nudge(self, failure: ActionFailure, state_changed: bool) -> str:
        """Format nudge message for blocked action repeat."""
        state_note = ""
        if not state_changed:
            state_note = "\n\nState has NOT changed. This action will fail again."
        
        return f"""[NudgeOps: Action Blocked]

You already tried: {failure.tool_name}({self._format_args(failure.args)})
Times attempted: {failure.count}
Result each time: {failure.error}
{state_note}
DO NOT repeat this exact action.
Choose a DIFFERENT approach."""

    def _format_action_warning(self, failure: ActionFailure) -> str:
        """Format warning message for action approaching threshold."""
        return f"""[NudgeOps: Warning]

You've tried {failure.tool_name}({self._format_args(failure.args)}) {failure.count} time(s).
Last result: {failure.error}

Consider trying a different approach before this action is blocked."""

    def _format_intent_nudge(self, cluster: IntentCluster) -> str:
        """Format nudge message for exhausted intent."""
        action_list = cluster.format_for_nudge(max_actions=5)
        
        return f"""[NudgeOps: Strategy Blocked]

You are stuck on: "{cluster.intent}"
Total attempts: {cluster.total_attempts}
Variations tried:
{action_list}

All variations of this approach have failed.
You MUST try a COMPLETELY DIFFERENT strategy.
Do NOT continue with "{cluster.intent}"."""

    def _format_intent_warning(self, cluster: IntentCluster) -> str:
        """Format warning for intent approaching threshold."""
        return f"""[NudgeOps: Warning]

You've been trying "{cluster.intent}" for {cluster.total_attempts} attempt(s).
Multiple variations have failed.

Consider switching to a different strategy."""

    def _format_args(self, args: Dict[str, Any]) -> str:
        """Format args dict for display."""
        if not args:
            return ""
        return ", ".join(f"{k}={repr(v)}" for k, v in args.items())


class SmartGuardBuilder:
    """Builder for SmartGuard with fluent API."""
    
    def __init__(self):
        self._llm_client = None
        self._action_threshold = 2
        self._intent_threshold = 3
        self._warn_threshold = 2
        self._cache_size = 1000
    
    def with_llm(self, client: LLMClient) -> "SmartGuardBuilder":
        self._llm_client = client
        return self
    
    def with_action_threshold(self, threshold: int) -> "SmartGuardBuilder":
        self._action_threshold = threshold
        return self
    
    def with_intent_threshold(self, threshold: int) -> "SmartGuardBuilder":
        self._intent_threshold = threshold
        return self
    
    def with_warn_threshold(self, threshold: int) -> "SmartGuardBuilder":
        self._warn_threshold = threshold
        return self
    
    def with_cache_size(self, size: int) -> "SmartGuardBuilder":
        self._cache_size = size
        return self
    
    def build(self) -> SmartGuard:
        return SmartGuard(
            llm_client=self._llm_client,
            action_repeat_threshold=self._action_threshold,
            intent_repeat_threshold=self._intent_threshold,
            warn_threshold=self._warn_threshold,
            cache_size=self._cache_size
        )

"""
Failure Memory - Tracks failed actions and intents per state.

Two-level tracking:
1. Action level: (state_hash, action_hash) → ActionFailure
2. Intent level: (state_hash, intent) → IntentCluster

This enables both:
- Blocking exact repeats (action level)
- Blocking exhausted strategies (intent level)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import threading
import json


@dataclass
class ActionFailure:
    """Record of a single failed action."""
    
    action_hash: str
    tool_name: str
    args: Dict[str, Any]
    error: str
    error_code: Optional[str] = None
    count: int = 1
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    
    def increment(self):
        """Increment failure count."""
        self.count += 1
        self.last_seen = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action_hash": self.action_hash,
            "tool_name": self.tool_name,
            "args": self.args,
            "error": self.error,
            "error_code": self.error_code,
            "count": self.count,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat()
        }
    
    def __str__(self) -> str:
        args_str = ", ".join(f"{k}={v}" for k, v in self.args.items())
        return f"{self.tool_name}({args_str}) → {self.error}"


@dataclass
class IntentCluster:
    """
    Cluster of failed actions with the same intent.
    
    Multiple different actions can all be trying to achieve the same intent.
    When all variations fail, the intent is considered "exhausted".
    """
    
    intent: str
    actions: List[ActionFailure] = field(default_factory=list)
    total_attempts: int = 0
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    
    def add_failure(self, failure: ActionFailure):
        """Add a failed action to this intent cluster."""
        # Check if we already have this action
        for existing in self.actions:
            if existing.action_hash == failure.action_hash:
                # Action already tracked - just update total_attempts
                # Note: Don't call increment() here since it's already incremented 
                # in FailureMemory.record_failure
                self.total_attempts += 1
                self.last_seen = datetime.now()
                return
        
        # New action variation - add to list
        self.actions.append(failure)
        self.total_attempts += failure.count
        self.last_seen = datetime.now()
    
    def get_unique_actions(self) -> int:
        """Number of unique action variations tried."""
        return len(self.actions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "intent": self.intent,
            "total_attempts": self.total_attempts,
            "unique_actions": self.get_unique_actions(),
            "actions": [a.to_dict() for a in self.actions],
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat()
        }
    
    def format_for_nudge(self, max_actions: int = 5) -> str:
        """Format for inclusion in nudge message."""
        lines = []
        for action in self.actions[-max_actions:]:
            lines.append(f"  - {action}")
        return "\n".join(lines)


class FailureMemory:
    """
    Tracks failed actions and intents per state.
    
    Thread-safe storage for failure information.
    
    Usage:
        memory = FailureMemory()
        
        # Record a failure
        memory.record_failure(
            state_hash="abc123",
            action_hash="def456", 
            tool_name="search",
            args={"query": "XYZ"},
            error="Not found",
            intent="find product by ID"
        )
        
        # Check if action is known to fail
        failure = memory.check_action("abc123", "def456")
        if failure and failure.count >= 2:
            print("This action has failed multiple times!")
        
        # Check if intent is exhausted
        cluster = memory.check_intent("abc123", "find product by ID")
        if cluster and cluster.total_attempts >= 3:
            print("This strategy is exhausted!")
    """
    
    def __init__(
        self,
        max_states: int = 1000,
        max_actions_per_state: int = 100
    ):
        """
        Initialize failure memory.
        
        Args:
            max_states: Maximum number of unique states to track
            max_actions_per_state: Maximum failed actions per state
        """
        self.max_states = max_states
        self.max_actions_per_state = max_actions_per_state
        
        # (state_hash, action_hash) → ActionFailure
        self._action_cache: Dict[Tuple[str, str], ActionFailure] = {}
        
        # (state_hash, intent) → IntentCluster
        self._intent_cache: Dict[Tuple[str, str], IntentCluster] = {}
        
        # Track states for LRU eviction
        self._state_access_order: List[str] = []
        
        self._lock = threading.RLock()
    
    def record_failure(
        self,
        state_hash: str,
        action_hash: str,
        tool_name: str,
        args: Dict[str, Any],
        error: str,
        error_code: Optional[str] = None,
        intent: Optional[str] = None
    ) -> Tuple[ActionFailure, Optional[IntentCluster]]:
        """
        Record a failed action.
        
        Args:
            state_hash: Hash of current state
            action_hash: Hash of the failed action
            tool_name: Name of the tool that failed
            args: Arguments that were passed
            error: Error message
            error_code: Optional error code
            intent: Optional normalized intent string
            
        Returns:
            Tuple of (ActionFailure, IntentCluster or None)
        """
        with self._lock:
            # Update state access order
            self._touch_state(state_hash)
            
            # Update or create action failure
            action_key = (state_hash, action_hash)
            
            if action_key in self._action_cache:
                failure = self._action_cache[action_key]
                failure.increment()
            else:
                failure = ActionFailure(
                    action_hash=action_hash,
                    tool_name=tool_name,
                    args=args,
                    error=error,
                    error_code=error_code
                )
                self._action_cache[action_key] = failure
            
            # Update intent cluster if intent provided
            cluster = None
            if intent:
                intent_key = (state_hash, intent)
                
                if intent_key not in self._intent_cache:
                    self._intent_cache[intent_key] = IntentCluster(intent=intent)
                
                cluster = self._intent_cache[intent_key]
                cluster.add_failure(failure)
            
            return failure, cluster
    
    def check_action(
        self,
        state_hash: str,
        action_hash: str
    ) -> Optional[ActionFailure]:
        """
        Check if action is known to fail in this state.
        
        Returns:
            ActionFailure if found, None otherwise
        """
        with self._lock:
            return self._action_cache.get((state_hash, action_hash))
    
    def check_intent(
        self,
        state_hash: str,
        intent: str
    ) -> Optional[IntentCluster]:
        """
        Check if intent has been tried in this state.
        
        Returns:
            IntentCluster if found, None otherwise
        """
        with self._lock:
            return self._intent_cache.get((state_hash, intent))
    
    def get_failures_for_state(self, state_hash: str) -> List[ActionFailure]:
        """Get all failed actions for a state."""
        with self._lock:
            return [
                failure for (s, _), failure in self._action_cache.items()
                if s == state_hash
            ]
    
    def get_intents_for_state(self, state_hash: str) -> List[IntentCluster]:
        """Get all intent clusters for a state."""
        with self._lock:
            return [
                cluster for (s, _), cluster in self._intent_cache.items()
                if s == state_hash
            ]
    
    def get_dead_intents(self, state_hash: str, threshold: int = 3) -> List[str]:
        """
        Get list of intents that have been exhausted (failed >= threshold times).
        """
        with self._lock:
            dead = []
            for (s, intent), cluster in self._intent_cache.items():
                if s == state_hash and cluster.total_attempts >= threshold:
                    dead.append(intent)
            return dead
    
    def clear_state(self, state_hash: str):
        """Clear all failures for a state."""
        with self._lock:
            self._action_cache = {
                k: v for k, v in self._action_cache.items()
                if k[0] != state_hash
            }
            self._intent_cache = {
                k: v for k, v in self._intent_cache.items()
                if k[0] != state_hash
            }
            if state_hash in self._state_access_order:
                self._state_access_order.remove(state_hash)
    
    def clear_all(self):
        """Clear all failure memory."""
        with self._lock:
            self._action_cache.clear()
            self._intent_cache.clear()
            self._state_access_order.clear()
    
    def _touch_state(self, state_hash: str):
        """Update state access order for LRU tracking."""
        if state_hash in self._state_access_order:
            self._state_access_order.remove(state_hash)
        self._state_access_order.append(state_hash)
        
        # Evict oldest states if over limit
        while len(self._state_access_order) > self.max_states:
            oldest = self._state_access_order.pop(0)
            self.clear_state(oldest)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        with self._lock:
            return {
                "unique_states": len(self._state_access_order),
                "total_action_failures": len(self._action_cache),
                "total_intent_clusters": len(self._intent_cache),
                "max_states": self.max_states
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export all memory as dictionary."""
        with self._lock:
            return {
                "action_cache": {
                    f"{s}:{a}": f.to_dict() 
                    for (s, a), f in self._action_cache.items()
                },
                "intent_cache": {
                    f"{s}:{i}": c.to_dict()
                    for (s, i), c in self._intent_cache.items()
                },
                "stats": self.get_stats()
            }
    
    def get_failure_summary(self, state_hash: str) -> Dict[str, Any]:
        """
        Get failure summary for injection into agent state.
        
        This is what gets passed to downstream agents.
        """
        with self._lock:
            dead_intents = []
            for (s, intent), cluster in self._intent_cache.items():
                if s == state_hash and cluster.total_attempts >= 3:
                    dead_intents.append({
                        "intent": cluster.intent,
                        "attempts": cluster.total_attempts,
                        "actions": [str(a) for a in cluster.actions[-3:]],
                        "last_error": cluster.actions[-1].error if cluster.actions else None
                    })
            
            return {
                "dead_intents": dead_intents,
                "total_failures": sum(
                    f.count for (s, _), f in self._action_cache.items()
                    if s == state_hash
                )
            }

"""
State and Action Hashers - Create deterministic hashes for comparison.

StateHasher: Hash environment state to detect if it changed
ActionHasher: Hash tool calls to detect exact repeats
"""

import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple


class StateHasher:
    """
    Creates deterministic hashes of agent state.
    
    Used to detect if state has changed between actions.
    If state hasn't changed and same action failed before, it will fail again.
    
    Usage:
        hasher = StateHasher()
        hash1 = hasher.hash(state)
        # ... agent does something ...
        hash2 = hasher.hash(new_state)
        if hash1 == hash2:
            print("State unchanged")
    """
    
    # Keys to ignore when hashing (volatile, non-deterministic)
    DEFAULT_IGNORE_KEYS = [
        "timestamp",
        "request_id",
        "trace_id",
        "session_id",
        "uuid",
        "created_at",
        "updated_at",
        "random",
        "nonce",
    ]
    
    def __init__(
        self,
        ignore_keys: List[str] = None,
        include_only: List[str] = None,
        hash_length: int = 16
    ):
        """
        Initialize state hasher.
        
        Args:
            ignore_keys: Keys to ignore when hashing
            include_only: If set, only hash these keys
            hash_length: Length of returned hash string
        """
        self.ignore_keys = set(ignore_keys or self.DEFAULT_IGNORE_KEYS)
        self.include_only = set(include_only) if include_only else None
        self.hash_length = hash_length
    
    def hash(self, state: Dict[str, Any]) -> str:
        """
        Create deterministic hash of state.
        
        Args:
            state: Agent state dictionary
            
        Returns:
            Hash string
        """
        if not state:
            return "empty_state"
        
        # Filter state
        filtered = self._filter_state(state)
        
        # Create canonical JSON string
        canonical = self._to_canonical_json(filtered)
        
        # Hash it
        return hashlib.sha256(canonical.encode()).hexdigest()[:self.hash_length]
    
    def has_changed(self, old_hash: str, new_state: Dict[str, Any]) -> bool:
        """Check if state has changed from a previous hash."""
        return old_hash != self.hash(new_state)
    
    def diff(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the difference between two states.
        
        Returns:
            Dict with 'added', 'removed', 'changed' keys
        """
        old_filtered = self._filter_state(old_state)
        new_filtered = self._filter_state(new_state)
        
        old_keys = set(old_filtered.keys())
        new_keys = set(new_filtered.keys())
        
        added = {k: new_filtered[k] for k in new_keys - old_keys}
        removed = {k: old_filtered[k] for k in old_keys - new_keys}
        changed = {
            k: {"old": old_filtered[k], "new": new_filtered[k]}
            for k in old_keys & new_keys
            if old_filtered[k] != new_filtered[k]
        }
        
        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "has_changes": bool(added or removed or changed)
        }
    
    def _filter_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Filter state based on ignore/include rules."""
        if self.include_only:
            return {k: v for k, v in state.items() if k in self.include_only}
        return {k: v for k, v in state.items() if k not in self.ignore_keys}
    
    def _to_canonical_json(self, obj: Any) -> str:
        """Convert object to canonical JSON string."""
        return json.dumps(obj, sort_keys=True, default=str, separators=(',', ':'))


class ActionHasher:
    """
    Creates hashes of tool/action calls.
    
    Two modes:
    1. Exact hash: Catches exact same call (same tool, same args)
    2. Normalized hash: Catches similar calls (normalizes IDs, numbers, etc.)
    
    Usage:
        hasher = ActionHasher()
        
        # Exact matching
        hash1 = hasher.hash_exact("search", {"query": "XYZ-9999"})
        hash2 = hasher.hash_exact("search", {"query": "XYZ-9999"})
        assert hash1 == hash2  # Same call
        
        # Normalized matching
        hash3 = hasher.hash_normalized("search", {"query": "XYZ-9999"})
        hash4 = hasher.hash_normalized("search", {"query": "ABC-1234"})
        assert hash3 == hash4  # Same pattern (ID search)
    """
    
    # Patterns to normalize (pattern, replacement)
    DEFAULT_NORMALIZATION_PATTERNS = [
        # Product/Order IDs: XYZ-9999, ABC123, etc.
        (r'\b[A-Z]{2,}-\d+\b', '<ID>'),
        (r'\b[A-Z]+\d+\b', '<ID>'),
        
        # UUIDs
        (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '<UUID>'),
        
        # Hex hashes
        (r'\b[a-f0-9]{32,}\b', '<HASH>'),
        
        # Long numbers (likely IDs)
        (r'\b\d{6,}\b', '<NUM>'),
        
        # Email addresses
        (r'\b[\w.-]+@[\w.-]+\.\w+\b', '<EMAIL>'),
        
        # URLs
        (r'https?://\S+', '<URL>'),
        
        # File paths
        (r'/[\w/.-]+\.\w+', '<PATH>'),
    ]
    
    def __init__(
        self,
        normalization_patterns: List[Tuple[str, str]] = None,
        hash_length: int = 16
    ):
        """
        Initialize action hasher.
        
        Args:
            normalization_patterns: List of (pattern, replacement) tuples
            hash_length: Length of returned hash string
        """
        self.patterns = normalization_patterns or self.DEFAULT_NORMALIZATION_PATTERNS
        self.compiled_patterns = [(re.compile(p), r) for p, r in self.patterns]
        self.hash_length = hash_length
    
    def hash_exact(self, tool_name: str, args: Dict[str, Any]) -> str:
        """
        Create exact hash of action (no normalization).
        
        Use for detecting exact same call repeated.
        """
        canonical = self._to_canonical({
            "tool": tool_name,
            "args": args
        })
        return hashlib.sha256(canonical.encode()).hexdigest()[:self.hash_length]
    
    def hash_normalized(self, tool_name: str, args: Dict[str, Any]) -> str:
        """
        Create normalized hash of action.
        
        Use for detecting similar calls (same pattern, different values).
        """
        normalized_args = self._normalize_args(args)
        canonical = self._to_canonical({
            "tool": tool_name,
            "args": normalized_args
        })
        return hashlib.sha256(canonical.encode()).hexdigest()[:self.hash_length]
    
    def hash(self, tool_name: str, args: Dict[str, Any], normalize: bool = False) -> str:
        """
        Create hash of action.
        
        Args:
            tool_name: Name of the tool
            args: Tool arguments
            normalize: Whether to normalize args
            
        Returns:
            Hash string
        """
        if normalize:
            return self.hash_normalized(tool_name, args)
        return self.hash_exact(tool_name, args)
    
    def _normalize_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize argument values using patterns."""
        normalized = {}
        for key, value in args.items():
            normalized[key] = self._normalize_value(value)
        return normalized
    
    def _normalize_value(self, value: Any) -> Any:
        """Normalize a single value."""
        if isinstance(value, str):
            result = value
            for pattern, replacement in self.compiled_patterns:
                result = pattern.sub(replacement, result)
            return result
        elif isinstance(value, dict):
            return self._normalize_args(value)
        elif isinstance(value, list):
            return [self._normalize_value(v) for v in value]
        return value
    
    def _to_canonical(self, obj: Any) -> str:
        """Convert to canonical JSON string."""
        return json.dumps(obj, sort_keys=True, default=str, separators=(',', ':'))
    
    def get_signature(self, tool_name: str, args: Dict[str, Any]) -> str:
        """
        Get human-readable signature of action.
        
        Example: "search(query=<ID>)"
        """
        normalized_args = self._normalize_args(args)
        args_str = ", ".join(f"{k}={v}" for k, v in sorted(normalized_args.items()))
        return f"{tool_name}({args_str})"


class CombinedHasher:
    """
    Combines state and action hashing for (state, action) pair tracking.
    """
    
    def __init__(self):
        self.state_hasher = StateHasher()
        self.action_hasher = ActionHasher()
    
    def hash_state_action(
        self,
        state: Dict[str, Any],
        tool_name: str,
        args: Dict[str, Any],
        normalize_action: bool = False
    ) -> Tuple[str, str]:
        """
        Hash both state and action.
        
        Returns:
            Tuple of (state_hash, action_hash)
        """
        state_hash = self.state_hasher.hash(state)
        action_hash = self.action_hasher.hash(tool_name, args, normalize=normalize_action)
        return state_hash, action_hash
    
    def combined_key(
        self,
        state: Dict[str, Any],
        tool_name: str,
        args: Dict[str, Any]
    ) -> str:
        """Get combined key for (state, action) pair."""
        state_hash, action_hash = self.hash_state_action(state, tool_name, args)
        return f"{state_hash}:{action_hash}"

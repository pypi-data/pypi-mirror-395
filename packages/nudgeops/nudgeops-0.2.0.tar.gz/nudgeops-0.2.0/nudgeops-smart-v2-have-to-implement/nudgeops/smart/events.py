"""
Failure Events - Structured failure records for cross-customer learning.

Events are designed to be:
1. Anonymized - No customer-specific data
2. Normalized - Canonical error signatures
3. Pattern-extractable - Can be clustered and learned from
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import json
import re


class FailureType(Enum):
    """Type of failure."""
    HARD = "hard"           # Permanent failure (404, not found)
    TRANSIENT = "transient"  # Might work later (rate limit, timeout)
    UNKNOWN = "unknown"


class RecoveryStatus(Enum):
    """Whether the agent recovered from the failure."""
    PENDING = "pending"     # Not yet determined
    RECOVERED = "recovered"  # Agent found alternative
    FAILED = "failed"       # Agent gave up
    BLOCKED = "blocked"     # NudgeOps blocked further attempts


@dataclass
class FailureEvent:
    """
    Anonymized failure event for cross-customer learning.
    
    Key design principle: No customer-specific data.
    Only patterns that can generalize across customers.
    """
    
    # === Identifiers (internal use, not for pattern learning) ===
    event_id: str = ""
    tenant_id: str = ""
    agent_id: str = ""
    session_id: str = ""
    
    # === Pattern-relevant fields (anonymized) ===
    state_sig: str = ""          # "ecommerce_checkout", "code_edit"
    action_sig: str = ""         # "search_product(id=*)", normalized
    intent_sig: str = ""         # "find product by ID"
    error_sig: str = ""          # "PRODUCT_NOT_FOUND", canonical
    
    # === Context ===
    failure_type: FailureType = FailureType.UNKNOWN
    repeat_count: int = 1
    
    # === Recovery tracking ===
    recovery_status: RecoveryStatus = RecoveryStatus.PENDING
    recovery_action: Optional[str] = None  # What worked, if anything
    recovery_intent: Optional[str] = None  # Intent that worked
    
    # === Metadata ===
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for storage."""
        d = asdict(self)
        d["failure_type"] = self.failure_type.value
        d["recovery_status"] = self.recovery_status.value
        d["timestamp"] = self.timestamp.isoformat()
        return d
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FailureEvent":
        """Create from dict."""
        d = d.copy()
        d["failure_type"] = FailureType(d.get("failure_type", "unknown"))
        d["recovery_status"] = RecoveryStatus(d.get("recovery_status", "pending"))
        if isinstance(d.get("timestamp"), str):
            d["timestamp"] = datetime.fromisoformat(d["timestamp"])
        return cls(**d)
    
    def anonymized(self) -> Dict[str, Any]:
        """Return only pattern-relevant fields (no tenant data)."""
        return {
            "state_sig": self.state_sig,
            "action_sig": self.action_sig,
            "intent_sig": self.intent_sig,
            "error_sig": self.error_sig,
            "failure_type": self.failure_type.value,
            "repeat_count": self.repeat_count,
            "recovery_status": self.recovery_status.value,
            "recovery_action": self.recovery_action,
            "recovery_intent": self.recovery_intent
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "FailureEvent":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))


# === Error Signature Canonicalization ===

# Mapping of error patterns to canonical signatures
ERROR_PATTERNS = {
    # HTTP errors
    r"404": "NOT_FOUND",
    r"401": "UNAUTHORIZED",
    r"403": "FORBIDDEN",
    r"429": "RATE_LIMITED",
    r"rate.?limit": "RATE_LIMITED",
    r"500": "SERVER_ERROR",
    r"502|503|504": "SERVICE_UNAVAILABLE",
    r"timeout": "TIMEOUT",
    
    # E-commerce
    r"product.*(not|no).*(found|exist)": "PRODUCT_NOT_FOUND",
    r"out.?of.?stock": "OUT_OF_STOCK",
    r"(invalid|wrong).*(size|variant|color)": "INVALID_VARIANT",
    r"(item|product).*(unavailable|discontinued)": "ITEM_UNAVAILABLE",
    r"cart.*(empty|no items)": "EMPTY_CART",
    r"payment.*(failed|declined|error)": "PAYMENT_FAILED",
    
    # File operations
    r"file.*(not|no).*(found|exist)": "FILE_NOT_FOUND",
    r"permission.*(denied|error)": "PERMISSION_DENIED",
    r"(directory|folder).*(not|no).*(found|exist)": "DIR_NOT_FOUND",
    
    # Code/Syntax
    r"syntax.?error": "SYNTAX_ERROR",
    r"import.?error": "IMPORT_ERROR",
    r"(name|type|attribute).?error": "RUNTIME_ERROR",
    r"(module|package).*(not|no).*(found|installed)": "MODULE_NOT_FOUND",
    
    # API
    r"api.*(error|failed)": "API_ERROR",
    r"(invalid|bad).*(request|input|param)": "INVALID_REQUEST",
    r"(auth|authentication).*(failed|error)": "AUTH_FAILED",
    
    # Network
    r"connection.*(refused|failed|error)": "CONNECTION_ERROR",
    r"dns.*(error|failed)": "DNS_ERROR",
    r"ssl.*(error|failed)": "SSL_ERROR",
    
    # General
    r"not.?found": "NOT_FOUND",
    r"(failed|failure)": "GENERAL_FAILURE",
    r"(error|exception)": "GENERAL_ERROR",
}

# Compiled patterns for efficiency
COMPILED_ERROR_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), sig)
    for pattern, sig in ERROR_PATTERNS.items()
]


def canonicalize_error(error_message: str) -> str:
    """
    Convert raw error message to canonical signature.
    
    Example:
        "Product XYZ-9999 was not found in our system"
        → "PRODUCT_NOT_FOUND"
    """
    if not error_message:
        return "UNKNOWN_ERROR"
    
    error_lower = error_message.lower()
    
    for pattern, signature in COMPILED_ERROR_PATTERNS:
        if pattern.search(error_lower):
            return signature
    
    return "UNKNOWN_ERROR"


def get_failure_type(error_sig: str) -> FailureType:
    """
    Determine if a failure is hard (permanent) or transient.
    """
    TRANSIENT_ERRORS = {
        "RATE_LIMITED",
        "TIMEOUT",
        "SERVICE_UNAVAILABLE",
        "CONNECTION_ERROR",
        "DNS_ERROR",
    }
    
    HARD_ERRORS = {
        "NOT_FOUND",
        "PRODUCT_NOT_FOUND",
        "FILE_NOT_FOUND",
        "UNAUTHORIZED",
        "FORBIDDEN",
        "INVALID_REQUEST",
        "SYNTAX_ERROR",
    }
    
    if error_sig in TRANSIENT_ERRORS:
        return FailureType.TRANSIENT
    if error_sig in HARD_ERRORS:
        return FailureType.HARD
    return FailureType.UNKNOWN


# === State Signature Canonicalization ===

# Mapping of state patterns to canonical signatures
STATE_PATTERNS = {
    r"search|browse|catalog|listing": "search_page",
    r"product|item|detail": "product_page",
    r"cart|basket": "cart_page",
    r"checkout|payment": "checkout_page",
    r"login|signin|auth": "auth_page",
    r"edit|write|modify": "edit_mode",
    r"read|view|display": "view_mode",
    r"file|document": "file_context",
    r"code|script|program": "code_context",
    r"api|endpoint|request": "api_context",
}

COMPILED_STATE_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), sig)
    for pattern, sig in STATE_PATTERNS.items()
]


def canonicalize_state(state: Dict[str, Any]) -> str:
    """
    Convert state dict to canonical signature.
    
    Looks for clues in state keys/values to determine context type.
    """
    state_str = json.dumps(state).lower()
    
    for pattern, signature in COMPILED_STATE_PATTERNS:
        if pattern.search(state_str):
            return signature
    
    return "unknown_context"


# === Action Signature Canonicalization ===

def canonicalize_action(tool_name: str, args: Dict[str, Any]) -> str:
    """
    Convert tool call to canonical action signature.
    
    Normalizes argument values to wildcards.
    
    Example:
        tool_name="search", args={"query": "XYZ-9999"}
        → "search(query=*)"
    """
    # Normalize args (replace specific values with wildcards)
    normalized_args = []
    for key in sorted(args.keys()):
        normalized_args.append(f"{key}=*")
    
    args_str = ", ".join(normalized_args)
    return f"{tool_name}({args_str})"


# === Event Builder ===

class FailureEventBuilder:
    """Builder for creating FailureEvent from raw data."""
    
    def __init__(self):
        self._event = FailureEvent()
    
    def with_identifiers(
        self,
        tenant_id: str,
        agent_id: str,
        session_id: str
    ) -> "FailureEventBuilder":
        self._event.tenant_id = tenant_id
        self._event.agent_id = agent_id
        self._event.session_id = session_id
        return self
    
    def with_state(self, state: Dict[str, Any]) -> "FailureEventBuilder":
        self._event.state_sig = canonicalize_state(state)
        return self
    
    def with_action(self, tool_name: str, args: Dict[str, Any]) -> "FailureEventBuilder":
        self._event.action_sig = canonicalize_action(tool_name, args)
        return self
    
    def with_intent(self, intent: str) -> "FailureEventBuilder":
        self._event.intent_sig = intent
        return self
    
    def with_error(self, error_message: str) -> "FailureEventBuilder":
        self._event.error_sig = canonicalize_error(error_message)
        self._event.failure_type = get_failure_type(self._event.error_sig)
        return self
    
    def with_repeat_count(self, count: int) -> "FailureEventBuilder":
        self._event.repeat_count = count
        return self
    
    def with_recovery(
        self,
        status: RecoveryStatus,
        action: Optional[str] = None,
        intent: Optional[str] = None
    ) -> "FailureEventBuilder":
        self._event.recovery_status = status
        self._event.recovery_action = action
        self._event.recovery_intent = intent
        return self
    
    def build(self) -> FailureEvent:
        return self._event


# === Event Storage Interface ===

class EventStore:
    """Interface for storing and retrieving failure events."""
    
    def save(self, event: FailureEvent):
        """Save a failure event."""
        raise NotImplementedError
    
    def get_by_pattern(
        self,
        intent_sig: Optional[str] = None,
        error_sig: Optional[str] = None,
        action_sig: Optional[str] = None,
        limit: int = 100
    ) -> List[FailureEvent]:
        """Get events matching pattern."""
        raise NotImplementedError
    
    def get_recoveries(
        self,
        intent_sig: str,
        error_sig: Optional[str] = None,
        limit: int = 100
    ) -> List[FailureEvent]:
        """Get events where recovery was successful."""
        raise NotImplementedError


class InMemoryEventStore(EventStore):
    """Simple in-memory event store for testing/MVP."""
    
    def __init__(self, max_events: int = 10000):
        self.events: List[FailureEvent] = []
        self.max_events = max_events
    
    def save(self, event: FailureEvent):
        self.events.append(event)
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
    
    def get_by_pattern(
        self,
        intent_sig: Optional[str] = None,
        error_sig: Optional[str] = None,
        action_sig: Optional[str] = None,
        limit: int = 100
    ) -> List[FailureEvent]:
        results = []
        for event in reversed(self.events):
            if intent_sig and event.intent_sig != intent_sig:
                continue
            if error_sig and event.error_sig != error_sig:
                continue
            if action_sig and event.action_sig != action_sig:
                continue
            results.append(event)
            if len(results) >= limit:
                break
        return results
    
    def get_recoveries(
        self,
        intent_sig: str,
        error_sig: Optional[str] = None,
        limit: int = 100
    ) -> List[FailureEvent]:
        results = []
        for event in reversed(self.events):
            if event.intent_sig != intent_sig:
                continue
            if event.recovery_status != RecoveryStatus.RECOVERED:
                continue
            if error_sig and event.error_sig != error_sig:
                continue
            results.append(event)
            if len(results) >= limit:
                break
        return results
    
    def count(self) -> int:
        return len(self.events)
    
    def clear(self):
        self.events.clear()

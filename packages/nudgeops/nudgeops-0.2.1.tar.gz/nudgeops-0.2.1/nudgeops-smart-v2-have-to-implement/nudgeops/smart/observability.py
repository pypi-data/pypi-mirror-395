"""
Observability Layer - Tracking and metrics for NudgeOps.

Tracks:
- Guard decisions (block/allow/warn)
- Failures recorded
- Tokens saved estimates
- Top failure patterns
- ROI metrics
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import json


@dataclass
class ObservabilityEvent:
    """Single observable event."""
    
    event_type: str  # "block", "allow", "warn", "failure", "recovery"
    timestamp: datetime
    tenant_id: str
    agent_id: str
    
    # Event details
    intent: Optional[str] = None
    action_sig: Optional[str] = None
    error_sig: Optional[str] = None
    reason: Optional[str] = None
    
    # Estimates
    tokens_saved_estimate: int = 0
    time_saved_ms_estimate: int = 0
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "tenant_id": self.tenant_id,
            "agent_id": self.agent_id,
            "intent": self.intent,
            "action_sig": self.action_sig,
            "error_sig": self.error_sig,
            "reason": self.reason,
            "tokens_saved_estimate": self.tokens_saved_estimate,
            "time_saved_ms_estimate": self.time_saved_ms_estimate,
            "metadata": self.metadata
        }


@dataclass
class AgentStats:
    """Statistics for a single agent."""
    
    total_checks: int = 0
    blocks: int = 0
    warns: int = 0
    allows: int = 0
    failures_recorded: int = 0
    recoveries: int = 0
    
    tokens_saved: int = 0
    time_saved_ms: int = 0
    
    # Breakdown by type
    blocks_by_reason: Dict[str, int] = field(default_factory=dict)
    failures_by_error: Dict[str, int] = field(default_factory=dict)
    failures_by_intent: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_checks": self.total_checks,
            "blocks": self.blocks,
            "warns": self.warns,
            "allows": self.allows,
            "failures_recorded": self.failures_recorded,
            "recoveries": self.recoveries,
            "tokens_saved": self.tokens_saved,
            "time_saved_ms": self.time_saved_ms,
            "blocks_by_reason": dict(self.blocks_by_reason),
            "top_failure_errors": dict(sorted(
                self.failures_by_error.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]),
            "top_failure_intents": dict(sorted(
                self.failures_by_intent.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10])
        }


@dataclass
class TenantStats:
    """Aggregated statistics for a tenant."""
    
    agents: Dict[str, AgentStats] = field(default_factory=dict)
    
    @property
    def total_checks(self) -> int:
        return sum(a.total_checks for a in self.agents.values())
    
    @property
    def total_blocks(self) -> int:
        return sum(a.blocks for a in self.agents.values())
    
    @property
    def total_tokens_saved(self) -> int:
        return sum(a.tokens_saved for a in self.agents.values())
    
    @property
    def total_failures(self) -> int:
        return sum(a.failures_recorded for a in self.agents.values())
    
    def get_agent(self, agent_id: str) -> AgentStats:
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentStats()
        return self.agents[agent_id]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agents_count": len(self.agents),
            "total_checks": self.total_checks,
            "total_blocks": self.total_blocks,
            "total_tokens_saved": self.total_tokens_saved,
            "total_failures": self.total_failures,
            "agents": {k: v.to_dict() for k, v in self.agents.items()}
        }


class ObservabilityLayer:
    """
    Tracks all guard decisions and provides analytics.
    
    Usage:
        obs = ObservabilityLayer()
        
        # Record events
        obs.record_block(tenant_id, agent_id, reason, intent, repeat_count)
        obs.record_failure(tenant_id, agent_id, error_sig, intent)
        
        # Get stats
        summary = obs.get_tenant_summary(tenant_id)
        print(f"Tokens saved: {summary['tokens_saved']}")
    """
    
    # Estimates for token/time savings
    TOKENS_PER_STEP = 150  # Average tokens per agent step
    MS_PER_STEP = 2000     # Average time per step (2 seconds)
    
    # Cost estimates (GPT-4o-mini pricing)
    COST_PER_1M_INPUT = 0.15
    COST_PER_1M_OUTPUT = 0.60
    
    def __init__(
        self,
        max_events: int = 100000,
        event_callback: Optional[Callable[[ObservabilityEvent], None]] = None
    ):
        """
        Initialize observability layer.
        
        Args:
            max_events: Maximum events to keep in memory
            event_callback: Optional callback for each event (for streaming)
        """
        self.max_events = max_events
        self.event_callback = event_callback
        
        self._events: List[ObservabilityEvent] = []
        self._stats: Dict[str, TenantStats] = defaultdict(TenantStats)
        self._lock = threading.RLock()
    
    def record_check(
        self,
        tenant_id: str,
        agent_id: str
    ):
        """Record a guard check."""
        with self._lock:
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.total_checks += 1
    
    def record_block(
        self,
        tenant_id: str,
        agent_id: str,
        reason: str,
        intent: Optional[str] = None,
        repeat_count: int = 1
    ):
        """Record a blocked action."""
        # Estimate tokens saved (prevent N more repeats)
        estimated_steps_saved = max(1, repeat_count)
        tokens_saved = self.TOKENS_PER_STEP * estimated_steps_saved
        time_saved = self.MS_PER_STEP * estimated_steps_saved
        
        event = ObservabilityEvent(
            event_type="block",
            timestamp=datetime.now(),
            tenant_id=tenant_id,
            agent_id=agent_id,
            intent=intent,
            reason=reason,
            tokens_saved_estimate=tokens_saved,
            time_saved_ms_estimate=time_saved
        )
        
        with self._lock:
            self._add_event(event)
            
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.blocks += 1
            stats.tokens_saved += tokens_saved
            stats.time_saved_ms += time_saved
            stats.blocks_by_reason[reason] = stats.blocks_by_reason.get(reason, 0) + 1
    
    def record_warn(
        self,
        tenant_id: str,
        agent_id: str,
        reason: str,
        intent: Optional[str] = None
    ):
        """Record a warning."""
        event = ObservabilityEvent(
            event_type="warn",
            timestamp=datetime.now(),
            tenant_id=tenant_id,
            agent_id=agent_id,
            intent=intent,
            reason=reason
        )
        
        with self._lock:
            self._add_event(event)
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.warns += 1
    
    def record_allow(
        self,
        tenant_id: str,
        agent_id: str
    ):
        """Record an allowed action."""
        with self._lock:
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.allows += 1
    
    def record_failure(
        self,
        tenant_id: str,
        agent_id: str,
        error_sig: str,
        intent: Optional[str] = None,
        action_sig: Optional[str] = None
    ):
        """Record a failure."""
        event = ObservabilityEvent(
            event_type="failure",
            timestamp=datetime.now(),
            tenant_id=tenant_id,
            agent_id=agent_id,
            intent=intent,
            error_sig=error_sig,
            action_sig=action_sig
        )
        
        with self._lock:
            self._add_event(event)
            
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.failures_recorded += 1
            stats.failures_by_error[error_sig] = stats.failures_by_error.get(error_sig, 0) + 1
            if intent:
                stats.failures_by_intent[intent] = stats.failures_by_intent.get(intent, 0) + 1
    
    def record_recovery(
        self,
        tenant_id: str,
        agent_id: str,
        recovery_intent: Optional[str] = None
    ):
        """Record a successful recovery."""
        event = ObservabilityEvent(
            event_type="recovery",
            timestamp=datetime.now(),
            tenant_id=tenant_id,
            agent_id=agent_id,
            intent=recovery_intent
        )
        
        with self._lock:
            self._add_event(event)
            stats = self._stats[tenant_id].get_agent(agent_id)
            stats.recoveries += 1
    
    def _add_event(self, event: ObservabilityEvent):
        """Add event to buffer."""
        self._events.append(event)
        
        # Trim if over limit
        if len(self._events) > self.max_events:
            self._events = self._events[-self.max_events:]
        
        # Callback if configured
        if self.event_callback:
            try:
                self.event_callback(event)
            except Exception:
                pass  # Don't let callback errors break observability
    
    def get_tenant_summary(
        self,
        tenant_id: str,
        since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get summary stats for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            since: Only count events since this time (default: last 30 days)
            
        Returns:
            Summary dict with stats and ROI
        """
        if since is None:
            since = datetime.now() - timedelta(days=30)
        
        with self._lock:
            tenant_stats = self._stats.get(tenant_id)
            if not tenant_stats:
                return self._empty_summary(since)
            
            total_tokens = tenant_stats.total_tokens_saved
            cost_saved = self._estimate_cost(total_tokens)
            
            return {
                "period_start": since.isoformat(),
                "period_end": datetime.now().isoformat(),
                "agents_monitored": len(tenant_stats.agents),
                
                # Activity metrics
                "total_checks": tenant_stats.total_checks,
                "blocks": tenant_stats.total_blocks,
                "failures_recorded": tenant_stats.total_failures,
                
                # Savings estimates
                "tokens_saved": total_tokens,
                "cost_saved_usd": cost_saved,
                "time_saved_seconds": sum(
                    a.time_saved_ms for a in tenant_stats.agents.values()
                ) / 1000,
                
                # Detailed breakdown
                "details": tenant_stats.to_dict()
            }
    
    def get_agent_summary(
        self,
        tenant_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """Get summary for a specific agent."""
        with self._lock:
            tenant_stats = self._stats.get(tenant_id)
            if not tenant_stats or agent_id not in tenant_stats.agents:
                return {"error": "Agent not found"}
            
            return tenant_stats.agents[agent_id].to_dict()
    
    def get_recent_events(
        self,
        tenant_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent events with optional filtering."""
        with self._lock:
            results = []
            for event in reversed(self._events):
                if tenant_id and event.tenant_id != tenant_id:
                    continue
                if event_type and event.event_type != event_type:
                    continue
                results.append(event.to_dict())
                if len(results) >= limit:
                    break
            return results
    
    def get_top_failure_patterns(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get most common failure patterns."""
        with self._lock:
            # Aggregate by (intent, error) pair
            patterns: Dict[tuple, int] = defaultdict(int)
            
            for event in self._events:
                if event.event_type != "failure":
                    continue
                if tenant_id and event.tenant_id != tenant_id:
                    continue
                
                key = (event.intent or "unknown", event.error_sig or "unknown")
                patterns[key] += 1
            
            # Sort and return top
            sorted_patterns = sorted(
                patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            return [
                {"intent": k[0], "error": k[1], "count": v}
                for k, v in sorted_patterns
            ]
    
    def get_roi_dashboard(
        self,
        tenant_id: str,
        subscription_cost: float = 99.0
    ) -> Dict[str, Any]:
        """
        Get ROI dashboard data.
        
        Args:
            tenant_id: Tenant identifier
            subscription_cost: Monthly subscription cost
            
        Returns:
            Dashboard data with ROI calculations
        """
        summary = self.get_tenant_summary(tenant_id)
        
        cost_saved = summary.get("cost_saved_usd", 0)
        roi = cost_saved / subscription_cost if subscription_cost > 0 else 0
        
        return {
            **summary,
            "subscription_cost_usd": subscription_cost,
            "roi_ratio": round(roi, 2),
            "roi_percentage": round(roi * 100, 1),
            "net_savings_usd": round(cost_saved - subscription_cost, 2)
        }
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost in USD for tokens."""
        # Assume 50/50 input/output split
        avg_price_per_1m = (self.COST_PER_1M_INPUT + self.COST_PER_1M_OUTPUT) / 2
        return round(tokens * avg_price_per_1m / 1_000_000, 2)
    
    def _empty_summary(self, since: datetime) -> Dict[str, Any]:
        """Return empty summary for tenant with no data."""
        return {
            "period_start": since.isoformat(),
            "period_end": datetime.now().isoformat(),
            "agents_monitored": 0,
            "total_checks": 0,
            "blocks": 0,
            "failures_recorded": 0,
            "tokens_saved": 0,
            "cost_saved_usd": 0,
            "time_saved_seconds": 0,
            "details": {}
        }
    
    def clear(self):
        """Clear all data."""
        with self._lock:
            self._events.clear()
            self._stats.clear()
    
    def export_events(self, tenant_id: Optional[str] = None) -> str:
        """Export events as JSON."""
        events = self.get_recent_events(tenant_id, limit=self.max_events)
        return json.dumps(events, indent=2)


# Global observability instance (optional singleton pattern)
_global_observability: Optional[ObservabilityLayer] = None


def get_observability() -> ObservabilityLayer:
    """Get global observability instance."""
    global _global_observability
    if _global_observability is None:
        _global_observability = ObservabilityLayer()
    return _global_observability


def set_observability(obs: ObservabilityLayer):
    """Set global observability instance."""
    global _global_observability
    _global_observability = obs

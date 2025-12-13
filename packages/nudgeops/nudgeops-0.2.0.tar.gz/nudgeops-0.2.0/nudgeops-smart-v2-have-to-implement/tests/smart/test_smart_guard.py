"""
Tests for Smart NudgeOps module.

Tests cover:
- Thought normalization
- State and action hashing
- Failure memory
- Smart guard decisions
- Observability
"""

import pytest
from datetime import datetime

# Import all components
from nudgeops.smart import (
    # Thought normalization
    ThoughtNormalizer,
    MockLLMClient,
    RuleBasedNormalizer,
    
    # Hashers
    StateHasher,
    ActionHasher,
    
    # Failure memory
    FailureMemory,
    ActionFailure,
    IntentCluster,
    
    # Guard
    SmartGuard,
    GuardResult,
    Decision,
    
    # Events
    FailureEvent,
    FailureType,
    RecoveryStatus,
    canonicalize_error,
    canonicalize_action,
    
    # Observability
    ObservabilityLayer,
)


# ============================================
# Thought Normalizer Tests
# ============================================

class TestThoughtNormalizer:
    """Tests for thought normalization."""
    
    def test_basic_normalization(self):
        """Test basic thought to intent conversion."""
        mock_llm = MockLLMClient({
            "search for product": "find product by ID"
        })
        normalizer = ThoughtNormalizer(mock_llm)
        
        intent = normalizer.normalize("I should search for the product XYZ-9999")
        assert intent == "find product by id"  # MockLLMClient returns this
    
    def test_caching(self):
        """Test that results are cached."""
        mock_llm = MockLLMClient()
        normalizer = ThoughtNormalizer(mock_llm)
        
        # First call
        intent1 = normalizer.normalize("search for product")
        
        # Second call with same input
        intent2 = normalizer.normalize("search for product")
        
        # Should be same result
        assert intent1 == intent2
        
        # LLM should only be called once
        assert len(mock_llm.calls) == 1
    
    def test_empty_thought(self):
        """Test handling of empty thought."""
        normalizer = ThoughtNormalizer(MockLLMClient())
        
        assert normalizer.normalize("") == "no intent"
        assert normalizer.normalize("   ") == "no intent"
    
    def test_stats(self):
        """Test statistics tracking."""
        normalizer = ThoughtNormalizer(MockLLMClient())
        
        normalizer.normalize("thought 1")
        normalizer.normalize("thought 2")
        normalizer.normalize("thought 1")  # Cache hit
        
        stats = normalizer.get_stats()
        assert stats["total_calls"] == 3
        assert stats["cache_hits"] == 1
        assert stats["cache_misses"] == 2


class TestRuleBasedNormalizer:
    """Tests for rule-based normalization."""
    
    def test_common_patterns(self):
        """Test matching common patterns."""
        normalizer = RuleBasedNormalizer()
        
        assert normalizer.normalize("I need to search for something") == "find item"
        assert normalizer.normalize("Let me browse the categories") == "browse category"
        assert normalizer.normalize("Submit the form now") == "submit form"
    
    def test_unknown_pattern(self):
        """Test fallback for unknown patterns."""
        normalizer = RuleBasedNormalizer()
        
        assert normalizer.normalize("xyzzy plugh") == "unknown intent"
    
    def test_custom_rules(self):
        """Test adding custom rules."""
        normalizer = RuleBasedNormalizer()
        normalizer.add_rule("frobnicate", "custom operation")
        
        assert normalizer.normalize("I should frobnicate the widget") == "custom operation"


# ============================================
# Hasher Tests
# ============================================

class TestStateHasher:
    """Tests for state hashing."""
    
    def test_deterministic_hash(self):
        """Test that same state gives same hash."""
        hasher = StateHasher()
        state = {"page": "search", "items": [1, 2, 3]}
        
        hash1 = hasher.hash(state)
        hash2 = hasher.hash(state)
        
        assert hash1 == hash2
    
    def test_different_states(self):
        """Test that different states give different hashes."""
        hasher = StateHasher()
        
        hash1 = hasher.hash({"page": "search"})
        hash2 = hasher.hash({"page": "checkout"})
        
        assert hash1 != hash2
    
    def test_ignore_volatile_keys(self):
        """Test that volatile keys are ignored."""
        hasher = StateHasher()
        
        state1 = {"page": "search", "timestamp": "2024-01-01"}
        state2 = {"page": "search", "timestamp": "2024-01-02"}
        
        # Should be same because timestamp is ignored
        assert hasher.hash(state1) == hasher.hash(state2)
    
    def test_empty_state(self):
        """Test handling of empty state."""
        hasher = StateHasher()
        assert hasher.hash({}) == "empty_state"
        assert hasher.hash(None) == "empty_state"
    
    def test_has_changed(self):
        """Test change detection."""
        hasher = StateHasher()
        
        state1 = {"page": "search"}
        hash1 = hasher.hash(state1)
        
        state2 = {"page": "checkout"}
        
        assert hasher.has_changed(hash1, state2) == True
        assert hasher.has_changed(hash1, state1) == False


class TestActionHasher:
    """Tests for action hashing."""
    
    def test_exact_hash(self):
        """Test exact action hashing."""
        hasher = ActionHasher()
        
        hash1 = hasher.hash_exact("search", {"query": "XYZ-9999"})
        hash2 = hasher.hash_exact("search", {"query": "XYZ-9999"})
        hash3 = hasher.hash_exact("search", {"query": "ABC-1234"})
        
        assert hash1 == hash2
        assert hash1 != hash3
    
    def test_normalized_hash(self):
        """Test normalized action hashing."""
        hasher = ActionHasher()
        
        # Different IDs should hash the same when normalized
        hash1 = hasher.hash_normalized("search", {"query": "XYZ-9999"})
        hash2 = hasher.hash_normalized("search", {"query": "ABC-1234"})
        
        assert hash1 == hash2  # Both normalize to search(query=<ID>)
    
    def test_signature(self):
        """Test human-readable signature."""
        hasher = ActionHasher()
        
        sig = hasher.get_signature("search", {"query": "XYZ-9999", "limit": 10})
        assert "search(" in sig
        assert "query=<ID>" in sig


# ============================================
# Failure Memory Tests
# ============================================

class TestFailureMemory:
    """Tests for failure memory."""
    
    def test_record_and_check_action(self):
        """Test recording and checking action failures."""
        memory = FailureMemory()
        
        # Record a failure
        memory.record_failure(
            state_hash="state1",
            action_hash="action1",
            tool_name="search",
            args={"query": "test"},
            error="Not found",
            intent="find item"
        )
        
        # Check it exists
        failure = memory.check_action("state1", "action1")
        assert failure is not None
        assert failure.count == 1
        assert failure.error == "Not found"
        
        # Check non-existent
        assert memory.check_action("state1", "action2") is None
    
    def test_increment_failure_count(self):
        """Test that failure count increments."""
        memory = FailureMemory()
        
        # Record same failure three times
        for i in range(3):
            failure, cluster = memory.record_failure(
                state_hash="state1",
                action_hash="action1",
                tool_name="search",
                args={},
                error="Not found",
                intent="find item"
            )
        
        # Check action failure count
        failure = memory.check_action("state1", "action1")
        assert failure is not None
        assert failure.count == 3
        
        # Check intent cluster total attempts
        cluster = memory.check_intent("state1", "find item")
        assert cluster is not None
        assert cluster.total_attempts == 3
    
    def test_intent_clustering(self):
        """Test that different actions with same intent are clustered."""
        memory = FailureMemory()
        
        # Record different actions with same intent
        memory.record_failure(
            state_hash="state1",
            action_hash="action1",
            tool_name="search",
            args={"query": "XYZ-9999"},
            error="Not found",
            intent="find product by ID"
        )
        
        memory.record_failure(
            state_hash="state1",
            action_hash="action2",
            tool_name="search",
            args={"query": "XYZ9999"},
            error="Not found",
            intent="find product by ID"
        )
        
        # Check intent cluster
        cluster = memory.check_intent("state1", "find product by ID")
        assert cluster is not None
        assert cluster.total_attempts == 2
        assert cluster.get_unique_actions() == 2
    
    def test_dead_intents(self):
        """Test getting dead (exhausted) intents."""
        memory = FailureMemory()
        
        # Record 3 failures for same intent
        for i in range(3):
            memory.record_failure(
                state_hash="state1",
                action_hash=f"action{i}",
                tool_name="search",
                args={"query": f"test{i}"},
                error="Not found",
                intent="find product"
            )
        
        dead = memory.get_dead_intents("state1", threshold=3)
        assert "find product" in dead
    
    def test_clear_state(self):
        """Test clearing state."""
        memory = FailureMemory()
        
        memory.record_failure(
            state_hash="state1",
            action_hash="action1",
            tool_name="search",
            args={},
            error="Not found",
            intent="find item"
        )
        
        memory.clear_state("state1")
        
        assert memory.check_action("state1", "action1") is None
        assert memory.check_intent("state1", "find item") is None


# ============================================
# Smart Guard Tests
# ============================================

class TestSmartGuard:
    """Tests for SmartGuard."""
    
    def test_allow_new_action(self):
        """Test that new actions are allowed."""
        guard = SmartGuard()
        
        result = guard.check(
            state={"page": "search"},
            thought="I should search for something",
            tool_name="search",
            args={"query": "test"}
        )
        
        assert result.decision == Decision.ALLOW
        assert not result.blocked
    
    def test_block_action_repeat(self):
        """Test blocking repeated action."""
        guard = SmartGuard(action_repeat_threshold=2)
        
        state = {"page": "search"}
        thought = "search for product"
        tool = "search"
        args = {"query": "XYZ"}
        
        # First attempt - allow
        result = guard.check(state, thought, tool, args)
        assert result.allowed
        
        # Record failure
        guard.record_failure(state, thought, tool, args, "Not found")
        
        # Second attempt - still allow (threshold is 2)
        result = guard.check(state, thought, tool, args)
        assert result.allowed
        
        # Record another failure
        guard.record_failure(state, thought, tool, args, "Not found")
        
        # Third attempt - now blocked
        result = guard.check(state, thought, tool, args)
        assert result.blocked
        assert result.reason == "exact_action_repeat"
        assert "DO NOT repeat" in result.nudge_message
    
    def test_block_intent_repeat(self):
        """Test blocking repeated intent with different actions."""
        guard = SmartGuard(intent_repeat_threshold=3)
        
        state = {"page": "search"}
        
        # Try different variations of same intent
        variations = [
            ("search for XYZ-9999", "search", {"query": "XYZ-9999"}),
            ("try XYZ9999 instead", "search", {"query": "XYZ9999"}),
            ("maybe XYZ 9999", "search", {"query": "XYZ 9999"}),
        ]
        
        for thought, tool, args in variations:
            # Check should allow
            result = guard.check(state, thought, tool, args)
            assert result.allowed or result.warned
            
            # Record failure
            guard.record_failure(state, thought, tool, args, "Not found")
        
        # Fourth attempt with same intent should be blocked
        result = guard.check(
            state,
            "one more try with XYZ",
            "search",
            {"query": "XYZ-99-99"}
        )
        
        assert result.blocked
        assert result.reason == "intent_exhausted"
        assert "DIFFERENT strategy" in result.nudge_message
    
    def test_nudge_message_format(self):
        """Test that nudge messages are well formatted."""
        guard = SmartGuard(action_repeat_threshold=1)
        
        state = {"page": "search"}
        
        # Record a failure
        guard.record_failure(
            state,
            "search for product",
            "search",
            {"query": "test"},
            "Product not found"
        )
        
        # Try again - should be blocked
        result = guard.check(state, "search for product", "search", {"query": "test"})
        
        assert result.blocked
        assert "[NudgeOps" in result.nudge_message
        assert "Product not found" in result.nudge_message
        assert "DO NOT" in result.nudge_message
    
    def test_stats_tracking(self):
        """Test that stats are tracked."""
        guard = SmartGuard()
        
        state = {"page": "search"}
        
        # Some checks
        guard.check(state, "thought 1", "tool1", {})
        guard.check(state, "thought 2", "tool2", {})
        guard.record_failure(state, "thought 1", "tool1", {}, "error")
        
        stats = guard.get_stats()
        assert stats["checks"] == 2
        assert stats["allows"] == 2
        assert stats["failures_recorded"] == 1
    
    def test_failure_summary(self):
        """Test getting failure summary for state injection."""
        guard = SmartGuard(intent_repeat_threshold=3)
        
        state = {"page": "search"}
        
        # Record 3 failures to exceed threshold
        guard.record_failure(state, "find product", "search", {"q": "1"}, "error")
        guard.record_failure(state, "find product", "search", {"q": "2"}, "error")
        guard.record_failure(state, "find product", "search", {"q": "3"}, "error")
        
        summary = guard.get_failure_summary(state)
        
        assert "dead_intents" in summary
        assert "total_failures" in summary
        assert summary["total_failures"] == 3


# ============================================
# Events Tests
# ============================================

class TestEvents:
    """Tests for failure events."""
    
    def test_canonicalize_error(self):
        """Test error message canonicalization."""
        # The pattern matching is regex-based
        assert canonicalize_error("Error 404: Not Found") == "NOT_FOUND"
        assert canonicalize_error("Product XYZ was not found in the database") == "PRODUCT_NOT_FOUND"
        assert canonicalize_error("Rate limit exceeded, please wait") == "RATE_LIMITED"
        assert canonicalize_error("Request timeout after 30s") == "TIMEOUT"
        assert canonicalize_error("xyzzy plugh") == "UNKNOWN_ERROR"
    
    def test_canonicalize_action(self):
        """Test action canonicalization."""
        sig = canonicalize_action("search", {"query": "XYZ-9999", "limit": 10})
        assert "search(" in sig
        assert "query=*" in sig
        assert "limit=*" in sig
    
    def test_failure_event_serialization(self):
        """Test event serialization."""
        event = FailureEvent(
            tenant_id="acme",
            agent_id="bot1",
            session_id="sess1",
            state_sig="search_page",
            action_sig="search(query=*)",
            intent_sig="find product",
            error_sig="NOT_FOUND",
            failure_type=FailureType.HARD,
            repeat_count=3
        )
        
        # To dict and back
        d = event.to_dict()
        event2 = FailureEvent.from_dict(d)
        
        assert event2.tenant_id == "acme"
        assert event2.failure_type == FailureType.HARD
        assert event2.repeat_count == 3
    
    def test_anonymized_export(self):
        """Test anonymized export strips tenant data."""
        event = FailureEvent(
            tenant_id="secret_tenant",
            agent_id="secret_agent",
            intent_sig="find product",
            error_sig="NOT_FOUND"
        )
        
        anon = event.anonymized()
        
        assert "tenant_id" not in anon
        assert "agent_id" not in anon
        assert anon["intent_sig"] == "find product"


# ============================================
# Observability Tests
# ============================================

class TestObservability:
    """Tests for observability layer."""
    
    def test_record_block(self):
        """Test recording blocked actions."""
        obs = ObservabilityLayer()
        
        obs.record_block(
            tenant_id="acme",
            agent_id="bot1",
            reason="action_repeat",
            intent="find product",
            repeat_count=3
        )
        
        summary = obs.get_tenant_summary("acme")
        assert summary["blocks"] == 1
        assert summary["tokens_saved"] > 0
    
    def test_record_failure(self):
        """Test recording failures."""
        obs = ObservabilityLayer()
        
        obs.record_failure(
            tenant_id="acme",
            agent_id="bot1",
            error_sig="NOT_FOUND",
            intent="find product"
        )
        
        summary = obs.get_tenant_summary("acme")
        assert summary["failures_recorded"] == 1
    
    def test_multiple_agents(self):
        """Test tracking multiple agents."""
        obs = ObservabilityLayer()
        
        obs.record_block("acme", "bot1", "test", repeat_count=1)
        obs.record_block("acme", "bot2", "test", repeat_count=1)
        obs.record_block("acme", "bot1", "test", repeat_count=1)
        
        summary = obs.get_tenant_summary("acme")
        assert summary["agents_monitored"] == 2
        assert summary["blocks"] == 3
    
    def test_roi_dashboard(self):
        """Test ROI dashboard calculation."""
        obs = ObservabilityLayer()
        
        # Simulate some blocks
        for _ in range(100):
            obs.record_block("acme", "bot1", "test", repeat_count=5)
        
        dashboard = obs.get_roi_dashboard("acme", subscription_cost=99.0)
        
        assert "cost_saved_usd" in dashboard
        assert "roi_ratio" in dashboard
        assert "tokens_saved" in dashboard
    
    def test_top_failure_patterns(self):
        """Test getting top failure patterns."""
        obs = ObservabilityLayer()
        
        # Record various failures
        for _ in range(10):
            obs.record_failure("acme", "bot1", "NOT_FOUND", "find product")
        for _ in range(5):
            obs.record_failure("acme", "bot1", "TIMEOUT", "api call")
        
        patterns = obs.get_top_failure_patterns("acme")
        
        assert len(patterns) == 2
        assert patterns[0]["count"] == 10  # Most common first


# ============================================
# Integration Tests
# ============================================

class TestIntegration:
    """Integration tests for full workflow."""
    
    def test_full_workflow(self):
        """Test complete workflow from check to block."""
        # Setup
        guard = SmartGuard(
            action_repeat_threshold=2,
            intent_repeat_threshold=3
        )
        obs = ObservabilityLayer()
        
        state = {"page": "search", "query": ""}
        
        # Simulate agent loop
        attempts = [
            ("search for XYZ-9999", "search", {"q": "XYZ-9999"}),
            ("try without hyphen", "search", {"q": "XYZ9999"}),
            ("try with space", "search", {"q": "XYZ 9999"}),
            ("one more try", "search", {"q": "XYZ-99-99"}),
        ]
        
        blocked_at = None
        for i, (thought, tool, args) in enumerate(attempts):
            result = guard.check(state, thought, tool, args)
            
            if result.blocked:
                blocked_at = i
                obs.record_block("test", "agent1", result.reason, result.intent)
                break
            
            # Simulate failure
            guard.record_failure(state, thought, tool, args, "Product not found")
            obs.record_failure("test", "agent1", "NOT_FOUND", result.intent)
        
        # Should be blocked at attempt 3 (0-indexed)
        assert blocked_at == 3
        
        # Check stats
        stats = guard.get_stats()
        assert stats["blocks"] == 1
        assert stats["failures_recorded"] == 3
        
        # Check observability
        summary = obs.get_tenant_summary("test")
        assert summary["blocks"] == 1
        assert summary["failures_recorded"] == 3


# ============================================
# Run tests
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
LangGraph Integration for Smart NudgeOps.

Provides easy integration with LangGraph workflows:
- Wraps tool nodes with guard checking
- Injects nudge messages when actions are blocked
- Injects failure summary into state for downstream agents
"""

from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass
import functools

from .guard import SmartGuard, GuardResult, Decision
from .thought_normalizer import LLMClient, MockLLMClient
from .observability import ObservabilityLayer, get_observability
from .events import FailureEventBuilder, RecoveryStatus


@dataclass
class SmartNudgeOpsConfig:
    """Configuration for SmartNudgeOps integration."""
    
    # Thresholds
    action_repeat_threshold: int = 2
    intent_repeat_threshold: int = 3
    warn_threshold: int = 2
    
    # Injection settings
    inject_nudge_as: str = "system"  # "system", "human", or "assistant"
    inject_failure_summary: bool = True
    failure_summary_key: str = "nudgeops_failure_summary"
    
    # Tenant/Agent identification
    tenant_id: str = "default"
    agent_id: str = "agent"
    
    # Observability
    enable_observability: bool = True


class SmartNudgeOps:
    """
    LangGraph integration for SmartGuard.
    
    Usage:
        from nudgeops.smart import SmartNudgeOps
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini")
        nudgeops = SmartNudgeOps(llm_client=llm)
        
        # Apply to graph builder
        nudgeops.apply(builder)
        
        # Or wrap individual functions
        @nudgeops.guard
        def my_tool_node(state):
            ...
    """
    
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        config: Optional[SmartNudgeOpsConfig] = None,
        observability: Optional[ObservabilityLayer] = None
    ):
        """
        Initialize SmartNudgeOps.
        
        Args:
            llm_client: LLM client for thought normalization
            config: Configuration options
            observability: Observability layer (uses global if not provided)
        """
        self.config = config or SmartNudgeOpsConfig()
        self.llm_client = llm_client or MockLLMClient()
        self.observability = observability or get_observability()
        
        self.guard = SmartGuard(
            llm_client=self.llm_client,
            action_repeat_threshold=self.config.action_repeat_threshold,
            intent_repeat_threshold=self.config.intent_repeat_threshold,
            warn_threshold=self.config.warn_threshold
        )
    
    def apply(self, builder: Any) -> Any:
        """
        Apply SmartNudgeOps to a LangGraph StateGraph builder.
        
        Wraps all tool nodes with guard checking.
        
        Args:
            builder: LangGraph StateGraph builder
            
        Returns:
            Modified builder
        """
        # Get original nodes
        original_nodes = dict(builder.nodes)
        
        for node_name, node_func in original_nodes.items():
            if self._is_tool_node(node_name):
                wrapped = self._wrap_node(node_name, node_func)
                builder.nodes[node_name] = wrapped
        
        return builder
    
    def guard_node(
        self,
        node_func: Callable,
        node_name: Optional[str] = None
    ) -> Callable:
        """
        Decorator to wrap a single node with guard checking.
        
        Usage:
            @nudgeops.guard_node
            def my_tool(state):
                ...
        """
        return self._wrap_node(node_name or node_func.__name__, node_func)
    
    def check(
        self,
        state: Dict[str, Any],
        thought: str,
        tool_name: str,
        args: Dict[str, Any]
    ) -> GuardResult:
        """
        Check if action should be allowed.
        
        Direct access to guard for manual integration.
        """
        result = self.guard.check(state, thought, tool_name, args)
        
        # Record in observability
        if self.config.enable_observability:
            self._record_check_result(result)
        
        return result
    
    def record_failure(
        self,
        state: Dict[str, Any],
        thought: str,
        tool_name: str,
        args: Dict[str, Any],
        error: str,
        error_code: Optional[str] = None
    ):
        """Record a failed action."""
        self.guard.record_failure(state, thought, tool_name, args, error, error_code)
        
        if self.config.enable_observability:
            from .events import canonicalize_error
            self.observability.record_failure(
                tenant_id=self.config.tenant_id,
                agent_id=self.config.agent_id,
                error_sig=canonicalize_error(error),
                intent=self.guard.normalizer.normalize(thought) if thought else None
            )
    
    def get_failure_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Get failure summary for injection."""
        return self.guard.get_failure_summary(state)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get combined stats from guard and observability."""
        return {
            "guard": self.guard.get_stats(),
            "observability": self.observability.get_tenant_summary(
                self.config.tenant_id
            )
        }
    
    def reset(self):
        """Reset all state."""
        self.guard.reset()
    
    # --- Internal Methods ---
    
    def _is_tool_node(self, node_name: str) -> bool:
        """Check if node is a tool node (not agent or special nodes)."""
        special_nodes = {"agent", "__start__", "__end__", "start", "end"}
        return node_name.lower() not in special_nodes
    
    def _wrap_node(self, node_name: str, node_func: Callable) -> Callable:
        """Wrap a node function with guard checking."""
        
        @functools.wraps(node_func)
        def wrapped(state: Dict[str, Any]) -> Dict[str, Any]:
            # Extract thought and action from state
            thought, tool_name, args = self._extract_from_state(state)
            
            # Default tool_name to node_name if not found
            if not tool_name:
                tool_name = node_name
            
            # Check with guard
            result = self.check(state, thought, tool_name, args)
            
            if result.blocked:
                # Inject nudge message instead of executing
                return self._inject_nudge(state, result.nudge_message)
            
            # Execute original node
            try:
                output = node_func(state)
                
                # Inject failure summary if configured
                if self.config.inject_failure_summary:
                    output = self._inject_failure_summary(state, output)
                
                return output
                
            except Exception as e:
                # Record failure
                self.record_failure(
                    state=state,
                    thought=thought,
                    tool_name=tool_name,
                    args=args,
                    error=str(e)
                )
                raise
        
        return wrapped
    
    def _extract_from_state(self, state: Dict[str, Any]) -> tuple:
        """
        Extract thought, tool_name, and args from state.
        
        Looks for common patterns in LangGraph state.
        """
        thought = ""
        tool_name = ""
        args = {}
        
        # Try to get from messages
        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            
            # Extract thought from content
            if hasattr(last_message, "content"):
                thought = str(last_message.content)
            elif isinstance(last_message, dict):
                thought = str(last_message.get("content", ""))
            
            # Extract tool call
            tool_calls = None
            if hasattr(last_message, "tool_calls"):
                tool_calls = last_message.tool_calls
            elif isinstance(last_message, dict):
                tool_calls = last_message.get("tool_calls", [])
            
            if tool_calls and len(tool_calls) > 0:
                call = tool_calls[0]
                if isinstance(call, dict):
                    tool_name = call.get("name", "")
                    args = call.get("args", {})
                elif hasattr(call, "name"):
                    tool_name = call.name
                    args = getattr(call, "args", {})
        
        # Fallback: check for direct state keys
        if not tool_name:
            tool_name = state.get("current_tool", state.get("tool_name", ""))
        if not args:
            args = state.get("tool_args", state.get("args", {}))
        if not thought:
            thought = state.get("thought", state.get("reasoning", ""))
        
        return thought, tool_name, args
    
    def _inject_nudge(self, state: Dict[str, Any], nudge: str) -> Dict[str, Any]:
        """Inject nudge message into state."""
        new_state = dict(state)
        
        # Try to inject as message
        messages = list(state.get("messages", []))
        
        try:
            # Try LangChain message types
            if self.config.inject_nudge_as == "system":
                from langchain_core.messages import SystemMessage
                msg = SystemMessage(content=nudge)
            elif self.config.inject_nudge_as == "human":
                from langchain_core.messages import HumanMessage
                msg = HumanMessage(content=nudge)
            else:
                from langchain_core.messages import AIMessage
                msg = AIMessage(content=nudge)
            
            messages.append(msg)
        except ImportError:
            # Fallback to dict format
            messages.append({
                "role": self.config.inject_nudge_as,
                "content": nudge
            })
        
        new_state["messages"] = messages
        
        # Also add as separate field
        new_state["nudgeops_nudge"] = nudge
        new_state["nudgeops_blocked"] = True
        
        return new_state
    
    def _inject_failure_summary(
        self,
        original_state: Dict[str, Any],
        output: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Inject failure summary into output state."""
        summary = self.get_failure_summary(original_state)
        
        if summary.get("dead_intents") or summary.get("total_failures", 0) > 0:
            output[self.config.failure_summary_key] = summary
        
        return output
    
    def _record_check_result(self, result: GuardResult):
        """Record check result in observability."""
        if result.blocked:
            self.observability.record_block(
                tenant_id=self.config.tenant_id,
                agent_id=self.config.agent_id,
                reason=result.reason or "unknown",
                intent=result.intent,
                repeat_count=result.metadata.get("repeat_count", 1)
            )
        elif result.warned:
            self.observability.record_warn(
                tenant_id=self.config.tenant_id,
                agent_id=self.config.agent_id,
                reason=result.reason or "unknown",
                intent=result.intent
            )
        else:
            self.observability.record_allow(
                tenant_id=self.config.tenant_id,
                agent_id=self.config.agent_id
            )


class SmartNudgeOpsBuilder:
    """Builder for SmartNudgeOps with fluent API."""
    
    def __init__(self):
        self._llm_client = None
        self._config = SmartNudgeOpsConfig()
        self._observability = None
    
    def with_llm(self, client: LLMClient) -> "SmartNudgeOpsBuilder":
        """Set LLM client for thought normalization."""
        self._llm_client = client
        return self
    
    def with_action_threshold(self, threshold: int) -> "SmartNudgeOpsBuilder":
        """Set action repeat threshold."""
        self._config.action_repeat_threshold = threshold
        return self
    
    def with_intent_threshold(self, threshold: int) -> "SmartNudgeOpsBuilder":
        """Set intent repeat threshold."""
        self._config.intent_repeat_threshold = threshold
        return self
    
    def with_tenant(self, tenant_id: str) -> "SmartNudgeOpsBuilder":
        """Set tenant ID for observability."""
        self._config.tenant_id = tenant_id
        return self
    
    def with_agent(self, agent_id: str) -> "SmartNudgeOpsBuilder":
        """Set agent ID for observability."""
        self._config.agent_id = agent_id
        return self
    
    def with_observability(self, obs: ObservabilityLayer) -> "SmartNudgeOpsBuilder":
        """Set observability layer."""
        self._observability = obs
        return self
    
    def without_observability(self) -> "SmartNudgeOpsBuilder":
        """Disable observability."""
        self._config.enable_observability = False
        return self
    
    def with_nudge_injection(
        self,
        inject_as: str = "system",
        inject_summary: bool = True
    ) -> "SmartNudgeOpsBuilder":
        """Configure nudge injection."""
        self._config.inject_nudge_as = inject_as
        self._config.inject_failure_summary = inject_summary
        return self
    
    def build(self) -> SmartNudgeOps:
        """Build SmartNudgeOps instance."""
        return SmartNudgeOps(
            llm_client=self._llm_client,
            config=self._config,
            observability=self._observability
        )


# Convenience function for quick setup
def apply_smart_guard(
    builder: Any,
    llm_client: Optional[LLMClient] = None,
    action_threshold: int = 2,
    intent_threshold: int = 3
) -> Any:
    """
    Quick helper to apply SmartNudgeOps to a LangGraph builder.
    
    Usage:
        from nudgeops.smart import apply_smart_guard
        
        builder = StateGraph(AgentState)
        # ... add nodes and edges ...
        apply_smart_guard(builder, llm_client=my_llm)
        graph = builder.compile()
    """
    nudgeops = SmartNudgeOpsBuilder() \
        .with_llm(llm_client) \
        .with_action_threshold(action_threshold) \
        .with_intent_threshold(intent_threshold) \
        .build()
    
    return nudgeops.apply(builder)

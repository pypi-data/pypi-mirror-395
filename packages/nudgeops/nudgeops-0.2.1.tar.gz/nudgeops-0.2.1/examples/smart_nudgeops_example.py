"""
Example: Using SmartNudgeOps with LangGraph and OpenAI

This shows how to integrate SmartNudgeOps with a real LLM agent.
"""

import os
from typing import Annotated, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Import SmartNudgeOps
from nudgeops.smart import (
    SmartNudgeOps,
    SmartNudgeOpsBuilder,
    SmartNudgeOpsConfig,
)


# ============================================
# 1. Define Agent State
# ============================================

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    current_page: str
    search_results: List[dict]
    cart: List[dict]


# ============================================
# 2. Define Tools
# ============================================

def search_product(query: str) -> dict:
    """Mock product search that fails for certain queries."""
    # Simulate failures for demo
    if "XYZ" in query.upper():
        raise Exception("Product not found: No products match your query")
    return {"products": [{"id": "ABC-123", "name": "Sample Product"}]}


def browse_category(category: str) -> dict:
    """Browse product category."""
    return {"products": [{"id": "CAT-001", "name": f"Product in {category}"}]}


def add_to_cart(product_id: str) -> dict:
    """Add product to cart."""
    return {"success": True, "cart_size": 1}


TOOLS = {
    "search_product": search_product,
    "browse_category": browse_category,
    "add_to_cart": add_to_cart,
}


# ============================================
# 3. Define LLM and Nodes
# ============================================

def create_agent():
    """Create the LLM agent."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Bind tools to LLM
    tools_schema = [
        {
            "type": "function",
            "function": {
                "name": "search_product",
                "description": "Search for a product by name or ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "browse_category",
                "description": "Browse products in a category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category name"}
                    },
                    "required": ["category"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_to_cart",
                "description": "Add a product to the cart",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string", "description": "Product ID"}
                    },
                    "required": ["product_id"]
                }
            }
        }
    ]
    
    return llm.bind(tools=tools_schema)


def agent_node(state: AgentState) -> dict:
    """Agent reasoning node."""
    llm = create_agent()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def tool_node(state: AgentState) -> dict:
    """Execute tool calls."""
    messages = state["messages"]
    last_message = messages[-1]
    
    results = []
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            
            if tool_name in TOOLS:
                try:
                    result = TOOLS[tool_name](**tool_args)
                    results.append({
                        "tool_call_id": tool_call["id"],
                        "content": str(result)
                    })
                except Exception as e:
                    results.append({
                        "tool_call_id": tool_call["id"],
                        "content": f"Error: {str(e)}"
                    })
    
    # Convert to tool messages
    from langchain_core.messages import ToolMessage
    tool_messages = [
        ToolMessage(content=r["content"], tool_call_id=r["tool_call_id"])
        for r in results
    ]
    
    return {"messages": tool_messages}


def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if blocked by NudgeOps
    if state.get("nudgeops_blocked"):
        return "agent"  # Let agent see the nudge and respond
    
    # Check if agent wants to use tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return END


# ============================================
# 4. Build Graph with SmartNudgeOps
# ============================================

def build_graph_with_nudgeops():
    """Build the agent graph with SmartNudgeOps protection."""
    
    # Create SmartNudgeOps
    # Option 1: Simple setup with mock LLM (for testing)
    from nudgeops.smart import MockLLMClient
    nudgeops = SmartNudgeOps(
        llm_client=MockLLMClient(),
        config=SmartNudgeOpsConfig(
            action_repeat_threshold=2,
            intent_repeat_threshold=3,
            tenant_id="demo",
            agent_id="ecommerce-bot"
        )
    )
    
    # Option 2: With real LLM for thought normalization (production)
    # llm = ChatOpenAI(model="gpt-4o-mini")
    # 
    # # Wrap to match LLMClient protocol
    # class OpenAIWrapper:
    #     def __init__(self, llm):
    #         self.llm = llm
    #     def complete(self, prompt: str) -> str:
    #         return self.llm.invoke(prompt).content
    # 
    # nudgeops = SmartNudgeOps(llm_client=OpenAIWrapper(llm))
    
    # Build graph
    builder = StateGraph(AgentState)
    
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)
    
    builder.set_entry_point("agent")
    builder.add_conditional_edges("agent", should_continue)
    builder.add_edge("tools", "agent")
    
    # Apply NudgeOps - wraps tool node with guard
    nudgeops.apply(builder)
    
    return builder.compile(), nudgeops


# ============================================
# 5. Run Example
# ============================================

def run_example():
    """Run the example agent."""
    
    print("=" * 60)
    print("SmartNudgeOps Demo: E-commerce Agent")
    print("=" * 60)
    
    graph, nudgeops = build_graph_with_nudgeops()
    
    # Initial state
    initial_state = {
        "messages": [
            HumanMessage(content="Find product XYZ-9999 and add it to my cart")
        ],
        "current_page": "home",
        "search_results": [],
        "cart": []
    }
    
    print("\nUser: Find product XYZ-9999 and add it to my cart\n")
    print("-" * 60)
    
    # Run agent
    try:
        # With a real LLM this would run the full loop
        # For demo, we'll simulate the steps
        print("Note: This demo requires OPENAI_API_KEY to run with real LLM")
        print("Running with mock components for demonstration...")
        print()
        
        # Simulate the flow
        state = {"page": "search", "query": ""}
        
        # Simulate agent trying same strategy
        attempts = [
            ("search for XYZ-9999", "search_product", {"query": "XYZ-9999"}),
            ("try without hyphen", "search_product", {"query": "XYZ9999"}),
            ("try with space", "search_product", {"query": "XYZ 9999"}),
            ("one more try", "search_product", {"query": "XYZ-99-99"}),
        ]
        
        for i, (thought, tool, args) in enumerate(attempts):
            print(f"Step {i+1}:")
            print(f"  Thought: {thought}")
            print(f"  Action: {tool}({args})")
            
            # Check with guard
            result = nudgeops.check(state, thought, tool, args)
            
            if result.blocked:
                print(f"  → BLOCKED by NudgeOps!")
                print(f"  Reason: {result.reason}")
                print()
                print("Nudge message injected:")
                print("-" * 40)
                print(result.nudge_message)
                print("-" * 40)
                break
            else:
                # Simulate failure
                error = "Product not found"
                print(f"  → Executed: Error - {error}")
                nudgeops.record_failure(state, thought, tool, args, error)
            print()
        
        # Show stats
        print()
        print("=" * 60)
        print("Guard Statistics:")
        print("=" * 60)
        stats = nudgeops.get_stats()
        print(f"  Checks: {stats['guard']['checks']}")
        print(f"  Allows: {stats['guard']['allows']}")
        print(f"  Blocks: {stats['guard']['blocks']}")
        print(f"  Failures recorded: {stats['guard']['failures_recorded']}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise


# ============================================
# 6. Usage without LangGraph (Manual)
# ============================================

def manual_usage_example():
    """Example of using SmartGuard directly without LangGraph."""
    
    from nudgeops.smart import SmartGuard, MockLLMClient
    
    print("\n" + "=" * 60)
    print("Manual Usage Example (without LangGraph)")
    print("=" * 60 + "\n")
    
    # Create guard
    guard = SmartGuard(
        llm_client=MockLLMClient(),
        action_repeat_threshold=2,
        intent_repeat_threshold=3
    )
    
    # Simulate agent state
    state = {"page": "checkout", "cart_items": 2}
    
    # Agent's first attempt
    thought = "I need to search for product XYZ"
    tool = "search"
    args = {"query": "XYZ-9999"}
    
    result = guard.check(state, thought, tool, args)
    print(f"Attempt 1: {result.decision.value}")
    
    if result.allowed:
        # Simulate failure
        guard.record_failure(state, thought, tool, args, "Not found")
    
    # Second attempt (different action, same intent)
    thought = "Let me try another format"
    args = {"query": "XYZ9999"}
    
    result = guard.check(state, thought, tool, args)
    print(f"Attempt 2: {result.decision.value}")
    
    if result.allowed:
        guard.record_failure(state, thought, tool, args, "Not found")
    
    # Third attempt
    thought = "Maybe with spaces"
    args = {"query": "XYZ 9999"}
    
    result = guard.check(state, thought, tool, args)
    print(f"Attempt 3: {result.decision.value}")
    
    if result.allowed:
        guard.record_failure(state, thought, tool, args, "Not found")
    
    # Fourth attempt - should be blocked
    thought = "One more try"
    args = {"query": "XYZ--9999"}
    
    result = guard.check(state, thought, tool, args)
    print(f"Attempt 4: {result.decision.value}")
    
    if result.blocked:
        print(f"\nBlocked! Reason: {result.reason}")
        print(f"Intent detected: {result.intent}")
    
    # Get failure summary for downstream agents
    summary = guard.get_failure_summary(state)
    print(f"\nFailure summary: {summary}")


if __name__ == "__main__":
    run_example()
    manual_usage_example()

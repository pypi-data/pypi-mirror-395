"""
Thought Normalizer - Converts agent thoughts to canonical intents.

Uses LLM to summarize thoughts to ~5 words, enabling semantic comparison
without embeddings. Different phrasings of same intent = same output.

Example:
    "I should search for the product using its ID XYZ-9999" → "find product by ID"
    "Let me try without the hyphen" → "find product by ID"
    "Maybe with spaces instead" → "find product by ID"
"""

import hashlib
from typing import Optional, Protocol, Dict, Any
from collections import OrderedDict


class LLMClient(Protocol):
    """Protocol for LLM clients."""
    def complete(self, prompt: str) -> str:
        """Generate completion for prompt."""
        ...


class MockLLMClient:
    """Mock LLM client for testing."""
    
    def __init__(self, responses: Dict[str, str] = None):
        self.responses = responses or {}
        self.calls = []
    
    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        
        # Check for exact match first
        if prompt in self.responses:
            return self.responses[prompt]
        
        # Try to extract thought from prompt and match
        for key, value in self.responses.items():
            if key.lower() in prompt.lower():
                return value
        
        # Default response based on content
        prompt_lower = prompt.lower()
        if "search" in prompt_lower or "find" in prompt_lower or "id" in prompt_lower:
            return "find product by ID"
        if "browse" in prompt_lower or "category" in prompt_lower:
            return "browse by category"
        if "cart" in prompt_lower or "checkout" in prompt_lower:
            return "complete checkout"
        if "retry" in prompt_lower or "again" in prompt_lower:
            return "retry failed request"
        
        return "unknown intent"


class LRUCache:
    """Simple LRU cache implementation."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: str):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                # Remove oldest
                self.cache.popitem(last=False)
        self.cache[key] = value
    
    def __contains__(self, key: str) -> bool:
        return key in self.cache
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __bool__(self) -> bool:
        """Cache always evaluates to True (it exists)."""
        return True


class ThoughtNormalizer:
    """
    Normalizes agent thoughts to canonical intents using LLM.
    
    The key insight: We don't need embeddings or vector similarity.
    We just need to reduce diverse thoughts to a small set of canonical intents.
    
    Usage:
        normalizer = ThoughtNormalizer(llm_client)
        intent = normalizer.normalize("I should search for product XYZ-9999")
        # Returns: "find product by ID"
    """
    
    SYSTEM_PROMPT = """You are an intent classifier. Your job is to summarize 
what an AI agent is trying to accomplish in exactly 5 words or less.

Rules:
1. Focus on WHAT, not HOW
2. Remove specific values (IDs, names, numbers, URLs)
3. Use simple, generic terms
4. Be consistent - same intent should always give same output

Examples:
- "I should search for the product using its ID XYZ-9999" → "find product by ID"
- "Let me try the search without the hyphen" → "find product by ID"  
- "I'll browse the electronics category" → "browse by category"
- "Let me check if checkout works now" → "complete checkout"
- "The API returned 404, trying again" → "retry failed request"
- "I need to read the error logs" → "read error logs"
- "Let me open the file main.py" → "open file"
"""

    def __init__(
        self, 
        llm_client: LLMClient,
        cache_size: int = 1000,
        use_cache: bool = True
    ):
        """
        Initialize the thought normalizer.
        
        Args:
            llm_client: Any LLM client with a complete() method
            cache_size: Max number of cached normalizations
            use_cache: Whether to cache results
        """
        self.llm = llm_client
        self.cache = LRUCache(cache_size) if use_cache else None
        self.stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "total_calls": 0
        }
    
    def normalize(self, thought: str) -> str:
        """
        Normalize a thought to a canonical intent string.
        
        Args:
            thought: The agent's raw reasoning/thought
            
        Returns:
            A canonical intent string (5 words or less)
        """
        if not thought or not thought.strip():
            return "no intent"
        
        self.stats["total_calls"] += 1
        
        # Hash the thought BEFORE building prompt
        thought_hash = self._hash(thought)
        
        # Check cache
        if self.cache:
            cached = self.cache.get(thought_hash)
            if cached:
                self.stats["cache_hits"] += 1
                return cached
            self.stats["cache_misses"] += 1
        
        # Call LLM
        prompt = self._build_prompt(thought)
        response = self.llm.complete(prompt)
        
        # Clean up response
        intent = self._clean_response(response)
        
        # Cache result
        if self.cache:
            self.cache.set(thought_hash, intent)
        
        return intent
    
    def normalize_batch(self, thoughts: list) -> list:
        """Normalize multiple thoughts."""
        return [self.normalize(t) for t in thoughts]
    
    def _build_prompt(self, thought: str) -> str:
        """Build the prompt for LLM."""
        return f"""{self.SYSTEM_PROMPT}

Now classify this thought:
"{thought}"

Intent (5 words max):"""

    def _clean_response(self, response: str) -> str:
        """Clean and normalize the LLM response."""
        # Strip whitespace and quotes
        intent = response.strip().strip('"\'').strip()
        
        # Lowercase for consistency
        intent = intent.lower()
        
        # Remove trailing punctuation
        intent = intent.rstrip('.')
        
        # Truncate if too long (shouldn't happen with good prompting)
        words = intent.split()
        if len(words) > 7:
            intent = ' '.join(words[:5])
        
        return intent
    
    def _hash(self, text: str) -> str:
        """Create hash of text for caching."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get normalization statistics."""
        stats = self.stats.copy()
        if stats["total_calls"] > 0:
            stats["cache_hit_rate"] = stats["cache_hits"] / stats["total_calls"]
        else:
            stats["cache_hit_rate"] = 0.0
        return stats


# Pre-defined intent mappings for common patterns (optional optimization)
COMMON_INTENTS = {
    # Search patterns
    "search": "find item",
    "find": "find item",
    "lookup": "find item",
    "query": "find item",
    
    # Navigation patterns
    "browse": "browse category",
    "navigate": "navigate to page",
    "go to": "navigate to page",
    
    # Action patterns
    "click": "interact with element",
    "select": "select option",
    "submit": "submit form",
    "add to cart": "add to cart",
    "checkout": "complete checkout",
    
    # File operations
    "read": "read file",
    "write": "write file",
    "open": "open file",
    "edit": "edit file",
    
    # Error handling
    "retry": "retry operation",
    "try again": "retry operation",
}


class RuleBasedNormalizer:
    """
    Fast, rule-based normalizer for common patterns.
    Use as a fallback or for testing without LLM.
    """
    
    def __init__(self):
        self.rules = COMMON_INTENTS.copy()
    
    def normalize(self, thought: str) -> str:
        """Normalize using rule-based matching."""
        thought_lower = thought.lower()
        
        for pattern, intent in self.rules.items():
            if pattern in thought_lower:
                return intent
        
        return "unknown intent"
    
    def add_rule(self, pattern: str, intent: str):
        """Add a custom rule."""
        self.rules[pattern.lower()] = intent


class HybridNormalizer:
    """
    Combines rule-based (fast) and LLM-based (accurate) normalization.
    Uses rules first, falls back to LLM if no match.
    """
    
    def __init__(self, llm_client: LLMClient, cache_size: int = 1000):
        self.rule_normalizer = RuleBasedNormalizer()
        self.llm_normalizer = ThoughtNormalizer(llm_client, cache_size)
    
    def normalize(self, thought: str) -> str:
        """
        Normalize thought using hybrid approach.
        
        1. Try rule-based first (fast)
        2. If unknown, use LLM (accurate)
        """
        intent = self.rule_normalizer.normalize(thought)
        
        if intent == "unknown intent":
            intent = self.llm_normalizer.normalize(thought)
        
        return intent

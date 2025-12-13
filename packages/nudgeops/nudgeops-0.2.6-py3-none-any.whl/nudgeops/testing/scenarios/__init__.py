"""
Scenario behaviors for mock testing.

Each scenario defines a specific failure pattern that an agent might fall into.
These are passed to mock environments to control how they respond to actions.

Code scenarios (from SWE-agent, Cursor, Claude Code research):
- infinite_edit_loop_behavior: Fix-Break-Fix oscillation
- compile_retry_loop_behavior: Same compile error repeatedly
- submit_spam_loop_behavior: 24+ useless submits
- phantom_edit_behavior: Silent edit failures
- hallucinated_library_behavior: Non-existent packages
- hallucination_spiral_behavior: Cascading fabrication
- daemon_linter_behavior: Impossible task (measures TTGU)
- ping_pong_handoff_behavior: Multi-agent deadlock

Shopping scenarios (from Amazon's "Buy For Me" research):
- variant_oos_loop_behavior: Size OOS variations
- checkout_sequence_error_behavior: Wrong step order
- search_synonym_loop_behavior: Semantic search loop
- add_to_cart_retry_loop_behavior: Missing prerequisite
- button_confusion_behavior: Dark pattern traps
- multi_agent_shopping_pingpong: Search↔Compare deadlock
"""

from __future__ import annotations

from nudgeops.testing.scenarios.code_scenarios import (
    infinite_edit_loop_behavior,
    compile_retry_loop_behavior,
    submit_spam_loop_behavior,
    phantom_edit_behavior,
    hallucinated_library_behavior,
    hallucination_spiral_behavior,
    daemon_linter_behavior,
    ping_pong_handoff_behavior,
)
from nudgeops.testing.scenarios.shopping_scenarios import (
    variant_oos_loop_behavior,
    checkout_sequence_error_behavior,
    search_synonym_loop_behavior,
    add_to_cart_retry_loop_behavior,
    button_confusion_behavior,
    multi_agent_shopping_pingpong,
)

__all__ = [
    # Code scenarios
    "infinite_edit_loop_behavior",
    "compile_retry_loop_behavior",
    "submit_spam_loop_behavior",
    "phantom_edit_behavior",
    "hallucinated_library_behavior",
    "hallucination_spiral_behavior",
    "daemon_linter_behavior",
    "ping_pong_handoff_behavior",
    # Shopping scenarios
    "variant_oos_loop_behavior",
    "checkout_sequence_error_behavior",
    "search_synonym_loop_behavior",
    "add_to_cart_retry_loop_behavior",
    "button_confusion_behavior",
    "multi_agent_shopping_pingpong",
]

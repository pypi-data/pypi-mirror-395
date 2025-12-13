"""
Domain-specific mock environments for testing.

Provides simulated environments for different agent types:
- MockCodeEnvironment: Simulates a code repository
- MockShoppingEnvironment: Simulates an e-commerce site
"""

from __future__ import annotations

from nudgeops.testing.environments.code_env import (
    CodeState,
    MockCodeEnvironment,
    ScenarioBehavior as CodeScenarioBehavior,
)
from nudgeops.testing.environments.shopping_env import (
    ShoppingState,
    MockShoppingEnvironment,
    ScenarioBehavior as ShoppingScenarioBehavior,
)

__all__ = [
    # Code environment
    "CodeState",
    "MockCodeEnvironment",
    "CodeScenarioBehavior",
    # Shopping environment
    "ShoppingState",
    "MockShoppingEnvironment",
    "ShoppingScenarioBehavior",
]

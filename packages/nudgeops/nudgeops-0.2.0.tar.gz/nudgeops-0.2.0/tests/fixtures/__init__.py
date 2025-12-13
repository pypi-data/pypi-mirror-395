"""
Test fixtures for NudgeOps.
"""

from tests.fixtures.synthetic_loops import (
    TYPE_I_STUTTER_HISTORY,
    TYPE_II_INSANITY_HISTORY,
    TYPE_III_PHANTOM_HISTORY,
    TYPE_IV_PINGPONG_HISTORY,
    create_stutter_scenario,
    create_insanity_scenario,
    create_phantom_scenario,
    create_pingpong_scenario,
)
from tests.fixtures.legitimate_patterns import (
    VALID_ITERATION_HISTORY,
    VALID_SEARCH_REFINEMENT_HISTORY,
    create_valid_iteration_scenario,
)

__all__ = [
    "TYPE_I_STUTTER_HISTORY",
    "TYPE_II_INSANITY_HISTORY",
    "TYPE_III_PHANTOM_HISTORY",
    "TYPE_IV_PINGPONG_HISTORY",
    "VALID_ITERATION_HISTORY",
    "VALID_SEARCH_REFINEMENT_HISTORY",
    "create_stutter_scenario",
    "create_insanity_scenario",
    "create_phantom_scenario",
    "create_pingpong_scenario",
    "create_valid_iteration_scenario",
]

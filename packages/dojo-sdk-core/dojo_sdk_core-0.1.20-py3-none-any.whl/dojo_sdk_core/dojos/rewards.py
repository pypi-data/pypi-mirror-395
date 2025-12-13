"""
Centralized reward functions for all dojos.

This module serves as a compatibility wrapper that imports from the modular
rewards package. All reward validation functions are organized by game/application
in the rewards/ subdirectory.

Each function takes (initial_state, final_state) and returns (score, reason).
"""

import logging

# Import from modular rewards package
from dojo_sdk_core.dojos.rewards import REWARD_FUNCTIONS, get_reward_function

logger = logging.getLogger(__name__)

# Re-export for backward compatibility
__all__ = ["REWARD_FUNCTIONS", "get_reward_function"]

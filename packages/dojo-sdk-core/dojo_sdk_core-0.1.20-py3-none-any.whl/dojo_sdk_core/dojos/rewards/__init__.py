"""
Modular reward functions organized by game/application.
"""

from dojo_sdk_core.dojos.rewards.jd_v2 import REWARD_FUNCTIONS_JD_V2
from dojo_sdk_core.dojos.rewards.weibo_v2 import REWARD_FUNCTIONS_WEIBO_V2
from dojo_sdk_core.dojos.rewards.xiaohongshu_v2 import (
    REWARD_FUNCTIONS_XIAOHONGSHU_V2,
    StateKey,
    StateKeyQuery,
    ValidateTask,
)

REWARD_FUNCTIONS = {
    **REWARD_FUNCTIONS_XIAOHONGSHU_V2,
    **REWARD_FUNCTIONS_JD_V2,
    **REWARD_FUNCTIONS_WEIBO_V2,
}


def get_reward_function(name: str) -> ValidateTask | None:
    """Get a ValidateTask by name from the unified registry."""
    return REWARD_FUNCTIONS.get(name)


__all__ = ["REWARD_FUNCTIONS", "get_reward_function", "ValidateTask", "StateKey", "StateKeyQuery"]

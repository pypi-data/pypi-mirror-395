"""
Reward functions for 2048 game tasks.

All functions validate the final board state, accounting for randomly spawned tiles.
Board is a 16-element array representing a 4x4 grid:
  [0, 1, 2, 3,
   4, 5, 6, 7,
   8, 9, 10, 11,
   12, 13, 14, 15]
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_get_2048(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 2048 tile is present on the board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")
    if 2048 in final_state["board"]:
        return 1.0, "A 2048 tile is present."
    return 0.0, "No 2048 tile is present."


def _validate_2048_make_first_move(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that any valid move was made from the initial board state."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    # Check if board changed (has non-zero tiles)
    if any(tile != 0 for tile in final_state["board"]):
        return 1.0, "Board changed from initial state - move was made successfully."

    return 0.0, "Board is still empty - no move was made."


def _validate_move_tiles_right(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that all tiles are in the rightmost column (positions 3, 7, 11, 15)."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]
    rightmost_positions = [3, 7, 11, 15]

    # Get all non-zero tiles and their positions
    non_zero_positions = [i for i, tile in enumerate(board) if tile != 0]

    # Check if all non-zero tiles are in rightmost column
    if all(pos in rightmost_positions for pos in non_zero_positions):
        return 1.0, f"All tiles successfully moved to rightmost column at positions {non_zero_positions}."

    # Find which tiles are not in the rightmost column
    misplaced = [pos for pos in non_zero_positions if pos not in rightmost_positions]
    return 0.0, f"Some tiles are not in rightmost column. Misplaced at positions: {misplaced}"


def _validate_get_32_tile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 32 tile is present on the board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    if 32 in final_state["board"]:
        return 1.0, "A 32 tile is present."
    return 0.0, "No 32 tile is present."


def _validate_get_128_tile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 128 tile is present on the board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    if 128 in final_state["board"]:
        return 1.0, "A 128 tile is present."
    return 0.0, "No 128 tile is present."


def _validate_get_256_tile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 256 tile is present on the board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    if 256 in final_state["board"]:
        return 1.0, "A 256 tile is present."
    return 0.0, "No 256 tile is present."


def _validate_get_512_tile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 512 tile is present on the board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    if 512 in final_state["board"]:
        return 1.0, "A 512 tile is present."
    return 0.0, "No 512 tile is present."


def _validate_create_two_high_tiles(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that at least two tiles with value 128 or higher are present."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    high_tiles = [tile for tile in final_state["board"] if tile >= 128]
    count = len(high_tiles)

    if count >= 2:
        return 1.0, f"Board contains {count} tiles with value 128 or higher: {high_tiles}."

    return 0.0, f"Board contains only {count} tile(s) with value 128 or higher. Need at least 2."


def _validate_reach_540_sum(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the sum of all tile values is 540 or greater."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    total_sum = sum(final_state["board"])

    if total_sum >= 540:
        return 1.0, f"Board sum is {total_sum}, which meets the requirement of 540 or greater."

    return 0.0, f"Board sum is {total_sum}, which is below the required 540."


def _validate_strategic_32(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a 32 tile was created strategically from an empty board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    if 32 in final_state["board"]:
        return 1.0, "A 32 tile was successfully created from empty board."
    return 0.0, "No 32 tile is present."


# Registry of all 2048 reward functions
REWARD_FUNCTIONS_2048 = {
    "_validate_get_2048": _validate_get_2048,
    "_validate_2048_make_first_move": _validate_2048_make_first_move,
    "_validate_move_tiles_right": _validate_move_tiles_right,
    "_validate_get_32_tile": _validate_get_32_tile,
    "_validate_get_128_tile": _validate_get_128_tile,
    "_validate_get_256_tile": _validate_get_256_tile,
    "_validate_get_512_tile": _validate_get_512_tile,
    "_validate_create_two_high_tiles": _validate_create_two_high_tiles,
    "_validate_reach_540_sum": _validate_reach_540_sum,
    "_validate_strategic_32": _validate_strategic_32,
}

"""
Reward functions for tic-tac-toe game tasks.

Board is a 9-element array representing a 3x3 grid:
  [0, 1, 2,
   3, 4, 5,
   6, 7, 8]

Players: "X" (human), "O" (computer), or null (empty)
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_tic_tac_toe_make_first_move(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a move was made on previously empty board."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]

    # Check if board has any non-null values
    if all(cell is None for cell in board):
        return 0.0, "Board is still empty - no move was made."

    # Check if board has at least one X
    if "X" in board:
        return 1.0, "First move made successfully - X placed on board."

    return 0.0, "No X found on board."


def _validate_take_center(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that X was placed in center position (index 4)."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]

    # Check if center position (index 4) contains X
    if board[4] == "X":
        return 1.0, "Center square successfully taken by X."

    center_value = board[4] if board[4] is not None else "empty"
    return 0.0, f"Center square not taken by X. Center is: {center_value}"


def _validate_block_computer_win(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that X blocked computer's win at position 2."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]

    # Check if position 2 (top-right) contains X
    if board[2] != "X":
        position_value = board[2] if board[2] is not None else "empty"
        return 0.0, f"Position 2 not blocked by X. Position 2 is: {position_value}"

    # Check that game is still ongoing (player hasn't lost)
    winner = final_state.get("winner")
    if winner == "O":
        return 0.0, "Computer (O) won - blocking was unsuccessful."

    return 1.0, "Successfully blocked computer's winning move at position 2."


# Registry of all tic-tac-toe reward functions
REWARD_FUNCTIONS_TIC_TAC_TOE = {
    "_validate_tic_tac_toe_make_first_move": _validate_tic_tac_toe_make_first_move,
    "_validate_take_center": _validate_take_center,
    "_validate_block_computer_win": _validate_block_computer_win,
}

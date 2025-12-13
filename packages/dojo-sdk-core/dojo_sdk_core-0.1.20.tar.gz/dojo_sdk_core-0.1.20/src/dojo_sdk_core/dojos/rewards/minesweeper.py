"""
Reward functions for Minesweeper game tasks.

Board is a 9x9 grid (2D array) of Cell objects:
  Cell: {
    isMine: boolean,
    isRevealed: boolean,
    isFlagged: boolean,
    neighborMineCount: number
  }

Game statuses: "not_started", "playing", "won", "lost"
"""

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


# Helper functions for common validation patterns


def _check_cells_flagged(board: List[List[Dict[str, Any]]], positions: List[Tuple[int, int]]) -> Tuple[float, str]:
    """
    Helper function to check if specific cells are flagged.

    Args:
        board: The game board (2D array)
        positions: List of (row, col) tuples to check

    Returns:
        (1.0, success_message) if all positions are flagged
        (0.0, error_message) otherwise
    """
    flagged = []
    unflagged = []

    for row, col in positions:
        # Check if position exists
        if row >= len(board) or col >= len(board[row]):
            return 0.0, f"Position [{row}][{col}] does not exist on board"

        if board[row][col].get("isFlagged"):
            flagged.append(f"[{row}][{col}]")
        else:
            unflagged.append(f"[{row}][{col}]")

    if len(flagged) == len(positions):
        cells_str = ", ".join(flagged)
        return 1.0, f"All {len(positions)} cell(s) flagged successfully: {cells_str}."

    return 0.0, f"Not all cells flagged. Flagged: {flagged}, Not flagged: {unflagged}"


def _check_cells_revealed(board: List[List[Dict[str, Any]]], min_count: int, check_for_mines: bool = True) -> Tuple[float, str]:
    """
    Helper function to check if minimum number of cells are revealed.

    Args:
        board: The game board (2D array)
        min_count: Minimum number of cells that should be revealed
        check_for_mines: If True, fail if any revealed cell is a mine

    Returns:
        (1.0, success_message) if criteria met
        (0.0, error_message) otherwise
    """
    revealed_count = 0
    revealed_mine = False

    for row in board:
        for cell in row:
            if cell.get("isRevealed"):
                revealed_count += 1
                if check_for_mines and cell.get("isMine"):
                    revealed_mine = True

    if check_for_mines and revealed_mine:
        return 0.0, "A mine was revealed - task failed"

    if revealed_count >= min_count:
        return 1.0, f"Successfully revealed {revealed_count} safe cells (target: {min_count}+)."

    return 0.0, f"Only {revealed_count} cells revealed, need at least {min_count}"


# Task-specific validation functions


def _validate_minesweeper_reveal_first_cell(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that first move was made - at least one cell revealed and game is playing."""
    if "gameStatus" not in final_state:
        return 0.0, "No gameStatus in final state"

    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    # Check if game status changed to playing
    if final_state["gameStatus"] != "playing":
        return 0.0, f"Game status is '{final_state['gameStatus']}', expected 'playing'"

    # Check if at least one cell is revealed
    board = final_state["board"]
    revealed_count = 0

    for row in board:
        for cell in row:
            if cell.get("isRevealed"):
                revealed_count += 1

    if revealed_count > 0:
        return 1.0, f"First move successful - {revealed_count} cell(s) revealed and game is playing."

    return 0.0, "No cells revealed yet."


def _validate_minesweeper_reveal_numbered_cell(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a numbered cell (with neighborMineCount > 0) was revealed at position [1][1]."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]

    # Check if position [1][1] exists
    if len(board) < 2 or len(board[1]) < 2:
        return 0.0, "Board does not have position [1][1]"

    target_cell = board[1][1]

    # Check if cell is revealed
    if not target_cell.get("isRevealed"):
        return 0.0, "Cell at [1][1] is not revealed"

    # Check if cell shows a number (neighborMineCount > 0)
    neighbor_count = target_cell.get("neighborMineCount", 0)

    if neighbor_count > 0:
        return 1.0, f"Cell at [1][1] revealed successfully showing {neighbor_count} neighboring mine(s)."

    return 0.0, f"Cell at [1][1] has neighborMineCount of {neighbor_count}, expected > 0"


def _validate_minesweeper_reveal_10_cells(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that at least 10 cells are revealed, none are mines, and game is still playing."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    if "gameStatus" not in final_state:
        return 0.0, "No gameStatus in final state"

    logger.debug(f"running reward function on state: {final_state}")

    # Check if game is still playing
    if final_state["gameStatus"] != "playing":
        return 0.0, f"Game status is '{final_state['gameStatus']}', expected 'playing'"

    return _check_cells_revealed(final_state["board"], 10, check_for_mines=True)


def _validate_minesweeper_reveal_20_cells(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that at least 20 cells are revealed and game is still playing."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    if "gameStatus" not in final_state:
        return 0.0, "No gameStatus in final state"

    logger.debug(f"running reward function on state: {final_state}")

    # Check if game is still playing
    if final_state["gameStatus"] != "playing":
        return 0.0, f"Game status is '{final_state['gameStatus']}', expected 'playing' (game should not be won or lost yet)"

    return _check_cells_revealed(final_state["board"], 20, check_for_mines=True)


def _validate_minesweeper_flag_single_mine(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that cell at position [0][0] is flagged."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    return _check_cells_flagged(final_state["board"], [(0, 0)])


def _validate_minesweeper_flag_three_mines(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that cells at [0][0], [0][8], and [8][0] are all flagged."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    target_positions = [(0, 0), (0, 8), (8, 0)]
    return _check_cells_flagged(final_state["board"], target_positions)


def _validate_minesweeper_flag_corner_mines(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that all four corner cells [0][0], [0][8], [8][0], [8][8] are flagged."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    corner_positions = [(0, 0), (0, 8), (8, 0), (8, 8)]
    return _check_cells_flagged(final_state["board"], corner_positions)


def _validate_minesweeper_reveal_safe_cell(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that cell at position [4][4] is revealed and has 0 neighboring mines."""
    if "board" not in final_state:
        return 0.0, "No board in final state"

    logger.debug(f"running reward function on state: {final_state}")

    board = final_state["board"]

    # Check if position [4][4] exists
    if len(board) < 5 or len(board[4]) < 5:
        return 0.0, "Board does not have position [4][4]"

    target_cell = board[4][4]

    # Check if cell is revealed
    if not target_cell.get("isRevealed"):
        return 0.0, "Cell at [4][4] is not revealed"

    # Check if it's not a mine
    if target_cell.get("isMine"):
        return 0.0, "Cell at [4][4] is a mine - task failed!"

    # Check if it has 0 neighboring mines
    neighbor_count = target_cell.get("neighborMineCount", -1)
    if neighbor_count == 0:
        return 1.0, "Cell at [4][4] revealed successfully with 0 neighboring mines."

    return 0.0, f"Cell at [4][4] has {neighbor_count} neighboring mines, expected 0"


# Registry of all minesweeper reward functions
REWARD_FUNCTIONS_MINESWEEPER = {
    "_validate_minesweeper_reveal_first_cell": _validate_minesweeper_reveal_first_cell,
    "_validate_minesweeper_reveal_numbered_cell": _validate_minesweeper_reveal_numbered_cell,
    "_validate_minesweeper_reveal_10_cells": _validate_minesweeper_reveal_10_cells,
    "_validate_minesweeper_reveal_20_cells": _validate_minesweeper_reveal_20_cells,
    "_validate_minesweeper_flag_single_mine": _validate_minesweeper_flag_single_mine,
    "_validate_minesweeper_flag_three_mines": _validate_minesweeper_flag_three_mines,
    "_validate_minesweeper_flag_corner_mines": _validate_minesweeper_flag_corner_mines,
    "_validate_minesweeper_reveal_safe_cell": _validate_minesweeper_reveal_safe_cell,
}

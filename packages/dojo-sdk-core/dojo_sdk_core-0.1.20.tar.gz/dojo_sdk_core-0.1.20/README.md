# Dojo SDK Core

Core models and types for the Dojo RL environment framework. **Not intended for standalone use by end users.**

## Overview

`dojo-sdk-core` provides the core components shared across the Dojo ecosystem:

- **Action Types** - Standardized action models for computer use (click, type, scroll, etc.)
- **Reward Functions** - Reward functions for dojos that need custom validation
- **Shared Types** - Common data structures for tasks, scores, and configurations
- **Settings** - Loading of environment variables used by the Dojo SDK
- **Task Loaders** - Loading of tasks from local files or remote datasets

## Installation

```bash
uv add dojo-sdk-core
```

## Key Components

### Action Types

Set of computer-use actions:
`KEY`, `CLICK`, `RIGHT_CLICK`, `DOUBLE_CLICK`, `MIDDLE_CLICK`, `DRAG`, `MOVE_TO`, `PRESS`, `HOTKEY`, `SCROLL`, `TYPE`, `DONE`, `WAIT`

### Reward Functions

Reward functions provide custom validation logic for tasks that cannot be completed by simple state comparison. Each reward function follows a standard signature:

```python
def reward_function(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Args:
        initial_state: The state before any actions were executed
        final_state: Current state of the environment

    Returns:
        Tuple of (score, reason) where:
        - score: float between 0.0 and 1.0 where environment is considered completed if score is 1.0
        - reason: human readable string explaining the validation result
    """
```

**Available reward functions:**

- `_validate_get_2048`: Checks if a 2048 tile is present on the game board
- `_validate_search_for_dzaka`: Validates successful search for a specific user in LinkedIn
- `_validate_drag_to_different_column`: Validates issue movement to a different column in Linear
- `_validate_drag_two_issues_same_user`: Validates multiple issues moved within same user's board

## Documentation

Visit [docs.trydojo.ai](https://docs.trydojo.ai) for complete documentation.

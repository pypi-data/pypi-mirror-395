"""
Reward functions for LinkedIn app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_search_for_dzaka(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the user successfully searched for Dzaka Athif."""
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "search"
    if final_state.get("currentView") != "search":
        return 0.0, f"Not on search page, current view: {final_state.get('currentView')}"

    # Check 2: searchQuery contains "dzaka" (case insensitive)
    query = final_state.get("searchQuery", "").lower()
    if "dzaka" not in query:
        return 0.0, f"Search query doesn't contain 'dzaka': {final_state.get('searchQuery')}"

    # Check 3: Dzaka Athif in search results
    search_results = final_state.get("searchResults", {})
    people = search_results.get("allPeople", [])

    dzaka_found = any(user.get("name") == "Dzaka Athif" for user in people)

    if dzaka_found:
        return 1.0, "Successfully searched for Dzaka Athif"

    return 0.0, f"Dzaka Athif not found in search results. Found {len(people)} people."


def _validate_fractional_find_user_profile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate LinkedIn profile navigation with fractional scoring.

    Awards 0.33 points for each criterion met:
    - currentView is 'profile'
    - viewedUserId is '2' (John Smith)
    - searchQuery contains 'john smith'
    """
    logger.debug(f"Running reward function on state: {final_state}")

    score = 0.0
    passed = []
    failed = []

    # Check 1: currentView is 'profile' (0.33 points)
    if final_state.get("currentView") == "profile":
        score += 0.33
        passed.append("currentView='profile'")
    else:
        failed.append(f"currentView='{final_state.get('currentView')}' (expected 'profile')")

    # Check 2: viewedUserId is '2' (0.33 points)
    if final_state.get("viewedUserId") == "2":
        score += 0.33
        passed.append("viewedUserId='2'")
    else:
        failed.append(f"viewedUserId='{final_state.get('viewedUserId')}' (expected '2')")

    # Check 3: searchQuery contains 'john smith' (0.33 points)
    query = final_state.get("searchQuery", "").lower()
    if "john smith" in query:
        score += 0.34  # Make it add up to 1.0
        passed.append("searchQuery contains 'john smith'")
    else:
        failed.append(f"searchQuery='{final_state.get('searchQuery')}' (expected to contain 'john smith')")

    # Build reason string
    reason_parts = []
    if passed:
        reason_parts.append(f"Passed: {', '.join(passed)}")
    if failed:
        reason_parts.append(f"Failed: {', '.join(failed)}")

    reason = "; ".join(reason_parts) if reason_parts else "No criteria evaluated"

    return round(score, 2), reason


# Registry of all LinkedIn reward functions
REWARD_FUNCTIONS_LINKEDIN = {
    "_validate_search_for_dzaka": _validate_search_for_dzaka,
    "_validate_fractional_find_user_profile": _validate_fractional_find_user_profile,
}

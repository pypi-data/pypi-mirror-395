"""
Reward functions for Weibo SPA tasks - V2 Architecture.

This version includes both frontend and backend validation with bundled reward functions.
Each task exports a bundle containing:
  - state_key: Dict defining backend queries (collection + filter)
  - validate_backend: Function (state_key, final_state) -> (float, str)
  - validate_frontend: Function (initial_state, final_state) -> (float, str)
"""

import logging
import re
from typing import Any, Callable, Dict, Optional, Tuple, TypedDict

logger = logging.getLogger(__name__)


# =============================================================================
# Type Definitions
# =============================================================================


class StateKeyQuery(TypedDict):
    collection: str
    filter: Dict[str, Any]


StateKey = Dict[str, StateKeyQuery]
ValidatorFunc = Callable[[Dict[str, Any], Dict[str, Any]], Tuple[float, str]]


class ValidateTask(TypedDict):
    state_key: StateKey
    validate_backend: ValidatorFunc
    validate_frontend: ValidatorFunc


# =============================================================================
# Helper Functions - Frontend State
# =============================================================================


def _check_current_view(final_state: Dict[str, Any], expected_view: str) -> Tuple[bool, str]:
    """Check if the current view matches the expected view."""
    view = final_state.get("currentView")
    if view != expected_view:
        return False, f"currentView='{view}' expected '{expected_view}'"
    return True, ""


def _check_theme(final_state: Dict[str, Any], expected_theme: str) -> Tuple[bool, str]:
    """Check if the theme matches the expected theme."""
    theme = final_state.get("theme")
    if theme != expected_theme:
        return False, f"theme='{theme}' expected '{expected_theme}'"
    return True, ""


def _check_viewed_user_id(final_state: Dict[str, Any], expected_id: str) -> Tuple[bool, str]:
    """Check if the viewed user ID matches."""
    viewed_id = final_state.get("viewedUserId")
    if viewed_id != expected_id:
        return False, f"viewedUserId='{viewed_id}' expected '{expected_id}'"
    return True, ""


def _check_viewed_post_id(final_state: Dict[str, Any], expected_id: str) -> Tuple[bool, str]:
    """Check if the viewed post ID matches."""
    viewed_id = final_state.get("viewedPostId")
    if viewed_id != expected_id:
        return False, f"viewedPostId='{viewed_id}' expected '{expected_id}'"
    return True, ""


def _check_search_category(final_state: Dict[str, Any], expected_category: str) -> Tuple[bool, str]:
    """Check if the search category matches."""
    category = final_state.get("searchCategory")
    if category != expected_category:
        return False, f"searchCategory='{category}' expected '{expected_category}'"
    return True, ""


def _check_search_query_equals(final_state: Dict[str, Any], expected_query: str) -> Tuple[bool, str]:
    """Check if the search query equals the expected value."""
    search_query = final_state.get("searchQuery", "")
    if search_query != expected_query:
        return False, f"searchQuery='{search_query}' expected '{expected_query}'"
    return True, ""


def _check_search_dropdown_open(final_state: Dict[str, Any], expected_open: bool) -> Tuple[bool, str]:
    """Check if the search dropdown is open."""
    dropdown_open = final_state.get("searchDropdownOpen", False)
    if dropdown_open != expected_open:
        return False, f"searchDropdownOpen={dropdown_open} expected {expected_open}"
    return True, ""


def _check_search_dropdown_results_empty(final_state: Dict[str, Any]) -> Tuple[bool, str]:
    """Check if the search dropdown results are empty."""
    results = final_state.get("searchDropdownResults", {})
    suggestions = results.get("suggestions", [])
    users = results.get("users", [])
    if suggestions or users:
        return False, f"searchDropdownResults should be empty. suggestions={len(suggestions)}, users={len(users)}"
    return True, ""


def _check_search_dropdown_has_suggestions(final_state: Dict[str, Any], min_count: int = 1) -> Tuple[bool, str]:
    """Check if the search dropdown has suggestions."""
    results = final_state.get("searchDropdownResults", {})
    suggestions = results.get("suggestions", [])
    if len(suggestions) < min_count:
        return False, f"Expected at least {min_count} suggestion(s), got {len(suggestions)}"
    return True, ""


def _check_more_options_dropdown_open(final_state: Dict[str, Any], expected_open: bool) -> Tuple[bool, str]:
    """Check if the more options dropdown is open."""
    dropdown_open = final_state.get("moreOptionsDropdownOpen", False)
    if dropdown_open != expected_open:
        return False, f"moreOptionsDropdownOpen={dropdown_open} expected {expected_open}"
    return True, ""


def _check_feed_post_comments_open(final_state: Dict[str, Any], post_id: str) -> Tuple[bool, str]:
    """Check if a post's inline comments section is open in the feed."""
    displayed_posts = final_state.get("feedDisplayedPosts", [])
    for post in displayed_posts:
        if post.get("_id") == post_id:
            if post.get("isCommentsOpen") is True:
                return True, ""
            return False, f"Post '{post_id}' has isCommentsOpen={post.get('isCommentsOpen')}"
    return False, f"Post '{post_id}' not found in feedDisplayedPosts"


def _check_local_post_like_override(final_state: Dict[str, Any], post_id: str, expected_liked: bool) -> Tuple[bool, str]:
    """Check if the post like override matches the expected state."""
    overrides = final_state.get("localPostLikeOverrides", {})
    post_override = overrides.get(post_id)
    if post_override is None:
        return False, f"Post '{post_id}' not in localPostLikeOverrides"
    is_liked = post_override.get("isLiked")
    if is_liked != expected_liked:
        return False, f"Post '{post_id}' isLiked={is_liked} expected {expected_liked}"
    return True, ""


# =============================================================================
# Helper Functions - Backend State
# =============================================================================


def _check_user_followed(final_state: Dict[str, Any], user_id: str) -> Tuple[bool, str]:
    """Check if a user is followed."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        return False, "userFollows array missing in backend final state"
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            return True, ""
    return False, f"User '{user_id}' not found in userFollows"


def _check_user_not_followed(final_state: Dict[str, Any], user_id: str) -> Tuple[bool, str]:
    """Check if a user is NOT followed."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        # If userFollows doesn't exist, the user is not followed
        return True, ""
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            return False, f"User '{user_id}' should not be in userFollows"
    return True, ""


def _check_user_in_group(final_state: Dict[str, Any], user_id: str, group_id: str) -> Tuple[bool, str]:
    """Check if a user is in a specific group."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        return False, "userFollows array missing in backend final state"
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            groups = entry.get("groups", [])
            if group_id in groups:
                return True, ""
            return False, f"User '{user_id}' not in group '{group_id}'. Groups: {groups}"
    return False, f"User '{user_id}' not found in userFollows"


def _check_user_not_in_group(final_state: Dict[str, Any], user_id: str, group_id: str) -> Tuple[bool, str]:
    """Check if a user is NOT in a specific group."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        return True, ""  # If no followed users, user is not in group
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            groups = entry.get("groups", [])
            if group_id in groups:
                return False, f"User '{user_id}' should not be in group '{group_id}'"
            return True, ""
    return True, ""


def _check_user_no_special_attention(final_state: Dict[str, Any], user_id: str) -> Tuple[bool, str]:
    """Check if a user does NOT have special attention status."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        return True, ""  # If no followed users, user has no special attention
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            is_special = entry.get("isSpecialAttention", False)
            if is_special:
                return False, f"User '{user_id}' should not have special attention"
            return True, ""
    return True, ""


def _check_user_has_no_groups(final_state: Dict[str, Any], user_id: str) -> Tuple[bool, str]:
    """Check if a user has no groups assigned."""
    followed = final_state.get("userFollows")
    if not isinstance(followed, list):
        return True, ""
    for entry in followed:
        if entry.get("followedUserId") == user_id:
            groups = entry.get("groups", [])
            if groups and len(groups) > 0:
                return False, f"User '{user_id}' should have no groups. Has: {groups}"
            return True, ""
    return True, ""


def _find_post_by_author_backend(final_state: Dict[str, Any], author_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Find a post by author ID in backend state."""
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return None, "Posts array missing in backend final state"
    for post in posts:
        if post.get("user", {}).get("_id") == author_id:
            return post, ""
    return None, f"Post with authorId '{author_id}' not found in backend final state"


# =============================================================================
# NAVIGATION & SEARCH TASKS (Frontend-only)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: profile-from-search-v2
# -----------------------------------------------------------------------------


def _validate_backend_profile_from_search(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_profile_from_search(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    # Check that we're viewing a user's profile
    viewed_user_id = final_state.get("viewedUserId")
    if not viewed_user_id:
        return 0.0, "viewedUserId is missing or null"

    return 1.0, f"Successfully navigated to profile from search (user: {viewed_user_id})"


_validate_profile_from_search: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_profile_from_search,
    "validate_frontend": _validate_frontend_profile_from_search,
}


# -----------------------------------------------------------------------------
# Task: search-users-v2
# -----------------------------------------------------------------------------


def _validate_backend_search_users(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_search_users(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "users")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to search users page"


_validate_search_users: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_users,
    "validate_frontend": _validate_frontend_search_users,
}


# -----------------------------------------------------------------------------
# Task: switch-theme-v2
# -----------------------------------------------------------------------------


def _validate_backend_switch_theme(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for theme change"


def _validate_frontend_switch_theme(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_theme(final_state, "dark")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully switched to dark theme"


_validate_switch_theme: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_switch_theme,
    "validate_frontend": _validate_frontend_switch_theme,
}


# -----------------------------------------------------------------------------
# Task: search-dropdown-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_search_dropdown_profile(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_search_dropdown_profile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user13")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to user profile via search dropdown"


_validate_search_dropdown_profile: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_search_dropdown_profile,
    "validate_frontend": _validate_frontend_search_dropdown_profile,
}


# -----------------------------------------------------------------------------
# Task: profile-from-sorted-comments-v2
# -----------------------------------------------------------------------------


def _validate_backend_profile_from_sorted_comments(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_profile_from_sorted_comments(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user13")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to profile from sorted comments"


_validate_profile_from_sorted_comments: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_profile_from_sorted_comments,
    "validate_frontend": _validate_frontend_profile_from_sorted_comments,
}


# -----------------------------------------------------------------------------
# Task: view-full-comment-thread-v2
# -----------------------------------------------------------------------------


def _validate_backend_view_full_comment_thread(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for viewing comments"


def _validate_frontend_view_full_comment_thread(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "5")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully viewing full comment thread on post 5"


_validate_view_full_comment_thread: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_view_full_comment_thread,
    "validate_frontend": _validate_frontend_view_full_comment_thread,
}


# -----------------------------------------------------------------------------
# Task: video-post-from-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_video_post_from_profile(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for viewing post"


def _validate_frontend_video_post_from_profile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "23")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to video post from profile"


_validate_video_post_from_profile: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_video_post_from_profile,
    "validate_frontend": _validate_frontend_video_post_from_profile,
}


# -----------------------------------------------------------------------------
# Task: refresh-list-of-trending-topics-v2
# -----------------------------------------------------------------------------


def _validate_backend_refresh_list_of_trending_topics(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # hotSearch is frontend-only state
    return 1.0, "No backend validation required for trending topics refresh"


def _validate_frontend_refresh_list_of_trending_topics(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # mineTrendingTopics is stored in React context state, not Dojo state
    # So we can only validate that the user is still on the feed view
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully refreshed trending topics"


_validate_refresh_list_of_trending_topics: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_refresh_list_of_trending_topics,
    "validate_frontend": _validate_frontend_refresh_list_of_trending_topics,
}


# -----------------------------------------------------------------------------
# Task: refresh-list-of-suggested-users-v2
# -----------------------------------------------------------------------------


def _validate_backend_refresh_list_of_suggested_users(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Backend state doesn't change for suggested users refresh
    # The refresh is a frontend re-query of the same backend data
    suggested = final_state.get("suggestedUsers")
    if not isinstance(suggested, list):
        return 0.0, "suggestedUsers array missing in backend final state"

    if len(suggested) == 0:
        return 0.0, "suggestedUsers array is empty"

    return 1.0, "Backend: Suggested users data exists"


def _validate_frontend_refresh_list_of_suggested_users(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Suggested users are backend-only data queried on-demand by components
    # There's no frontend state that tracks which users are currently displayed
    # So we can only validate that the user is still on the feed view
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully refreshed suggested users"


_validate_refresh_list_of_suggested_users: ValidateTask = {
    "state_key": {
        "suggestedUsers": {"collection": "suggestedUsers", "filter": {}},
    },
    "validate_backend": _validate_backend_refresh_list_of_suggested_users,
    "validate_frontend": _validate_frontend_refresh_list_of_suggested_users,
}


# =============================================================================
# LIKE/UNLIKE TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: unlike-single-post-from-feed-v2
# -----------------------------------------------------------------------------


def _validate_backend_unlike_single_post_from_feed(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that post 1 has isLiked=false
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("_id") == "1":
            if post.get("isLiked") is False:
                return 1.0, "Backend: Post unliked successfully"
            else:
                return 0.0, "Post 1 is still liked in backend"

    return 0.0, "Post 1 not found in backend"


def _validate_frontend_unlike_single_post_from_feed(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_local_post_like_override(final_state, "1", False)
    if not ok:
        return 0.0, error
    return 1.0, "Successfully unliked post from feed"


_validate_unlike_single_post_from_feed: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {"_id": "1"}},
    },
    "validate_backend": _validate_backend_unlike_single_post_from_feed,
    "validate_frontend": _validate_frontend_unlike_single_post_from_feed,
}


# -----------------------------------------------------------------------------
# Task: unlike-all-posts-on-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_unlike_all_posts_on_profile(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that all the current user's posts have isLiked=false
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    # Profile post IDs for current user (8200663693)
    profile_post_ids = [
        "1",
        "16",
        "31",
        "trending-1-2",
        "trending-7-2",
        "trending-9-3",
        "trending-13-2",
        "trending-17-3",
        "trending-18-2",
        "nt-1",
        "nt-16",
        "nt-31",
        "dot-1",
    ]

    for post in posts:
        if post.get("_id") in profile_post_ids:
            if post.get("isLiked") is True:
                return 0.0, f"Post '{post.get('_id')}' is still liked in backend"

    return 1.0, "Backend: All profile posts unliked successfully"


def _validate_frontend_unlike_all_posts_on_profile(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check localPostLikeOverrides - all posts should be unliked
    overrides = final_state.get("localPostLikeOverrides", {})

    # All overrides should have isLiked=False
    for post_id, override in overrides.items():
        if override.get("isLiked") is True:
            return 0.0, f"Post '{post_id}' should be unliked"

    return 1.0, "Successfully unliked all posts on profile"


_validate_unlike_all_posts_on_profile: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {"user._id": "8200663693"}},
    },
    "validate_backend": _validate_backend_unlike_all_posts_on_profile,
    "validate_frontend": _validate_frontend_unlike_all_posts_on_profile,
}


# =============================================================================
# FOLLOW/UNFOLLOW TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: unfollow-user-from-profile-page-v2
# -----------------------------------------------------------------------------


def _validate_backend_unfollow_user_from_profile_page(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_user_not_followed(final_state, "user5")
    if not ok:
        return 0.0, error
    return 1.0, "Backend: User unfollowed successfully"


def _validate_frontend_unfollow_user_from_profile_page(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user5")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully unfollowed user from profile page"


_validate_unfollow_user_from_profile_page: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_unfollow_user_from_profile_page,
    "validate_frontend": _validate_frontend_unfollow_user_from_profile_page,
}


# -----------------------------------------------------------------------------
# Task: search-follow-last-user-v2
# -----------------------------------------------------------------------------


def _validate_backend_search_follow_last_user(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that user "8200663693" (当前用户) is followed in userFollows
    user_follows = final_state.get("userFollows")
    if not isinstance(user_follows, list):
        return 0.0, "userFollows array missing in backend final state"

    # Check if the target user (8200663693) was followed
    target_user_id = "8200663693"
    for entry in user_follows:
        if entry.get("followedUserId") == target_user_id:
            return 1.0, f"Backend: User {target_user_id} successfully followed"

    return 0.0, f"User {target_user_id} not found in userFollows"


def _validate_frontend_search_follow_last_user(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "users")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully searched and followed last user"


_validate_search_follow_last_user: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_search_follow_last_user,
    "validate_frontend": _validate_frontend_search_follow_last_user,
}


# =============================================================================
# GROUP MANAGEMENT TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: remove-user-from-single-group-v2
# -----------------------------------------------------------------------------


def _validate_backend_remove_user_from_single_group(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 is NOT in "classmates" group anymore
    ok, error = _check_user_not_in_group(final_state, "user1", "classmates")
    if not ok:
        return 0.0, error

    # Check that user1 is still in "celebrities" group
    ok, error = _check_user_in_group(final_state, "user1", "celebrities")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: User removed from classmates group successfully"


def _validate_frontend_remove_user_from_single_group(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully removed user from single group"


_validate_remove_user_from_single_group: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_remove_user_from_single_group,
    "validate_frontend": _validate_frontend_remove_user_from_single_group,
}


# -----------------------------------------------------------------------------
# Task: reassign-user-to-different-group-v2
# -----------------------------------------------------------------------------


def _validate_backend_reassign_user_to_different_group(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 is NOT in "classmates" group anymore
    ok, error = _check_user_not_in_group(final_state, "user1", "classmates")
    if not ok:
        return 0.0, error

    # Check that user1 is now in "colleagues" group
    ok, error = _check_user_in_group(final_state, "user1", "colleagues")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: User reassigned from classmates to colleagues successfully"


def _validate_frontend_reassign_user_to_different_group(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully reassigned user to different group"


_validate_reassign_user_to_different_group: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_reassign_user_to_different_group,
    "validate_frontend": _validate_frontend_reassign_user_to_different_group,
}


# -----------------------------------------------------------------------------
# Task: unassign-special-attention-and-groups-v2
# -----------------------------------------------------------------------------


def _validate_backend_unassign_special_attention_and_groups(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 has no groups assigned
    ok, error = _check_user_has_no_groups(final_state, "user1")
    if not ok:
        return 0.0, error

    # Check that user1 has no special attention
    ok, error = _check_user_no_special_attention(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: All groups and special attention removed successfully"


def _validate_frontend_unassign_special_attention_and_groups(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully unassigned special attention and groups"


_validate_unassign_special_attention_and_groups: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_unassign_special_attention_and_groups,
    "validate_frontend": _validate_frontend_unassign_special_attention_and_groups,
}


# =============================================================================
# COMMENT TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: reply-to-comment-v2
# -----------------------------------------------------------------------------


def _validate_backend_reply_to_comment(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that a new reply was created on post 1
    replies = final_state.get("replies")
    if not isinstance(replies, list):
        return 0.0, "Replies array missing in backend final state"

    # Look for a new reply from current user on post 1
    for reply in replies:
        if reply.get("postId") == "1" and reply.get("user", {}).get("_id") == "8200663693":
            return 1.0, "Backend: Reply created successfully"

    return 0.0, "No new reply from current user found on post 1"


def _validate_frontend_reply_to_comment(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that comment section is open
    displayed_posts = final_state.get("feedDisplayedPosts", [])
    for post in displayed_posts:
        if post.get("_id") == "1":
            if post.get("isCommentsOpen") is True:
                return 1.0, "Successfully opened comments and replied"

    return 1.0, "Reply submitted (UI state may not track replies)"


_validate_reply_to_comment: ValidateTask = {
    "state_key": {
        "replies": {"collection": "replies", "filter": {"postId": "1"}},
    },
    "validate_backend": _validate_backend_reply_to_comment,
    "validate_frontend": _validate_frontend_reply_to_comment,
}


# =============================================================================
# ADDITIONAL NAVIGATION TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: navigate-to-latest-feed-section-v2
# -----------------------------------------------------------------------------


def _validate_backend_navigate_to_latest_feed_section(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_to_latest_feed_section(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "latest")
    if not ok:
        return 0.0, error
    return 1.0, "Successfully navigated to latest feed section"


_validate_navigate_to_latest_feed_section: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_to_latest_feed_section,
    "validate_frontend": _validate_frontend_navigate_to_latest_feed_section,
}


# -----------------------------------------------------------------------------
# Task: navigate-via-trending-topic-v2
# -----------------------------------------------------------------------------


def _validate_backend_navigate_via_trending_topic(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_via_trending_topic(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "comprehensive")
    if not ok:
        return 0.0, error

    # Search query should be set to the trending topic
    search_query = final_state.get("searchQuery", "")
    if not search_query:
        return 0.0, "searchQuery is empty"

    return 1.0, f"Successfully navigated via trending topic: {search_query}"


_validate_navigate_via_trending_topic: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_via_trending_topic,
    "validate_frontend": _validate_frontend_navigate_via_trending_topic,
}


# -----------------------------------------------------------------------------
# Task: no-search-suggestions-v2
# -----------------------------------------------------------------------------


def _validate_backend_no_search_suggestions(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_no_search_suggestions(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_search_query_equals(final_state, "asdf")
    if not ok:
        return 0.0, error

    ok, error = _check_search_dropdown_open(final_state, True)
    if not ok:
        return 0.0, error

    ok, error = _check_search_dropdown_results_empty(final_state)
    if not ok:
        return 0.0, error

    return 1.0, "Search dropdown shows no suggestions for obscure query"


_validate_no_search_suggestions: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_no_search_suggestions,
    "validate_frontend": _validate_frontend_no_search_suggestions,
}


# -----------------------------------------------------------------------------
# Task: open-inline-comments-section-v2
# -----------------------------------------------------------------------------


def _validate_backend_open_inline_comments_section(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for opening comments"


def _validate_frontend_open_inline_comments_section(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    ok, error = _check_feed_post_comments_open(final_state, "1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully opened inline comments section"


_validate_open_inline_comments_section: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_open_inline_comments_section,
    "validate_frontend": _validate_frontend_open_inline_comments_section,
}


# -----------------------------------------------------------------------------
# Task: open-post-composer-more-dropdown-v2
# -----------------------------------------------------------------------------


def _validate_backend_open_post_composer_more_dropdown(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for opening dropdown"


def _validate_frontend_open_post_composer_more_dropdown(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    ok, error = _check_more_options_dropdown_open(final_state, True)
    if not ok:
        return 0.0, error

    return 1.0, "Successfully opened post composer more dropdown"


_validate_open_post_composer_more_dropdown: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_open_post_composer_more_dropdown,
    "validate_frontend": _validate_frontend_open_post_composer_more_dropdown,
}


# -----------------------------------------------------------------------------
# Task: partial-search-query-v2
# -----------------------------------------------------------------------------


def _validate_backend_partial_search_query(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_partial_search_query(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_search_query_equals(final_state, "电影")
    if not ok:
        return 0.0, error

    ok, error = _check_search_dropdown_open(final_state, True)
    if not ok:
        return 0.0, error

    ok, error = _check_search_dropdown_has_suggestions(final_state, 1)
    if not ok:
        return 0.0, error

    return 1.0, "Search dropdown shows suggestions for partial query"


_validate_partial_search_query: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_partial_search_query,
    "validate_frontend": _validate_frontend_partial_search_query,
}


# -----------------------------------------------------------------------------
# Task: post-and-view-hashtag-v2
# -----------------------------------------------------------------------------


def _validate_backend_post_and_view_hashtag(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that a new post with #weibo# hashtag was created
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            if "#weibo#" in content:
                return 1.0, "Backend: Post with #weibo# hashtag created"

    return 0.0, "No post with #weibo# hashtag found"


def _validate_frontend_post_and_view_hashtag(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_query_equals(final_state, "#weibo#")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "comprehensive")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully posted and navigated to hashtag view"


_validate_post_and_view_hashtag: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_post_and_view_hashtag,
    "validate_frontend": _validate_frontend_post_and_view_hashtag,
}


# -----------------------------------------------------------------------------
# Task: post-from-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_post_from_profile(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_post_from_profile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "dot-1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to post from profile"


_validate_post_from_profile: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_post_from_profile,
    "validate_frontend": _validate_frontend_post_from_profile,
}


# -----------------------------------------------------------------------------
# Task: post-from-search-v2
# -----------------------------------------------------------------------------


def _validate_backend_post_from_search(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_post_from_search(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "35")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to post from search"


_validate_post_from_search: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_post_from_search,
    "validate_frontend": _validate_frontend_post_from_search,
}


# -----------------------------------------------------------------------------
# Task: post-image-v2
# -----------------------------------------------------------------------------


def _validate_backend_post_image(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that a new post with image media was created
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            media = post.get("media", [])
            for m in media:
                if m.get("type") == "image":
                    return 1.0, "Backend: Post with image created"

    return 0.0, "No post with image media found"


def _validate_frontend_post_image(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully posted image"


_validate_post_image: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_post_image,
    "validate_frontend": _validate_frontend_post_image,
}


# -----------------------------------------------------------------------------
# Task: post-video-v2
# -----------------------------------------------------------------------------


def _validate_backend_post_video(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that a new post with video media was created
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            media = post.get("media", [])
            for m in media:
                if m.get("type") == "video":
                    return 1.0, "Backend: Post with video created"

    return 0.0, "No post with video media found"


def _validate_frontend_post_video(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully posted video"


_validate_post_video: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_post_video,
    "validate_frontend": _validate_frontend_post_video,
}


# -----------------------------------------------------------------------------
# Task: profile-from-comments-v2
# -----------------------------------------------------------------------------


def _validate_backend_profile_from_comments(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_profile_from_comments(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user9")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to profile from comments"


_validate_profile_from_comments: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_profile_from_comments,
    "validate_frontend": _validate_frontend_profile_from_comments,
}


# -----------------------------------------------------------------------------
# Task: profile-from-post-v2
# -----------------------------------------------------------------------------


def _validate_backend_profile_from_post(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_profile_from_post(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user5")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to profile from post"


_validate_profile_from_post: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_profile_from_post,
    "validate_frontend": _validate_frontend_profile_from_post,
}


# -----------------------------------------------------------------------------
# Task: profile-from-reply-v2
# -----------------------------------------------------------------------------


def _validate_backend_profile_from_reply(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_profile_from_reply(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user4")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to profile from reply"


_validate_profile_from_reply: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_profile_from_reply,
    "validate_frontend": _validate_frontend_profile_from_reply,
}


# =============================================================================
# CUSTOM GROUP MANAGEMENT TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: delete-custom-group-v2
# -----------------------------------------------------------------------------


def _validate_backend_delete_custom_group(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that the custom group 名人明星 is deleted
    custom_groups = final_state.get("customGroups")
    if not isinstance(custom_groups, list):
        return 0.0, "customGroups array missing in backend final state"

    for group in custom_groups:
        if group.get("label") == "名人明星" or group.get("_id") == "celebrities":
            return 0.0, "Custom group '名人明星' should have been deleted"

    return 1.0, "Backend: Custom group deleted successfully"


def _validate_frontend_delete_custom_group(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    # Check that manage groups modal is closed
    if final_state.get("manageGroupsModalOpen", False):
        return 0.0, "manageGroupsModalOpen should be false"

    return 1.0, "Successfully deleted custom group"


_validate_delete_custom_group: ValidateTask = {
    "state_key": {
        "customGroups": {"collection": "customGroups", "filter": {}},
    },
    "validate_backend": _validate_backend_delete_custom_group,
    "validate_frontend": _validate_frontend_delete_custom_group,
}


# -----------------------------------------------------------------------------
# Task: edit-custom-group-name-v2
# -----------------------------------------------------------------------------


def _validate_backend_edit_custom_group_name(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that the custom group was renamed
    custom_groups = final_state.get("customGroups")
    if not isinstance(custom_groups, list):
        return 0.0, "customGroups array missing in backend final state"

    # Look for the renamed group (should have the new label)
    for group in custom_groups:
        if group.get("label") == "新分组名":
            return 1.0, "Backend: Custom group renamed successfully"

    return 0.0, "Custom group with new name '新分组名' not found"


def _validate_frontend_edit_custom_group_name(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    # Check that manage groups modal is closed
    if final_state.get("manageGroupsModalOpen", False):
        return 0.0, "manageGroupsModalOpen should be false"

    return 1.0, "Successfully edited custom group name"


_validate_edit_custom_group_name: ValidateTask = {
    "state_key": {
        "customGroups": {"collection": "customGroups", "filter": {}},
    },
    "validate_backend": _validate_backend_edit_custom_group_name,
    "validate_frontend": _validate_frontend_edit_custom_group_name,
}


# =============================================================================
# FOLLOW FLOW TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: follow-and-set-special-attention-flow-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_and_set_special_attention_flow(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 (用户小王) is followed
    ok, error = _check_user_followed(final_state, "user1")
    if not ok:
        return 0.0, error

    # Check that user2 (科技资讯) is followed
    ok, error = _check_user_followed(final_state, "user2")
    if not ok:
        return 0.0, error

    # Check that user2 has special attention
    user_follows = final_state.get("userFollows")
    if not isinstance(user_follows, list):
        return 0.0, "userFollows array missing in backend final state"

    for entry in user_follows:
        if entry.get("followedUserId") == "user2":
            if entry.get("isSpecialAttention") is True:
                return 1.0, "Backend: Both users followed, user2 has special attention"
            else:
                return 0.0, "user2 is followed but does not have special attention"

    return 0.0, "user2 not found in userFollows"


def _validate_frontend_follow_and_set_special_attention_flow(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "special-follow")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to special follow feed"


_validate_follow_and_set_special_attention_flow: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_and_set_special_attention_flow,
    "validate_frontend": _validate_frontend_follow_and_set_special_attention_flow,
}


# -----------------------------------------------------------------------------
# Task: follow-and-unfollow-from-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_and_unfollow_from_profile(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user2 (科技资讯) is NOT followed (was followed then unfollowed)
    ok, error = _check_user_not_followed(final_state, "user2")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: User followed and then unfollowed successfully"


def _validate_frontend_follow_and_unfollow_from_profile(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user2")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully on profile page after follow/unfollow"


_validate_follow_and_unfollow_from_profile: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_and_unfollow_from_profile,
    "validate_frontend": _validate_frontend_follow_and_unfollow_from_profile,
}


# -----------------------------------------------------------------------------
# Task: follow-assign-to-group-and-navigate-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_assign_to_group_and_navigate(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 is followed
    ok, error = _check_user_followed(final_state, "user1")
    if not ok:
        return 0.0, error

    # Check that user1 is in "celebrities" group
    ok, error = _check_user_in_group(final_state, "user1", "celebrities")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: User followed and assigned to celebrities group successfully"


def _validate_frontend_follow_assign_to_group_and_navigate(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that current view is custom-group-celebrities
    view = final_state.get("currentView")
    if view != "custom-group-celebrities":
        return 0.0, f"currentView='{view}' expected 'custom-group-celebrities'"

    return 1.0, "Successfully navigated to custom group feed"


_validate_follow_assign_to_group_and_navigate: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_assign_to_group_and_navigate,
    "validate_frontend": _validate_frontend_follow_assign_to_group_and_navigate,
}


# -----------------------------------------------------------------------------
# Task: follow-create-group-and-assign-flow-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_create_group_and_assign_flow(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 is followed
    ok, error = _check_user_followed(final_state, "user1")
    if not ok:
        return 0.0, error

    # Check that a new custom group "test" was created
    custom_groups = final_state.get("customGroups")
    if not isinstance(custom_groups, list):
        return 0.0, "customGroups array missing in backend final state"

    group_id = None
    for group in custom_groups:
        if group.get("label") == "test":
            group_id = group.get("_id")
            break

    if not group_id:
        return 0.0, "Custom group 'test' not found"

    # Check that user1 is in the new group
    ok, error = _check_user_in_group(final_state, "user1", group_id)
    if not ok:
        return 0.0, error

    return 1.0, "Backend: User followed, group created, and user assigned successfully"


def _validate_frontend_follow_create_group_and_assign_flow(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user1")
    if not ok:
        return 0.0, error

    # Check that manage groups modal is closed
    if final_state.get("manageGroupsModalOpen", False):
        return 0.0, "manageGroupsModalOpen should be false"

    return 1.0, "Successfully created group and assigned user"


_validate_follow_create_group_and_assign_flow: ValidateTask = {
    "state_key": {
        "customGroups": {"collection": "customGroups", "filter": {}},
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_create_group_and_assign_flow,
    "validate_frontend": _validate_frontend_follow_create_group_and_assign_flow,
}


# -----------------------------------------------------------------------------
# Task: follow-multiple-users-from-search-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_multiple_users_from_search(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that at least 2 users are followed (we count total follows from current user)
    user_follows = final_state.get("userFollows")
    if not isinstance(user_follows, list):
        return 0.0, "userFollows array missing in backend final state"

    # Count follows by current user (8200663693)
    current_user_follows = [entry for entry in user_follows if entry.get("userId") == "8200663693"]

    if len(current_user_follows) >= 2:
        return 1.0, f"Backend: {len(current_user_follows)} users followed successfully"
    else:
        return 0.0, f"Expected at least 2 users followed, found {len(current_user_follows)}"


def _validate_frontend_follow_multiple_users_from_search(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "users")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully followed multiple users from search"


_validate_follow_multiple_users_from_search: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_multiple_users_from_search,
    "validate_frontend": _validate_frontend_follow_multiple_users_from_search,
}


# -----------------------------------------------------------------------------
# Task: follow-user-and-check-latest-feed-v2
# -----------------------------------------------------------------------------


def _validate_backend_follow_user_and_check_latest_feed(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that user1 (用户小王) is followed
    ok, error = _check_user_followed(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Backend: user1 followed successfully"


def _validate_frontend_follow_user_and_check_latest_feed(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "latest")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to latest feed after following user"


_validate_follow_user_and_check_latest_feed: ValidateTask = {
    "state_key": {
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_follow_user_and_check_latest_feed,
    "validate_frontend": _validate_frontend_follow_user_and_check_latest_feed,
}


# =============================================================================
# NAVIGATION TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: home-from-search-v2
# -----------------------------------------------------------------------------


def _validate_backend_home_from_search(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_home_from_search(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated home from search"


_validate_home_from_search: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_home_from_search,
    "validate_frontend": _validate_frontend_home_from_search,
}


# -----------------------------------------------------------------------------
# Task: navigate-post-v2
# -----------------------------------------------------------------------------


def _validate_backend_navigate_post(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_post(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "4")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to post detail page"


_validate_navigate_post: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_post,
    "validate_frontend": _validate_frontend_navigate_post,
}


# -----------------------------------------------------------------------------
# Task: navigate-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_navigate_profile(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for navigation"


def _validate_frontend_navigate_profile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user2")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to user profile"


_validate_navigate_profile: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_navigate_profile,
    "validate_frontend": _validate_frontend_navigate_profile,
}


# -----------------------------------------------------------------------------
# Task: load-more-posts-v2
# -----------------------------------------------------------------------------


def _validate_backend_load_more_posts(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for loading posts"


def _validate_frontend_load_more_posts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    # Check that scrollPosition has increased (more posts loaded)
    initial_scroll = initial_state.get("feedScrollPosition", 0)
    final_scroll = final_state.get("feedScrollPosition", 0)

    if final_scroll <= initial_scroll:
        return 0.0, f"feedScrollPosition did not increase: {initial_scroll} -> {final_scroll}"

    return 1.0, f"Successfully loaded more posts (scrolled from {initial_scroll} to {final_scroll})"


_validate_load_more_posts: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_load_more_posts,
    "validate_frontend": _validate_frontend_load_more_posts,
}


# -----------------------------------------------------------------------------
# Task: load-many-posts-v2
# -----------------------------------------------------------------------------


def _validate_backend_load_many_posts(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for loading posts"


def _validate_frontend_load_many_posts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "11")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully navigated to post from far down in feed"


_validate_load_many_posts: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_load_many_posts,
    "validate_frontend": _validate_frontend_load_many_posts,
}


# =============================================================================
# LIKE TASKS
# =============================================================================

# -----------------------------------------------------------------------------
# Task: like-post-from-main-feed-v2
# -----------------------------------------------------------------------------


def _validate_backend_like_post_from_main_feed(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that post 1 has isLiked=true
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("_id") == "1":
            if post.get("isLiked") is True:
                return 1.0, "Backend: Post liked successfully"
            else:
                return 0.0, "Post 1 is not liked in backend"

    return 0.0, "Post 1 not found in backend"


def _validate_frontend_like_post_from_main_feed(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    ok, error = _check_local_post_like_override(final_state, "1", True)
    if not ok:
        return 0.0, error

    return 1.0, "Successfully liked post from main feed"


_validate_like_post_from_main_feed: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {"_id": "1"}},
    },
    "validate_backend": _validate_backend_like_post_from_main_feed,
    "validate_frontend": _validate_frontend_like_post_from_main_feed,
}


# -----------------------------------------------------------------------------
# Task: like-comment-on-post-detail-v2
# -----------------------------------------------------------------------------


def _validate_backend_like_comment_on_post_detail(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that comment p1-c1 has isLiked=true
    comments = final_state.get("comments")
    if not isinstance(comments, list):
        return 0.0, "Comments array missing in backend final state"

    for comment in comments:
        if comment.get("_id") == "p1-c1" and comment.get("postId") == "1":
            if comment.get("isLiked") is True:
                return 1.0, "Backend: Comment liked successfully"
            else:
                return 0.0, "Comment p1-c1 is not liked in backend"

    return 0.0, "Comment p1-c1 not found in backend"


def _validate_frontend_like_comment_on_post_detail(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully liked comment on post detail page"


_validate_like_comment_on_post_detail: ValidateTask = {
    "state_key": {
        "comments": {"collection": "comments", "filter": {"postId": "1"}},
    },
    "validate_backend": _validate_backend_like_comment_on_post_detail,
    "validate_frontend": _validate_frontend_like_comment_on_post_detail,
}


# -----------------------------------------------------------------------------
# Task: like-2-comments-v2
# -----------------------------------------------------------------------------


def _validate_backend_like_2_comments(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that comments p1-c1 and p1-c2 have isLiked=true
    comments = final_state.get("comments")
    if not isinstance(comments, list):
        return 0.0, "Comments array missing in backend final state"

    liked_count = 0
    for comment in comments:
        if comment.get("postId") == "1" and comment.get("_id") in ["p1-c1", "p1-c2"]:
            if comment.get("isLiked") is True:
                liked_count += 1

    if liked_count >= 2:
        return 1.0, "Backend: Both comments liked successfully"
    elif liked_count == 1:
        return 0.0, "Only 1 comment liked, expected 2"
    else:
        return 0.0, "Neither comment is liked in backend"


def _validate_frontend_like_2_comments(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    # Check that the post's comments section is open
    ok, error = _check_feed_post_comments_open(final_state, "1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully liked 2 comments"


_validate_like_2_comments: ValidateTask = {
    "state_key": {
        "comments": {"collection": "comments", "filter": {"postId": "1"}},
    },
    "validate_backend": _validate_backend_like_2_comments,
    "validate_frontend": _validate_frontend_like_2_comments,
}


# =============================================================================
# SEARCH & NAVIGATION TASKS (NEW)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: accept-search-suggestion-v2
# -----------------------------------------------------------------------------


def _validate_backend_accept_search_suggestion(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search"


def _validate_frontend_accept_search_suggestion(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_query_equals(final_state, "用户小王")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully accepted search suggestion"


_validate_accept_search_suggestion: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_accept_search_suggestion,
    "validate_frontend": _validate_frontend_accept_search_suggestion,
}


# -----------------------------------------------------------------------------
# Task: change-search-categories-v2
# -----------------------------------------------------------------------------


def _validate_backend_change_search_categories(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    return 1.0, "No backend validation required for search category change"


def _validate_frontend_change_search_categories(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    ok, error = _check_search_category(final_state, "users")
    if not ok:
        return 0.0, error

    ok, error = _check_search_query_equals(final_state, "用户小王")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully changed search category to users"


_validate_change_search_categories: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_change_search_categories,
    "validate_frontend": _validate_frontend_change_search_categories,
}


# -----------------------------------------------------------------------------
# Task: change-trending-tab-and-navigate-v2
# -----------------------------------------------------------------------------


def _validate_backend_change_trending_tab_and_navigate(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    return 1.0, "No backend validation required for trending tab navigation"


def _validate_frontend_change_trending_tab_and_navigate(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "search")
    if not ok:
        return 0.0, error

    # Check that hotSearchTab is "trending"
    hot_search_tab = final_state.get("hotSearchTab")
    if hot_search_tab != "trending":
        return 0.0, f"hotSearchTab='{hot_search_tab}' expected 'trending'"

    # Check that searchQuery is not empty (it should be the trending topic)
    search_query = final_state.get("searchQuery", "")
    if not search_query:
        return 0.0, "searchQuery is empty"

    return 1.0, f"Successfully changed trending tab and navigated to topic: {search_query}"


_validate_change_trending_tab_and_navigate: ValidateTask = {
    "state_key": {},
    "validate_backend": _validate_backend_change_trending_tab_and_navigate,
    "validate_frontend": _validate_frontend_change_trending_tab_and_navigate,
}


# =============================================================================
# GROUP & USER MANAGEMENT TASKS (NEW)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: add-user-to-new-custom-group-from-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_add_user_to_new_custom_group_from_profile(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new custom group "兴趣爱好" exists
    custom_groups = final_state.get("customGroups")
    if not isinstance(custom_groups, list):
        return 0.0, "customGroups array missing in backend final state"

    group_id = None
    for group in custom_groups:
        if group.get("label") == "兴趣爱好":
            group_id = group.get("_id")
            break

    if not group_id:
        return 0.0, "Custom group '兴趣爱好' not found"

    # Check that user1 is in the new group (using group ID)
    ok, error = _check_user_in_group(final_state, "user1", group_id)
    if not ok:
        return 0.0, error

    return 1.0, "Backend: New group created and user assigned"


def _validate_frontend_add_user_to_new_custom_group_from_profile(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "user1")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully on profile page after adding user to new group"


_validate_add_user_to_new_custom_group_from_profile: ValidateTask = {
    "state_key": {
        "customGroups": {"collection": "customGroups", "filter": {}},
        "userFollows": {"collection": "userFollows", "filter": {}},
    },
    "validate_backend": _validate_backend_add_user_to_new_custom_group_from_profile,
    "validate_frontend": _validate_frontend_add_user_to_new_custom_group_from_profile,
}


# -----------------------------------------------------------------------------
# Task: create-custom-group-and-navigate-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_custom_group_and_navigate(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a custom group "test" exists
    custom_groups = final_state.get("customGroups")
    if not isinstance(custom_groups, list):
        return 0.0, "customGroups array missing in backend final state"

    for group in custom_groups:
        if group.get("label") == "test":
            return 1.0, "Backend: Custom group 'test' created"

    return 0.0, "Custom group 'test' not found"


def _validate_frontend_create_custom_group_and_navigate(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that current view starts with "custom-group-"
    view = final_state.get("currentView", "")
    if not view.startswith("custom-group-"):
        return 0.0, f"currentView='{view}' expected to start with 'custom-group-'"

    return 1.0, f"Successfully navigated to custom group feed: {view}"


_validate_create_custom_group_and_navigate: ValidateTask = {
    "state_key": {
        "customGroups": {"collection": "customGroups", "filter": {}},
    },
    "validate_backend": _validate_backend_create_custom_group_and_navigate,
    "validate_frontend": _validate_frontend_create_custom_group_and_navigate,
}


# =============================================================================
# COMMENT TASKS (NEW)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: create-comment-with-expressions-on-detail-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_comment_with_expressions_on_detail(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that post 2 has a new comment with expression
    comments = final_state.get("comments")
    if not isinstance(comments, list):
        return 0.0, "Comments array missing in backend final state"

    # Look for a new comment from current user with expression content on post 2
    for comment in comments:
        if comment.get("postId") == "2" and comment.get("user", {}).get("_id") == "8200663693":
            content = comment.get("content", "")
            # Check if it contains expression codes like [xxx]
            if "[" in content and "]" in content:
                return 1.0, "Backend: Comment with expression created successfully"

    return 0.0, "No new comment with expression found on post 2"


def _validate_frontend_create_comment_with_expressions_on_detail(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "post")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_post_id(final_state, "2")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created comment with expressions on post detail"


_validate_create_comment_with_expressions_on_detail: ValidateTask = {
    "state_key": {
        "comments": {"collection": "comments", "filter": {"postId": "2"}},
    },
    "validate_backend": _validate_backend_create_comment_with_expressions_on_detail,
    "validate_frontend": _validate_frontend_create_comment_with_expressions_on_detail,
}


# -----------------------------------------------------------------------------
# Task: create-comment-with-inline-section-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_comment_with_inline_section(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that post 2 has a new comment from current user
    comments = final_state.get("comments")
    if not isinstance(comments, list):
        return 0.0, "Comments array missing in backend final state"

    for comment in comments:
        if comment.get("postId") == "2" and comment.get("user", {}).get("_id") == "8200663693":
            return 1.0, "Backend: New comment created on post 2"

    return 0.0, "No new comment from current user found on post 2"


def _validate_frontend_create_comment_with_inline_section(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    ok, error = _check_feed_post_comments_open(final_state, "2")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created comment using inline section"


_validate_create_comment_with_inline_section: ValidateTask = {
    "state_key": {
        "comments": {"collection": "comments", "filter": {"postId": "2"}},
    },
    "validate_backend": _validate_backend_create_comment_with_inline_section,
    "validate_frontend": _validate_frontend_create_comment_with_inline_section,
}


# =============================================================================
# POST CREATION TASKS (NEW)
# =============================================================================

# -----------------------------------------------------------------------------
# Task: create-post-and-verify-in-profile-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_and_verify_in_profile(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new post by current user exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            if "这是我的新微博" in content or "#日常生活#" in content:
                return 1.0, "Backend: New post created successfully"

    return 0.0, "No new post with expected content found"


def _validate_frontend_create_post_and_verify_in_profile(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "profile")
    if not ok:
        return 0.0, error

    ok, error = _check_viewed_user_id(final_state, "8200663693")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post and verified in profile"


_validate_create_post_and_verify_in_profile: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_and_verify_in_profile,
    "validate_frontend": _validate_frontend_create_post_and_verify_in_profile,
}


# -----------------------------------------------------------------------------
# Task: create-post-with-emoji-expression-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_with_emoji_expression(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new post with [doge] exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            if "[doge]" in content:
                return 1.0, "Backend: Post with [doge] expression created"

    return 0.0, "No post with [doge] expression found"


def _validate_frontend_create_post_with_emoji_expression(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post with emoji expression"


_validate_create_post_with_emoji_expression: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_with_emoji_expression,
    "validate_frontend": _validate_frontend_create_post_with_emoji_expression,
}


# -----------------------------------------------------------------------------
# Task: create-post-with-hashtags-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_with_hashtags(state_key: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    # Check that a new post with hashtags exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            if "#生活分享#" in content and "#每日心情#" in content:
                return 1.0, "Backend: Post with hashtags created"

    return 0.0, "No post with both hashtags #生活分享# and #每日心情# found"


def _validate_frontend_create_post_with_hashtags(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post with hashtags"


_validate_create_post_with_hashtags: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_with_hashtags,
    "validate_frontend": _validate_frontend_create_post_with_hashtags,
}


# -----------------------------------------------------------------------------
# Task: create-post-with-three-expressions-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_with_three_expressions(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new post with 3 expressions exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            # Count expression codes [xxx]
            expressions = re.findall(r"\[[^\]]+\]", content)
            if len(expressions) >= 3:
                return 1.0, f"Backend: Post with {len(expressions)} expressions created"

    return 0.0, "No post with at least 3 expressions found"


def _validate_frontend_create_post_with_three_expressions(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post with three expressions"


_validate_create_post_with_three_expressions: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_with_three_expressions,
    "validate_frontend": _validate_frontend_create_post_with_three_expressions,
}


# -----------------------------------------------------------------------------
# Task: create-post-with-two-or-more-emojis-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_with_two_or_more_emojis(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new post with 2+ different emojis exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            # Count unique expression codes [xxx]
            expressions = set(re.findall(r"\[[^\]]+\]", content))
            if len(expressions) >= 2:
                return 1.0, f"Backend: Post with {len(expressions)} different emojis created"

    return 0.0, "No post with at least 2 different emojis found"


def _validate_frontend_create_post_with_two_or_more_emojis(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post with two or more emojis"


_validate_create_post_with_two_or_more_emojis: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_with_two_or_more_emojis,
    "validate_frontend": _validate_frontend_create_post_with_two_or_more_emojis,
}


# -----------------------------------------------------------------------------
# Task: create-post-with-user-mention-v2
# -----------------------------------------------------------------------------


def _validate_backend_create_post_with_user_mention(
    state_key: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    # Check that a new post with @mention exists
    posts = final_state.get("posts")
    if not isinstance(posts, list):
        return 0.0, "Posts array missing in backend final state"

    for post in posts:
        if post.get("user", {}).get("_id") == "8200663693":
            content = post.get("content", "")
            if "@科技资讯" in content:
                return 1.0, "Backend: Post with @mention created"

    return 0.0, "No post with @科技资讯 mention found"


def _validate_frontend_create_post_with_user_mention(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    ok, error = _check_current_view(final_state, "feed")
    if not ok:
        return 0.0, error

    return 1.0, "Successfully created post with user mention"


_validate_create_post_with_user_mention: ValidateTask = {
    "state_key": {
        "posts": {"collection": "posts", "filter": {}},
    },
    "validate_backend": _validate_backend_create_post_with_user_mention,
    "validate_frontend": _validate_frontend_create_post_with_user_mention,
}


# =============================================================================
# Registry of all V2 Reward Functions
# =============================================================================

REWARD_FUNCTIONS_WEIBO_V2: Dict[str, ValidateTask] = {
    # Navigation & Search Tasks
    "_validate_profile_from_search": _validate_profile_from_search,
    "_validate_search_users": _validate_search_users,
    "_validate_switch_theme": _validate_switch_theme,
    "_validate_search_dropdown_profile": _validate_search_dropdown_profile,
    "_validate_profile_from_sorted_comments": _validate_profile_from_sorted_comments,
    "_validate_view_full_comment_thread": _validate_view_full_comment_thread,
    "_validate_video_post_from_profile": _validate_video_post_from_profile,
    "_validate_refresh_list_of_trending_topics": _validate_refresh_list_of_trending_topics,
    "_validate_refresh_list_of_suggested_users": _validate_refresh_list_of_suggested_users,
    "_validate_navigate_to_latest_feed_section": _validate_navigate_to_latest_feed_section,
    "_validate_navigate_via_trending_topic": _validate_navigate_via_trending_topic,
    "_validate_no_search_suggestions": _validate_no_search_suggestions,
    "_validate_open_inline_comments_section": _validate_open_inline_comments_section,
    "_validate_open_post_composer_more_dropdown": _validate_open_post_composer_more_dropdown,
    "_validate_partial_search_query": _validate_partial_search_query,
    "_validate_post_from_profile": _validate_post_from_profile,
    "_validate_post_from_search": _validate_post_from_search,
    "_validate_profile_from_comments": _validate_profile_from_comments,
    "_validate_profile_from_post": _validate_profile_from_post,
    "_validate_profile_from_reply": _validate_profile_from_reply,
    "_validate_home_from_search": _validate_home_from_search,
    "_validate_navigate_post": _validate_navigate_post,
    "_validate_navigate_profile": _validate_navigate_profile,
    "_validate_load_more_posts": _validate_load_more_posts,
    "_validate_load_many_posts": _validate_load_many_posts,
    "_validate_accept_search_suggestion": _validate_accept_search_suggestion,
    "_validate_change_search_categories": _validate_change_search_categories,
    "_validate_change_trending_tab_and_navigate": _validate_change_trending_tab_and_navigate,
    # Like/Unlike Tasks
    "_validate_unlike_single_post_from_feed": _validate_unlike_single_post_from_feed,
    "_validate_unlike_all_posts_on_profile": _validate_unlike_all_posts_on_profile,
    "_validate_like_post_from_main_feed": _validate_like_post_from_main_feed,
    "_validate_like_comment_on_post_detail": _validate_like_comment_on_post_detail,
    "_validate_like_2_comments": _validate_like_2_comments,
    # Follow/Unfollow Tasks
    "_validate_unfollow_user_from_profile_page": _validate_unfollow_user_from_profile_page,
    "_validate_search_follow_last_user": _validate_search_follow_last_user,
    "_validate_follow_and_set_special_attention_flow": _validate_follow_and_set_special_attention_flow,
    "_validate_follow_and_unfollow_from_profile": _validate_follow_and_unfollow_from_profile,
    "_validate_follow_assign_to_group_and_navigate": _validate_follow_assign_to_group_and_navigate,
    "_validate_follow_create_group_and_assign_flow": _validate_follow_create_group_and_assign_flow,
    "_validate_follow_multiple_users_from_search": _validate_follow_multiple_users_from_search,
    "_validate_follow_user_and_check_latest_feed": _validate_follow_user_and_check_latest_feed,
    # Group Management Tasks
    "_validate_remove_user_from_single_group": _validate_remove_user_from_single_group,
    "_validate_reassign_user_to_different_group": _validate_reassign_user_to_different_group,
    "_validate_unassign_special_attention_and_groups": _validate_unassign_special_attention_and_groups,
    "_validate_delete_custom_group": _validate_delete_custom_group,
    "_validate_edit_custom_group_name": _validate_edit_custom_group_name,
    "_validate_add_user_to_new_custom_group_from_profile": _validate_add_user_to_new_custom_group_from_profile,
    "_validate_create_custom_group_and_navigate": _validate_create_custom_group_and_navigate,
    # Comment Tasks
    "_validate_reply_to_comment": _validate_reply_to_comment,
    "_validate_create_comment_with_expressions_on_detail": _validate_create_comment_with_expressions_on_detail,
    "_validate_create_comment_with_inline_section": _validate_create_comment_with_inline_section,
    # Post Creation Tasks
    "_validate_post_and_view_hashtag": _validate_post_and_view_hashtag,
    "_validate_post_image": _validate_post_image,
    "_validate_post_video": _validate_post_video,
    "_validate_create_post_and_verify_in_profile": _validate_create_post_and_verify_in_profile,
    "_validate_create_post_with_emoji_expression": _validate_create_post_with_emoji_expression,
    "_validate_create_post_with_hashtags": _validate_create_post_with_hashtags,
    "_validate_create_post_with_three_expressions": _validate_create_post_with_three_expressions,
    "_validate_create_post_with_two_or_more_emojis": _validate_create_post_with_two_or_more_emojis,
    "_validate_create_post_with_user_mention": _validate_create_post_with_user_mention,
}


__all__ = [
    "REWARD_FUNCTIONS_WEIBO_V2",
    "ValidateTask",
    "StateKey",
    "StateKeyQuery",
]

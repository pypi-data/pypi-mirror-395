"""
Reward functions for Weibo app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_navigateprofile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID
    - profileTab should be set appropriately

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user2"
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user2":
        return 0.0, f"Expected viewedUserId to be 'user2', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (optional but good to validate)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    return 1.0, "Successfully navigated to user2's profile page"


def _validate_navigatepost(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a post detail page.

    This function validates the final state matches the expected target state:
    - currentView should be "post"
    - viewedPostId should match the expected post ID
    - commentTab should be set appropriately

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "post"
    current_view = final_state.get("currentView")
    if current_view != "post":
        return 0.0, f"Not on post detail page, current view: {current_view}"

    # Check 2: viewedPostId is "4"
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id != "4":
        return 0.0, f"Expected viewedPostId to be '4', got '{viewed_post_id}'"

    # Check 3: commentTab is "hot" (default tab for post detail)
    comment_tab = final_state.get("commentTab")
    if comment_tab != "hot":
        return 0.0, f"Expected commentTab to be 'hot', got '{comment_tab}'"

    return 1.0, "Successfully navigated to post 4 detail page"


def _validate_loadmoreposts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that more posts were successfully loaded in the feed.

    This function validates the final state matches the expected target state:
    - currentView should remain "feed"
    - displayedPosts should have increased (from 10 to 30 posts)
    - isLoadingPosts should be False (loading completed)

    Args:
        initial_state: The initial state before loading more posts
        final_state: The final state after loading more posts

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "feed"
    current_view = final_state.get("currentView")
    if current_view != "feed":
        return 0.0, f"Not on feed page, current view: {current_view}"

    # Check 2: displayedPosts has increased
    initial_posts = initial_state.get("displayedPosts", [])
    final_posts = final_state.get("displayedPosts", [])

    initial_count = len(initial_posts)
    final_count = len(final_posts)

    if final_count <= initial_count:
        return 0.0, f"Posts did not increase: {initial_count} -> {final_count} (expected increase)"

    # Check 3: Final count should be 30 posts
    if final_count != 30:
        return 0.0, f"Expected 30 posts in final state, got {final_count}"

    # Check 4: isLoadingPosts should be False (loading completed)
    is_loading = final_state.get("isLoadingPosts")
    if is_loading:
        return 0.0, f"Expected isLoadingPosts to be False after loading, got {is_loading}"

    return 1.0, f"Successfully loaded more posts: {initial_count} -> {final_count} posts"


def _validate_postfromprofile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a post detail page from a profile page.

    This function validates the final state matches the expected target state:
    - currentView should be "post"
    - viewedPostId should match the expected post ID (31)
    - commentTab should be "hot" (default tab)
    - viewedUserId should be None (cleared when navigating to post detail)
    - displayedPosts should remain unchanged (persisted across pages)

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "post"
    current_view = final_state.get("currentView")
    if current_view != "post":
        return 0.0, f"Not on post detail page, current view: {current_view}"

    # Check 2: viewedPostId is "31"
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id != "31":
        return 0.0, f"Expected viewedPostId to be '31', got '{viewed_post_id}'"

    # Check 3: commentTab is "hot" (default tab for post detail)
    comment_tab = final_state.get("commentTab")
    if comment_tab != "hot":
        return 0.0, f"Expected commentTab to be 'hot', got '{comment_tab}'"

    # Check 4: viewedUserId should be None (cleared when navigating to post)
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id is not None:
        return 0.0, f"Expected viewedUserId to be None after navigating to post, got '{viewed_user_id}'"

    # Check 5: displayedPosts should remain unchanged (persisted across pages)
    initial_posts = initial_state.get("displayedPosts", [])
    final_posts = final_state.get("displayedPosts", [])

    initial_count = len(initial_posts)
    final_count = len(final_posts)

    if initial_count != final_count:
        return 0.0, f"displayedPosts count changed: {initial_count} -> {final_count} (should remain unchanged)"

    return 1.0, "Successfully navigated to post 31 detail page from profile"


def _validate_partialsearchquery(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully typed a partial search query and the dropdown shows results.

    This function validates the final state matches the expected target state:
    - searchQuery should be "电影"
    - searchDropdownOpen should be True
    - searchBarFocused should be True
    - searchDropdownResults.suggestions should have exactly 1 item containing "电影"
    - searchDropdownResults.users should have exactly 1 user whose name or bio contains "电影"

    Args:
        initial_state: The initial state before typing the query
        final_state: The final state after typing the query

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: searchQuery is "电影"
    search_query = final_state.get("searchQuery")
    if search_query != "电影":
        return 0.0, f"Expected searchQuery to be '电影', got '{search_query}'"

    # Check 2: searchDropdownOpen is True
    search_dropdown_open = final_state.get("searchDropdownOpen")
    if search_dropdown_open is not True:
        return 0.0, f"Expected searchDropdownOpen to be True, got {search_dropdown_open}"

    # Check 3: searchBarFocused is True
    search_bar_focused = final_state.get("searchBarFocused")
    if search_bar_focused is not True:
        return 0.0, f"Expected searchBarFocused to be True, got {search_bar_focused}"

    # Check 4: searchDropdownResults exists and has suggestions
    search_dropdown_results = final_state.get("searchDropdownResults", {})
    suggestions = search_dropdown_results.get("suggestions", [])

    if len(suggestions) != 1:
        return 0.0, f"Expected 1 search suggestion, got {len(suggestions)}"

    # Check 5: The suggestion contains "电影" as a substring
    suggestion = suggestions[0]
    if "电影" not in suggestion:
        return 0.0, f"Expected suggestion to contain '电影', got '{suggestion}'"

    # Check 6: searchDropdownResults has users
    users = search_dropdown_results.get("users", [])

    if len(users) != 1:
        return 0.0, f"Expected 1 suggested user, got {len(users)}"

    # Check 7: The user's name or bio contains "电影" as a substring
    user = users[0]
    user_name = user.get("name", "")
    user_bio = user.get("bio", "")

    if "电影" not in user_name and "电影" not in user_bio:
        return 0.0, f"Expected user name or bio to contain '电影', got name='{user_name}', bio='{user_bio}'"

    return 1.0, f"Successfully typed search query '电影' with 1 suggestion '{suggestion}' and 1 user '{user_name}'"


def _validate_searchdropdownprofile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from the search dropdown.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user13)
    - profileTab should be "posts" (default tab)
    - searchQuery should be empty (cleared after navigation)
    - searchDropdownOpen should be False (closed after navigation)

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user13"
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user13":
        return 0.0, f"Expected viewedUserId to be 'user13', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: searchQuery should be empty (cleared after navigation)
    search_query = final_state.get("searchQuery")
    if search_query != "":
        return 0.0, f"Expected searchQuery to be empty after navigation, got '{search_query}'"

    # Check 5: searchDropdownOpen should be False (closed after navigation)
    search_dropdown_open = final_state.get("searchDropdownOpen")
    if search_dropdown_open is not False:
        return 0.0, f"Expected searchDropdownOpen to be False after navigation, got {search_dropdown_open}"

    return 1.0, "Successfully navigated to user13's profile page from search dropdown"


def _validate_profilefrompost(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from a post detail page.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user5)
    - profileTab should be "posts" (default tab)
    - viewedPostId should be None (cleared when navigating to profile)

    Args:
        initial_state: The initial state before navigation (on post detail page)
        final_state: The final state after navigation (on profile page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user5"
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user5":
        return 0.0, f"Expected viewedUserId to be 'user5', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: viewedPostId should be None (cleared when navigating to profile)
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id is not None:
        return 0.0, f"Expected viewedPostId to be None after navigating to profile, got '{viewed_post_id}'"

    return 1.0, "Successfully navigated to user5's profile page from post detail page"


def _validate_nosearchsuggestions(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user typed a search query that yields no suggestions or users in the dropdown.

    This function validates the final state matches the expected target state:
    - searchQuery should be "asdf"
    - searchDropdownOpen should be True
    - searchBarFocused should be True
    - searchDropdownResults.suggestions should be empty (no suggestions)
    - searchDropdownResults.users should be empty (no users)

    Args:
        initial_state: The initial state before typing the query
        final_state: The final state after typing the query

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: searchQuery is "asdf"
    search_query = final_state.get("searchQuery")
    if search_query != "asdf":
        return 0.0, f"Expected searchQuery to be 'asdf', got '{search_query}'"

    # Check 2: searchDropdownOpen is True
    search_dropdown_open = final_state.get("searchDropdownOpen")
    if search_dropdown_open is not True:
        return 0.0, f"Expected searchDropdownOpen to be True, got {search_dropdown_open}"

    # Check 3: searchBarFocused is True
    search_bar_focused = final_state.get("searchBarFocused")
    if search_bar_focused is not True:
        return 0.0, f"Expected searchBarFocused to be True, got {search_bar_focused}"

    # Check 4: searchDropdownResults exists and has no suggestions
    search_dropdown_results = final_state.get("searchDropdownResults", {})
    suggestions = search_dropdown_results.get("suggestions", [])

    if len(suggestions) != 0:
        return 0.0, f"Expected 0 search suggestions, got {len(suggestions)}"

    # Check 5: searchDropdownResults has no users
    users = search_dropdown_results.get("users", [])

    if len(users) != 0:
        return 0.0, f"Expected 0 suggested users, got {len(users)}"

    return 1.0, "Successfully typed search query 'asdf' with no suggestions or users in dropdown"


def _validate_postfromsearch(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a post detail page from the search results page.

    This function validates the final state matches the expected target state:
    - currentView should be "post"
    - viewedPostId should match the expected post ID (35)
    - commentTab should be "hot" (default tab)
    - searchQuery should be empty (cleared after navigation)
    - viewedUserId should be None (cleared when navigating to post detail)

    Args:
        initial_state: The initial state before navigation (on search results page)
        final_state: The final state after navigation (on post detail page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "post"
    current_view = final_state.get("currentView")
    if current_view != "post":
        return 0.0, f"Not on post detail page, current view: {current_view}"

    # Check 2: viewedPostId is "35"
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id != "35":
        return 0.0, f"Expected viewedPostId to be '35', got '{viewed_post_id}'"

    # Check 3: commentTab is "hot" (default tab for post detail)
    comment_tab = final_state.get("commentTab")
    if comment_tab != "hot":
        return 0.0, f"Expected commentTab to be 'hot', got '{comment_tab}'"

    # Check 4: searchQuery should be empty (cleared after navigation)
    search_query = final_state.get("searchQuery")
    if search_query != "":
        return 0.0, f"Expected searchQuery to be empty after navigation, got '{search_query}'"

    # Check 5: viewedUserId should be None (cleared when navigating to post)
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id is not None:
        return 0.0, f"Expected viewedUserId to be None after navigating to post, got '{viewed_user_id}'"

    return 1.0, "Successfully navigated to post 35 detail page from search results"


def _validate_acceptsearchsuggestion(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully selected a search suggestion and navigated to search results.

    This function validates the final state matches the expected target state:
    - currentView should be "search" (navigated to search results page)
    - searchQuery should match the selected suggestion ("用户小王")
    - searchCategory should be "comprehensive" (default category)
    - searchDropdownOpen should be False (closed after selection)

    Args:
        initial_state: The initial state before selecting the suggestion
        final_state: The final state after selecting the suggestion

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "search"
    current_view = final_state.get("currentView")
    if current_view != "search":
        return 0.0, f"Not on search results page, current view: {current_view}"

    # Check 2: searchQuery is "用户小王" (the selected suggestion)
    search_query = final_state.get("searchQuery")
    if search_query != "用户小王":
        return 0.0, f"Expected searchQuery to be '用户小王', got '{search_query}'"

    # Check 3: searchCategory is "comprehensive" (default category)
    search_category = final_state.get("searchCategory")
    if search_category != "comprehensive":
        return 0.0, f"Expected searchCategory to be 'comprehensive', got '{search_category}'"

    # Check 4: searchDropdownOpen should be False (closed after selection)
    search_dropdown_open = final_state.get("searchDropdownOpen")
    if search_dropdown_open is not False:
        return 0.0, f"Expected searchDropdownOpen to be False after selection, got {search_dropdown_open}"

    return 1.0, "Successfully selected search suggestion '用户小王' and navigated to search results"


def _validate_changesearchcategories(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully changed the search category from comprehensive to users.

    This function validates the final state matches the expected target state:
    - currentView should remain "search" (stays on search page)
    - searchQuery should remain unchanged ("用户小王")
    - searchCategory should be "users" (changed from comprehensive)
    - searchPageResults.users should have exactly 1 user

    Args:
        initial_state: The initial state before changing category (comprehensive)
        final_state: The final state after changing category (users)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "search" (stays on search page)
    current_view = final_state.get("currentView")
    if current_view != "search":
        return 0.0, f"Not on search results page, current view: {current_view}"

    # Check 2: searchQuery remains unchanged ("用户小王")
    search_query = final_state.get("searchQuery")
    if search_query != "用户小王":
        return 0.0, f"Expected searchQuery to remain '用户小王', got '{search_query}'"

    # Check 3: searchCategory is "users" (changed from comprehensive)
    search_category = final_state.get("searchCategory")
    if search_category != "users":
        return 0.0, f"Expected searchCategory to be 'users', got '{search_category}'"

    # Check 4: searchPageResults has exactly 1 user
    search_page_results = final_state.get("searchPageResults", {})
    users = search_page_results.get("users", [])

    if len(users) != 1:
        return 0.0, f"Expected 1 user in search results, got {len(users)}"

    return 1.0, "Successfully changed search category from comprehensive to users"


def _validate_profilefromsearch(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from the search results page.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user16 - 新用户)
    - profileTab should be "posts" (default tab)
    - searchQuery should be empty (cleared after navigation)

    Args:
        initial_state: The initial state before navigation (on search results page)
        final_state: The final state after navigation (on profile page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user16" (the user with name "新用户")
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user16":
        return 0.0, f"Expected viewedUserId to be 'user16', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: searchQuery should be empty (cleared after navigation)
    search_query = final_state.get("searchQuery")
    if search_query != "":
        return 0.0, f"Expected searchQuery to be empty after navigation, got '{search_query}'"

    return 1.0, "Successfully navigated to user16's (新用户) profile page from search results"


def _validate_profilefromcomments(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from a comment on a post detail page.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user14 - 日常分享)
    - profileTab should be "posts" (default tab)
    - viewedPostId should be None (cleared when navigating to profile)

    Args:
        initial_state: The initial state before navigation (on post detail page with comments)
        final_state: The final state after navigation (on profile page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user14" (the user with name "日常分享")
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user14":
        return 0.0, f"Expected viewedUserId to be 'user14', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: viewedPostId should be None (cleared when navigating to profile)
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id is not None:
        return 0.0, f"Expected viewedPostId to be None after navigating to profile, got '{viewed_post_id}'"

    return 1.0, "Successfully navigated to user14's (日常分享) profile page from comments"


def _validate_loadmanyposts(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully loaded more posts and navigated to a specific post detail page.

    This function validates the final state matches the expected target state:
    - currentView should be "post"
    - viewedPostId should match the expected post ID (23)
    - commentTab should be "hot" (default tab)
    - The post should be from user "读书笔记"
    - The post should have exactly 3 attachments (media items)

    Args:
        initial_state: The initial state before loading more posts (on feed page)
        final_state: The final state after navigating to post detail page

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "post"
    current_view = final_state.get("currentView")
    if current_view != "post":
        return 0.0, f"Not on post detail page, current view: {current_view}"

    # Check 2: viewedPostId is "23"
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id != "23":
        return 0.0, f"Expected viewedPostId to be '23', got '{viewed_post_id}'"

    # Check 3: commentTab is "hot" (default tab for post detail)
    comment_tab = final_state.get("commentTab")
    if comment_tab != "hot":
        return 0.0, f"Expected commentTab to be 'hot', got '{comment_tab}'"

    # Check 4: Find the post in allPosts and validate user name and attachments
    all_posts = final_state.get("allPosts", [])
    target_post = next((p for p in all_posts if p.get("id") == "23"), None)

    if target_post is None:
        return 0.0, "Post with ID '23' not found in allPosts"

    # Check 5: Post should be from user "读书笔记"
    post_user = target_post.get("user", {})
    user_name = post_user.get("name", "")
    if user_name != "读书笔记":
        return 0.0, f"Expected post to be from user '读书笔记', got '{user_name}'"

    # Check 6: Post should have exactly 3 attachments (media items)
    media = target_post.get("media", [])
    media_count = len(media)
    if media_count != 3:
        return 0.0, f"Expected post to have 3 attachments, got {media_count}"

    return 1.0, f"Successfully navigated to post 23 detail page (from 读书笔记 with {media_count} attachments)"


def _validate_profilefromsortedcomments(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from a comment after sorting comments by time.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user13 - 电影评论)
    - profileTab should be "posts" (default tab)
    - viewedPostId should be None (cleared when navigating to profile)

    Args:
        initial_state: The initial state before navigation (on post detail page with sorted comments)
        final_state: The final state after navigation (on profile page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user13" (the user with name "电影评论")
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user13":
        return 0.0, f"Expected viewedUserId to be 'user13', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: viewedPostId should be None (cleared when navigating to profile)
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id is not None:
        return 0.0, f"Expected viewedPostId to be None after navigating to profile, got '{viewed_post_id}'"

    return 1.0, "Successfully navigated to user13's (电影评论) profile page from sorted comments"


def _validate_switchtheme(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully switched the theme from light mode to dark mode.

    This function validates the final state matches the expected target state:
    - theme should be "dark" (changed from "light")

    Args:
        initial_state: The initial state before switching theme (light mode)
        final_state: The final state after switching theme (dark mode)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: theme is "dark"
    theme = final_state.get("theme")
    if theme != "dark":
        return 0.0, f"Expected theme to be 'dark', got '{theme}'"

    return 1.0, "Successfully switched theme from light to dark"


def _validate_homefromsearch(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from the search results page to the home feed.

    This function validates the final state matches the expected target state:
    - currentView should be "feed" (navigated to home feed)
    - searchQuery should be empty (cleared after navigation)

    Args:
        initial_state: The initial state before navigation (on search results page)
        final_state: The final state after navigation (on home feed)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "feed"
    current_view = final_state.get("currentView")
    if current_view != "feed":
        return 0.0, f"Not on home feed page, current view: {current_view}"

    # Check 2: searchQuery should be empty (cleared after navigation)
    search_query = final_state.get("searchQuery")
    if search_query != "":
        return 0.0, f"Expected searchQuery to be empty after navigation, got '{search_query}'"

    return 1.0, "Successfully navigated from search results to home feed"


def _validate_videopostfromprofile(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a video post detail page from a profile page.

    This function validates the final state matches the expected target state:
    - currentView should be "post"
    - viewedPostId should match the expected post ID (23)
    - commentTab should be "hot" (default tab)
    - The post should be from user "读书笔记"
    - The post should have at least one video attachment (media item with type "video")

    Args:
        initial_state: The initial state before navigation (on profile page with video tab selected)
        final_state: The final state after navigation (on post detail page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "post"
    current_view = final_state.get("currentView")
    if current_view != "post":
        return 0.0, f"Not on post detail page, current view: {current_view}"

    # Check 2: viewedPostId is "23"
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id != "23":
        return 0.0, f"Expected viewedPostId to be '23', got '{viewed_post_id}'"

    # Check 3: commentTab is "hot" (default tab for post detail)
    comment_tab = final_state.get("commentTab")
    if comment_tab != "hot":
        return 0.0, f"Expected commentTab to be 'hot', got '{comment_tab}'"

    # Check 4: Find the post in allPosts and validate user name and video attachment
    all_posts = final_state.get("allPosts", [])
    target_post = next((p for p in all_posts if p.get("id") == "23"), None)

    if target_post is None:
        return 0.0, "Post with ID '23' not found in allPosts"

    # Check 5: Post should be from user "读书笔记"
    post_user = target_post.get("user", {})
    user_name = post_user.get("name", "")
    if user_name != "读书笔记":
        return 0.0, f"Expected post to be from user '读书笔记', got '{user_name}'"

    # Check 6: Post should have at least one video attachment
    media = target_post.get("media", [])
    video_media = [m for m in media if m.get("type") == "video"]

    if len(video_media) == 0:
        return (
            0.0,
            f"Expected post to have at least one video attachment, got {len(media)} media items with {len(video_media)} videos",
        )

    return 1.0, "Successfully navigated to post 23 detail page (from 读书笔记 with video attachment)"


def _validate_profilefromreply(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to a profile page from a reply to a comment on a post detail page.

    This function validates the final state matches the expected target state:
    - currentView should be "profile"
    - viewedUserId should match the expected user ID (user4 - 旅行达人)
    - profileTab should be "posts" (default tab)
    - viewedPostId should be None (cleared when navigating to profile)

    Args:
        initial_state: The initial state before navigation (on post detail page with replies)
        final_state: The final state after navigation (on profile page)

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "profile"
    current_view = final_state.get("currentView")
    if current_view != "profile":
        return 0.0, f"Not on profile page, current view: {current_view}"

    # Check 2: viewedUserId is "user4" (the user with name "旅行达人")
    viewed_user_id = final_state.get("viewedUserId")
    if viewed_user_id != "user4":
        return 0.0, f"Expected viewedUserId to be 'user4', got '{viewed_user_id}'"

    # Check 3: profileTab is "posts" (default tab)
    profile_tab = final_state.get("profileTab")
    if profile_tab != "posts":
        return 0.0, f"Expected profileTab to be 'posts', got '{profile_tab}'"

    # Check 4: viewedPostId should be None (cleared when navigating to profile)
    viewed_post_id = final_state.get("viewedPostId")
    if viewed_post_id is not None:
        return 0.0, f"Expected viewedPostId to be None after navigating to profile, got '{viewed_post_id}'"

    return 1.0, "Successfully navigated to user4's (旅行达人) profile page from reply"


def _validate_searchusers(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully searched for users and navigated to the users category of search results.

    This function validates the final state matches the expected target state:
    - currentView should be "search" (navigated to search results page)
    - searchQuery should be "好" (the search term)
    - searchCategory should be "users" (users category selected)
    - searchPageResults.users should have at least one user (list of users in search results)

    Args:
        initial_state: The initial state before searching (on feed page)
        final_state: The final state after navigating to users search results

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: currentView is "search" (navigated to search results page)
    current_view = final_state.get("currentView")
    if current_view != "search":
        return 0.0, f"Not on search results page, current view: {current_view}"

    # Check 2: searchQuery is "好" (the search term)
    search_query = final_state.get("searchQuery")
    if search_query != "好":
        return 0.0, f"Expected searchQuery to be '好', got '{search_query}'"

    # Check 3: searchCategory is "users" (users category selected)
    search_category = final_state.get("searchCategory")
    if search_category != "users":
        return 0.0, f"Expected searchCategory to be 'users', got '{search_category}'"

    # Check 4: searchPageResults has at least one user (list of users in search results)
    search_page_results = final_state.get("searchPageResults", {})
    users = search_page_results.get("users", [])

    if len(users) == 0:
        return 0.0, f"Expected at least one user in search results, got {len(users)} users"

    return 1.0, f"Successfully navigated to users search results page with {len(users)} users"


# Registry of all Weibo reward functions
REWARD_FUNCTIONS_WEIBO = {
    "_validate_navigateprofile": _validate_navigateprofile,
    "_validate_navigatepost": _validate_navigatepost,
    "_validate_loadmoreposts": _validate_loadmoreposts,
    "_validate_postfromprofile": _validate_postfromprofile,
    "_validate_partialsearchquery": _validate_partialsearchquery,
    "_validate_searchdropdownprofile": _validate_searchdropdownprofile,
    "_validate_profilefrompost": _validate_profilefrompost,
    "_validate_nosearchsuggestions": _validate_nosearchsuggestions,
    "_validate_postfromsearch": _validate_postfromsearch,
    "_validate_acceptsearchsuggestion": _validate_acceptsearchsuggestion,
    "_validate_changesearchcategories": _validate_changesearchcategories,
    "_validate_profilefromsearch": _validate_profilefromsearch,
    "_validate_profilefromcomments": _validate_profilefromcomments,
    "_validate_loadmanyposts": _validate_loadmanyposts,
    "_validate_profilefromsortedcomments": _validate_profilefromsortedcomments,
    "_validate_switchtheme": _validate_switchtheme,
    "_validate_homefromsearch": _validate_homefromsearch,
    "_validate_videopostfromprofile": _validate_videopostfromprofile,
    "_validate_profilefromreply": _validate_profilefromreply,
    "_validate_searchusers": _validate_searchusers,
}

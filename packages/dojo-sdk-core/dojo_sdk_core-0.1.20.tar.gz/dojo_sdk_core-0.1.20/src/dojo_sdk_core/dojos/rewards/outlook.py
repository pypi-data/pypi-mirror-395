"""
Reward functions for Outlook app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_go_to_the_drafts_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the Drafts page.

    This function checks:
    1. The currentPage is "drafts"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: currentPage should be "drafts"
        current_page = final_state.get("currentPage")
        if current_page != "drafts":
            return (
                0.0,
                f"Expected currentPage to be 'drafts', got '{current_page}'",
            )

        return 1.0, "Successfully navigated to Drafts page"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_go_to_the_sent_items_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the Sent Items page.

    This function checks:
    1. The currentPage is "sent"

    Args:
        initial_state: The initial state before navigation
        final_state: The final state after navigation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: currentPage should be "sent"
        current_page = final_state.get("currentPage")
        if current_page != "sent":
            return (
                0.0,
                f"Expected currentPage to be 'sent', got '{current_page}'",
            )

        return 1.0, "Successfully navigated to Sent Items page"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_open_an_email_from_the_list(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully opened an email from the list.

    This function checks:
    1. The selectedEmailId is "3" (LinkedIn email)
    2. Email with id "3" has read status set to true

    Args:
        initial_state: The initial state before opening
        final_state: The final state after opening

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: selectedEmailId should be "3"
        selected_email_id = final_state.get("selectedEmailId")
        if selected_email_id != "3":
            return (
                0.0,
                f"Expected selectedEmailId to be '3', got '{selected_email_id}'",
            )

        # Check 2: Email with id "3" should have read = true
        emails = final_state.get("emails", [])
        email_3 = next((e for e in emails if e.get("id") == "3"), None)

        if email_3 is None:
            return 0.0, "Email with id '3' not found in emails array"

        if not email_3.get("read"):
            return (
                0.0,
                f"Expected email '3' to have read=true, got read={email_3.get('read')}",
            )

        return 1.0, "Successfully opened email from the list"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_delete_an_email_from_the_list(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully deleted an email from the list.

    This function checks:
    1. Email with id "3" (LinkedIn) is removed from the emails array

    Args:
        initial_state: The initial state before deletion
        final_state: The final state after deletion

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: Email with id "3" should not exist in emails array
        emails = final_state.get("emails", [])
        email_3 = next((e for e in emails if e.get("id") == "3"), None)

        if email_3 is not None:
            return 0.0, "Email with id '3' (LinkedIn) still exists, should be deleted"

        return 1.0, "Successfully deleted email from the list"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_flag_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully flagged an email.

    This function checks:
    1. Email with id "3" (LinkedIn) has flagged status set to true

    Args:
        initial_state: The initial state before flagging
        final_state: The final state after flagging

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: Email with id "3" should have flagged = true
        emails = final_state.get("emails", [])
        email_3 = next((e for e in emails if e.get("id") == "3"), None)

        if email_3 is None:
            return 0.0, "Email with id '3' not found in emails array"

        if not email_3.get("flagged"):
            return (
                0.0,
                f"Expected email '3' to have flagged=true, got flagged={email_3.get('flagged')}",
            )

        return 1.0, "Successfully flagged the email"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_pin_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully pinned an email.

    This function checks:
    1. Email with id "6" (Google Calendar) has pinned status set to true

    Args:
        initial_state: The initial state before pinning
        final_state: The final state after pinning

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: Email with id "6" should have pinned = true
        emails = final_state.get("emails", [])
        email_6 = next((e for e in emails if e.get("id") == "6"), None)

        if email_6 is None:
            return 0.0, "Email with id '6' not found in emails array"

        if not email_6.get("pinned"):
            return (
                0.0,
                f"Expected email '6' to have pinned=true, got pinned={email_6.get('pinned')}",
            )

        return 1.0, "Successfully pinned the email"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_toggle_read_on_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully toggled read status on an email.

    This function checks:
    1. Email with id "3" (LinkedIn) has read status set to true

    Args:
        initial_state: The initial state before toggling
        final_state: The final state after toggling

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: Email with id "3" should have read = true
        emails = final_state.get("emails", [])
        email_3 = next((e for e in emails if e.get("id") == "3"), None)

        if email_3 is None:
            return 0.0, "Email with id '3' not found in emails array"

        if not email_3.get("read"):
            return (
                0.0,
                f"Expected email '3' to have read=true, got read={email_3.get('read')}",
            )

        return 1.0, "Successfully toggled read status on the email"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_toggle_unread_on_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully toggled unread status on an email.

    This function checks:
    1. Email with id "2" (Netflix) has read status set to false

    Args:
        initial_state: The initial state before toggling
        final_state: The final state after toggling

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: Email with id "2" should have read = false
        emails = final_state.get("emails", [])
        email_2 = next((e for e in emails if e.get("id") == "2"), None)

        if email_2 is None:
            return 0.0, "Email with id '2' not found in emails array"

        if email_2.get("read"):
            return (
                0.0,
                f"Expected email '2' to have read=false, got read={email_2.get('read')}",
            )

        return 1.0, "Successfully toggled unread status on the email"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_compose_a_new_draft(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully composed a new draft.

    This function checks:
    1. A new draft email exists (id starts with "draft-")
    2. The currentPage is "drafts"
    3. The selectedEmailId is set to the new draft

    Args:
        initial_state: The initial state before composing
        final_state: The final state after composing

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "drafts"
        current_page = final_state.get("currentPage")
        if current_page != "drafts":
            return (
                0.0,
                f"Expected currentPage to be 'drafts', got '{current_page}'",
            )

        # Check 2: Find a new draft email
        emails = final_state.get("emails", [])
        new_draft = next((e for e in emails if e.get("id", "").startswith("draft-") and e.get("folder") == "drafts"), None)

        if new_draft is None:
            return 0.0, "No new draft email found with id starting with 'draft-'"

        # Check 3: selectedEmailId should be set to the new draft
        selected_email_id = final_state.get("selectedEmailId")
        if selected_email_id != new_draft.get("id"):
            return (
                0.0,
                f"Expected selectedEmailId to be '{new_draft.get('id')}', got '{selected_email_id}'",
            )

        return 1.0, "Successfully composed a new draft"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_fill_draft_fields(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filled draft fields.

    This function checks:
    1. The draft email has to="teammate@example.com"
    2. The draft email has subject="Weekly update"
    3. The draft email has body containing "This is an update from me!"

    Args:
        initial_state: The initial state before filling
        final_state: The final state after filling

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Find the draft email
        emails = final_state.get("emails", [])
        draft_email = next((e for e in emails if e.get("id", "").startswith("draft-") and e.get("folder") == "drafts"), None)

        if draft_email is None:
            return 0.0, "No draft email found"

        # Check 1: to field should be "teammate@example.com"
        to_field = draft_email.get("to", "")
        if to_field != "teammate@example.com":
            return (
                0.0,
                f"Expected 'to' field to be 'teammate@example.com', got '{to_field}'",
            )

        # Check 2: subject should be "Weekly update"
        subject = draft_email.get("subject", "")
        if subject != "Weekly update":
            return (
                0.0,
                f"Expected subject to be 'Weekly update', got '{subject}'",
            )

        # Check 3: body should contain "This is an update from me!"
        body = draft_email.get("body", "")
        if "This is an update from me!" not in body:
            return (
                0.0,
                f"Expected body to contain 'This is an update from me!', got '{body}'",
            )

        return 1.0, "Successfully filled draft fields"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_send_the_draft(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully sent the draft.

    This function checks:
    1. The currentPage is "sent"
    2. A new sent email exists with id starting with "sent-"
    3. The sent email has to="teammate@example.com"
    4. The sent email has subject="Weekly update"
    5. The sent email has body="This is an update from me!"
    6. The sent email has folder="sent"

    Args:
        initial_state: The initial state before sending
        final_state: The final state after sending

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "sent"
        current_page = final_state.get("currentPage")
        if current_page != "sent":
            return (
                0.0,
                f"Expected currentPage to be 'sent', got '{current_page}'",
            )

        # Check 2: Find a new sent email
        emails = final_state.get("emails", [])
        sent_email = next((e for e in emails if e.get("id", "").startswith("sent-") and e.get("folder") == "sent"), None)

        if sent_email is None:
            return 0.0, "No new sent email found with id starting with 'sent-'"

        # Check 3: to field should be "teammate@example.com"
        to_field = sent_email.get("to", "")
        if to_field != "teammate@example.com":
            return (
                0.0,
                f"Expected 'to' field to be 'teammate@example.com', got '{to_field}'",
            )

        # Check 4: subject should be "Weekly update"
        subject = sent_email.get("subject", "")
        if subject != "Weekly update":
            return (
                0.0,
                f"Expected subject to be 'Weekly update', got '{subject}'",
            )

        # Check 5: body should be "This is an update from me!"
        body = sent_email.get("body", "")
        if body.strip() != "This is an update from me!":
            return (
                0.0,
                f"Expected body to be 'This is an update from me!', got '{body}'",
            )

        return 1.0, "Successfully sent the draft"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_discard_a_draft(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully discarded a draft.

    This function checks:
    1. Email with id "13" (Weekend plans draft) is removed from emails array
    2. The currentPage is "drafts"
    3. The selectedEmailId is null

    Args:
        initial_state: The initial state before discarding
        final_state: The final state after discarding

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: Email with id "13" should not exist
        emails = final_state.get("emails", [])
        email_13 = next((e for e in emails if e.get("id") == "13"), None)

        if email_13 is not None:
            return 0.0, "Email with id '13' still exists, should be discarded"

        # Check 2: currentPage should be "drafts"
        current_page = final_state.get("currentPage")
        if current_page != "drafts":
            return (
                0.0,
                f"Expected currentPage to be 'drafts', got '{current_page}'",
            )

        # Check 3: selectedEmailId should be null
        selected_email_id = final_state.get("selectedEmailId")
        if selected_email_id is not None:
            return (
                0.0,
                f"Expected selectedEmailId to be null, got '{selected_email_id}'",
            )

        return 1.0, "Successfully discarded the draft"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_type_to_show_search_suggestions(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully typed to show search suggestions.

    This function checks:
    1. The searchQuery is "GitHub"
    2. The searchInputValue is "GitHub"
    3. The isSearchExpanded is true

    Args:
        initial_state: The initial state before typing
        final_state: The final state after typing

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: searchQuery should be "GitHub"
        search_query = final_state.get("searchQuery", "")
        if search_query != "GitHub":
            return (
                0.0,
                f"Expected searchQuery to be 'GitHub', got '{search_query}'",
            )

        # Check 2: searchInputValue should be "GitHub"
        search_input_value = final_state.get("searchInputValue", "")
        if search_input_value != "GitHub":
            return (
                0.0,
                f"Expected searchInputValue to be 'GitHub', got '{search_input_value}'",
            )

        # Check 3: isSearchExpanded should be true
        is_search_expanded = final_state.get("isSearchExpanded")
        if not is_search_expanded:
            return (
                0.0,
                f"Expected isSearchExpanded to be true, got '{is_search_expanded}'",
            )

        return 1.0, "Successfully typed to show search suggestions"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_submit_a_search_with_enter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully submitted a search with enter.

    This function checks:
    1. The currentPage is "search"
    2. The searchQuery is "user"
    3. The searchInputValue is "user"

    Args:
        initial_state: The initial state before submitting
        final_state: The final state after submitting

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchQuery should be "user"
        search_query = final_state.get("searchQuery", "")
        if search_query != "user":
            return (
                0.0,
                f"Expected searchQuery to be 'user', got '{search_query}'",
            )

        # Check 3: searchInputValue should be "user"
        search_input_value = final_state.get("searchInputValue", "")
        if search_input_value != "user":
            return (
                0.0,
                f"Expected searchInputValue to be 'user', got '{search_input_value}'",
            )

        return 1.0, "Successfully submitted search with enter"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_open_an_email_from_the_search_dropdown(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully opened an email from the search dropdown.

    This function checks:
    1. The currentPage is "search"
    2. The selectedEmailId is "1"
    3. Email with id "1" has read status set to true

    Args:
        initial_state: The initial state before opening
        final_state: The final state after opening

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: selectedEmailId should be "1"
        selected_email_id = final_state.get("selectedEmailId")
        if selected_email_id != "1":
            return (
                0.0,
                f"Expected selectedEmailId to be '1', got '{selected_email_id}'",
            )

        # Check 3: Email with id "1" should have read = true
        emails = final_state.get("emails", [])
        email_1 = next((e for e in emails if e.get("id") == "1"), None)

        if email_1 is None:
            return 0.0, "Email with id '1' not found in emails array"

        if not email_1.get("read"):
            return (
                0.0,
                f"Expected email '1' to have read=true, got read={email_1.get('read')}",
            )

        return 1.0, "Successfully opened email from search dropdown"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_apply_the_has_attachments_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully applied the has attachments filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchFilters includes "hasAttachments"

    Args:
        initial_state: The initial state before applying filter
        final_state: The final state after applying filter

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchFilters should include "hasAttachments"
        search_filters = final_state.get("searchFilters", [])
        if "hasAttachments" not in search_filters:
            return (
                0.0,
                f"Expected searchFilters to include 'hasAttachments', got {search_filters}",
            )

        return 1.0, "Successfully applied has attachments filter"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_apply_the_unread_search_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully applied the unread search filter.

    This function checks:
    1. The currentPage is "search"
    2. The searchFilters includes "unreads"

    Args:
        initial_state: The initial state before applying filter
        final_state: The final state after applying filter

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: currentPage should be "search"
        current_page = final_state.get("currentPage")
        if current_page != "search":
            return (
                0.0,
                f"Expected currentPage to be 'search', got '{current_page}'",
            )

        # Check 2: searchFilters should include "unreads"
        search_filters = final_state.get("searchFilters", [])
        if "unreads" not in search_filters:
            return (
                0.0,
                f"Expected searchFilters to include 'unreads', got {search_filters}",
            )

        return 1.0, "Successfully applied unread search filter"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_choose_sent_items_from_the_folder_selector(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully chose sent items from the folder selector.

    This function checks:
    1. The isSearchExpanded is true
    2. The selectedFolder is "sent"

    Args:
        initial_state: The initial state before selecting
        final_state: The final state after selecting

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check 1: isSearchExpanded should be true
        is_search_expanded = final_state.get("isSearchExpanded")
        if not is_search_expanded:
            return (
                0.0,
                f"Expected isSearchExpanded to be true, got '{is_search_expanded}'",
            )

        # Check 2: selectedFolder should be "sent"
        selected_folder = final_state.get("selectedFolder")
        if selected_folder != "sent":
            return (
                0.0,
                f"Expected selectedFolder to be 'sent', got '{selected_folder}'",
            )

        return 1.0, "Successfully chose sent items from folder selector"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_collapse_the_favorites_section(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully collapsed the favorites section.

    This function checks:
    1. The isFavoritesOpen is false

    Args:
        initial_state: The initial state before collapsing
        final_state: The final state after collapsing

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: isFavoritesOpen should be false
        is_favorites_open = final_state.get("isFavoritesOpen")
        if is_favorites_open:
            return (
                0.0,
                f"Expected isFavoritesOpen to be false, got '{is_favorites_open}'",
            )

        return 1.0, "Successfully collapsed the favorites section"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_expand_the_navigation_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully expanded the navigation sidebar.

    This function checks:
    1. The sidebarCollapsed is false

    Args:
        initial_state: The initial state before expanding
        final_state: The final state after expanding

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: sidebarCollapsed should be false
        sidebar_collapsed = final_state.get("sidebarCollapsed")
        if sidebar_collapsed:
            return (
                0.0,
                f"Expected sidebarCollapsed to be false, got '{sidebar_collapsed}'",
            )

        return 1.0, "Successfully expanded the navigation sidebar"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_collapse_the_navigation_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully collapsed the navigation sidebar.

    This function checks:
    1. The sidebarCollapsed is true

    Args:
        initial_state: The initial state before collapsing
        final_state: The final state after collapsing

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        logger.debug(f"Running reward function on state: {final_state}")

        # Check: sidebarCollapsed should be true
        sidebar_collapsed = final_state.get("sidebarCollapsed")
        if not sidebar_collapsed:
            return (
                0.0,
                f"Expected sidebarCollapsed to be true, got '{sidebar_collapsed}'",
            )

        return 1.0, "Successfully collapsed the navigation sidebar"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


# Registry of all Outlook reward functions
REWARD_FUNCTIONS_OUTLOOK = {
    "_validate_go_to_the_drafts_page": _validate_go_to_the_drafts_page,
    "_validate_go_to_the_sent_items_page": _validate_go_to_the_sent_items_page,
    "_validate_open_an_email_from_the_list": _validate_open_an_email_from_the_list,
    "_validate_delete_an_email_from_the_list": _validate_delete_an_email_from_the_list,
    "_validate_flag_an_email": _validate_flag_an_email,
    "_validate_pin_an_email": _validate_pin_an_email,
    "_validate_toggle_read_on_an_email": _validate_toggle_read_on_an_email,
    "_validate_toggle_unread_on_an_email": _validate_toggle_unread_on_an_email,
    "_validate_compose_a_new_draft": _validate_compose_a_new_draft,
    "_validate_fill_draft_fields": _validate_fill_draft_fields,
    "_validate_send_the_draft": _validate_send_the_draft,
    "_validate_discard_a_draft": _validate_discard_a_draft,
    "_validate_type_to_show_search_suggestions": _validate_type_to_show_search_suggestions,
    "_validate_submit_a_search_with_enter": _validate_submit_a_search_with_enter,
    "_validate_open_an_email_from_the_search_dropdown": _validate_open_an_email_from_the_search_dropdown,
    "_validate_apply_the_has_attachments_filter": _validate_apply_the_has_attachments_filter,
    "_validate_apply_the_unread_search_filter": _validate_apply_the_unread_search_filter,
    "_validate_choose_sent_items_from_the_folder_selector": _validate_choose_sent_items_from_the_folder_selector,
    "_validate_collapse_the_favorites_section": _validate_collapse_the_favorites_section,
    "_validate_expand_the_navigation_sidebar": _validate_expand_the_navigation_sidebar,
    "_validate_collapse_the_navigation_sidebar": _validate_collapse_the_navigation_sidebar,
}

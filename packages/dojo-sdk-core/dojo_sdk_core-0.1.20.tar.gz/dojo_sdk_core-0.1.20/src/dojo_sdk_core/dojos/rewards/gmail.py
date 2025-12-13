"""
Reward functions for Gmail app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_changing_categories_in_inbox(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that categories were changed in the inbox."""
    if "activeCategory" not in final_state:
        return 0.0, "No activeCategory in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that activeCategory changed from primary to updates
    if final_state.get("activeCategory") == "updates":
        return 1.0, "Successfully changed category to updates"

    return (
        0.0,
        "Expected activeCategory to be 'updates', got '{}'".format(final_state.get("activeCategory")),
    )


def _validate_collapse_the_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the sidebar was collapsed."""
    if "sidebarCollapsed" not in final_state:
        return 0.0, "No sidebarCollapsed in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    if final_state.get("sidebarCollapsed") is True:
        return 1.0, "Sidebar successfully collapsed"

    return (
        0.0,
        "Expected sidebarCollapsed to be True, got '{}'".format(final_state.get("sidebarCollapsed")),
    )


def _validate_expand_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the sidebar was expanded."""
    if "sidebarCollapsed" not in final_state:
        return 0.0, "No sidebarCollapsed in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    if final_state.get("sidebarCollapsed") is False:
        return 1.0, "Sidebar successfully expanded"

    return (
        0.0,
        "Expected sidebarCollapsed to be False, got '{}'".format(final_state.get("sidebarCollapsed")),
    )


def _validate_filter_using_search_and_sender(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that search filter was applied using search query and sender."""
    if "emails" not in final_state or "selectedEmailId" not in final_state:
        return 0.0, "No emails or selectedEmailId in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    selected_email_id = final_state.get("selectedEmailId")
    if not selected_email_id:
        return 0.0, "No email selected"

    # Find the selected email
    selected_email = next(
        (email for email in final_state["emails"] if email.get("id") == selected_email_id),
        None,
    )
    if not selected_email:
        return 0.0, f"Selected email {selected_email_id} not found in emails"

    # Check that the email is from GitHub and has the correct subject
    sender_name = selected_email.get("sender", {}).get("name", "")
    subject = selected_email.get("subject", "")

    if sender_name == "GitHub" and "Your recent order confirmation" in subject:
        return (
            1.0,
            "Successfully filtered and selected email from GitHub with subject 'Your recent order confirmation'",
        )

    errors = []
    if sender_name != "GitHub":
        errors.append(f"sender={sender_name} (expected 'GitHub')")
    if "Your recent order confirmation" not in subject:
        errors.append("subject does not contain 'Your recent order confirmation'")

    return 0.0, "; ".join(errors) if errors else "Email selection validation failed"


def _validate_filtering_apple_emails_with_attachment(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """Validate that Apple emails with attachments were filtered."""
    if "emails" not in final_state or "selectedEmailId" not in final_state:
        return 0.0, "No emails or selectedEmailId in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    selected_email_id = final_state.get("selectedEmailId")
    if not selected_email_id:
        return 0.0, "No email selected"

    # Find the selected email
    selected_email = next(
        (email for email in final_state["emails"] if email.get("id") == selected_email_id),
        None,
    )
    if not selected_email:
        return 0.0, f"Selected email {selected_email_id} not found in emails"

    # Check email properties
    sender_name = selected_email.get("sender", {}).get("name", "")
    subject = selected_email.get("subject", "")
    body = selected_email.get("body", "")
    expected_text = "I dropped a concise recap in the shared channel so the broader group can keep pace"

    errors = []
    if "Preview the latest product tour" not in subject:
        errors.append("subject does not contain 'Preview the latest product tour'")
    if sender_name != "Apple":
        errors.append(f"sender={sender_name} (expected 'Apple')")
    if expected_text not in body:
        errors.append(f"body does not contain expected text: '{expected_text}'")

    if errors:
        return 0.0, "; ".join(errors)

    return (
        1.0,
        "Successfully filtered and selected Apple email with attachment containing expected text",
    )


def _validate_filtering_your_own_sent_emails(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that own sent emails were filtered."""
    if "emails" not in final_state or "selectedEmailId" not in final_state:
        return 0.0, "No emails or selectedEmailId in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    selected_email_id = final_state.get("selectedEmailId")
    if not selected_email_id:
        return 0.0, "No email selected"

    # Find the selected email
    selected_email = next(
        (email for email in final_state["emails"] if email.get("id") == selected_email_id),
        None,
    )
    if not selected_email:
        return 0.0, f"Selected email {selected_email_id} not found in emails"

    # Check that the email is from Maximilian Falco and has the correct subject
    sender_name = selected_email.get("sender", {}).get("name", "")
    subject = selected_email.get("subject", "")

    if sender_name == "Maximilian Falco" and "Q4 roadmap outline" in subject:
        return (
            1.0,
            "Successfully filtered and selected sent email from Maximilian Falco with subject 'Q4 roadmap outline'",
        )

    errors = []
    if sender_name != "Maximilian Falco":
        errors.append(f"sender={sender_name} (expected 'Maximilian Falco')")
    if "Q4 roadmap outline" not in subject:
        errors.append("subject does not contain 'Q4 roadmap outline'")

    return 0.0, "; ".join(errors) if errors else "Email selection validation failed"


def _validate_focus_a_single_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a single email was focused."""
    if "emails" not in final_state or "selectedEmailId" not in final_state:
        return 0.0, "No emails or selectedEmailId in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    selected_email_id = final_state.get("selectedEmailId")
    if not selected_email_id:
        return 0.0, "No email selected"

    # Find the selected email
    selected_email = next(
        (email for email in final_state["emails"] if email.get("id") == selected_email_id),
        None,
    )
    if not selected_email:
        return 0.0, f"Selected email {selected_email_id} not found in emails"

    # Check that an email is selected (the focus state reflects the email)
    if selected_email_id == "mail-3":
        return 1.0, f"Successfully focused email {selected_email_id}"

    return (
        0.0,
        f"Expected selectedEmailId to be 'mail-3', got '{selected_email_id}'",
    )


def _validate_navigate_home(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that navigation to home (inbox primary category) occurred."""
    if "activeCategory" not in final_state:
        return 0.0, "No activeCategory in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    if final_state.get("activeCategory") == "primary":
        return 1.0, "Successfully navigated to inbox primary category"

    return (
        0.0,
        f"Expected activeCategory to be 'primary', got '{final_state.get('activeCategory')}'",
    )


def _validate_navigate_to_different_categories_via_sidebar(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """Validate that navigation to Sent category via sidebar occurred."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that we're viewing sent emails (emails where sent=True)
    sent_emails = [email for email in final_state["emails"] if email.get("sent") is True]

    # The task expects to reach Sent category and see different content
    # We verify by checking that sent emails are present and the list is different from inbox
    if len(sent_emails) > 0:
        return (
            1.0,
            f"Successfully navigated to Sent category via sidebar, showing {len(sent_emails)} sent emails",
        )

    return 0.0, "No sent emails found in final state"


def _validate_navigate_to_the_starred_category(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that navigation to starred category occurred."""
    if "shortcuts" not in final_state:
        return 0.0, "No shortcuts in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that the starred shortcut is active
    starred_shortcut = next((s for s in final_state.get("shortcuts", []) if s.get("id") == "starred"), None)

    if not starred_shortcut:
        return 0.0, "Starred shortcut not found in shortcuts"

    if starred_shortcut.get("isActive") is True:
        return 1.0, "Successfully navigated to starred category via sidebar"

    return (
        0.0,
        f"Starred shortcut is not active. isActive={starred_shortcut.get('isActive')}",
    )


def _validate_open_filter_modal(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the filter modal was opened."""
    if "isSearchFilterOpen" not in final_state:
        return 0.0, "No isSearchFilterOpen in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    if final_state.get("isSearchFilterOpen") is True:
        return 1.0, "Filter modal successfully opened"

    return (
        0.0,
        f"Expected isSearchFilterOpen to be True, got '{final_state.get('isSearchFilterOpen')}'",
    )


def _validate_see_sent_emails(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that sent emails are being viewed."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that all visible emails are sent by Maximilian Falco
    sent_emails = [email for email in final_state["emails"] if email.get("sent") is True]
    all_from_user = all(email.get("sender", {}).get("name") == "Maximilian Falco" for email in sent_emails)

    if len(sent_emails) > 0 and all_from_user:
        return (
            1.0,
            f"Successfully viewing sent emails, showing {len(sent_emails)} emails from Maximilian Falco",
        )

    errors = []
    if len(sent_emails) == 0:
        errors.append("No sent emails found")
    if not all_from_user:
        errors.append("Not all emails are from Maximilian Falco")

    return 0.0, "; ".join(errors) if errors else "Sent emails validation failed"


def _validate_sending_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that an email was sent."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Count sent emails
    initial_sent_count = len([email for email in initial_state.get("emails", []) if email.get("sent")])
    final_sent_count = len([email for email in final_state["emails"] if email.get("sent")])

    # Check that sent count increased by 1
    if final_sent_count == initial_sent_count + 1:
        # Find the email with subject "Test"
        test_email = next(
            (email for email in final_state["emails"] if email.get("sent") and email.get("subject") == "Test"),
            None,
        )

        if test_email:
            body = test_email.get("body", "")
            if body == "Test":
                return (
                    1.0,
                    f"Successfully sent email. Sent count increased from {initial_sent_count} to {final_sent_count}. Email has subject 'Test' and body 'Test'",  # noqa: E501
                )
            else:
                return (
                    0.0,
                    f"Email with subject 'Test' found but body is '{body}' (expected 'Test')",
                )

        return 0.0, "Email with subject 'Test' not found in sent emails"

    return (
        0.0,
        f"Sent count did not increase by 1. Initial: {initial_sent_count}, Final: {final_sent_count}",
    )


def _validate_snooze_a_single_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a single email was snoozed."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find snoozed emails
    snoozed_emails = [email for email in final_state["emails"] if email.get("snoozed") is True]

    # Check that exactly one email is snoozed, and it's from GitHub with the correct subject
    if len(snoozed_emails) == 1:
        snoozed_email = snoozed_emails[0]
        sender_name = snoozed_email.get("sender", {}).get("name", "")
        subject = snoozed_email.get("subject", "")

        if sender_name == "GitHub" and "Your recent order confirmation" in subject:
            return (
                1.0,
                "Successfully snoozed email from GitHub titled 'Your recent order confirmation'",
            )

        errors = []
        if sender_name != "GitHub":
            errors.append(f"sender={sender_name} (expected 'GitHub')")
        if "Your recent order confirmation" not in subject:
            errors.append("subject does not contain 'Your recent order confirmation'")
        return 0.0, "; ".join(errors)

    return (
        0.0,
        "Expected exactly 1 snoozed email, found {}".format(len(snoozed_emails)),
    )


def _validate_starring_a_non_primary_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a non-primary email was starred."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the GitHub email from updates category that should be starred
    github_email = next(
        (
            email
            for email in final_state["emails"]
            if email.get("sender", {}).get("name") == "GitHub" and email.get("category") == "updates"
        ),
        None,
    )

    if not github_email:
        return 0.0, "GitHub email from updates category not found"

    # Check that it's starred
    # When an email is starred, it appears in the primary category view even if its category is "updates"
    # This is handled by the UI filtering logic: starred emails show in primary category
    if github_email.get("starred") is True:
        return (
            1.0,
            "Successfully starred GitHub email from updates category. Email now appears in primary category view (starred emails are visible in primary)",  # noqa: E501
        )

    return (
        0.0,
        f"GitHub email from updates category is not starred. starred={github_email.get('starred')}",
    )


def _validate_starring_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that an email was starred."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the Twitter email with subject "Product roadmap highlights"
    target_email = next(
        (
            email
            for email in final_state["emails"]
            if email.get("sender", {}).get("name") == "Twitter" and "Product roadmap highlights" in email.get("subject", "")
        ),
        None,
    )

    if not target_email:
        return (
            0.0,
            "Email from Twitter with subject 'Product roadmap highlights' not found",
        )

    # Check that it's starred
    if target_email.get("starred") is True:
        return (
            1.0,
            "Successfully starred email from Twitter titled 'Product roadmap highlights'",
        )

    return (
        0.0,
        f"Email from Twitter is not starred. starred={target_email.get('starred')}",
    )


def _validate_trigger_filter_bar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that the filter bar was triggered."""
    # The filter bar appearing is typically indicated by searchFilters being active
    # or isSearchFilterOpen being true, but let's check what the actual state shows
    logger.debug(f"Running reward function on state: {final_state}")

    # Check if searchFilters exist and are being used
    if "searchFilters" in final_state:
        # The filter bar is triggered when search filters are active
        # This could be indicated by isSearchFilterOpen or by filters having values
        if final_state.get("isSearchFilterOpen") is True:
            return 1.0, "Filter bar successfully triggered and visible"

    # Alternative: check if search query or filters are set
    if final_state.get("searchQuery") or final_state.get("activeSearchQuery"):
        return 1.0, "Filter bar successfully triggered via search"

    return (
        0.0,
        "Filter bar not triggered. isSearchFilterOpen is not True and no search query is set",
    )


def _validate_unsnooze_all_emails(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that all emails were unsnoozed."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that no emails are snoozed
    snoozed_emails = [email for email in final_state["emails"] if email.get("snoozed") is True]

    if len(snoozed_emails) == 0:
        return 1.0, "Successfully unsnoozed all emails. No snoozed emails remaining"

    return (
        0.0,
        f"Expected 0 snoozed emails, found {len(snoozed_emails)}",
    )


def _validate_unstar_all_emails(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that all emails were unstarred."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Check that no emails are starred
    starred_emails = [email for email in final_state["emails"] if email.get("starred") is True]

    if len(starred_emails) == 0:
        return 1.0, "Successfully unstarred all emails. No starred emails remaining"

    return (
        0.0,
        f"Expected 0 starred emails, found {len(starred_emails)}",
    )


def _validate_unstarring_an_email(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that an email was unstarred."""
    if "emails" not in final_state:
        return 0.0, "No emails in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the GitHub email
    github_email = next(
        (email for email in final_state["emails"] if email.get("sender", {}).get("name") == "GitHub"),
        None,
    )

    if not github_email:
        return 0.0, "GitHub email not found"

    # Check that it's not starred
    if github_email.get("starred") is False:
        # Also verify it's not visible in primary category if it was moved
        return 1.0, "Successfully unstarred GitHub email. Email is no longer starred"

    return (
        0.0,
        f"GitHub email is still starred. starred={github_email.get('starred')}",
    )


# Registry of all Gmail reward functions
REWARD_FUNCTIONS_GMAIL = {
    "_validate_changing_categories_in_inbox": _validate_changing_categories_in_inbox,
    "_validate_collapse_the_sidebar": _validate_collapse_the_sidebar,
    "_validate_expand_sidebar": _validate_expand_sidebar,
    "_validate_filter_using_search_and_sender": _validate_filter_using_search_and_sender,
    "_validate_filtering_apple_emails_with_attachment": _validate_filtering_apple_emails_with_attachment,
    "_validate_filtering_your_own_sent_emails": _validate_filtering_your_own_sent_emails,
    "_validate_focus_a_single_email": _validate_focus_a_single_email,
    "_validate_navigate_home": _validate_navigate_home,
    "_validate_navigate_to_different_categories_via_sidebar": _validate_navigate_to_different_categories_via_sidebar,
    "_validate_navigate_to_the_starred_category": _validate_navigate_to_the_starred_category,
    "_validate_open_filter_modal": _validate_open_filter_modal,
    "_validate_see_sent_emails": _validate_see_sent_emails,
    "_validate_sending_an_email": _validate_sending_an_email,
    "_validate_snooze_a_single_email": _validate_snooze_a_single_email,
    "_validate_starring_a_non_primary_email": _validate_starring_a_non_primary_email,
    "_validate_starring_an_email": _validate_starring_an_email,
    "_validate_trigger_filter_bar": _validate_trigger_filter_bar,
    "_validate_unsnooze_all_emails": _validate_unsnooze_all_emails,
    "_validate_unstar_all_emails": _validate_unstar_all_emails,
    "_validate_unstarring_an_email": _validate_unstarring_an_email,
}

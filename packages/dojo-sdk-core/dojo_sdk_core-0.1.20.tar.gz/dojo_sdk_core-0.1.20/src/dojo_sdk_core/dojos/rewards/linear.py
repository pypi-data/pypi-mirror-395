"""
Reward functions for Linear app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_drag_to_different_column(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that an issue was moved to a different column."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the issue we're tracking (VSS-101)
    target_issue = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-101"), None)

    if not target_issue:
        return 0.0, "Target issue VSS-101 not found in final state"

    # Check if it moved to in_progress status
    if target_issue.get("status") == "in_progress" and target_issue.get("assigneeId") == "1":
        return 1.0, "Issue VSS-101 successfully moved to In Progress column for user 1"

    return (
        0.0,
        f"Issue VSS-101 has status={target_issue.get('status')}, "
        f"assigneeId={target_issue.get('assigneeId')}, expected status=in_progress, assigneeId=1",
    )


def _validate_drag_two_issues_same_user(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that two issues were moved within the same user's board."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find both target issues
    issue_101 = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-101"), None)
    issue_106 = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-106"), None)

    if not issue_101:
        return 0.0, "Target issue VSS-101 not found in final state"
    if not issue_106:
        return 0.0, "Target issue VSS-106 not found in final state"

    # Check both issues
    issue_101_correct = issue_101.get("status") == "in_progress" and issue_101.get("assigneeId") == "1"
    issue_106_correct = issue_106.get("status") == "queued" and issue_106.get("assigneeId") == "1"

    if issue_101_correct and issue_106_correct:
        return 1.0, "Both issues successfully moved to target columns for user 1"

    errors = []
    if not issue_101_correct:
        errors.append(
            f"VSS-101: status={issue_101.get('status')}, assigneeId={issue_101.get('assigneeId')} (expected in_progress, 1)"
        )
    if not issue_106_correct:
        errors.append(
            f"VSS-106: status={issue_106.get('status')}, assigneeId={issue_106.get('assigneeId')} (expected queued, 1)"
        )

    return 0.0, "; ".join(errors)


def _validate_create_new_issue(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a new issue was created with correct properties."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find issue by title
    target_issue = next(
        (issue for issue in final_state["issues"] if issue.get("title") == "Implement user authentication system"), None
    )

    if not target_issue:
        return 0.0, "Issue with title 'Implement user authentication system' not found in final state"

    # Validate properties
    errors = []

    if target_issue.get("assigneeId") != "2":
        errors.append(f"assigneeId={target_issue.get('assigneeId')} (expected '2')")

    if target_issue.get("priority") != "high":
        errors.append(f"priority={target_issue.get('priority')} (expected 'high')")

    description = target_issue.get("description", "")
    if "JWT-based authentication" not in description:
        errors.append("description does not contain 'JWT-based authentication'")

    if errors:
        return 0.0, "; ".join(errors)

    return 1.0, "Issue successfully created with correct properties"


def _validate_drag_and_reassign_issue(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that issue VSS-106 was dragged to different status and assignee."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the target issue
    target_issue = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-106"), None)

    if not target_issue:
        return 0.0, "Target issue VSS-106 not found in final state"

    # Check if it has correct status and assigneeId
    if target_issue.get("status") == "in_progress" and target_issue.get("assigneeId") == "2":
        return 1.0, "Issue VSS-106 successfully moved to In Progress column for Chen (assigneeId=2)"

    return (
        0.0,
        f"Issue VSS-106 has status={target_issue.get('status')}, "
        f"assigneeId={target_issue.get('assigneeId')}, expected status=in_progress, assigneeId=2",
    )


def _validate_update_issue_properties(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that issue VSS-105 has updated priority and label."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find the target issue
    target_issue = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-105"), None)

    if not target_issue:
        return 0.0, "Target issue VSS-105 not found in final state"

    # Validate properties
    errors = []

    if target_issue.get("priority") != "urgent":
        errors.append(f"priority={target_issue.get('priority')} (expected 'urgent')")

    labels = target_issue.get("labels", [])
    has_operations_label = any(label.get("id") == "label2" for label in labels)
    if not has_operations_label:
        errors.append("Operations label (id='label2') not found in labels array")

    if errors:
        return 0.0, "; ".join(errors)

    return 1.0, "Issue VSS-105 successfully updated with urgent priority and Operations label"


def _validate_multi_issue_reorganization(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that three issues were reorganized to different columns and assignees."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find all three target issues
    issue_101 = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-101"), None)
    issue_102 = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-102"), None)
    issue_103 = next((issue for issue in final_state["issues"] if issue.get("identifier") == "VSS-103"), None)

    if not issue_101:
        return 0.0, "Target issue VSS-101 not found in final state"
    if not issue_102:
        return 0.0, "Target issue VSS-102 not found in final state"
    if not issue_103:
        return 0.0, "Target issue VSS-103 not found in final state"

    # Check all issues
    issue_101_correct = issue_101.get("status") == "in_progress" and issue_101.get("assigneeId") == "2"
    issue_102_correct = issue_102.get("status") == "blocked" and issue_102.get("assigneeId") == "3"
    issue_103_correct = issue_103.get("status") == "in_review" and issue_103.get("assigneeId") == "1"

    if issue_101_correct and issue_102_correct and issue_103_correct:
        return 1.0, "All three issues successfully reorganized to target columns and assignees"

    errors = []
    if not issue_101_correct:
        errors.append(
            f"VSS-101: status={issue_101.get('status')}, assigneeId={issue_101.get('assigneeId')} (expected in_progress, 2)"
        )
    if not issue_102_correct:
        errors.append(
            f"VSS-102: status={issue_102.get('status')}, assigneeId={issue_102.get('assigneeId')} (expected blocked, 3)"
        )
    if not issue_103_correct:
        errors.append(
            f"VSS-103: status={issue_103.get('status')}, assigneeId={issue_103.get('assigneeId')} (expected in_review, 1)"
        )

    return 0.0, "; ".join(errors)


def _validate_complete_issue_workflow(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """Validate that a complete issue workflow was executed."""
    if "issues" not in final_state:
        return 0.0, "No issues in final state"

    logger.debug(f"Running reward function on state: {final_state}")

    # Find issue by title
    target_issue = next(
        (issue for issue in final_state["issues"] if issue.get("title") == "Fix critical database connection bug"), None
    )

    if not target_issue:
        return 0.0, "Issue with title 'Fix critical database connection bug' not found in final state"

    # Validate all properties
    errors = []

    if target_issue.get("priority") != "high":
        errors.append(f"priority={target_issue.get('priority')} (expected 'high')")

    if target_issue.get("assigneeId") != "2":
        errors.append(f"assigneeId={target_issue.get('assigneeId')} (expected '2')")

    if target_issue.get("status") != "in_progress":
        errors.append(f"status={target_issue.get('status')} (expected 'in_progress')")

    labels = target_issue.get("labels", [])
    has_bug_label = any(label.get("id") == "label1" for label in labels)
    if not has_bug_label:
        errors.append("Bug label (id='label1') not found in labels array")

    comments = target_issue.get("comments", [])
    has_comment = any("Starting investigation" in comment.get("text", "") for comment in comments)
    if not has_comment:
        errors.append("Comment containing 'Starting investigation' not found")

    if errors:
        return 0.0, "; ".join(errors)

    return 1.0, "Complete issue workflow successfully executed"


# Registry of all Linear reward functions
REWARD_FUNCTIONS_LINEAR = {
    "_validate_drag_to_different_column": _validate_drag_to_different_column,
    "_validate_drag_two_issues_same_user": _validate_drag_two_issues_same_user,
    "_validate_create_new_issue": _validate_create_new_issue,
    "_validate_drag_and_reassign_issue": _validate_drag_and_reassign_issue,
    "_validate_update_issue_properties": _validate_update_issue_properties,
    "_validate_multi_issue_reorganization": _validate_multi_issue_reorganization,
    "_validate_complete_issue_workflow": _validate_complete_issue_workflow,
}

"""
Salesforce reward functions for CRM task validation.

This module contains reward validation functions for Salesforce CRM tasks,
particularly for complex workflows like lead conversion.
"""

from typing import Any, Dict, Tuple


def _validate_salesforce_convert_lead(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that a lead has been successfully converted to a contact.

    This function checks:
    1. The active tab is the leads list page
    2. The lead has status 'Converted' and a convertedToContactId
    3. A new contact exists with the lead's information (name: Michael Brown)

    Args:
        initial_state: The initial state before the conversion
        final_state: The final state after the conversion

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Check 1: Active tab should be the leads list page
        active_tab_id = final_state.get("activeTabId")
        if active_tab_id != "home-listLeads":
            return 0.0, f"Expected activeTabId to be 'home-listLeads', got '{active_tab_id}'"

        # Check 2: Lead should be marked as converted
        leads = final_state.get("leads", [])
        if not leads:
            return 0.0, "No leads found in final state"

        # Find the lead (should be lead-001)
        lead = None
        for temp_lead in leads:
            if temp_lead.get("id") == "lead-001":
                lead = temp_lead
                break

        if not lead:
            return 0.0, "Lead with id 'lead-001' not found"

        # Check lead status and convertedToContactId
        lead_status = lead.get("leadStatus")
        converted_to_contact_id = lead.get("convertedToContactId")

        if lead_status != "Converted":
            return 0.0, f"Expected leadStatus to be 'Converted', got '{lead_status}'"

        if not converted_to_contact_id:
            return 0.0, "Expected convertedToContactId to be set, but it's missing"

        # Check 3: Contact should exist with the lead's information
        contacts = final_state.get("contacts", [])
        if not contacts:
            return 0.0, "No contacts found in final state"

        # Find the contact by the convertedToContactId
        contact = None
        for c in contacts:
            if c.get("id") == converted_to_contact_id:
                contact = c
                break

        if not contact:
            return 0.0, f"Contact with id '{converted_to_contact_id}' not found"

        # Verify the contact has the correct information (name should be Michael Brown)
        contact_name = contact.get("name")
        if contact_name != "Michael Brown":
            return 0.0, f"Expected contact name to be 'Michael Brown', got '{contact_name}'"

        # Additional validation: check that contact has the lead's company
        contact_company = contact.get("company")
        lead_company = lead.get("company")
        if contact_company != lead_company:
            return 0.0, f"Contact company '{contact_company}' doesn't match lead company '{lead_company}'"

        # All checks passed
        return 1.0, "Lead successfully converted to contact with correct information"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_salesforce_create_and_convert_lead(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that a lead has been created and successfully converted to a contact.

    This function checks:
    1. The active tab is the leads list page
    2. A lead exists with name 'Robert Taylor' and status 'Converted'
    3. The lead has a convertedToContactId set
    4. A new contact exists with the lead's information
    5. The contact has the correct name and company

    Args:
        initial_state: The initial state before the creation and conversion
        final_state: The final state after the creation and conversion

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Check 1: Active tab should be the leads list page
        active_tab_id = final_state.get("activeTabId")
        if active_tab_id != "home-listLeads":
            return 0.0, f"Expected activeTabId to be 'home-listLeads', got '{active_tab_id}'"

        # Check 2: Lead should exist and be marked as converted
        leads = final_state.get("leads", [])
        if not leads:
            return 0.0, "No leads found in final state"

        # Find the lead with name 'Robert Taylor'
        robert_lead = None
        for lead in leads:
            if lead.get("name") == "Robert Taylor":
                robert_lead = lead
                break

        if not robert_lead:
            return 0.0, "Lead with name 'Robert Taylor' not found"

        # Check lead status and convertedToContactId
        lead_status = robert_lead.get("leadStatus")
        converted_to_contact_id = robert_lead.get("convertedToContactId")

        if lead_status != "Converted":
            return 0.0, f"Expected leadStatus to be 'Converted', got '{lead_status}'"

        if not converted_to_contact_id:
            return 0.0, "Expected convertedToContactId to be set, but it's missing"

        # Check 3: Contact should exist with the lead's information
        contacts = final_state.get("contacts", [])
        if not contacts:
            return 0.0, "No contacts found in final state"

        # Find the contact by the convertedToContactId
        contact = None
        for c in contacts:
            if c.get("id") == converted_to_contact_id:
                contact = c
                break

        if not contact:
            return 0.0, f"Contact with id '{converted_to_contact_id}' not found"

        # Verify the contact has the correct information
        contact_name = contact.get("name")
        if contact_name != "Robert Taylor":
            return 0.0, f"Expected contact name to be 'Robert Taylor', got '{contact_name}'"

        # Check that contact has the lead's company
        contact_company = contact.get("company")
        lead_company = robert_lead.get("company")
        if contact_company != lead_company:
            return 0.0, f"Contact company '{contact_company}' doesn't match lead company '{lead_company}'"

        # Additional validation: check that contact has the lead's email
        contact_email = contact.get("email")
        lead_email = robert_lead.get("email")
        if contact_email != lead_email:
            return 0.0, f"Contact email '{contact_email}' doesn't match lead email '{lead_email}'"

        # Verify the lead was created from scratch (not in initial state)
        initial_leads = initial_state.get("leads", [])
        initial_robert_exists = any(lead.get("name") == "Robert Taylor" for lead in initial_leads)
        if initial_robert_exists:
            return 0.0, "Lead 'Robert Taylor' already existed in initial state - should be newly created"

        # All checks passed
        return 1.0, "Lead 'Robert Taylor' successfully created and converted to contact with correct information"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_salesforce_create_new_lead(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that a new lead has been successfully created.

    This function checks:
    1. The active tab is a lead details page
    2. A lead exists with name 'Jane Smith' and company 'Innovation Labs'
    3. The lead was not in the initial state (proves it was created)

    Args:
        initial_state: The initial state before the lead creation
        final_state: The final state after the lead creation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Check 1: Active tab should be a lead details page
        active_tab_id = final_state.get("activeTabId")
        if not active_tab_id or not active_tab_id.startswith("lead-"):
            return 0.0, f"Expected activeTabId to start with 'lead-', got '{active_tab_id}'"

        # Check 2: Lead should exist with correct information
        leads = final_state.get("leads", [])
        if not leads:
            return 0.0, "No leads found in final state"

        # Find the lead with name 'Jane Smith'
        jane_lead = None
        for lead in leads:
            if lead.get("name") == "Jane Smith":
                jane_lead = lead
                break

        if not jane_lead:
            return 0.0, "Lead with name 'Jane Smith' not found"

        # Check company
        if jane_lead.get("company") != "Innovation Labs":
            return 0.0, f"Expected company to be 'Innovation Labs', got '{jane_lead.get('company')}'"

        # Check 3: Verify the lead was created from scratch
        initial_leads = initial_state.get("leads", [])
        initial_jane_exists = any(lead.get("name") == "Jane Smith" for lead in initial_leads)
        if initial_jane_exists:
            return 0.0, "Lead 'Jane Smith' already existed in initial state - should be newly created"

        # All checks passed
        return 1.0, "Lead 'Jane Smith' successfully created with correct information"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_salesforce_create_new_case(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that a new case has been successfully created.

    This function checks:
    1. The active tab is a case details page
    2. A case exists with subject 'Technical support request'
    3. The case was not in the initial state (proves it was created)

    Args:
        initial_state: The initial state before the case creation
        final_state: The final state after the case creation

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Check 1: Active tab should be a case details page
        active_tab_id = final_state.get("activeTabId")
        if not active_tab_id or not active_tab_id.startswith("case-"):
            return 0.0, f"Expected activeTabId to start with 'case-', got '{active_tab_id}'"

        # Check 2: Case should exist with correct subject
        cases = final_state.get("cases", [])
        if not cases:
            return 0.0, "No cases found in final state"

        # Find the case with subject 'Technical support request'
        support_case = None
        for case in cases:
            if case.get("subject") == "Technical support request":
                support_case = case
                break

        if not support_case:
            return 0.0, "Case with subject 'Technical support request' not found"

        # Check 3: Verify the case was created from scratch
        initial_cases = initial_state.get("cases", [])
        initial_case_exists = any(case.get("subject") == "Technical support request" for case in initial_cases)
        if initial_case_exists:
            return 0.0, "Case 'Technical support request' already existed in initial state - should be newly created"

        # All checks passed
        return 1.0, "Case 'Technical support request' successfully created"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_salesforce_edit_lead_inline(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that a lead's title has been successfully edited inline.

    This function checks:
    1. Lead with id 'lead-001' exists
    2. The lead's title has been changed from 'VP of Sales' to 'Senior VP of Sales'
    3. Other lead fields remain unchanged

    Args:
        initial_state: The initial state before the edit
        final_state: The final state after the edit

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Get the lead from both states
        initial_leads = initial_state.get("leads", [])
        final_leads = final_state.get("leads", [])

        initial_lead = None
        for lead in initial_leads:
            if lead.get("id") == "lead-001":
                initial_lead = lead
                break

        final_lead = None
        for lead in final_leads:
            if lead.get("id") == "lead-001":
                final_lead = lead
                break

        if not initial_lead:
            return 0.0, "Lead 'lead-001' not found in initial state"

        if not final_lead:
            return 0.0, "Lead 'lead-001' not found in final state"

        # Check that title was updated correctly
        if initial_lead.get("title") != "VP of Sales":
            return 0.0, f"Initial title should be 'VP of Sales', got '{initial_lead.get('title')}'"

        if final_lead.get("title") != "Senior VP of Sales":
            return 0.0, f"Expected title to be 'Senior VP of Sales', got '{final_lead.get('title')}'"

        # Check that other important fields remain unchanged
        fields_to_check = ["name", "company", "email", "phone", "leadStatus"]
        for field in fields_to_check:
            if initial_lead.get(field) != final_lead.get(field):
                return 0.0, f"Field '{field}' should not have changed, but it did"

        # All checks passed
        return 1.0, "Lead title successfully updated to 'Senior VP of Sales'"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


def _validate_salesforce_create_and_close_case(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that a case has been created and successfully closed.

    This function checks:
    1. The active tab is still a case details page
    2. A case exists with subject 'Customer complaint resolved' and status 'Closed'
    3. The case was not in the initial state (proves it was created)

    Args:
        initial_state: The initial state before the case creation and closure
        final_state: The final state after the case creation and closure

    Returns:
        Tuple of (score, reason) where score is 1.0 for success, 0.0 for failure
    """
    try:
        # Check 1: Active tab should still be a case details page
        active_tab_id = final_state.get("activeTabId")
        if not active_tab_id or not active_tab_id.startswith("case-"):
            return 0.0, f"Expected activeTabId to start with 'case-', got '{active_tab_id}'"

        # Check 2: Case should exist with correct subject and be closed
        cases = final_state.get("cases", [])
        if not cases:
            return 0.0, "No cases found in final state"

        # Find the case with subject 'Customer complaint resolved'
        complaint_case = None
        for case in cases:
            if case.get("subject") == "Customer complaint resolved":
                complaint_case = case
                break

        if not complaint_case:
            return 0.0, "Case with subject 'Customer complaint resolved' not found"

        # Check case status
        case_status = complaint_case.get("status")
        if case_status != "Closed":
            return 0.0, f"Expected case status to be 'Closed', got '{case_status}'"

        # Check 3: Verify the case was created from scratch
        initial_cases = initial_state.get("cases", [])
        initial_case_exists = any(case.get("subject") == "Customer complaint resolved" for case in initial_cases)
        if initial_case_exists:
            return 0.0, "Case 'Customer complaint resolved' already existed in initial state - should be newly created"

        # All checks passed
        return 1.0, "Case 'Customer complaint resolved' successfully created and closed"

    except Exception as e:
        return 0.0, f"Error during validation: {str(e)}"


# Registry of Salesforce reward functions
REWARD_FUNCTIONS_SALESFORCE = {
    "_validate_salesforce_convert_lead": _validate_salesforce_convert_lead,
    "_validate_salesforce_create_and_convert_lead": _validate_salesforce_create_and_convert_lead,
    "_validate_salesforce_create_new_lead": _validate_salesforce_create_new_lead,
    "_validate_salesforce_create_new_case": _validate_salesforce_create_new_case,
    "_validate_salesforce_edit_lead_inline": _validate_salesforce_edit_lead_inline,
    "_validate_salesforce_create_and_close_case": _validate_salesforce_create_and_close_case,
}

__all__ = [
    "REWARD_FUNCTIONS_SALESFORCE",
    "_validate_salesforce_convert_lead",
    "_validate_salesforce_create_and_convert_lead",
    "_validate_salesforce_create_new_lead",
    "_validate_salesforce_create_new_case",
    "_validate_salesforce_edit_lead_inline",
    "_validate_salesforce_create_and_close_case",
]

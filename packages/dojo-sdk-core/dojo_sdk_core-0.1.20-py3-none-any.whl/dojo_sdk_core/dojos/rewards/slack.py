"""
Reward functions for Slack app tasks.
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def _validate_navigate_to_search_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated to the search page with query 'coffee'.

    This function checks:
    1. The page is "SEARCH"
    2. The params.query is "coffee"
    3. The searchQuery is "coffee"
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: params.query should be "coffee"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "coffee":
        return 0.0, f"Expected params.query to be 'coffee', got '{query_param}'"

    # Check 3: searchQuery should be "coffee"
    search_query = final_state.get("searchQuery")
    if search_query != "coffee":
        return 0.0, f"Expected searchQuery to be 'coffee', got '{search_query}'"

    return 1.0, "Successfully navigated to search page with query 'coffee'"


def _validate_switch_to_different_channel(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully switched from #social channel to #all-slack channel.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-1" (all-slack)
    3. The currentDM is null (not viewing a DM)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-1" (all-slack)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-1":
        return 0.0, f"Expected currentChannel to be 'channel-1', got '{current_channel}'"

    # Check 3: currentDM should be null (not viewing a DM)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null, got '{current_dm}'"

    return 1.0, "Successfully switched to #all-slack channel"


def _validate_view_user_profile_from_message(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully opened Dzaka's user profile sidebar from a message.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. The showUserProfile is true
    4. The selectedUserId is "user-1" (Dzaka's user ID)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3', got '{current_channel}'"

    # Check 3: showUserProfile should be true
    show_user_profile = final_state.get("showUserProfile")
    if show_user_profile is not True:
        return 0.0, f"Expected showUserProfile to be true, got '{show_user_profile}'"

    # Check 4: selectedUserId should be "user-1" (Dzaka's user ID)
    selected_user_id = final_state.get("selectedUserId")
    if selected_user_id != "user-1":
        return 0.0, f"Expected selectedUserId to be 'user-1', got '{selected_user_id}'"

    return 1.0, "Successfully opened Dzaka's user profile sidebar from message"


def _validate_open_thread_panel_from_message(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully opened the thread panel from a message.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. The threadPanel.isOpen is true
    4. The threadPanel.parentMessageId is "msg-01" (the "Morning crew! Coffee walk at 10?" message)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3', got '{current_channel}'"

    # Check 3: threadPanel should exist
    thread_panel = final_state.get("threadPanel")
    if thread_panel is None:
        return 0.0, "Expected threadPanel to exist in final state"

    # Check 4: threadPanel.isOpen should be true
    is_open = thread_panel.get("isOpen")
    if is_open is not True:
        return 0.0, f"Expected threadPanel.isOpen to be true, got '{is_open}'"

    # Check 5: threadPanel.parentMessageId should be "msg-01"
    parent_message_id = thread_panel.get("parentMessageId")
    if parent_message_id != "msg-01":
        return 0.0, f"Expected threadPanel.parentMessageId to be 'msg-01', got '{parent_message_id}'"

    return 1.0, "Successfully opened thread panel for message 'Morning crew! Coffee walk at 10?'"


def _validate_navigate_from_direct_message_to_channel(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from a direct message to a channel.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. The currentDM is null (not viewing a DM)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3', got '{current_channel}'"

    # Check 3: currentDM should be null (not viewing a DM)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null, got '{current_dm}'"

    return 1.0, "Successfully navigated from direct message to #social channel"


def _validate_switch_search_filter_to_people(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully switched the search mode from "Messages" to "People".

    This function checks:
    1. The page is "SEARCH"
    2. The searchFilters.mode is "people"
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchFilters should exist
    search_filters = final_state.get("searchFilters")
    if search_filters is None:
        return 0.0, "Expected searchFilters to exist in final state"

    # Check 3: searchFilters.mode should be "people"
    search_mode = search_filters.get("mode")
    if search_mode != "people":
        return 0.0, f"Expected searchFilters.mode to be 'people', got '{search_mode}'"

    return 1.0, "Successfully switched search mode to 'People'"


def _validate_search_and_open_message_result(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully searched for a message and clicked on a search result.

    This function checks:
    1. The page is "SEARCH"
    2. The searchQuery is "vanta"
    3. The params.query is "vanta"
    4. The searchSelection is set to a message (type: "message", messageId: "msg-05")
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchQuery should be "vanta"
    search_query = final_state.get("searchQuery")
    if search_query != "vanta":
        return 0.0, f"Expected searchQuery to be 'vanta', got '{search_query}'"

    # Check 3: params.query should be "vanta"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "vanta":
        return 0.0, f"Expected params.query to be 'vanta', got '{query_param}'"

    # Check 4: searchSelection should exist and be a message selection
    search_selection = final_state.get("searchSelection")
    if search_selection is None:
        return 0.0, "Expected searchSelection to be set, got null"

    # Check 5: searchSelection.type should be "message"
    selection_type = search_selection.get("type")
    if selection_type != "message":
        return 0.0, f"Expected searchSelection.type to be 'message', got '{selection_type}'"

    # Check 6: searchSelection.messageId should be "msg-05" (the message from Alistair containing "vanta")
    message_id = search_selection.get("messageId")
    if message_id != "msg-05":
        return 0.0, f"Expected searchSelection.messageId to be 'msg-05', got '{message_id}'"

    return 1.0, "Successfully searched for 'vanta' and opened message result in thread panel"


def _validate_send_message_in_channel(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully sent a message in the channel.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. A new message exists in the messages array with:
       - channelId: "channel-3"
       - userId: "user-1" (the current user Dzaka)
       - content: "Thanks for sharing the recipe!"
    4. The messageInputValue is empty (message was sent)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3', got '{current_channel}'"

    # Check 3: messages array should exist
    messages = final_state.get("messages", [])
    if not isinstance(messages, list):
        return 0.0, "Expected messages to be an array"

    # Check 4: Find a message in channel-3 from user-1 with the expected content
    target_message = None
    for message in messages:
        if (
            message.get("channelId") == "channel-3"
            and message.get("userId") == "user-1"
            and message.get("content") == "Thanks for sharing the recipe!"
        ):
            target_message = message
            break

    if target_message is None:
        return 0.0, "Expected to find a new message with content 'Thanks for sharing the recipe!' from user-1 in channel-3"

    # Check 5: The message should have a valid id and timestamp
    message_id = target_message.get("id")
    if not message_id:
        return 0.0, "Expected the new message to have an id"

    message_timestamp = target_message.get("timestamp")
    if not message_timestamp:
        return 0.0, "Expected the new message to have a timestamp"

    # Check 6: messageInputValue should be empty (message was sent)
    message_input_value = final_state.get("messageInputValue", "")
    if message_input_value != "":
        return 0.0, f"Expected messageInputValue to be empty after sending, got '{message_input_value}'"

    return 1.0, "Successfully sent message 'Thanks for sharing the recipe!' in #social channel"


def _validate_search_with_from_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully applied a "from" filter to search results.

    This function checks:
    1. The page is "SEARCH"
    2. The searchQuery is "a"
    3. The params.query is "a"
    4. The searchFilters.fromUserId is "user-2" (Alistair)
    5. The searchFilters.mode is "messages"
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchQuery should be "a"
    search_query = final_state.get("searchQuery")
    if search_query != "a":
        return 0.0, f"Expected searchQuery to be 'a', got '{search_query}'"

    # Check 3: params.query should be "a"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "a":
        return 0.0, f"Expected params.query to be 'a', got '{query_param}'"

    # Check 4: searchFilters should exist
    search_filters = final_state.get("searchFilters")
    if search_filters is None:
        return 0.0, "Expected searchFilters to exist in final state"

    # Check 5: searchFilters.mode should be "messages"
    search_mode = search_filters.get("mode")
    if search_mode != "messages":
        return 0.0, f"Expected searchFilters.mode to be 'messages', got '{search_mode}'"

    # Check 6: searchFilters.fromUserId should be "user-2" (Alistair)
    from_user_id = search_filters.get("fromUserId")
    if from_user_id != "user-2":
        return 0.0, f"Expected searchFilters.fromUserId to be 'user-2' (Alistair), got '{from_user_id}'"

    return 1.0, "Successfully applied 'from' filter to search results showing only messages from Alistair"


def _validate_search_with_in_filter(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully applied an "in" filter to search results.

    This function checks:
    1. The page is "SEARCH"
    2. The searchQuery is "a"
    3. The params.query is "a"
    4. The searchFilters.inId is "channel-1" (#all-slack channel)
    5. The searchFilters.mode is "messages"
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchQuery should be "a"
    search_query = final_state.get("searchQuery")
    if search_query != "a":
        return 0.0, f"Expected searchQuery to be 'a', got '{search_query}'"

    # Check 3: params.query should be "a"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "a":
        return 0.0, f"Expected params.query to be 'a', got '{query_param}'"

    # Check 4: searchFilters should exist
    search_filters = final_state.get("searchFilters")
    if search_filters is None:
        return 0.0, "Expected searchFilters to exist in final state"

    # Check 5: searchFilters.mode should be "messages"
    search_mode = search_filters.get("mode")
    if search_mode != "messages":
        return 0.0, f"Expected searchFilters.mode to be 'messages', got '{search_mode}'"

    # Check 6: searchFilters.inId should be "channel-1" (#all-slack channel)
    in_id = search_filters.get("inId")
    if in_id != "channel-1":
        return 0.0, f"Expected searchFilters.inId to be 'channel-1' (#all-slack), got '{in_id}'"

    return 1.0, "Successfully applied 'in' filter to search results showing only messages from #all-slack channel"


def _validate_create_new_public_channel(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully created a new public channel named "engineering".

    This function checks:
    1. The page is "CHANNEL"
    2. A new channel exists in the channels array with name "engineering"
    3. The currentChannel is set to the new channel's ID
    4. The new channel ID is in joinedChannelIds
    5. The currentDM is null (not viewing a DM)
    6. The isCreateChannelOpen is false (modal is closed)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentDM should be null (not viewing a DM)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null, got '{current_dm}'"

    # Check 3: channels array should exist
    channels = final_state.get("channels", [])
    if not isinstance(channels, list):
        return 0.0, "Expected channels to be an array"

    # Check 4: Find the new channel with name "engineering"
    engineering_channel = None
    for channel in channels:
        if channel.get("name") == "engineering":
            engineering_channel = channel
            break

    if engineering_channel is None:
        return 0.0, "Expected to find a new channel with name 'engineering' in the channels array"

    # Check 5: The engineering channel should have an id
    engineering_channel_id = engineering_channel.get("id")
    if not engineering_channel_id:
        return 0.0, "Expected the engineering channel to have an id"

    # Check 6: currentChannel should be set to the new engineering channel's ID
    current_channel = final_state.get("currentChannel")
    if current_channel != engineering_channel_id:
        return (
            0.0,
            f"Expected currentChannel to be '{engineering_channel_id}' (the new engineering channel), got '{current_channel}'",
        )

    # Check 7: The new channel ID should be in joinedChannelIds
    joined_channel_ids = final_state.get("joinedChannelIds", [])
    if not isinstance(joined_channel_ids, list):
        return 0.0, "Expected joinedChannelIds to be an array"

    if engineering_channel_id not in joined_channel_ids:
        return 0.0, f"Expected joinedChannelIds to include the new engineering channel ID '{engineering_channel_id}'"

    # Check 8: isCreateChannelOpen should be false (modal is closed)
    is_create_channel_open = final_state.get("isCreateChannelOpen")
    if is_create_channel_open is not False:
        return 0.0, f"Expected isCreateChannelOpen to be false (modal closed), got '{is_create_channel_open}'"

    return 1.0, "Successfully created new public channel 'engineering' and navigated to it"


def _validate_navigate_to_direct_message_page_from_search_and_send_a_message(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully searched for a person, navigated to their DM page, and sent a message.

    This function checks:
    1. The page is "USER_DM"
    2. The params.userId is "user-2" (Alistair)
    3. The currentDM is "dm-1" (the DM with Alistair)
    4. The searchQuery is "Alistair"
    5. A new message exists in the messages array with:
       - userId: "user-1" (the current user Dzaka)
       - dmId: "dm-1"
       - content: "testing"
    6. The messageInputValue is empty (message was sent)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "USER_DM"
    page = final_state.get("page")
    if page != "USER_DM":
        return 0.0, f"Expected page to be 'USER_DM', got '{page}'"

    # Check 2: params.userId should be "user-2" (Alistair)
    params = final_state.get("params", {})
    user_id_param = params.get("userId")
    if user_id_param != "user-2":
        return 0.0, f"Expected params.userId to be 'user-2' (Alistair), got '{user_id_param}'"

    # Check 3: currentDM should be "dm-1" (the DM with Alistair)
    current_dm = final_state.get("currentDM")
    if current_dm != "dm-1":
        return 0.0, f"Expected currentDM to be 'dm-1' (the DM with Alistair), got '{current_dm}'"

    # Check 4: searchQuery should be "Alistair"
    search_query = final_state.get("searchQuery")
    if search_query != "Alistair":
        return 0.0, f"Expected searchQuery to be 'Alistair', got '{search_query}'"

    # Check 5: messages array should exist
    messages = final_state.get("messages", [])
    if not isinstance(messages, list):
        return 0.0, "Expected messages to be an array"

    # Check 6: Find a message in dm-1 from user-1 with the expected content
    target_message = None
    for message in messages:
        if message.get("dmId") == "dm-1" and message.get("userId") == "user-1" and message.get("content") == "testing":
            target_message = message
            break

    if target_message is None:
        return 0.0, "Expected to find a new message with content 'testing' from user-1 in dm-1"

    # Check 7: The message should have a valid id and timestamp
    message_id = target_message.get("id")
    if not message_id:
        return 0.0, "Expected the new message to have an id"

    message_timestamp = target_message.get("timestamp")
    if not message_timestamp:
        return 0.0, "Expected the new message to have a timestamp"

    # Check 8: messageInputValue should be empty (message was sent)
    message_input_value = final_state.get("messageInputValue", "")
    if message_input_value != "":
        return 0.0, f"Expected messageInputValue to be empty after sending, got '{message_input_value}'"

    return 1.0, "Successfully searched for 'Alistair', navigated to DM page, and sent message 'testing'"


def _validate_using_exclude_automations_filter_on_search_results(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Validate that the user successfully applied the "Exclude automations" filter to search results.

    This function checks:
    1. The page is "SEARCH"
    2. The searchQuery is "a"
    3. The params.query is "a"
    4. The searchFilters.mode is "messages"
    5. The searchFilters.excludeAutomations is true
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchQuery should be "a"
    search_query = final_state.get("searchQuery")
    if search_query != "a":
        return 0.0, f"Expected searchQuery to be 'a', got '{search_query}'"

    # Check 3: params.query should be "a"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "a":
        return 0.0, f"Expected params.query to be 'a', got '{query_param}'"

    # Check 4: searchFilters should exist
    search_filters = final_state.get("searchFilters")
    if search_filters is None:
        return 0.0, "Expected searchFilters to exist in final state"

    # Check 5: searchFilters.mode should be "messages"
    search_mode = search_filters.get("mode")
    if search_mode != "messages":
        return 0.0, f"Expected searchFilters.mode to be 'messages', got '{search_mode}'"

    # Check 6: searchFilters.excludeAutomations should be true
    exclude_automations = search_filters.get("excludeAutomations")
    if exclude_automations is not True:
        return 0.0, f"Expected searchFilters.excludeAutomations to be true, got '{exclude_automations}'"

    return 1.0, "Successfully applied 'Exclude automations' filter to search results"


def _validate_open_direct_message_from_sidebar(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully opened a direct message from the sidebar.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "" (empty string when viewing a DM)
    3. The currentDM is "dm-1" (the DM with Alistair)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "" (empty string when viewing a DM)
    current_channel = final_state.get("currentChannel")
    if current_channel != "":
        return 0.0, f"Expected currentChannel to be empty string when viewing DM, got '{current_channel}'"

    # Check 3: currentDM should be "dm-1" (the DM with Alistair)
    current_dm = final_state.get("currentDM")
    if current_dm != "dm-1":
        return 0.0, f"Expected currentDM to be 'dm-1' (the DM with Alistair), got '{current_dm}'"

    return 1.0, "Successfully opened direct message with Alistair from sidebar"


def _validate_search_and_filter_by_people(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully searched for people and opened a user profile.

    This function checks:
    1. The page is "SEARCH"
    2. The searchQuery is "Mara"
    3. The params.query is "Mara"
    4. The searchFilters.mode is "people"
    5. The searchSelection is set to a user (type: "user", userId: "user-4")
    6. The showUserProfile is true
    7. The selectedUserId is "user-4" (Mara Okafor)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: searchQuery should be "Mara"
    search_query = final_state.get("searchQuery")
    if search_query != "Mara":
        return 0.0, f"Expected searchQuery to be 'Mara', got '{search_query}'"

    # Check 3: params.query should be "Mara"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "Mara":
        return 0.0, f"Expected params.query to be 'Mara', got '{query_param}'"

    # Check 4: searchFilters should exist
    search_filters = final_state.get("searchFilters")
    if search_filters is None:
        return 0.0, "Expected searchFilters to exist in final state"

    # Check 5: searchFilters.mode should be "people"
    search_mode = search_filters.get("mode")
    if search_mode != "people":
        return 0.0, f"Expected searchFilters.mode to be 'people', got '{search_mode}'"

    # Check 6: searchSelection should exist and be a user selection
    search_selection = final_state.get("searchSelection")
    if search_selection is None:
        return 0.0, "Expected searchSelection to be set, got null"

    # Check 7: searchSelection.type should be "user"
    selection_type = search_selection.get("type")
    if selection_type != "user":
        return 0.0, f"Expected searchSelection.type to be 'user', got '{selection_type}'"

    # Check 8: searchSelection.userId should be "user-4" (Mara Okafor)
    user_id = search_selection.get("userId")
    if user_id != "user-4":
        return 0.0, f"Expected searchSelection.userId to be 'user-4' (Mara Okafor), got '{user_id}'"

    # Check 9: showUserProfile should be true
    show_user_profile = final_state.get("showUserProfile")
    if show_user_profile is not True:
        return 0.0, f"Expected showUserProfile to be true, got '{show_user_profile}'"

    # Check 10: selectedUserId should be "user-4" (Mara Okafor)
    selected_user_id = final_state.get("selectedUserId")
    if selected_user_id != "user-4":
        return 0.0, f"Expected selectedUserId to be 'user-4' (Mara Okafor), got '{selected_user_id}'"

    return 1.0, "Successfully searched for 'Mara', switched to people mode, and opened Mara Okafor's user profile"


def _validate_navigate_from_search_to_channel(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from the search page to the channel view.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. The currentDM is null (not viewing a DM)
    4. The searchQuery is "" (empty, no longer on search page)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3' (#social), got '{current_channel}'"

    # Check 3: currentDM should be null (not viewing a DM)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null, got '{current_dm}'"

    # Check 4: searchQuery should be "" (empty, no longer on search page)
    search_query = final_state.get("searchQuery")
    if search_query != "":
        return 0.0, f"Expected searchQuery to be empty string after navigating from search, got '{search_query}'"

    return 1.0, "Successfully navigated from search page to #social channel"


def _validate_closing_a_user_dm(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully closed a user DM on the User DM page.

    This function checks:
    1. The page is "USER_DM"
    2. The params.userId is "user-1"
    3. The currentDM is null (DM is closed)
    4. The selectedDMUserId is null (no DM selected)
    5. The showBlankState is true (blank page shown in DM area)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "USER_DM"
    page = final_state.get("page")
    if page != "USER_DM":
        return 0.0, f"Expected page to be 'USER_DM', got '{page}'"

    # Check 2: params.userId should be "user-1"
    params = final_state.get("params", {})
    user_id_param = params.get("userId")
    if user_id_param != "user-1":
        return 0.0, f"Expected params.userId to be 'user-1', got '{user_id_param}'"

    # Check 3: currentDM should be null (DM is closed)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null after closing DM, got '{current_dm}'"

    # Check 4: selectedDMUserId should be null (no DM selected)
    selected_dm_user_id = final_state.get("selectedDMUserId")
    if selected_dm_user_id is not None:
        return 0.0, f"Expected selectedDMUserId to be null after closing DM, got '{selected_dm_user_id}'"

    # Check 5: showBlankState should be true (blank page shown in DM area)
    show_blank_state = final_state.get("showBlankState")
    if show_blank_state is not True:
        return 0.0, f"Expected showBlankState to be true after closing DM, got '{show_blank_state}'"

    return 1.0, "Successfully closed user DM, showing blank state on User DM page"


def _validate_filter_names_in_dm_view(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully filtered names in the DM view and opened a DM.

    This function checks:
    1. The page is "USER_DM"
    2. The params.userId is "user-1"
    3. The currentDM is "dm-3" (the DM with Mara)
    4. The userListSearchTerm is "Mara" (the filter term used)
    5. The selectedDMUserId is "user-4" (Mara Okafor)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "USER_DM"
    page = final_state.get("page")
    if page != "USER_DM":
        return 0.0, f"Expected page to be 'USER_DM', got '{page}'"

    # Check 2: params.userId should be "user-1"
    params = final_state.get("params", {})
    user_id_param = params.get("userId")
    if user_id_param != "user-1":
        return 0.0, f"Expected params.userId to be 'user-1', got '{user_id_param}'"

    # Check 3: currentDM should be "dm-3" (the DM with Mara)
    current_dm = final_state.get("currentDM")
    if current_dm != "dm-3":
        return 0.0, f"Expected currentDM to be 'dm-3' (the DM with Mara), got '{current_dm}'"

    # Check 4: userListSearchTerm should be "Mara" (the filter term used)
    user_list_search_term = final_state.get("userListSearchTerm")
    if user_list_search_term != "Mara":
        return 0.0, f"Expected userListSearchTerm to be 'Mara', got '{user_list_search_term}'"

    # Check 5: selectedDMUserId should be "user-4" (Mara Okafor)
    selected_dm_user_id = final_state.get("selectedDMUserId")
    if selected_dm_user_id != "user-4":
        return 0.0, f"Expected selectedDMUserId to be 'user-4' (Mara Okafor), got '{selected_dm_user_id}'"

    return 1.0, "Successfully filtered names in DM view with 'Mara' and opened DM with Mara Okafor"


def _validate_dm_view_to_search_view(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully navigated from the DM view to the search view.

    This function checks:
    1. The page is "SEARCH"
    2. The params.query is "Alistair"
    3. The searchQuery is "Alistair"
    4. The currentDM is null (not viewing a DM anymore)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "SEARCH"
    page = final_state.get("page")
    if page != "SEARCH":
        return 0.0, f"Expected page to be 'SEARCH', got '{page}'"

    # Check 2: params.query should be "Alistair"
    params = final_state.get("params", {})
    query_param = params.get("query")
    if query_param != "Alistair":
        return 0.0, f"Expected params.query to be 'Alistair', got '{query_param}'"

    # Check 3: searchQuery should be "Alistair"
    search_query = final_state.get("searchQuery")
    if search_query != "Alistair":
        return 0.0, f"Expected searchQuery to be 'Alistair', got '{search_query}'"

    # Check 4: currentDM should be null (not viewing a DM anymore)
    current_dm = final_state.get("currentDM")
    if current_dm is not None:
        return 0.0, f"Expected currentDM to be null after navigating to search view, got '{current_dm}'"

    return 1.0, "Successfully navigated from DM view to search view with 'Alistair' query"


def _validate_reply_to_message_in_thread(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Validate that the user successfully replied to a message in a thread.

    This function checks:
    1. The page is "CHANNEL"
    2. The currentChannel is "channel-3" (social channel)
    3. The threadPanel.isOpen is true
    4. The threadPanel.parentMessageId is "msg-01"
    5. A new message exists in the messages array with:
       - userId: "user-1" (the current user Dzaka)
       - channelId: "channel-3"
       - content: "Count me in!"
       - threadParentId: "msg-01"
    6. The messageInputValue is empty (message was sent)
    """
    logger.debug(f"Running reward function on state: {final_state}")

    # Check 1: page should be "CHANNEL"
    page = final_state.get("page")
    if page != "CHANNEL":
        return 0.0, f"Expected page to be 'CHANNEL', got '{page}'"

    # Check 2: currentChannel should be "channel-3" (social channel)
    current_channel = final_state.get("currentChannel")
    if current_channel != "channel-3":
        return 0.0, f"Expected currentChannel to be 'channel-3', got '{current_channel}'"

    # Check 3: threadPanel should exist
    thread_panel = final_state.get("threadPanel")
    if thread_panel is None:
        return 0.0, "Expected threadPanel to exist in final state"

    # Check 4: threadPanel.isOpen should be true
    thread_panel_is_open = thread_panel.get("isOpen")
    if thread_panel_is_open is not True:
        return 0.0, f"Expected threadPanel.isOpen to be true, got '{thread_panel_is_open}'"

    # Check 5: threadPanel.parentMessageId should be "msg-01"
    parent_message_id = thread_panel.get("parentMessageId")
    if parent_message_id != "msg-01":
        return 0.0, f"Expected threadPanel.parentMessageId to be 'msg-01', got '{parent_message_id}'"

    # Check 6: messages array should exist
    messages = final_state.get("messages", [])
    if not isinstance(messages, list):
        return 0.0, "Expected messages to be an array"

    # Check 7: Find a message in channel-3 from user-1 with the expected content and threadParentId
    target_message = None
    for message in messages:
        if (
            message.get("channelId") == "channel-3"
            and message.get("userId") == "user-1"
            and message.get("content") == "Count me in!"
            and message.get("threadParentId") == "msg-01"
        ):
            target_message = message
            break

    if target_message is None:
        return (
            0.0,
            (
                "Expected to find a new reply message with content 'Count me in!' from user-1",
                "in channel-3 with threadParentId 'msg-01'",
            ),
        )

    # Check 8: The message should have a valid id and timestamp
    message_id = target_message.get("id")
    if not message_id:
        return 0.0, "Expected the new reply message to have an id"

    message_timestamp = target_message.get("timestamp")
    if not message_timestamp:
        return 0.0, "Expected the new reply message to have a timestamp"

    # Check 9: messageInputValue should be empty (message was sent)
    message_input_value = final_state.get("messageInputValue", "")
    if message_input_value != "":
        return 0.0, f"Expected messageInputValue to be empty after sending, got '{message_input_value}'"

    return 1.0, "Successfully replied to message 'Morning crew! Coffee walk at 10?' in thread with 'Count me in!'"


# Registry of all Slack reward functions
REWARD_FUNCTIONS_SLACK = {
    "_validate_navigate_to_search_page": _validate_navigate_to_search_page,
    "_validate_switch_to_different_channel": _validate_switch_to_different_channel,
    "_validate_view_user_profile_from_message": _validate_view_user_profile_from_message,
    "_validate_open_thread_panel_from_message": _validate_open_thread_panel_from_message,
    "_validate_navigate_from_direct_message_to_channel": _validate_navigate_from_direct_message_to_channel,
    "_validate_switch_search_filter_to_people": _validate_switch_search_filter_to_people,
    "_validate_search_and_open_message_result": _validate_search_and_open_message_result,
    "_validate_send_message_in_channel": _validate_send_message_in_channel,
    "_validate_reply_to_message_in_thread": _validate_reply_to_message_in_thread,
    "_validate_search_with_from_filter": _validate_search_with_from_filter,
    "_validate_search_with_in_filter": _validate_search_with_in_filter,
    "_validate_create_new_public_channel": _validate_create_new_public_channel,
    "_validate_navigate_to_direct_message_page_from_search_and_send_a_message": _validate_navigate_to_direct_message_page_from_search_and_send_a_message,  # noqa: E501
    "_validate_using_exclude_automations_filter_on_search_results": _validate_using_exclude_automations_filter_on_search_results,  # noqa: E501
    "_validate_open_direct_message_from_sidebar": _validate_open_direct_message_from_sidebar,
    "_validate_search_and_filter_by_people": _validate_search_and_filter_by_people,
    "_validate_navigate_from_search_to_channel": _validate_navigate_from_search_to_channel,
    "_validate_closing_a_user_dm": _validate_closing_a_user_dm,
    "_validate_filter_names_in_dm_view": _validate_filter_names_in_dm_view,
    "_validate_dm_view_to_search_view": _validate_dm_view_to_search_view,
}

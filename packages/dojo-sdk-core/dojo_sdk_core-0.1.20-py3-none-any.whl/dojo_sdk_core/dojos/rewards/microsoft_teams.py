"""
Reward function for Microsoft Teams SPA
"""

from typing import Any, Dict, List, Tuple


# === Easy ===
def _validate_respond_to_hermione(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has sent the message
    "Sure thing - it looks good!" to Hermione.

    Args:
        state: The current SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if message sent, 0.0 otherwise
    """
    user_id = "you"
    target_conversation_id = "hermione-granger"
    expected_content = "Sure thing - it looks good!"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Find Hermione's conversation
    hermione_convo = None
    for convo in messages:
        if convo.get("conversationId") == target_conversation_id:
            hermione_convo = convo
            break

    if hermione_convo is None:
        return 0.0, "Hermione's conversation not found."

    # Check if the expected message exists in the conversation
    for msg in hermione_convo.get("messages", []):
        if msg.get("senderId") == user_id and msg.get("content") == expected_content:
            return 1.0, "Success! The expected message was sent to Hermione."

    return 0.0, f"Message not sent. Expected: '{expected_content}'"


def _validate_message_tim_white_twice(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has sent two specific messages
    to Tim White.

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if both messages sent, 0.0 otherwise
    """
    user_id = "you"
    target_conversation_id = "tim-white"
    expected_messages = ["Hey Tim, smoke test completed.", "Let me know if you need a hand with anything."]

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Find Tim White's conversation
    tim_convo = None
    for convo in messages:
        if convo.get("conversationId") == target_conversation_id:
            tim_convo = convo
            break

    if tim_convo is None:
        return 0.0, "Tim White's conversation not found."

    # Check if both expected messages exist in the conversation
    sent_messages = [msg.get("content") for msg in tim_convo.get("messages", []) if msg.get("senderId") == user_id]
    missing = [msg for msg in expected_messages if msg not in sent_messages]

    if not missing:
        return 1.0, "Success! Both messages were sent to Tim White."
    else:
        return 0.0, f"Message(s) not sent: {missing}"


def _validate_harry_hagrid_harry_hagrid(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user completed the sequence:
      1. Messaged Harry: "Hey Harry, can we reschedule to 2? I have a meeting with Hagrid."
      2. Messaged Hagrid: "Hey Hagrid, should be all good - I'll let you know asap."
      3. Messaged Harry: "Good to hear - see you at 2!"
      4. Messaged Hagrid: "Harry said yes, I'll see you at 12 then!"

    Args:
        initial_state: The starting SPA state
        final_state: The final SPA state after user actions

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if all messages are correctly sent, 0.0 otherwise
    """
    user_id = "you"
    harry_convo_id = "harry-potter"
    hagrid_convo_id = "hagrid-cao"

    expected_messages = {
        harry_convo_id: ["Hey Harry, can we reschedule to 2? I have a meeting with Hagrid.", "Good to hear - see you at 2!"],
        hagrid_convo_id: [
            "Hey Hagrid, should be all good - I'll let you know asap.",
            "Harry said yes, I'll see you at 12 then!",
        ],
    }

    messages: List[Dict[str, Any]] = final_state.get("messages", [])
    found: dict[str, list[str]] = {harry_convo_id: [], hagrid_convo_id: []}

    for convo in messages:
        convo_id = convo.get("conversationId")
        if convo_id in expected_messages:
            for msg in convo.get("messages", []):
                if msg.get("senderId") == user_id:
                    content = msg.get("content", "")
                    if content in expected_messages[convo_id]:
                        found[convo_id].append(content)

    harry_msgs = set(found[harry_convo_id])
    hagrid_msgs = set(found[hagrid_convo_id])

    harry_ok = harry_msgs == set(expected_messages[harry_convo_id])
    hagrid_ok = hagrid_msgs == set(expected_messages[hagrid_convo_id])

    if harry_ok and hagrid_ok:
        return 1.0, "Success! All messages were correctly sent to Harry and Hagrid in both chats."

    missing: list[str] = []
    for convo_id, expected in expected_messages.items():
        convo_name = "Harry" if convo_id == harry_convo_id else "Hagrid"
        missing_msgs = [m for m in expected if m not in found[convo_id]]
        if missing_msgs:
            missing.append(f"{convo_name}: {missing_msgs}")

    return 0.0, f"Some messages are missing or incorrect: {', '.join(missing)}"


def _validate_open_search_page_for_hagrid(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user opened the search page for Hagrid.

    Args:
        initial_state: The SPA state before user action
        final_state: The SPA state after user action

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if the search page shows results for Hagrid, 0.0 otherwise
    """
    expected_search_term = "hagrid"
    expected_page = "SEARCH"
    expected_search_page_type = "PEOPLE"

    # Check if the search page is open
    page = final_state.get("page")
    search_page = final_state.get("searchPage")
    search_term = final_state.get("searchTerm", "").lower()

    if page != expected_page:
        return 0.0, f"Wrong page open: {page}. Expected HOME → SEARCH."

    if search_page != expected_search_page_type:
        return 0.0, f"Search page type is '{search_page}', expected '{expected_search_page_type}'."

    if search_term != expected_search_term:
        return 0.0, f"Search term is '{search_term}', expected '{expected_search_term}'."

    return 1.0, "Success! Hagrid's search page is open and ready."


def _validate_prepare_to_make_a_new_chat(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has selected the new chat icon
    and entered the new chat screen.

    Args:
        initial_state: The SPA state before the action
        final_state: The SPA state after the action

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if the new chat screen is shown, 0.0 otherwise
    """
    # Check if the SPA has transitioned to creating a new chat
    creating_chat = final_state.get("creatingChat", False)

    if creating_chat:
        return 1.0, "Success! The new chat screen is now shown."

    return 0.0, "New chat screen not shown. Make sure the new chat icon was clicked."


def _validate_filter_chats_for_harry(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the sidebar chats are filtered
    for the name 'harry', meaning only Harry Potter's chat is shown.

    Args:
        state: The current SPA state as a dictionary.

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if only Harry Potter's chat is displayed after filtering,
                 0.0 otherwise.
    """
    target_filter = "harry"

    # Extract filtering info
    filter_string: str = final_state.get("filterString", "")
    filtering: bool = final_state.get("filtering", False)
    # messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # If filtering not active or filter string is wrong
    if not filtering:
        return 0.0, "Filtering is not active."
    if filter_string.lower() != target_filter:
        return 0.0, f"Expected filter string '{target_filter}', got '{filter_string}'."

    return 1.0, "Success! Filters for Harry potter's chat."


def _validate_navigate_to_harrys_files_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has navigated to Harry's files page.

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if files page is open, 0.0 otherwise
    """
    expected_page = "FILES"
    current_page = final_state.get("mainChatPage", "")

    if current_page == expected_page:
        return 1.0, "Success! The files page is open."

    return 0.0, f"Files page not open. Current page: '{current_page}'"


def _validate_navigate_to_harrys_photos_page(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has navigated to Harry's photos page.

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if files page is open, 0.0 otherwise
    """
    expected_page = "PHOTOS"
    current_page = final_state.get("mainChatPage", "")

    if current_page == expected_page:
        return 1.0, "Success! The photos page is open."

    return 0.0, f"Photos page not open. Current page: '{current_page}'"


# === Medium ===
def _validate_message_hermione_and_then_tim(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has:
    1. Sent Hermione the message "All done. Let me know if you get it!"
    2. Sent Tim the message "Smoke tested! Should be with you shortly."

    Args:
        initial_state: The initial SPA state
        final_state: The final SPA state after user interaction

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if both messages were sent correctly, 0.5 if only one was sent, 0.0 otherwise
    """
    user_id = "you"

    # Define targets
    hermione_conversation_id = "hermione-granger"
    tim_conversation_id = "tim-white"

    expected_hermione_msg = "All done. Let me know if you get it!"
    expected_tim_msg = "Smoke tested! Should be with you shortly."

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Helper to find a conversation by ID
    def find_convo(convo_id: str) -> Dict[str, Any]:
        for convo in messages:
            if convo.get("conversationId") == convo_id:
                return convo
        return {}

    # Check Hermione convo
    hermione_convo = find_convo(hermione_conversation_id)
    hermione_msg_sent = (
        any(
            msg.get("senderId") == user_id and msg.get("content") == expected_hermione_msg
            for msg in hermione_convo.get("messages", [])
        )
        if hermione_convo
        else False
    )

    # Check Tim convo
    tim_convo = find_convo(tim_conversation_id)
    tim_msg_sent = (
        any(msg.get("senderId") == user_id and msg.get("content") == expected_tim_msg for msg in tim_convo.get("messages", []))
        if tim_convo
        else False
    )

    # Reward logic
    if hermione_msg_sent and tim_msg_sent:
        return 1.0, "Success! Messages sent to both Hermione and Tim."
    elif hermione_msg_sent or tim_msg_sent:
        missing = "Tim" if hermione_msg_sent else "Hermione"
        return 0.5, f"Partially complete. Missing message to {missing}."
    else:
        return 0.0, "Messages not sent to either Hermione or Tim."


def _validate_make_a_group_chat_with_hagrid_and_ron(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that checks if the user has created a group chat
    including Hagrid and Ron, and sent the message "Hey guys!".

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if the correct group chat was created and message sent, 0.0 otherwise
    """
    user_id = "you"
    expected_participants = {"hagrid-cao", "ron-weasley"}
    expected_message = "Hey guys!"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])
    if not messages:
        return 0.0, "No messages found in final state."

    # Look for a new conversation containing both Hagrid and Ron
    for convo in messages:
        user_ids = set(convo.get("userIds", []))
        if expected_participants.issubset(user_ids):
            # Check that the user sent "Hey guys!" in this conversation
            for msg in convo.get("messages", []):
                if msg.get("senderId") == user_id and msg.get("content") == expected_message:
                    return 1.0, "Success! Created group chat with Hagrid and Ron and sent 'Hey guys!'."
            return 0.0, "Group chat found, but expected message not sent."

    return 0.0, "No group chat found with both Hagrid and Ron."


def _validate_create_a_chat_with_fred_weasely(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that checks if a new chat was created with Fred Weasley
    and the message "Hey Fred, how are you!" was sent.

    Args:
        state: The current SPA state as a dictionary.

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if chat created and message sent, 0.0 otherwise.
    """
    user_id = "you"
    target_conversation_id = "fred-weasley"
    expected_content = "Hey Fred, how are you!"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Find Fred's conversation
    fred_convo = None
    for convo in messages:
        if convo.get("conversationId") == target_conversation_id:
            fred_convo = convo
            break

    if fred_convo is None:
        return 0.0, "Conversation with Fred Weasley not found. Make sure you started a new chat."

    # Check if the expected message exists in the conversation
    for msg in fred_convo.get("messages", []):
        if msg.get("senderId") == user_id and msg.get("content") == expected_content:
            return 1.0, "Success! Chat with Fred Weasley created and message sent."

    return 0.0, f"Message not found in Fred's chat. Expected: '{expected_content}'"


def _validate_message_tim_and_select_hermiones_photos(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that validates whether:
      1. The user sent "Hey Tim, it's me" to Tim White.
      2. The user navigated to Hermione's chat and selected the Photos tab.

    Args:
        initial_state: The SPA's starting state as a dictionary.
        final_state: The SPA's ending state as a dictionary.

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if both actions are complete, 0.5 if only message is sent,
                 0.0 otherwise.
    """

    user_id = "you"
    tim_conversation_id = "tim-white"
    hermione_conversation_id = "hermione-granger"
    expected_message = "Hey Tim, it's me"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # --- Step 1: Check message to Tim ---
    tim_convo = None
    for convo in messages:
        if convo.get("conversationId") == tim_conversation_id:
            tim_convo = convo
            break

    message_sent = False
    if tim_convo:
        for msg in tim_convo.get("messages", []):
            if msg.get("senderId") == user_id and msg.get("content") == expected_message:
                message_sent = True
                break

    # --- Step 2: Check Hermione's chat and Photos tab ---
    active_convo = final_state.get("msgId")
    active_tab = final_state.get("mainChatPage")

    on_hermione_photos = active_convo == hermione_conversation_id and active_tab == "PHOTOS"

    # --- Combine results ---
    if message_sent and on_hermione_photos:
        return 1.0, "Success! Message sent to Tim and Hermione's Photos tab is open."
    elif message_sent:
        return 0.5, "Partial success. Message sent to Tim, but not on Hermione's Photos tab."
    else:
        return 0.0, "Message to Tim not sent yet, and Hermione's Photos tab not open."


def _validate_search_for_messages_containing_hey(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that checks if a search for 'hey' was performed and
    if the result containing "Hey Hugo — are we still on for Friday at 12pm?" is shown.

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if search result is present, 0.0 otherwise
    """
    expected_message_content = "Hey Hugo — are we still on for Friday at 12pm?"

    # Check if the user navigated to the MESSAGES tab in the search page
    if final_state.get("page") != "SEARCH" or final_state.get("searchPage") != "MESSAGES":
        return 0.0, "User did not navigate to the messages tab after searching."

    # Look through all messages in the final state
    messages: List[Dict[str, Any]] = final_state.get("messages", [])
    for convo in messages:
        for msg in convo.get("messages", []):
            if expected_message_content in msg.get("content", ""):
                return 1.0, f"Success! Found expected message: '{expected_message_content}'"

    return 0.0, f"Message not found. Expected: '{expected_message_content}'"


def _validate_message_tim_and_alex_langford(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user sent the message
    "Smoke test finished, looks good!" to Tim and also started a
    new conversation with Alex Langford, sending "Good to see you Alex!".

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple[float, str]:
            reward = 1.0 if both conditions met,
                     0.5 if only one of them is met,
                     0.0 otherwise.
            message = explanation of result.
    """
    user_id = "you"
    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # --- Targets ---
    tim_convo_id = "tim-white"
    tim_expected_content = "Smoke test finished, looks good!"

    alex_convo_id = "alex-langford"
    alex_expected_content = "Good to see you Alex!"

    tim_message_sent = False
    alex_message_sent = False

    # Check Tim’s conversation
    for convo in messages:
        if convo.get("conversationId") == tim_convo_id:
            for msg in convo.get("messages", []):
                if msg.get("senderId") == user_id and msg.get("content") == tim_expected_content:
                    tim_message_sent = True
                    break

    # Check Alex’s conversation (it must exist and have the message)
    for convo in messages:
        if convo.get("conversationId") == alex_convo_id:
            for msg in convo.get("messages", []):
                if msg.get("senderId") == user_id and msg.get("content") == alex_expected_content:
                    alex_message_sent = True
                    break

    # --- Scoring logic ---
    if tim_message_sent and alex_message_sent:
        return 1.0, "Success! Messages sent to both Tim and Alex."
    elif tim_message_sent:
        return 0.5, "Partial success: message sent to Tim, but not to Alex."
    elif alex_message_sent:
        return 0.5, "Partial success: message sent to Alex, but not to Tim."
    else:
        return 0.0, "No valid messages sent to Tim or Alex."


# === Hard ===
def _validate_large_group_chat(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has created a group chat with
    Harry Potter, Hermione Granger, Tim White, and Tim White 2,
    and sent the message 'What a group chat!'.

    Args:
        initial_state: The initial SPA state as a dictionary
        final_state: The final SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if the group chat and message exist, 0.0 otherwise
    """
    user_id = "you"
    expected_users = {"harry-potter", "hermione-granger", "tim-white", "tim-white-2"}
    expected_message = "What a group chat!"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Find a conversation that has exactly the expected users
    group_convo = None
    for convo in messages:
        convo_users = set(convo.get("userIds", []))
        if convo_users == expected_users:
            group_convo = convo
            break

    if group_convo is None:
        return 0.0, "Group chat with the required users not found."

    # Check if the expected message was sent by the user in that chat
    for msg in group_convo.get("messages", []):
        if msg.get("senderId") == user_id and msg.get("content") == expected_message:
            return 1.0, "Success! Group chat created and message sent."

    return 0.0, f"Message not found in the group chat. Expected: '{expected_message}'"


def _validate_message_hermione_and_search_for_it(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that verifies:
    1. The user sent the message "All good Hermione, it's finished." to Hermione.
    2. The user performed a search for 'Hermi' and opened the 'messages' tab.

    Args:
        initial_state: The initial SPA state as a dictionary.
        final_state: The final SPA state as a dictionary.

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if both conditions are met, partial reward if only one is met.
    """
    user_id = "you"
    target_conversation_id = "hermione-granger"
    expected_content = "All good Hermione, it's finished."
    expected_search_term = "Hermi"
    expected_search_page = "MESSAGES"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Step 1: Verify Hermione's conversation and message
    hermione_convo = None
    for convo in messages:
        if convo.get("conversationId") == target_conversation_id:
            hermione_convo = convo
            break

    if hermione_convo is None:
        return 0.0, "Hermione's conversation not found."

    sent_message = any(
        msg.get("senderId") == user_id and msg.get("content") == expected_content for msg in hermione_convo.get("messages", [])
    )

    # Step 2: Verify search term and tab
    search_term = final_state.get("searchTerm", "")
    search_page = final_state.get("searchPage", "")
    on_search_page = final_state.get("page") == "SEARCH"

    correct_search = on_search_page and search_term == expected_search_term and search_page == expected_search_page

    # Evaluate total reward
    if sent_message and correct_search:
        return 1.0, "Success! You messaged Hermione and searched for it correctly."
    elif sent_message:
        return 0.5, "Message sent, but search not completed correctly."
    elif correct_search:
        return 0.5, "Search was correct, but Hermione’s message wasn’t sent."
    else:
        return 0.0, "Neither the message nor the search action were completed correctly."


def _validate_message_the_third_user_in_the_search(
    initial_state: Dict[str, Any], final_state: Dict[str, Any]
) -> Tuple[float, str]:  # noqa: E501
    """
    Reward function that checks if the user has messaged the third user in the
    search list ("Anne Peters") with the message "Hi Anne, it's me."

    Args:
        initial_state: The starting SPA state as a dictionary
        final_state: The resulting SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if message sent correctly, 0.0 otherwise
    """
    user_id = "you"
    target_conversation_id = "anne-peters"
    expected_content = "Hi Anne, it's me."

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Locate Anne's conversation
    anne_convo = None
    for convo in messages:
        if convo.get("conversationId") == target_conversation_id:
            anne_convo = convo
            break

    if anne_convo is None:
        return 0.0, "Anne's conversation not found — looks like you didn't message her."

    # Check if the expected message exists
    for msg in anne_convo.get("messages", []):
        if msg.get("senderId") == user_id and msg.get("content") == expected_content:
            return 1.0, "Nice! You successfully messaged Anne Peters with the correct text."

    return 0.0, f"Message not sent or incorrect. Expected: '{expected_content}'"


# _validate_harry_hagrid_harry_hagrid
def _validate_message_and_search_for_2(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function for verifying that:
    1. The user sent two specific messages to Harry Potter.
    2. The user searched for the number '2' in messages.
    3. The search results display five messages (four from user, one from Harry).

    Args:
        initial_state: The starting state of the SPA
        final_state: The ending state after the user's actions

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if all criteria are met, 0.0 otherwise
    """
    user_id = "you"
    target_conversation_id = "harry-potter"

    required_messages = ["What do you mean you said we'd meet at two?!", "Wait let me check my message history"]

    # 1. Check messages to Harry
    messages: List[Dict[str, Any]] = final_state.get("messages", [])
    harry_convo = next((convo for convo in messages if convo.get("conversationId") == target_conversation_id), None)

    if harry_convo is None:
        return 0.0, "Harry's conversation not found."

    convo_messages = harry_convo.get("messages", [])
    sent_texts = [m.get("content") for m in convo_messages if m.get("senderId") == user_id]

    if not all(req in sent_texts for req in required_messages):
        return 0.0, "Missing one or more required messages to Harry."

    # 2. Check search parameters
    search_term = final_state.get("searchTerm", "")
    search_page = final_state.get("searchPage", "")

    if search_term != "2" or search_page != "MESSAGES":
        return (
            0.0,
            f"Search not completed correctly. Expected term='2' and page='MESSAGES', got term='{search_term}', page='{search_page}'.",  # noqa: E501
        )  # noqa: E501

    # 3. Check number of messages in search results (five total, four from user, one from Harry)
    harry_msgs = [
        msg for convo in messages if convo.get("conversationId") == target_conversation_id for msg in convo.get("messages", [])
    ]

    num_from_user = sum(1 for m in harry_msgs if m.get("senderId") == user_id)
    num_from_harry = sum(1 for m in harry_msgs if m.get("senderId") == "harry-potter")

    if num_from_user == 5 and num_from_harry == 1:  # three to harry, one to hermione and tim.
        return 1.0, "Success! Messages sent, search performed, and correct results displayed."
    else:
        return 0.0, f"Incorrect number of messages displayed. Found {num_from_user} from you and {num_from_harry} from Harry."


def _validate_the_a_team(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function for the "The A team" task in Microsoft Teams.
    Checks if a group chat with Alex Langford, Alex Langford II, and Anne Peters
    exists and contains the message "The A team" sent by the user.

    Args:
        initial_state: The initial SPA state (not used here)
        final_state: The final SPA state

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if group chat exists and message sent, 0.0 otherwise
    """
    user_id = "you"
    target_users = {"alex-langford", "alex-langford-2", "anne-peters"}
    expected_message = "The A team"

    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # Find the group chat containing all three target users
    target_chat = None
    for convo in messages:
        convo_users = set(["alex-langford", "alex-langford-2", "anne-peters"])
        if target_users.issubset(convo_users):
            target_chat = convo
            break

    if target_chat is None:
        return 0.0, "Group chat with Alex Langford, Alex Langford II, and Anne Peters not found."

    # Check if the expected message was sent by the user
    for msg in target_chat.get("messages", []):
        if msg.get("senderId") == user_id and msg.get("content") == expected_message:
            return 1.0, "Success! The group chat was created and message sent."

    return 0.0, f"Group chat exists but message '{expected_message}' was not sent."


def _validate_birthday_for_george(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function that checks if the user has:
      1. Created a group chat with Fred Weasley, Hermione Granger, and Harry Potter
      2. Sent the correct message in that group chat
      3. Sent a follow-up message to George Weasley
      4. Typed "Ron Weasley" into the search bar (without pressing enter)
      5. Stayed on the HOME page

    Args:
        state: The current SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if all criteria are met, 0.0 otherwise
    """

    user_id = "you"
    messages: List[Dict[str, Any]] = final_state.get("messages", [])
    page: str = final_state.get("page", "")
    search_term: str = final_state.get("searchTerm", "").strip().lower()

    # --- 1. Check for group chat ---
    expected_group_users = {"fred-weasley", "harry-potter", "hermione-granger"}
    group_message_text = "Hey guys, just confirming we're throwing a surprise party for George tomorrow at 3. See you then!"

    group_chat_found = False
    group_message_ok = False
    george_message_ok = False

    for convo in messages:
        user_ids = set(convo.get("userIds", []))
        convo_messages = convo.get("messages", [])

        # Check group chat
        if user_ids == expected_group_users:
            group_chat_found = True
            for msg in convo_messages:
                if msg.get("senderId") == user_id and msg.get("content") == group_message_text:
                    group_message_ok = True
                    break

        # Check message to George
        if user_ids == {"george-weasley"}:
            for msg in convo_messages:
                if (
                    msg.get("senderId") == user_id
                    and msg.get("content") == "Hey George, is it your day off tomorrow? I can't remember if you're out."
                ):
                    george_message_ok = True
                    break

    # --- 2. Check all criteria ---
    if not group_chat_found:
        return 0.0, "Group chat with Fred, Harry, and Hermione not found."

    if not group_message_ok:
        return 0.0, "Expected message to the group chat not found."

    if not george_message_ok:
        return 0.0, "Expected message to George Weasley not found."

    if search_term != "ron weasley":
        return 0.0, f"Search term incorrect. Expected 'Ron Weasley', found '{final_state.get('searchTerm', '')}'."

    if page != "HOME":
        return 0.0, f"User is not on HOME page (found '{page}')."

    return 1.0, "Success! All expected actions were completed correctly."


def _validate_group_chat_and_hermione(initial_state: Dict[str, Any], final_state: Dict[str, Any]) -> Tuple[float, str]:
    """
    Reward function for validating that:
      1. The user created a group chat with Harry and Hagrid and sent the message:
         "I'll see you both at 2. Looking forward to it!"
      2. Then messaged Hermione saying:
         "Hey Hermione, me, Harry and Hagrid are meeting up if you want to join us!"

    Args:
        state: The current SPA state as a dictionary

    Returns:
        Tuple of (reward, message)
        reward = 1.0 if both conditions met, 0.5 if only group chat message sent,
                 0.0 otherwise
    """
    user_id = "you"
    messages: List[Dict[str, Any]] = final_state.get("messages", [])

    # --- Condition 1: Group chat with Harry and Hagrid ---
    expected_group_users = {"hagrid-cao", "harry-potter"}
    expected_group_message = "I'll see you both at 2. Looking forward to it!"
    group_chat_found = False
    group_message_sent = False

    for convo in messages:
        convo_users = set(convo.get("userIds", []))
        if convo_users == expected_group_users:
            group_chat_found = True
            for msg in convo.get("messages", []):
                if msg.get("senderId") == user_id and msg.get("content") == expected_group_message:
                    group_message_sent = True
                    break
            break

    if not group_chat_found:
        return 0.0, "Group chat with Harry and Hagrid not found."

    if not group_message_sent:
        return 0.0, f"Group chat found, but expected message '{expected_group_message}' not sent."

    # --- Condition 2: Message Hermione ---
    hermione_convo = next((c for c in messages if c.get("conversationId") == "hermione-granger"), None)
    expected_hermione_message = "Hey Hermione, me, Harry and Hagrid are meeting up if you want to join us!"
    hermione_message_sent = False

    if hermione_convo is not None:
        for msg in hermione_convo.get("messages", []):
            if msg.get("senderId") == user_id and msg.get("content") == expected_hermione_message:
                hermione_message_sent = True
                break
    else:
        return 0.5, "Hermione's conversation not found, but group chat message was sent."

    if group_message_sent and hermione_message_sent:
        return 1.0, "Success! Both group chat message and Hermione message were sent."
    elif group_message_sent:
        return 0.5, "Partial success — group chat message sent, but Hermione message missing."
    else:
        return 0.0, "Messages missing or incorrect."

    # Registry of all microsoft teams reward functions


REWARD_FUNCTIONS_MICROSOFT_TEAMS = {
    "_validate_respond_to_hermione": _validate_respond_to_hermione,
    "_validate_message_tim_white_twice": _validate_message_tim_white_twice,
    "_validate_prepare_to_make_a_new_chat": _validate_prepare_to_make_a_new_chat,
    "_validate_open_search_page_for_hagrid": _validate_open_search_page_for_hagrid,
    "_validate_filter_chats_for_harry": _validate_filter_chats_for_harry,
    "_validate_navigate_to_harrys_files_page": _validate_navigate_to_harrys_files_page,
    "_validate_navigate_to_harrys_photos_page": _validate_navigate_to_harrys_photos_page,
    "_validate_message_hermione_and_then_tim": _validate_message_hermione_and_then_tim,
    "_validate_make_a_group_chat_with_hagrid_and_ron": _validate_make_a_group_chat_with_hagrid_and_ron,
    "_validate_create_a_chat_with_fred_weasely": _validate_create_a_chat_with_fred_weasely,
    "_validate_message_tim_and_select_hermiones_photos": _validate_message_tim_and_select_hermiones_photos,
    "_validate_search_for_messages_containing_hey": _validate_search_for_messages_containing_hey,
    "_validate_message_tim_and_alex_langford": _validate_message_tim_and_alex_langford,
    "_validate_large_group_chat": _validate_large_group_chat,
    "_validate_message_hermione_and_search_for_it": _validate_message_hermione_and_search_for_it,
    "_validate_message_the_third_user_in_the_search": _validate_message_the_third_user_in_the_search,
    "_validate_harry_hagrid_harry_hagrid": _validate_harry_hagrid_harry_hagrid,
    "_validate_message_and_search_for_2": _validate_message_and_search_for_2,
    "_validate_the_a_team": _validate_the_a_team,
    "_validate_birthday_for_george": _validate_birthday_for_george,
    "_validate_group_chat_and_hermione": _validate_group_chat_and_hermione,
}

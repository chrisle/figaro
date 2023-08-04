"""
Example chat bot that has a short term memory.

This example uses the figaro-ai-chat and figaro-ai to create a chat bot that
remembers the conversation. You can configure how much it remembers by changing
the number in the session.messages[-5:] slice.

The {% for message in session.messages[-5:] %} loop in the template will
include the last 5 messages from the session as part of the prompt to the LLM.

We use the before and after hook in figaro-ai to save the users input and the
LLM response to memory. In this demo, it's stored in a temporary file on disk
but you can swap it out for a different storage mechanism.

The prompt_toolkit library has nothing to do with figaro-ai. It is simply used
to create a user interface on the command line.
"""

import figaro_ai
import figaro_ai_chat
import prompt_toolkit
import uuid

template = """
You are a chat bot.

Conversation summary:
{{ session.chat_summary }}

Continue this conversation:
{% for message in session.messages[-5:] %}
{{ message.sender }}: {{ message.content }}
{% endfor %}

{{ session.user_display_name }}: {{ user_input }}
{{ session.ai_display_name }}:
{% gen vertexai "response" model="text-bison" %}
"""

# Start a new chat session.
session = figaro_ai_chat(
    # Create a session with a unique ID.
    session_id=str(uuid.uuid4()),

    # Use a temporary file on disk to store the chat history.
    history_store=figaro_ai_chat.history_stores.TempDisk,

    # Enable verbose logging.
    verbose=True)

# Create a hook that will be called before sending the user input to the LLM.
def before_response_hook(prompt, args, kwargs):

    # Get the user input from the kwargs.
    user_input = kwargs['user_input']

    # Save the user input to the session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.USER,
        content=user_input,
    ))

    # Return the prompt, args, and kwargs back to figaro_ai.
    return (prompt, args, kwargs)

# Create a hook that will be called after receiving the response from the LLM.
def after_response_hook(response):

    # Save the response to the session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.AI,
        content=response,
    ))

    # Return the response back to figaro_ai.
    return response

# Initialize figaro_ai and include before and after hooks.
chat_bot = figaro_ai(
    template=template,
    verbose=True,
    google_project_id='acn-agbg-ai',
    google_project_location='us-central1',
    hooks={
        'before_response': [before_response_hook],
        'after_response': [after_response_hook]
    }
)

while True:
    print ('Enter "q" to quit.')

    # Get user input.
    message = prompt_toolkit.prompt('>> ')
    if message == 'q': break

    # Get response from chat bot.
    response = chat_bot(session=session.get_session(),
                        user_input=message)
    print(response)

import figaro_ai_chat
import figaro_ai
import uuid
import prompt_toolkit

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
    session_id=str(uuid.uuid4()),
    history_store=figaro_ai_chat.history_stores.TempDisk,
    verbose=True)

# Create a hook that will be called before sending the user input to the LLM.
def before_response_hook(prompt, args, kwargs):
    user_input = kwargs['user_input']

    # Save the user input to the session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.USER,
        content=user_input,
    ))

    return (prompt, args, kwargs)

# Create a hook that will be called after receiving the response from the LLM.
def after_response_hook(response):

    # Save the response to the session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.AI,
        content=response,
    ))
    return response

# Setup the chat bot.
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
    # Get user input.
    message = prompt_toolkit.prompt('>> ')
    if message == 'q': break

    # Get response from chat bot.
    response = chat_bot(session=session.get_session(),
                        user_input=message)
    print(response)

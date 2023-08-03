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
{{ session.ai_display_name }}:

{% gen vertexai "response" model="text-bison" %}
"""

# Start a new chat session.
session = figaro_ai_chat(
    session_id=str(uuid.uuid4()),
    history_store=figaro_ai_chat.history_stores.TempDisk,
    verbose=True)

# Setup the chat bot.
chat_bot = figaro_ai(template=template,
                     verbose=True,
                     google_project_id='acn-agbg-ai',
                     google_project_location='us-central1')

while True:
    # Get user input.
    message = prompt_toolkit.prompt('>> ')

    if message == 'q': break

    # Append user input to session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.USER,
        content=message,
    ))

    # Get response from chat bot.
    response = chat_bot(session=session.get_session(),
                        user_input=message)

    # Append response to session.
    session.append(figaro_ai_chat.models.ChatSessionMessage(
        role_type=figaro_ai_chat.models.Roles.AI,
        content=response,
    ))

    print(response)

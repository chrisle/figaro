# from figaro_memory import ConversationHistory
from prompt_toolkit import prompt
import figaro_ai
import sys

class Message:
    def __init__(self, id, role_type, content):
        self.id = id
        self.role_type = role_type
        self.content = content

class FakeSession:

    def __init__(self, session_id, user_role_name, ai_role_name):
        self.session_id = session_id
        self.user_role_name = user_role_name
        self.ai_role_name = ai_role_name

    @property
    def summary(self):
        return 'summary'

    def get_messages(self, last_n):
        return [
            Message(id="1", role_type="user", content="hello ai"),
            Message(id="2", role_type="ai", content="hello human!"),
        ]

# Get a specific session
# session = ConversationHistory.get_session(
#     session_id="12345",
#     user_role_name="Chris",
#     ai_role_name="AI"
# )
session = FakeSession( session_id="12345", user_role_name="Chris", ai_role_name="AI" )

PERSONALITY = "You are a chat bot that speaks like a sea pirate!"

print ("Type 'q' to quit the chat bot")
while True:
    user_input = prompt("> ")
    if user_input == "q": sys.exit(0)

    template = """
{{ personality }}
Conversation summary: {{ session.summary }}

Complete this conversation:
{% for message in session.get_messages(last_n=10) -%}
{%- if message.role_type == "user" -%}
{{ session.user_role_name }}: {{ message.content }}
{% else %}
{{ session.ai_role_name }}: {{ message.content }}
{% endif %}
{%- endfor %}

{{ session.user_role_name }}: {{ user_input }}
{{ session.ai_role_name }}:
{% gen vertexai "response" model="text-bison" %}
    """
    turn = figaro_ai(template=template, verbose=True)
    response = turn(personality=PERSONALITY, session=session, user_input=user_input)
    print (response)

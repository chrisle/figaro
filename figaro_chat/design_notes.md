```py

import figaro_chat

personality = "You are a chat assistant"

turn_template = """
{{ personality }}

Conversation Summary: {{ conversation_summary }}

Last 10 messages:
{% for message of messsages %}
  {{ message.role_name }}: {{ message.content }}
{% endfor %}
{{ message.role_name }}: {{ user_input }}
"""

chatbot = figaro_chat(personality=personality, turn_template=turn_template)

response = chatbot(user_input=)
```
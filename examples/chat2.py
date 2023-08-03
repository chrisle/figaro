import figaro_ai_chat
import uuid

chat_session: figaro_ai_chat.ChatSession = figaro_ai_chat(
    session_id=str(uuid.uuid4()),
    history_store=figaro_ai_chat.history_stores.TempDisk,
    verbose=True,
)

for n in range(40, 50):
    if n % 2 == 0:
        role = figaro_ai_chat.models.Roles.AI
        message = f'hello human ({n})'
    else:
        role = figaro_ai_chat.models.Roles.USER
        message = f'hello computer ({n})'

    chat_session.append(figaro_ai_chat.models.Message(
        id=str(n),
        role_type=role,
        content=message,
    ))

messages = chat_session.messages(last_n=5)
for message in messages:
    if message.role_type == figaro_ai_chat.models.Roles.AI:
        print(f'AI: {message.content}')
    else:
        print(f'USER: {message.content}')

import figaro_ai_chat

chat_session: figaro_ai_chat.ChatSession = figaro_ai_chat(
    session_id='1234',
    history_store=figaro_ai_chat.history_stores.TempDisk,
)

for n in range(0, 10):
    if n % 2 == 0:
        role = figaro_ai_chat.models.Roles.ai
        message = f'hello human ({n})'
    else:
        role = figaro_ai_chat.models.Roles.user
        message = f'hello computer ({n})'

    message = figaro_ai_chat.models.Message(
        id=str(n),
        role_type=role,
        content=message,
    )
    chat_session.append(message)

print(chat_session.get_chat(last_n=5))
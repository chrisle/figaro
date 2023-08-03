import figaro_ai_chat

chat_session = figaro_ai_chat(
    session_id='1234',
    history_store=figaro_ai_chat.history_stores.TempDisk,
    verbose=True,
)

chat_session.append(figaro_ai_chat.models.Message(
    id='1',
    role_type=figaro_ai_chat.models.Roles.user,
    content='hello world',
))

chat_session.append(figaro_ai_chat.models.Message(
    id='2',
    role_type=figaro_ai_chat.models.Roles.ai,
    content='hello human',
))

print(chat_session.messages)
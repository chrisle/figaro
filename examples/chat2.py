import figaro_chat

chat_session = figaro_chat(
    session_id='1234',
    history_store=figaro_chat.history_stores.TempDisk,
)

chat_session.append()
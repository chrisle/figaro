from figaro_ai_chat.history_stores.base import HistoryStoreBase
from figaro_ai_chat.models import ChatSessionMessage
from figaro_ai_chat.models import ChatDisplayMessage
from figaro_ai_chat.models import ChatBotEnvironment
from figaro_ai_chat.models import Roles
from typing import Union
from figaro_ai.types import HookMap


class ChatSession():

    def __init__(self,
                 ai_display_name: str = 'AI',
                 user_display_name: str = 'User',
                 history_store: HistoryStoreBase = None,
                 session_id: Union[str, None] = None,
                 **kwargs
                 ):

        # Ensure history_store is not None.
        if history_store is None:
            raise ValueError('history_store cannot be None')

        self._ai_display_name = ai_display_name
        self._user_display_name = user_display_name

        self._session_id = session_id
        self._history_store = history_store(self._session_id)
        self._session = self._history_store.load_session()


    @property
    def session_id(self):
        return self._session_id

    @property
    def title(self):
        return self._session.title

    def get_session(self):
        display_messages: list[ChatDisplayMessage] = []
        for message in self._session.messages:
            sender = self._ai_display_name if message.role_type == Roles.AI \
                else self._user_display_name
            display_messages.append(ChatDisplayMessage(
                sender=sender,
                content=message.content))

        return ChatBotEnvironment(
            ai_display_name=self._ai_display_name,
            user_display_name=self._user_display_name,
            chat_summary=self._session.summary,
            messages=display_messages)

    def append(self, message: ChatSessionMessage):
        self._session.messages.append(message)
        self._history_store.write_session(chat_session=self._session)

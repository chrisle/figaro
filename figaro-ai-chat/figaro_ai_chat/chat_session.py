from figaro_ai_chat.history_stores.base import HistoryStoreBase
from figaro_ai_chat.models import Message
from typing import Union

class ChatSession():

    def __init__(self,
                 ai_display_name: str,
                 user_display_name: str,
                 history_store: HistoryStoreBase = None,
                 session_id: Union[str, None] = None,
                 **kwargs
                 ):
        self._ai_display_name = ai_display_name,
        self._user_display_name = user_display_name

        # Ensure history_store is not None.
        if history_store is None:
            raise ValueError('history_store cannot be None')

        self._session_id = session_id
        self._history_store = history_store(self._session_id)
        self._session = self._history_store.load_session()

    @property
    def ai_display_name(self):
        return self._ai_display_name

    @property
    def user_display_name(self):
        return self._user_diplay_name

    @property
    def session_id(self):
        return self._session_id

    @property
    def title(self):
        return self._session.title

    @property
    def summary(self):
        return self._session.summary

    def messages(self,
                 last_n: int = None,
                 before=None,
                 after=None):
        messages = self._session.messages
        if last_n is not None:
            return messages[-last_n:]
        return self._session.messages

    def append(self, message: Message):
        self._session.messages.append(message)
        self._history_store.write_session(chat_session=self._session)

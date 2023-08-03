from figaro_ai_chat.history_stores.base import HistoryStoreBase
from figaro_ai_chat.models import Message
from figaro_ai_chat.models import ChatSessionModel
from typing import Union
import uuid

class ChatSession():

    def __init__(self,
                 ai_display_name: str,
                 user_display_name: str,
                 history_store: HistoryStoreBase = None,
                 session_id: Union[str, None] = None,
                 **kwargs
                 ):
        self._ai_display_name = ai_display_name,
        self._user_diplay_name = user_display_name

        # Ensure history_store is not None.
        if history_store is None:
            raise ValueError('history_store cannot be None')

        # Initialize the history store.

        if session_id is None:
            # Generate a new session.
            self._session_id = uuid.uuid4()
            self._history_store = history_store(self._session_id)
            self._session = ChatSessionModel(
                id=self._session_id,
                title='Chat Session',
                summary='Chat Session',
                messages=[])
        else:
            # Load an existing session.
            self._session_id = session_id
            self._history_store = history_store(self._session_id)
            self._session = self._history_store.load_session(self._session_id)

    def append(self, message: Message):
        self._session.messages.append(message)
        self._history_store.write_session(chat_session=self._session)

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

    @property
    def messages(self):
        return self._session.messages

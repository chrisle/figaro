from figaro_ai_chat.history_stores.base import HistoryStoreBase
from figaro_ai_chat.models import ChatSessionModel
from figaro_ai_chat.models import Message
from figaro_ai_chat.models import Roles
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
        self._user_display_name = user_display_name

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

    def append(self, message: Message):
        self._session.messages.append(message)
        self._history_store.write_session(chat_session=self._session)

    def get_chat(self,
                 last_n: int = None,
                 before=None,
                 after=None):
        messages = self._session.messages
        if last_n is not None:
            return self._format_messages(messages[-last_n:])
        return self._format_messages(messages)

    def _format_messages(self, messages: list[Message]) -> str:
        output = ''
        for message in messages:
            username = self._ai_display_name \
                if message.role_type == Roles.ai \
                    else self._user_display_name

            output += f'{message.id} <{username}>: {message.content}\n'
        return output

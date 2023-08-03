from abc import abstractmethod
from typing import List
from figaro_ai_chat.models import Message
from figaro_ai_chat.models import ChatSessionModel

class HistoryStoreBase():

    def __init__(self, session_id: str = None):
        if session_id is None:
            raise ValueError('session_id cannot be None')
        self._session_id = session_id

    @abstractmethod
    def load_session(self, session_id: str) -> List[Message]:
        raise NotImplementedError()

    @abstractmethod
    def write_session(self, chat_session: ChatSessionModel):
        raise NotImplementedError()

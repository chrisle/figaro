from abc import abstractmethod
from figaro_ai_chat.models import ChatSessionModel

class HistoryStoreBase():

    def __init__(self, session_id: str = None):
        self._session_id = session_id

    #----------------------

    def load_session(self) -> ChatSessionModel:
        if self._session_id is not None and self._session_exists():
            return self._load_session()
        else:
            return ChatSessionModel.new()

    @abstractmethod
    def _load_session(self) -> ChatSessionModel:
        raise NotImplementedError()

    #----------------------

    def session_exists(self) -> bool:
        return self._session_exists()

    @abstractmethod
    def _session_exists(self) -> bool:
        raise NotImplementedError()

    #----------------------

    def write_session(self, chat_session: ChatSessionModel):
        return self._write_session(chat_session)

    @abstractmethod
    def _write_session(self, chat_session: ChatSessionModel):
        raise NotImplementedError()

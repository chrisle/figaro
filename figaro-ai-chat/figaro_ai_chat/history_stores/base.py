from abc import abstractmethod
from figaro_ai_chat.models import ChatSessionModel
import logging

class HistoryStoreBase():

    def __init__(self, session_id: str = None):
        self._session_id = session_id

    #----------------------

    def load_session(self) -> ChatSessionModel:
        logging.info(f'Loading chat session id={self._session_id}')
        if self._session_id is not None and self._session_exists():
            return self._load_session()
        else:
            return ChatSessionModel.new()

    @abstractmethod
    def _load_session(self) -> ChatSessionModel:
        raise NotImplementedError()

    #----------------------

    def session_exists(self) -> bool:
        logging.info(f'Checking if chat session exists id={self._session_id}')
        result = self._session_exists()
        if result:
            logging.info(f'Chat session exists id={self._session_id}')
        else:
            logging.info(f'Chat session does not exist id={self._session_id}')
        return result

    @abstractmethod
    def _session_exists(self) -> bool:
        raise NotImplementedError()

    #----------------------

    def write_session(self, chat_session: ChatSessionModel):
        logging.info(f'Writing chat session id={self._session_id}')
        return self._write_session(chat_session)

    @abstractmethod
    def _write_session(self, chat_session: ChatSessionModel):
        raise NotImplementedError()

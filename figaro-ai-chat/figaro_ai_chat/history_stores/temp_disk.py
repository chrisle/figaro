from .base import HistoryStoreBase
from figaro_ai_chat.models import ChatSessionModel
import json
import logging
import os
import tempfile


class TempDisk(HistoryStoreBase):
    """Stores chat history in a temporary file on local disk."""

    def __init__(self, session_id: str = None):
        super().__init__(session_id)
        self._session_filename = f'{tempfile.gettempdir()}/{self._session_id}.json'
        logging.info(f'Initializing TempDisk history store: {self._session_filename}')

    @property
    def session_filename(self):
        return self._session_filename

    def _write_session(self, chat_session: ChatSessionModel):
        logging.info(f'Writing chat session id={self._session_id}: {self.session_filename}')
        with open(self.session_filename, 'w') as f:
            f.write(chat_session.model_dump_json())

    def _load_session(self) -> ChatSessionModel:
        logging.info(f'Loading existing chat session id={self._session_id}: {self.session_filename}')
        with open(self.session_filename, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            session = ChatSessionModel(**data)
            return session

    def _session_exists(self) -> bool:
        logging.info(f'Checking if chat session exists id={self._session_id}: {self.session_filename}')
        return os.path.exists(self.session_filename)

from .base import HistoryStoreBase
from figaro_ai_chat.models import ChatSessionModel
import json
import logging
import tempfile

class TempDisk(HistoryStoreBase):

    def __init__(self, session_id: str = None):
        super().__init__(session_id)
        self._session_filename = f'{tempfile.gettempdir()}/{self._session_id}.json'
        logging.info(f'Initializing TempDisk history store: {self._session_filename}')

    @property
    def session_filename(self):
        return self._session_filename

    def write_session(self, chat_session: ChatSessionModel):
        logging.info(f'Writing chat session id={self._session_id}: {self.session_filename}')
        with open(self.session_filename, 'w') as f:
            f.write(chat_session.model_dump_json())

    def load_session(self) -> ChatSessionModel:
        logging.info(f'Loading chat session id={self._session_id}: {self.session_filename}')
        with open(self.session_filename, 'r') as f:
            data = json.loads(f)
            return ChatSessionModel(**data)

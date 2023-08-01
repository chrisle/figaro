from .base import HistoryStoreBase
import tempfile
import logging


class TempDisk(HistoryStoreBase):

    def __init__(self):
        self._temp_dir = tempfile.TemporaryDirectory()

    def get_session(self, session_id: str):
        logging.debug('Getting chat session id={session_id}')

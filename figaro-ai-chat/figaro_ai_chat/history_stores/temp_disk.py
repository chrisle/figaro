from .base import HistoryStoreBase
from figaro_ai_chat.models import Message
import json
import logging
import os
import tempfile


class TempDisk(HistoryStoreBase):

    def load_session(self):
        logging.debug('Getting chat session id={self._session_id}')

        filename = f'{tempfile.gettempdir()}/{self._session_id}.json'

        # Create emptry file if it doesn't exist.
        if not os.path.exists(filename):
            f = open(filename, 'w')
            f.write('[]')
            f.close()

        return self._parse_session_file(filename)

    def _parse_session_file(self, session_file: str):
        output = []
        with open(session_file, 'r') as f:
            content = f.read()
            data = json.loads(content)
        for message in data:
            output.append(Message(**message))

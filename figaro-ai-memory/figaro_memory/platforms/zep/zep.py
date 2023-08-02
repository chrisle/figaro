from .....figaro_ai.figaro_ai.memory.base_memory import BaseMemory
from zep_python import Memory, Message, MemorySearchPayload, ZepClient
from typing import Union
from figaro_ai.memory.chat_history_model import ChatHistoryModel

class Zep(BaseMemory):

    def __init__(self,
                 client_url='http://localhost:8000',
                 session_id: Union[str, None] = None,
                 # TODO: Add config options https://docs.getzep.com/deployment/config/#configuration-options
                 ):
        self._client = ZepClient(client_url)
        self._session_id = session_id

    @property
    def client(self):
        return self._client

    def _get_memory(self):
        if self._session_id is None:
            raise ValueError('Zep memory session ID was not set.')
        return self._client.get_memory(self._session_id)

    def get_summary(self):
        return self._get_memory().summary.content

    def get_chat_history(self):
        messages = self._get_memory().messages
        return [
            { 'role': message.role, 'content': message.content }
            for message in messages
        ]

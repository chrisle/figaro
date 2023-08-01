from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from figaro_chat.history_stores.base import HistoryStoreBase

class RoleTypeEnum(str, Enum):
    user = 'USER'
    ai = 'AI'

class MessageModel(BaseModel):
    id: str
    role_type: RoleTypeEnum = None
    content: str

class ChatSessionModel(BaseModel):
    id: str
    title: str
    summary: str
    messages: Optional[List[MessageModel]] = []


class ChatSession():

    def __init__(self,
                 ai_display_name: str,
                 history_store: HistoryStoreBase,
                 user_display_name: str,
                 session_id: str = None,
                 ):
        self._history_store = history_store

        if not session_id is None:
            self._history_store.get_session(session_id)

    def append(self):
        pass

    def get_messages(self, last_n=10, before: str = None, after: str = None):
        pass

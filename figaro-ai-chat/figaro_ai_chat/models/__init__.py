from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional, Union
import datetime
import time
import uuid

def current_timestamp():
    """Return current timestamp as an integer."""
    return int(time.mktime(datetime.datetime.now().timetuple()))

class Roles(Enum):
    USER = 1
    AI = 2

class Message(BaseModel):
    id: str
    role_type: Roles = None
    created_at: int = current_timestamp()
    content: str

class ChatSessionModel(BaseModel):
    id: str
    title: str
    summary: str
    created_at: int
    messages: Optional[List[Message]] = []

    def append(self, message: Union[Message, None] = None, **kwargs):
        if message is None:
            append_message = Message(**kwargs)
        else:
            append_message = message
        self.messages.append(append_message)

    def new():
        return ChatSessionModel(
            id=str(uuid.uuid4()),
            title='Chat Session',
            summary='Chat Session',
            created_at=current_timestamp(),
            messages=[])

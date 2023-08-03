from enum import Enum
from pydantic import BaseModel
from typing import Optional, Union
import datetime
import time
import uuid

def current_timestamp():
    """Return current timestamp as an integer."""
    return int(time.mktime(datetime.datetime.now().timetuple()))

class Roles(Enum):
    USER = 1
    AI = 2

class ChatDisplayMessage(BaseModel):
    sender: str
    content: str

class ChatBotEnvironment(BaseModel):
    ai_display_name: str
    user_display_name: str
    chat_summary: str
    messages: list[ChatDisplayMessage] = []

class ChatSessionMessage(BaseModel):
    id: str = str(uuid.uuid4())
    role_type: Roles = None
    created_at: int = current_timestamp()
    content: str

class ChatSessionModel(BaseModel):
    id: str
    title: str
    summary: str
    created_at: int
    messages: Optional[list[ChatSessionMessage]] = []

    def append(self, message: Union[ChatSessionMessage, None] = None, **kwargs):
        if message is None:
            append_message = ChatSessionMessage(**kwargs)
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

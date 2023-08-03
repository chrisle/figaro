from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Roles(str, Enum):
    user = 'USER'
    ai = 'AI'

class Message(BaseModel):
    id: str
    role_type: Roles = None
    content: str

class ChatSessionModel(BaseModel):
    id: str
    title: str
    summary: str
    messages: Optional[List[Message]] = []
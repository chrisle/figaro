from pydantic import BaseModel
from enum import Enum

class Roles(str, Enum):
    user = 'USER'
    ai = 'AI'

class Message(BaseModel):
    id: str
    role_type: Roles = None
    content: str
from pydantic import BaseModel

class ChatHistoryModel(BaseModel):
    subject_name: str
    ai_name: str

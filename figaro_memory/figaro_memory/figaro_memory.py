from typing import Union
from .models.message import Message

class FigaroMemory():

    def __init__(self, llm=None, memory_store=None, vector_store=None):
        pass

    def summarize(self, text: Union[str, list[str]]):
        pass

    def add_message(self, message: Message):
        pass

    def search(self, query: str):
        pass
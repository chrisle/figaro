from .figaro_memory import FigaroMemory
import sys
import types
import logging

llm = None
memory_store = None
vector_store = None

class Memory(types.ModuleType):
    def __call__(self, llm=llm, memory_store=memory_store, vector_store=vector_store, verbose=False, level=logging.INFO) -> FigaroMemory:
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return FigaroMemory(llm=llm, memory_store=memory_store, vector_store=vector_store)

sys.modules[__name__].__class__ = Memory
from abc import abstractmethod
from figaro.llms.base_llm import BaseLLM
from figaro.memory.base_memory import BaseMemory
from typing import Union


class BaseAgent:

    def __init__(self,
                 llm: Union[BaseLLM, None] = None,
                 memory: Union[BaseMemory, None] = None,
                 verbose: bool = False,
                 ):
        self._llm = llm
        self._memory = memory
        self._verbose = verbose
        pass


    def get(self, user_input: Union[str, None] = None):
        if user_input is None:
            raise ValueError('user_input must be specified.')
        return self._get(user_input)


    @abstractmethod
    def _get(self, user_input: Union[str, None] = None):
        raise NotImplementedError('_get() not implemented')

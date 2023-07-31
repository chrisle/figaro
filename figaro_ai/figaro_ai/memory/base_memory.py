from abc import abstractmethod

class BaseMemory:

    def __init__(self):
        pass

    @abstractmethod
    def get_summary(self):
        raise NotImplementedError('Abstract method get_summary() is not implemented.')

    @abstractmethod
    def get_chat_history(self):
        raise NotImplementedError('Abstract method get_chat_history() is not implemented.')

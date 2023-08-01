from abc import abstractmethod
class HistoryStoreBase():

    def __init__(self):
        pass

    @abstractmethod
    def get_session(self, session_id: str):
        pass

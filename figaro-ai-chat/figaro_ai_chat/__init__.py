from .chat_session import ChatSession
import logging
import sys
import types


class FigaroChat(types.ModuleType):
    def __call__(self,
                 session_id=None,
                 history_store=None,
                 verbose=False,
                 level=logging.INFO,
                 ):

        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return ChatSession(
            history_store=history_store,
            session_id=session_id,
            verbose=verbose,
            level=level,
            )

sys.modules[__name__].__class__ = FigaroChat
import types
from . import history_stores
import logging
import sys
from .chat_session import ChatSession

class FigaroChat(types.ModuleType):
    def __call__(self,
                 session_id=None,
                 history_store=None,
                 user_display_name='User',
                 ai_display_name='AI',
                 verbose=False,
                 level=logging.INFO):
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return ChatSession(
            ai_display_name=ai_display_name,
            history_store=history_store,
            session_id=session_id,
            user_display_name=user_display_name,
            )

sys.modules[__name__].__class__ = FigaroChat
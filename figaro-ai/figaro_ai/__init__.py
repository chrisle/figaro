from . import llms
from . import types
from .executor import Executor
import logging
import sys
import types

class Figaro(types.ModuleType):
    def __call__(self,
                 template,
                 hooks={},
                 verbose=False,
                 level=logging.INFO,
                 **kwargs):
        # When verbose=True, send logs to stdout
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return Executor(
            template,
            hooks=hooks,
            verbose=False,
            level=logging.INFO,
            **kwargs)

sys.modules[__name__].__class__ = Figaro

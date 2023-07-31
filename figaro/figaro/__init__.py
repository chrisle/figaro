from . import llms
from .executor import Executor
import sys
import types
import logging

class Figaro(types.ModuleType):
    def __call__(self, template, verbose=False, level=logging.INFO, **kwargs):
        # When verbose=True, send logs to stdout
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return Executor(template, verbose=False, level=logging.INFO, **kwargs)

sys.modules[__name__].__class__ = Figaro

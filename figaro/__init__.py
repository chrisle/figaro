from . import llms

from .chain import Chain
import sys
import types
import logging

llm = None

class Figaro(types.ModuleType):
    def __call__(self, template, llm=None, verbose=False, level=logging.INFO, **kwargs):
        # When verbose=True, send logs to stdout
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        return Chain(template, llm=llm, **kwargs)

sys.modules[__name__].__class__ = Figaro

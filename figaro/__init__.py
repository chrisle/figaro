from . import llms

from .chain import Chain
import sys
import types


llm = None

class Figaro(types.ModuleType):
    def __call__(self, template, llm=None, verbose=False, **kwargs):
        return Chain(template, llm=llm, verbose=verbose, **kwargs)

sys.modules[__name__].__class__ = Figaro

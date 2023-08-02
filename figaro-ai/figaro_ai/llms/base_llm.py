from typing import Any


class BaseLLM():

    def __init__(self, **environment_globals: dict[str, Any]):
        pass

    def call(self, prompt: str, **options):
        raise NotImplementedError()
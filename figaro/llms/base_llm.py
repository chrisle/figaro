
class BaseLLM():

    def call(self, prompt: str) -> str:
        raise NotImplementedError()
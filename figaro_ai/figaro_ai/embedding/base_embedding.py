from typing import Union


class BaseEmbedding():

    model = None

    def text_embedding(self, text: Union[str, list[str]]) -> list:
        raise NotImplementedError()
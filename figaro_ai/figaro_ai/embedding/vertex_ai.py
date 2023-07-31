from .base_embedding import BaseEmbedding
from typing import Union
from vertexai.language_models import TextEmbeddingModel


DEFAULT_MODEL = "textembedding-gecko@001"

class VertexAI(BaseEmbedding):

    model = DEFAULT_MODEL

    def text_embedding(self, text: Union[str, list[str]]) -> list:
        """Text embedding with a Large Language Model."""
        model = TextEmbeddingModel.from_pretrained(self.model)
        embed_text = text if isinstance(text, list) else [text]
        embeddings = model.get_embeddings(embed_text)
        for embedding in embeddings:
            vector = embedding.values
            print(f"Length of Embedding Vector: {len(vector)}")
        return vector
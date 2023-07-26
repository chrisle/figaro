from figaro.llms.base_llm import BaseLLM
from vertexai.language_models import TextGenerationModel
import google.auth
import vertexai


class VertexAI(BaseLLM):

    def call(self, prompt: str):
        credentials, _ = google.auth.default()
        vertexai.init(
            project='acn-agbg-ai',
            location='us-central1',
            credentials=credentials
        )
        model = TextGenerationModel.from_pretrained('text-bison')
        parameters = {
            'temperature': 0.2,
            'max_output_tokens': 256,
            'top_p': 0.8,
            'top_k': 40
        }
        response = model.predict(prompt, **parameters)
        return response.text

from typing import Any
from figaro_ai.llms.base_llm import BaseLLM
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import CodeGenerationModel
import google.auth
import vertexai
import re
import logging

class VertexAI(BaseLLM):


    def __init__(self, **environment_globals: dict[str, Any]):
        self.project_id = environment_globals['google_project_id']
        self.location = environment_globals['google_project_location']
        credentials, _ = google.auth.default()
        self._credentials = credentials
        vertexai.init(
            project=self.project_id,
            location=self.location,
            credentials=credentials
        )

    def _default_option(self, key, options, default):
        if key in options:
            return options[key]
        else:
            return default

    def call(self, prompt: str, **options):
        if 'model' not in options:
            options['model'] = 'text-bison'

        if bool(re.search(r'text-bison.*', options['model'])):
            model = TextGenerationModel.from_pretrained(options['model'])
            parameters = {
                'temperature': self._default_option('temperature', options, 0.2),
                'max_output_tokens': self._default_option('max_output_tokens', options, 1024),
                'top_p': self._default_option('top_p', options, 0.8),
                'top_k': self._default_option('top_k', options, 40),
            }
        elif bool(re.search(r'code-bison.*', options['model'])):
            model = CodeGenerationModel.from_pretrained(options['model'])
            parameters = {
                'temperature': self._default_option('temperature', options, 0),
                'max_output_tokens': self._default_option('max_output_tokens', options, 1024),
            }
        else:
            raise ValueError(f'{options["model"]} is not a valid Vertex AI model')

        logging.debug(f'Parameters={parameters}'.strip())
        logging.debug(f'Prompt: {prompt}'.strip())
        response = model.predict(prompt, **parameters)
        logging.debug(f'Prediction: {response}'.strip())
        return response.text

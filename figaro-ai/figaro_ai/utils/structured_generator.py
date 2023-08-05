import json
import re
import sys

# https://github.com/1rgs/jsonformer/blob/main/jsonformer/main.py

class StructuredGenerator():

    def __init__(self,
                 schema: dict,
                 prompt: str,
                 llm):
        self.schema = schema
        self.prompt = prompt
        self.generation_marker = '|GENERATION|'
        self.llm = llm

    def generate_object(self, properties, obj):
        for key, schema in properties.items():
            obj[key] = self.generate_value(schema, obj, key)
        return obj

    def generate_value(self, schema, obj, key = None):
        schema_type = schema["type"]
        if schema_type == "integer":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_integer(**schema)
        elif schema_type == "float":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_float(**schema)
        elif schema_type == "boolean":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_boolean()
        elif schema_type == "string":
            if key:
                obj[key] = self.generation_marker
            else:
                obj.append(self.generation_marker)
            return self.generate_string(**schema)
        elif schema_type == "array":
            new_array = []
            obj[key] = new_array
            return self.generate_array(schema["items"], new_array, **schema)
        elif schema_type == "object":
            new_obj = {}
            if key:
                obj[key] = new_obj
            else:
                obj.append(new_obj)
            return self.generate_object(schema["properties"], new_obj)
        else:
            raise ValueError(f"Unsupported schema type: {schema_type}")

    def generate_string(self, **kwargs):
        prompt = self._prompt() + '"'
        response = self.llm.call(prompt, **kwargs)
        result = re.search(r'[^"]*', response).group()
        return result

    def generate_integer(self, **kwargs):
        prompt = self._prompt()
        parameters = { 'temperature': 1.0, 'max_output_tokens': 6 }
        args = { **kwargs, **parameters }
        response = self.llm.call(prompt, **args)
        result = re.search(r'[^,]*', response).group()
        return int(result)

    def generate_float(self, **kwargs):
        prompt = self._prompt()
        parameters = { 'temperature': 1, 'max_output_tokens': 6 }
        args = { **kwargs, **parameters }
        response = self.llm.call(prompt, model="text-bison", **args)
        result = re.search(r'[^,]*', response).group()
        return float(result)

    def generate_boolean(self, **kwargs):
        prompt = self._prompt()
        response = self.llm.call(prompt, **kwargs)
        result = re.search(r'[^,]*', response).group()
        return int(result) == 1

    def generate_array(self, item_schema, obj, **kwargs):
        for _ in range(kwargs['count']):
            # forces array to have at least one element
            element = self.generate_value(item_schema, obj)
            obj[-1] = element
            obj.append(self.generation_marker)
            obj.pop()
        return obj

    def generate(self):
        self.value = {}
        return self.generate_object(self.schema['properties'], self.value)

    def _prompt(self):
        template = """{prompt}\nOutput result in the following JSON schema format:\n{schema}\nResult: {progress}"""
        progress = json.dumps(self.value)
        gen_marker_index = progress.find(f'"{self.generation_marker}"')
        if gen_marker_index != -1:
            progress = progress[:gen_marker_index]
        else:
            raise ValueError("Failed to find generation marker")

        prompt = template.format(
            prompt=self.prompt,
            schema=json.dumps(self.schema),
            progress=progress,
        )
        return prompt

#########################################

from figaro_ai.llms.vertex_ai import VertexAI
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

llm = VertexAI(
            google_project_id='acn-agbg-ai',
            google_project_location='us-central1')

json_schema = {
    "type": "object",
    "properties": {
        "full_name": { "type": "string" },
        "age": { "type": "integer" },
        "rank": { "type": "float" },
        "is_student": { "type": "boolean" },
        "description": {
            "type": "object",
            "properties": {
                "hair_color": {"type": "string"},
                "shirt_color": {"type": "string"},
            }
        },
        "favorite_foods": {
            "type": "array",
            "count": 5,
            "items": { "type": "string" }
        },
        "favorite_subject": {"type": "string"},
    }
}

generator = StructuredGenerator(
    llm=llm,
    schema=json_schema,
    prompt="Generate a person based on the following schema:"
)
result = generator.generate()
print(result)

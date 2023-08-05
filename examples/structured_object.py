from figaro_ai.llms.vertex_ai import VertexAI
from figaro_ai.utils import StructuredGenerator
import logging
import sys
from pprint import pprint

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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
    prompt="Generate a person based on the following schema"
)
result = generator.generate()
pprint(result)

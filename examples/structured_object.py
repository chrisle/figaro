"""
This example demonstrates how to generate a structured object using a JSON schema.
"""

from figaro_ai.llms.vertex_ai import VertexAI
from figaro_ai.utils import StructuredGenerator
from pprint import pprint
import logging
import sys

# Enable logging to show what is happening under the hood.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Create an instance of the Language Model API.
llm = VertexAI(google_project_id='acn-agbg-ai', google_project_location='us-central1')

# Define a JSON schema that describes the structure of the object to be generated.
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

# Create an instance of the StructuredGenerator.
generator = StructuredGenerator(
    llm=llm,
    schema=json_schema,
    prompt="Generate a person based on the following schema"
)

# Generate the structured object.
result = generator.generate()

# Print the result.
pprint(result)

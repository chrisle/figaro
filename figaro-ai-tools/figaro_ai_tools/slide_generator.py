import figaro_ai
import json
from figaro_ai.utils.response_json_parser import response_json_parser

function_schema = {
    "name": "slide_generator",
    "description": "Generates slides for a presentation",
    "input": {
        "type": "object",
        "properties": {
            "context": {
                "type": "string",
                "description": "The context of the presentation"
            },
            "objective": {
                "type": "string",
                "description": "The objective of the presentation"
            }
        }
    },
    "output": {
        "type": "object",
        "properties": {
            "slides": {
                "type": "array<slide>",
                "description": "The slides to generate",
                "slide": {
                    "type": "object",
                    "description": "A slide",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the slide"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content of the slide as a single line of HTML."
                        }
                    }
                }
            }
        }
    }
}

def slide_generator(context: str, objective: str, slide_count: int):
    prompt_template = """
    Context: {{ context }}

    Objective: {{ objective }}

    In {{ slide_count }} slides answer the objective as JSON string using the following schema:
    {{ output_schema }}
    {% gen vertexai "result" model="code-bison" %}
    """

    generator = figaro_ai(
        template=prompt_template,
        verbose=True,
        google_project_id='acn-agbg-ai',
        google_project_location='us-central1')

    output_schema = function_schema['output']
    result = generator(
        context=context,
        objective=objective,
        output_schema=json.dumps(output_schema),
        slide_count=slide_count)

    return response_json_parser(result)

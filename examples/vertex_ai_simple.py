import figaro
import logging

template = """
{# This is a comment. It does nothing. #}

{# Start the chain by asking it for the capital of "us_state" #}
You are an AI assistant. Answer the following question:
What is the capital of {{us_state}}?
Reply with just the city name:

{# The next line sends the above template to VertexAI. It will use #}
{# VertexAI's "text-bison" model, and the answer will be stored in "capital" #}
{% gen vertexai 'capital' model='text-bison' %}

{# The next prompt takes the answer from the previous prompt, "capital", and #}
{# uses it in the next prompt. #}
What is the population of {{capital}}?
Reply with just an integer without separators.

{# Call VertexAI again, and store the answer in "population". #}
{% gen vertexai 'population' model='text-bison' %}

{# Now ask when was the city built but by continuing the context by saying "it" #}
What year was the city built? Reply with only the year.
{% gen vertexai 'built' model='text-bison' %}
"""

# Instanciate the chain.
chain = figaro(template=template, verbose=True, level=logging.INFO)

# Run the chain for California.
population = chain(us_state="California")

print(f'Final answer: {population}')
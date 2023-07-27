import figaro

template = """
What is the capital of {{us_state}}?
Respond with only the city name.
{% gen vertexai "capital" model="text-bison" %}

What is {{capital}}'s current population?
Respond as an integer without separators.
{% gen vertexai "population" model="text-bison" %}

Generate a JSON object with, state, city name, and capital.
Respond using this schema:
{ "state": "<state>", "capital": "<capital>", "population": "<population>" }
{% gen vertexai "result" model="code-bison" %}
"""

# Create a Figaro chain.
chain = figaro(template=template, verbose=True)

# Execute the chain with "California" as the input.
result = chain(us_state="California", type=dict)
print(result)
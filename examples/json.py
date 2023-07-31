import figaro

template = """
The following is a character profile for an RPG game. Fill in name and class..
Respond with this JSON schema:
{ "description": "{{description}}", "name": "", "class": "" }

{% gen vertexai "name" model="code-bison" %}
"""

# Create a Figaro chain.
chain = figaro(template=template, verbose=True)

# Execute the chain with "California" as the input.
result = chain(description="Male Elf warrior")
print(result)
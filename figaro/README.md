# Figaro

A simplified framework for working with large language models that's extendable
with code that easier to understand.

Features:

  * [X] Prompt templating powered by Jinja2.
  * [X] Easily switch LLM models anytime. Even within the same prompt chain!

------------------------------------------------------------------------------

## Examples

### Prompt Chain

```py
import figaro

template = """
What is the capital of {{us_state}}?
Respond with only the city name.
{% gen vertexai "capital" model="text-bison" %}

What is {{capital}}'s current population?
Respond with only a number.
{% gen vertexai "capital" model="text-bison" %}

Generate a JSON object with, state, city name, and capital.
For example: { "state": <string>, "capital": <string>, "population": <number> }
{% gen vertexai "capital" model="code-bison" %}
"""

# Create a Figaro chain.
chain = figaro(template=template, verbose=True)

# Execute the chain with "California" as the input.
capital = chain(us_state="California")

# "The capital is: Sacramento."
print(f"The capital is: {capital}.")
```

------------------------------------------------------------------------------

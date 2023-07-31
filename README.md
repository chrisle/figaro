# Figaro

A simplified framework for working with large language models that's extendable
with code that easier to understand.

Figaro attempts to solve the following probems:

  * [X] Simplify writing prompts and working with a Gen AI API.
  * [X] Switching between differnt LLM models.
  * [X] Combining multiple LLM models to produce the best result.
  * [ ] (Coming soon) Simplified multi-turn chat bot with memory.
  * [ ] (Coming soon) Using LLMs as a definable tool.

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

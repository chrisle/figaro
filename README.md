# Figaro

Figaro is a set of tools to make working prompt chains and multiple LLMs
easier to use. Prompts are created using Jinja templates. Additional features
such as chat, memory, and tools are separate so you can import only the parts
you need.

Figaro attempts to solve the following problems:

* [X] Simplify writing prompts and working with a Gen AI API.
* [X] Switch between differnt LLM models.
* [X] Combining multiple LLM models to produce the best result.
* [ ] (Coming soon) Simplified multi-turn chat bot with memory.
* [ ] (Coming soon) Using LLMs as a definable tool.

[Read the documentation](docs/README.md)

------------------------------------------------------------------------------

## Example

```py
import figaro_ai

def get_capital_and_population(us_state: str):
    """Use Vertex AI to get the capital city and population of a US State.

    Args:
        us_state: A US state to get capital city and population

    Returns:
        Dict with state, capital, and population.
    """

    # Define a Figaro prompt template.
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
    chain = figaro_ai(template=template, verbose=True)

    # Execute the chain with "California" as the input. The expected
    # result will be a dict.
    result = chain(us_state=us_state, type=dict)

    # Return the result.
    return result


data = get_capital_and_population(us_state="California")
print (data) # {'state': 'California', 'capital': 'Sacramento', 'population': 493648}

```

------------------------------------------------------------------------------

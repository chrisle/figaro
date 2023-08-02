# Figaro

Simplify working with prompt chains and multiple LLMs for generative AI in your
application.

Figaro is a versatile set of tools designed to streamline prompt chains and
multiple LLMs usage. With the power of Jinja templates, creating prompts becomes
effortless. Moreover, you can selectively import additional features like chat,
memory, and tools, tailoring the library to suit your specific needs. Enhance
your application with generative AI capabilities using Figaro.

[Read the documentation](docs/README.md)

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
    chain = figaro_ai(template=template, verbose=True,
                      google_project_id='google_project_id',
                      google_project_location='us-central1')

    # Execute the chain with "California" as the input. The expected
    # result will be a dict.
    result = chain(us_state=us_state, type=dict)

    # Return the result.
    return result


data = get_capital_and_population(us_state="California")
print (data) # {'state': 'California', 'capital': 'Sacramento', 'population': 493648}

```

------------------------------------------------------------------------------

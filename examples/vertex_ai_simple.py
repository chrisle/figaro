import figaro_ai

"""
FIGARO EXAMPLE
--------------

Figaro allows you to do multi-turn prompting using Jinja templates. Meaning
you can asking Gen AI a question then ask it another question based on the
answer of the first question.

The intention is that you can wrap a complex LLM tasks into a function in your
own program.

1) How variables work

    Variables in the template are strings that get replaced before being sent to
    the Gen AI. They are enclosed in double brackets: {{variable}}

    Example: What is the capital of {{us_state}}?

2) Get response from Gen AI

    To get a response from a Gen AI use the built-in function "gen". When Figaro
    encounters a {% gen %} command, it will construct a prompt that includes
    the entire template up to that point.

    The arguments are:
    gen <generative ai> <return jinja variable> [optional arguments]...

    Optional arguments will depend on what generative AI API you use. In this
    case Vertex AI can take the "model" argument.

    In the below example Figaro will send everything above the {% gen %} command
    to Vertex AI's "text-bison" model and  return the response into a Jinja
    variable "capital".

    Example:
        What is the capital of {{us_state}}?
        {% gen vertexai "capital" model="text-bison" %}

3) Multi-turn Prompting with Figaro

    Figaro will then continue to walk down your template to the next prompt. In
    the below example the next prompt will again include everything before it.

    The previous {% gen %} command returns the variable "capital" meaning you
    can use the answer in the next prompt.

    For example, in your template you can use {{capital}}:

        What is {{capital}}'s current population?
        {% gen vertexai "population" model="text-bison" %}

    Figaro will actually send everything before it including the last prompt as
    context.

    Meaning the actual prompt sent to the Gen AI the second time is:

        What is the capital of California?
        Respond with only the city name.
        Sacramento
        What is Sacramento's current population?
        Respond as an integer without separators.

4) Switching Models

    To switch models or Gen AI APIs in Figaro you can specify them inside the
    prompt template.

    For example the last prompt in this template uses "code-bison" instead of
    "text-bison"

    Example:
        Generate a JSON object with, state, city name, and capital.
        {% gen vertexai "result" model="code-bison" %}

5) Final output

    The last {% gen %} command in your template will be the returned value.
    Optionally, you can specify the exact type that you expect to be returned.

    Example:
        template = "{% gen vertexai "result" model="code-bison" %}"
        chain = figaro(template=template, verbose=True)
        returned_value = chain(us_state=us_state, type=dict)
        print returned_value

6) Debug logging

    When you create a Figaro chain include the argument "verbose=True". It
    will use the Python standard "logging" module for output.

    To increase the logging verbosity use the "level" argument. Such as
    logging.INFO or logging.DEBUG.

    Example:
        chain = figaro(template=template, verbose=True, level=logging.DEBUG)

7) Intended Use Case

    The intended use case is to wrap multiple complex Gen AI prompts into
    a function that is easy to read and understand.

    Example:

        def my_llm_chain(args):
            template = "...."
            chain = figaro(template=template)
            result = chain(argument1=args)
            return result

"""

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
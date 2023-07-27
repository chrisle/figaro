import figaro

chain = figaro(\
"""
{# Generate 5 US states #}

{% block us_states %}
  Generate the name of a random US state.
  Return only the abbriviated name of the state. Example: CA
  {% gen vertexai 'capital' model='text-bison' n=5 %}
{% endblock %}

""")

chain(us_state="California")

import figaro

chain = figaro("""You are an AI assistant. Answer the following question:
What is the capital of {{us_state}}?

{% gen vertexai 'capital' model='text-bison' %}

What is it's population?

{% gen vertexai 'population' model='text-bison' %}
""")

chain(us_state="California")

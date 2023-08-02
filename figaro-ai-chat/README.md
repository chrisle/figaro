
# (Coming Soon) Simple Chatbot Agent

```py
import figaro_chat
from flask import Flask

app = Flask(__name__)

personality = "You are a chat bot that speaks like a pirate."
prompt_template = "Answer the following question: {{query}}"
chatbot = figaro_chat(personality=personality, prompt_template=prompt_template)

@app.route("/chat", methods=["POST"])
def hello_ai():
    """Return response from AI.

    Example:
      POST /chat
      { "query": "Write me a poem." }
    """

    query = request.form.get('query')
    response = chatbot(query=query)
    return jsonify(data=response)
```
## (Coming Soon) Figaro Memory

Module for extending a Figaro chain with a vector store.

Features:

  * [ ] Summarizing memory
  * [ ] Embedding
  * [ ] Vector storage with selectable vector store
  * [ ] Index storage with user selectable storage
  * [ ] Nearest neighbor search

```py
import figaro
import figaro_memory

def answer_question_based_on_docs(query):
    template = """
    The user originally asked the following question:
    {{ query }}

    Relevant entries in my database about that topic:
    {% for entry in entries %}
      Page number: {{ entry.metadata.pdf.page_number }}
      Summary: {{ entry.content }}
      Link: {{ entry.metadata.self_link }}
    {% endfor %}

    Answer the above user's question given the above relevant entries.
    Return an object that looks like this:
    {
      "query": "<query>",
      "answer": "<answer>",
      "documents": [
        {
          "page_number": "<page_number>"
          "summary": "<summary>"
          "link": "<self_link>"
        }
      ]
    {% gen vertexai "response" model="code-bison" %}
    """

    # Find relevant information about the multi-cloud solutions from your
    # internal documents.
    entries = figaro_memory(query=query, verbose=True)

    # Create a Figaro prompt chain.
    chain = figaro(template=template, verbose=True)

    # Feed the results from internal documents to the chain and answer the
    # user's question.
    return chain(query=query, entries=entries, type=dict)

answer = answer_question_based_on_docs("Describe an database migraions but using our ABCD managament framework.")
print(answer)
```

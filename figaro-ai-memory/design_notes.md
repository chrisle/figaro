memory should provide the following services

- general text summarization

- document search
  - create embedding from text
  - vector store
    - add
    - delete
    - update
    - find
      - filter by
  - text (aka snippet) stores
    - add
    - delete
    - update
    - find
  - unified vector store and index data type

```py

import figaro_memory
from figaro_memory import DocumentCollection

# Document Collection on Google Matching Engine + GCS
collection = DocumentCollection(
  name="collection_name",
  vector_store=figaro_memory.vector_stores.vertex_ai.matching_engine.get_vector_store(index_id="someID"),
  text_store=figaro_memory.text_stores.google.cloud_storage.get_text_store(bucket="gs://bucket_name"),
  embed_model=figaro_memory.embed_models.vertex_ai.get_embed_model(model="textembedding-gecko@001")
)

# Document Collection on Google Matching Engine + Firestore
collection = DocumentCollection(
  name="collection_name",
  vector_store=figaro_memory.vector_stores.vertex_ai.matching_engine(index_id="some-index"),
  text_store=figaro_memory.text_stores.google.firestore(collection="some-collection-name"),
  embed_model=figaro_memory.embed_models.vertex_ai.get_embed_model(model="textembedding-gecko@001")
)

# Document Collection on Pinecone (since vector and text are in the same database)
collection = DocumentCollection(
  name="collection_name",
  vector_store=figaro_memory.vector_stores.pinecone.get_vector_store(index_id="someID"),
  text_store=figaro_memory.text_stores.pinecone.get_text_store(index_id="someID"),
  embed_model=figaro_memory.embed_models.openai.get_embed_model(embed_model="text-embedding-ada-002")
)

# Add text snippet
doc_id = collection.upsert(
  content="Text to add",
  metadata={
    "self_link": "gs://path/to/document",
    "source": "something",
    "allow": ['chris@domain.com']
  }
)

# Find documents
docs = collection.find(
  query="Find info about this",
  max_results=10,
  lazy_fetch=False, # False does not return text. True returns text.
  filters={
    "metadata": {
      "allow": ["chris@domain.com"]
    }
  }
)
for doc in docs:
  print(doc)

# Update a document in the collection
collection.update("some doc id",
  content="Text to add",
  metadata={
    "self_link": "gs://path/to/document",
    "source": "something",
    "allow": ['chris@domain.com']
  }
)

# Delete text snippet
collection.delete(doc_id=doc_id)
collection.delete_all()
```

-----------------------------------------------------------------------------

- memory api
  - document search
    - combine vector + index store
      - input: query + filter
      - return: summary
  - conversation history
    - history (session id)
      - create
      - delete
      - rename
      - return history
      - return summary of whole conversation
    - conversation
      - should be completely async
      - add one message
      - remove one message
      - auto summarize when changed

```py
import figaro_memory
from figaro_memory import ConversationHistory

# List all conversations
conversations = ConversationHistory.get_sessions(
  where={
    "owner_id": "some id",
    "created_at": "> some date"
  }
) # [{ id: "123456", title: "something", created_at: "timestamp" }, ...]

# Get one session
session = ConversationHistory.get_session("123456", roles={ "user": "Chris", "ai": "AI" })
print(session.message_count)
print(session.title)
session.title = "something"
print(session.summary) # summary of entire session.

# Add message
message = seession.append(role_type="user", content="hello ai!")
message.up_vote() # 1
message.down_vote() # -1
message.clear_vote() # 0

# Get last 10 messages
messages = session.get_messages(last_n=10)
# Get messages between X and Y.
messages = session.get_messages(before="some date", after="some other date")
for message in messages:
  print(message.role_type) # "user"
  print(message.role_name) # "Chris"
  print(message.content) # "hello ai!"
  print(message.vote) # -1, 0, 1

# Summarize these 10 messages
message_summary = messages.summarize() # summarize all intents.
print(message_summary.content) # "user and ai has conversation about something"
print(message_summary.average_vote) # number between -1 and 1

# Delete one message from session
message.delete_all()
session.delete(before="some date", after="some date")
session.delete(message_id="message_id")
session.delete(last_n=10)
```
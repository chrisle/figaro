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
  - index store
    - add
    - delete
    - update
    - find
  - unified vector store and index data type

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

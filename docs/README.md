# Figaro

## Introduction

Figaro is a framework for developing applications powered by large language
models.

The main value that Figaro brings are:

* Figaro allows you to develop prompts and build around LLM faster by combining
  the familiarity of Jinja templates and an easy to understand programming
  pattern.
* Figaro is vendor agnosti allowing you to swap or combine different AI
  vendors such as Google Vertex AI or OpenAI ChatPT.
* Figaro extensions (like chat, memory, etc) are separate so you only need to
  import the parts you need.

## Installation

```
# Install Figaro core
pip install figaro-ai

# (Optional) Install Figaro chat extension
pip install figaro-ai-chat

# (Optional) Install Figaro memory extension
pip install figaro-ai-memory

# (Optional) Install Figaro tools
pip install figaro-ai-tools
```

## Quick Start
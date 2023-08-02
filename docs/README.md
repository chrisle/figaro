# Figaro

Simplify working with prompt chains and multiple LLMs for generative AI in your
application.

Figaro is a versatile set of tools designed to streamline prompt chains and
multiple LLMs usage. With the power of Jinja templates, creating prompts becomes
effortless. Moreover, you can selectively import additional features like chat,
memory, and tools, tailoring the library to suit your specific needs. Enhance
your application with generative AI capabilities using Figaro.

## Getting Started

### Installing Figaro

> 🚨 **NOTE**: Figaro has not been uploaded to PyPI yet. So the below commands
> won't work.

```bash
# Install Figaro core
pip install figaro-ai
```

```bash
# (Optional) Install Figaro chat extension
pip install figaro-ai-chat
```

```bash
# (Optional) Install Figaro memory extension
pip install figaro-ai-memory
```

```bash
# (Optional) Install Figaro tools
pip install figaro-ai-tools
```

## Examples

[**BARD 2: Simple Example**](../examples/vertex_ai_simple.py)</br> Simple
example of creating a prompt and getting a response back from Vertex AI using
Figaro.

## Figaro Documentation

[**Figaro**](figaro-ai/README.md)</br> Main module for Figaro.

[**Figaro Chat**](figaro-chat/README.md)</br> Figaro Module for creating a turn
based chat bot that includes user sessions, conversation history, and chat
summarization.

[**Figaro Memory**](figaro-chat/README.md)</br> Figaro module for using vector
store and index databases.

[**Figaro Tools**](figaro-chat/README.md)</br> Figaro module that contains
various LLM tools and instructions for creating custom tools.

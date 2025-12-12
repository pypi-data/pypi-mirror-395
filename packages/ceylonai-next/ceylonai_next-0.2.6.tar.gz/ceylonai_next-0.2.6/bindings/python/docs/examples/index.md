# Examples Overview

Welcome to the Ceylon AI examples! This section provides comprehensive, step-by-step tutorials for building various types of agents and systems.

## Categories

### 🚀 Basic Examples

Perfect for getting started with Ceylon AI:

- [**Simple Agent**](basic/simple-agent.md) - Create your first agent with custom message handling
- [**LLM Conversation**](basic/llm-conversation.md) - Build an intelligent conversational agent
- [**Custom Actions**](basic/custom-actions.md) - Add tools and actions to your agents

### 💾 Memory Examples

Learn to build agents with memory:

- [**Basic Memory**](memory/basic-memory.md) - Store and retrieve information
- [**Agent Memory Integration**](memory/agent-memory.md) - Agents that remember conversations
- [**Custom Memory Backend**](memory/custom-memory.md) - Build your own storage solution

### ⚡ Async Examples

Build high-performance async agents:

- [**Async LLM Operations**](async/async-llm.md) - Concurrent LLM queries
- [**Concurrent Queries**](async/concurrent-queries.md) - Process multiple requests in parallel
- [**Async Agents**](async/async-agents.md) - Async message handlers

### 📚 RAG Examples

Retrieval-Augmented Generation patterns:

- [**Basic RAG**](rag/basic-rag.md) - Simple RAG implementation
- [**Markdown RAG System**](rag/markdown-rag.md) - Advanced RAG with markdown documents
- [**RAG Web Application**](rag/web-app.md) - Full-stack RAG web app

## Quick Navigation

### By Skill Level

**Beginner** (Start here!)
- Simple Agent
- LLM Conversation
- Basic Memory

**Intermediate**
- Custom Actions
- Agent Memory Integration
- Async LLM Operations

**Advanced**
- Custom Memory Backend
- Markdown RAG System
- RAG Web Application

### By Use Case

**Chatbots & Assistants**
- LLM Conversation
- Agent Memory Integration
- Async LLM Operations

**Knowledge Management**
- Basic RAG
- Markdown RAG System
- Custom Memory Backend

**Multi-Agent Systems**
- Simple Agent
- Custom Actions
- Async Agents

**Production Applications**
- RAG Web Application
- Custom Memory Backend
- Concurrent Queries

## Example Structure

Each example includes:

- **📖 Overview**: What you'll build and learn
- **🎯 Prerequisites**: What you need before starting
- **📝 Step-by-Step Guide**: Detailed implementation
- **💡 Key Concepts**: Important ideas explained
- **🔧 Complete Code**: Full working implementation
- **🚀 Running the Example**: How to test it
- **📚 Next Steps**: Where to go from here

## Get the Code

All examples are available in the Ceylon repository:

```bash
git clone https://github.com/ceylonai/next-processor.git
cd next-processor/bindings/python/examples
```

## Running Examples

### Prerequisites

1. Install Ceylon AI:
   ```bash
   pip install ceylonai-next
   ```

2. For LLM examples, install Ollama:
   ```bash
   # Visit https://ollama.ai for installation
   ollama pull llama3.2:latest
   ```

### Run an Example

```bash
# Navigate to examples directory
cd examples

# Run an example
python demo_simple_agent.py
python demo_conversation.py
python demo_async_llm.py
```

## Example Index

### Basic Examples

| Example | Description | Difficulty | Time |
|---------|-------------|------------|------|
| [Simple Agent](basic/simple-agent.md) | Create a basic agent with message handling | ⭐ | 10 min |
| [LLM Conversation](basic/llm-conversation.md) | Build an LLM-powered chatbot | ⭐ | 15 min |
| [Custom Actions](basic/custom-actions.md) | Add custom tools to your agent | ⭐⭐ | 20 min |

### Memory Examples

| Example | Description | Difficulty | Time |
|---------|-------------|------------|------|
| [Basic Memory](memory/basic-memory.md) | Store and retrieve information | ⭐ | 15 min |
| [Agent Memory](memory/agent-memory.md) | Agents with conversation memory | ⭐⭐ | 20 min |
| [Custom Memory](memory/custom-memory.md) | Build custom storage backend | ⭐⭐⭐ | 30 min |

### Async Examples

| Example | Description | Difficulty | Time |
|---------|-------------|------------|------|
| [Async LLM](async/async-llm.md) | Concurrent LLM operations | ⭐⭐ | 20 min |
| [Concurrent Queries](async/concurrent-queries.md) | Process requests in parallel | ⭐⭐ | 25 min |
| [Async Agents](async/async-agents.md) | Async message handlers | ⭐⭐⭐ | 30 min |

### RAG Examples

| Example | Description | Difficulty | Time |
|---------|-------------|------------|------|
| [Basic RAG](rag/basic-rag.md) | Simple RAG implementation | ⭐⭐ | 25 min |
| [Markdown RAG](rag/markdown-rag.md) | Advanced RAG system | ⭐⭐⭐ | 45 min |
| [Web App](rag/web-app.md) | Full-stack RAG application | ⭐⭐⭐ | 60 min |

## Learning Path

### Path 1: Chatbot Developer

1. [Simple Agent](basic/simple-agent.md) - Learn the basics
2. [LLM Conversation](basic/llm-conversation.md) - Add intelligence
3. [Agent Memory Integration](memory/agent-memory.md) - Add memory
4. [Async LLM Operations](async/async-llm.md) - Improve performance

### Path 2: RAG Developer

1. [Basic Memory](memory/basic-memory.md) - Understand storage
2. [LLM Conversation](basic/llm-conversation.md) - LLM integration
3. [Basic RAG](rag/basic-rag.md) - Simple RAG pattern
4. [Markdown RAG System](rag/markdown-rag.md) - Production RAG

### Path 3: Full-Stack Developer

1. [Simple Agent](basic/simple-agent.md) - Basics
2. [Custom Actions](basic/custom-actions.md) - Tool integration
3. [Async Operations](async/async-llm.md) - Performance
4. [Web Application](rag/web-app.md) - Full application

## Code Snippets

### Quick Start: Basic Agent

```python
from ceylonai_next import Agent

class MyAgent(Agent):
    def on_message(self, message, context=None):
        return f"Received: {message}"

agent = MyAgent("my_agent")
print(agent.send_message("Hello!"))
```

### Quick Start: LLM Agent

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.build()

response = agent.send_message("What is Python?")
print(response)
```

### Quick Start: Memory

```python
from ceylonai_next import InMemoryBackend, MemoryEntry

memory = InMemoryBackend()
entry = MemoryEntry("Important fact")
entry.with_metadata("type", "knowledge")
memory.store(entry)
```

### Quick Start: Async

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    tasks = [
        agent.send_message_async("Query 1"),
        agent.send_message_async("Query 2")
    ]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

## Common Patterns

### Pattern: Conversational Agent

```python
from ceylonai_next import LlmAgent, InMemoryBackend

memory = InMemoryBackend()
agent = LlmAgent("chatbot", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.with_system_prompt("You are a friendly chatbot.")
agent.build()

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = agent.send_message(user_input)
    print(f"Bot: {response}")
```

### Pattern: Tool-Using Agent

```python
from ceylonai_next import LlmAgent, PyAction
import datetime

def get_time(context, inputs):
    return datetime.datetime.now().strftime("%H:%M:%S")

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.register_action(
    PyAction("get_time", "Get current time", '{}', None)
)
agent.build()

response = agent.send_message("What time is it?")
```

### Pattern: RAG Agent

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Build knowledge base
knowledge = ["Fact 1", "Fact 2", "Fact 3"]
memory = InMemoryBackend()
for fact in knowledge:
    entry = MemoryEntry(fact)
    memory.store(entry)

# Create RAG agent
agent = LlmAgent("rag", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.with_system_prompt("Answer using the knowledge base.")
agent.build()

answer = agent.send_message("Tell me about...")
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'ceylon'**
```bash
pip install ceylonai-next
```

**RuntimeError: Agent not built**
```python
# Always call build() before using
agent.build()
```

**Connection refused (Ollama)**
```bash
# Make sure Ollama is running
ollama serve
```

**Model not found**
```bash
# Pull the model first
ollama pull llama3.2:latest
```

## Getting Help

- **Documentation**: [User Guide](../guide/agents/overview.md)
- **API Reference**: [API Docs](../api/core/agent.md)
- **GitHub**: [Issues](https://github.com/ceylonai/next-processor/issues)

## Contributing Examples

Have a cool example? We'd love to include it!

1. Fork the repository
2. Add your example to `examples/`
3. Create documentation in `docs/examples/`
4. Submit a pull request

See [Contributing Guide](../contributing/docs.md) for details.

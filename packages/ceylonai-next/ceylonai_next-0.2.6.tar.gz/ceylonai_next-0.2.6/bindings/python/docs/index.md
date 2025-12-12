# Ceylon AI - Agent Mesh Framework

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Fast to Get Started__

    ---

    Install Ceylon AI with `pip` and get your first agent running in minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-lightning-bolt:{ .lg .middle } __Built on Rust__

    ---

    High-performance Rust core with Python bindings for the best of both worlds

    [:octicons-arrow-right-24: Architecture](getting-started/concepts.md)

-   :material-brain:{ .lg .middle } __LLM-Powered__

    ---

    Seamless integration with multiple LLM providers including Ollama, OpenAI, and Claude

    [:octicons-arrow-right-24: LLM Guide](guide/llm/overview.md)

-   :material-memory:{ .lg .middle } __Memory System__

    ---

    Built-in memory backends with support for custom implementations and RAG patterns

    [:octicons-arrow-right-24: Memory Guide](guide/memory/overview.md)

</div>

## What is Ceylon AI?

**Ceylon AI** is a powerful, production-ready framework for building **local and distributed AI agent systems**. Built with a high-performance Rust core and intuitive Python bindings, it provides everything you need to create intelligent, autonomous agents that can:

- 🤖 **Communicate** through a flexible mesh architecture
- 🧠 **Think** using state-of-the-art LLMs
- 💾 **Remember** with built-in memory backends
- 🔧 **Act** using a powerful action/tool system
- ⚡ **Scale** with async/await support

## Key Features

### 🎯 Simple and Intuitive API

```python
from ceylonai_next import LlmAgent

# Create an LLM-powered agent in 3 lines
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful coding assistant.")
agent.build()

# Start chatting
response = agent.send_message("What is Python?")
print(response)
```

!!! tip "Import Alias"
    For convenience, you can use a shorter import alias:
    ```python
    import ceylonai_next as ceylon

    agent = ceylon.LlmAgent("assistant", "ollama::llama3.2:latest")
    ```

### 🔌 Multiple LLM Providers

Ceylon AI supports all major LLM providers out of the box:

- **Ollama** - Local LLM inference
- **OpenAI** - GPT-3.5, GPT-4, and more
- **Anthropic** - Claude models
- **Custom** - Easy to add your own providers

### 🛠️ Powerful Action System

Define custom actions with automatic schema generation:

```python
from ceylonai_next import Agent

class MyAgent(Agent):
    @Agent.action(name="calculate", description="Perform calculations")
    def calculate(self, expression: str) -> float:
        """Evaluate a mathematical expression."""
        return eval(expression)  # Don't do this in production!
```

### 💾 Flexible Memory System

Built-in memory backends with support for RAG (Retrieval-Augmented Generation):

```python
from ceylonai_next import InMemoryBackend, MemoryEntry

# Create a memory backend
memory = InMemoryBackend.with_max_entries(1000)

# Store memories with metadata
entry = MemoryEntry("Important fact about AI")
entry.with_metadata("category", "knowledge")
entry.with_ttl_seconds(3600)  # Expires in 1 hour
memory.store(entry)

# Use with agents
agent = LlmAgent("smart_agent", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.build()
```

### ⚡ Async/Await Support

Built for modern Python with full async support:

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    # Concurrent queries
    tasks = [
        agent.send_message_async("What is Python?"),
        agent.send_message_async("What is Rust?"),
        agent.send_message_async("What is AI?")
    ]

    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)

asyncio.run(main())
```

### 🌐 Mesh Networking

Connect agents in a flexible mesh architecture:

```python
from ceylonai_next import LocalMesh, Agent

# Create a mesh
mesh = LocalMesh()

# Register multiple agents
agent1 = Agent("agent1")
agent2 = Agent("agent2")

mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Agents can now communicate
mesh.send_message("agent1", "agent2", "Hello!")
```

## Installation

Install Ceylon AI using pip:

```bash
pip install ceylonai-next
```

For development or from source:

```bash
# Clone the repository
git clone https://github.com/ceylonai/next-processor.git
cd next-processor/bindings/python

# Install with pip
pip install -e .
```

See the [Installation Guide](getting-started/installation.md) for more details.

## Quick Example

Here's a complete example showing the power of Ceylon AI:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Create memory backend
memory = InMemoryBackend()

# Store some knowledge
entry = MemoryEntry("Ceylon is a Rust-based agent framework")
entry.with_metadata("topic", "framework")
memory.store(entry)

# Create an LLM agent with memory
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful assistant with memory.")
agent.with_memory(memory)
agent.with_temperature(0.7)
agent.build()

# Chat with the agent
response = agent.send_message("Tell me about Ceylon")
print(response)
```

## Architecture

Ceylon AI is built with a layered architecture:

```
┌─────────────────────────────────────┐
│     Python Application Layer        │  ← Your Code
├─────────────────────────────────────┤
│     Python Bindings (PyO3)          │  ← Ceylon Python API
├─────────────────────────────────────┤
│     Rust Runtime Core               │  ← High-Performance Core
│  ┌─────────┬─────────┬───────────┐  │
│  │  Agents │   Mesh  │  Memory   │  │
│  ├─────────┼─────────┼───────────┤  │
│  │   LLM   │ Actions │  Context  │  │
│  └─────────┴─────────┴───────────┘  │
└─────────────────────────────────────┘
```

- **Python Layer**: Intuitive, Pythonic API for application development
- **Rust Core**: High-performance, memory-safe runtime
- **PyO3 Bindings**: Seamless integration between Python and Rust

Learn more about the [Architecture](getting-started/concepts.md).

## Use Cases

Ceylon AI is perfect for:

- 🤖 **AI Assistants** - Build intelligent conversational agents
- 📚 **RAG Systems** - Create knowledge bases with semantic search
- 🔄 **Multi-Agent Systems** - Orchestrate multiple agents working together
- 🌐 **Distributed AI** - Scale agents across multiple nodes
- 🧪 **Research** - Experiment with agent architectures and AI workflows

## Next Steps

<div class="grid cards" markdown>

-   [:material-book-open-page-variant: **Getting Started**](getting-started/installation.md)

    Learn how to install and set up Ceylon AI

-   [:material-code-braces: **User Guide**](guide/agents/overview.md)

    Deep dive into agents, actions, memory, and more

-   [:material-application: **Examples**](examples/index.md)

    Explore complete examples and tutorials

-   [:material-api: **API Reference**](api/core/agent.md)

    Detailed API documentation for all components

</div>

## Community & Support

- **GitHub**: [github.com/ceylonai/next-processor](https://github.com/ceylonai/next-processor)
- **Issues**: [Report bugs or request features](https://github.com/ceylonai/next-processor/issues)
- **PyPI**: [pypi.org/project/ceylonai-next](https://pypi.org/project/ceylonai-next/)

## License

Ceylon AI is released under the [MIT License](https://github.com/ceylonai/next-processor/blob/main/LICENSE).

---

**Ready to build your first agent?** Start with the [Quick Start Guide](getting-started/quickstart.md)!

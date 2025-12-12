# Quick Start

Get started with Ceylon AI in 5 minutes! This guide will walk you through creating your first agent and exploring core features.

## Prerequisites

Make sure you have Ceylon AI installed:

```bash
pip install ceylonai-next
```

!!! tip "Import Alias"
    The package name is `ceylonai-next` but imports as `ceylonai_next`. For convenience, use an alias:
    ```python
    import ceylonai_next as ceylon

    agent = ceylon.LlmAgent("assistant", "ollama::llama3.2:latest")
    ```

## Your First Agent

### 1. Basic Agent

Create a simple agent that responds to messages:

```python
from ceylonai_next import Agent

# Create an agent
agent = Agent("greeter")

# Send a message
response = agent.send_message("Hello, Ceylon!")
print(response)  # Output: "Message received"
```

### 2. Custom Message Handler

Override the `on_message` method to customize behavior:

```python
from ceylonai_next import Agent

class GreeterAgent(Agent):
    def on_message(self, message, context=None):
        return f"You said: {message}"

# Create and use the agent
agent = GreeterAgent("greeter")
response = agent.send_message("Hello!")
print(response)  # Output: "You said: Hello!"
```

## LLM-Powered Agent

Create an intelligent agent using a Large Language Model:

### With Ollama (Local)

```python
from ceylonai_next import LlmAgent

# Create an LLM agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful Python programming assistant.")
agent.with_temperature(0.7)
agent.build()

# Chat with the agent
response = agent.send_message("What is a Python decorator?")
print(response)
```

### With OpenAI

```python
from ceylonai_next import LlmAgent

# Create an OpenAI-powered agent
agent = LlmAgent("gpt_assistant", "openai::gpt-4")
agent.with_api_key("your-api-key")  # Or set OPENAI_API_KEY env var
agent.with_system_prompt("You are a helpful assistant.")
agent.build()

# Chat with the agent
response = agent.send_message("Explain async/await in Python")
print(response)
```

## Adding Custom Actions

Define custom tools/actions for your agent:

```python
from ceylonai_next import Agent

class CalculatorAgent(Agent):
    def __init__(self):
        super().__init__("calculator")

    @Agent.action(
        name="add",
        description="Add two numbers together"
    )
    def add(self, a: int, b: int) -> int:
        """Add two integers."""
        return a + b

    @Agent.action(
        name="multiply",
        description="Multiply two numbers"
    )
    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers."""
        return a * b

# Create agent
agent = CalculatorAgent()

# Actions are automatically registered and can be invoked
# by LLM agents or through the tool invoker
```

## Adding Memory

Give your agent memory capabilities:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Create a memory backend
memory = InMemoryBackend.with_max_entries(100)

# Store some information
entry = MemoryEntry("Ceylon is a Rust-based agent framework for Python")
entry.with_metadata("category", "knowledge")
entry.with_metadata("importance", "high")
memory.store(entry)

# Create agent with memory
agent = LlmAgent("smart_assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a knowledgeable assistant.")
agent.with_memory(memory)
agent.build()

# The agent can now access stored memories
response = agent.send_message("What do you know about Ceylon?")
print(response)
```

## Async Operations

Use async/await for concurrent operations:

```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    # Create agent
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt("You are a helpful assistant.")
    agent.build()

    # Send multiple queries concurrently
    queries = [
        "What is Python?",
        "What is Rust?",
        "What is machine learning?"
    ]

    # Execute all queries in parallel
    tasks = [agent.send_message_async(q) for q in queries]
    responses = await asyncio.gather(*tasks)

    # Print results
    for query, response in zip(queries, responses):
        print(f"\nQ: {query}")
        print(f"A: {response}")

# Run the async function
asyncio.run(main())
```

## Multi-Agent System

Create multiple agents that communicate through a mesh:

```python
from ceylonai_next import LocalMesh, Agent

class Agent1(Agent):
    def on_message(self, message, context=None):
        return f"Agent1 received: {message}"

class Agent2(Agent):
    def on_message(self, message, context=None):
        return f"Agent2 received: {message}"

# Create mesh
mesh = LocalMesh()

# Create and register agents
agent1 = Agent1("agent1")
agent2 = Agent2("agent2")

mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Agents can now communicate
# (This is a simplified example - see Mesh guide for details)
```

## Complete Example

Here's a complete example combining multiple features:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry
import asyncio

async def main():
    # Setup memory
    memory = InMemoryBackend()

    # Store knowledge
    facts = [
        "Python was created by Guido van Rossum",
        "Rust is a systems programming language",
        "Ceylon AI is built with Rust and Python"
    ]

    for fact in facts:
        entry = MemoryEntry(fact)
        entry.with_metadata("type", "fact")
        memory.store(entry)

    # Create intelligent agent
    agent = LlmAgent("knowledgeable_assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt(
        "You are a knowledgeable assistant. "
        "Use the information in your memory to answer questions accurately."
    )
    agent.with_memory(memory)
    agent.with_temperature(0.7)
    agent.with_max_tokens(500)
    agent.build()

    # Interactive chat
    questions = [
        "Who created Python?",
        "Tell me about Rust",
        "What is Ceylon AI?"
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")

        response = await agent.send_message_async(question)
        print(f"Answer: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Common Patterns

### Builder Pattern

Ceylon uses a fluent builder pattern for configuration:

```python
agent = (LlmAgent("assistant", "ollama::llama3.2:latest")
    .with_system_prompt("You are helpful")
    .with_temperature(0.8)
    .with_max_tokens(1000)
    .with_memory(memory)
    .build())
```

### Error Handling

```python
try:
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()
    response = agent.send_message("Hello!")
except Exception as e:
    print(f"Error: {e}")
```

### Configuration from Environment

```python
import os
from ceylonai_next import LlmAgent

# Set environment variables
os.environ["LLM_MODEL"] = "ollama::llama3.2:latest"
os.environ["TEMPERATURE"] = "0.7"

# Use in code
model = os.getenv("LLM_MODEL")
temp = float(os.getenv("TEMPERATURE", "0.7"))

agent = LlmAgent("assistant", model)
agent.with_temperature(temp)
agent.build()
```

## What's Next?

Now that you've seen the basics, explore:

- [**Your First Agent**](first-agent.md) - Detailed walkthrough of building an agent
- [**Core Concepts**](concepts.md) - Understanding Ceylon's architecture
- [**Agents Guide**](../guide/agents/overview.md) - Deep dive into agent types
- [**LLM Guide**](../guide/llm/overview.md) - Working with language models
- [**Memory Guide**](../guide/memory/overview.md) - Implementing memory systems
- [**Examples**](../examples/index.md) - Complete examples and tutorials

## Tips for Success

1. **Start Simple**: Begin with basic agents, add complexity gradually
2. **Use Type Hints**: Type hints enable automatic schema generation
3. **Handle Errors**: Always wrap LLM calls in try-except blocks
4. **Monitor Costs**: Be aware of API costs when using cloud LLM providers
5. **Test Locally**: Use Ollama for development and testing
6. **Go Async**: Use async operations for better performance

## Getting Help

- **Documentation**: Browse the full [User Guide](../guide/agents/overview.md)
- **Examples**: Check out [Examples](../examples/index.md)
- **GitHub**: Report issues at [github.com/ceylonai/next-processor/issues](https://github.com/ceylonai/next-processor/issues)

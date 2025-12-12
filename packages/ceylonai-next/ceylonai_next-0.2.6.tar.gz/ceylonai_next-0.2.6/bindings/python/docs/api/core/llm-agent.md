# LlmAgent

The `LlmAgent` class provides a high-level interface for creating agents powered by Large Language Models (LLMs). It supports multiple LLM providers, fluent builder API, memory integration, and both synchronous and asynchronous message handling.

## Class Signature

```python
class LlmAgent:
    def __init__(
        self,
        name_or_mesh: str | LocalMesh,
        model_or_name: str | None = None,
        config: LlmConfig | None = None,
        memory: InMemoryBackend | Memory | None = None
    ) -> None:
        ...
```

## Description

`LlmAgent` is a Python wrapper around `PyLlmAgent` that simplifies creating LLM-powered agents with a fluent builder API. It handles LLM provider configuration, system prompts, temperature settings, token limits, and memory backends.

## Constructors

### Constructor 1: Simple Model String

```python
LlmAgent(name: str, model: str, memory: InMemoryBackend | None = None)
```

Creates an agent with a model string (e.g., `"ollama::llama3.2:latest"`).

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | Required | Agent identifier |
| `model` | `str` | Required | Model string in format `provider::model_name` |
| `memory` | `InMemoryBackend \| Memory \| None` | `None` | Optional memory backend |

**Returns:** LlmAgent instance (requires calling `.build()`)

**Example:**
```python
from ceylonai_next import LlmAgent

# Create agent with Ollama model
agent = LlmAgent("my-agent", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful assistant.")
agent.with_temperature(0.7)
agent.build()
```

### Constructor 2: Mesh with Config

```python
LlmAgent(mesh: LocalMesh, name: str, config: LlmConfig, memory: InMemoryBackend | None = None)
```

Creates an agent with a config object and automatically registers it with a mesh.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mesh` | `LocalMesh` | Required | Mesh to register agent with |
| `name` | `str` | Required | Agent identifier |
| `config` | `LlmConfig` | Required | LLM configuration object |
| `memory` | `InMemoryBackend \| Memory \| None` | `None` | Optional memory backend |

**Returns:** LlmAgent instance (auto-built)

**Example:**
```python
from ceylonai_next import LlmAgent, LlmConfig, LocalMesh

mesh = LocalMesh()
config = (LlmConfig.builder()
    .provider("ollama")
    .model("llama2")
    .temperature(0.5)
    .build())

agent = LlmAgent(mesh, "my-agent", config)
# Already built and registered with mesh
response = agent.send_message("Hello!")
```

## Configuration Methods

### `with_api_key(api_key: str) -> LlmAgent`

Set the API key for the LLM provider.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | API key for the provider (e.g., OpenAI key) |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
import os
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "openai::gpt-4")
agent.with_api_key(os.getenv("OPENAI_API_KEY"))
agent.with_system_prompt("You are a helpful assistant.")
agent.build()
```

---

### `with_system_prompt(prompt: str) -> LlmAgent`

Set the system prompt that defines the agent's behavior and personality.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `str` | System prompt text (can be multi-line) |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
agent = LlmAgent("expert", "ollama::gemma:latest")
agent.with_system_prompt("""
You are an expert Python developer.
- Provide clear, well-commented code
- Explain your reasoning
- Ask clarifying questions when needed
""")
agent.build()
```

---

### `with_temperature(temperature: float) -> LlmAgent`

Set the sampling temperature for generation (controls randomness).

**Parameters:**

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `temperature` | `float` | 0.0 - 2.0 | Lower = more deterministic, Higher = more random |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
# For creative tasks
creative_agent = LlmAgent("storyteller", "ollama::llama2")
creative_agent.with_temperature(1.2)

# For factual tasks
factual_agent = LlmAgent("calculator", "ollama::llama2")
factual_agent.with_temperature(0.3)
```

---

### `with_max_tokens(tokens: int) -> LlmAgent`

Set the maximum number of tokens to generate per response.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `tokens` | `int` | Maximum token count (provider-dependent) |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
# For concise responses
agent = LlmAgent("summarizer", "ollama::mistral:latest")
agent.with_max_tokens(100)  # Short summaries

# For detailed responses
agent2 = LlmAgent("writer", "ollama::llama2")
agent2.with_max_tokens(2000)  # Longer content
```

---

### `with_memory(memory: InMemoryBackend | Memory) -> LlmAgent`

Set the memory backend for the agent.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `memory` | `InMemoryBackend \| Memory` | Memory backend instance |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
from ceylonai_next import LlmAgent, InMemoryBackend

# Simple in-memory backend
agent = LlmAgent("chatbot", "ollama::llama3.2:latest")
memory = InMemoryBackend.with_max_entries(100)
agent.with_memory(memory)
agent.build()

# With custom memory
class VectorMemory(Memory):
    def store(self, entry):
        # Custom storage logic
        pass
    # ... implement other methods

agent2 = LlmAgent("assistant", "ollama::llama2")
agent2.with_memory(VectorMemory())
```

---

### `build() -> LlmAgent`

Build/compile the agent configuration. Must be called before sending messages.

**Parameters:** None

**Returns:** `LlmAgent` - Returns self for method chaining

**Raises:** `RuntimeError` - If required configuration is missing

**Example:**
```python
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.with_temperature(0.7)
agent.with_max_tokens(512)
agent.build()

# Now ready to send messages
response = agent.send_message("Hello!")
```

---

### `register_action(action: PyAction) -> LlmAgent`

Register a Python action with the agent.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `PyAction` | Action instance to register |

**Returns:** `LlmAgent` - Returns self for method chaining

**Example:**
```python
from ceylonai_next import LlmAgent, PyAction
import json

class WebSearchAction(PyAction):
    def __init__(self):
        schema = json.dumps({
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "num_results": {"type": "integer"}
            },
            "required": ["query"]
        })
        super().__init__("web_search", "Search the web", schema)

    def execute(self, context, inputs):
        query = inputs.get("query", "")
        # Implement search logic
        return f"Found results for: {query}"

agent = LlmAgent("researcher", "ollama::llama2")
agent.register_action(WebSearchAction())
agent.build()
```

## Message Methods

### `send_message(message: str) -> str`

Send a synchronous message to the agent.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | User message |

**Returns:** `str` - Agent's response

**Raises:**
- `RuntimeError` - If agent not built (call `.build()` first)

**Example:**
```python
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful assistant.")
agent.build()

response = agent.send_message("What is Python?")
print(response)
```

---

### `send_message_async(message: str) -> Awaitable[str]`

Send an asynchronous message to the agent. Use for non-blocking operations.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | User message |

**Returns:** `Awaitable[str]` - Coroutine that resolves to agent's response

**Raises:**
- `RuntimeError` - If agent not built

**Example:**
```python
import asyncio
from ceylonai_next import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_temperature(0.7)
    agent.build()

    # Non-blocking message send
    response = await agent.send_message_async("How are you?")
    print(response)

    # Concurrent messages
    responses = await asyncio.gather(
        agent.send_message_async("Question 1"),
        agent.send_message_async("Question 2"),
        agent.send_message_async("Question 3"),
    )
    for resp in responses:
        print(resp)

asyncio.run(main())
```

---

### `query_async(message: str) -> Awaitable[str]`

Alias for `send_message_async()`. Provides alternative naming convention.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | User message |

**Returns:** `Awaitable[str]` - Coroutine that resolves to agent's response

**Example:**
```python
async def chat():
    agent = LlmAgent("gpt-bot", "openai::gpt-4")
    agent.with_api_key("sk-...")
    agent.build()

    # Using query_async alias
    response = await agent.query_async("What's new in Python 3.13?")
    return response
```

## Complete Examples

### Example 1: Basic Chat Agent

```python
from ceylonai_next import LlmAgent

def main():
    # Create and configure agent
    agent = LlmAgent("chatbot", "ollama::llama3.2:latest")
    agent.with_system_prompt(
        "You are a friendly and helpful chatbot. Keep responses concise."
    )
    agent.with_temperature(0.8)
    agent.with_max_tokens(256)
    agent.build()

    # Chat
    messages = [
        "Hello! What can you help me with?",
        "Tell me a joke",
        "What's 2 + 2?",
    ]

    for msg in messages:
        print(f"User: {msg}")
        response = agent.send_message(msg)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
```

### Example 2: Async Agent with Memory

```python
import asyncio
from ceylonai_next import LlmAgent, InMemoryBackend

async def main():
    # Create memory backend
    memory = InMemoryBackend.with_max_entries(50)

    # Create agent with memory
    agent = LlmAgent("smart-assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt(
        "You are a helpful assistant with memory. "
        "Remember important details from the conversation."
    )
    agent.with_memory(memory)
    agent.build()

    # Simulate conversation
    questions = [
        "My name is Alice and I'm a software engineer",
        "What's my name?",
        "What's my profession?",
    ]

    for question in questions:
        print(f"Q: {question}")
        response = await agent.send_message_async(question)
        print(f"A: {response}\n")

asyncio.run(main())
```

### Example 3: Expert Agent with Specific Role

```python
from ceylonai_next import LlmAgent

def create_code_expert():
    """Create a coding expert agent"""
    agent = LlmAgent("code-expert", "ollama::llama2")
    agent.with_system_prompt("""
You are an expert Python developer with 10+ years of experience.
- Write clean, maintainable code
- Follow PEP 8 standards
- Include docstrings and type hints
- Explain complex concepts clearly
- Suggest best practices
    """)
    agent.with_temperature(0.3)  # More deterministic for code
    agent.with_max_tokens(1024)
    agent.build()
    return agent

def main():
    expert = create_code_expert()

    questions = [
        "How do I implement a singleton pattern in Python?",
        "What's the difference between list and tuple?",
        "Show me a good example of a decorator",
    ]

    for question in questions:
        print(f"Q: {question}")
        response = expert.send_message(question)
        print(f"A: {response}\n")

if __name__ == "__main__":
    main()
```

### Example 4: Concurrent Async Queries

```python
import asyncio
from ceylonai_next import LlmAgent

async def process_documents():
    """Process multiple documents concurrently"""
    agent = LlmAgent("summarizer", "ollama::mistral:latest")
    agent.with_system_prompt(
        "Summarize the given text in 2-3 sentences."
    )
    agent.with_max_tokens(150)
    agent.with_temperature(0.5)
    agent.build()

    documents = [
        "Document 1 content...",
        "Document 2 content...",
        "Document 3 content...",
    ]

    # Process all documents concurrently
    summaries = await asyncio.gather(
        *[agent.send_message_async(doc) for doc in documents]
    )

    for i, summary in enumerate(summaries, 1):
        print(f"Document {i} Summary: {summary}\n")

asyncio.run(process_documents())
```

## Related APIs

- **[Agent](./agent.md)** - Base agent class
- **[LlmConfig](../types/llm-config.md)** - LLM configuration builder
- **[InMemoryBackend](../memory/in-memory.md)** - Memory storage backend
- **[Memory](../memory/memory-interface.md)** - Custom memory interface
- **[PyAction](../actions/action.md)** - Action definition

## See Also

- [LLM Configuration Guide](../../guide/llm-config.md)
- [Memory Integration Guide](../../guide/memory.md)
- [Async Agent Examples](../../examples/async-agent.md)
- [LLM Agent Tutorial](../../getting-started/llm-agent.md)

# Ceylon Python Bindings

Python bindings for [Ceylon](https://github.com/ceylonai/ceylon), a Rust-based agent mesh framework for building local and distributed AI agent systems.

## Overview

Ceylon provides a unified API for creating agent-based systems that work seamlessly in both local (in-memory) and distributed (network-based) scenarios. The Python bindings allow you to build sophisticated agent systems using clean Python code while leveraging Rust's performance and safety.

## Features

- 🤖 **Custom Agents**: Create agents with synchronous message handlers
- 🧠 **LLM Integration**: Built-in support for LLM agents (Ollama, OpenAI, etc.)
- ⚡ **Async Support**: Concurrent LLM operations with `send_message_async()`
- 🛠️ **Actions/Tools**: Define custom actions with automatic schema generation
- 🌐 **Mesh Architecture**: Local and distributed agent communication
- 📊 **Metrics & Monitoring**: Built-in metrics for performance, costs, and errors
- 🐍 **Pythonic API**: Fluent builder patterns and decorators

## Installation

```bash
cd bindings/python
pip install -e .
```

## Quick Start

### Simple Agent

```python
from ceylon import Agent, PyLocalMesh

class EchoAgent(Agent):
    def on_message(self, message, context=None):
        print(f"Received: {message}")
        return f"Echo: {message}"

# Create mesh and agent
mesh = PyLocalMesh("my_mesh")
agent = EchoAgent("echo")
mesh.add_agent(agent)

# Send message
mesh.send_to("echo", "Hello!")
```

### LLM Agent (Synchronous)

```python
from ceylon import LlmAgent

# Create and configure
agent = LlmAgent("assistant", "ollama::gemma3:latest")
agent.with_system_prompt("You are a helpful assistant.")
agent.with_temperature(0.7)
agent.with_max_tokens(100)
agent.build()

# Send message
response = agent.send_message("What is 2+2?")
print(response)
```

### LLM Agent (Async)

```python
import asyncio
from ceylon import LlmAgent

async def main():
    agent = LlmAgent("assistant", "ollama::gemma3:latest")
    agent.build()

    # Concurrent queries
    tasks = [
        agent.send_message_async("What is 2+2?"),
        agent.send_message_async("What is 3+3?"),
        agent.send_message_async("What is 5+5?"),
    ]

    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)

asyncio.run(main())
```

### Custom Actions

```python
from ceylon import Agent

class CalculatorAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    @Agent.action(name="add")
    def add(self, a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @Agent.action(name="multiply")
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

# Create agent
agent = CalculatorAgent("calc")

# Invoke actions
result = agent.tool_invoker.invoke("add", '{"a": 5, "b": 3}')
print(result)  # 8
```


### Metrics and Monitoring

Ceylon includes built-in metrics collection for monitoring performance, costs, and errors:

```python
import ceylonai_next as ceylon

# Run your agents...
# mesh.send_to("agent", "message")

# Get metrics snapshot
metrics = ceylon.get_metrics()

# Available metrics
print(f"Messages processed: {metrics['message_throughput']}")
print(f"Avg latency: {metrics['avg_message_latency_us']/1000:.2f} ms")
print(f"LLM tokens used: {metrics['total_llm_tokens']}")
print(f"LLM cost: ${metrics['total_llm_cost_us']/1_000_000:.4f}")
print(f"Memory hit rate: {metrics['memory_hits']/(metrics['memory_hits']+metrics['memory_misses'])*100:.1f}%")
print(f"Errors: {metrics['errors']}")
```

**Key Metrics:**
- `message_throughput` - Total messages processed
- `avg_message_latency_us` - Average message latency (microseconds)
- `avg_agent_execution_time_us` - Average agent execution time (microseconds)
- `total_llm_tokens` - Total LLM tokens consumed
- `avg_llm_latency_us` - Average LLM API latency (microseconds)
- `total_llm_cost_us` - Total LLM cost in micro-dollars ($1 = 1,000,000 μ$)
- `memory_hits`/`memory_misses`/`memory_writes` - Memory operation counts
- `errors` - Dictionary of error types and counts

See [examples/README_METRICS.md](./examples/README_METRICS.md) for detailed examples.

## Examples

Example scripts are located in the `examples/` directory, and tests are in the `tests/` directory.

### Basic Examples

- **`examples/demo_simple_agent.py`** - Basic agent with synchronous message handling

  ```bash
  python examples/demo_simple_agent.py
  ```

- **`examples/demo_conversation.py`** - LLM agent conversation (synchronous)
  ```bash
  python examples/demo_conversation.py
  ```

### Async Examples

- **`examples/demo_async_llm.py`** ⭐ **NEW** - Concurrent LLM operations (recommended)

  ```bash
  python examples/demo_async_llm.py
  ```

  Demonstrates:

  - Concurrent queries with `asyncio.gather()`
  - Streaming responses with `asyncio.as_completed()`
  - Batch processing with concurrency control
  - Error handling in async contexts

- **`examples/demo_async_agent.py`** ✨ **NEW** - Async message handlers and actions

  ```bash
  python examples/demo_async_agent.py
  ```

  Demonstrates:

  - Async `on_message()` handlers
  - Async action execution
  - Thread-local event loop handling


### Metrics Examples

- **`examples/metrics_quickstart.py`** ⚡ **NEW** - Quick start guide for metrics

  ```bash
  python examples/metrics_quickstart.py
  ```

  Demonstrates:

  - Basic metrics collection with `get_metrics()`
  - Retrieving and displaying metrics snapshots

- **`examples/metrics_demo.py`** 📊 **NEW** - Comprehensive metrics demo

  ```bash
  python examples/metrics_demo.py
  ```

  Demonstrates:

  - Message throughput and latency tracking
  - Memory cache hit rate monitoring
  - Error tracking and reporting
  - Continuous monitoring patterns

See [examples/README_METRICS.md](./examples/README_METRICS.md) for complete metrics documentation.

### Test Files

All test files are located in the `tests/` directory:

- `tests/test_actions.py` - Action system tests
- `tests/test_agent_messages.py` - Agent messaging tests
- `tests/test_async_agent.py` - Async functionality tests
- `tests/test_advanced_features.py` - Advanced features
- `tests/test_bindings.py` - Basic bindings tests
- `tests/test_decorator.py` - Action decorator tests
- `tests/test_llm_agent.py` - LLM agent tests
- `tests/test_mesh.py` - Mesh operations tests
- `tests/test_ollama_simple.py` - Ollama connectivity tests
- `tests/test_response.py` - Response handling tests

## API Reference

### Core Classes

#### `Agent`

Base class for creating custom agents.

```python
class MyAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Handle incoming messages (synchronous)"""
        return "response"

    @Agent.action(name="my_action")
    def custom_action(self, param: str) -> str:
        """Custom action callable by other agents"""
        return f"Processed: {param}"
```

**Methods**:

- `name() -> str` - Get agent name
- `send_message(target: str, message: str)` - Send message to another agent
- `on_message(message: str, context=None)` - Override to handle messages

**Decorators**:

- `@Agent.action(name="action_name")` - Register a custom action

#### `LlmAgent`

LLM-powered agent with fluent builder API.

```python
agent = LlmAgent("name", "ollama::model_name")
agent.with_system_prompt("...")
agent.with_temperature(0.7)
agent.with_max_tokens(100)
agent.build()
```

**Builder Methods**:

- `with_system_prompt(prompt: str)` - Set system prompt
- `with_temperature(temp: float)` - Set temperature (0.0-1.0)
- `with_max_tokens(max: int)` - Set max tokens
- `build()` - Finalize configuration

**Message Methods**:

- `send_message(message: str) -> str` - Synchronous LLM call
- `send_message_async(message: str) -> Awaitable[str]` - Async LLM call ✅

#### `PyLocalMesh`

Local in-memory mesh for agent communication.

```python
mesh = PyLocalMesh("mesh_name")
mesh.add_agent(agent)
mesh.send_to("agent_name", "message")
```

**Methods**:

- `add_agent(agent: Agent)` - Register an agent
- `send_to(target: str, payload: str)` - Send message to agent

#### `PyAction`

Custom action definition with schema generation.

```python
from ceylon import PyAction

action = PyAction(
    name="my_action",
    description="Action description",
    schema='{"type": "object", ...}'
)
```

#### `PyToolInvoker`

Execute registered actions.

```python
invoker = agent.tool_invoker
result = invoker.invoke("action_name", '{"param": "value"}')
```

## Async Support

### ✅ Fully Supported Async Features

**1. `send_message_async()` on `LlmAgent`**

- Fully functional and production-ready
- Supports concurrent execution with asyncio
- Proper error propagation

```python
async def example():
    agent = LlmAgent("agent", "ollama::model")
    agent.build()

    # Concurrent queries
    tasks = [agent.send_message_async(q) for q in queries]
    results = await asyncio.gather(*tasks)
```

**2. Async `on_message()` handlers** ✨ **NEW**

- Now fully supported with thread-local event loops
- Can use async/await in custom agent message handlers
- Supports async actions as well

```python
class MyAgent(Agent):
    async def on_message(self, message, context=None):
        await asyncio.sleep(0.1)  # Async operations work!
        return f"Processed: {message}"
```

For detailed async examples, see [`ASYNC_EXAMPLES.md`](./ASYNC_EXAMPLES.md) and [`ASYNC_STATUS.md`](./ASYNC_STATUS.md).

## Documentation

- **[ASYNC_EXAMPLES.md](./ASYNC_EXAMPLES.md)** - Comprehensive async examples guide
- **[ASYNC_STATUS.md](./ASYNC_STATUS.md)** - Current status of async features
- **[examples/README_METRICS.md](./examples/README_METRICS.md)** - Metrics collection and monitoring guide
- **[Ceylon Docs](../../docs/)** - Full framework documentation

## Requirements

- Python 3.8+
- Rust toolchain (for building from source)
- Ollama (for LLM examples)

### Installing Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve

# Pull a model
ollama pull gemma3:latest
```

## Development

### Building from Source

```bash
cd bindings/python
cargo build --release
pip install -e .
```

### Running Tests

```bash
cd bindings/python
python -m pytest tests/
```

Or run individual tests:

```bash
python tests/test_actions.py
python tests/test_agent_messages.py
python tests/test_llm_agent.py
```

## Architecture

Ceylon uses a **mesh architecture** where agents communicate through a unified mesh abstraction:

```
┌─────────────────────────────────────┐
│          Application Code           │
│         (Python/Rust)               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Agent Mesh (Rust)           │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │Agent1│  │Agent2│  │Agent3│      │
│  └──┬───┘  └──┬───┘  └──┬───┘      │
│     └─────────┴─────────┘          │
│      Message Routing & Delivery    │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Local (In-Memory) or Distributed  │
│      (Network) Communication        │
└─────────────────────────────────────┘
```

**Key Concepts**:

- **Agents**: Autonomous entities that process messages and execute actions
- **Mesh**: Communication layer that routes messages between agents
- **Actions**: Callable functions/tools that agents can invoke
- **Messages**: Data exchanged between agents

## Contributing

Contributions are welcome! Please:

1. Check existing issues or create a new one
2. Fork the repository
3. Create a feature branch
4. Make your changes with tests
5. Submit a pull request

## License

See the main Ceylon repository for license information.

## Support

- **Issues**: [GitHub Issues](https://github.com/ceylonai/ceylon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ceylonai/ceylon/discussions)
- **Docs**: [Ceylon Documentation](../../docs/)

## Roadmap

- [ ] Full async/await support for message handlers
- [ ] Additional LLM provider integrations
- [ ] Distributed mesh implementation
- [ ] Agent lifecycle hooks
- [ ] Advanced debugging tools
- [ ] Performance monitoring

---

**Status**: Alpha - API may change

For more information about Ceylon, visit the [main repository](https://github.com/ceylonai/ceylon).

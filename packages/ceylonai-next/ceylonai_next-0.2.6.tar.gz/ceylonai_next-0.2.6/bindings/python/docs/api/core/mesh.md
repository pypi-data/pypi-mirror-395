# LocalMesh and PyLocalMesh

`LocalMesh` and `PyLocalMesh` provide infrastructure for creating mesh networks where multiple agents can communicate with each other and exchange messages in a coordinated manner.

## Class Signatures

```python
class LocalMesh(PyLocalMesh):
    """Python wrapper for LocalMesh"""
    pass

class PyLocalMesh:
    """Rust-backed mesh implementation"""
    def __init__(self, name: str) -> None:
        ...
```

## Description

A mesh is a distributed communication network that allows agents to register, start/stop, and exchange messages. `LocalMesh` is the Python interface to the Rust-based `PyLocalMesh` implementation, suitable for single-machine deployments with multiple agents.

The mesh handles:
- Agent registration and lifecycle management
- Message routing between agents
- Synchronous message delivery
- Multi-agent orchestration

## Constructor

### `__init__(name: str)`

Creates a new local mesh instance.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name identifier for the mesh |

**Returns:** LocalMesh/PyLocalMesh instance

**Example:**
```python
from ceylonai_next import LocalMesh, PyLocalMesh

# Using Python wrapper
mesh1 = LocalMesh("main-mesh")

# Using Rust implementation directly
mesh2 = PyLocalMesh("task-mesh")
```

## Methods

### `add_agent(agent: PyAgent) -> None`

Register an agent with the mesh.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | `PyAgent` | Agent instance to register |

**Returns:** `None`

**Raises:**
- `ValueError` - If agent name is not set or already registered

**Example:**
```python
from ceylonai_next import LocalMesh, Agent

mesh = LocalMesh("demo")
agent1 = Agent("agent-1")
agent2 = Agent("agent-2")

mesh.add_agent(agent1)
mesh.add_agent(agent2)
```

---

### `register_agent(agent: PyAgent) -> None`

Alternative method name for adding agents to the mesh.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | `PyAgent` | Agent instance to register |

**Returns:** `None`

**Example:**
```python
from ceylonai_next import LocalMesh, LlmAgent

mesh = LocalMesh("production")
agent = LlmAgent("assistant", "ollama::llama2")
agent.build()

mesh.register_agent(agent)
```

---

### `start() -> None`

Start the mesh and initialize all registered agents.

**Parameters:** None

**Returns:** `None`

**Notes:**
- Must be called after all agents are registered
- Initializes agent lifecycle handlers (`on_start`)

**Example:**
```python
from ceylonai_next import LocalMesh, Agent

mesh = LocalMesh("demo")

class MyAgent(Agent):
    def on_start(self, context):
        print(f"{self.name()} starting...")

agent = MyAgent("worker")
mesh.add_agent(agent)
mesh.start()  # Triggers on_start() for all agents
```

---

### `send_to(agent_name: str, message: str) -> None`

Send a message to a specific agent in the mesh.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_name` | `str` | Name of the target agent |
| `message` | `str` | Message content |

**Returns:** `None`

**Raises:**
- `ValueError` - If agent name not found

**Example:**
```python
from ceylonai_next import LocalMesh, Agent
import time

class EchoAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.last_message = None

    def on_message(self, message, context=None):
        self.last_message = message
        print(f"[{self.name()}] Received: {message}")
        return f"Echo: {message}"

# Create mesh with agents
mesh = LocalMesh("chat")
echo = EchoAgent("echo-bot")
mesh.add_agent(echo)
mesh.start()

# Send messages
mesh.send_to("echo-bot", "Hello")
mesh.send_to("echo-bot", "How are you?")

time.sleep(0.1)  # Allow processing
print(f"Last message: {echo.last_message}")
```

---

### `stop() -> None`

Stop the mesh and all registered agents.

**Parameters:** None

**Returns:** `None`

**Notes:**
- Triggers `on_stop()` handler for all agents
- Cleans up resources

**Example:**
```python
from ceylonai_next import LocalMesh, Agent

class CleanableAgent(Agent):
    def on_stop(self, context):
        print(f"{self.name()} shutting down...")
        # Cleanup operations

mesh = LocalMesh("temporary")
agent = CleanableAgent("temp-worker")
mesh.add_agent(agent)
mesh.start()

# ... do work ...

mesh.stop()  # Triggers on_stop()
```

---

## Agent Lifecycle Hooks

Agents registered with a mesh can implement lifecycle methods:

### `on_start(context: PyAgentContext) -> None`

Called when the mesh starts.

```python
class LifecycleAgent(Agent):
    def on_start(self, context):
        print(f"{self.name()} is starting up...")
        # Initialize resources, connect to services, etc.
```

### `on_message(message: str, context: PyAgentContext) -> str | None`

Called when the agent receives a message via `mesh.send_to()`.

```python
class MessageAgent(Agent):
    def on_message(self, message, context=None):
        print(f"Processing message: {message}")
        return f"Processed: {message}"
```

### `on_stop(context: PyAgentContext) -> None`

Called when the mesh stops.

```python
class ShutdownAgent(Agent):
    def on_stop(self, context):
        print(f"{self.name()} is shutting down...")
        # Cleanup, save state, close connections, etc.
```

## Complete Examples

### Example 1: Simple Two-Agent Mesh

```python
from ceylonai_next import LocalMesh, Agent

class WorkerAgent(Agent):
    """Worker that processes tasks"""
    def on_message(self, message, context=None):
        print(f"[Worker] Processing: {message}")
        return f"Completed: {message}"

class ManagerAgent(Agent):
    """Manager that dispatches tasks"""
    def __init__(self):
        super().__init__("manager")
        self.tasks = ["Task A", "Task B", "Task C"]

    def on_start(self, context):
        print("[Manager] Starting task dispatch...")

# Create mesh
mesh = LocalMesh("work-mesh")

# Register agents
manager = ManagerAgent()
worker = WorkerAgent("worker")

mesh.add_agent(manager)
mesh.add_agent(worker)

# Start mesh
mesh.start()

# Dispatch tasks
print("\n--- Dispatching Tasks ---")
for task in manager.tasks:
    print(f"[Manager] Sending: {task}")
    mesh.send_to("worker", task)

print("\nMesh demo complete!")
```

### Example 2: Multi-Agent Communication

```python
from ceylonai_next import LocalMesh, Agent
import time

class RelayAgent(Agent):
    """Relays messages between agents"""
    def __init__(self, name, next_agent=None):
        super().__init__(name)
        self.next_agent = next_agent
        self.mesh = None

    def on_message(self, message, context=None):
        print(f"[{self.name()}] Received: {message}")
        if self.next_agent and self.mesh:
            processed = f"{message} -> processed by {self.name()}"
            print(f"[{self.name()}] Forwarding to {self.next_agent}")
            self.mesh.send_to(self.next_agent, processed)
        return f"Handled by {self.name()}"

# Create chain: agent1 -> agent2 -> agent3
mesh = LocalMesh("relay-mesh")

agent1 = RelayAgent("agent-1", "agent-2")
agent1.mesh = mesh

agent2 = RelayAgent("agent-2", "agent-3")
agent2.mesh = mesh

agent3 = RelayAgent("agent-3")
agent3.mesh = mesh

# Register all
for agent in [agent1, agent2, agent3]:
    mesh.add_agent(agent)

mesh.start()

# Start the chain
print("Starting message chain...")
mesh.send_to("agent-1", "Initial message")

time.sleep(0.2)
print("\nRelay demo complete!")
```

### Example 3: Mesh with Different Agent Types

```python
from ceylonai_next import LocalMesh, Agent, LlmAgent
import time

class CoordinatorAgent(Agent):
    """Coordinates work between agents"""
    def on_message(self, message, context=None):
        return f"Coordinating: {message}"

# Create mesh
mesh = LocalMesh("multi-type-mesh")

# Add different agent types
coordinator = CoordinatorAgent("coordinator")
mesh.add_agent(coordinator)

# Add LLM-based agent
llm_agent = LlmAgent("assistant", "ollama::llama2")
llm_agent.with_system_prompt("You are a helpful assistant")
llm_agent.build()
mesh.register_agent(llm_agent)

# Start mesh
mesh.start()

# Send messages to different agents
print("[Testing different agent types]")
mesh.send_to("coordinator", "Coordinate task 1")
time.sleep(0.1)

# Note: LLM agent messaging depends on implementation
print("Multi-type mesh demo complete!")
```

### Example 4: Stateful Mesh with Agent State

```python
from ceylonai_next import LocalMesh, Agent
import time

class StatefulAgent(Agent):
    """Agent that maintains state"""
    def __init__(self, name):
        super().__init__(name)
        self.state = {
            "messages_received": 0,
            "last_message": None,
            "active": False
        }

    def on_start(self, context):
        self.state["active"] = True
        print(f"[{self.name()}] Activated")

    def on_message(self, message, context=None):
        self.state["messages_received"] += 1
        self.state["last_message"] = message
        return f"[{self.state['messages_received']}] {message}"

    def on_stop(self, context):
        self.state["active"] = False
        print(f"[{self.name()}] Deactivated")
        print(f"  Total messages: {self.state['messages_received']}")
        print(f"  Last message: {self.state['last_message']}")

# Create mesh
mesh = LocalMesh("stateful-mesh")

agents = [
    StatefulAgent("processor-1"),
    StatefulAgent("processor-2"),
    StatefulAgent("processor-3"),
]

for agent in agents:
    mesh.add_agent(agent)

mesh.start()

# Send messages to each agent
print("\nProcessing messages...")
for i in range(5):
    for agent in agents:
        mesh.send_to(agent.name(), f"Message {i}")

time.sleep(0.1)

print("\nShutting down...")
mesh.stop()
```

## Important Concepts

### Message Delivery

Messages sent via `send_to()` are delivered synchronously and trigger the `on_message()` handler of the target agent.

### Agent Naming

Agent names must be unique within a mesh. Use descriptive names:
```python
# Good
agent = Agent("database-writer")
agent = Agent("api-gateway")

# Avoid
agent = Agent("a")
agent = Agent("123")
```

### Resource Management

Always call `mesh.stop()` when done:
```python
mesh = LocalMesh("temp")
# ... use mesh ...
mesh.stop()  # Cleanup resources
```

## Related APIs

- **[Agent](./agent.md)** - Base agent class
- **[LlmAgent](./llm-agent.md)** - LLM-powered agent
- **[PyAgent](../../guide/python-agent.md)** - Rust agent interface

## See Also

- [Mesh Architecture](../../concept/mesh.md)
- [Multi-Agent Communication Guide](../../guide/mesh.md)
- [Agent Lifecycle Hooks](../../guide/agent-lifecycle.md)
- [Mesh Examples](../../examples/mesh-examples.md)

# Mesh Networking - Overview

The Mesh is Ceylon's unified architecture for agent communication. A mesh allows agents to discover each other, send messages, and coordinate actions - whether they're on the same machine or distributed across multiple computers.

## What is a Mesh?

A **Mesh** is a network of interconnected agents that:

- **Register** agents for discovery
- **Route messages** between agents
- **Manage communication** (local or distributed)
- **Scale transparently** from single machine to clusters
- **Provide unified API** regardless of deployment

```python
from ceylonai_next import LocalMesh, Agent

# Create a mesh
mesh = LocalMesh()

# Register agents
agent1 = Agent("agent1")
agent2 = Agent("agent2")

mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Agents can now communicate through the mesh
mesh.send_message("agent1", "agent2", "Hello!")
```

## Mesh Types

### Local Mesh

Agents on the same computer using in-memory communication:

```python
from ceylonai_next import LocalMesh

mesh = LocalMesh()

agent1 = Agent("processor")
agent2 = Agent("validator")

mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Fast, low-latency communication
mesh.send_message("processor", "validator", "Process this")
```

**Characteristics:**
- **Speed:** Ultra-low latency, microsecond range
- **Reliability:** Process memory based, no network overhead
- **Scalability:** Limited by machine resources
- **Use Case:** Single-machine deployments, testing, prototyping

### Distributed Mesh

Agents across multiple computers (coming soon):

```python
# Future: Distributed mesh
# mesh = DistributedMesh(config="mesh_config.yaml")
# Agents can be on any computer, same API as LocalMesh
```

**Characteristics:**
- **Scalability:** Unlimited, add computers as needed
- **Resilience:** Survive individual machine failures
- **Flexibility:** Deploy agents where resources are available
- **Complexity:** Network coordination, potential latency
- **Use Case:** Production systems, large-scale deployments

## Core Concepts

### Agent Registration

Register agents with a mesh:

```python
from ceylonai_next import LocalMesh, Agent

mesh = LocalMesh()

# Create agents
agent1 = Agent("worker1")
agent2 = Agent("worker2")
agent3 = Agent("coordinator")

# Register all agents
mesh.register_agent(agent1)
mesh.register_agent(agent2)
mesh.register_agent(agent3)

# All agents are now discoverable by name
```

**Important:** Agents must be registered before they can receive mesh messages.

### Message Routing

Send messages between registered agents:

```python
# Send message from agent1 to agent2
mesh.send_message("agent1", "agent2", "Hello from agent1")

# The mesh:
# 1. Validates both agents are registered
# 2. Routes message from sender to receiver
# 3. Delivers to receiver's on_message() handler
# 4. Returns response
```

### Discovery

Find agents in the mesh:

```python
# List all registered agents
agents = mesh.list_agents()
print(agents)  # ["agent1", "agent2", "agent3"]

# Check if agent exists
if "worker1" in mesh.list_agents():
    mesh.send_message("coordinator", "worker1", "Get status")
```

## Building Applications with Mesh

### Simple Multi-Agent System

```python
from ceylonai_next import LocalMesh, Agent

class RequestHandler(Agent):
    def on_message(self, message: str, context=None) -> str:
        return f"Handled: {message}"

class Router(Agent):
    def __init__(self, mesh):
        super().__init__("router")
        self.mesh = mesh

    def on_message(self, message: str, context=None) -> str:
        # Route to handler
        response = self.mesh.send_message(
            "router",
            "handler",
            message
        )
        return f"Routed response: {response}"

# Create mesh
mesh = LocalMesh()

# Create agents
handler = RequestHandler("handler")
router = Router(mesh)

# Register
mesh.register_agent(handler)
mesh.register_agent(router)

# Use
response = mesh.send_message(
    "user",
    "router",
    "Process this request"
)
print(response)
```

### Hierarchical Structure

```python
from ceylonai_next import LocalMesh, Agent

class Coordinator(Agent):
    def __init__(self, mesh, workers):
        super().__init__("coordinator")
        self.mesh = mesh
        self.workers = workers

    def on_message(self, message: str, context=None) -> str:
        """Coordinate work across workers."""
        results = []

        for worker in self.workers:
            response = self.mesh.send_message(
                "coordinator",
                worker,
                message
            )
            results.append(response)

        return f"Results: {results}"

class Worker(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Process work."""
        return f"Worker processed: {message}"

# Create mesh
mesh = LocalMesh()

# Create workers
worker1 = Worker("worker1")
worker2 = Worker("worker2")
worker3 = Worker("worker3")

# Create coordinator
coordinator = Coordinator(mesh, ["worker1", "worker2", "worker3"])

# Register all
for worker in [worker1, worker2, worker3, coordinator]:
    mesh.register_agent(worker)

# Use
response = mesh.send_message(
    "client",
    "coordinator",
    "Process data"
)
print(response)
```

### Pipeline Architecture

```python
from ceylonai_next import LocalMesh, Agent

class StageAgent(Agent):
    def __init__(self, name: str, next_stage: str = None):
        super().__init__(name)
        self.next_stage = next_stage
        self.mesh = None

    def set_mesh(self, mesh):
        self.mesh = mesh

    def on_message(self, message: str, context=None) -> str:
        # Process
        processed = self.process(message)

        # Forward to next stage
        if self.next_stage and self.mesh:
            return self.mesh.send_message(
                self.name(),
                self.next_stage,
                processed
            )

        return processed

    def process(self, message: str) -> str:
        return f"{self.name()} processed: {message}"

# Create pipeline
stage1 = StageAgent("validate", "normalize")
stage2 = StageAgent("normalize", "analyze")
stage3 = StageAgent("analyze")

mesh = LocalMesh()

# Set mesh for all stages
for stage in [stage1, stage2, stage3]:
    stage.set_mesh(mesh)
    mesh.register_agent(stage)

# Process through pipeline
result = mesh.send_message("client", "validate", "raw data")
print(result)
```

## LLM Agents in Mesh

Use LLM agents in a mesh:

```python
from ceylonai_next import LocalMesh, LlmAgent, Agent

class DataAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        # Process and return data
        return f"Data: {message}"

# Create mesh
mesh = LocalMesh()

# LLM agent
ai_assistant = LlmAgent("assistant", "ollama::llama3.2:latest")
ai_assistant.with_system_prompt(
    "You are helpful. You can request data from the data_agent."
)
ai_assistant.build()

# Data provider
data_agent = DataAgent("data_agent")

# Register
mesh.register_agent(ai_assistant)
mesh.register_agent(data_agent)

# AI can request data
response = mesh.send_message(
    "client",
    "assistant",
    "What data do we have?"
)
print(response)
```

## Memory Sharing in Mesh

Share knowledge across agents:

```python
from ceylonai_next import LocalMesh, LlmAgent, InMemoryBackend, MemoryEntry

# Create shared memory
shared_memory = InMemoryBackend()

# Store shared knowledge
knowledge = [
    "Agent1 is for processing",
    "Agent2 is for validation",
    "Agent3 is for analysis"
]

for fact in knowledge:
    entry = MemoryEntry(fact)
    entry.with_metadata("shared", "true")
    shared_memory.store(entry)

# Create agents with shared memory
mesh = LocalMesh()

agent1 = LlmAgent("processor", "ollama::llama3.2:latest")
agent1.with_memory(shared_memory)
agent1.build()

agent2 = LlmAgent("validator", "ollama::llama3.2:latest")
agent2.with_memory(shared_memory)
agent2.build()

# Register
mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Both agents have access to shared knowledge
```

## Error Handling in Mesh

### Agent Not Found

```python
from ceylonai_next import LocalMesh, Agent

mesh = LocalMesh()
agent = Agent("worker")
mesh.register_agent(agent)

try:
    # This will fail - agent not registered
    response = mesh.send_message(
        "client",
        "nonexistent",
        "Hello"
    )
except ValueError as e:
    print(f"Agent not found: {e}")
```

### Message Failure

```python
class FailingAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        if "error" in message:
            raise RuntimeError("Processing error")
        return "OK"

mesh = LocalMesh()
failing_agent = FailingAgent("failing")
mesh.register_agent(failing_agent)

try:
    response = mesh.send_message(
        "client",
        "failing",
        "error trigger"
    )
except Exception as e:
    print(f"Message processing failed: {e}")
```

### Timeout Handling

```python
import asyncio
from ceylonai_next import LocalMesh, Agent

class SlowAgent(Agent):
    async def on_message_async(self, message: str, context=None) -> str:
        await asyncio.sleep(5)  # Slow operation
        return "Done"

mesh = LocalMesh()
slow_agent = SlowAgent("slow")
mesh.register_agent(slow_agent)

async def query_with_timeout():
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                lambda: mesh.send_message("client", "slow", "Process")
            ),
            timeout=2.0
        )
        return response
    except asyncio.TimeoutError:
        return "Request timed out"

# Result: "Request timed out"
```

## Mesh Patterns

### Request-Reply

```python
from ceylonai_next import LocalMesh, Agent

class Service(Agent):
    def on_message(self, message: str, context=None) -> str:
        # Process and return response
        return f"Service response: {message}"

mesh = LocalMesh()
service = Service("service")
mesh.register_agent(service)

# Request-reply pattern
response = mesh.send_message(
    "client",
    "service",
    "Request"
)
print(response)
```

### Fan-Out

```python
from ceylonai_next import LocalMesh, Agent

class Orchestrator(Agent):
    def __init__(self, mesh, workers):
        super().__init__("orchestrator")
        self.mesh = mesh
        self.workers = workers

    def on_message(self, message: str, context=None) -> str:
        """Send request to multiple workers."""
        responses = []

        for worker in self.workers:
            response = self.mesh.send_message(
                "orchestrator",
                worker,
                message
            )
            responses.append(response)

        return f"Collected {len(responses)} responses"

class Worker(Agent):
    def on_message(self, message: str, context=None) -> str:
        return f"{self.name()} processed: {message}"

# Setup
mesh = LocalMesh()

workers = [
    Worker(f"worker{i}")
    for i in range(1, 4)
]

orchestrator = Orchestrator(mesh, [w.name() for w in workers])

# Register all
for worker in workers + [orchestrator]:
    mesh.register_agent(worker)

# Fan-out
response = mesh.send_message(
    "client",
    "orchestrator",
    "Process everywhere"
)
```

### Fan-In

```python
# Collect results from multiple sources
```

### Pub-Sub (Future)

```python
# Future: Publish-subscribe pattern
# mesh.publish("topic", message)
# mesh.subscribe("topic", agent)
```

## Monitoring and Debugging

### List Registered Agents

```python
mesh = LocalMesh()

# Register some agents
for i in range(5):
    agent = Agent(f"agent{i}")
    mesh.register_agent(agent)

# List all agents
agents = mesh.list_agents()
print(f"Registered agents: {agents}")
```

### Trace Messages

```python
from ceylonai_next import LocalMesh, Agent

class TracingAgent(Agent):
    def __init__(self, name: str, mesh=None):
        super().__init__(name)
        self.mesh = mesh

    def on_message(self, message: str, context=None) -> str:
        sender = context.sender if context and hasattr(context, 'sender') else "unknown"
        print(f"[{self.name()}] Message from {sender}: {message}")
        return f"{self.name()} processed: {message}"

mesh = LocalMesh()

agent1 = TracingAgent("agent1", mesh)
agent2 = TracingAgent("agent2", mesh)

mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Send message - will be traced
response = mesh.send_message("agent1", "agent2", "test")
```

### Logging

```python
import logging
from ceylonai_next import LocalMesh, Agent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LoggingAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        logger.info(f"Received: {message}")
        try:
            result = self.process(message)
            logger.info(f"Sent: {result}")
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
            raise

    def process(self, message: str) -> str:
        return f"Processed: {message}"

mesh = LocalMesh()
agent = LoggingAgent("agent")
mesh.register_agent(agent)
```

## Best Practices

### 1. Always Register Before Use

```python
# Good
agent = Agent("worker")
mesh.register_agent(agent)
mesh.send_message("client", "worker", "task")

# Avoid
agent = Agent("worker")
mesh.send_message("client", "worker", "task")  # Will fail
```

### 2. Use Descriptive Agent Names

```python
# Good
mesh.register_agent(Agent("email_validator"))
mesh.register_agent(Agent("payment_processor"))

# Avoid
mesh.register_agent(Agent("a1"))
mesh.register_agent(Agent("worker"))
```

### 3. Handle Agent Not Found

```python
agents = mesh.list_agents()
if "target" in agents:
    response = mesh.send_message("client", "target", "msg")
else:
    print("Agent not found")
```

### 4. Avoid Deadlocks

```python
# Avoid circular dependencies
# agent1 -> agent2 -> agent1
```

### 5. Document Message Formats

```python
class APIAgent(Agent):
    """
    API Agent handles requests.

    Expected message format:
    {
        "method": "GET|POST|PUT|DELETE",
        "path": "/api/resource",
        "body": optional_json
    }

    Response format:
    {
        "status": 200-599,
        "data": response_data,
        "error": optional_error_message
    }
    """
    pass
```

## Scaling Considerations

### Single Machine (Local Mesh)

- Fast communication (in-memory)
- Suitable for: Development, testing, small applications
- Limitation: Single machine resources

### Multiple Machines (Distributed Mesh - Future)

- Network communication
- Suitable for: Large-scale systems, high availability
- Considerations: Network latency, reliability

## Next Steps

- [Agents](../agents/overview.md) - Agent fundamentals
- [Async](../async/overview.md) - Asynchronous operations in mesh
- [Memory](../memory/overview.md) - Shared knowledge between agents
- [Actions](../actions/overview.md) - Agent capabilities
- [Examples](../../examples/index.md) - Browse complete examples

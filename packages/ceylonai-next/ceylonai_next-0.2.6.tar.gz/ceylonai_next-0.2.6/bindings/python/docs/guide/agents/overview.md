# Agents - Overview

Agents are the core building blocks of Ceylon AI. They are autonomous entities that can receive messages, perform actions, and communicate with other agents. This guide covers the fundamental concepts and architecture of Ceylon agents.

## What is an Agent?

An **Agent** is a self-contained entity that:

- **Receives messages** from users or other agents
- **Processes information** according to its logic or LLM configuration
- **Performs actions** using tools and integrations
- **Sends responses** back to the sender
- **Maintains state** (optional memory, context, configuration)
- **Communicates** with other agents through a mesh

```python
from ceylonai_next import Agent

# Create a basic agent
agent = Agent("my_agent")
```

## Core Agent Concepts

### Agent Identity

Every agent has a unique name:

```python
agent = Agent("customer_support_agent")
print(agent.name())  # "customer_support_agent"
```

**Best practices:**
- Use descriptive names: `payment_processor`, `content_analyzer`, not `agent1`
- Use lowercase with underscores: `web_crawler`, `data_validator`
- Names should reflect the agent's role/responsibility

### Agent Types

Ceylon supports different types of agents for different use cases:

| Type | Purpose | Use Case |
|------|---------|----------|
| **Agent** | Custom logic | Business rules, complex workflows |
| **LlmAgent** | LLM-powered | Conversational AI, reasoning, content generation |
| **Node** | Mesh participant | Advanced distributed systems (coming soon) |

```python
# Basic agent with custom logic
agent = Agent("rule_engine")

# LLM-powered agent
llm_agent = LlmAgent("assistant", "ollama::llama3.2:latest")
```

## Agent Lifecycle

```
Creation → Configuration → Building → Running → Cleanup
```

### 1. Creation

Create an agent instance:

```python
from ceylonai_next import Agent

agent = Agent("my_agent")
```

### 2. Configuration

Configure the agent's behavior:

```python
# Add system prompt (for LLM agents)
llm_agent.with_system_prompt("You are helpful")

# Add memory
llm_agent.with_memory(memory_backend)

# Add actions
agent.register_action(my_action)
```

### 3. Building

Finalize the agent configuration:

```python
agent.build()
```

**Note:** Call `build()` after all configuration. It prepares the agent for use.

### 4. Running

Use the agent to process messages:

```python
response = agent.send_message("Hello!")
```

### 5. Cleanup

The agent automatically cleans up resources when garbage collected. For explicit cleanup:

```python
# Optional - Python handles this automatically
del agent
```

## Agent Architecture

```
┌─────────────────────────────────┐
│     Agent Instance              │
├─────────────────────────────────┤
│  Properties                     │
│  - name                         │
│  - state (optional)             │
│  - memory (optional)            │
│  - actions (optional)           │
├─────────────────────────────────┤
│  Methods                        │
│  - send_message()               │
│  - send_message_async()         │
│  - on_message()                 │
│  - register_action()            │
├─────────────────────────────────┤
│  Event Handlers                 │
│  - on_message                   │
│  - on_error                     │
│  - on_shutdown                  │
└─────────────────────────────────┘
```

## Sending Messages

### Synchronous Messages

Send a message and wait for response:

```python
response = agent.send_message("What is Python?")
print(response)
```

**Use when:**
- Single message processing
- Response is needed immediately
- Synchronous context

### Asynchronous Messages

Send a message without blocking:

```python
response = await agent.send_message_async("What is Python?")
print(response)
```

**Use when:**
- Multiple concurrent messages
- Long-running operations
- Async context (web servers, etc.)

## Message Handling

### Default Behavior

If you don't override `on_message()`, the agent returns the message as-is:

```python
agent = Agent("echo")
agent.build()
response = agent.send_message("Hello")  # Returns "Hello"
```

### Custom Logic

Override `on_message()` to add custom behavior:

```python
class GreeterAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Handle incoming messages."""
        return f"Hello! You said: {message}"

agent = GreeterAgent("greeter")
agent.build()
response = agent.send_message("Hi")  # "Hello! You said: Hi"
```

## Agent State

Agents can maintain internal state:

```python
class CounterAgent(Agent):
    def __init__(self):
        super().__init__("counter")
        self.count = 0

    def on_message(self, message: str, context=None) -> str:
        """Increment counter with each message."""
        self.count += 1
        return f"Message #{self.count}: {message}"

agent = CounterAgent()
agent.build()
agent.send_message("First")      # Message #1: First
agent.send_message("Second")     # Message #2: Second
```

## Actions and Tools

Agents can register and execute actions (tools):

```python
from ceylonai_next import Agent, PyAction

class CalculatorAgent(Agent):
    @Agent.action(name="add", description="Add two numbers")
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    @Agent.action(name="multiply", description="Multiply two numbers")
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

agent = CalculatorAgent("calculator")
agent.build()

# Agent can now use these actions (especially in mesh or with LLM agents)
```

See the [Actions & Tools](../actions/overview.md) guide for more details.

## Agent Integration Points

### With Memory

Store and retrieve information:

```python
from ceylonai_next import InMemoryBackend, LlmAgent

memory = InMemoryBackend()
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_memory(memory)
agent.build()
```

### With Mesh

Communicate with other agents:

```python
from ceylonai_next import LocalMesh

mesh = LocalMesh()
mesh.register_agent(agent1)
mesh.register_agent(agent2)

# Agents can now send messages to each other
```

### With LLM

Add AI reasoning:

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("ai_agent", "openai::gpt-4")
agent.build()
```

## Quick Start Examples

### Simple Echo Agent

```python
from ceylonai_next import Agent

class EchoAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        return message.upper()

agent = EchoAgent("echo")
agent.build()

response = agent.send_message("hello")
print(response)  # "HELLO"
```

### Stateful Agent

```python
from ceylonai_next import Agent

class CounterAgent(Agent):
    def __init__(self):
        super().__init__("counter")
        self.messages = []

    def on_message(self, message: str, context=None) -> str:
        self.messages.append(message)
        return f"Received {len(self.messages)} messages so far"

agent = CounterAgent()
agent.build()

print(agent.send_message("Hello"))    # Received 1 messages so far
print(agent.send_message("World"))    # Received 2 messages so far
```

### Agent with Actions

```python
from ceylonai_next import Agent

class UtilityAgent(Agent):
    @Agent.action(name="reverse", description="Reverse a string")
    def reverse(self, text: str) -> str:
        return text[::-1]

    @Agent.action(name="uppercase", description="Convert to uppercase")
    def uppercase(self, text: str) -> str:
        return text.upper()

agent = UtilityAgent("utility")
agent.build()
```

## Common Patterns

### Factory Pattern

Create agents programmatically:

```python
def create_agent(role: str, name: str) -> Agent:
    """Factory function for agent creation."""
    class RoleBasedAgent(Agent):
        def on_message(self, message: str, context=None) -> str:
            return f"[{role}] {message}"

    agent = RoleBasedAgent(name)
    agent.build()
    return agent

# Create different agents
admin_agent = create_agent("Admin", "admin_bot")
user_agent = create_agent("User", "user_bot")
```

### Agent Registry

Store and manage multiple agents:

```python
class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, agent: Agent) -> None:
        """Register an agent."""
        self.agents[agent.name()] = agent

    def get(self, name: str) -> Agent:
        """Get agent by name."""
        return self.agents.get(name)

    def list_agents(self) -> list:
        """Get all agent names."""
        return list(self.agents.keys())

registry = AgentRegistry()
registry.register(agent1)
registry.register(agent2)
```

### Context-Aware Agent

Access context information in message handlers:

```python
class ContextAwareAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        if context:
            sender = context.sender if hasattr(context, 'sender') else "unknown"
            timestamp = context.timestamp if hasattr(context, 'timestamp') else "unknown"
            return f"[{sender} @ {timestamp}] {message}"
        return message

agent = ContextAwareAgent("aware_bot")
agent.build()
```

## Error Handling

### Basic Error Handling

```python
from ceylonai_next import Agent

class SafeAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        try:
            if not message:
                raise ValueError("Empty message")
            return f"Processing: {message}"
        except ValueError as e:
            return f"Error: {e}"

agent = SafeAgent("safe")
agent.build()

print(agent.send_message(""))        # Error: Empty message
print(agent.send_message("Hello"))   # Processing: Hello
```

### Async Error Handling

```python
import asyncio
from ceylonai_next import Agent

class RobustAgent(Agent):
    async def on_message_async(self, message: str, context=None) -> str:
        try:
            # Simulate async operation
            await asyncio.sleep(0.1)
            return f"Processed: {message}"
        except asyncio.TimeoutError:
            return "Operation timed out"
        except Exception as e:
            return f"Error: {str(e)}"
```

## Best Practices

### 1. Use Descriptive Names

```python
# Good
agent = Agent("email_validator")
agent = Agent("translation_service")

# Avoid
agent = Agent("agent")
agent = Agent("a1")
```

### 2. Implement Idempotency

Messages should produce the same result when processed multiple times:

```python
class IdempotentAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        # Good: Same input always produces same output
        return message.strip().lower()
```

### 3. Keep Logic Simple

```python
# Good: Clear, single responsibility
class ValidationAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        return "valid" if len(message) > 0 else "invalid"

# Avoid: Complex, multiple responsibilities
class ComplexAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        # Too much logic here
        pass
```

### 4. Handle Timeouts

```python
import asyncio
from ceylonai_next import Agent

class TimeoutAwareAgent(Agent):
    async def on_message_async(self, message: str, context=None) -> str:
        try:
            result = await asyncio.wait_for(
                self.process(message),
                timeout=5.0
            )
            return result
        except asyncio.TimeoutError:
            return "Operation timed out"

    async def process(self, message: str) -> str:
        await asyncio.sleep(0.1)
        return f"Processed: {message}"
```

### 5. Log Important Events

```python
import logging
from ceylonai_next import Agent

logger = logging.getLogger(__name__)

class LoggingAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        logger.info(f"Received message: {message}")
        try:
            result = self.process(message)
            logger.info(f"Sent response: {result}")
            return result
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise

    def process(self, message: str) -> str:
        return f"Processed: {message}"
```

## Next Steps

- [Creating Basic Agents](basic-agents.md) - Learn how to create custom agents
- [LLM Agents](llm-agents.md) - Build AI-powered agents
- [Actions & Tools](../actions/overview.md) - Add capabilities to agents
- [Mesh](../mesh/overview.md) - Connect agents together
- [Async](../async/overview.md) - Concurrent agent operations

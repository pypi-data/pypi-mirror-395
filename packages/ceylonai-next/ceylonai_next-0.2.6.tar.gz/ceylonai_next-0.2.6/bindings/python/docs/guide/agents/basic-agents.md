# Creating Basic Agents

This guide shows you how to create custom agents with Ceylon AI. Learn to build agents that handle messages, maintain state, and integrate with your applications.

## Creating Your First Agent

The simplest agent is created by subclassing `Agent`:

```python
from ceylonai_next import Agent

class MyAgent(Agent):
    pass

agent = MyAgent("my_agent")
agent.build()

# Send a message
response = agent.send_message("Hello")
```

By default, the agent returns the message as-is. To add custom behavior, override `on_message()`.

## Message Handling

### Simple Message Handler

Override `on_message()` to process messages:

```python
from ceylonai_next import Agent

class GreeterAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Greet the user."""
        return f"Hello! You said: {message}"

agent = GreeterAgent("greeter")
agent.build()

response = agent.send_message("World")
print(response)  # "Hello! You said: World"
```

### Message Transformation

Transform incoming messages:

```python
class TransformerAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Transform message to uppercase."""
        return message.upper()

agent = TransformerAgent("transformer")
agent.build()

print(agent.send_message("hello"))    # "HELLO"
print(agent.send_message("python"))   # "PYTHON"
```

### Conditional Response

Return different responses based on input:

```python
class ConditionalAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Return different responses based on input."""
        message = message.strip().lower()

        if message == "hello":
            return "Hi there!"
        elif message == "bye":
            return "Goodbye!"
        else:
            return f"You said: {message}"

agent = ConditionalAgent("conditional")
agent.build()

print(agent.send_message("hello"))   # "Hi there!"
print(agent.send_message("bye"))     # "Goodbye!"
print(agent.send_message("other"))   # "You said: other"
```

## Agent State

Agents can maintain internal state between messages:

### Simple Counter

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

print(agent.send_message("First"))   # "Message #1: First"
print(agent.send_message("Second"))  # "Message #2: Second"
print(agent.send_message("Third"))   # "Message #3: Third"
```

### State Dictionary

Store complex state:

```python
class StatefulAgent(Agent):
    def __init__(self):
        super().__init__("stateful")
        self.state = {
            "messages": [],
            "users": set(),
            "data": {}
        }

    def on_message(self, message: str, context=None) -> str:
        """Store message and track users."""
        # Store message
        self.state["messages"].append(message)

        # Extract user (simplified)
        user = context.sender if context and hasattr(context, 'sender') else "unknown"
        self.state["users"].add(user)

        return f"Total messages: {len(self.state['messages'])}, Users: {len(self.state['users'])}"

agent = StatefulAgent()
agent.build()
```

### Session Management

Track user sessions:

```python
class SessionAgent(Agent):
    def __init__(self):
        super().__init__("session")
        self.sessions = {}  # session_id -> session_data

    def on_message(self, message: str, context=None) -> str:
        """Handle message with session tracking."""
        # Get session ID from context
        session_id = context.session_id if context and hasattr(context, 'session_id') else "default"

        # Initialize session if needed
        if session_id not in self.sessions:
            self.sessions[session_id] = {"messages": [], "created": True}

        # Add message to session
        session = self.sessions[session_id]
        session["messages"].append(message)

        return f"Session {session_id}: {len(session['messages'])} messages"

agent = SessionAgent()
agent.build()
```

## Agent Configuration

### Configuration in Constructor

```python
class ConfigurableAgent(Agent):
    def __init__(self, name: str, greeting: str = "Hello"):
        super().__init__(name)
        self.greeting = greeting

    def on_message(self, message: str, context=None) -> str:
        return f"{self.greeting}! You said: {message}"

# Create with custom greeting
agent = ConfigurableAgent("greeter", greeting="Welcome")
agent.build()

print(agent.send_message("Hi"))  # "Welcome! You said: Hi"
```

### Configuration from Dictionary

```python
class DictConfigAgent(Agent):
    def __init__(self, config: dict):
        super().__init__(config.get("name", "agent"))
        self.config = config

    def on_message(self, message: str, context=None) -> str:
        if self.config.get("echo"):
            return message
        return f"Config-based response: {message}"

config = {
    "name": "dict_agent",
    "echo": True,
    "debug": False
}

agent = DictConfigAgent(config)
agent.build()
```

## Actions and Tools

Agents can register actions (tools) that can be called:

### Simple Actions

```python
from ceylonai_next import Agent

class CalculatorAgent(Agent):
    @Agent.action(name="add", description="Add two numbers")
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    @Agent.action(name="multiply", description="Multiply two numbers")
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    def on_message(self, message: str, context=None) -> str:
        """Handle text messages."""
        return f"I can calculate things. You said: {message}"

agent = CalculatorAgent("calculator")
agent.build()
```

### Actions with State

```python
class StorageAgent(Agent):
    def __init__(self):
        super().__init__("storage")
        self.storage = {}

    @Agent.action(name="store", description="Store a value")
    def store(self, key: str, value: str) -> str:
        """Store a key-value pair."""
        self.storage[key] = value
        return f"Stored: {key} = {value}"

    @Agent.action(name="retrieve", description="Retrieve a value")
    def retrieve(self, key: str) -> str:
        """Retrieve a value by key."""
        value = self.storage.get(key)
        if value is None:
            return f"Key '{key}' not found"
        return f"Retrieved: {key} = {value}"

    def on_message(self, message: str, context=None) -> str:
        return f"You said: {message}"

agent = StorageAgent()
agent.build()
```

### Dynamic Actions

```python
from ceylonai_next import Agent, PyAction

class DynamicAgent(Agent):
    def register_custom_action(self, name: str, description: str, func):
        """Dynamically register an action."""
        action = PyAction(
            name,
            description,
            '{"type": "object", "properties": {}}',
            None
        )
        action.func = func
        self.register_action(action)

# Usage
agent = DynamicAgent("dynamic")

def my_tool(context, inputs):
    return "Custom tool result"

agent.register_custom_action("custom", "My custom tool", my_tool)
agent.build()
```

## Error Handling

### Try-Except Pattern

```python
class SafeAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Handle messages safely."""
        try:
            if not message or not isinstance(message, str):
                raise ValueError("Invalid input")

            return self.process(message)

        except ValueError as e:
            return f"Validation error: {e}"
        except Exception as e:
            return f"Error: {e}"

    def process(self, message: str) -> str:
        """Process the message."""
        return f"Processed: {message}"

agent = SafeAgent("safe")
agent.build()

print(agent.send_message(""))      # Validation error: Invalid input
print(agent.send_message("Hello")) # Processed: Hello
```

### Retry Logic

```python
from ceylonai_next import Agent
import time

class RetryAgent(Agent):
    def __init__(self, max_retries: int = 3):
        super().__init__("retry")
        self.max_retries = max_retries

    def on_message(self, message: str, context=None) -> str:
        """Process with automatic retry."""
        for attempt in range(self.max_retries):
            try:
                return self.process(message)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Failed after {self.max_retries} attempts: {e}"
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff

    def process(self, message: str) -> str:
        """Process message (may fail)."""
        # Simulate operation that might fail
        if len(message) == 0:
            raise ValueError("Empty message")
        return f"Processed: {message}"

agent = RetryAgent()
agent.build()
```

### Validation

```python
class ValidatingAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Validate input before processing."""
        # Validate
        error = self.validate(message)
        if error:
            return f"Validation failed: {error}"

        # Process
        return self.process(message)

    def validate(self, message: str) -> str:
        """Return error message if invalid, None if valid."""
        if not message:
            return "Message cannot be empty"
        if len(message) > 1000:
            return "Message too long (max 1000 chars)"
        if not isinstance(message, str):
            return "Message must be a string"
        return None

    def process(self, message: str) -> str:
        """Process valid message."""
        return f"Valid message: {message}"

agent = ValidatingAgent("validating")
agent.build()
```

## Context Usage

Access context information in message handlers:

### Extracting Context

```python
from ceylonai_next import Agent

class ContextAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Use context information."""
        if context is None:
            return message

        # Extract context fields
        sender = getattr(context, 'sender', 'unknown')
        timestamp = getattr(context, 'timestamp', 'unknown')

        return f"From {sender} @ {timestamp}: {message}"

agent = ContextAgent("context")
agent.build()
```

### Context-Aware Behavior

```python
class SmartAgent(Agent):
    def on_message(self, message: str, context=None) -> str:
        """Change behavior based on context."""
        if context is None:
            return f"(No context) {message}"

        # Behavior changes based on sender
        sender = getattr(context, 'sender', None)
        if sender == "admin":
            return f"[ADMIN] Processing: {message}"
        elif sender == "user":
            return f"[USER] Received: {message}"
        else:
            return f"[UNKNOWN] {message}"

agent = SmartAgent("smart")
agent.build()
```

## Inheritance and Composition

### Agent Inheritance

```python
class BaseAgent(Agent):
    """Base agent with common functionality."""
    def validate_message(self, message: str) -> bool:
        return message is not None and len(message) > 0

class SpecializedAgent(BaseAgent):
    """Specialized agent inheriting from base."""
    def on_message(self, message: str, context=None) -> str:
        if not self.validate_message(message):
            return "Invalid message"
        return self.special_process(message)

    def special_process(self, message: str) -> str:
        return f"Special: {message}"

agent = SpecializedAgent("specialized")
agent.build()
```

### Composition Pattern

```python
class Processor:
    """Helper class for message processing."""
    def process(self, text: str) -> str:
        return text.strip().upper()

class CompositeAgent(Agent):
    def __init__(self):
        super().__init__("composite")
        self.processor = Processor()  # Composition

    def on_message(self, message: str, context=None) -> str:
        return self.processor.process(message)

agent = CompositeAgent()
agent.build()
```

## Common Patterns

### Pipeline Pattern

```python
class PipelineAgent(Agent):
    """Process messages through a pipeline of steps."""

    def on_message(self, message: str, context=None) -> str:
        """Process through pipeline."""
        result = message
        result = self.step1(result)
        result = self.step2(result)
        result = self.step3(result)
        return result

    def step1(self, text: str) -> str:
        return text.strip()

    def step2(self, text: str) -> str:
        return text.lower()

    def step3(self, text: str) -> str:
        return text.replace(" ", "_")

agent = PipelineAgent("pipeline")
agent.build()

print(agent.send_message("  HELLO WORLD  "))  # "hello_world"
```

### Builder Pattern for Configuration

```python
class ConfigBuilder:
    def __init__(self):
        self.config = {}

    def set_greeting(self, greeting: str):
        self.config["greeting"] = greeting
        return self

    def set_debug(self, debug: bool):
        self.config["debug"] = debug
        return self

    def build(self, name: str) -> Agent:
        agent = Agent(name)
        agent.config = self.config
        return agent

# Usage
builder = ConfigBuilder()
agent = (builder
    .set_greeting("Welcome")
    .set_debug(True)
    .build("my_agent"))
agent.build()
```

### Strategy Pattern

```python
class ProcessingStrategy:
    def process(self, text: str) -> str:
        raise NotImplementedError

class UppercaseStrategy(ProcessingStrategy):
    def process(self, text: str) -> str:
        return text.upper()

class ReverseStrategy(ProcessingStrategy):
    def process(self, text: str) -> str:
        return text[::-1]

class StrategyAgent(Agent):
    def __init__(self, strategy: ProcessingStrategy):
        super().__init__("strategy")
        self.strategy = strategy

    def on_message(self, message: str, context=None) -> str:
        return self.strategy.process(message)

# Usage
agent = StrategyAgent(UppercaseStrategy())
agent.build()
print(agent.send_message("hello"))  # "HELLO"

# Switch strategy
agent.strategy = ReverseStrategy()
print(agent.send_message("hello"))  # "olleh"
```

## Advanced Techniques

### Decorators for Common Patterns

```python
from functools import wraps
from ceylonai_next import Agent

def with_logging(func):
    @wraps(func)
    def wrapper(self, message, context=None):
        print(f"Received: {message}")
        result = func(self, message, context)
        print(f"Sent: {result}")
        return result
    return wrapper

class LoggedAgent(Agent):
    @with_logging
    def on_message(self, message: str, context=None) -> str:
        return f"Processed: {message}"

agent = LoggedAgent("logged")
agent.build()
agent.send_message("test")
```

### Metaclass for Auto-Registration

```python
from ceylonai_next import Agent

class AutoRegisterMeta(type):
    """Metaclass that auto-registers all action methods."""
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Could auto-register actions here
        return cls

class AutoRegisterAgent(Agent, metaclass=AutoRegisterMeta):
    pass
```

## Testing Agents

### Unit Testing

```python
import unittest
from ceylonai_next import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MyAgent("test_agent")
        self.agent.build()

    def test_message_processing(self):
        response = self.agent.send_message("hello")
        self.assertIsNotNone(response)

    def test_state_management(self):
        agent = CounterAgent()
        agent.build()
        agent.send_message("first")
        agent.send_message("second")
        self.assertEqual(agent.count, 2)

    def tearDown(self):
        del self.agent

if __name__ == '__main__':
    unittest.main()
```

## Best Practices

### 1. Always Call build()

```python
agent = MyAgent("my_agent")
agent.build()  # Don't forget this!
```

### 2. Handle None Messages

```python
def on_message(self, message: str, context=None) -> str:
    if message is None:
        return "Error: empty message"
    return message
```

### 3. Use Type Hints

```python
# Good
def on_message(self, message: str, context=None) -> str:
    return f"Processed: {message}"

# Avoid
def on_message(self, message, context=None):
    return f"Processed: {message}"
```

### 4. Keep on_message() Simple

```python
# Good: Delegate to helper methods
def on_message(self, message: str, context=None) -> str:
    return self.process(message)

def process(self, message: str) -> str:
    # Complex logic here
    pass
```

### 5. Document Behavior

```python
class DocumentedAgent(Agent):
    """Agent that demonstrates best practices."""

    def on_message(self, message: str, context=None) -> str:
        """
        Handle incoming messages.

        Args:
            message: The incoming message string
            context: Optional context about the sender

        Returns:
            Response string

        Raises:
            ValueError: If message is invalid
        """
        # Implementation
        pass
```

## Next Steps

- [LLM Agents](llm-agents.md) - Add AI capabilities
- [Actions & Tools](../actions/overview.md) - Define what agents can do
- [Memory](../memory/overview.md) - Give agents memory
- [Mesh](../mesh/overview.md) - Connect agents together
- [Async](../async/overview.md) - Concurrent operations

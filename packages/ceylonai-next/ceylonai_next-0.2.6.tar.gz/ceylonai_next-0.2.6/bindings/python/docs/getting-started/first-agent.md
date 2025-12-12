# Your First Agent

This tutorial will guide you through creating your first Ceylon AI agent step-by-step. You'll learn the fundamentals of agent creation, message handling, and adding custom functionality.

## What You'll Build

By the end of this tutorial, you'll have:

- A custom agent with message handling
- Custom actions (tools)
- Integration with an LLM
- A simple interactive chat interface

## Step 1: Basic Agent

Let's start with the simplest possible agent:

```python
from ceylonai_next import Agent

# Create an agent
agent = Agent("my_first_agent")

# Send a message
response = agent.send_message("Hello, Ceylon!")
print(response)
```

**Output:**
```
Message received
```

This creates a basic agent with default behavior. Not very interesting yet!

## Step 2: Custom Message Handler

Let's make the agent respond intelligently:

```python
from ceylonai_next import Agent

class EchoAgent(Agent):
    """An agent that echoes messages back."""

    def __init__(self, name="echo"):
        super().__init__(name)

    def on_message(self, message, context=None):
        """Handle incoming messages."""
        return f"Echo: {message}"

# Create and test the agent
agent = EchoAgent()
response = agent.send_message("Hello, Ceylon!")
print(response)
```

**Output:**
```
Echo: Hello, Ceylon!
```

### Understanding the Code

- **`class EchoAgent(Agent)`**: We subclass `Agent` to create a custom agent
- **`on_message()`**: This method is called when the agent receives a message
- **`return ...`**: The return value is sent back as the response

## Step 3: Adding State

Agents can maintain state across messages:

```python
from ceylonai_next import Agent

class CounterAgent(Agent):
    """An agent that counts messages."""

    def __init__(self, name="counter"):
        super().__init__(name)
        self.message_count = 0

    def on_message(self, message, context=None):
        self.message_count += 1
        return f"Message #{self.message_count}: {message}"

# Create and test
agent = CounterAgent()
print(agent.send_message("First"))   # Message #1: First
print(agent.send_message("Second"))  # Message #2: Second
print(agent.send_message("Third"))   # Message #3: Third
```

## Step 4: Adding Custom Actions

Actions (also called tools) let agents perform specific tasks:

```python
from ceylonai_next import Agent

class MathAgent(Agent):
    """An agent with mathematical capabilities."""

    def __init__(self):
        super().__init__("math_agent")

    @Agent.action(
        name="add",
        description="Add two numbers together"
    )
    def add(self, a: int, b: int) -> int:
        """Add two integers and return the result."""
        return a + b

    @Agent.action(
        name="multiply",
        description="Multiply two numbers"
    )
    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers and return the result."""
        return a * b

    @Agent.action(
        name="power",
        description="Raise a number to a power"
    )
    def power(self, base: int, exponent: int) -> int:
        """Calculate base^exponent."""
        return base ** exponent

# Create agent
agent = MathAgent()

# Actions are registered automatically and have schemas generated
# from type hints - they can be used by LLM agents or invoked directly
```

### Key Points About Actions

1. **Decorator**: Use `@Agent.action()` to mark a method as an action
2. **Type Hints**: Type hints generate JSON schemas automatically
3. **Descriptions**: Provide clear descriptions for LLMs to understand
4. **Automatic Registration**: Actions are registered when the agent is created

## Step 5: LLM-Powered Agent

Now let's create an agent powered by a Large Language Model:

```python
from ceylonai_next import LlmAgent

# Create an LLM agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a helpful assistant that specializes in Python programming. "
    "Provide clear, concise answers with code examples when appropriate."
)
agent.with_temperature(0.7)
agent.build()

# Chat with the agent
questions = [
    "What is a Python list comprehension?",
    "How do I read a file in Python?",
    "Explain decorators in simple terms"
]

for question in questions:
    print(f"\nQ: {question}")
    response = agent.send_message(question)
    print(f"A: {response}")
    print("-" * 60)
```

### Configuration Options

```python
agent = LlmAgent("assistant", "ollama::llama3.2:latest")

# System prompt - defines the agent's behavior
agent.with_system_prompt("You are a helpful assistant.")

# Temperature (0.0-2.0) - controls randomness
# Lower = more focused, Higher = more creative
agent.with_temperature(0.7)

# Max tokens - limits response length
agent.with_max_tokens(500)

# API key (for cloud providers)
agent.with_api_key("your-api-key")

# Must call build() before using
agent.build()
```

## Step 6: LLM Agent with Actions

Combine LLM intelligence with custom actions:

```python
from ceylonai_next import LlmAgent, PyAction
import datetime

class CalendarAgent:
    """An LLM agent that can tell the current date and time."""

    def __init__(self):
        # Create LLM agent
        self.agent = LlmAgent("calendar_assistant", "ollama::llama3.2:latest")
        self.agent.with_system_prompt(
            "You are a helpful assistant that can tell users the current "
            "date and time. Use the available actions when users ask for "
            "this information."
        )

        # Register custom actions
        self.register_actions()

        # Build the agent
        self.agent.build()

    def register_actions(self):
        """Register custom actions with the agent."""

        # Create get_date action
        def get_current_date(context, inputs):
            """Get the current date."""
            return datetime.datetime.now().strftime("%Y-%m-%d")

        date_action = PyAction(
            "get_current_date",
            "Get the current date in YYYY-MM-DD format",
            '{"type": "object", "properties": {}}',  # No inputs needed
            None
        )

        # Create get_time action
        def get_current_time(context, inputs):
            """Get the current time."""
            return datetime.datetime.now().strftime("%H:%M:%S")

        time_action = PyAction(
            "get_current_time",
            "Get the current time in HH:MM:SS format",
            '{"type": "object", "properties": {}}',
            None
        )

        # Register actions
        self.agent.register_action(date_action)
        self.agent.register_action(time_action)

    def chat(self, message):
        """Send a message to the agent."""
        return self.agent.send_message(message)

# Usage
agent = CalendarAgent()
print(agent.chat("What's the date today?"))
print(agent.chat("What time is it?"))
```

## Step 7: Complete Interactive Agent

Let's build a complete interactive agent with all features:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry
import sys

class InteractiveAssistant:
    """A complete interactive AI assistant with memory."""

    def __init__(self, model="ollama::llama3.2:latest"):
        # Setup memory
        self.memory = InMemoryBackend.with_max_entries(100)

        # Create agent
        self.agent = LlmAgent("assistant", model)
        self.agent.with_system_prompt(
            "You are a helpful, friendly AI assistant. "
            "You have memory of previous conversations and can "
            "remember information about the user. "
            "Be concise but informative."
        )
        self.agent.with_memory(self.memory)
        self.agent.with_temperature(0.8)
        self.agent.build()

        # Conversation history
        self.history = []

    def remember(self, key, value):
        """Store a fact in memory."""
        entry = MemoryEntry(f"{key}: {value}")
        entry.with_metadata("type", "user_fact")
        entry.with_metadata("key", key)
        self.memory.store(entry)

    def chat(self, message):
        """Send a message and get a response."""
        response = self.agent.send_message(message)
        self.history.append({"user": message, "assistant": response})
        return response

    def run(self):
        """Run an interactive chat session."""
        print("Interactive Assistant Started!")
        print("Type 'quit' to exit, 'history' to see conversation history")
        print("-" * 60)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break

                if user_input.lower() == 'history':
                    print("\nConversation History:")
                    for i, turn in enumerate(self.history, 1):
                        print(f"\n{i}. You: {turn['user']}")
                        print(f"   Assistant: {turn['assistant']}")
                    continue

                # Get response
                response = self.chat(user_input)
                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

# Run the assistant
if __name__ == "__main__":
    assistant = InteractiveAssistant()
    assistant.run()
```

### Running the Interactive Agent

```bash
python interactive_assistant.py
```

**Example Session:**

```
Interactive Assistant Started!
Type 'quit' to exit, 'history' to see conversation history
------------------------------------------------------------

You: Hi, my name is Alice
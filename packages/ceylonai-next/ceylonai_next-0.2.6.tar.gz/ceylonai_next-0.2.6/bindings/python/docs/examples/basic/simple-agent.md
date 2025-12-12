# Simple Agent Example

## Overview

This example demonstrates the **basic fundamentals** of Ceylon agents and message passing. You'll learn how to create a simple agent that receives and processes messages synchronously.

This is the perfect starting point if you're new to Ceylon - it covers the core concepts you need to understand before moving to more advanced features.

## What You'll Learn

- **Agent Creation**: How to define a custom agent by extending the `Agent` base class
- **Message Handling**: Implementing the `on_message()` handler to process incoming messages
- **Local Mesh Communication**: How agents communicate through a local mesh
- **Message Lifecycle**: Understanding how messages are sent and processed
- **State Management**: Storing and tracking received messages in an agent

## Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher installed
- Ceylon SDK installed: `pip install ceylon`
- Basic understanding of Python classes and methods
- Familiarity with Python `super()` and inheritance

## Step-by-Step Guide

### Step 1: Understand Agent Basics

An **Agent** in Ceylon is an autonomous entity that can:
- Receive messages from other agents
- Process those messages through a handler method
- Maintain internal state
- Send messages to other agents

The most basic agent needs:
1. A name to identify it in the mesh
2. A message handler to process incoming messages
3. Optional state to track information

### Step 2: Create Your Custom Agent Class

```python
class SimpleAgent(Agent):
    """Agent with synchronous message handler"""

    def __init__(self, name):
        super().__init__(name)
        self.received = []
```

Breaking this down:

- **`class SimpleAgent(Agent)`**: Inherit from the `Agent` base class to create a custom agent
- **`super().__init__(name)`**: Call the parent class constructor to initialize the agent with a name
- **`self.received = []`**: Create a list to track all received messages (this is our state)

### Step 3: Implement the Message Handler

```python
def on_message(self, message, context=None):
    """Synchronous message handler"""
    print(f"[{self.name()}] Received: {message}")
    self.received.append(message)
    print(f"[{self.name()}] Processed: {message}")
    return f"Processed: {message}"
```

What's happening here:

- **`on_message(self, message, context=None)`**: This method is called whenever the agent receives a message
- **`self.name()`**: Get the agent's name (calling the method from the parent `Agent` class)
- **`self.received.append(message)`**: Store the message in our list
- **`return f"Processed: {message}"`**: Return a response (optional, but useful for verification)

### Step 4: Initialize the Mesh

```python
agent = SimpleAgent("simple_agent")
mesh = PyLocalMesh("demo_mesh")
mesh.add_agent(agent)
```

Here's what each line does:

- **`SimpleAgent("simple_agent")`**: Create an agent instance with the name `"simple_agent"`
- **`PyLocalMesh("demo_mesh")`**: Create a local mesh (a communication channel for agents)
- **`mesh.add_agent(agent)`**: Register the agent with the mesh so it can receive messages

### Step 5: Send Messages

```python
messages = ["Hello", "World", "Test"]
for msg in messages:
    print(f"\nSending: {msg}")
    mesh.send_to("simple_agent", msg)
    time.sleep(0.1)  # Give time for processing
```

This demonstrates:

- **Message List**: Define multiple messages to send
- **`mesh.send_to(agent_name, message)`**: Send a message to a specific agent by name
- **`time.sleep(0.1)`**: Small delay to let the agent process each message before sending the next

### Step 6: Verify Results

```python
time.sleep(0.5)  # Wait for all messages to process
print(f"\n✅ Agent received {len(agent.received)} messages: {agent.received}")

if len(agent.received) == len(messages):
    print("✅ All messages processed successfully!")
```

This shows:

- **Wait for Processing**: Give the system time to complete all asynchronous operations
- **Verification**: Check that all messages were received and stored
- **Feedback**: Provide clear output about what happened

## Complete Code with Inline Comments

```python
#!/usr/bin/env python3
"""
Simple synchronous agent demo - verifies basic functionality

This is the simplest possible Ceylon example. It demonstrates:
1. Creating a custom agent
2. Implementing message handling
3. Creating a local mesh
4. Sending messages
5. Verifying message delivery
"""
import time
from ceylonai_next import Agent, PyLocalMesh


class SimpleAgent(Agent):
    """
    A simple agent that receives and tracks messages.

    This agent:
    - Extends the Agent base class
    - Implements on_message() to handle incoming messages
    - Stores received messages in a list for tracking
    """

    def __init__(self, name):
        # Call parent constructor with agent name
        super().__init__(name)
        # Initialize a list to store all received messages
        self.received = []

    def on_message(self, message, context=None):
        """
        Handle incoming messages synchronously.

        Args:
            message: The message content (can be any Python object)
            context: Optional context information (usually None for simple agents)

        Returns:
            A confirmation string

        This method is called by Ceylon whenever this agent receives a message.
        """
        # Print when message arrives
        print(f"[{self.name()}] Received: {message}")

        # Store the message in our internal list
        self.received.append(message)

        # Process the message (in this case, just log it)
        print(f"[{self.name()}] Processed: {message}")

        # Return a response (optional, useful for debugging)
        return f"Processed: {message}"


def main():
    """Main entry point for the demo"""
    print("\n🚀 Ceylon Simple Agent Demo\n")
    print("=" * 60)

    # Step 1: Create an agent instance
    # The name "simple_agent" is how we'll refer to this agent in the mesh
    agent = SimpleAgent("simple_agent")

    # Step 2: Create a local mesh
    # A mesh is a communication layer that agents use to talk to each other
    mesh = PyLocalMesh("demo_mesh")

    # Step 3: Register the agent with the mesh
    # This tells the mesh about our agent and lets it receive messages
    mesh.add_agent(agent)

    print(f"Created mesh with agent '{agent.name()}'")

    # Step 4: Prepare messages to send
    messages = ["Hello", "World", "Test"]

    # Step 5: Send each message to the agent
    for msg in messages:
        print(f"\nSending: {msg}")
        # Send the message to the agent by its name
        mesh.send_to("simple_agent", msg)
        # Small delay to ensure processing completes
        time.sleep(0.1)

    # Step 6: Wait for all processing to complete
    # Since message handling might be asynchronous internally,
    # we wait a bit longer for the final message
    time.sleep(0.5)

    # Step 7: Verify results
    print(f"\n✅ Agent received {len(agent.received)} messages: {agent.received}")

    # Step 8: Check if everything worked
    if len(agent.received) == len(messages):
        print("✅ All messages processed successfully!")
    else:
        print(f"⚠️  Expected {len(messages)} messages, got {len(agent.received)}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
```

## Running the Example

### 1. Set Up Your Environment

```bash
# Navigate to the examples directory
cd bindings/python/examples

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Ensure Ceylon is installed
pip install ceylon
```

### 2. Run the Script

```bash
python demo_simple_agent.py
```

### 3. Expected Output

```
🚀 Ceylon Simple Agent Demo

============================================================
Created mesh with agent 'simple_agent'

Sending: Hello
[simple_agent] Received: Hello
[simple_agent] Processed: Hello

Sending: World
[simple_agent] Received: World
[simple_agent] Processed: World

Sending: Test
[simple_agent] Received: Test
[simple_agent] Processed: Test

✅ Agent received 3 messages: ['Hello', 'World', 'Test']
✅ All messages processed successfully!

============================================================
```

## Key Concepts Explained

### Agent

An agent is an independent entity that can:
- Have a unique identity (name)
- Receive messages asynchronously
- Process those messages with custom logic
- Maintain internal state
- Be extended with custom behavior

```python
class MyAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        # Your custom initialization here

    def on_message(self, message, context=None):
        # Your custom message handling here
        return response
```

### on_message Handler

This is the core of agent behavior. When a message arrives:
1. Ceylon automatically calls your `on_message()` method
2. You have access to the message content and optional context
3. You can perform any processing you need
4. You can optionally return a response

The handler is **synchronous** - it processes messages one at a time.

### Local Mesh (PyLocalMesh)

The mesh is the communication infrastructure:
- Creates a local network for agents to communicate
- Routes messages from sender to receiver
- Handles agent registration
- Manages the message passing lifecycle

Think of it like a post office - agents are people, and the mesh delivers their mail.

### Message Flow

```
Agent 1                    Mesh                    Agent 2
   |                        |                         |
   |---> send_to ---------> |                         |
   |       "Hello"          |                         |
   |                        |                         |
   |                        | ---> on_message ------> |
   |                        |      "Hello"            |
   |                        |                         |
   |                        | <--- response ----------|
   | <--- response ---------|                         |
   |
```

### State Management

Agents can maintain state between messages:

```python
class CountingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.message_count = 0  # State

    def on_message(self, message, context=None):
        self.message_count += 1  # Modify state
        return f"Message #{self.message_count}: {message}"
```

This is useful for:
- Tracking conversation history
- Maintaining counters or statistics
- Storing configuration
- Keeping agent-specific context

## Troubleshooting

### Issue: Messages Not Being Received

**Problem**: Agent receives 0 messages

**Solutions**:
1. Verify the agent is properly registered: `mesh.add_agent(agent)`
2. Check the agent name matches: `mesh.send_to("simple_agent", msg)` should match the name passed to the agent constructor
3. Ensure sufficient wait time: `time.sleep()` might need to be longer
4. Check for exceptions in the `on_message()` method

### Issue: ImportError: No module named 'ceylon'

**Problem**: Ceylon is not installed

**Solution**:
```bash
pip install ceylon
```

### Issue: Agent Name Mismatch

**Problem**: Getting errors like "Agent not found"

**Solution**:
```python
# Make sure these match:
agent = SimpleAgent("simple_agent")      # Name used here
mesh.send_to("simple_agent", msg)        # Name used here
```

### Issue: Messages Seem to Process Out of Order

**Problem**: The order of received messages doesn't match send order

**Solution**:
This can happen with concurrent processing. Use `time.sleep()` to ensure sequential processing, or implement a queue-based approach for message ordering guarantees.

## Next Steps

Now that you understand the basics, explore these next examples:

1. **LLM Conversation** (`llm-conversation.md`): Learn how to create agents that interact with LLMs like Claude or Ollama
2. **Async Operations** (`../async/async-llm.md`): Handle multiple operations concurrently using Python's asyncio
3. **Memory System** (`../memory/basic-memory.md`): Store and retrieve information using Ceylon's memory system
4. **RAG System** (`../rag/markdown-rag.md`): Build Retrieval-Augmented Generation systems for knowledge bases

## Common Extensions

### Add Message Validation

```python
def on_message(self, message, context=None):
    if not message:
        print("Empty message received!")
        return "Error: Empty message"

    self.received.append(message)
    return f"Processed: {message}"
```

### Add Message Type Handling

```python
def on_message(self, message, context=None):
    if isinstance(message, str):
        self.received.append(message)
        return f"String processed: {message}"
    elif isinstance(message, dict):
        self.received.append(message.get('content', ''))
        return f"Dict processed: {message.get('content', '')}"
    else:
        return "Unsupported message type"
```

### Add Response Tracking

```python
def __init__(self, name):
    super().__init__(name)
    self.received = []
    self.responses = []  # Track what we return

def on_message(self, message, context=None):
    self.received.append(message)
    response = f"Processed: {message}"
    self.responses.append(response)
    return response
```

## Summary

The simple agent example demonstrates:
- ✅ Creating custom agents by extending the `Agent` class
- ✅ Implementing message handlers with `on_message()`
- ✅ Setting up a local mesh for agent communication
- ✅ Sending and receiving messages
- ✅ Verifying message delivery

This foundation prepares you for more complex scenarios involving multiple agents, LLM integration, and asynchronous processing.

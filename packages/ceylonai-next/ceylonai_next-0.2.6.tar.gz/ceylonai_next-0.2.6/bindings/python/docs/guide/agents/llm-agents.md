# LLM Agents

LLM Agents are agents powered by Large Language Models. They can understand natural language, reason about problems, and generate intelligent responses. This guide covers creating and using LLM agents in Ceylon.

## What is an LLM Agent?

An **LLM Agent** is a specialized agent that:

- Uses an LLM for reasoning and response generation
- Supports multiple LLM providers (Ollama, OpenAI, Anthropic)
- Can be configured with system prompts and parameters
- Integrates with memory, actions, and mesh

```python
from ceylonai_next import LlmAgent

# Create an LLM agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.build()

response = agent.send_message("What is Python?")
print(response)
```

## Creating LLM Agents

### Basic Creation

```python
from ceylonai_next import LlmAgent

# Create with model string
agent = LlmAgent("my_assistant", "ollama::llama3.2:latest")
agent.build()
```

### Supported LLM Providers

| Provider | Format | API Key Required | Best For |
|----------|--------|------------------|----------|
| **Ollama** | `ollama::model_name` | No | Local development, privacy |
| **OpenAI** | `openai::gpt-4` | Yes | Production, high quality |
| **Anthropic** | `anthropic::claude-3-sonnet` | Yes | Advanced reasoning, safety |

### Full Configuration

```python
from ceylonai_next import LlmAgent
import os

# Create agent
agent = LlmAgent("assistant", "openai::gpt-4")

# Configure behavior
agent.with_system_prompt(
    "You are a helpful coding assistant. "
    "Provide clear, production-ready code with explanations."
)

# Configure generation
agent.with_temperature(0.3)     # Focused responses
agent.with_max_tokens(1000)     # Allow detailed answers

# Set authentication
agent.with_api_key(os.getenv("OPENAI_API_KEY"))

# Build
agent.build()
```

## System Prompts

System prompts define the agent's personality and behavior:

### Basic System Prompt

```python
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful assistant.")
agent.build()

response = agent.send_message("Hello!")
# Response will follow the system prompt
```

### Role-Based Prompts

```python
# Python Expert
python_expert = LlmAgent("python_expert", "ollama::llama3.2:latest")
python_expert.with_system_prompt(
    "You are an expert Python developer. "
    "Provide production-ready code with comprehensive error handling. "
    "Explain your reasoning and suggest best practices."
)
python_expert.build()

# Creative Writer
writer = LlmAgent("writer", "ollama::llama3.2:latest")
writer.with_system_prompt(
    "You are a creative writer. "
    "Write engaging, imaginative stories and content. "
    "Use vivid language and interesting narrative techniques."
)
writer.build()

# Data Analyst
analyst = LlmAgent("analyst", "ollama::llama3.2:latest")
analyst.with_system_prompt(
    "You are a data analyst. "
    "Provide data-driven insights and statistical analysis. "
    "Always cite your reasoning and sources."
)
analyst.build()
```

### Instruction-Based Prompts

```python
agent = LlmAgent("agent", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a helpful assistant. Follow these rules:\n"
    "1. Always be polite and respectful\n"
    "2. Provide accurate, factual information\n"
    "3. If unsure, say 'I don't know'\n"
    "4. Keep responses concise and clear"
)
agent.build()
```

### Context-Rich Prompts

```python
system_prompt = """
You are a customer support agent for TechCorp.

COMPANY INFO:
- Product: Advanced analytics platform
- Founded: 2020
- Customers: 5000+ companies

YOUR ROLE:
- Help customers with product questions
- Troubleshoot technical issues
- Process refund requests
- Escalate complex issues

TONE:
- Professional but friendly
- Helpful and empathetic
- Clear and concise

KNOWLEDGE BASE:
The platform supports REST API, Python SDK, and JavaScript SDK.
Standard support response time is 24 hours.
Premium customers get 2-hour response time.
"""

agent = LlmAgent("support_bot", "openai::gpt-4")
agent.with_system_prompt(system_prompt)
agent.build()
```

## Configuration Parameters

### Temperature

Controls response randomness (0.0 - 2.0):

```python
# Deterministic, focused (use for data extraction, code)
agent.with_temperature(0.0)

# Balanced (default, general purpose)
agent.with_temperature(0.7)

# Creative, diverse (use for writing, brainstorming)
agent.with_temperature(1.5)
```

### Max Tokens

Limits response length:

```python
# Short responses (summaries, labels)
agent.with_max_tokens(100)

# Medium responses (explanations, code snippets)
agent.with_max_tokens(500)

# Long responses (comprehensive guides, detailed analysis)
agent.with_max_tokens(2000)
```

### API Key

For cloud providers:

```python
import os
from ceylonai_next import LlmAgent

# From environment variable (recommended)
agent = LlmAgent("assistant", "openai::gpt-4")
api_key = os.getenv("OPENAI_API_KEY")
agent.with_api_key(api_key)
agent.build()

# Or directly (not recommended for security)
# agent.with_api_key("sk-...")
# agent.build()
```

## Integration with Memory

Add memory to LLM agents:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Create memory
memory = InMemoryBackend()

# Store knowledge
knowledge = [
    "Ceylon is a Rust-based agent framework",
    "Ceylon supports local and distributed deployments",
    "Ceylon has built-in memory and RAG support"
]

for fact in knowledge:
    entry = MemoryEntry(fact)
    entry.with_metadata("type", "knowledge")
    memory.store(entry)

# Create agent with memory
agent = LlmAgent("knowledgeable", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are a helpful assistant with access to a knowledge base. "
    "Use the available information to answer accurately."
)
agent.with_memory(memory)
agent.build()

# Agent can now use stored knowledge
response = agent.send_message("Tell me about Ceylon")
print(response)
```

## Integration with Actions

### Method 1: Instance Decorator (Recommended)

The simplest way to add actions to an LLM agent is using the `@agent.action()` decorator:

```python
from ceylonai_next import LlmAgent

# Create agent
agent = LlmAgent("smart", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are helpful and have access to tools. "
    "Use them when appropriate."
)

# Register actions using decorator
@agent.action(description="Get the current weather for a location")
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get weather information for a city."""
    if "london" in location.lower():
        return f"Weather in {location}: Rainy, 15 degrees {unit}"
    elif "paris" in location.lower():
        return f"Weather in {location}: Sunny, 22 degrees {unit}"
    else:
        return f"Weather in {location}: Partly cloudy, 20 degrees {unit}"

@agent.action(description="Get current time")
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@agent.action(description="Get information about the agent environment")
def get_agent_info(context) -> str:
    """Get information using agent context."""
    return f"I am running on mesh: {context.mesh_name}"

# Build agent
agent.build()

# Agent can now use actions when responding
response = agent.send_message("What time is it?")
print(response)

response = agent.send_message("What's the weather in Paris?")
print(response)
```

**Key Features:**
- `name` parameter is optional (defaults to function name)
- `description` parameter is required for LLM to understand when to use the action
- Actions can optionally accept `context` as first parameter for agent information
- Type hints are automatically converted to JSON schemas
- Return values can be any JSON-serializable type

### Method 2: Class-Based Actions

For more complex scenarios, you can subclass LlmAgent:

```python
from ceylonai_next import LlmAgent

class SmartAgent(LlmAgent):
    @LlmAgent.action(name="calculate", description="Calculate expression")
    def calculate(self, expression: str) -> float:
        """Safely evaluate a math expression."""
        try:
            # Safe evaluation with limited operators
            allowed = {'abs': abs, 'round': round}
            return eval(expression, {"__builtins__": {}}, allowed)
        except:
            return None

    @LlmAgent.action(name="get_time", description="Get current time")
    def get_time(self) -> str:
        """Get current time."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create agent
agent = SmartAgent("smart", "ollama::llama3.2:latest")
agent.with_system_prompt(
    "You are helpful and have access to tools. "
    "Use them when appropriate."
)
agent.build()

# Agent can now use actions when responding
response = agent.send_message("What time is it?")
```

## Conversation Patterns

### Single Query

```python
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.build()

response = agent.send_message("Explain Python decorators")
print(response)
```

### Multi-Turn Conversation

Note: Ceylon agents process each message independently by default. For stateful conversations, use memory:

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry
from datetime import datetime

class ConversationalBot:
    def __init__(self, model="ollama::llama3.2:latest"):
        self.memory = InMemoryBackend()
        self.agent = LlmAgent("chatbot", model)

        self.agent.with_system_prompt(
            "You are a friendly chatbot. "
            "Remember previous messages to provide context. "
            "Reference the conversation history when relevant."
        )
        self.agent.with_memory(self.memory)
        self.agent.build()

    def chat(self, user_message: str) -> str:
        """Handle a chat message."""
        # Store user message
        user_entry = MemoryEntry(f"User: {user_message}")
        user_entry.with_metadata("type", "user_message")
        user_entry.with_metadata("timestamp", str(datetime.now()))
        self.memory.store(user_entry)

        # Get response
        response = self.agent.send_message(user_message)

        # Store agent response
        agent_entry = MemoryEntry(f"Assistant: {response}")
        agent_entry.with_metadata("type", "assistant_message")
        agent_entry.with_metadata("timestamp", str(datetime.now()))
        self.memory.store(agent_entry)

        return response

# Usage
bot = ConversationalBot()
print(bot.chat("What's your name?"))
print(bot.chat("Can you help me with Python?"))
```

## Batch Processing

### Sequential Processing

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.build()

questions = [
    "What is Python?",
    "What is Rust?",
    "What is AI?"
]

responses = []
for question in questions:
    response = agent.send_message(question)
    responses.append(response)
    print(f"Q: {question}\nA: {response}\n")
```

### Concurrent Processing

```python
import asyncio
from ceylonai_next import LlmAgent

async def process_batch(questions: list, agent: LlmAgent):
    """Process multiple questions concurrently."""
    tasks = [
        agent.send_message_async(q)
        for q in questions
    ]

    responses = await asyncio.gather(*tasks)
    return responses

# Usage
async def main():
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.with_system_prompt("You are helpful.")
    agent.build()

    questions = [
        "What is Python?",
        "What is Rust?",
        "What is AI?"
    ]

    responses = await process_batch(questions, agent)
    for q, r in zip(questions, responses):
        print(f"Q: {q}\nA: {r}\n")

asyncio.run(main())
```

## Provider-Specific Usage

### Ollama

```python
from ceylonai_next import LlmAgent

# Pull a model first
# ollama pull llama3.2:latest

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are helpful.")
agent.with_temperature(0.7)
agent.build()

response = agent.send_message("Hello!")
print(response)
```

**Advantages:**
- Free, local inference
- No API key needed
- Privacy (data stays local)
- No rate limits
- Works offline

### OpenAI

```python
import os
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "openai::gpt-4")
agent.with_system_prompt("You are a helpful coding assistant.")
agent.with_temperature(0.3)
agent.with_api_key(os.getenv("OPENAI_API_KEY"))
agent.build()

response = agent.send_message("Explain type hints in Python")
print(response)
```

**Best Models:**
- **gpt-4**: Best quality, most expensive
- **gpt-3.5-turbo**: Fast, cost-effective
- **gpt-4-turbo-preview**: Balance of quality and speed

### Anthropic

```python
import os
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "anthropic::claude-3-sonnet")
agent.with_system_prompt("You are a thoughtful assistant.")
agent.with_temperature(0.5)
agent.with_api_key(os.getenv("ANTHROPIC_API_KEY"))
agent.build()

response = agent.send_message("Analyze this argument...")
print(response)
```

**Best Models:**
- **claude-3-opus**: Highest capability, most expensive
- **claude-3-sonnet**: Balanced, cost-effective
- **claude-3-haiku**: Fastest, cheapest

## Specialized LLM Agents

### Code Generation Agent

```python
from ceylonai_next import LlmAgent

def create_code_agent() -> LlmAgent:
    agent = LlmAgent("code_gen", "openai::gpt-4")

    agent.with_system_prompt(
        "You are an expert Python developer. "
        "Generate clean, well-documented, production-ready code. "
        "Include type hints, docstrings, and error handling. "
        "Explain your implementation."
    )

    agent.with_temperature(0.2)  # Low temperature for consistency
    agent.with_max_tokens(1000)

    return agent

agent = create_code_agent()
agent.build()

code = agent.send_message("Write a function to validate email addresses")
print(code)
```

### Question Answering Agent

```python
from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

def create_qa_agent(knowledge_base: list) -> LlmAgent:
    """Create a QA agent with knowledge base."""
    # Build memory from knowledge base
    memory = InMemoryBackend()
    for idx, doc in enumerate(knowledge_base):
        entry = MemoryEntry(doc)
        entry.with_metadata("source", "knowledge_base")
        entry.with_metadata("index", str(idx))
        memory.store(entry)

    # Create agent
    agent = LlmAgent("qa_bot", "openai::gpt-4")

    agent.with_system_prompt(
        "You are a helpful Q&A assistant. "
        "Answer questions based on the provided knowledge base. "
        "If information isn't available, say so clearly."
    )

    agent.with_temperature(0.2)
    agent.with_memory(memory)

    return agent

knowledge = [
    "Python is a high-level programming language",
    "Python emphasizes code readability",
    "Python supports multiple programming paradigms"
]

agent = create_qa_agent(knowledge)
agent.build()

response = agent.send_message("What is Python?")
print(response)
```

### Summarization Agent

```python
from ceylonai_next import LlmAgent

def create_summarizer() -> LlmAgent:
    agent = LlmAgent("summarizer", "openai::gpt-4")

    agent.with_system_prompt(
        "You are a summarization expert. "
        "Create clear, concise summaries that capture key points. "
        "Use bullet points when appropriate. "
        "Maintain the original meaning and tone."
    )

    agent.with_temperature(0.3)
    agent.with_max_tokens(500)

    return agent

agent = create_summarizer()
agent.build()

text = """
Python is a versatile programming language known for its simplicity and readability.
It supports multiple paradigms including procedural, object-oriented, and functional.
Python has a large standard library and extensive third-party ecosystem.
It's used in web development, data science, AI, automation, and many other fields.
"""

summary = agent.send_message(f"Summarize:\n{text}")
print(summary)
```

## Error Handling

### Connection Errors

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.build()

try:
    response = agent.send_message("Hello")
    print(response)
except ConnectionError as e:
    print(f"Connection failed: {e}")
    print("Make sure Ollama is running: ollama serve")
```

### API Errors

```python
import os
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "openai::gpt-4")
agent.with_api_key(os.getenv("OPENAI_API_KEY"))
agent.build()

try:
    response = agent.send_message("Hello")
    print(response)
except RuntimeError as e:
    if "invalid" in str(e).lower():
        print("Invalid API key")
    elif "quota" in str(e).lower():
        print("API quota exceeded")
    else:
        print(f"API error: {e}")
```

### Timeout Handling

```python
import asyncio
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.build()

async def query_with_timeout(agent: LlmAgent, message: str, timeout: float = 10.0):
    """Query agent with timeout."""
    try:
        response = await asyncio.wait_for(
            agent.send_message_async(message),
            timeout=timeout
        )
        return response
    except asyncio.TimeoutError:
        return "Request timed out"

# Usage
async def main():
    response = await query_with_timeout(agent, "Hello", timeout=5.0)
    print(response)

asyncio.run(main())
```

## Performance Optimization

### Caching Responses

```python
from ceylonai_next import LlmAgent
from functools import lru_cache

class CachingAgent:
    def __init__(self, model="ollama::llama3.2:latest"):
        self.agent = LlmAgent("cached", model)
        self.agent.with_system_prompt("You are helpful.")
        self.agent.build()
        self._cache = {}

    def send_message(self, message: str) -> str:
        """Send message with caching."""
        if message in self._cache:
            return self._cache[message]

        response = self.agent.send_message(message)
        self._cache[message] = response

        return response

bot = CachingAgent()
print(bot.send_message("What is Python?"))  # Calls LLM
print(bot.send_message("What is Python?"))  # From cache
```

### Model Selection

```python
from ceylonai_next import LlmAgent

def create_agent_for_task(task_type: str) -> LlmAgent:
    """Create appropriate agent based on task."""
    if task_type == "complex_reasoning":
        model = "openai::gpt-4"
        temperature = 0.3
    elif task_type == "creative_writing":
        model = "openai::gpt-4"
        temperature = 1.2
    elif task_type == "simple_qa":
        model = "openai::gpt-3.5-turbo"
        temperature = 0.5
    else:
        model = "ollama::llama3.2:latest"
        temperature = 0.7

    agent = LlmAgent(f"{task_type}_agent", model)
    agent.with_temperature(temperature)

    return agent

# Use appropriate model for task
coder = create_agent_for_task("complex_reasoning")
writer = create_agent_for_task("creative_writing")
qa = create_agent_for_task("simple_qa")
```

## Best Practices

### 1. Use Appropriate System Prompts

```python
# Good: Clear, specific role
agent.with_system_prompt("You are a Python expert...")

# Avoid: Vague prompts
agent.with_system_prompt("Be helpful")
```

### 2. Choose Right Temperature

```python
# Factual tasks: Low temperature
agent.with_temperature(0.2)

# Creative tasks: Higher temperature
agent.with_temperature(1.0)
```

### 3. Handle API Keys Securely

```python
# Good: From environment
import os
api_key = os.getenv("OPENAI_API_KEY")
agent.with_api_key(api_key)

# Avoid: Hardcoded keys
# agent.with_api_key("sk-...")
```

### 4. Reuse Agents

```python
# Good: Create once, use multiple times
agent = LlmAgent("assistant", "openai::gpt-4")
agent.build()

for query in queries:
    response = agent.send_message(query)

# Avoid: Creating new agent for each query
```

### 5. Set Reasonable Token Limits

```python
# Good: Appropriate limit for use case
agent.with_max_tokens(500)  # For summaries

# Avoid: Unlimited responses
# No max_tokens = very long responses
```

## Next Steps

- [Agents Overview](overview.md) - Agent fundamentals
- [Memory](../memory/overview.md) - Add memory to agents
- [Actions](../actions/overview.md) - Define agent capabilities
- [Async](../async/overview.md) - Concurrent operations
- [Mesh](../mesh/overview.md) - Multi-agent communication

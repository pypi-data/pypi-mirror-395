# LLM Integration - Overview

Ceylon AI provides seamless integration with Large Language Models (LLMs) from multiple providers. This guide covers everything you need to know about using LLMs with Ceylon.

## Quick Start

```python
from ceylonai_next import LlmAgent

# Create an LLM-powered agent
agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.with_system_prompt("You are a helpful coding assistant.")
agent.with_temperature(0.7)
agent.build()

# Chat with the agent
response = agent.send_message("Explain Python decorators")
print(response)
```

## Supported Providers

Ceylon supports multiple LLM providers with a unified API:

| Provider | Models | Type | API Key Required |
|----------|--------|------|------------------|
| **Ollama** | llama3.2, gemma, mistral, etc. | Local | No |
| **OpenAI** | gpt-4, gpt-3.5-turbo, etc. | Cloud | Yes |
| **Anthropic** | claude-3-opus, claude-3-sonnet | Cloud | Yes |

## Model String Format

All models use the format: `provider::model_name`

### Examples

```python
# Ollama (local)
"ollama::llama3.2:latest"
"ollama::gemma:7b"
"ollama::mistral:latest"

# OpenAI
"openai::gpt-4"
"openai::gpt-3.5-turbo"
"openai::gpt-4-turbo-preview"

# Anthropic
"anthropic::claude-3-opus"
"anthropic::claude-3-sonnet"
"anthropic::claude-3-haiku"
```

## Configuration Options

### System Prompt

Defines the agent's behavior and personality:

```python
agent.with_system_prompt(
    "You are an expert Python developer. "
    "Provide clear, concise answers with code examples. "
    "Always follow best practices and explain your reasoning."
)
```

### Temperature

Controls randomness (0.0 - 2.0):

```python
# Deterministic, focused
agent.with_temperature(0.0)

# Balanced (recommended)
agent.with_temperature(0.7)

# Creative, diverse
agent.with_temperature(1.5)
```

**Guidelines:**
- **0.0-0.3**: Factual tasks, code generation, data extraction
- **0.4-0.8**: General conversation, creative writing, brainstorming
- **0.9-2.0**: Very creative tasks, story writing, idea generation

### Max Tokens

Limits response length:

```python
# Short responses
agent.with_max_tokens(100)

# Medium responses (default)
agent.with_max_tokens(500)

# Long responses
agent.with_max_tokens(2000)
```

### API Key

For cloud providers:

```python
# Direct
agent.with_api_key("sk-...")

# From environment
import os
agent.with_api_key(os.getenv("OPENAI_API_KEY"))
```

## Complete Example

```python
from ceylonai_next import LlmAgent
import os

# Create agent with full configuration
agent = LlmAgent("coding_assistant", "openai::gpt-4")

# Configure behavior
agent.with_system_prompt(
    "You are an expert Python developer specializing in AI and ML. "
    "Provide production-ready code with error handling and type hints. "
    "Explain complex concepts in simple terms."
)

# Configure generation
agent.with_temperature(0.3)  # Focused for coding tasks
agent.with_max_tokens(1000)  # Allow detailed responses

# Set authentication
agent.with_api_key(os.getenv("OPENAI_API_KEY"))

# Build the agent
agent.build()

# Use the agent
questions = [
    "How do I implement a singleton in Python?",
    "What's the best way to handle async database operations?",
    "Explain the difference between @staticmethod and @classmethod"
]

for question in questions:
    print(f"\nQ: {question}")
    response = agent.send_message(question)
    print(f"A: {response}")
    print("-" * 80)
```

## Provider-Specific Setup

### Ollama Setup

1. **Install Ollama**:
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # Or download from https://ollama.ai
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama3.2:latest
   ollama pull gemma:7b
   ollama pull mistral:latest
   ```

3. **Verify**:
   ```bash
   ollama list
   ```

4. **Use in Ceylon**:
   ```python
   agent = LlmAgent("assistant", "ollama::llama3.2:latest")
   agent.build()
   ```

**Advantages:**
- Free and local
- No API key required
- Privacy (data stays local)
- No rate limits
- Offline capable

### OpenAI Setup

1. **Get API Key**:
   - Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Create new secret key

2. **Set environment variable**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. **Use in Ceylon**:
   ```python
   agent = LlmAgent("assistant", "openai::gpt-4")
   agent.with_api_key(os.getenv("OPENAI_API_KEY"))
   agent.build()
   ```

**Best Models:**
- **gpt-4**: Best quality, more expensive
- **gpt-3.5-turbo**: Fast, cost-effective
- **gpt-4-turbo-preview**: Balance of quality and speed

### Anthropic Setup

1. **Get API Key**:
   - Visit [console.anthropic.com](https://console.anthropic.com)
   - Generate API key

2. **Set environment variable**:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Use in Ceylon**:
   ```python
   agent = LlmAgent("assistant", "anthropic::claude-3-sonnet")
   agent.with_api_key(os.getenv("ANTHROPIC_API_KEY"))
   agent.build()
   ```

**Models:**
- **claude-3-opus**: Highest capability
- **claude-3-sonnet**: Balanced
- **claude-3-haiku**: Fastest

## Builder Pattern

Ceylon uses a fluent builder pattern:

```python
agent = (LlmAgent("assistant", "ollama::llama3.2:latest")
    .with_system_prompt("You are helpful")
    .with_temperature(0.7)
    .with_max_tokens(1000)
    .with_memory(memory_backend)
    .build())
```

## Synchronous vs Async

### Synchronous

```python
response = agent.send_message("Hello")
```

**Use when:**
- Single query at a time
- Simple scripts
- Learning/prototyping

### Asynchronous

```python
response = await agent.send_message_async("Hello")
```

**Use when:**
- Multiple concurrent queries
- Web applications
- High-performance requirements

See [Async Operations](async.md) for details.

## Common Patterns

### Configuration from File

```python
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Create agent
agent = LlmAgent(
    config['name'],
    f"{config['provider']}::{config['model']}"
)
agent.with_system_prompt(config['system_prompt'])
agent.with_temperature(config['temperature'])
agent.build()
```

### Multiple Agents

```python
# Create specialized agents
code_agent = LlmAgent("coder", "openai::gpt-4")
code_agent.with_system_prompt("You are a coding expert.")
code_agent.with_temperature(0.2)
code_agent.build()

creative_agent = LlmAgent("writer", "openai::gpt-4")
creative_agent.with_system_prompt("You are a creative writer.")
creative_agent.with_temperature(1.2)
creative_agent.build()

# Use for different tasks
code = code_agent.send_message("Write a function to sort a list")
story = creative_agent.send_message("Write a short story about AI")
```

### Agent Factory

```python
def create_specialist_agent(role: str, expertise: str) -> LlmAgent:
    """Factory function to create specialized agents."""
    agent = LlmAgent(f"{role}_agent", "ollama::llama3.2:latest")
    agent.with_system_prompt(
        f"You are an expert {role} specializing in {expertise}. "
        f"Provide detailed, accurate information about {expertise}."
    )
    agent.with_temperature(0.5)
    agent.build()
    return agent

# Create specialists
python_expert = create_specialist_agent("developer", "Python")
rust_expert = create_specialist_agent("developer", "Rust")
ml_expert = create_specialist_agent("data scientist", "Machine Learning")
```

## Error Handling

```python
from ceylonai_next import LlmAgent

try:
    agent = LlmAgent("assistant", "ollama::llama3.2:latest")
    agent.build()

    response = agent.send_message("Hello")
    print(response)

except ValueError as e:
    print(f"Configuration error: {e}")
    # Check model string format, configuration

except RuntimeError as e:
    print(f"Runtime error: {e}")
    # Check if model is available, API key is valid

except ConnectionError as e:
    print(f"Connection error: {e}")
    # Check network, Ollama service, API endpoint

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tips

1. **Reuse agents**: Create once, use multiple times
   ```python
   agent = LlmAgent(...).build()
   # Reuse for multiple queries
   ```

2. **Use appropriate models**: Don't use GPT-4 for simple tasks
   ```python
   # Simple tasks -> gpt-3.5-turbo or local model
   # Complex tasks -> gpt-4
   ```

3. **Set reasonable token limits**:
   ```python
   agent.with_max_tokens(500)  # Prevents very long responses
   ```

4. **Use async for multiple queries**:
   ```python
   await asyncio.gather(*[agent.send_message_async(q) for q in queries])
   ```

5. **Cache responses** for repeated queries

## Next Steps

- [LLM Agents](../agents/llm-agents.md) - Build AI-powered agents with LLMs
- [Async Operations](../async/overview.md) - Concurrent LLM operations
- [Memory](../memory/overview.md) - Add memory to LLM agents
- [Actions](../actions/overview.md) - Give agents tools and capabilities
- [Examples](../../examples/basic/llm-conversation.md) - Complete examples

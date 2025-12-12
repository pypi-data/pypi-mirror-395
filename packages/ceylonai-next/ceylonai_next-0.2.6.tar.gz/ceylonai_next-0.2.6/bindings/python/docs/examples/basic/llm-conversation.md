# LLM Conversation Example

## Overview

This example demonstrates how to **create an intelligent agent that converses with a Large Language Model (LLM)**. You'll learn how to set up an LLM agent, configure it with system prompts, and have natural conversations with language models like Claude (via Anthropic) or Ollama.

This is the bridge between basic agents and intelligent, context-aware applications.

## What You'll Learn

- **LLM Agent Creation**: How to instantiate an `LlmAgent` with language model configuration
- **System Prompts**: Setting instructions that guide the LLM's behavior
- **Agent Configuration**: Adjusting temperature, max tokens, and other LLM parameters
- **Synchronous Conversation**: Sending messages and receiving LLM responses
- **Error Handling**: Managing API calls and responses gracefully

## Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher
- Ceylon SDK: `pip install ceylon`
- Access to an LLM (either Ollama local instance or API key)
- Basic understanding of Large Language Models (LLMs)
- Knowledge of Python strings and basic syntax

### LLM Provider Options

**Option 1: Ollama (Local)**
- Download Ollama from [ollama.com](https://ollama.com)
- Pull a model: `ollama pull gemma3:latest` or `ollama pull mistral`
- No API keys needed
- Runs on your machine

**Option 2: Anthropic Claude (Cloud)**
- Get an API key from [console.anthropic.com](https://console.anthropic.com)
- Set environment variable: `export ANTHROPIC_API_KEY="sk-..."`
- Access to state-of-the-art models

**Option 3: OpenAI GPT (Cloud)**
- Get an API key from [platform.openai.com](https://platform.openai.com)
- Set environment variable: `export OPENAI_API_KEY="sk-..."`

## Step-by-Step Guide

### Step 1: Understand LLM Agents

An **LLM Agent** in Ceylon is a special type of agent that:
- Connects to a language model (local or cloud)
- Maintains the LLM's configuration
- Sends messages to the LLM and returns responses
- Can be configured with prompts and parameters
- Manages the conversation context internally

### Step 2: Create and Configure the Agent

```python
# Create agent instance with model identifier
agent = ceylon.LlmAgent("demo_agent", "ollama::gemma3:latest")
```

Breaking this down:

- **First parameter (`"demo_agent"`)**: The name of your agent (unique identifier in the mesh)
- **Second parameter (`"ollama::gemma3:latest"`)**: The model identifier
  - Format: `provider::model:tag`
  - `ollama::` = Use local Ollama instance
  - `gemma3:latest` = Model name and version

Other model examples:
- `"ollama::mistral:latest"` - Mistral model via Ollama
- `"anthropic::claude-3-5-sonnet-20241022"` - Claude via Anthropic
- `"openai::gpt-4o"` - GPT-4o via OpenAI

### Step 3: Set System Prompt

```python
agent.with_system_prompt("You are a helpful assistant. Be concise.")
```

The system prompt:
- Sets the persona and behavior of the LLM
- Is sent with every message to guide responses
- Should be clear and specific
- Common examples:
  - `"You are a helpful assistant."` - General purpose
  - `"You are a Python expert. Give concise answers."` - Specialized
  - `"You are a teacher. Explain concepts clearly for beginners."` - Role-based

### Step 4: Configure LLM Parameters

```python
# Set randomness (0.0 = deterministic, 1.0 = very creative)
agent.with_temperature(0.7)

# Set maximum response length (in tokens, roughly 4 chars per token)
agent.with_max_tokens(100)
```

**Temperature** controls response creativity:
- `0.0`: Deterministic, same response every time (good for factual Q&A)
- `0.3-0.5`: Focused, slightly varied (good for most applications)
- `0.7`: Balanced, creative but reasonable (default for conversations)
- `1.0+`: Very random and creative (good for brainstorming)

**Max Tokens** controls response length:
- `50`: Brief, one-sentence responses
- `100-200`: Paragraph-length responses
- `500+`: Multi-paragraph, detailed responses
- `0` or not set: Let the model decide (may be longer)

### Step 5: Build the Agent

```python
agent.build()
```

This finalizes the agent configuration and connects to the LLM. After building:
- Configuration is locked in
- Agent is ready to accept messages
- Connection to LLM is established

### Step 6: Have a Conversation

```python
questions = [
    "What is 2+2?",
    "What is the capital of France?",
    "Write a haiku about Python programming",
]

for i, question in enumerate(questions, 1):
    print(f"Q{i}: {question}")
    try:
        response = agent.send_message(question)
        print(f"A{i}: {response}\n")
    except Exception as e:
        print(f"Error: {e}\n")
```

How this works:

- **`enumerate(questions, 1)`**: Loop through questions, starting numbering at 1
- **`agent.send_message(question)`**: Send message to LLM, get response
- **`try/except`**: Handle potential errors gracefully
- **Print results**: Display Q&A pairs

## Complete Code with Inline Comments

```python
#!/usr/bin/env python3
"""
Demo showing LLM conversation with actual responses.

This example demonstrates:
1. Creating an LLM agent
2. Configuring the agent with system prompt and parameters
3. Having a conversation with the LLM
4. Handling errors gracefully

The agent can use either:
- Local Ollama instance (free, no API keys needed)
- Cloud LLM APIs (Claude, GPT, etc.)
"""

import ceylon

def main():
    """Main demo function"""
    # Print header
    print("=" * 60)
    print("Ceylon LlmAgent - Conversation Demo")
    print("=" * 60)

    # STEP 1: Create an LLM agent
    # The agent will use Ollama's gemma3 model running locally
    # If you have a different model, change "gemma3:latest" to your model
    print("\n1. Creating LLM agent with gemma3:latest...")
    agent = ceylon.LlmAgent("demo_agent", "ollama::gemma3:latest")

    # STEP 2: Configure the system prompt
    # This tells the model how to behave and what role to play
    agent.with_system_prompt("You are a helpful assistant. Be concise.")

    # STEP 3: Configure temperature
    # 0.7 is a good balance between creativity and consistency
    # Lower (0.1-0.3) = more deterministic/factual
    # Higher (0.8-1.0) = more creative/varied
    agent.with_temperature(0.7)

    # STEP 4: Set maximum token limit
    # This limits response length (roughly 1 token ≈ 4 characters)
    # 100 tokens ≈ 1-2 paragraphs
    agent.with_max_tokens(100)

    # STEP 5: Build the agent
    # This finalizes configuration and connects to the LLM
    agent.build()
    print("[OK] Agent created and built")

    # STEP 6: Start conversation
    print("\n2. Starting conversation...\n")

    # Define some test questions
    questions = [
        "What is 2+2?",
        "What is the capital of France?",
        "Write a haiku about Python programming",
    ]

    # Ask each question and get responses
    for i, question in enumerate(questions, 1):
        print(f"Q{i}: {question}")
        try:
            # Send message to LLM and get response
            response = agent.send_message(question)
            # Display the response
            print(f"A{i}: {response}\n")
        except Exception as e:
            # Handle any errors gracefully
            print(f"Error: {e}\n")

    # Print footer
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

## Running the Example

### 1. Prepare Your Environment

**If using Ollama:**

```bash
# Install Ollama from https://ollama.com
# Start Ollama server
ollama serve

# In a new terminal, pull a model
ollama pull gemma3:latest
```

**If using Anthropic Claude:**

```bash
# Get API key from https://console.anthropic.com
# Set environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Or on Windows PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. Run the Script

```bash
cd bindings/python/examples
python demo_conversation.py
```

### 3. Expected Output (with Ollama)

```
============================================================
Ceylon LlmAgent - Conversation Demo
============================================================

1. Creating LLM agent with gemma3:latest...
[OK] Agent created and built

2. Starting conversation...

Q1: What is 2+2?
A1: 2+2 equals 4.

Q2: What is the capital of France?
A2: The capital of France is Paris.

Q3: Write a haiku about Python programming
A3: Code flows so free,
Logic weaves through the symbols,
Beauty in the bytes.

============================================================
Demo complete!
============================================================
```

## Key Concepts Explained

### LLM Agent vs Regular Agent

| Aspect | Regular Agent | LLM Agent |
|--------|---------------|-----------|
| Message Handler | Custom Python code | LLM model |
| Response | Deterministic | Probabilistic |
| Capability | Whatever you code | General intelligence |
| Configuration | Constructor params | Prompts + parameters |
| Use Case | Logic/workflow | Natural conversation |

### System Prompt Best Practices

```python
# ✅ Good: Clear and specific
agent.with_system_prompt("You are a math tutor. Explain each step clearly.")

# ✅ Good: Role-based
agent.with_system_prompt("You are a professional Python code reviewer.")

# ✅ Good: Behavior-guided
agent.with_system_prompt("Answer in 1-2 sentences. Be technical.")

# ❌ Bad: Too vague
agent.with_system_prompt("Be helpful.")

# ❌ Bad: Contradictory
agent.with_system_prompt("Be concise and write very detailed explanations.")
```

### Model Provider Formats

```python
# Ollama (local)
"ollama::gemma3:latest"
"ollama::mistral:latest"
"ollama::llama2:latest"

# Anthropic
"anthropic::claude-3-5-sonnet-20241022"
"anthropic::claude-opus-4-1-20250805"

# OpenAI
"openai::gpt-4o"
"openai::gpt-4-turbo"
"openai::gpt-3.5-turbo"

# Google Vertex (if supported)
"vertex::gemini-pro"
"vertex::gemini-2-flash"
```

### Configuration Pipeline

```python
agent = ceylon.LlmAgent("name", "model_id")
    .with_system_prompt("...")    # Set behavior
    .with_temperature(0.7)         # Set creativity
    .with_max_tokens(200)          # Set length limit
    .build()                        # Finalize config
```

Each method returns the agent, allowing chaining (fluent interface).

## Troubleshooting

### Issue: "Connection refused" or "Cannot connect to Ollama"

**Symptoms**: Error message about connection to Ollama

**Solutions**:
1. Verify Ollama is running: `ollama serve` in a terminal
2. Check the model is pulled: `ollama list`
3. If not pulled yet: `ollama pull gemma3:latest`
4. Verify the model name matches exactly

### Issue: "Model not found"

**Symptoms**: Error saying the model doesn't exist

**Solutions**:
1. List available models: `ollama list`
2. Pull the model: `ollama pull mistral:latest`
3. Check spelling in code matches exactly

### Issue: "ANTHROPIC_API_KEY not set" or API authentication errors

**Symptoms**: Error about API key when using Claude

**Solutions**:
1. Get your key from [console.anthropic.com](https://console.anthropic.com)
2. Set the environment variable:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```
3. Verify it's set: `echo $ANTHROPIC_API_KEY`
4. Restart your terminal or Python session after setting

### Issue: Responses are too long or too short

**Problem**: Response length doesn't match expectations

**Solutions**:
```python
# For shorter responses
agent.with_max_tokens(50)

# For longer responses
agent.with_max_tokens(500)

# For more consistent responses (less creative)
agent.with_temperature(0.3)

# For more varied responses
agent.with_temperature(0.8)
```

### Issue: Rate limiting or API quota errors

**Problem**: Getting errors about rate limits

**Solutions**:
1. Add delays between requests: `time.sleep(1)`
2. Check your API usage/quota in the provider console
3. Consider upgrading your API plan
4. Switch to local Ollama to avoid API limits

### Issue: SSL Certificate Error

**Problem**: Certificate validation errors with API calls

**Solutions**:
```python
# This is usually an environment issue, not code
# Ensure you have proper SSL certificates installed:
# - Windows: Run "Install Certificates.command" in Python folder
# - macOS: Install certificates via Python installer
# - Linux: `sudo apt-get install ca-certificates`
```

## Advanced Usage Patterns

### Multi-Turn Conversations

```python
agent = ceylon.LlmAgent("chat", "ollama::gemma3:latest")
agent.with_system_prompt("You are a helpful assistant.")
agent.build()

# Each send_message maintains context
response1 = agent.send_message("What's Python?")
print(response1)

response2 = agent.send_message("Why is it popular?")  # Agent remembers context
print(response2)

response3 = agent.send_message("Can you give an example?")
print(response3)
```

### Specialized Agents

```python
# Code reviewer agent
code_reviewer = ceylon.LlmAgent("reviewer", "anthropic::claude-3-5-sonnet-20241022")
code_reviewer.with_system_prompt(
    "You are an expert code reviewer. Review the code and suggest improvements."
)
code_reviewer.with_temperature(0.3)  # More deterministic for reviews
code_reviewer.build()

# Creative writing agent
writer = ceylon.LlmAgent("writer", "ollama::gemma3:latest")
writer.with_system_prompt("You are a creative fiction writer.")
writer.with_temperature(0.9)  # More creative
writer.build()
```

### Error Handling Pattern

```python
def safe_query(agent, question: str, max_retries: int = 3) -> str:
    """Safely query an agent with retry logic"""
    for attempt in range(max_retries):
        try:
            return agent.send_message(question)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(1)
            else:
                print(f"Failed after {max_retries} attempts")
                return None
```

## Next Steps

Now that you understand LLM conversation, explore:

1. **Async Operations** (`../async/async-llm.md`): Handle multiple LLM queries concurrently
2. **Memory System** (`../memory/basic-memory.md`): Store conversation history
3. **RAG System** (`../rag/markdown-rag.md`): Combine LLMs with knowledge bases for better answers
4. **Agent Networks**: Connect multiple agents with different capabilities

## Common Mistakes to Avoid

1. **Forgetting to call `.build()`**: Agent won't work until built
2. **Wrong model identifier**: Always verify the provider and model name
3. **No API key**: Set environment variables before running
4. **Unrealistic max_tokens**: Set a reasonable limit (start with 100-200)
5. **Not handling exceptions**: Network calls can fail, always use try/except

## Summary

The LLM conversation example demonstrates:
- ✅ Creating LLM agents with language models
- ✅ Configuring agent behavior with system prompts
- ✅ Tuning LLM parameters (temperature, max tokens)
- ✅ Sending messages and receiving responses
- ✅ Error handling for API interactions

This example is your foundation for building intelligent applications with large language models.

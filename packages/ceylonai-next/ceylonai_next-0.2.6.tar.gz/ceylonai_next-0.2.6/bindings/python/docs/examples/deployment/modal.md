# Modal.com Deployment Example

This example demonstrates deploying a Ceylon AI agent to Modal.com's serverless platform.

## Overview

Modal.com provides serverless infrastructure perfect for deploying Ceylon AI agents. This example shows the complete workflow from development to production deployment.

## Example Code

### Simple Chat Agent

```python
import modal

# Create Modal app
app = modal.App("ceylon-chat-agent")

# Persistent volume for Ollama models
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# Image with Ceylon AI and Ollama
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("curl")
    .run_commands("curl -fsSL https://ollama.ai/install.sh | sh")
    .pip_install("ceylonai-next>=0.2.5", "fastapi[standard]")
)

def ensure_ollama_running():
    """Start Ollama server and ensure model is available."""
    import subprocess
    import time

    # Start Ollama
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)

    # Pull model if not available
    result = subprocess.run(["ollama", "list"],
                           capture_output=True, text=True)
    if "qwen2.5:0.5b" not in result.stdout:
        print("Downloading model (first run only)...")
        subprocess.run(["ollama", "pull", "qwen2.5:0.5b"], check=True)
        ollama_volume.commit()

@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def chat(message: str) -> dict:
    """Process a chat message with Ceylon AI."""
    from ceylonai_next import LlmAgent

    ensure_ollama_running()

    # Create agent
    agent = LlmAgent("assistant", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt("You are a helpful AI assistant.")
    agent.build()

    # Get response
    response = await agent.send_message_async(message)

    return {
        "message": message,
        "response": response,
        "status": "success"
    }

@app.function(image=image, volumes={"/root/.ollama": ollama_volume})
@modal.web_endpoint(method="POST")
async def api(request: dict) -> dict:
    """HTTP API endpoint for the chat agent."""
    message = request.get("message", "")
    if not message:
        return {"error": "No message provided"}

    return await chat.remote.aio(message)

@app.local_entrypoint()
def main():
    """Test the agent locally."""
    print("Testing Ceylon AI agent on Modal...")
    result = chat.remote("What is Ceylon AI?")
    print(f"Response: {result['response']}")

if __name__ == "__main__":
    print("Run with: modal run example.py")
    print("Deploy with: modal deploy example.py")
```

## Running the Example

### 1. Install Dependencies

```bash
pip install ceylonai-next modal
```

### 2. Authenticate with Modal

```bash
modal setup
```

### 3. Test Locally

```bash
modal run example.py
```

Output:

```
✓ Created objects.
✓ Ollama server started
✓ Model already available (or downloading on first run)
Testing Ceylon AI agent on Modal...
Response: Ceylon AI is a framework for building multi-agent AI systems...
```

### 4. Deploy to Production

```bash
modal deploy example.py
```

Modal will output your deployment URL:

```
✓ Deployed web_endpoint api => https://your-app-modal.com
```

### 5. Test the Deployed API

```bash
curl -X POST https://your-app-modal.com \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from production!"}'
```

Response:

```json
{
  "message": "Hello from production!",
  "response": "Hello! How can I help you today?",
  "status": "success"
}
```

## More Examples

Ceylon AI provides several complete Modal.com examples in the repository:

### Simple Chatbot

**File**: `examples/modal_examples/simple_chatbot_modal.py`

Features multiple personality modes (friendly, professional, humorous).

```bash
modal run examples/modal_examples/simple_chatbot_modal.py
```

### Agent with Actions

**File**: `examples/modal_examples/action_tools_modal.py`

Demonstrates custom tool-calling with 5 different actions.

```bash
modal run examples/modal_examples/action_tools_modal.py
```

### Multi-Agent System

**File**: `examples/modal_examples/multi_agent_modal.py`

Customer service routing with specialized agents.

```bash
modal run examples/modal_examples/multi_agent_modal.py
```

### Conversation Agent

**File**: `examples/modal_examples/memory_agent_modal.py`

Multi-turn conversations with context retention.

```bash
modal run examples/modal_examples/memory_agent_modal.py
```

## Key Concepts

### Persistent Volumes

Modal's persistent volumes cache the Ollama models:

```python
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)
```

This prevents re-downloading models on every deployment, saving time and bandwidth.

### Image Configuration

Ceylon AI requires Ubuntu 24.04 for GLIBC 2.38+ support:

```python
image = modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
```

### Timeout Settings

First run needs time for model download:

```python
@app.function(timeout=900)  # 15 minutes
```

Subsequent runs are much faster as models are cached.

## Next Steps

- Read the [complete Modal.com guide](../../guide/deployment/modal.md)
- Explore [example files](https://github.com/ceylonai/next-processor/tree/main/bindings/python/examples/modal_examples)
- Check [Modal's documentation](https://modal.com/docs)
- Try different [Ollama models](https://ollama.ai/library)

## Resources

- [Modal.com Deployment Guide](../../guide/deployment/modal.md)
- [Example Files on GitHub](https://github.com/ceylonai/next-processor/tree/main/bindings/python/examples/modal_examples)
- [Modal Documentation](https://modal.com/docs)
- [Ollama Models](https://ollama.ai/library)

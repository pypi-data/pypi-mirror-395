# Modal + Ceylon AI Quick Start

This guide helps you quickly get started with running Ceylon AI on Modal.

## Step 1: Setup

```bash
# Navigate to the python bindings directory
cd bindings/python

# Activate virtual environment
../../.venv/Scripts/activate  # Windows
# source ../../.venv/bin/activate  # Linux/Mac

# Install Modal
uv pip install modal

# Setup Modal authentication
modal setup
```

## Step 2: Install and Start Ollama

Modal will run Ollama inside containers, but **NOTE**: The current example installs Ollama in the container, which makes the image build slower.

**For faster local testing**, you have two options:

### Option A: Local Ollama (Recommended for testing)

1. Install Ollama locally: [https://ollama.ai](https://ollama.ai)
2. Run Ollama: `ollama serve`
3. Pull a small model: `ollama pull qwen2.5:0.5b`
4. Modify the example to connect to your local Ollama (see below)

### Option B: Use Modal's Ollama in Container (Current example)

The example automatically installs and runs Ollama in the Modal container. This is slower to build but works without local setup.

## Step 3: Run the Example

```bash
# Make sure you're in the bindings/python directory
# and your virtual environment is activated

# Run the Ceylon AI Modal example
modal run examples/modal_examples/ceylon_modal_agent.py
```

## Alternative: Simple Local Example

If Modal setup is taking too long, try this simple local Ceylon AI example first:

```python
# examples/modal_examples/simple_local_test.py
import asyncio
from ceylonai_next import LlmAgent

async def main():
    # Create agent with Ollama
    agent = LlmAgent("assistant", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt("You are a helpful assistant.")
    agent.build()

    # Test message
    response = await agent.send_message_async("What is Python?")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python examples/modal_examples/simple_local_test.py
```

## Troubleshooting

### Modal command not found

- Ensure your virtual environment is activated
- Try: `python -m modal` instead of `modal`
- Or add the virtual environment's Scripts folder to PATH

### Ollama connection issues

- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Pull the model if needed: `ollama pull qwen2.5:0.5b`

### Slow Modal image build

- The first run will be slow as it downloads and installs Ollama
- Subsequent runs will be faster due to caching
- Consider using local Ollama for testing (Option A above)

## What model should I use?

For testing and demos:

- **qwen2.5:0.5b** - Smallest, fastest (500MB)
- **qwen2.5:1.5b** - Good balance (1.5GB)
- **llama3.2:1b** - Better quality (1.3GB)

For production:

- **llama3.1:8b** - High quality (4.7GB)
- **gemma2:9b** - Very good quality (5.5GB)

## Next Steps

1. ✅ Run the basic Modal example
2. ✅ Try the Ceylon AI integration
3. Deploy your agent: `modal deploy examples/modal_examples/ceylon_modal_agent.py`
4. Access via web API (Modal provides the URL after deployment)

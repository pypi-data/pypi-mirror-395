# Ceylon AI on Modal - Examples

This directory contains examples demonstrating how to deploy Ceylon AI agents on [Modal](https://modal.com) - a serverless platform for running Python code in the cloud.

## What is Modal?

Modal is a serverless compute platform that makes it easy to run Python code in the cloud without managing infrastructure. Combined with Ceylon AI, you can build and deploy scalable AI agent systems with:

- **Serverless Deployment**: No infrastructure management needed
- **Automatic Scaling**: Handles traffic spikes automatically
- **GPU Support**: Optional GPU acceleration for larger models
- **Easy Deployment**: Single command to deploy
- **No API Keys**: Uses local Ollama models

## Ceylon AI Examples

All examples use Ceylon AI's `ceylonai_next` library with Ollama integration for local LLM inference.

### 1. Ceylon AI Agent (`ceylon_modal_agent.py`)

**Comprehensive example** showing multiple Ceylon AI patterns in one file.

**Features:**

- Simple agent with async messaging
- Agent with custom actions/tools
- Batch message processing
- Web API endpoint

```bash
modal run ceylon_modal_agent.py
```

**Learning Path:** Start here to see all basic patterns in one place.

---

### 2. Multi-Agent System (`multi_agent_modal.py`)

**Use case:** Customer service routing system with specialized agents

**Features:**

- Multiple agents communicating via PyLocalMesh
- Intelligent query routing
- Specialized agents for different domains (technical, billing, general)
- Agent coordination patterns

```bash
modal run multi_agent_modal.py
```

**Example:** Routes customer queries to technical support, billing, or general agents based on content.

---

### 3. Memory-Enhanced Agent (`memory_agent_modal.py`)

**Use case:** Conversational assistant that remembers context

**Features:**

- InMemoryBackend for persistent conversations
- Memory save and search capabilities
- Multi-turn conversation handling
- Context-aware responses

```bash
modal run memory_agent_modal.py
```

**Example:** Agent remembers user preferences and previous conversation details.

---

### 4. Simple Chatbot (`simple_chatbot_modal.py`)

**Use case:** Interactive Q&A chatbot with personality modes

**Features:**

- Basic LlmAgent usage
- Multiple personality configurations (friendly, professional, humorous)
- Single-turn and multi-turn conversations
- Async messaging patterns

```bash
modal run simple_chatbot_modal.py
```

**Learning Path:** Best example for learning Ceylon AI basics.

---

### 5. Action Tools Agent (`action_tools_modal.py`)

**Use case:** Agent with real-time data access and calculation abilities

**Features:**

- Defining custom actions with `@agent.action` decorator
- Automatic tool selection by the LLM
- Function calling with parameters
- Multiple tool types (calculations, data retrieval, conversions)

```bash
modal run action_tools_modal.py
```

**Tools Included:**

- Current time/date
- Math calculator
- Weather lookup
- Knowledge base search
- Temperature conversion

---

## Prerequisites

1. **Install Modal**:

   ```bash
   pip install modal
   ```

2. **Authenticate**:

   ```bash
   modal setup
   ```

   This will open a browser window to authenticate with Modal.

3. **Create a Modal account** at [modal.com](https://modal.com) if you don't have one.

4. **For Ceylon AI** (automatic):
   - Ceylon AI examples use **Ollama** with the **qwen2.5:0.5b** model
   - The model downloads automatically on first run (~397 MB)
   - No API keys required!

## Running Examples

### Quick Start

```bash
# Activate your virtual environment
cd bindings/python
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Test an example locally
modal run examples/modal_examples/simple_chatbot_modal.py

# Deploy to production
modal deploy examples/modal_examples/simple_chatbot_modal.py

# View your deployed apps
modal app list
```

### Commands

- **`modal run <script.py>`** - Execute once for testing
- **`modal deploy <script.py>`** - Deploy as a persistent service
- **`modal serve <script.py>`** - Run locally with hot reload for development

## Ceylon AI Features Showcase

The examples demonstrate various framework capabilities:

| Feature                | Example File              | Description                       |
| ---------------------- | ------------------------- | --------------------------------- |
| **LlmAgent**           | `simple_chatbot_modal.py` | Basic conversational agent        |
| **Custom Actions**     | `action_tools_modal.py`   | Agent with tool-calling abilities |
| **Memory**             | `memory_agent_modal.py`   | Persistent conversation history   |
| **Multi-Agent**        | `multi_agent_modal.py`    | Agent coordination & routing      |
| **Async Messaging**    | All examples              | Non-blocking communication        |
| **Ollama Integration** | All examples              | Local LLM without API keys        |
| **Batch Processing**   | `ceylon_modal_agent.py`   | Process multiple messages         |
| **Web API**            | All examples              | FastAPI endpoint deployment       |

## Learning Path

Recommended order for learning:

1. **Start**: `simple_chatbot_modal.py` - Understand basic patterns
2. **Actions**: `action_tools_modal.py` - Learn to add custom tools
3. **Memory**: `memory_agent_modal.py` - Add conversation persistence
4. **Advanced**: `multi_agent_modal.py` - Build multi-agent systems
5. **Reference**: `ceylon_modal_agent.py` - See all patterns together

## Troubleshooting

### Modal authentication fails

- Run `modal token new` to create a new token
- Check your internet connection

### Ollama model not found

- The model downloads automatically on first run
- If it fails, check Modal function logs in the dashboard
- First run takes ~5-10 minutes for model download

### Function timeout

- Increase the `timeout` parameter in `@app.function(timeout=900)`
- First run is slower due to model downloading
- Subsequent runs use cached model from volume

### "Module not found" errors

- Ensure `ceylonai-next>=0.2.5` is in the image pip_install
- Check that Modal image build completed successfully

## Deployment Tips

### Cost Optimization

- Use the small `qwen2.5:0.5b` model for lower costs
- Set appropriate timeout values (default: 900s)
- Use volumes to cache Ollama models

### Production Readiness

- Add error handling for edge cases
- Implement request validation
- Add logging and monitoring
- Set up rate limiting if needed

### Scaling

- Modal automatically scales based on traffic
- No configuration needed for basic scaling
- Monitor usage in Modal dashboard

## Architecture

All examples follow this common pattern:

```python
# 1. Image with Ceylon AI + Ollama
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("curl")
    .run_commands("curl -fsSL https://ollama.ai/install.sh | sh")
    .pip_install("ceylonai-next>=0.2.5", "fastapi[standard]")
)

# 2. Persistent volume for models
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# 3. Function with Ceylon AI agent
@app.function(image=image, volumes={"/root/.ollama": ollama_volume})
async def run_agent(message: str):
    ensure_ollama_running()  # Start Ollama + download model
    agent = LlmAgent("agent_name", "ollama::qwen2.5:0.5b")
    agent.build()
    response = await agent.send_message_async(message)
    return {"response": response}

# 4. Web endpoint (optional)
@app.function(image=image, volumes={"/root/.ollama": ollama_volume})
@modal.web_endpoint(method="POST")
async def api(request: dict):
    return await run_agent.remote.aio(request["message"])
```

## Resources

### Modal

- [Modal Documentation](https://modal.com/docs)
- [Modal API Reference](https://modal.com/docs/reference)
- [Modal Examples](https://modal.com/docs/examples)

### Ceylon AI

- [Ceylon AI Documentation](https://github.com/ceylonai/ceylon)
- [Ceylon AI Python Bindings](https://github.com/ceylonai/ceylon/tree/main/bindings/python)

### Ollama

- [Ollama Website](https://ollama.ai)
- [Ollama Models](https://ollama.ai/library)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Next Steps

1. **Try the examples** - Start with `simple_chatbot_modal.py`
2. **Customize** - Modify prompts, actions, and personalities
3. **Deploy** - Use `modal deploy` to make it production-ready
4. **Extend** - Add new features like RAG, database integration, etc.
5. **Monitor** - Check Modal dashboard for logs and metrics

## Support

- Check the [QUICKSTART.md](QUICKSTART.md) for quick setup
- Review example code comments for implementation details
- Modal dashboard has logs and debugging tools
- Ceylon AI has comprehensive documentation

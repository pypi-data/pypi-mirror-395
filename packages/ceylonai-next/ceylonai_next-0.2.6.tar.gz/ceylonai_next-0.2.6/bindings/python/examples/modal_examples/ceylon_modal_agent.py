"""
Ceylon AI + Modal Integration Example

This example demonstrates how to run Ceylon AI agents on Modal for scalable compute.
It uses Ollama with a small model (qwen2.5:0.5b) for fast, efficient inference.

Prerequisites:
1. Install Modal: pip install modal
2. Setup Modal: modal setup
3. Have Ollama running with qwen2.5:0.5b model:
   - Install Ollama: https://ollama.ai
   - Pull model: ollama pull qwen2.5:0.5b

Run with: modal run ceylon_modal_agent.py
Deploy with: modal deploy ceylon_modal_agent.py
"""

import modal

# Create a Modal app
app = modal.App("ceylon-modal-agent")

# Create a persistent volume for Ollama models (avoids re-downloading)
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# Define image with Ceylon AI and dependencies
# We install ceylonai-next from PyPI
# Using Ubuntu 24.04 for GLIBC 2.39 (ceylonai-next requires GLIBC 2.38+)
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("curl")  # For Ollama installation
    .run_commands(
        # Install Ollama (only installation, not model pulling)
        "curl -fsSL https://ollama.ai/install.sh | sh",
    )
    .pip_install(
        "ceylonai-next>=0.2.5",
        "fastapi[standard]"
    )
)


def ensure_ollama_running():
    """Ensure Ollama server is running and model is available."""
    import subprocess
    import time
    
    # Start Ollama server in the background
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Give it time to start
        time.sleep(3)
        print("✓ Ollama server started")
    except Exception as e:
        print(f"Note: Ollama server might already be running: {e}")
    
    # Check if model is available, pull if not
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "qwen2.5:0.5b" not in result.stdout:
            print("Pulling qwen2.5:0.5b model (first run only, ~397 MB)...")
            subprocess.run(
                ["ollama", "pull", "qwen2.5:0.5b"],
                check=True,
                timeout=600  # 10 minutes for model download
            )
            print("✓ Model pulled successfully")
            # Commit the volume to persist the downloaded model
            ollama_volume.commit()
        else:
            print("✓ Model already available")
    except Exception as e:
        print(f"Warning: Error checking/pulling model: {e}")


@app.function(
    image=image,
    timeout=900,  # 15 minutes for first-time model download
    volumes={"/root/.ollama": ollama_volume},  # Persist Ollama models
)
async def run_ceylon_agent(user_message: str) -> dict:
    """
    Run a Ceylon AI agent on Modal using Ollama.
    
    This function demonstrates how to run Ceylon AI LlmAgent in a serverless environment.
    Uses a small, efficient model (qwen2.5:0.5b) for fast inference.
    """
    from ceylonai_next import LlmAgent
    
    # Ensure Ollama is running
    ensure_ollama_running()
    
    print(f"Processing message: {user_message}")
    
    # Create an LLM agent using Ollama with a small model
    # qwen2.5:0.5b is a fast, lightweight model perfect for demos
    agent = LlmAgent("modal_assistant", "ollama::qwen2.5:0.5b")
    
    # Configure the agent
    agent.with_system_prompt(
        "You are a helpful assistant running on Modal. "
        "Provide concise, accurate responses."
    )
    
    # Build the agent
    agent.build()
    
    # Get response
    print(f"Sending message to agent: {user_message}")
    response = await agent.send_message_async(user_message)
    
    return {
        "message": user_message,
        "response": response,
        "agent": "modal_assistant",
        "model": "ollama::qwen2.5:0.5b",
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def run_agent_with_actions(user_message: str) -> dict:
    """
    Run a Ceylon AI agent with custom actions/tools.
    
    This demonstrates how to add custom functions that the agent can call.
    """
    from ceylonai_next import LlmAgent
    
    # Ensure Ollama is running
    ensure_ollama_running()
    
    print(f"Processing message with actions: {user_message}")
    
    # Create agent
    agent = LlmAgent("tool_assistant", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt(
        "You are a helpful assistant with access to tools. "
        "Use the available tools when appropriate."
    )
    
    # Define custom actions
    @agent.action(description="Get the current weather for a location")
    def get_weather(location: str) -> str:
        print(f"  [Action] Checking weather for {location}...")
        # Mock weather data
        weather_data = {
            "london": "Rainy, 15°C",
            "paris": "Sunny, 22°C",
            "tokyo": "Cloudy, 18°C",
            "new york": "Partly cloudy, 20°C",
        }
        return weather_data.get(location.lower(), f"Weather in {location}: Partly cloudy, 20°C")
    
    @agent.action(description="Calculate the result of a mathematical expression")
    def calculate(expression: str) -> str:
        print(f"  [Action] Calculating: {expression}")
        try:
            # Safe eval for basic math
            result = eval(expression, {"__builtins__": {}})
            return f"The result is: {result}"
        except:
            return f"Could not calculate: {expression}"
    
    # Build the agent
    agent.build()
    
    # Get response
    response = await agent.send_message_async(user_message)
    
    return {
        "message": user_message,
        "response": response,
        "agent": "tool_assistant",
        "model": "ollama::qwen2.5:0.5b",
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def batch_process_messages(messages: list[str]) -> list[dict]:
    """Process multiple messages with a single agent instance."""
    from ceylonai_next import LlmAgent
    
    # Ensure Ollama is running
    ensure_ollama_running()
    
    print(f"Batch processing {len(messages)} messages...")
    
    # Create one agent for all messages
    agent = LlmAgent("batch_assistant", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt("You are a helpful assistant. Be concise.")
    agent.build()
    
    results = []
    for i, msg in enumerate(messages, 1):
        print(f"Processing message {i}/{len(messages)}: {msg}")
        response = await agent.send_message_async(msg)
        results.append({
            "message": msg,
            "response": response,
            "index": i
        })
    
    return results


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
@modal.fastapi_endpoint(method="POST")
async def agent_api(request: dict) -> dict:
    """
    Web API endpoint for Ceylon AI agent.
    
    Deploy with: modal deploy ceylon_modal_agent.py
    
    Example request:
    curl -X POST <your-modal-url> \
      -H "Content-Type: application/json" \
      -d '{"message": "Hello, Ceylon!", "use_actions": false}'
    """
    message = request.get("message", "")
    use_actions = request.get("use_actions", False)
    
    if not message:
        return {"error": "No message provided"}
    
    # Choose which agent to use
    if use_actions:
        result = await run_agent_with_actions.remote.aio(message)
    else:
        result = await run_ceylon_agent.remote.aio(message)
    
    return result


@app.local_entrypoint()
def main():
    """Test Ceylon AI agent on Modal."""
    print("=" * 60)
    print("Ceylon AI + Modal Integration")
    print("Using Ollama with qwen2.5:0.5b model")
    print("=" * 60)
    
    # Test 1: Simple message
    print("\n1. Testing simple agent:")
    print("-" * 60)
    message = "What is Python? Answer in one sentence."
    print(f"User: {message}")
    result = run_ceylon_agent.remote(message)
    print(f"Agent: {result['response']}")
    print(f"Status: {result['status']}")
    
    # Test 2: Agent with actions
    print("\n2. Testing agent with custom actions:")
    print("-" * 60)
    message = "What's the weather in London?"
    print(f"User: {message}")
    result = run_agent_with_actions.remote(message)
    print(f"Agent: {result['response']}")
    
    # Test 3: Calculation action
    print("\n3. Testing calculation action:")
    print("-" * 60)
    message = "Calculate 42 * 17"
    print(f"User: {message}")
    result = run_agent_with_actions.remote(message)
    print(f"Agent: {result['response']}")
    
    # Test 4: Batch processing
    print("\n4. Testing batch processing:")
    print("-" * 60)
    messages = [
        "What is AI?",
        "Explain modal computing in one line",
        "What is 2+2?",
    ]
    print(f"Processing {len(messages)} messages...")
    results = batch_process_messages.remote(messages)
    for res in results:
        print(f"\n  Q: {res['message']}")
        print(f"  A: {res['response']}")
    
    print("\n" + "=" * 60)
    print("Integration Tips:")
    print("=" * 60)
    print("""
    ✓ No API keys needed - uses local Ollama
    ✓ Fast, small model (qwen2.5:0.5b)
    ✓ Custom actions/tools support
    ✓ Batch processing support
    
    Deployment:
    1. Deploy as web API:
       modal deploy ceylon_modal_agent.py
    
    2. Scale automatically:
       Modal handles scaling based on request volume
    
    3. Monitor via Modal dashboard:
       https://modal.com/apps
    
    4. Use different models:
       - qwen2.5:0.5b (small, fast)
       - llama3.2:1b (larger, better quality)
       - gemma2:2b (good balance)
    """)


if __name__ == "__main__":
    print("Run with: modal run ceylon_modal_agent.py")
    print("Deploy with: modal deploy ceylon_modal_agent.py")

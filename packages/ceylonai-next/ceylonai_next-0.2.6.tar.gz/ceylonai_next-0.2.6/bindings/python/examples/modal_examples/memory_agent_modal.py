"""
Ceylon AI Conversation Agent on Modal

This example demonstrates a multi-turn conversational agent using Ceylon AI.
The agent maintains context across messages within a single conversation.

Use case: Conversational chatbot that remembers context within the conversation

Prerequisites:
1. Install Modal: pip install modal
2. Setup Modal: modal setup

Run with: modal run memory_agent_modal.py
Deploy with: modal deploy memory_agent_modal.py
"""

import modal

# Create a Modal app
app = modal.App("ceylon-conversation-agent")

# Create a persistent volume for Ollama models
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# Define image with Ceylon AI and dependencies
image = (
    modal.Image.from_registry("ubuntu:24.04", add_python="3.12")
    .apt_install("curl")
    .run_commands(
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
    
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        print("✓ Ollama server started")
    except Exception as e:
        print(f"Note: Ollama server might already be running: {e}")
    
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
                timeout=600
            )
            print("✓ Model pulled successfully")
            ollama_volume.commit()
        else:
            print("✓ Model already available")
    except Exception as e:
        print(f"Warning: Error checking/pulling model: {e}")


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def run_conversation(messages: list[str]) -> dict:
    """
    Run a multi-turn conversation with a Ceylon AI agent.
    
    Args:
        messages: List of user messages to send in sequence
    
    This demonstrates conversation context retention across multiple messages.
    """
    from ceylonai_next import LlmAgent
    
    ensure_ollama_running()
    
    print(f"Starting conversation with {len(messages)} messages")
    
    # Create agent
    agent = LlmAgent("conversation_agent", "ollama::qwen2.5:0.5b")
    agent.with_system_prompt(
        "You are a friendly assistant. Pay attention to details users share "
        "and reference them in your responses when relevant."
    )
    agent.build()
    
    print("✓ Agent initialized")
    
    # Process messages in sequence
    conversation = []
    for i, msg in enumerate(messages, 1):
        print(f"\n[{i}] User: {msg}")
        response = await agent.send_message_async(msg)
        print(f"[{i}] Agent: {response}")
        
        conversation.append({
            "turn": i,
            "user": msg,
            "agent": response
        })
    
    return {
        "conversation": conversation,
        "total_turns": len(conversation),
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
@modal.fastapi_endpoint(method="POST")
async def conversation_api(request: dict) -> dict:
    """
    Web API endpoint for conversational agent.
    
    Deploy with: modal deploy memory_agent_modal.py
    
    Example request:
    curl -X POST <your-modal-url> \\
      -H "Content-Type: application/json" \\
      -d '{
        "messages": [
          "Hi, my name is Alice",
          "What is my name?"
        ]
      }'
    """
    messages = request.get("messages", [])
    
    if not messages:
        return {"error": "No messages provided"}
    
    result = await run_conversation.remote.aio(messages)
    return result


@app.local_entrypoint()
def main():
    """Test conversational agent on Modal."""
    print("=" * 60)
    print("Ceylon AI Conversation Agent on Modal")
    print("Multi-Turn Conversation Demo")
    print("=" * 60)
    
    # Test 1: Context retention test
    print("\n1. Testing conversation context retention:")
    print("-" * 60)
    
    messages = [
        "Hi! My name is Alice and I love Python programming.",
        "What's my name?",
        "What programming language do I like?",
    ]
    
    result = run_conversation.remote(messages)
    
    print("\n" + "=" * 60)
    print("Conversation Results:")
    print("=" * 60)
    for turn in result["conversation"]:
        print(f"\nTurn {turn['turn']}:")
        print(f"  User: {turn['user']}")
        print(f"  Agent: {turn['agent']}")
    
    print(f"\nTotal turns: {result['total_turns']}")
    print(f"Status: {result['status']}")
    
    # Test 2: Another conversation
    print("\n\n2. Testing another conversation:")
    print("-" * 60)
    
    messages = [
        "I prefer dark mode for my IDE",
        "I also like tabs over spaces",
        "What coding preferences did I mention?",
    ]
    
    result = run_conversation.remote(messages)
    
    print("\n" + "=" * 60)
    print("Conversation Results:")
    print("=" * 60)
    for turn in result["conversation"]:
        print(f"\nTurn {turn['turn']}:")
        print(f"  User: {turn['user']}")
        print(f"  Agent: {turn['agent']}")
    
    print(f"\nTotal turns: {result['total_turns']}")
    
    print("\n" + "=" * 60)
    print("Conversation Agent Features:")
    print("=" * 60)
    print("""
    ✓ Multi-turn conversation handling
    ✓ Context retention across messages
    ✓ Natural conversation flow
    ✓ Fast responses (qwen2.5:0.5b model)
    
    Use Cases:
    - Personal assistants
    - Customer support chatbots
    - Tutoring systems
    - Interactive Q&A
    
    Deployment:
    1. Deploy: modal deploy memory_agent_modal.py
    2. Use API endpoint for persistent service
    """)


if __name__ == "__main__":
    print("Run with: modal run memory_agent_modal.py")
    print("Deploy with: modal deploy memory_agent_modal.py")

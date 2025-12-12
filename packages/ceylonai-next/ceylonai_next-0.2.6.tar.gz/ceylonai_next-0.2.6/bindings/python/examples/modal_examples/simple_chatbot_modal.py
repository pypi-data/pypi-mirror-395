"""
Ceylon AI Simple Chatbot on Modal

This example demonstrates a simple conversational chatbot using Ceylon AI.
Perfect for understanding the basics of LlmAgent and async messaging.

Use case: Interactive Q&A chatbot

Prerequisites:
1. Install Modal: pip install modal
2. Setup Modal: modal setup

Run with: modal run simple_chatbot_modal.py
Deploy with: modal deploy simple_chatbot_modal.py
"""

import modal

# Create a Modal app
app = modal.App("ceylon-simple-chatbot")

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
async def chat(message: str, personality: str = "friendly") -> dict:
    """
    Simple chat function using Ceylon AI.
    
    Args:
        message: User's message
        personality: Chatbot personality ('friendly', 'professional', 'humorous')
    
    Returns:
        Response dict with message and metadata
    """
    from ceylonai_next import LlmAgent
    
    ensure_ollama_running()
    
    print(f"Chat request - Personality: {personality}, Message: {message}")
    
    # Define personality prompts
    prompts = {
        "friendly": "You are a friendly and warm chatbot. Be helpful and conversational.",
        "professional": "You are a professional assistant. Be concise and formal.",
        "humorous": "You are a witty chatbot with a good sense of humor. Make people smile.",
    }
    
    system_prompt = prompts.get(personality, prompts["friendly"])
    
    # Create chatbot agent
    chatbot = LlmAgent("chatbot", "ollama::qwen2.5:0.5b")
    chatbot.with_system_prompt(system_prompt)
    chatbot.build()
    
    print("✓ Chatbot initialized")
    
    # Get response
    response = await chatbot.send_message_async(message)
    
    return {
        "user_message": message,
        "bot_response": response,
        "personality": personality,
        "model": "ollama::qwen2.5:0.5b",
        "status": "success"
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
async def interactive_conversation(messages: list[str], personality: str = "friendly") -> dict:
    """
    Have a multi-turn conversation with the chatbot.
    
    Args:
        messages: List of user messages
        personality: Chatbot personality
    
    Returns:
        Full conversation history
    """
    from ceylonai_next import LlmAgent
    
    ensure_ollama_running()
    
    prompts = {
        "friendly": "You are a friendly and warm chatbot. Be helpful and conversational.",
        "professional": "You are a professional assistant. Be concise and formal.",
        "humorous": "You are a witty chatbot with a good sense of humor. Make people smile.",
    }
    
    chatbot = LlmAgent("chatbot", "ollama::qwen2.5:0.5b")
    chatbot.with_system_prompt(prompts.get(personality, prompts["friendly"]))
    chatbot.build()
    
    conversation = []
    for i, msg in enumerate(messages, 1):
        print(f"\n[Turn {i}] User: {msg}")
        response = await chatbot.send_message_async(msg)
        print(f"[Turn {i}] Bot: {response}")
        
        conversation.append({
            "turn": i,
            "user": msg,
            "bot": response
        })
    
    return {
        "conversation": conversation,
        "personality": personality,
        "total_turns": len(conversation)
    }


@app.function(
    image=image,
    timeout=900,
    volumes={"/root/.ollama": ollama_volume},
)
@modal.web_endpoint(method="POST")
async def chatbot_api(request: dict) -> dict:
    """
    Web API endpoint for the chatbot.
    
    Deploy with: modal deploy simple_chatbot_modal.py
    
    Example request:
    curl -X POST <your-modal-url> \\
      -H "Content-Type: application/json" \\
      -d '{
        "message": "Tell me a joke",
        "personality": "humorous"
      }'
    """
    message = request.get("message", "")
    personality = request.get("personality", "friendly")
    
    if not message:
        return {"error": "No message provided"}
    
    result = await chat.remote.aio(message, personality)
    return result


@app.local_entrypoint()
def main():
    """Test simple chatbot on Modal."""
    print("=" * 60)
    print("Ceylon AI Simple Chatbot on Modal")
    print("=" * 60)
    
    # Test 1: Single messages with different personalities
    print("\n1. Testing different personalities:")
    print("-" * 60)
    
    test_cases = [
        ("What's the weather like today?", "friendly"),
        ("Explain quantum computing", "professional"),
        ("Why did the chicken cross the road?", "humorous"),
    ]
    
    for message, personality in test_cases:
        print(f"\nPersonality: {personality}")
        print(f"User: {message}")
        result = chat.remote(message, personality)
        print(f"Bot: {result['bot_response']}")
    
    # Test 2: Multi-turn conversation
    print("\n\n2. Testing multi-turn conversation:")
    print("-" * 60)
    
    messages = [
        "Hi, how are you?",
        "What can you help me with?",
        "Tell me something interesting about AI",
    ]
    
    result = interactive_conversation.remote(messages, "friendly")
    for turn in result["conversation"]:
        print(f"\nTurn {turn['turn']}:")
        print(f"  User: {turn['user']}")
        print(f"  Bot: {turn['bot']}")
    
    print(f"\nTotal turns: {result['total_turns']}")
    
    print("\n" + "=" * 60)
    print("Chatbot Features:")
    print("=" * 60)
    print("""
    ✓ Multiple personality modes
    ✓ Single-turn and multi-turn conversations
    ✓ Fast responses with small model
    ✓ Easy to customize
    
    Personalities:
    - friendly: Warm and conversational
    - professional: Concise and formal
    - humorous: Witty and entertaining
    
    Deployment:
    modal deploy simple_chatbot_modal.py
    """)


if __name__ == "__main__":
    print("Run with: modal run simple_chatbot_modal.py")
    print("Deploy with: modal deploy simple_chatbot_modal.py")

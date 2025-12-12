#!/usr/bin/env python3
"""
Simple local Ceylon AI test - no Modal required

This is a simple test to verify Ceylon AI works with Ollama locally
before trying to run it on Modal.

Prerequisites:
1. Install Ollama: https://ollama.ai
2. Start Ollama: ollama serve
3. Pull model: ollama pull qwen2.5:0.5b
4. Install ceylonai-next: pip install ceylonai-next

Run: python simple_local_test.py
"""

import asyncio
from ceylonai_next import LlmAgent


async def main():
    """Test Ceylon AI agent locally."""
    print("=" * 60)
    print("Ceylon AI Local Test")
    print("Using Ollama with qwen2.5:0.5b")
    print("=" * 60)
    
    # Create agent with Ollama
    print("\nCreating agent...")
    agent = LlmAgent("local_assistant", "ollama::qwen2.5:0.5b")
    
    # Configure agent
    agent.with_system_prompt(
        "You are a helpful assistant. Provide concise, accurate answers."
    )
    
    # Build agent
    print("Building agent...")
    agent.build()
    
    # Test messages
    test_messages = [
        "What is Python?",
        "What is 5 + 7?",
        "Name one benefit of using Rust.",
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Test {i}] User: {message}")
        response = await agent.send_message_async(message)
        print(f"[Test {i}] Agent: {response}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\nIf this works, you're ready to try Modal!")
    print("Run: modal run examples/modal_examples/ceylon_modal_agent.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Is Ollama running? Try: ollama serve")
        print("2. Is the model downloaded? Try: ollama pull qwen2.5:0.5b")
        print("3. Is ceylonai-next installed? Try: pip install ceylonai-next")

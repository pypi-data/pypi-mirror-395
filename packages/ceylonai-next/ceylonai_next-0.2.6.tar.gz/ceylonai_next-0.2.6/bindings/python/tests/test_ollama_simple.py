#!/usr/bin/env python3
"""Simple test to diagnose Ollama connection."""

import ceylonai_next

print("Creating LLM agent...")
agent = ceylonai_next.LlmAgent("test", "ollama::gemma3:latest")
agent.with_system_prompt("You are helpful.")
agent.with_max_tokens(20)
agent.build()

print("Sending message...")
try:
    response = agent.send_message("Say hello")
    print(f"Success! Response: {response}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

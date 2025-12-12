#!/usr/bin/env python3
"""Simple test showing actual LLM response."""

import ceylonai_next

# Create agent
agent = ceylonai_next.LlmAgent("test", "ollama::gemma3:latest")
agent.with_system_prompt("Answer very briefly in one short sentence.")
agent.with_max_tokens(50)
agent.build()

# Ask a simple question
question = "What is 5 + 3?"
print(f"Question: {question}")

response = agent.send_message(question)
print(f"Response: {response}")

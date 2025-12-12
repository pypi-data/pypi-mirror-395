print("\n1. Creating LLM agent with gemma3:latest...")
agent = ceylon.LlmAgent("demo_agent", "ollama::gemma3:latest")
agent.with_system_prompt("You are a helpful assistant. Be concise.")
agent.with_temperature(0.7)
agent.with_max_tokens(100)
agent.build()
print("[OK] Agent created and built")

# Test conversation
print("\n2. Starting conversation...\n")

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

print("=" * 60)
print("Demo complete!")
print("=" * 60)

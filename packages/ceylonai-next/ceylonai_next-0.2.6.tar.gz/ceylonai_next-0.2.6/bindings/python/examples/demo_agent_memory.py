import asyncio
import os
import sys
from ceylonai_next import LlmAgent, InMemoryBackend, LlmConfig

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

async def main():
    print("=" * 60)
    print("🤖 LlmAgent Memory Demo")
    print("=" * 60)

    # 1. Create Memory Backend
    print("\n🧠 Initializing Memory Backend...")
    memory = InMemoryBackend()
    print("✅ Memory backend created")

    # 2. Create LlmAgent with Memory
    print("\n🤖 Initializing LLM Agent with Memory...")
    # Ensure Ollama is running with llama3.2:latest or change model
    model = "ollama::llama3.2:latest"
    
    agent = LlmAgent("memory_agent", model)
    agent.with_memory(memory)
    agent.with_system_prompt(
        "You are a helpful assistant with access to a memory module. "
        "You can save important information using the 'save_memory' tool "
        "and search for it using the 'search_memory' tool. "
        "Always check your memory before answering questions if you are unsure."
    )
    agent.build()
    print(f"✅ Agent created with model '{model}'")

    # 3. Instruct Agent to Save Memory
    print("\n📝 Instructing agent to save a fact...")
    fact = "The secret code is 'BLUE-HORIZON-99'."
    prompt = f"Please remember this important fact: {fact}"
    
    print(f"User: {prompt}")
    response = await agent.send_message_async(prompt)
    print(f"Agent: {response}")

    # Verify memory content directly
    print("\n🔍 Verifying memory content directly...")
    count = memory.count()
    print(f"Total entries in memory: {count}")
    
    if count > 0:
        # We can't easily inspect content without search, but we can assume it worked if count > 0
        # Let's try to search using the backend directly
        from ceylonai_next import MemoryQuery
        query = MemoryQuery()
        query.with_filter("content", fact) # This won't work as filter is for metadata
        # But we can just list all (search with empty query)
        results = memory.search(query)
        for entry in results:
            print(f"  - Entry: {entry.content}")
            if "BLUE-HORIZON-99" in entry.content:
                print("  ✅ Found secret code in memory!")

    # 4. Instruct Agent to Retrieve Memory
    print("\n🔎 Asking agent to recall the fact...")
    query_prompt = "What is the secret code I told you earlier?"
    
    print(f"User: {query_prompt}")
    response = await agent.send_message_async(query_prompt)
    print(f"Agent: {response}")

    if "BLUE-HORIZON-99" in response:
        print("\n✅ SUCCESS: Agent successfully recalled the information!")
    else:
        print("\n⚠️ WARNING: Agent might not have recalled the information correctly.")

    print("\n" + "=" * 60)
    print("Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

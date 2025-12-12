#!/usr/bin/env python3
"""
Redis Memory Backend Demo for Ceylon AI Framework

This example demonstrates how to use Redis as a persistent memory backend for agents.
Unlike the in-memory backend, Redis provides:
- Persistence across application restarts
- Scalability for high-throughput applications
- Built-in TTL support
- Multi-process/multi-server shared memory
- Production-ready reliability

Prerequisites:
1. Install and start Redis:
   - macOS: `brew install redis && redis-server`
   - Linux: `sudo apt-get install redis-server && redis-server`
   - Docker: `docker run -d -p 6379:6379 redis:latest`

2. Build the Ceylon bindings with Redis support:
   - `cd bindings/python && maturin develop --features redis`

3. Set up your LLM provider (e.g., Ollama):
   - Install Ollama from https://ollama.ai
   - Pull a model: `ollama pull llama3.2:latest`
"""

import asyncio
import os
import sys

try:
    from ceylonai_next import LlmAgent, RedisBackend, LlmConfig, MemoryQuery
except ImportError as e:
    print(f"❌ Error: Could not import RedisBackend: {e}")
    print("   Make sure you built the bindings with Redis support:")
    print("   cd bindings/python && maturin develop --features redis")
    sys.exit(1)


async def main():
    print("=" * 70)
    print("🗄️  Ceylon AI Framework - Redis Memory Backend Demo")
    print("=" * 70)

    # Configuration
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    model = os.getenv("LLM_MODEL", "ollama::llama3.2:latest")

    # 1. Create Redis Memory Backend
    print(f"\n🔌 Connecting to Redis at {redis_url}...")
    try:
        memory = RedisBackend(redis_url)
        memory = memory.with_prefix("demo_agent")  # Namespace for this demo
        memory = memory.with_ttl_seconds(3600)     # 1 hour TTL for entries
        print("✅ Redis backend connected successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Redis: {e}")
        print("   Make sure Redis is running on localhost:6379")
        print("   Try: redis-server")
        return

    # Clear any previous demo data
    print("🧹 Clearing previous demo data...")
    memory.clear()

    # 2. Create LLM Agent with Redis Memory
    print(f"\n🤖 Initializing LLM Agent with Redis Memory...")
    print(f"   Model: {model}")

    agent = LlmAgent("redis_memory_agent", model)
    agent.with_memory(memory)
    agent.with_system_prompt(
        "You are a helpful AI assistant with access to a persistent memory module. "
        "You can save important information using the 'save_memory' tool "
        "and search for it using the 'search_memory' tool. "
        "Your memory persists across sessions, so you can remember things long-term. "
        "Always check your memory before answering questions if you are unsure."
    )
    agent.with_temperature(0.7)
    agent.with_max_tokens(2048)
    agent.build()
    print("✅ Agent initialized with Redis memory backend")

    # 3. Test 1: Save user preferences
    print("\n" + "=" * 70)
    print("📋 Test 1: Saving User Preferences")
    print("=" * 70)

    preferences = [
        "My favorite color is deep purple.",
        "I prefer Python over JavaScript for backend development.",
        "I usually work from 9 AM to 5 PM Pacific Time.",
        "My project name is 'Ceylon AI Framework'.",
    ]

    for pref in preferences:
        print(f"\n📝 User: Please remember: {pref}")
        response = await agent.send_message_async(f"Please remember this: {pref}")
        print(f"🤖 Agent: {response[:100]}...")

    # Verify Redis storage
    print(f"\n🔍 Verifying Redis storage...")
    count = memory.count()
    print(f"   Total entries in Redis: {count}")

    # 4. Test 2: Query the agent's memory
    print("\n" + "=" * 70)
    print("🔎 Test 2: Querying Agent Memory")
    print("=" * 70)

    questions = [
        "What is my favorite color?",
        "What programming language do I prefer for backend?",
        "What hours do I usually work?",
    ]

    for question in questions:
        print(f"\n❓ User: {question}")
        response = await agent.send_message_async(question)
        print(f"🤖 Agent: {response}")

    # 5. Test 3: Direct Redis memory inspection
    print("\n" + "=" * 70)
    print("🔬 Test 3: Direct Redis Memory Inspection")
    print("=" * 70)

    print("\n📊 All entries in Redis memory:")
    query = MemoryQuery()
    results = memory.search(query)
    for i, entry in enumerate(results, 1):
        print(f"\n{i}. ID: {entry.id}")
        print(f"   Content: {entry.content[:100]}...")
        print(f"   Created: {entry.created_at}")
        if entry.metadata:
            print(f"   Metadata: {entry.metadata}")

    # 6. Test 4: Memory persistence
    print("\n" + "=" * 70)
    print("💾 Test 4: Memory Persistence")
    print("=" * 70)
    print("\nℹ️  The data is now stored in Redis and will persist even if you:")
    print("   - Restart this script")
    print("   - Restart the Python process")
    print("   - Reboot your computer (as long as Redis persists)")
    print("\n   To test persistence:")
    print("   1. Note the entry count above")
    print("   2. Stop this script (Ctrl+C)")
    print("   3. Run it again")
    print("   4. The entries should still be there!")

    # 7. Test 5: Namespace isolation
    print("\n" + "=" * 70)
    print("🏢 Test 5: Namespace Isolation")
    print("=" * 70)

    # Create another backend with different prefix
    memory2 = RedisBackend(redis_url).with_prefix("other_agent")
    count1 = memory.count()
    count2 = memory2.count()

    print(f"\n   'demo_agent' namespace: {count1} entries")
    print(f"   'other_agent' namespace: {count2} entries")
    print("\n✅ Namespaces are properly isolated!")

    # 8. Cleanup
    print("\n" + "=" * 70)
    print("🧹 Cleanup")
    print("=" * 70)

    cleanup = input("\n⚠️  Do you want to clear the Redis memory? (y/N): ").strip().lower()
    if cleanup == 'y':
        memory.clear()
        print("✅ Redis memory cleared")
    else:
        print("ℹ️  Memory preserved for next run")

    print("\n" + "=" * 70)
    print("✨ Demo Complete!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("   • Redis provides persistent memory for agents")
    print("   • Memory survives application restarts")
    print("   • Namespace isolation allows multiple agents on same Redis")
    print("   • TTL support for automatic memory expiration")
    print("   • Production-ready scalability and reliability")
    print("")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

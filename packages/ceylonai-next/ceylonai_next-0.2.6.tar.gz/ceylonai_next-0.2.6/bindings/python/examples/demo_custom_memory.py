"""
Custom Memory Backend Example

This example demonstrates how to create a custom memory backend by extending
the Memory abstract base class. This is useful for integr

ating external storage
systems like vector databases, cloud storage, or specialized data stores.
"""

import asyncio
from typing import List, Optional, Dict
from ceylonai_next import Memory, MemoryEntry, MemoryQuery, LlmAgent

class SimpleVectorMemory(Memory):
    """
    A simple custom memory implementation that demonstrates the Memory interface.
    
    In a real application, you might integrate a vector database like:
    - Qdrant
    - Pinecone
    - Weaviate 
    - Chroma
    - FAISS
    
    This example uses a simple dictionary for storage.
    """
    
    def __init__(self):
        self.storage: Dict[str, MemoryEntry] = {}
        print("📦 SimpleVectorMemory initialized")
    
    def store(self, entry: MemoryEntry) -> str:
        """Store a memory entry."""
        self.storage[entry.id] = entry
        print(f"  ✅ Stored entry {entry.id[:8]}... content: '{entry.content[:50]}...'")
        return entry.id
    
    def get(self, id: str) -> Optional[MemoryEntry]:
        """Retrieve a memory entry by ID."""
        return self.storage.get(id)
    
    def search(self, query: MemoryQuery) -> List[MemoryEntry]:
        """
        Search for entries matching the query.
        
        In a real vector database, this would perform semantic similarity search.
        """
        results = []
        
        for entry in self.storage.values():
            # Filter by metadata
            matches_filters = all(
               entry.metadata.get(k) == v 
                for k, v in query.filters.items()
            )
            
            if matches_filters:
                results.append(entry)
        
        # Sort by most recent
        results.sort(key=lambda e: e.created_at, reverse=True)
        
        # Apply limit
        if query.limit:
            results = results[:query.limit]
        
        return results
    
    def delete(self, id: str) -> bool:
        """Delete a memory entry."""
        if id in self.storage:
            del self.storage[id]
            return True
        return False
    
    def clear(self):
        """Clear all entries."""
        self.storage.clear()
        print("  🗑️  Memory cleared")
    
    def count(self) -> int:
        """Return number of entries."""
        return len(self.storage)


async def main():
    print("=" * 60)
    print("🧪 Custom Memory Backend Demo")
    print("=" * 60)
    
    # 1. Create custom memory backend
    print("\n🔧 Creating custom memory backend...")
    memory = SimpleVectorMemory()
    
    # 2. Test basic operations
    print("\n📝 Testing basic memory operations...")
    entry1 = MemoryEntry("The Eiffel Tower is in Paris, France.")
    entry2 = MemoryEntry("The Great Wall of China is in China.")
    entry3 = MemoryEntry("The Statue of Liberty is in New York, USA.")
    
    memory.store(entry1)
    memory.store(entry2)
    memory.store(entry3)
    
    print(f"\n📊 Total entries: {memory.count()}")
    
    # 3. Use with LlmAgent
    print("\n🤖 Integrating with LlmAgent...")
    agent = LlmAgent("geography_agent", "ollama::llama3.2:latest")
    agent.with_memory(memory)
    agent.with_system_prompt(
        "You are a helpful geography assistant. "
        "When asked about landmarks, use the 'search_memory' tool to find information. "
        "Always cite the information from your memory."
    )
    agent.build()
    print("✅ Agent built with custom memory backend")
    
    # 4. Ask the agent a question
    print("\n❓ Testing agent with custom memory...")
    question = "Where is the Eiffel Tower located?"
    print(f"User: {question}")
    
    response = await agent.send_message_async(question)
    print(f"Agent: {response}")
    
    # 5. Demonstrate memory persistence
    print("\n🔍 Verifying memory persistence...")
    print(f"Memory still has {memory.count()} entries after agent interaction")
    
    print("\n" + "=" * 60)
    print("🎉 Custom Memory Demo Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("  - Extend the Memory ABC to create custom backends")
    print("  - Integrate vector databases, cloud storage, etc.")
    print("  - LlmAgent automatically uses your custom memory with search/save tools")
    print("  - Your memory backend has full control over storage and retrieval")


if __name__ == "__main__":
    asyncio.run(main())

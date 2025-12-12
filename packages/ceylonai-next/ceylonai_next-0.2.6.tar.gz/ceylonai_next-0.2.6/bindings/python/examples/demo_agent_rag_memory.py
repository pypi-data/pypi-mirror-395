"""
RAG (Retrieval Augmented Generation) Example using LlmAgent Memory

This example demonstrates how to use the LlmAgent's built-in memory module
to implement a RAG pipeline.

Unlike `demo_rag_embeddings.py` which uses external vector storage and embeddings,
this example uses the agent's internal memory and keyword search capabilities.
While less semantic than vector search, it demonstrates the agent's ability to
autonomously query its memory to answer questions.

Pipeline:
1. Document loading and chunking
2. Storing chunks in LlmAgent's memory
3. Asking the agent questions
4. Agent autonomously calls `search_memory` tool
5. Agent synthesizes answer from retrieved memory
"""

import os
import sys
import asyncio
from typing import List

# Add parent directory to path for Ceylon imports
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ceylonai_next import LlmAgent, InMemoryBackend, MemoryEntry

# Sample content (same as demo_rag_embeddings.py)
EVERGLADES_CONTENT = """
The Indigenous people of the Everglades region arrived in the Florida peninsula approximately 15,000 years ago. Paleo-Indians came to Florida probably following large game that included giant sloths, saber-toothed cats, and spectacled bears. They found an arid landscape that supported plants and animals adapted for desert conditions. However, 6,500 years ago, climate changes brought a wetter landscape; large Paleo-Indian animals became extinct. They adapted to the changes by creating tools with the available resources.

The two major tribes in the area were the Calusa and the Tequesta. The Calusa lived on the southwest coast of Florida and controlled much of south Florida. The Calusa society was stratified, with commoners and nobles. The Calusa were known as the "Shell Indians" because they used shells for tools, utensils, jewelry, and to construct mounds and ridges.

The Tequesta lived on the southeastern coast of Florida. They were hunters and gatherers who relied on the sea, rivers, and the Everglades for food. They did not practice agriculture. They gathered roots and nuts, and hunted deer and small mammals.

After European contact in the 16th century, both tribes declined due to disease and conflict. By the 1800s, the Seminole and Miccosukee tribes, who had migrated into Florida from the north, established themselves in the Everglades, adapting to the wetland environment.
"""

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """Simple text chunking"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

async def main():
    print("=" * 60)
    print("🤖 LlmAgent Memory RAG Demo")
    print("=" * 60)

    # 1. Initialize Memory Backend
    print("\n🧠 Initializing Memory Backend...")
    memory = InMemoryBackend()
    
    # 2. Process and Store Documents
    print("\n📚 Processing documents...")
    chunks = chunk_text(EVERGLADES_CONTENT, chunk_size=50, overlap=10)
    print(f"Created {len(chunks)} chunks.")

    print("💾 Storing chunks in memory...")
    for i, chunk in enumerate(chunks):
        # We store the chunk content directly.
        # In a real app, we might add metadata like source, page, etc.
        entry = MemoryEntry(chunk)
        memory.store(entry)
    
    print(f"✅ Stored {len(chunks)} entries in memory.")

    # 3. Initialize Agent
    print("\n🤖 Initializing Agent...")
    # Ensure Ollama is running
    model = "ollama::llama3.2:latest"
    
    agent = LlmAgent("rag_agent", model)
    agent.with_memory(memory)
    agent.with_system_prompt(
        "You are a helpful AI assistant with access to a knowledge base about the Everglades. "
        "When asked a question, you MUST use the 'search_memory' tool to find relevant information "
        "before answering. "
        "To use the tool, you must provide a 'query' argument with the search terms. "
        "Example: search_memory(query='Calusa tribe') "
        "Do not answer from your own training data if the information is likely to be in your memory. "
        "If you find relevant information, summarize it to answer the user's question."
    )
    agent.build()
    print(f"✅ Agent created.")

    # 4. Ask Questions
    questions = [
        "Who were the 'Shell Indians' and why were they called that?",
        "What happened to the Paleo-Indian animals?",
        "Did the Tequesta practice agriculture?",
    ]

    for q in questions:
        print(f"\n❓ Question: {q}")
        print("-" * 30)
        
        # We use send_message_async which returns the final response
        # The agent should autonomously call search_memory during processing
        response = await agent.send_message_async(q)
        
        print(f"🤖 Agent: {response}")
        print("-" * 30)

    print("\n" + "=" * 60)
    print("Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

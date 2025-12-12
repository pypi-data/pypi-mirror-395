"""
RAG (Retrieval Augmented Generation) Example with Embeddings

This example demonstrates a complete RAG pipeline:
1. Document loading and chunking
2. Embedding generation using sentence-transformers
3. Vector storage and semantic similarity search
4. Integration with Ceylon's LLM agent for question answering

The example uses content about Indigenous people of the Everglades region
as the knowledge base.

Requirements:
    pip install sentence-transformers numpy
"""

import os
import sys
import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import asyncio

# Add parent directory to path for Ceylon imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ceylonai_next import Agent, LlmAgent, LocalMesh, LlmConfig


@dataclass
class DocumentChunk:
    """Represents a chunk of text with its embedding and metadata"""
    text: str
    embedding: np.ndarray
    chunk_id: int
    metadata: Dict[str, Any]


class SimpleVectorStore:
    """
    Simple in-memory vector store with cosine similarity search.

    This demonstrates the core RAG functionality. In production, you would
    use a dedicated vector database like Qdrant, Pinecone, or Weaviate.
    """

    def __init__(self):
        self.chunks: List[DocumentChunk] = []

    def add_chunk(self, chunk: DocumentChunk):
        """Add a document chunk to the store"""
        self.chunks.append(chunk)

    def similarity_search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        threshold: float = 0.0
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for the most similar chunks using cosine similarity.

        Args:
            query_embedding: The embedding vector of the query
            top_k: Number of top results to return
            threshold: Minimum similarity score (0-1)

        Returns:
            List of (chunk, similarity_score) tuples, sorted by similarity
        """
        if not self.chunks:
            return []

        # Calculate cosine similarity for all chunks
        similarities = []
        for chunk in self.chunks:
            # Cosine similarity = dot product of normalized vectors
            similarity = self._cosine_similarity(query_embedding, chunk.embedding)
            if similarity >= threshold:
                similarities.append((chunk, float(similarity)))

        # Sort by similarity (highest first) and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        # Normalize vectors
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-10)
        vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-10)
        # Return dot product
        return np.dot(vec1_norm, vec2_norm)


class RAGSystem:
    """
    Complete RAG system with document processing, embedding, and retrieval.
    """

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG system.

        Args:
            embedding_model_name: Name of the sentence-transformers model to use
        """
        print(f"🔧 Initializing RAG system...")
        print(f"📦 Loading embedding model: {embedding_model_name}")

        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer(embedding_model_name)
            print(f"✅ Embedding model loaded successfully")
        except ImportError:
            print("❌ Error: sentence-transformers not installed")
            print("   Please run: pip install sentence-transformers")
            raise
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise

        self.vector_store = SimpleVectorStore()
        self.chunk_size = 500  # Characters per chunk
        self.chunk_overlap = 50  # Overlap between chunks

    def load_and_process_document(self, file_path: str):
        """
        Load a document and process it into chunks with embeddings.

        Args:
            file_path: Path to the text document
        """
        print(f"\n📄 Loading document: {file_path}")

        # Read the document
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"📊 Document size: {len(text)} characters")

        # Split into chunks
        chunks = self._chunk_text(text)
        print(f"✂️  Created {len(chunks)} chunks")

        # Generate embeddings for all chunks
        print(f"🔮 Generating embeddings...")
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedding_model.encode(
            chunk_texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        # Store chunks with embeddings
        for i, (chunk_dict, embedding) in enumerate(zip(chunks, embeddings)):
            doc_chunk = DocumentChunk(
                text=chunk_dict['text'],
                embedding=embedding,
                chunk_id=i,
                metadata=chunk_dict['metadata']
            )
            self.vector_store.add_chunk(doc_chunk)

        print(f"✅ Processed and stored {len(chunks)} chunks with embeddings")
        print(f"📐 Embedding dimension: {embeddings[0].shape[0]}")

    def _chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: The text to chunk

        Returns:
            List of chunk dictionaries with text and metadata
        """
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""
        chunk_start_para = 0

        for i, para in enumerate(paragraphs):
            # If adding this paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append({
                    'text': current_chunk.strip(),
                    'metadata': {
                        'start_paragraph': chunk_start_para,
                        'end_paragraph': i - 1
                    }
                })

                # Start new chunk with overlap (last 50 chars)
                if len(current_chunk) > self.chunk_overlap:
                    current_chunk = current_chunk[-self.chunk_overlap:] + "\n\n"
                else:
                    current_chunk = ""

                chunk_start_para = i

            current_chunk += para + "\n\n"

        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'metadata': {
                    'start_paragraph': chunk_start_para,
                    'end_paragraph': len(paragraphs) - 1
                }
            })

        return chunks

    def search(self, query: str, top_k: int = 3) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for relevant chunks using semantic similarity.

        Args:
            query: The search query
            top_k: Number of results to return

        Returns:
            List of (chunk, similarity_score) tuples
        """
        print(f"\n🔍 Searching for: '{query}'")

        # Generate embedding for the query
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        )

        # Search in vector store
        results = self.vector_store.similarity_search(
            query_embedding,
            top_k=top_k,
            threshold=0.0
        )

        print(f"📋 Found {len(results)} relevant chunks")
        return results

    def format_context(self, results: List[Tuple[DocumentChunk, float]]) -> str:
        """
        Format search results into a context string for the LLM.

        Args:
            results: List of (chunk, similarity_score) tuples

        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found."

        context_parts = []
        for i, (chunk, score) in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}] (Relevance: {score:.3f})\n{chunk.text}"
            )

        return "\n\n---\n\n".join(context_parts)


async def rag_query(
    rag_system: RAGSystem,
    llm_agent: LlmAgent,
    question: str,
    top_k: int = 3
) -> str:
    """
    Perform a complete RAG query: retrieve relevant context and generate answer.

    Args:
        rag_system: The RAG system instance
        llm_agent: The LLM agent for generating answers
        question: The user's question
        top_k: Number of relevant chunks to retrieve

    Returns:
        The LLM's answer based on retrieved context
    """
    # Step 1: Retrieve relevant context
    results = rag_system.search(question, top_k=top_k)

    # Display retrieved chunks
    print("\n📚 Retrieved Context:")
    for i, (chunk, score) in enumerate(results, 1):
        print(f"\n  [{i}] Similarity: {score:.3f}")
        preview = chunk.text[:150].replace('\n', ' ')
        print(f"      {preview}...")

    # Step 2: Format context for the LLM
    context = rag_system.format_context(results)

    # Step 3: Create prompt with context and question
    prompt = f"""You are a knowledgeable assistant answering questions about Indigenous people of the Everglades region.

Use the following context to answer the question. If the answer cannot be found in the context, say so.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 4: Generate answer using LLM
    print(f"\n🤖 Generating answer with LLM...")
    response = await llm_agent.query_async(prompt)

    return response


async def main():
    """Main function demonstrating the RAG pipeline"""

    print("=" * 70)
    print("🌴 RAG Example: Indigenous People of the Everglades")
    print("=" * 70)

    # Initialize RAG system
    rag = RAGSystem(embedding_model_name="all-MiniLM-L6-v2")

    # Load and process the document
    doc_path = os.path.join(os.path.dirname(__file__), "everglades_content.txt")
    rag.load_and_process_document(doc_path)

    # Initialize Ceylon LLM Agent with Ollama
    print(f"\n🤖 Initializing LLM Agent...")
    print(f"   Using Ollama with model: llama3.2:latest")
    print(f"   Make sure Ollama is running: ollama serve")

    mesh = LocalMesh("rag_mesh")

    llm_config = (
        LlmConfig.builder()
        .provider("ollama")
        .model("llama3.2:latest")
        .base_url("http://localhost:11434")
        .temperature(0.7)
        .max_tokens(500)
        .build()
    )

    llm_agent = LlmAgent(mesh, "llm_assistant", llm_config)
    print(f"✅ LLM Agent ready")

    # Example questions to ask
    questions = [
        "Who were the Calusa people and what were they known for?",
        "How did the Seminole people adapt to the Everglades environment?",
        "What impact did European contact have on indigenous peoples?",
        "What are modern indigenous communities doing to preserve their culture?",
    ]

    print("\n" + "=" * 70)
    print("💬 Asking Questions with RAG")
    print("=" * 70)

    for i, question in enumerate(questions, 1):
        print(f"\n{'━' * 70}")
        print(f"❓ Question {i}: {question}")
        print(f"{'━' * 70}")

        # Perform RAG query
        answer = await rag_query(rag, llm_agent, question, top_k=3)

        print(f"\n💡 Answer:")
        print(f"{answer}")

        if i < len(questions):
            print(f"\n⏳ Waiting before next question...")
            await asyncio.sleep(2)

    print("\n" + "=" * 70)
    print("✅ RAG Demo Complete!")
    print("=" * 70)

    # Interactive mode
    print("\n💬 Interactive Mode - Ask your own questions!")
    print("   (Type 'quit' or 'exit' to end)")

    while True:
        try:
            user_question = input("\n❓ Your question: ").strip()

            if user_question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not user_question:
                continue

            print()
            answer = await rag_query(rag, llm_agent, user_question, top_k=3)
            print(f"\n💡 Answer:")
            print(f"{answer}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Check dependencies
    try:
        import sentence_transformers
        import numpy
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print(f"\n📦 Please install required packages:")
        print(f"   pip install sentence-transformers numpy")
        sys.exit(1)

    # Run the async main function
    asyncio.run(main())

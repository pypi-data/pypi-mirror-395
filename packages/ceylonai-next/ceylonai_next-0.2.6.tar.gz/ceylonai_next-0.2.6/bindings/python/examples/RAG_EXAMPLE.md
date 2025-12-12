# RAG (Retrieval Augmented Generation) Example

This example demonstrates a complete RAG pipeline using Ceylon's LLM agent with embedding-based semantic search.

## Overview

The RAG system consists of:

1. **Document Processing**: Load and chunk text documents into manageable pieces
2. **Embedding Generation**: Convert text chunks into vector embeddings using sentence-transformers
3. **Vector Storage**: Store embeddings in a simple in-memory vector database
4. **Semantic Search**: Find relevant chunks using cosine similarity
5. **Answer Generation**: Use Ceylon's LLM agent to generate answers based on retrieved context

## Architecture

```
┌─────────────────┐
│   Document      │
│  (everglades_   │
│   content.txt)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Text Chunking   │
│  (500 chars,    │
│   50 overlap)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Embedding     │
│   Generation    │
│ (all-MiniLM-    │
│    L6-v2)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Store    │
│  (Cosine        │
│  Similarity)    │
└────────┬────────┘
         │
         ▼
    User Query
         │
         ▼
┌─────────────────┐
│  Embed Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Similarity      │
│ Search (top-k)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieve        │
│ Top Chunks      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Format Context  │
│ + Question      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Ceylon LLM     │
│  Agent Query    │
│ (Ollama/Llama)  │
└────────┬────────┘
         │
         ▼
     Answer
```

## Prerequisites

### 1. Install Python Dependencies

```bash
pip install sentence-transformers numpy
```

### 2. Install and Run Ollama

Download and install Ollama from https://ollama.ai/

Start Ollama:
```bash
ollama serve
```

Pull the Llama model:
```bash
ollama pull llama3.2:latest
```

### 3. Install Ceylon Python Bindings

From the `bindings/python` directory:
```bash
pip install -e .
```

## Files

- `demo_rag_embeddings.py` - Main RAG implementation with examples
- `everglades_content.txt` - Knowledge base document about Indigenous Everglades peoples
- `RAG_EXAMPLE.md` - This documentation file

## Running the Example

```bash
cd bindings/python/examples
python demo_rag_embeddings.py
```

## What the Example Does

### 1. Initialization Phase
- Loads the `all-MiniLM-L6-v2` embedding model (384-dimensional vectors)
- Creates a simple in-memory vector store

### 2. Document Processing Phase
- Reads `everglades_content.txt` (about 6,000 characters)
- Splits into ~12 chunks with 500 character size and 50 character overlap
- Generates embeddings for all chunks
- Stores chunks with their embeddings

### 3. Query Phase
Demonstrates 4 example questions:
1. "Who were the Calusa people and what were they known for?"
2. "How did the Seminole people adapt to the Everglades environment?"
3. "What impact did European contact have on indigenous peoples?"
4. "What are modern indigenous communities doing to preserve their culture?"

For each question:
- Embeds the question text
- Finds top 3 most similar chunks using cosine similarity
- Displays similarity scores and chunk previews
- Constructs a prompt with retrieved context
- Sends to Ceylon LLM agent (Ollama + Llama 3.2)
- Displays the generated answer

### 4. Interactive Mode
After the examples, you can ask your own questions interactively.

## Key Components

### SimpleVectorStore Class

A lightweight in-memory vector database implementation:

```python
class SimpleVectorStore:
    def add_chunk(self, chunk: DocumentChunk)
    def similarity_search(self, query_embedding, top_k=3, threshold=0.0)
```

Uses cosine similarity for vector comparison:
```
similarity = dot(normalize(vec1), normalize(vec2))
```

### RAGSystem Class

Main orchestrator for the RAG pipeline:

```python
class RAGSystem:
    def __init__(self, embedding_model_name)
    def load_and_process_document(self, file_path)
    def search(self, query, top_k=3)
    def format_context(self, results)
```

Features:
- Configurable chunk size and overlap
- Automatic paragraph-aware chunking
- Batch embedding generation with progress bar
- Metadata tracking per chunk

### RAG Query Function

```python
async def rag_query(rag_system, llm_agent, question, top_k=3):
    # 1. Retrieve relevant chunks
    results = rag_system.search(question, top_k)

    # 2. Format context
    context = rag_system.format_context(results)

    # 3. Build prompt with context + question
    prompt = f"Context: {context}\n\nQuestion: {question}"

    # 4. Query LLM
    answer = await llm_agent.query_async(prompt)

    return answer
```

## Example Output

```
🔧 Initializing RAG system...
📦 Loading embedding model: all-MiniLM-L6-v2
✅ Embedding model loaded successfully

📄 Loading document: everglades_content.txt
📊 Document size: 6247 characters
✂️  Created 12 chunks
🔮 Generating embeddings...
Batches: 100%|████████████| 1/1 [00:00<00:00, 12.34it/s]
✅ Processed and stored 12 chunks with embeddings
📐 Embedding dimension: 384

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ Question 1: Who were the Calusa people and what were they known for?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Searching for: 'Who were the Calusa people and what were they known for?'
📋 Found 3 relevant chunks

📚 Retrieved Context:

  [1] Similarity: 0.745
      The Calusa People The Calusa were one of the most powerful indigenous groups in southern Florida...

  [2] Similarity: 0.623
      The Tequesta inhabited the southeastern coast of Florida, including the area that is now Miami...

  [3] Similarity: 0.587
      The Seminole and Miccosukee The Seminole and Miccosukee peoples are more recent arrivals...

🤖 Generating answer with LLM...

💡 Answer:
Based on the context provided, the Calusa people were one of the most powerful
indigenous groups in southern Florida. They were known for being fierce warriors
and skilled navigators who inhabited the coastal areas and Ten Thousand Islands
region of the Everglades. Unlike many other tribes, the Calusa did not practice
agriculture but relied entirely on fishing, hunting, and gathering. They were
expert fishermen using sophisticated techniques including nets, weirs, and spears,
and they created extensive canal systems and impressive shell mounds.
```

## Customization

### Use Different Embedding Models

Change the model in `RAGSystem` initialization:

```python
# Smaller, faster model (default)
rag = RAGSystem(embedding_model_name="all-MiniLM-L6-v2")

# Larger, more accurate model
rag = RAGSystem(embedding_model_name="all-mpnet-base-v2")

# Multilingual model
rag = RAGSystem(embedding_model_name="paraphrase-multilingual-MiniLM-L12-v2")
```

See https://www.sbert.net/docs/pretrained_models.html for more options.

### Use Different LLM Models

Modify the `LlmConfig`:

```python
# Use different Ollama model
llm_config = (
    LlmConfig.builder()
    .provider("ollama")
    .model("mistral:latest")  # or "codellama:latest", "phi3:latest", etc.
    .base_url("http://localhost:11434")
    .temperature(0.7)
    .max_tokens(500)
    .build()
)

# Use OpenAI instead
llm_config = (
    LlmConfig.builder()
    .provider("openai")
    .model("gpt-4")
    .api_key("your-api-key")
    .temperature(0.7)
    .max_tokens(500)
    .build()
)
```

### Adjust Chunk Parameters

Modify chunk size and overlap:

```python
rag = RAGSystem()
rag.chunk_size = 300  # Smaller chunks
rag.chunk_overlap = 100  # More overlap
```

### Change Retrieval Parameters

Adjust number of chunks retrieved:

```python
# Retrieve more context (top 5 instead of top 3)
answer = await rag_query(rag, llm_agent, question, top_k=5)

# Or modify the search directly
results = rag.search(query, top_k=5)

# Add similarity threshold
results = rag.vector_store.similarity_search(
    query_embedding,
    top_k=3,
    threshold=0.5  # Only return chunks with similarity >= 0.5
)
```

## Integration with Ceylon Memory System

This example uses a simple in-memory vector store for demonstration. To integrate with Ceylon's memory system:

```python
from ceylon import Memory, MemoryEntry

# Store chunks in Ceylon memory with embeddings
memory = Memory(backend="in_memory")

for chunk in chunks:
    entry = MemoryEntry(
        content=chunk.text,
        metadata=chunk.metadata,
        embedding=chunk.embedding.tolist()  # Convert numpy array to list
    )
    await memory.store(entry)

# Query using semantic search (when VectorMemory trait is implemented)
results = await memory.similarity_search(
    query="Who were the Calusa people?",
    limit=3,
    threshold=0.5
)
```

## Production Considerations

For production RAG systems, consider:

1. **Vector Databases**: Use dedicated vector databases like:
   - Qdrant (fast, open-source, Rust-based)
   - Pinecone (managed service)
   - Weaviate (GraphQL-based)
   - Milvus (distributed)

2. **Embedding Models**:
   - Use API-based embeddings (OpenAI, Cohere) for better quality
   - Cache embeddings to avoid recomputation
   - Consider domain-specific fine-tuned models

3. **Chunking Strategies**:
   - Semantic chunking (split by meaning, not just size)
   - Hierarchical chunking (summaries + details)
   - Sliding window with larger overlap

4. **Retrieval Improvements**:
   - Hybrid search (keyword + semantic)
   - Reranking with cross-encoders
   - Query expansion and reformulation
   - Metadata filtering

5. **Performance**:
   - Batch processing for embedding generation
   - Asynchronous operations throughout
   - Connection pooling for databases
   - Caching frequently accessed chunks

## Troubleshooting

### Ollama Connection Error

```
Error: Connection refused to localhost:11434
```

**Solution**: Make sure Ollama is running:
```bash
ollama serve
```

### Missing Dependencies

```
ImportError: No module named 'sentence_transformers'
```

**Solution**: Install required packages:
```bash
pip install sentence-transformers numpy
```

### Model Download Issues

If the embedding model fails to download, manually download it:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
```

The model will be cached in `~/.cache/torch/sentence_transformers/`

## Learn More

- Ceylon Documentation: `../docs/`
- Sentence Transformers: https://www.sbert.net/
- Ollama: https://ollama.ai/
- RAG Tutorial: https://www.pinecone.io/learn/retrieval-augmented-generation/

## License

This example is part of the Ceylon project and follows the same license.

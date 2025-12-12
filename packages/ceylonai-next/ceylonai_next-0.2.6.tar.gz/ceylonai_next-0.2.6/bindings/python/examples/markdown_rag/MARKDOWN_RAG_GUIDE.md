# Advanced Markdown RAG System - Complete Guide

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Components](#components)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

## Overview

The Advanced Markdown RAG (Retrieval-Augmented Generation) System is a comprehensive solution for building intelligent Q&A systems from markdown documentation. It combines:

- **Intelligent Markdown Parsing**: Structure-aware parsing that preserves headings, code blocks, and document hierarchy
- **Semantic Search**: Vector embeddings with cosine similarity for finding relevant information
- **LLM Integration**: Powered by Claude (Anthropic) or other LLM providers via the Ceylon agent framework
- **Automatic Q&A Generation**: Creates well-formatted markdown Q&A files with citations
- **File Watching**: Automatically detects and processes changes to your knowledge base
- **Async Support**: Concurrent question answering for high throughput

## Features

### 🎯 Core Features

- ✅ **Section-Based Chunking**: Intelligently chunks markdown by headings and sections
- ✅ **Metadata Extraction**: Captures file paths, heading hierarchy, section numbers, code blocks, and links
- ✅ **Vector Embeddings**: Uses sentence-transformers for semantic search
- ✅ **Smart Search**: Configurable similarity thresholds and top-k retrieval
- ✅ **Auto-Indexing**: File watcher with debounced re-indexing
- ✅ **Q&A Generation**: LLM-powered answers with proper citations
- ✅ **Markdown Output**: Generates structured Q&A markdown files
- ✅ **Async Operations**: Concurrent question answering with asyncio
- ✅ **Update Detection**: Automatically detects new, modified, and deleted files
- ✅ **Multi-Provider Support**: Works with Claude, OpenAI, Ollama, and 10+ other LLM providers

### 📊 Advanced Capabilities

- Hierarchical heading path tracking (e.g., "Introduction > Getting Started > Installation")
- Code block extraction with language detection
- Link extraction and tracking
- File hash-based change detection
- Configurable chunk sizes and overlap
- Debounced file watching to prevent excessive re-indexing
- Batch processing with async support
- Q&A history export

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Markdown Files (.md)                        │
│                   (Your Knowledge Base)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MarkdownParser                                │
│  • Extracts headings, code blocks, links                        │
│  • Calculates file hashes for change detection                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MarkdownChunker                               │
│  • Section-based chunking (by headings)                         │
│  • Preserves heading hierarchy                                  │
│  • Splits large sections with overlap                           │
│  • Generates section numbers (1.2.3, etc.)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VectorKnowledgeBase                            │
│  • Generates embeddings (sentence-transformers)                 │
│  • Stores chunks with metadata                                  │
│  • Semantic search with cosine similarity                       │
│  • Update detection and re-indexing                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MarkdownRAGAgent                               │
│  • Retrieves relevant chunks                                    │
│  • Formats context for LLM                                      │
│  • Generates answers with LLM (Ceylon/Claude)                   │
│  • Creates markdown Q&A files                                   │
│  • Manages Q&A history                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Markdown Q&A Files                              │
│  • Structured question/answer format                            │
│  • Source citations with relevance scores                       │
│  • Timestamped and organized                                    │
└─────────────────────────────────────────────────────────────────┘

              ┌─────────────────────────────────┐
              │   KnowledgeBaseWatcher          │
              │  (Optional File Monitoring)     │
              │  • Detects file changes         │
              │  • Triggers re-indexing         │
              │  • Debounced updates            │
              └─────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Install Dependencies

```bash
cd /path/to/next-processor/bindings/python/examples
pip install -r requirements-markdown-rag.txt
```

### Step 2: Install Ceylon Agent Framework

```bash
# From the Python bindings directory
cd /path/to/next-processor/bindings/python
pip install -e .
```

### Step 3: Set Up API Keys

For **Claude (Anthropic)**:
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

For **OpenAI**:
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

For **Ollama** (local models):
```bash
# No API key needed - just ensure Ollama is running
# Default: http://localhost:11434
```

### Step 4: Verify Installation

```python
from markdown_kb_manager import MarkdownKnowledgeBase
from rag_markdown_agent import MarkdownRAGAgent

print("✓ Installation successful!")
```

## Quick Start

### 1. Basic Usage

```python
from markdown_kb_manager import MarkdownKnowledgeBase

# Initialize knowledge base
kb = MarkdownKnowledgeBase(
    kb_dir="./my_markdown_docs",
    model_name='all-MiniLM-L6-v2'
)

# Index all markdown files
kb.index_all_files()

# Search the knowledge base
results = kb.search("How do I install?", top_k=5)

for chunk, score in results:
    print(f"[{score:.2f}] {chunk.heading_path} - {chunk.content[:100]}...")
```

### 2. Q&A Generation

```python
import os
from ceylon import LlmConfig
from rag_markdown_agent import MarkdownRAGAgent

# Create LLM config
llm_config = LlmConfig.anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    model="claude-3-5-sonnet-20241022"
)

# Create RAG agent
agent = MarkdownRAGAgent(
    knowledge_base=kb,
    llm_config=llm_config,
    output_dir="./qa_output"
)

# Ask a question
result = agent.answer_question(
    question="What are the main features?",
    save_to_file=True
)

print(result['answer'])
# Q&A saved to: ./qa_output/qa_20250122_143045_what_are_the_main_features.md
```

### 3. Automatic File Watching

```python
from kb_file_watcher import watch_knowledge_base

# Watch knowledge base directory for changes
watch_knowledge_base(
    kb_dir="./my_markdown_docs",
    debounce_seconds=2.0
)
# Now any file changes will trigger automatic re-indexing!
```

### 4. Run Complete Demo

```bash
# Run the complete demonstration
python demo_markdown_rag_system.py

# Or with your own knowledge base
python demo_markdown_rag_system.py /path/to/your/markdown/files
```

## Usage Examples

### Example 1: Custom Chunk Configuration

```python
from markdown_kb_manager import MarkdownKnowledgeBase

kb = MarkdownKnowledgeBase(
    kb_dir="./docs",
    model_name='all-mpnet-base-v2',  # More accurate model
    chunk_config={
        'min_chunk_size': 300,       # Larger minimum chunk
        'max_chunk_size': 2000,      # Larger maximum chunk
        'chunk_overlap': 200         # More overlap for context
    }
)
```

### Example 2: Using Different LLM Providers

```python
from ceylon import LlmConfig

# OpenAI GPT-4
llm_config = LlmConfig.openai(
    api_key=os.getenv('OPENAI_API_KEY'),
    model="gpt-4-turbo-preview"
)

# Ollama (local)
llm_config = LlmConfig.ollama(
    base_url="http://localhost:11434",
    model="llama2"
)

# Google Gemini
llm_config = LlmConfig.google(
    api_key=os.getenv('GOOGLE_API_KEY'),
    model="gemini-pro"
)

# Then use with RAG agent
agent = MarkdownRAGAgent(kb, llm_config=llm_config)
```

### Example 3: Async Batch Processing

```python
import asyncio
from rag_markdown_agent import MarkdownRAGAgent

async def process_questions():
    questions = [
        "What is the installation process?",
        "What are the system requirements?",
        "How do I troubleshoot errors?",
        "What are the best practices?",
        "How do I contribute?"
    ]

    results = await agent.answer_multiple_questions_async(
        questions=questions,
        save_to_file=True
    )

    print(f"Processed {len(results)} questions!")
    return results

# Run async processing
results = asyncio.run(process_questions())
```

### Example 4: Filtered Search

```python
# Search only in a specific file
results = kb.search(
    query="installation steps",
    top_k=3,
    filter_file="./docs/installation.md"
)
```

### Example 5: Custom Update Callback

```python
from kb_file_watcher import KnowledgeBaseWatcher

def on_update(stats):
    """Custom callback when knowledge base is updated."""
    print(f"📊 Knowledge base updated!")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total chunks: {stats['total_chunks']}")

    # You could trigger additional actions here:
    # - Send notification
    # - Update dashboard
    # - Re-run queries
    # - etc.

watcher = KnowledgeBaseWatcher(
    knowledge_base=kb,
    debounce_seconds=3.0,
    on_update_callback=on_update
)

watcher.start(recursive=True)
```

### Example 6: Export Q&A History

```python
# After answering several questions
agent.export_qa_history("./qa_output/complete_history.md")

# This creates a single markdown file with all Q&As
```

## Components

### 1. MarkdownParser

Parses markdown files and extracts structure.

**Key Methods:**
- `parse_file(file_path)` - Parse file and return content with hash
- `extract_headings(content)` - Extract all headings with positions
- `extract_code_blocks(content)` - Extract code blocks with language
- `extract_links(content)` - Extract all markdown links

### 2. MarkdownChunker

Intelligently chunks markdown content by sections.

**Configuration:**
- `min_chunk_size` - Minimum characters per chunk (default: 200)
- `max_chunk_size` - Maximum characters per chunk (default: 1500)
- `chunk_overlap` - Overlap between chunks (default: 100)

**Key Methods:**
- `chunk_by_sections(file_path, content, file_hash)` - Main chunking method

### 3. VectorKnowledgeBase

Vector-based storage and semantic search.

**Features:**
- Sentence-transformers for embeddings
- Cosine similarity search
- File hash-based change detection
- Efficient numpy-based storage

**Key Methods:**
- `add_chunks(chunks)` - Add chunks and generate embeddings
- `remove_file_chunks(file_path)` - Remove all chunks from a file
- `search(query, top_k, filter_file)` - Semantic search
- `get_stats()` - Get knowledge base statistics

### 4. MarkdownKnowledgeBase

High-level manager for markdown knowledge base.

**Key Methods:**
- `index_all_files()` - Index all markdown files in directory
- `index_file(file_path)` - Index a single file
- `check_for_updates()` - Detect and process file changes
- `search(query, top_k, filter_file)` - Search the knowledge base

### 5. MarkdownRAGAgent

LLM-powered Q&A agent.

**Features:**
- Context retrieval from knowledge base
- LLM answer generation with citations
- Markdown Q&A file creation
- Q&A history tracking
- Async support

**Key Methods:**
- `answer_question(question, filter_file, save_to_file, file_name)` - Sync Q&A
- `answer_question_async(...)` - Async Q&A
- `answer_multiple_questions_async(questions, save_to_file)` - Batch processing
- `export_qa_history(file_path)` - Export all Q&As

### 6. KnowledgeBaseWatcher

Automatic file monitoring and re-indexing.

**Features:**
- Watchdog-based file monitoring
- Debounced updates
- Recursive directory watching
- Custom update callbacks

**Key Methods:**
- `start(recursive)` - Start watching
- `stop()` - Stop watching
- `watch_forever(recursive)` - Block and watch until interrupted

## Configuration

### Embedding Models

Choose based on your needs:

| Model | Speed | Accuracy | Dimension | Best For |
|-------|-------|----------|-----------|----------|
| `all-MiniLM-L6-v2` | ⚡⚡⚡ | ⭐⭐ | 384 | Quick prototyping, fast search |
| `all-mpnet-base-v2` | ⚡⚡ | ⭐⭐⭐ | 768 | Production, high accuracy |
| `multi-qa-mpnet-base-dot-v1` | ⚡⚡ | ⭐⭐⭐ | 768 | Q&A specific tasks |

### Chunk Configuration

```python
chunk_config = {
    'min_chunk_size': 200,   # Minimum size before forced chunking
    'max_chunk_size': 1500,  # Maximum size before splitting
    'chunk_overlap': 100     # Overlap for context preservation
}
```

**Recommendations:**
- **Small docs** (<10 pages): min=100, max=1000, overlap=50
- **Medium docs** (10-100 pages): min=200, max=1500, overlap=100
- **Large docs** (>100 pages): min=300, max=2000, overlap=150

### Similarity Thresholds

```python
kb = VectorKnowledgeBase(
    model_name='all-MiniLM-L6-v2',
    similarity_threshold=0.3  # Adjust based on precision/recall needs
)
```

**Guidelines:**
- `0.2-0.3` - High recall (more results, some less relevant)
- `0.3-0.5` - Balanced (default)
- `0.5+` - High precision (fewer, highly relevant results)

## Best Practices

### 1. Knowledge Base Organization

✅ **DO:**
- Use clear, hierarchical heading structure
- Include code examples in fenced code blocks with language tags
- Use descriptive file and section names
- Keep related content in the same file/section

❌ **DON'T:**
- Use flat structure without headings
- Mix unrelated topics in the same section
- Use generic headings like "Information" or "Details"

### 2. Performance Optimization

- **For large knowledge bases**: Consider using batch indexing
- **For frequent updates**: Use appropriate debounce time (2-5 seconds)
- **For fast search**: Use `all-MiniLM-L6-v2` model
- **For accuracy**: Use `all-mpnet-base-v2` model

### 3. Q&A Generation

```python
# Use specific questions for better results
❌ "Tell me about this"
✅ "What are the installation steps for the system?"

# Leverage filtering for large knowledge bases
results = agent.answer_question(
    "How do I configure?",
    filter_file="./docs/configuration.md"  # Narrow scope
)
```

### 4. Error Handling

```python
try:
    kb = MarkdownKnowledgeBase(kb_dir="./docs")
    kb.index_all_files()
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Indexing error: {e}")
```

## Troubleshooting

### Issue: Slow Indexing

**Symptoms:** Taking too long to index files

**Solutions:**
1. Use faster embedding model: `all-MiniLM-L6-v2`
2. Reduce chunk overlap
3. Increase `max_chunk_size` to create fewer chunks
4. Use GPU if available (automatic with sentence-transformers)

### Issue: No Search Results

**Symptoms:** Search returns empty results

**Solutions:**
1. Lower similarity threshold: `similarity_threshold=0.2`
2. Increase `top_k` parameter
3. Try different phrasings of your query
4. Check if files were actually indexed: `kb.get_stats()`

### Issue: Memory Errors

**Symptoms:** Out of memory errors with large knowledge bases

**Solutions:**
1. Process files in batches
2. Use smaller embedding model
3. Increase system RAM or use external vector database
4. Reduce `max_chunk_size` to create smaller chunks

### Issue: File Watcher Not Detecting Changes

**Symptoms:** Modified files not triggering re-index

**Solutions:**
1. Check file permissions
2. Ensure files are `.md` extension
3. Wait for debounce period to complete
4. Verify watcher is actually running: `watcher.is_watching()`

### Issue: LLM Errors

**Symptoms:** Errors when generating answers

**Solutions:**
1. Verify API key is set: `echo $ANTHROPIC_API_KEY`
2. Check API rate limits
3. Try with simpler questions first
4. Use alternative LLM provider

## API Reference

### MarkdownKnowledgeBase

```python
MarkdownKnowledgeBase(
    kb_dir: str,
    model_name: str = 'all-MiniLM-L6-v2',
    chunk_config: Optional[Dict] = None
)
```

**Methods:**
- `index_all_files() -> None`
- `index_file(file_path: str) -> None`
- `check_for_updates() -> Set[str]`
- `search(query: str, top_k: int = 5, filter_file: Optional[str] = None) -> List[Tuple[MarkdownChunk, float]]`
- `get_stats() -> Dict`

### MarkdownRAGAgent

```python
MarkdownRAGAgent(
    knowledge_base: MarkdownKnowledgeBase,
    llm_config: Optional[LlmConfig] = None,
    output_dir: str = "./qa_output",
    top_k_results: int = 5,
    include_code_blocks: bool = True
)
```

**Methods:**
- `answer_question(question: str, filter_file: Optional[str] = None, save_to_file: bool = True, file_name: Optional[str] = None) -> Dict`
- `answer_question_async(...) -> Dict`
- `answer_multiple_questions_async(questions: List[str], save_to_file: bool = True) -> List[Dict]`
- `export_qa_history(file_path: str) -> None`

### KnowledgeBaseWatcher

```python
KnowledgeBaseWatcher(
    knowledge_base: MarkdownKnowledgeBase,
    debounce_seconds: float = 2.0,
    on_update_callback: Optional[Callable] = None
)
```

**Methods:**
- `start(recursive: bool = True) -> None`
- `stop() -> None`
- `watch_forever(recursive: bool = True) -> None`
- `is_watching() -> bool`

---

## Examples in This Directory

| File | Description |
|------|-------------|
| `markdown_kb_manager.py` | Core knowledge base management with parsing, chunking, and vector search |
| `rag_markdown_agent.py` | RAG agent for Q&A generation with LLM integration |
| `kb_file_watcher.py` | Automatic file watching and re-indexing |
| `demo_markdown_rag_system.py` | Complete demonstration of all features |
| `requirements-markdown-rag.txt` | Dependencies list |
| `MARKDOWN_RAG_GUIDE.md` | This guide |

## License

This is part of the Ceylon Agent Framework project. See the main repository for license information.

## Support

For issues, questions, or contributions, please refer to the main project repository.

---

**Happy Building! 🚀**

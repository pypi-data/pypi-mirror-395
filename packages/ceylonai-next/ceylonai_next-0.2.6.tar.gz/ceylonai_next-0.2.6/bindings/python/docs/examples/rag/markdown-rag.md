# Markdown RAG System

Build intelligent Q&A systems from markdown documentation using Retrieval-Augmented Generation (RAG).

## Overview

The Markdown RAG system combines semantic search with LLM capabilities to create a knowledge-aware Q&A system that:

- **Indexes** markdown files with intelligent chunking
- **Searches** using vector embeddings for semantic understanding
- **Generates** contextual answers with LLM integration
- **Tracks** sources with proper citations
- **Auto-updates** when documentation changes

## Quick Start

### Installation

```bash
cd bindings/python/examples/markdown_rag
pip install -r requirements-markdown-rag.txt

# Set up API key
export ANTHROPIC_API_KEY="your-api-key"
```

### Basic Usage

```python
from markdown_kb_manager import MarkdownKnowledgeBase
from rag_markdown_agent import MarkdownRAGAgent
from ceylonai_next import LlmConfig
import os

# 1. Create knowledge base
kb = MarkdownKnowledgeBase(
    kb_dir="./your_docs",
    model_name='all-MiniLM-L6-v2'
)

# 2. Index markdown files
kb.index_all_files()

# 3. Create RAG agent
llm_config = LlmConfig.anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    model="claude-3-5-sonnet-20241022"
)

agent = MarkdownRAGAgent(
    knowledge_base=kb,
    llm_config=llm_config,
    output_dir="./qa_output"
)

# 4. Ask questions
result = agent.answer_question(
    question="How do I install the system?",
    save_to_file=True
)

print(result['answer'])
```

### Run the Demo

```bash
# With auto-generated sample knowledge base
python demo_markdown_rag_system.py

# With your own markdown files
python demo_markdown_rag_system.py /path/to/your/docs
```

## Key Features

### Semantic Search

Unlike keyword search, semantic search understands **meaning**:

```python
# Search by meaning, not exact words
results = kb.search("How to set up?", top_k=5)

# Matches: "installation", "setup", "configuration"
# Even though they don't contain "set up"
```

### Intelligent Chunking

Automatically splits documents while preserving context:

- Respects markdown structure (headings, sections)
- Configurable chunk sizes (200-1500 chars by default)
- Overlapping chunks for context preservation
- Maintains heading hierarchy

```python
kb = MarkdownKnowledgeBase(
    kb_dir="./docs",
    chunk_config={
        'min_chunk_size': 200,
        'max_chunk_size': 1500,
        'chunk_overlap': 100
    }
)
```

### Async Batch Processing

Process multiple questions concurrently:

```python
import asyncio

questions = [
    "What is RAG?",
    "How do I deploy this?",
    "What are best practices?"
]

results = await agent.answer_multiple_questions_async(
    questions=questions,
    save_to_file=True
)
```

### Automatic Updates

Monitor and re-index when files change:

```python
from kb_file_watcher import KnowledgeBaseWatcher

watcher = KnowledgeBaseWatcher(
    knowledge_base=kb,
    debounce_seconds=2.0
)

watcher.start(recursive=True)
# Files are now being monitored for changes
```

## Configuration

### Embedding Models

| Model                        | Speed  | Accuracy | Dimension | Best For            |
| ---------------------------- | ------ | -------- | --------- | ------------------- |
| `all-MiniLM-L6-v2`           | ⚡⚡⚡ | ⭐⭐     | 384       | Fast prototyping    |
| `all-mpnet-base-v2`          | ⚡⚡   | ⭐⭐⭐   | 768       | Production accuracy |
| `multi-qa-mpnet-base-dot-v1` | ⚡⚡   | ⭐⭐⭐   | 768       | Q&A specific        |

### LLM Providers

Works with multiple LLM providers through Ceylon:

```python
# Anthropic Claude
llm_config = LlmConfig.anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    model="claude-3-5-sonnet-20241022"
)

# OpenAI
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
```

## How It Works

### RAG Pipeline

```
1. User Question
   ↓
2. Convert to Vector Embedding
   ↓
3. Search Knowledge Base
   (Find top-k similar chunks)
   ↓
4. Format Context
   (Question + Retrieved Chunks)
   ↓
5. Send to LLM
   ↓
6. Generate Answer + Citations
```

### Example Flow

```python
# User asks
question = "What are the installation steps?"

# System retrieves relevant chunks
chunks = kb.search(question, top_k=5)
# → Returns 5 most relevant sections about installation

# Sends to LLM with context
answer = agent.answer_question(question)
# → LLM generates answer using retrieved documentation

# Result includes citations
print(answer['answer'])
print(answer['sources'])  # Lists source files/sections
```

## Best Practices

### Documentation Structure

✅ **DO:**

- Use clear heading hierarchy
- Include code examples in fenced blocks
- Keep related content together
- Use descriptive section names

❌ **DON'T:**

- Use flat files without headings
- Mix unrelated topics
- Use generic section names

### Performance Optimization

**For large knowledge bases:**

- Use `all-MiniLM-L6-v2` for faster indexing
- Increase chunk sizes to reduce total chunks
- Consider batch indexing

**For better accuracy:**

- Use `all-mpnet-base-v2` model
- Increase chunk overlap (150-200)
- Adjust top_k results (5-10)

### Query Tips

```python
# ❌ Vague queries
"tell me about this"

# ✅ Specific questions
"What are the installation steps for Python 3.8?"
"How do I configure the database connection?"
"What are the system requirements?"
```

## Troubleshooting

### Slow Indexing

**Solutions:**

1. Use faster model: `all-MiniLM-L6-v2`
2. Reduce chunk overlap
3. Increase max_chunk_size
4. Enable GPU (automatic with PyTorch)

### No Search Results

**Solutions:**

1. Check stats: `kb.get_stats()`
2. Try simpler queries
3. Increase top_k parameter
4. Verify markdown files have headings

### Poor Results Quality

**Solutions:**

1. Use better model: `all-mpnet-base-v2`
2. Increase top_k results
3. Adjust chunk overlap (100-200)
4. Improve document structure

### API Errors

**Solutions:**

1. Verify API key: `echo $ANTHROPIC_API_KEY`
2. Check rate limits
3. Try alternative LLM provider

## Components

### MarkdownKnowledgeBase

Main manager for markdown documentation.

**Key Methods:**

- `index_all_files()` - Index all markdown files
- `index_file(path)` - Index single file
- `search(query, top_k)` - Semantic search
- `check_for_updates()` - Detect file changes
- `get_stats()` - Get KB statistics

### MarkdownRAGAgent

LLM-powered Q&A generation.

**Key Methods:**

- `answer_question(question, save_to_file)` - Generate answer
- `answer_question_async()` - Async version
- `answer_multiple_questions_async(questions)` - Batch processing
- `export_qa_history(path)` - Export all Q&As

### KnowledgeBaseWatcher

Automatic file monitoring.

**Key Methods:**

- `start(recursive)` - Start watching
- `stop()` - Stop watching
- `watch_forever(recursive)` - Block and watch

## Advanced Usage

### Filtered Search

Search within specific files:

```python
results = kb.search(
    query="installation",
    filter_file="./docs/getting-started.md"
)
```

### Custom Update Callbacks

```python
def on_kb_update(stats):
    print(f"KB updated: {stats['total_chunks']} chunks")
    # Trigger notifications, update dashboard, etc.

watcher = KnowledgeBaseWatcher(
    knowledge_base=kb,
    on_update_callback=on_kb_update
)
```

### Export Q&A History

```python
# After answering questions
agent.export_qa_history("./complete_qa_history.md")
```

## Example Files

| File                          | Description              |
| ----------------------------- | ------------------------ |
| `demo_markdown_rag_system.py` | Complete demonstration   |
| `quick_start_markdown_rag.py` | Minimal quick start      |
| `markdown_kb_manager.py`      | Core KB management       |
| `rag_markdown_agent.py`       | RAG agent implementation |
| `kb_file_watcher.py`          | File watching system     |
| `MARKDOWN_RAG_GUIDE.md`       | Comprehensive guide      |

## Next Steps

1. Try with your own markdown documentation
2. Experiment with different embedding models
3. Customize chunk sizes for your content
4. Integrate into your application
5. Deploy with monitoring and caching

## Further Reading

- [Getting Started Guide](../../getting-started/quickstart.md)
- [LLM Integration](../../guide/llm/overview.md)
- [Async Programming](../../guide/async/overview.md)
- [API Reference](../../api/core/llm-agent.md)

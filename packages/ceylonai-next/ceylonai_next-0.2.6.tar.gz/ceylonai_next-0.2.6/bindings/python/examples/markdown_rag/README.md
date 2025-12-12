# Advanced Markdown RAG System

Build intelligent Q&A systems from markdown documentation with automatic updates and LLM-powered answers.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements-markdown-rag.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# 3. Run the interactive quick start
python quick_start_markdown_rag.py

# OR run the complete demo
python demo_markdown_rag_system.py
```

## 📚 What's Included

| File | Description |
|------|-------------|
| `markdown_kb_manager.py` | Core knowledge base with intelligent markdown parsing and vector search |
| `rag_markdown_agent.py` | LLM-powered Q&A agent that generates markdown Q&A files |
| `kb_file_watcher.py` | Automatic file monitoring and re-indexing |
| `demo_markdown_rag_system.py` | Complete demonstration with 5 interactive demos |
| `quick_start_markdown_rag.py` | Simple interactive quick start |
| `requirements-markdown-rag.txt` | All dependencies |
| `MARKDOWN_RAG_GUIDE.md` | **Complete documentation** (architecture, API, troubleshooting) |
| `__init__.py` | Python package interface |

## 💡 Basic Usage

### From Within This Directory

```python
# If you're running code from within the markdown_rag folder
from markdown_kb_manager import MarkdownKnowledgeBase
from rag_markdown_agent import MarkdownRAGAgent
from ceylon import LlmConfig
import os

# Initialize knowledge base
kb = MarkdownKnowledgeBase("./my_docs")
kb.index_all_files()

# Create RAG agent
llm_config = LlmConfig.anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    model="claude-3-5-sonnet-20241022"
)

agent = MarkdownRAGAgent(kb, llm_config=llm_config)

# Ask questions
result = agent.answer_question(
    "What are the main features?",
    save_to_file=True
)

print(result['answer'])
# Q&A saved to ./qa_output/
```

### As a Python Package

```python
# If you're importing from outside this folder
from examples.markdown_rag import (
    MarkdownKnowledgeBase,
    MarkdownRAGAgent,
    watch_knowledge_base
)

# Same usage as above
kb = MarkdownKnowledgeBase("./my_docs")
kb.index_all_files()
# ... etc
```

## 🎯 Key Features

✅ **Intelligent Markdown Parsing** - Preserves structure, headings, code blocks
✅ **Section-Based Chunking** - Smart chunking by headings, not arbitrary splits
✅ **Semantic Search** - Vector embeddings for finding relevant information
✅ **Auto-Updates** - File watching with automatic re-indexing
✅ **Q&A Generation** - LLM-powered answers with source citations
✅ **Markdown Output** - Well-formatted Q&A files
✅ **Async Support** - Concurrent question processing
✅ **Multi-Provider** - Works with Claude, OpenAI, Ollama, and 10+ LLM providers

## 📖 Examples

### Example 1: Simple Search

```python
from markdown_kb_manager import MarkdownKnowledgeBase

kb = MarkdownKnowledgeBase("./my_docs")
kb.index_all_files()

results = kb.search("How do I install?", top_k=5)
for chunk, score in results:
    print(f"[{score:.2f}] {chunk.heading_path}")
```

### Example 2: Q&A with File Watching

```python
from markdown_rag import MarkdownKnowledgeBase, MarkdownRAGAgent
from kb_file_watcher import KnowledgeBaseWatcher

# Initialize
kb = MarkdownKnowledgeBase("./my_docs")
kb.index_all_files()

agent = MarkdownRAGAgent(kb, llm_config=your_config)

# Start file watcher
watcher = KnowledgeBaseWatcher(kb, debounce_seconds=2.0)
watcher.start(recursive=True)

# Ask questions (knowledge base auto-updates when files change!)
result = agent.answer_question("What's new?")
```

### Example 3: Batch Processing (Async)

```python
import asyncio
from markdown_rag import MarkdownKnowledgeBase, MarkdownRAGAgent

async def process_questions():
    kb = MarkdownKnowledgeBase("./my_docs")
    kb.index_all_files()

    agent = MarkdownRAGAgent(kb, llm_config=your_config)

    questions = [
        "What is the installation process?",
        "What are the requirements?",
        "How do I troubleshoot?"
    ]

    results = await agent.answer_multiple_questions_async(questions)
    return results

results = asyncio.run(process_questions())
```

## 🔧 Configuration

### Chunk Sizes

```python
kb = MarkdownKnowledgeBase(
    kb_dir="./docs",
    model_name='all-MiniLM-L6-v2',
    chunk_config={
        'min_chunk_size': 200,
        'max_chunk_size': 1500,
        'chunk_overlap': 100
    }
)
```

### Embedding Models

- `all-MiniLM-L6-v2` - Fast, good for prototyping (default)
- `all-mpnet-base-v2` - More accurate, slightly slower
- `multi-qa-mpnet-base-dot-v1` - Optimized for Q&A tasks

### LLM Providers

```python
from ceylon import LlmConfig

# Claude (Anthropic)
llm_config = LlmConfig.anthropic(api_key=key, model="claude-3-5-sonnet-20241022")

# OpenAI
llm_config = LlmConfig.openai(api_key=key, model="gpt-4-turbo-preview")

# Ollama (local)
llm_config = LlmConfig.ollama(base_url="http://localhost:11434", model="llama2")
```

## 📂 File Organization

All markdown RAG files are now organized in this folder:

```
markdown_rag/
├── README.md                          # This file
├── MARKDOWN_RAG_GUIDE.md             # Complete documentation
├── __init__.py                        # Package interface
├── markdown_kb_manager.py            # Core knowledge base
├── rag_markdown_agent.py             # Q&A agent
├── kb_file_watcher.py                # File watching
├── demo_markdown_rag_system.py       # Full demo
├── quick_start_markdown_rag.py       # Quick start
└── requirements-markdown-rag.txt     # Dependencies
```

## 📖 Full Documentation

For complete documentation including:
- Architecture diagrams
- API reference
- Best practices
- Troubleshooting
- Advanced usage

See **[MARKDOWN_RAG_GUIDE.md](MARKDOWN_RAG_GUIDE.md)**

## 🆘 Troubleshooting

**No search results?**
→ Lower the similarity threshold: `VectorKnowledgeBase(similarity_threshold=0.2)`

**Slow indexing?**
→ Use faster model: `model_name='all-MiniLM-L6-v2'`

**File watcher not working?**
→ Check file permissions and ensure files have `.md` extension

**LLM errors?**
→ Verify API key: `echo $ANTHROPIC_API_KEY`

See MARKDOWN_RAG_GUIDE.md for more troubleshooting tips.

## 📄 License

Part of the Ceylon Agent Framework. See main repository for license.

---

**Ready to build intelligent documentation systems? Start with `quick_start_markdown_rag.py`!**

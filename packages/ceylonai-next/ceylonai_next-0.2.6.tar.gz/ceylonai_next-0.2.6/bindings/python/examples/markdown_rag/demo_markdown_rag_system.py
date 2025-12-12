"""
Complete Demonstration of Advanced Markdown RAG System

This example demonstrates:
1. Creating a markdown knowledge base from a folder
2. Intelligent parsing and chunking of markdown files
3. Vector-based semantic search
4. Q&A generation with LLM (Claude)
5. Automatic markdown Q&A file creation
6. File watching for auto-updates
7. Concurrent question answering

Usage:
    # Set your API key first
    export ANTHROPIC_API_KEY="your-api-key-here"

    # Run the demo
    python demo_markdown_rag_system.py

    # Or with custom knowledge base directory
    python demo_markdown_rag_system.py /path/to/your/markdown/files
"""

import os
import sys
import asyncio
from pathlib import Path

from ceylonai_next import LlmConfig
from markdown_kb_manager import MarkdownKnowledgeBase
from rag_markdown_agent import MarkdownRAGAgent
from kb_file_watcher import KnowledgeBaseWatcher


def demo_basic_usage(kb_dir: str):
    """
    Demonstrate basic usage of the markdown RAG system.

    Args:
        kb_dir: Path to knowledge base directory
    """
    print("\n" + "="*80)
    print("DEMO 1: Basic Markdown RAG System Usage")
    print("="*80 + "\n")

    # Step 1: Initialize knowledge base
    print("Step 1: Initializing knowledge base...")
    kb = MarkdownKnowledgeBase(
        kb_dir=kb_dir,
        model_name='all-MiniLM-L6-v2',  # Fast and efficient model
        chunk_config={
            'min_chunk_size': 200,
            'max_chunk_size': 1500,
            'chunk_overlap': 100
        }
    )

    # Step 2: Index all markdown files
    print("\nStep 2: Indexing all markdown files...")
    kb.index_all_files()

    # Step 3: Show statistics
    print("\nStep 3: Knowledge base statistics:")
    stats = kb.get_stats()
    print(f"  📚 Total files indexed: {stats['total_files']}")
    print(f"  📄 Total chunks created: {stats['total_chunks']}")
    print(f"  🧮 Embedding dimension: {stats['embedding_dimension']}")
    print(f"\n  Files:")
    for file in stats['files']:
        print(f"    - {Path(file).name}")

    # Step 4: Test semantic search
    print("\nStep 4: Testing semantic search...")
    test_queries = [
        "What is this documentation about?",
        "How do I get started?",
        "What are the main features?"
    ]

    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = kb.search(query, top_k=3)

        if results:
            print(f"  Found {len(results)} relevant chunks:")
            for i, (chunk, score) in enumerate(results, 1):
                heading = " > ".join(chunk.heading_path) if chunk.heading_path else "Content"
                print(f"    {i}. [{score:.3f}] {Path(chunk.file_path).name} - {heading}")
        else:
            print("  No results found")

    print("\n" + "="*80 + "\n")
    return kb


def demo_rag_agent(kb: MarkdownKnowledgeBase):
    """
    Demonstrate RAG agent Q&A generation.

    Args:
        kb: Initialized MarkdownKnowledgeBase
    """
    print("\n" + "="*80)
    print("DEMO 2: RAG Agent Q&A Generation")
    print("="*80 + "\n")

    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY not set. Skipping LLM demo.")
        print("   Set the environment variable to enable Q&A generation:")
        print("   export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\n" + "="*80 + "\n")
        return None

    # Step 1: Create RAG agent
    print("Step 1: Creating RAG agent with Claude...")
    llm_config = LlmConfig.anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        model="claude-3-5-sonnet-20241022"
    )

    agent = MarkdownRAGAgent(
        knowledge_base=kb,
        llm_config=llm_config,
        output_dir="./qa_output",
        top_k_results=5
    )

    # Step 2: Ask questions
    print("\nStep 2: Asking questions and generating Q&A files...")

    questions = [
        "What is the main purpose of this documentation?",
        "What are the key features or components described?",
        "How do I get started with this system?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i}/{len(questions)} ---")
        result = agent.answer_question(
            question=question,
            save_to_file=True
        )

        print(f"\n📝 Answer Preview:")
        answer_preview = result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer']
        print(answer_preview)

    # Step 3: Export Q&A history
    print("\nStep 3: Exporting Q&A history...")
    history_file = "./qa_output/qa_history.md"
    agent.export_qa_history(history_file)

    print("\n" + "="*80 + "\n")
    return agent


async def demo_async_qa(agent: MarkdownRAGAgent):
    """
    Demonstrate concurrent Q&A generation using async.

    Args:
        agent: Initialized MarkdownRAGAgent
    """
    print("\n" + "="*80)
    print("DEMO 3: Concurrent Question Answering (Async)")
    print("="*80 + "\n")

    if agent is None:
        print("⚠️  Skipped (no API key provided)")
        print("\n" + "="*80 + "\n")
        return

    print("Asking multiple questions concurrently...")

    questions = [
        "What are the technical requirements?",
        "What are the best practices mentioned?",
        "What examples are provided?"
    ]

    results = await agent.answer_multiple_questions_async(
        questions=questions,
        save_to_file=True
    )

    print(f"\n✅ Successfully answered {len(results)} questions concurrently!")

    print("\n" + "="*80 + "\n")


def demo_knowledge_base_updates(kb: MarkdownKnowledgeBase):
    """
    Demonstrate knowledge base update detection.

    Args:
        kb: Initialized MarkdownKnowledgeBase
    """
    print("\n" + "="*80)
    print("DEMO 4: Knowledge Base Update Detection")
    print("="*80 + "\n")

    print("Checking for updates to the knowledge base...")
    print("(This will detect any new, modified, or deleted files)\n")

    updated_files = kb.check_for_updates()

    if updated_files:
        print(f"\n✓ Updated {len(updated_files)} files:")
        for file in updated_files:
            print(f"  - {Path(file).name}")
    else:
        print("\n✓ No updates detected - knowledge base is up to date")

    print("\n" + "="*80 + "\n")


def demo_file_watching(kb: MarkdownKnowledgeBase, duration_seconds: int = 30):
    """
    Demonstrate automatic file watching (runs for limited time in demo).

    Args:
        kb: Initialized MarkdownKnowledgeBase
        duration_seconds: How long to watch for changes
    """
    print("\n" + "="*80)
    print("DEMO 5: Automatic File Watching")
    print("="*80 + "\n")

    print(f"Starting file watcher for {duration_seconds} seconds...")
    print(f"Directory: {kb.kb_dir}")
    print("\nTry modifying a markdown file in the knowledge base directory!")
    print("The system will automatically detect changes and re-index.\n")

    def on_update(stats):
        """Callback when files are updated."""
        print(f"\n✨ Knowledge base updated!")
        print(f"   Files: {stats['total_files']}, Chunks: {stats['total_chunks']}\n")

    watcher = KnowledgeBaseWatcher(
        knowledge_base=kb,
        debounce_seconds=2.0,
        on_update_callback=on_update
    )

    watcher.start(recursive=True)

    try:
        import time
        for remaining in range(duration_seconds, 0, -1):
            print(f"\r⏱️  Time remaining: {remaining}s  ", end='', flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    finally:
        watcher.stop()

    print("\n\n" + "="*80 + "\n")


def create_sample_knowledge_base(base_dir: str = "./sample_kb"):
    """
    Create a sample knowledge base with example markdown files.

    Args:
        base_dir: Directory to create sample files in

    Returns:
        Path to the created knowledge base directory
    """
    kb_path = Path(base_dir)
    kb_path.mkdir(exist_ok=True, parents=True)

    # Sample file 1: Introduction
    intro_md = """# Introduction to the Advanced RAG System

## Overview

This is an advanced Retrieval-Augmented Generation (RAG) system designed for markdown knowledge bases.

## What is RAG?

RAG combines the power of:
- **Information Retrieval**: Finding relevant documents from a knowledge base
- **Language Generation**: Using LLMs to generate natural, contextual answers
- **Semantic Search**: Vector embeddings for intelligent document matching

## Key Features

### 1. Intelligent Markdown Parsing

The system intelligently parses markdown files while preserving:
- Document structure and hierarchy
- Section headings and numbering
- Code blocks with syntax highlighting
- Internal and external links

### 2. Vector-Based Search

Uses state-of-the-art sentence transformers for semantic search:
- Cosine similarity matching
- Configurable relevance thresholds
- Metadata-based filtering

### 3. Automatic Updates

The system can automatically detect and process changes:
- File creation detection
- Modification tracking
- Deletion handling
- Debounced re-indexing for efficiency

## Getting Started

To use this system, you need:
1. Python 3.8 or higher
2. An API key for your LLM provider (e.g., Anthropic Claude)
3. A directory containing markdown documentation

See the installation guide for detailed setup instructions.
"""

    # Sample file 2: Installation
    install_md = """# Installation Guide

## Prerequisites

Before installing, ensure you have:
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements-markdown-rag.txt
```

### 2. Set Up API Keys

For Claude (Anthropic):
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

For OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Prepare Your Knowledge Base

Create a directory with your markdown files:
```bash
mkdir my_knowledge_base
cp *.md my_knowledge_base/
```

## Verification

Test your installation:

```python
from markdown_kb_manager import MarkdownKnowledgeBase

kb = MarkdownKnowledgeBase("./my_knowledge_base")
kb.index_all_files()
print(kb.get_stats())
```

If you see statistics about indexed files and chunks, you're ready to go!
"""

    # Sample file 3: Usage Examples
    usage_md = """# Usage Examples

## Basic Usage

### Indexing a Knowledge Base

```python
from markdown_kb_manager import MarkdownKnowledgeBase

kb = MarkdownKnowledgeBase(
    kb_dir="./my_docs",
    model_name='all-MiniLM-L6-v2'
)
kb.index_all_files()
```

### Searching the Knowledge Base

```python
results = kb.search("How do I install?", top_k=5)

for chunk, score in results:
    print(f"Relevance: {score:.2f}")
    print(f"Section: {' > '.join(chunk.heading_path)}")
    print(f"Content: {chunk.content[:200]}...")
```

## Advanced Features

### Q&A Generation

```python
from rag_markdown_agent import MarkdownRAGAgent
from ceylon import LlmConfig

llm_config = LlmConfig.anthropic(
    api_key="your-key",
    model="claude-3-5-sonnet-20241022"
)

agent = MarkdownRAGAgent(kb, llm_config=llm_config)

result = agent.answer_question(
    "What are the main features?",
    save_to_file=True
)

print(result['answer'])
```

### Automatic File Watching

```python
from kb_file_watcher import watch_knowledge_base

watch_knowledge_base(
    kb_dir="./my_docs",
    debounce_seconds=2.0
)
```

## Best Practices

1. **Chunk Size**: Use 1000-1500 characters for optimal performance
2. **Model Selection**: all-MiniLM-L6-v2 for speed, all-mpnet-base-v2 for accuracy
3. **Update Frequency**: Set debounce to 2-5 seconds to avoid excessive re-indexing
4. **API Rate Limits**: Use async methods for batch processing

## Troubleshooting

### Common Issues

**Problem**: Slow indexing
- **Solution**: Reduce chunk size or use a faster embedding model

**Problem**: No results found
- **Solution**: Lower the similarity threshold (default 0.3)

**Problem**: Memory errors with large knowledge bases
- **Solution**: Use batch processing or consider external vector database
"""

    # Write files
    files = {
        'introduction.md': intro_md,
        'installation.md': install_md,
        'usage.md': usage_md
    }

    for filename, content in files.items():
        file_path = kb_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"✓ Created sample knowledge base at: {kb_path}")
    print(f"  Files created: {len(files)}")

    return str(kb_path)


def main():
    """Main demo function."""
    print("\n" + "="*80)
    print("Advanced Markdown RAG System - Complete Demonstration")
    print("="*80)

    # Determine knowledge base directory
    if len(sys.argv) > 1:
        kb_dir = sys.argv[1]
        if not Path(kb_dir).exists():
            print(f"\n❌ Error: Directory not found: {kb_dir}")
            sys.exit(1)
    else:
        # Create sample knowledge base
        print("\nNo knowledge base directory specified.")
        print("Creating sample knowledge base...\n")
        kb_dir = create_sample_knowledge_base("./sample_kb")

    # Run demos
    kb = demo_basic_usage(kb_dir)
    agent = demo_rag_agent(kb)

    # Run async demo
    if agent:
        asyncio.run(demo_async_qa(agent))

    demo_knowledge_base_updates(kb)

    # Ask user if they want to run file watcher demo
    print("\n" + "="*80)
    print("Optional: File Watcher Demo")
    print("="*80)
    print("\nThe file watcher demo will monitor the knowledge base for 30 seconds.")
    print("You can modify markdown files during this time to see auto-updates.\n")

    response = input("Run file watcher demo? (y/N): ").strip().lower()
    if response == 'y':
        demo_file_watching(kb, duration_seconds=30)
    else:
        print("\nSkipping file watcher demo.\n")

    # Summary
    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nWhat was demonstrated:")
    print("  ✓ Markdown knowledge base creation and indexing")
    print("  ✓ Intelligent section-based chunking")
    print("  ✓ Vector-based semantic search")

    if agent:
        print("  ✓ LLM-powered Q&A generation")
        print("  ✓ Automatic markdown Q&A file creation")
        print("  ✓ Concurrent question answering (async)")
        print(f"\n📁 Q&A files saved to: ./qa_output/")

    print("  ✓ Knowledge base update detection")

    print("\nNext steps:")
    print("  1. Try with your own markdown files")
    print("  2. Experiment with different embedding models")
    print("  3. Customize chunk sizes and overlap")
    print("  4. Integrate with your own applications")
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()

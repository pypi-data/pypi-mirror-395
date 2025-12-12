"""
Quick Start - Markdown RAG System

The simplest way to get started with the Markdown RAG system.

Usage:
    1. Set your API key:
       export ANTHROPIC_API_KEY="your-api-key"

    2. Run the script:
       python quick_start_markdown_rag.py

    3. Follow the interactive prompts!
"""

import os
from pathlib import Path

from markdown_kb_manager import MarkdownKnowledgeBase
from rag_markdown_agent import MarkdownRAGAgent
from ceylonai_next import LlmConfig


def main():
    print("\n" + "="*60)
    print("Markdown RAG System - Quick Start")
    print("="*60 + "\n")

    # Step 1: Get knowledge base directory
    kb_dir = input("Enter path to your markdown files directory\n(or press Enter for './sample_kb'): ").strip()

    if not kb_dir:
        kb_dir = "./sample_kb"

        # Create sample if it doesn't exist
        if not Path(kb_dir).exists():
            print("\nCreating sample knowledge base...")
            Path(kb_dir).mkdir(exist_ok=True)

            # Create a sample markdown file
            sample_content = """# Sample Documentation

## Introduction

This is a sample markdown knowledge base for testing the RAG system.

## Features

The system includes:
- Intelligent markdown parsing
- Vector-based semantic search
- Automatic Q&A generation
- File watching capabilities

## Getting Started

To use this system:
1. Point it to your markdown directory
2. Ask questions about your documentation
3. Get AI-generated answers with citations

## Example Code

```python
from markdown_kb_manager import MarkdownKnowledgeBase

kb = MarkdownKnowledgeBase("./docs")
kb.index_all_files()
results = kb.search("How do I get started?")
```

## Conclusion

This is a powerful tool for making your documentation interactive and searchable!
"""
            with open(Path(kb_dir) / "sample.md", 'w') as f:
                f.write(sample_content)

            print(f"✓ Created sample knowledge base at: {kb_dir}")

    # Step 2: Initialize knowledge base
    print(f"\nIndexing markdown files in: {kb_dir}")
    try:
        kb = MarkdownKnowledgeBase(
            kb_dir=kb_dir,
            model_name='all-MiniLM-L6-v2'
        )
        kb.index_all_files()

        stats = kb.get_stats()
        print(f"\n✓ Knowledge base ready!")
        print(f"  Files indexed: {stats['total_files']}")
        print(f"  Chunks created: {stats['total_chunks']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return

    # Step 3: Try semantic search
    print("\n" + "="*60)
    print("Testing Semantic Search")
    print("="*60 + "\n")

    query = input("Enter a search query (or press Enter for default): ").strip()
    if not query:
        query = "What features are available?"

    print(f"\nSearching for: '{query}'")
    results = kb.search(query, top_k=3)

    if results:
        print(f"\nFound {len(results)} relevant chunks:\n")
        for i, (chunk, score) in enumerate(results, 1):
            heading = " > ".join(chunk.heading_path) if chunk.heading_path else "Content"
            print(f"{i}. [{score:.3f}] {Path(chunk.file_path).name}")
            print(f"   Section: {heading}")
            print(f"   Preview: {chunk.content[:150]}...\n")
    else:
        print("No results found. Try a different query.")

    # Step 4: Q&A Generation (optional)
    print("\n" + "="*60)
    print("Q&A Generation (Optional)")
    print("="*60 + "\n")

    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY not set.")
        print("   To use Q&A generation, set your API key:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("\nSkipping Q&A generation demo.")
        return

    use_llm = input("Generate AI answer? (y/N): ").strip().lower()

    if use_llm == 'y':
        print("\nInitializing RAG agent with Claude...")

        try:
            llm_config = LlmConfig.anthropic(
                api_key=os.getenv('ANTHROPIC_API_KEY'),
                model="claude-3-5-sonnet-20241022"
            )

            agent = MarkdownRAGAgent(
                knowledge_base=kb,
                llm_config=llm_config,
                output_dir="./qa_output"
            )

            question = input("\nAsk a question (or press Enter for default): ").strip()
            if not question:
                question = "What is this documentation about?"

            print(f"\nGenerating answer to: '{question}'")
            result = agent.answer_question(
                question=question,
                save_to_file=True
            )

            print("\n" + "="*60)
            print("Answer:")
            print("="*60 + "\n")
            print(result['answer'])
            print("\n" + "="*60)

            if result.get('file_path'):
                print(f"\n💾 Q&A saved to: {result['file_path']}")

        except Exception as e:
            print(f"\n❌ Error generating answer: {e}")
            return

    # Done!
    print("\n" + "="*60)
    print("Quick Start Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Try with your own markdown files")
    print("  2. Run the full demo: python demo_markdown_rag_system.py")
    print("  3. Read the guide: MARKDOWN_RAG_GUIDE.md")
    print("  4. Set up file watching for auto-updates")
    print("\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

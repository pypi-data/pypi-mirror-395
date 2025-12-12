"""
Advanced Markdown RAG System

A comprehensive RAG (Retrieval-Augmented Generation) system for markdown knowledge bases.

Main Components:
    - MarkdownKnowledgeBase: Manage and index markdown documentation
    - MarkdownRAGAgent: LLM-powered Q&A with citation generation
    - KnowledgeBaseWatcher: Automatic file monitoring and re-indexing

Quick Start:
    >>> from markdown_rag import MarkdownKnowledgeBase, MarkdownRAGAgent
    >>> from ceylonai_next import LlmConfig
    >>> import os
    >>>
    >>> # Initialize knowledge base
    >>> kb = MarkdownKnowledgeBase("./my_docs")
    >>> kb.index_all_files()
    >>>
    >>> # Create RAG agent
    >>> llm_config = LlmConfig.anthropic(
    ...     api_key=os.getenv('ANTHROPIC_API_KEY'),
    ...     model="claude-3-5-sonnet-20241022"
    ... )
    >>> agent = MarkdownRAGAgent(kb, llm_config=llm_config)
    >>>
    >>> # Ask questions
    >>> result = agent.answer_question("What is this about?", save_to_file=True)
    >>> print(result['answer'])

For more information, see MARKDOWN_RAG_GUIDE.md
"""

from .markdown_kb_manager import (
    MarkdownKnowledgeBase,
    MarkdownParser,
    MarkdownChunker,
    VectorKnowledgeBase,
    MarkdownChunk
)

from .rag_markdown_agent import (
    MarkdownRAGAgent,
    quick_answer
)

from .kb_file_watcher import (
    KnowledgeBaseWatcher,
    MarkdownFileWatcher,
    watch_knowledge_base
)

__all__ = [
    # Knowledge Base Management
    'MarkdownKnowledgeBase',
    'MarkdownParser',
    'MarkdownChunker',
    'VectorKnowledgeBase',
    'MarkdownChunk',

    # RAG Agent
    'MarkdownRAGAgent',
    'quick_answer',

    # File Watching
    'KnowledgeBaseWatcher',
    'MarkdownFileWatcher',
    'watch_knowledge_base',
]

__version__ = '1.0.0'
__author__ = 'Ceylon AI'

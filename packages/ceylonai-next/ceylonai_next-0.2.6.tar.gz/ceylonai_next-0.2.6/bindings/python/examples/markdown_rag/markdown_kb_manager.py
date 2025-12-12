"""
Advanced Markdown Knowledge Base Manager for RAG System

This module provides intelligent markdown parsing, chunking, and indexing
for RAG (Retrieval-Augmented Generation) applications.

Features:
- Intelligent markdown parsing with structure preservation
- Section-based chunking (by headings)
- Metadata extraction (file path, heading hierarchy, section numbers)
- Vector embeddings with semantic search
- File watching for automatic knowledge base updates
- Efficient re-indexing on file changes
"""

import os
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class MarkdownChunk:
    """Represents a chunk of markdown content with metadata."""

    chunk_id: str
    content: str
    file_path: str
    heading_path: List[str]  # Hierarchical path of headings, e.g., ["Introduction", "Getting Started"]
    heading_level: int
    section_number: str  # e.g., "1.2.3"
    chunk_index: int  # Index within the file
    char_start: int
    char_end: int
    code_blocks: List[Dict[str, str]]  # List of code blocks with language
    links: List[str]  # Internal and external links
    file_hash: str  # Hash of source file for change detection
    created_at: str
    embedding: Optional[np.ndarray] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage."""
        data = asdict(self)
        if self.embedding is not None:
            data['embedding'] = self.embedding.tolist()
        return data

    def get_display_content(self, max_length: int = 200) -> str:
        """Get truncated content for display."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."


class MarkdownParser:
    """Intelligent markdown parser that preserves structure."""

    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    CODE_BLOCK_PATTERN = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

    @staticmethod
    def parse_file(file_path: str) -> Tuple[str, str]:
        """
        Parse a markdown file and return content with file hash.

        Args:
            file_path: Path to the markdown file

        Returns:
            Tuple of (content, file_hash)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Calculate file hash for change detection
        file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

        return content, file_hash

    @staticmethod
    def extract_headings(content: str) -> List[Tuple[int, int, str, int]]:
        """
        Extract all headings with their positions.

        Args:
            content: Markdown content

        Returns:
            List of tuples: (start_pos, end_pos, heading_text, level)
        """
        headings = []
        for match in MarkdownParser.HEADING_PATTERN.finditer(content):
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((match.start(), match.end(), text, level))
        return headings

    @staticmethod
    def extract_code_blocks(content: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown content.

        Args:
            content: Markdown content

        Returns:
            List of dictionaries with 'language' and 'code' keys
        """
        code_blocks = []
        for match in MarkdownParser.CODE_BLOCK_PATTERN.finditer(content):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            code_blocks.append({'language': language, 'code': code})
        return code_blocks

    @staticmethod
    def extract_links(content: str) -> List[str]:
        """
        Extract all links from markdown content.

        Args:
            content: Markdown content

        Returns:
            List of link URLs
        """
        return [match.group(2) for match in MarkdownParser.LINK_PATTERN.finditer(content)]


class MarkdownChunker:
    """Intelligent chunking of markdown documents by sections."""

    def __init__(
        self,
        min_chunk_size: int = 200,
        max_chunk_size: int = 1500,
        chunk_overlap: int = 100
    ):
        """
        Initialize the chunker.

        Args:
            min_chunk_size: Minimum size for a chunk (chars)
            max_chunk_size: Maximum size for a chunk (chars)
            chunk_overlap: Overlap between chunks (chars)
        """
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_by_sections(
        self,
        file_path: str,
        content: str,
        file_hash: str
    ) -> List[MarkdownChunk]:
        """
        Chunk markdown content by sections (headings).

        Args:
            file_path: Path to the source file
            content: Markdown content
            file_hash: Hash of the file for change detection

        Returns:
            List of MarkdownChunk objects
        """
        chunks = []
        headings = MarkdownParser.extract_headings(content)

        if not headings:
            # No headings found, treat entire content as one section
            return self._chunk_content_without_headings(
                file_path, content, file_hash
            )

        # Build heading hierarchy
        heading_stack = []  # Stack to track current heading path
        section_counter = [0] * 6  # Counters for section numbers at each level

        for i, (start, end, heading_text, level) in enumerate(headings):
            # Update heading stack for hierarchy
            while heading_stack and heading_stack[-1][1] >= level:
                heading_stack.pop()
            heading_stack.append((heading_text, level))

            # Update section counter
            section_counter[level - 1] += 1
            for j in range(level, 6):
                section_counter[j] = 0

            # Build section number (e.g., "1.2.3")
            section_number = '.'.join(
                str(c) for c in section_counter[:level] if c > 0
            )

            # Get heading path (hierarchical)
            heading_path = [h[0] for h in heading_stack]

            # Determine section content boundaries
            section_start = end
            section_end = headings[i + 1][0] if i + 1 < len(headings) else len(content)

            # Extract section content (excluding the heading itself)
            section_content = content[section_start:section_end].strip()

            # Include heading in the chunk for context
            full_section = f"{'#' * level} {heading_text}\n\n{section_content}"

            # Extract metadata from this section
            code_blocks = MarkdownParser.extract_code_blocks(full_section)
            links = MarkdownParser.extract_links(full_section)

            # If section is too large, split it further
            if len(full_section) > self.max_chunk_size:
                sub_chunks = self._split_large_section(
                    full_section,
                    file_path,
                    heading_path,
                    level,
                    section_number,
                    code_blocks,
                    links,
                    file_hash,
                    start
                )
                chunks.extend(sub_chunks)
            else:
                # Create chunk
                chunk_id = self._generate_chunk_id(file_path, section_number, 0)
                chunk = MarkdownChunk(
                    chunk_id=chunk_id,
                    content=full_section,
                    file_path=file_path,
                    heading_path=heading_path,
                    heading_level=level,
                    section_number=section_number,
                    chunk_index=len(chunks),
                    char_start=start,
                    char_end=section_end,
                    code_blocks=code_blocks,
                    links=links,
                    file_hash=file_hash,
                    created_at=datetime.now().isoformat()
                )
                chunks.append(chunk)

        return chunks

    def _chunk_content_without_headings(
        self,
        file_path: str,
        content: str,
        file_hash: str
    ) -> List[MarkdownChunk]:
        """Chunk content that has no headings."""
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(content):
            end = min(start + self.max_chunk_size, len(content))

            # Try to break at paragraph boundary
            if end < len(content):
                last_para = content[start:end].rfind('\n\n')
                if last_para > self.min_chunk_size:
                    end = start + last_para

            chunk_content = content[start:end].strip()

            if chunk_content:
                chunk_id = self._generate_chunk_id(file_path, "0", chunk_index)
                code_blocks = MarkdownParser.extract_code_blocks(chunk_content)
                links = MarkdownParser.extract_links(chunk_content)

                chunk = MarkdownChunk(
                    chunk_id=chunk_id,
                    content=chunk_content,
                    file_path=file_path,
                    heading_path=[],
                    heading_level=0,
                    section_number="0",
                    chunk_index=chunk_index,
                    char_start=start,
                    char_end=end,
                    code_blocks=code_blocks,
                    links=links,
                    file_hash=file_hash,
                    created_at=datetime.now().isoformat()
                )
                chunks.append(chunk)
                chunk_index += 1

            start = end - self.chunk_overlap

        return chunks

    def _split_large_section(
        self,
        content: str,
        file_path: str,
        heading_path: List[str],
        level: int,
        section_number: str,
        code_blocks: List[Dict],
        links: List[str],
        file_hash: str,
        start_pos: int
    ) -> List[MarkdownChunk]:
        """Split a large section into smaller chunks."""
        chunks = []
        start = 0
        sub_index = 0

        while start < len(content):
            end = min(start + self.max_chunk_size, len(content))

            # Try to break at paragraph boundary
            if end < len(content):
                last_para = content[start:end].rfind('\n\n')
                if last_para > self.min_chunk_size:
                    end = start + last_para

            chunk_content = content[start:end].strip()

            if chunk_content:
                chunk_id = self._generate_chunk_id(file_path, section_number, sub_index)

                chunk = MarkdownChunk(
                    chunk_id=chunk_id,
                    content=chunk_content,
                    file_path=file_path,
                    heading_path=heading_path,
                    heading_level=level,
                    section_number=f"{section_number}.{sub_index}",
                    chunk_index=sub_index,
                    char_start=start_pos + start,
                    char_end=start_pos + end,
                    code_blocks=code_blocks if start == 0 else [],
                    links=links if start == 0 else [],
                    file_hash=file_hash,
                    created_at=datetime.now().isoformat()
                )
                chunks.append(chunk)
                sub_index += 1

            start = end - self.chunk_overlap

        return chunks

    @staticmethod
    def _generate_chunk_id(file_path: str, section_number: str, chunk_index: int) -> str:
        """Generate a unique chunk ID."""
        base = f"{file_path}::{section_number}::{chunk_index}"
        return hashlib.md5(base.encode('utf-8')).hexdigest()


class VectorKnowledgeBase:
    """Vector-based knowledge base for semantic search."""

    def __init__(
        self,
        model_name: str = 'all-MiniLM-L6-v2',
        similarity_threshold: float = 0.3
    ):
        """
        Initialize the knowledge base.

        Args:
            model_name: Name of the sentence transformer model
            similarity_threshold: Minimum similarity score for retrieval
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold

        # Storage
        self.chunks: List[MarkdownChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        self.file_hashes: Dict[str, str] = {}  # file_path -> hash

        print(f"✓ Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")

    def add_chunks(self, chunks: List[MarkdownChunk]) -> None:
        """
        Add chunks to the knowledge base and generate embeddings.

        Args:
            chunks: List of MarkdownChunk objects
        """
        if not chunks:
            return

        print(f"Generating embeddings for {len(chunks)} chunks...")

        # Generate embeddings
        texts = [chunk.content for chunk in chunks]
        new_embeddings = self.model.encode(texts, show_progress_bar=True)

        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, new_embeddings):
            chunk.embedding = embedding

        # Update storage
        self.chunks.extend(chunks)

        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])

        # Update file hashes
        for chunk in chunks:
            self.file_hashes[chunk.file_path] = chunk.file_hash

        print(f"✓ Added {len(chunks)} chunks. Total chunks: {len(self.chunks)}")

    def remove_file_chunks(self, file_path: str) -> int:
        """
        Remove all chunks from a specific file.

        Args:
            file_path: Path to the file

        Returns:
            Number of chunks removed
        """
        indices_to_remove = [
            i for i, chunk in enumerate(self.chunks)
            if chunk.file_path == file_path
        ]

        if not indices_to_remove:
            return 0

        # Remove chunks in reverse order to maintain indices
        for i in sorted(indices_to_remove, reverse=True):
            del self.chunks[i]

        # Rebuild embeddings array
        if self.chunks:
            self.embeddings = np.array([chunk.embedding for chunk in self.chunks])
        else:
            self.embeddings = None

        # Remove file hash
        if file_path in self.file_hashes:
            del self.file_hashes[file_path]

        return len(indices_to_remove)

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_file: Optional[str] = None
    ) -> List[Tuple[MarkdownChunk, float]]:
        """
        Search for relevant chunks using semantic similarity.

        Args:
            query: Search query
            top_k: Number of top results to return
            filter_file: Optional file path to filter results

        Returns:
            List of tuples (chunk, similarity_score)
        """
        if not self.chunks or self.embeddings is None:
            return []

        # Generate query embedding
        query_embedding = self.model.encode([query])[0]

        # Calculate cosine similarities
        similarities = self._cosine_similarity(query_embedding, self.embeddings)

        # Filter by file if specified
        if filter_file:
            indices = [
                i for i, chunk in enumerate(self.chunks)
                if chunk.file_path == filter_file
            ]
        else:
            indices = list(range(len(self.chunks)))

        # Get top-k results
        filtered_sims = [(i, similarities[i]) for i in indices]
        filtered_sims.sort(key=lambda x: x[1], reverse=True)

        # Apply threshold and limit
        results = []
        for idx, sim in filtered_sims[:top_k]:
            if sim >= self.similarity_threshold:
                results.append((self.chunks[idx], float(sim)))

        return results

    @staticmethod
    def _cosine_similarity(vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between a vector and a matrix of vectors."""
        vec_norm = vec / np.linalg.norm(vec)
        matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        return np.dot(matrix_norm, vec_norm)

    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        files = set(chunk.file_path for chunk in self.chunks)
        return {
            'total_chunks': len(self.chunks),
            'total_files': len(files),
            'files': list(files),
            'embedding_dimension': self.model.get_sentence_embedding_dimension()
        }


class MarkdownKnowledgeBase:
    """
    Main class for managing markdown knowledge base with file watching.
    """

    def __init__(
        self,
        kb_dir: str,
        model_name: str = 'all-MiniLM-L6-v2',
        chunk_config: Optional[Dict] = None
    ):
        """
        Initialize the knowledge base manager.

        Args:
            kb_dir: Directory containing markdown files
            model_name: Sentence transformer model name
            chunk_config: Configuration for chunking (min_size, max_size, overlap)
        """
        self.kb_dir = Path(kb_dir)
        if not self.kb_dir.exists():
            raise ValueError(f"Knowledge base directory does not exist: {kb_dir}")

        # Initialize components
        chunk_config = chunk_config or {}
        self.chunker = MarkdownChunker(
            min_chunk_size=chunk_config.get('min_chunk_size', 200),
            max_chunk_size=chunk_config.get('max_chunk_size', 1500),
            chunk_overlap=chunk_config.get('chunk_overlap', 100)
        )

        self.vector_kb = VectorKnowledgeBase(model_name=model_name)

        print(f"✓ Markdown Knowledge Base initialized")
        print(f"  Directory: {self.kb_dir}")

    def index_all_files(self) -> None:
        """Index all markdown files in the knowledge base directory."""
        md_files = list(self.kb_dir.rglob('*.md'))

        if not md_files:
            print(f"⚠ No markdown files found in {self.kb_dir}")
            return

        print(f"\nIndexing {len(md_files)} markdown files...")

        for md_file in md_files:
            try:
                self.index_file(str(md_file))
            except Exception as e:
                print(f"✗ Error indexing {md_file}: {e}")

        print(f"\n{'='*60}")
        print("Indexing complete!")
        stats = self.vector_kb.get_stats()
        print(f"Total files indexed: {stats['total_files']}")
        print(f"Total chunks created: {stats['total_chunks']}")
        print(f"{'='*60}\n")

    def index_file(self, file_path: str) -> None:
        """
        Index a single markdown file.

        Args:
            file_path: Path to the markdown file
        """
        # Parse file
        content, file_hash = MarkdownParser.parse_file(file_path)

        # Check if file has changed
        if file_path in self.vector_kb.file_hashes:
            if self.vector_kb.file_hashes[file_path] == file_hash:
                print(f"  ⊙ Skipping {Path(file_path).name} (unchanged)")
                return
            else:
                # File changed, remove old chunks
                removed = self.vector_kb.remove_file_chunks(file_path)
                print(f"  ↻ Re-indexing {Path(file_path).name} ({removed} old chunks removed)")
        else:
            print(f"  + Indexing {Path(file_path).name}")

        # Chunk the content
        chunks = self.chunker.chunk_by_sections(file_path, content, file_hash)

        # Add to vector knowledge base
        self.vector_kb.add_chunks(chunks)

    def check_for_updates(self) -> Set[str]:
        """
        Check all markdown files for updates and re-index if needed.

        Returns:
            Set of file paths that were updated
        """
        md_files = list(self.kb_dir.rglob('*.md'))
        updated_files = set()

        print("\nChecking for updates...")

        for md_file in md_files:
            file_path = str(md_file)
            try:
                _, current_hash = MarkdownParser.parse_file(file_path)

                # Check if file is new or changed
                if file_path not in self.vector_kb.file_hashes:
                    self.index_file(file_path)
                    updated_files.add(file_path)
                elif self.vector_kb.file_hashes[file_path] != current_hash:
                    self.index_file(file_path)
                    updated_files.add(file_path)
            except Exception as e:
                print(f"✗ Error checking {md_file}: {e}")

        # Check for deleted files
        indexed_files = set(self.vector_kb.file_hashes.keys())
        current_files = set(str(f) for f in md_files)
        deleted_files = indexed_files - current_files

        for deleted_file in deleted_files:
            removed = self.vector_kb.remove_file_chunks(deleted_file)
            print(f"  - Removed {Path(deleted_file).name} ({removed} chunks)")
            updated_files.add(deleted_file)

        if updated_files:
            print(f"✓ Updated {len(updated_files)} files")
        else:
            print("✓ No updates found")

        return updated_files

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_file: Optional[str] = None
    ) -> List[Tuple[MarkdownChunk, float]]:
        """
        Search the knowledge base.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_file: Optional file path to filter results

        Returns:
            List of (chunk, similarity_score) tuples
        """
        return self.vector_kb.search(query, top_k, filter_file)

    def get_stats(self) -> Dict:
        """Get knowledge base statistics."""
        return self.vector_kb.get_stats()

"""
Simple Knowledge Base Manager for Markdown files
Handles indexing and semantic search of markdown documents
"""

from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import numpy as np


@dataclass
class DocumentChunk:
    """A chunk of text from a document"""
    file_path: str
    content: str
    embedding: np.ndarray = None


class KnowledgeBase:
    """Simple knowledge base for markdown files"""

    def __init__(self, kb_dir: str):
        self.kb_dir = Path(kb_dir)
        self.kb_dir.mkdir(exist_ok=True, parents=True)

        # Use a lightweight embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks: List[DocumentChunk] = []

    def index_files(self):
        """Index all markdown files in the knowledge base directory"""
        self.chunks = []

        # Find all markdown files
        md_files = list(self.kb_dir.glob("*.md"))

        if not md_files:
            return

        # Read and chunk each file
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple chunking: split by paragraphs
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

            for paragraph in paragraphs:
                if len(paragraph) > 50:  # Skip very short chunks
                    chunk = DocumentChunk(
                        file_path=str(md_file),
                        content=paragraph
                    )
                    self.chunks.append(chunk)

        # Create embeddings for all chunks
        if self.chunks:
            texts = [chunk.content for chunk in self.chunks]
            embeddings = self.model.encode(texts, show_progress_bar=False)

            for chunk, embedding in zip(self.chunks, embeddings):
                chunk.embedding = embedding

    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """Search for relevant chunks using semantic similarity"""
        if not self.chunks:
            return []

        # Encode query
        query_embedding = self.model.encode([query], show_progress_bar=False)[0]

        # Calculate similarity scores
        scores = []
        for chunk in self.chunks:
            # Cosine similarity
            similarity = np.dot(query_embedding, chunk.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(chunk.embedding)
            )
            scores.append((chunk, float(similarity)))

        # Sort by score and return top k
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def get_stats(self):
        """Get knowledge base statistics"""
        files = list(set([chunk.file_path for chunk in self.chunks]))
        return {
            'total_files': len(files),
            'total_chunks': len(self.chunks),
            'files': files
        }

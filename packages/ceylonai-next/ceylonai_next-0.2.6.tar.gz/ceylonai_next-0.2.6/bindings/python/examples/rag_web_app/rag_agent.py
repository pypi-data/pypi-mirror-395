"""
Simple RAG Agent for question answering
Uses knowledge base for context and LLM for generation
"""

from typing import Dict
from kb_manager import KnowledgeBase
from ceylonai_next import LlmAgent


class RAGAgent:
    """Simple RAG agent for Q&A"""

    def __init__(self, knowledge_base: KnowledgeBase, ollama_model: str = "gemma3:latest"):
        self.kb = knowledge_base

        # Create LLM agent with Ollama
        self.llm = LlmAgent("rag-agent", f"ollama::{ollama_model}")
        self.llm.with_system_prompt(
            "You are a helpful assistant. Answer questions based on the provided context. "
            "If the context doesn't contain relevant information, say so."
        )
        self.llm.build()

    def answer(self, question: str) -> Dict:
        """Answer a question using RAG"""
        # Search knowledge base
        results = self.kb.search(question, top_k=3)

        if not results:
            return {
                'answer': "I don't have any information to answer this question.",
                'sources': []
            }

        # Build context from search results
        context = "\n\n".join([
            f"Source {i+1}:\n{chunk.content}"
            for i, (chunk, score) in enumerate(results)
        ])

        # Create prompt
        prompt = f"""Context:
{context}

Question: {question}

Answer based on the context above:"""

        # Get answer from LLM
        answer = self.llm.send_message(prompt)

        # Prepare sources
        sources = [
            {
                'file': chunk.file_path.split('/')[-1],
                'score': score
            }
            for chunk, score in results
        ]

        return {
            'answer': answer,
            'sources': sources
        }

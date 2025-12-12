"""
RAG Agent for Markdown Q&A Generation

This module provides an intelligent RAG agent that:
- Searches markdown knowledge base for relevant information
- Generates comprehensive answers using LLM
- Creates markdown Q&A files with proper citations
- Maintains conversation history and context
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from datetime import datetime
import asyncio

from ceylonai_next import LocalMesh, LlmAgent, LlmConfig
from markdown_kb_manager import MarkdownKnowledgeBase, MarkdownChunk


class MarkdownRAGAgent:
    """
    RAG Agent that answers questions using markdown knowledge base
    and generates structured markdown Q&A files.
    """

    def __init__(
        self,
        knowledge_base: MarkdownKnowledgeBase,
        llm_config: Optional[LlmConfig] = None,
        output_dir: str = "./qa_output",
        top_k_results: int = 5,
        include_code_blocks: bool = True
    ):
        """
        Initialize the RAG agent.

        Args:
            knowledge_base: MarkdownKnowledgeBase instance
            llm_config: LLM configuration (defaults to Claude)
            output_dir: Directory to save Q&A markdown files
            top_k_results: Number of chunks to retrieve for context
            include_code_blocks: Whether to include code blocks in context
        """
        self.kb = knowledge_base
        self.top_k = top_k_results
        self.include_code_blocks = include_code_blocks

        # Create output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Initialize LLM
        if llm_config is None:
            # Default to Claude (Anthropic) - check for API key
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable not set. "
                    "Please set it or provide a custom LlmConfig."
                )
            llm_config = LlmConfig.anthropic(api_key=api_key, model="claude-3-5-sonnet-20241022")

        # Create mesh and agent
        self.mesh = LocalMesh()
        self.agent = LlmAgent(
            agent_id="markdown-rag-agent",
            mesh=self.mesh,
            llm_config=llm_config
        )

        # Conversation history
        self.qa_history: List[Dict] = []

        print(f"✓ RAG Agent initialized")
        print(f"  LLM Provider: {llm_config.provider}")
        print(f"  Output directory: {self.output_dir}")

    def retrieve_context(
        self,
        query: str,
        filter_file: Optional[str] = None
    ) -> Tuple[str, List[Tuple[MarkdownChunk, float]]]:
        """
        Retrieve relevant context from knowledge base.

        Args:
            query: User query
            filter_file: Optional file path to filter results

        Returns:
            Tuple of (formatted_context, list of (chunk, score) tuples)
        """
        # Search knowledge base
        results = self.kb.search(query, top_k=self.top_k, filter_file=filter_file)

        if not results:
            return "No relevant information found in the knowledge base.", []

        # Format context for LLM
        context_parts = []
        for i, (chunk, score) in enumerate(results, 1):
            # Create section header
            heading_str = " > ".join(chunk.heading_path) if chunk.heading_path else "Content"
            file_name = Path(chunk.file_path).name

            context_parts.append(f"## Source {i} (Relevance: {score:.2f})")
            context_parts.append(f"**File:** `{file_name}`")
            context_parts.append(f"**Section:** {heading_str}")
            context_parts.append(f"**Section Number:** {chunk.section_number}")
            context_parts.append("")
            context_parts.append(chunk.content)

            # Add code blocks if enabled and present
            if self.include_code_blocks and chunk.code_blocks:
                context_parts.append("")
                context_parts.append("**Code Examples:**")
                for code_block in chunk.code_blocks:
                    context_parts.append(f"```{code_block['language']}")
                    context_parts.append(code_block['code'])
                    context_parts.append("```")

            context_parts.append("")
            context_parts.append("---")
            context_parts.append("")

        return "\n".join(context_parts), results

    def generate_answer(
        self,
        question: str,
        context: str,
        include_citations: bool = True
    ) -> str:
        """
        Generate answer using LLM with retrieved context.

        Args:
            question: User question
            context: Retrieved context from knowledge base
            include_citations: Whether to include source citations

        Returns:
            Generated answer
        """
        # Build prompt
        system_prompt = """You are a helpful AI assistant with access to a markdown knowledge base.
Your task is to answer questions based ONLY on the provided context from the knowledge base.

Guidelines:
- Provide clear, comprehensive, and accurate answers
- Use markdown formatting for better readability
- If the context contains code examples, include them in your answer when relevant
- If the question cannot be answered from the context, say so explicitly
- Do not make up information that isn't in the context
"""

        if include_citations:
            system_prompt += """- IMPORTANT: Always cite your sources using the format [Source N] where N is the source number from the context
- Include a "Sources" section at the end listing all referenced sources
"""

        user_prompt = f"""# Context from Knowledge Base

{context}

# Question

{question}

# Instructions

Please answer the question based on the context provided above. Provide a comprehensive answer with proper citations."""

        # Send to LLM
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = self.agent.send_message(full_prompt)

        return response

    async def generate_answer_async(
        self,
        question: str,
        context: str,
        include_citations: bool = True
    ) -> str:
        """
        Asynchronously generate answer using LLM.

        Args:
            question: User question
            context: Retrieved context
            include_citations: Whether to include citations

        Returns:
            Generated answer
        """
        # Build prompt (same as sync version)
        system_prompt = """You are a helpful AI assistant with access to a markdown knowledge base.
Your task is to answer questions based ONLY on the provided context from the knowledge base.

Guidelines:
- Provide clear, comprehensive, and accurate answers
- Use markdown formatting for better readability
- If the context contains code examples, include them in your answer when relevant
- If the question cannot be answered from the context, say so explicitly
- Do not make up information that isn't in the context
"""

        if include_citations:
            system_prompt += """- IMPORTANT: Always cite your sources using the format [Source N] where N is the source number from the context
- Include a "Sources" section at the end listing all referenced sources
"""

        user_prompt = f"""# Context from Knowledge Base

{context}

# Question

{question}

# Instructions

Please answer the question based on the context provided above. Provide a comprehensive answer with proper citations."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = await self.agent.send_message_async(full_prompt)

        return response

    def answer_question(
        self,
        question: str,
        filter_file: Optional[str] = None,
        save_to_file: bool = True,
        file_name: Optional[str] = None
    ) -> Dict:
        """
        Answer a question using RAG and optionally save to markdown file.

        Args:
            question: User question
            filter_file: Optional file path to filter search results
            save_to_file: Whether to save Q&A to markdown file
            file_name: Custom file name (auto-generated if None)

        Returns:
            Dictionary containing question, answer, sources, and file path
        """
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")

        # Step 1: Retrieve context
        print("🔍 Searching knowledge base...")
        context, sources = self.retrieve_context(question, filter_file)

        if not sources:
            print("⚠ No relevant sources found")
            answer = "I couldn't find relevant information in the knowledge base to answer this question."
        else:
            print(f"✓ Found {len(sources)} relevant sources")

            # Step 2: Generate answer
            print("🤖 Generating answer...")
            answer = self.generate_answer(question, context, include_citations=True)
            print("✓ Answer generated")

        # Step 3: Create Q&A record
        qa_record = {
            'question': question,
            'answer': answer,
            'sources': [
                {
                    'file': chunk.file_path,
                    'section': ' > '.join(chunk.heading_path),
                    'section_number': chunk.section_number,
                    'relevance': float(score)
                }
                for chunk, score in sources
            ],
            'timestamp': datetime.now().isoformat(),
            'file_path': None
        }

        # Step 4: Save to markdown file if requested
        if save_to_file:
            file_path = self.save_qa_to_markdown(qa_record, file_name)
            qa_record['file_path'] = str(file_path)
            print(f"💾 Saved to: {file_path}")

        # Add to history
        self.qa_history.append(qa_record)

        print(f"\n{'='*60}\n")

        return qa_record

    async def answer_question_async(
        self,
        question: str,
        filter_file: Optional[str] = None,
        save_to_file: bool = True,
        file_name: Optional[str] = None
    ) -> Dict:
        """
        Asynchronously answer a question using RAG.

        Args:
            question: User question
            filter_file: Optional file path to filter search results
            save_to_file: Whether to save Q&A to markdown file
            file_name: Custom file name

        Returns:
            Dictionary containing question, answer, sources, and file path
        """
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")

        # Retrieve context (synchronous - embedding search)
        print("🔍 Searching knowledge base...")
        context, sources = self.retrieve_context(question, filter_file)

        if not sources:
            print("⚠ No relevant sources found")
            answer = "I couldn't find relevant information in the knowledge base to answer this question."
        else:
            print(f"✓ Found {len(sources)} relevant sources")

            # Generate answer asynchronously
            print("🤖 Generating answer...")
            answer = await self.generate_answer_async(question, context, include_citations=True)
            print("✓ Answer generated")

        # Create Q&A record
        qa_record = {
            'question': question,
            'answer': answer,
            'sources': [
                {
                    'file': chunk.file_path,
                    'section': ' > '.join(chunk.heading_path),
                    'section_number': chunk.section_number,
                    'relevance': float(score)
                }
                for chunk, score in sources
            ],
            'timestamp': datetime.now().isoformat(),
            'file_path': None
        }

        # Save to markdown file if requested
        if save_to_file:
            file_path = self.save_qa_to_markdown(qa_record, file_name)
            qa_record['file_path'] = str(file_path)
            print(f"💾 Saved to: {file_path}")

        # Add to history
        self.qa_history.append(qa_record)

        print(f"\n{'='*60}\n")

        return qa_record

    def save_qa_to_markdown(
        self,
        qa_record: Dict,
        file_name: Optional[str] = None
    ) -> Path:
        """
        Save Q&A to a markdown file.

        Args:
            qa_record: Q&A record dictionary
            file_name: Custom file name (auto-generated if None)

        Returns:
            Path to the saved file
        """
        if file_name is None:
            # Generate file name from question
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            question_slug = self._slugify(qa_record['question'][:50])
            file_name = f"qa_{timestamp}_{question_slug}.md"

        file_path = self.output_dir / file_name

        # Build markdown content
        lines = []
        lines.append(f"# Q&A: {qa_record['question']}")
        lines.append("")
        lines.append(f"**Generated:** {qa_record['timestamp']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## Question")
        lines.append("")
        lines.append(qa_record['question'])
        lines.append("")

        lines.append("## Answer")
        lines.append("")
        lines.append(qa_record['answer'])
        lines.append("")

        # Add sources section if available
        if qa_record['sources']:
            lines.append("## Knowledge Base Sources")
            lines.append("")
            lines.append("The following sources from the knowledge base were used to generate this answer:")
            lines.append("")

            for i, source in enumerate(qa_record['sources'], 1):
                file_name_display = Path(source['file']).name
                lines.append(f"### Source {i} (Relevance: {source['relevance']:.2f})")
                lines.append("")
                lines.append(f"- **File:** `{file_name_display}`")
                lines.append(f"- **Section:** {source['section']}")
                lines.append(f"- **Section Number:** {source['section_number']}")
                lines.append("")

        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return file_path

    async def answer_multiple_questions_async(
        self,
        questions: List[str],
        save_to_file: bool = True
    ) -> List[Dict]:
        """
        Answer multiple questions concurrently using async.

        Args:
            questions: List of questions
            save_to_file: Whether to save each Q&A to markdown

        Returns:
            List of Q&A records
        """
        print(f"\n🚀 Answering {len(questions)} questions concurrently...\n")

        tasks = [
            self.answer_question_async(q, save_to_file=save_to_file)
            for q in questions
        ]

        results = await asyncio.gather(*tasks)

        print(f"✓ All {len(questions)} questions answered!")

        return list(results)

    def export_qa_history(self, file_path: str) -> None:
        """
        Export all Q&A history to a single markdown file.

        Args:
            file_path: Path to save the export
        """
        lines = []
        lines.append("# Q&A History")
        lines.append("")
        lines.append(f"**Exported:** {datetime.now().isoformat()}")
        lines.append(f"**Total Q&As:** {len(self.qa_history)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, qa in enumerate(self.qa_history, 1):
            lines.append(f"## Q&A #{i}")
            lines.append("")
            lines.append(f"**Timestamp:** {qa['timestamp']}")
            lines.append("")

            lines.append(f"### Question")
            lines.append("")
            lines.append(qa['question'])
            lines.append("")

            lines.append(f"### Answer")
            lines.append("")
            lines.append(qa['answer'])
            lines.append("")

            if qa['sources']:
                lines.append(f"### Sources ({len(qa['sources'])})")
                for j, source in enumerate(qa['sources'], 1):
                    lines.append(f"{j}. `{Path(source['file']).name}` - {source['section']} (Relevance: {source['relevance']:.2f})")
                lines.append("")

            if qa.get('file_path'):
                lines.append(f"**Saved to:** `{qa['file_path']}`")
                lines.append("")

            lines.append("---")
            lines.append("")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"✓ Exported Q&A history to: {file_path}")

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to a valid file name slug."""
        # Replace non-alphanumeric characters with underscores
        slug = ''.join(c if c.isalnum() else '_' for c in text)
        # Remove consecutive underscores
        slug = '_'.join(filter(None, slug.split('_')))
        return slug.lower()


# Convenience function for quick Q&A
def quick_answer(
    knowledge_base_dir: str,
    question: str,
    llm_config: Optional[LlmConfig] = None,
    output_dir: str = "./qa_output"
) -> str:
    """
    Quick function to get an answer from a markdown knowledge base.

    Args:
        knowledge_base_dir: Directory containing markdown files
        question: Question to answer
        llm_config: Optional LLM configuration
        output_dir: Directory to save Q&A file

    Returns:
        Generated answer
    """
    # Initialize knowledge base
    print("Initializing knowledge base...")
    kb = MarkdownKnowledgeBase(knowledge_base_dir)
    kb.index_all_files()

    # Create RAG agent
    agent = MarkdownRAGAgent(kb, llm_config=llm_config, output_dir=output_dir)

    # Get answer
    result = agent.answer_question(question, save_to_file=True)

    return result['answer']

#!/usr/bin/env python3
"""
Notebook Agent - AI agent that helps users create and fill Jupyter notebooks

This agent can:
- Load and analyze existing notebooks
- Guide users through filling notebook cells
- Add/modify/delete cells
- Provide suggestions for code and markdown
"""

import os
import sys
from typing import Optional, Dict, Any

# Add parent directory to path to import ceylon
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ceylonai_next import LlmAgent, ReActConfig
from notebook_manager import NotebookManager, CellType


class NotebookAgent:
    """Agent that helps users work with Jupyter notebooks"""

    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.2:latest",
        notebook_path: Optional[str] = None
    ):
        """
        Initialize the notebook agent

        Args:
            provider: LLM provider (openai, anthropic, ollama, etc.)
            model: Model name
            notebook_path: Path to existing notebook or None for new
        """
        self.provider = provider
        self.model = model
        self.notebook_manager = NotebookManager(notebook_path)

        # Initialize LLM agent
        model_string = f"{provider}::{model}"
        self.agent = LlmAgent("notebook_assistant", model_string)

        # Configure agent with system prompt
        system_prompt = self._create_system_prompt()
        self.agent.with_system_prompt(system_prompt)
        self.agent.with_temperature(0.7)
        self.agent.with_max_tokens(1000)

        self.agent = self.agent.build()

        # Configure ReAct for multi-step reasoning
        react_config = ReActConfig().with_max_iterations(5)
        self.agent.with_react(react_config)

        # Build the agent
        self.agent.build()

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the agent"""
        return """You are a helpful AI assistant that guides users in creating and filling Jupyter notebooks.

Your capabilities:
- Analyze notebook structure and content
- Suggest code and markdown for cells
- Help users understand what to add to empty cells
- Provide explanations for data analysis workflows
- Guide users through data science and ML tasks

When helping users:
1. Ask clarifying questions if the request is ambiguous
2. Provide clear, concise code examples
3. Explain the purpose of each cell
4. Follow best practices for notebook organization
5. Suggest markdown cells for documentation

You should be conversational and friendly while being technically accurate."""

    def load_notebook(self, notebook_path: str) -> str:
        """Load an existing notebook"""
        try:
            self.notebook_manager.load(notebook_path)
            return f"✓ Loaded notebook: {notebook_path}\n{self.notebook_manager.get_structure()}"
        except Exception as e:
            return f"✗ Error loading notebook: {str(e)}"

    def create_notebook(self, title: str = "New Notebook", save_path: Optional[str] = None) -> str:
        """Create a new notebook"""
        try:
            self.notebook_manager.create_new(title)
            if save_path:
                self.notebook_manager.notebook_path = save_path
                self.notebook_manager.save()
                return f"✓ Created new notebook: {save_path}"
            return f"✓ Created new notebook in memory: {title}"
        except Exception as e:
            return f"✗ Error creating notebook: {str(e)}"

    def save_notebook(self, path: Optional[str] = None) -> str:
        """Save the current notebook"""
        try:
            self.notebook_manager.save(path)
            save_path = path or self.notebook_manager.notebook_path
            return f"✓ Saved notebook: {save_path}"
        except Exception as e:
            return f"✗ Error saving notebook: {str(e)}"

    def add_code_cell(self, code: str, position: Optional[int] = None) -> str:
        """Add a code cell to the notebook"""
        try:
            idx = self.notebook_manager.add_cell(CellType.CODE, code, position)
            return f"✓ Added code cell at position {idx}"
        except Exception as e:
            return f"✗ Error adding code cell: {str(e)}"

    def add_markdown_cell(self, markdown: str, position: Optional[int] = None) -> str:
        """Add a markdown cell to the notebook"""
        try:
            idx = self.notebook_manager.add_cell(CellType.MARKDOWN, markdown, position)
            return f"✓ Added markdown cell at position {idx}"
        except Exception as e:
            return f"✗ Error adding markdown cell: {str(e)}"

    def update_cell(self, index: int, content: str) -> str:
        """Update a cell's content"""
        try:
            self.notebook_manager.update_cell(index, content)
            return f"✓ Updated cell {index}"
        except Exception as e:
            return f"✗ Error updating cell: {str(e)}"

    def delete_cell(self, index: int) -> str:
        """Delete a cell"""
        try:
            self.notebook_manager.delete_cell(index)
            return f"✓ Deleted cell {index}"
        except Exception as e:
            return f"✗ Error deleting cell: {str(e)}"

    def get_notebook_info(self) -> str:
        """Get information about the current notebook"""
        if not self.notebook_manager.cells:
            return "No notebook loaded. Create or load a notebook first."

        return self.notebook_manager.get_structure()

    def get_cell_content(self, index: int) -> str:
        """Get the content of a specific cell"""
        cell = self.notebook_manager.get_cell(index)
        if cell:
            return f"Cell {index} ({cell.cell_type.value}):\n{cell.source}"
        return f"Cell {index} not found"

    def analyze_notebook(self) -> Dict[str, Any]:
        """Analyze the notebook and provide insights"""
        if not self.notebook_manager.cells:
            return {"error": "No notebook loaded"}

        empty_cells = self.notebook_manager.find_empty_cells()
        cell_counts = self.notebook_manager.count_by_type()

        return {
            "total_cells": len(self.notebook_manager.cells),
            "cell_counts": cell_counts,
            "empty_cells": empty_cells,
            "empty_count": len(empty_cells),
            "notebook_path": self.notebook_manager.notebook_path
        }

    def chat(self, user_message: str, include_notebook_context: bool = True) -> str:
        """
        Chat with the agent about the notebook

        Args:
            user_message: User's message
            include_notebook_context: Whether to include current notebook state in context

        Returns:
            Agent's response
        """
        # Build context with notebook information if requested
        context = ""
        if include_notebook_context and self.notebook_manager.cells:
            analysis = self.analyze_notebook()
            context = f"\n\n[Current Notebook Context]\n"
            context += f"Total cells: {analysis['total_cells']}\n"
            context += f"Cell types: {analysis['cell_counts']}\n"
            context += f"Empty cells at positions: {analysis['empty_cells']}\n"
            context += f"\nNotebook structure:\n{self.notebook_manager.get_structure()}\n"

        # Combine user message with context
        full_message = user_message
        if context:
            full_message = f"{user_message}\n{context}"

        # Send message to agent
        try:
            response = self.agent.send_message(full_message)
            return response
        except Exception as e:
            return f"Error communicating with agent: {str(e)}"

    def suggest_next_steps(self) -> str:
        """Get suggestions for what to do next with the notebook"""
        if not self.notebook_manager.cells:
            return "Start by creating a new notebook or loading an existing one."

        analysis = self.analyze_notebook()

        suggestions = ["📝 Suggestions for your notebook:\n"]

        if analysis['empty_count'] > 0:
            suggestions.append(
                f"- You have {analysis['empty_count']} empty cell(s) at position(s) "
                f"{analysis['empty_cells']}. What would you like to add?"
            )

        if analysis['cell_counts']['markdown'] == 0:
            suggestions.append(
                "- Consider adding markdown cells to document your analysis"
            )

        if analysis['total_cells'] < 3:
            suggestions.append(
                "- Your notebook is quite small. What analysis would you like to perform?"
            )

        return "\n".join(suggestions)

    def get_notebook_content(self) -> str:
        """Get the full content of the notebook"""
        if not self.notebook_manager.cells:
            return "No notebook loaded."

        return self.notebook_manager.get_content_summary()


def demo():
    """Demo of the notebook agent"""
    print("=== Notebook Agent Demo ===\n")

    # Create agent
    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")

    # Create a new notebook
    print(agent.create_notebook("Data Analysis Demo"))

    # Add some cells
    print(agent.add_markdown_cell("# Data Analysis Notebook\n\nThis notebook analyzes sales data."))
    print(agent.add_code_cell("import pandas as pd\nimport numpy as np"))
    print(agent.add_code_cell("# TODO: Load the data"))

    # Show notebook info
    print("\n" + agent.get_notebook_info())

    # Chat with agent about filling empty cells
    print("\n=== Chatting with agent ===")
    response = agent.chat("I have a CSV file with sales data. How should I load it?")
    print(f"Agent: {response}")

    # Get suggestions
    print("\n" + agent.suggest_next_steps())


if __name__ == "__main__":
    demo()

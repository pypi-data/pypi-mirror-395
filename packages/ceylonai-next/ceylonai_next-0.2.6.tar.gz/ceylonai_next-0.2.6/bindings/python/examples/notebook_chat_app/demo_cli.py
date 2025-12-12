#!/usr/bin/env python3
"""
CLI Demo - Notebook Chat Assistant

This demo shows programmatic usage of the Notebook Agent without the UI.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from notebook_agent import NotebookAgent
from notebook_manager import CellType


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_create_notebook():
    """Demo: Create a new notebook from scratch"""
    print_section("Demo 1: Create New Notebook")

    # Create agent
    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")

    # Create notebook
    print("Creating new notebook...")
    result = agent.create_notebook(
        title="Sales Analysis",
        save_path="sales_analysis.ipynb"
    )
    print(result)

    # Add markdown title
    print("\nAdding title cell...")
    result = agent.add_markdown_cell("# Sales Data Analysis\n\nAnalyzing Q4 2024 sales data.")
    print(result)

    # Add imports
    print("\nAdding import cell...")
    imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')"""
    result = agent.add_code_cell(imports)
    print(result)

    # Add data loading section
    print("\nAdding data loading section...")
    agent.add_markdown_cell("## Load Data")
    agent.add_code_cell("# TODO: Load sales data from CSV")

    # Show notebook structure
    print("\n" + agent.get_notebook_info())

    # Save
    print("\nSaving notebook...")
    result = agent.save_notebook()
    print(result)

    return agent


def demo_chat_guidance():
    """Demo: Chat with agent for guidance"""
    print_section("Demo 2: Chat for Guidance")

    # Create agent with sample notebook
    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")
    agent.load_notebook("sample_notebook.ipynb")

    print("Loaded sample notebook:")
    print(agent.get_notebook_info())

    # Ask for help with empty cells
    print("\n📝 User: I have empty cells with TODOs. How should I fill them?")
    print("\n🤖 Agent:")
    response = agent.chat("I have empty cells with TODOs. How should I fill them?")
    print(response)

    # Ask for specific help
    print("\n\n📝 User: Help me write code to load a CSV file")
    print("\n🤖 Agent:")
    response = agent.chat("Help me write code to load a CSV file named 'sales_data.csv'")
    print(response)

    return agent


def demo_analyze_notebook():
    """Demo: Analyze existing notebook"""
    print_section("Demo 3: Analyze Notebook")

    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")
    agent.load_notebook("sample_notebook.ipynb")

    # Get analysis
    print("Analyzing notebook...")
    analysis = agent.analyze_notebook()

    print(f"Total cells: {analysis['total_cells']}")
    print(f"Cell types: {analysis['cell_counts']}")
    print(f"Empty cells: {analysis['empty_count']} at positions {analysis['empty_cells']}")

    # Get suggestions
    print("\n" + agent.suggest_next_steps())

    # Show full content
    print("\n" + "-" * 60)
    print("Full notebook content:")
    print("-" * 60)
    print(agent.get_notebook_content())

    return agent


def demo_modify_cells():
    """Demo: Modify notebook cells"""
    print_section("Demo 4: Modify Cells")

    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")
    agent.create_notebook("Test Notebook")

    # Add some cells
    print("Adding cells...")
    agent.add_markdown_cell("# Test Notebook")
    agent.add_code_cell("print('Hello')")
    agent.add_code_cell("# Empty cell")

    print("\nInitial state:")
    print(agent.get_notebook_info())

    # Update a cell
    print("\nUpdating cell 1...")
    agent.update_cell(1, "print('Hello, World!')\nprint('Updated!')")
    print(agent.get_cell_content(1))

    # Delete a cell
    print("\nDeleting cell 2...")
    agent.delete_cell(2)

    print("\nFinal state:")
    print(agent.get_notebook_info())

    return agent


def interactive_chat():
    """Interactive chat mode"""
    print_section("Interactive Chat Mode")

    print("Starting interactive chat...")
    print("Commands:")
    print("  /load <path>  - Load notebook")
    print("  /new <title>  - Create new notebook")
    print("  /save [path]  - Save notebook")
    print("  /info         - Show notebook info")
    print("  /quit         - Exit")
    print()

    agent = NotebookAgent(provider="ollama", model="llama3.2:latest")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input == "/quit":
                print("Goodbye!")
                break

            elif user_input.startswith("/load "):
                path = user_input[6:].strip()
                result = agent.load_notebook(path)
                print(f"\n{result}\n")

            elif user_input.startswith("/new "):
                title = user_input[5:].strip()
                result = agent.create_notebook(title)
                print(f"\n{result}\n")

            elif user_input.startswith("/save"):
                parts = user_input.split(maxsplit=1)
                path = parts[1] if len(parts) > 1 else None
                result = agent.save_notebook(path)
                print(f"\n{result}\n")

            elif user_input == "/info":
                print(f"\n{agent.get_notebook_info()}\n")

            else:
                # Chat with agent
                response = agent.chat(user_input)
                print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    """Main demo"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║          📓 Notebook Chat Assistant - CLI Demo            ║
    ║                                                            ║
    ║    An AI-powered tool for creating Jupyter notebooks      ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
        return

    print("\nRunning demos...\n")
    print("Note: Make sure Ollama is running with llama3.2 model")
    print("      Or modify the model in the code\n")

    try:
        # Run demos
        demo_create_notebook()
        input("\nPress Enter to continue to next demo...")

        demo_chat_guidance()
        input("\nPress Enter to continue to next demo...")

        demo_analyze_notebook()
        input("\nPress Enter to continue to next demo...")

        demo_modify_cells()

        print_section("Demos Complete")
        print("To try interactive mode, run:")
        print("  python demo_cli.py --interactive")
        print()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError running demo: {e}")
        print("\nMake sure:")
        print("1. Ceylon framework is installed")
        print("2. Ollama is running (or change the model)")
        print("3. Required model is pulled (ollama pull llama3.2)")


if __name__ == "__main__":
    main()

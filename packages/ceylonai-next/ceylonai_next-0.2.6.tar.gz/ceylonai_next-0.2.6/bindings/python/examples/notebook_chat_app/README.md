# 📓 Notebook Chat Assistant

An AI-powered application that helps you create and fill Jupyter notebooks through interactive chat.

## Features

### 🤖 AI-Powered Guidance
- Chat with an intelligent agent that understands notebook structure
- Get suggestions for code and markdown content
- Receive guidance on best practices for data analysis workflows
- Multi-step reasoning with ReAct framework

### 📝 Notebook Management
- Load existing `.ipynb` files
- Create new notebooks from scratch
- Add, edit, and delete cells
- Save and download notebooks
- Preview notebook content in real-time

### ⚙️ Model Configuration
- Support for multiple LLM providers:
  - **Ollama** (local models like Llama, Gemma, Mistral)
  - **OpenAI** (GPT-3.5, GPT-4)
  - **Anthropic** (Claude)
  - **Google Gemini**
  - And more...
- Add custom models from settings panel
- Switch between models on-the-fly

### 💬 Interactive Chat
- Natural language conversation about your notebook
- Context-aware responses (agent knows your notebook state)
- Ask questions like:
  - "How should I load a CSV file?"
  - "What visualization would work best for this data?"
  - "Help me fill the empty cells in my notebook"
  - "How do I handle missing values?"

## Installation

### 1. Prerequisites

Make sure you have Python 3.8+ installed.

### 2. Install Ceylon Framework

From the repository root:

```bash
cd bindings/python
pip install -e .
```

### 3. Install Dependencies

```bash
cd examples/notebook_chat_app
pip install -r requirements.txt
```

### 4. Setup LLM Provider

#### Option A: Ollama (Recommended for Local)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama3.2
   # or
   ollama pull gemma2
   ```

#### Option B: OpenAI

Set your API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

#### Option C: Anthropic

Set your API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

### Running the Application

```bash
cd examples/notebook_chat_app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Quick Start Guide

1. **Configure Model** (Sidebar)
   - Select your preferred model from the dropdown
   - Or add a new model using the "Manage Models" section

2. **Create or Load Notebook**
   - Click "📝 New Notebook" to start fresh
   - Or use "📂 Load Notebook" to upload an existing `.ipynb` file
   - Try loading `sample_notebook.ipynb` to see the demo

3. **Chat with the Assistant**
   - Switch to the "💬 Chat" tab
   - Ask questions about your notebook
   - Request help with specific cells
   - Get code suggestions

4. **Edit Notebook**
   - Switch to the "📓 Notebook" tab to view cells
   - Use the ✏️ button to edit cells
   - Use the 🗑️ button to delete cells
   - Use "Quick Add Cell" to add new content

5. **Save Your Work**
   - Click "💾 Save Notebook" in the sidebar
   - Or "⬇️ Download Notebook" to get the file

### Example Interactions

**Example 1: Getting Started**
```
User: I want to analyze sales data. How should I start?

Agent: Great! Let's structure your analysis notebook. I recommend:
1. Import libraries (pandas, numpy, matplotlib)
2. Load your CSV data
3. Explore with df.head() and df.describe()
4. Clean any missing values
5. Create visualizations
6. Perform your analysis

Would you like me to help you add these sections?
```

**Example 2: Filling Empty Cells**
```
User: I have a cell that says "TODO: Load your CSV data here".
      What code should I put there?

Agent: Here's how to load a CSV file:

import pandas as pd
df = pd.read_csv('your_file.csv')

# Display basic info
print(f"Shape: {df.shape}")
print(df.head())

Replace 'your_file.csv' with your actual filename.
```

**Example 3: Data Cleaning**
```
User: How do I handle missing values?

Agent: Here are several strategies for handling missing values:

# Check for missing values
df.isnull().sum()

# Option 1: Drop rows with missing values
df_clean = df.dropna()

# Option 2: Fill with mean (for numeric columns)
df['column_name'].fillna(df['column_name'].mean(), inplace=True)

# Option 3: Fill with mode (for categorical)
df['category'].fillna(df['category'].mode()[0], inplace=True)

Which approach would work best for your data?
```

## Architecture

### Components

```
notebook_chat_app/
├── app.py                 # Streamlit UI application
├── notebook_agent.py      # AI agent with notebook capabilities
├── notebook_manager.py    # Notebook operations (load/save/edit)
├── sample_notebook.ipynb  # Example notebook
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### How It Works

1. **Notebook Manager** (`notebook_manager.py`)
   - Handles `.ipynb` file I/O
   - Parses JSON structure
   - Provides cell manipulation APIs
   - Manages notebook metadata

2. **Notebook Agent** (`notebook_agent.py`)
   - Built on Ceylon's `LlmAgent`
   - Uses ReAct framework for reasoning
   - Provides actions for notebook operations
   - Maintains context about notebook state

3. **Streamlit UI** (`app.py`)
   - Chat interface for user interaction
   - Notebook viewer/editor
   - Settings panel for model configuration
   - Session state management

### Agent System Prompt

The agent is configured with a specialized system prompt:

```python
"""You are a helpful AI assistant that guides users in creating
and filling Jupyter notebooks.

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
"""
```

## Advanced Features

### Model Management

Add custom models in the settings panel:

1. Click "📋 Manage Models" in the sidebar
2. Enter:
   - **Display Name**: Human-readable name
   - **Provider**: `ollama`, `openai`, `anthropic`, etc.
   - **Model**: Model identifier (e.g., `llama3.2:latest`, `gpt-4`)
3. Click "➕ Add Model"

Models are persisted in `models_config.json`.

### Custom System Prompts

To customize the agent's behavior, edit `notebook_agent.py`:

```python
def _create_system_prompt(self) -> str:
    return """Your custom prompt here..."""
```

### Context-Aware Responses

The agent includes notebook context in every chat message:

- Total number of cells
- Cell types distribution
- Empty cell positions
- Notebook structure

This allows the agent to provide relevant, specific guidance.

### ReAct Reasoning

The agent uses the ReAct (Reasoning + Acting) framework for complex queries:

```python
react_config = ReActConfig().with_max_iterations(5)
self.agent.with_react(react_config)
```

This enables multi-step reasoning for complex tasks.

## Troubleshooting

### "Error communicating with agent"

**Problem**: LLM provider not configured correctly.

**Solutions**:
- For Ollama: Ensure Ollama is running (`ollama serve`)
- For OpenAI/Anthropic: Check API keys are set
- Verify model name is correct

### "No notebook loaded"

**Problem**: Trying to chat without a notebook.

**Solution**: Create a new notebook or load an existing one first.

### Slow responses

**Problem**: Model is taking too long to respond.

**Solutions**:
- Use a smaller local model (e.g., `gemma2:2b` instead of `llama3.2:70b`)
- Reduce `max_tokens` in `notebook_agent.py`
- Check your internet connection (for cloud providers)

### Streamlit errors

**Problem**: Module not found or import errors.

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Ensure Ceylon is installed
cd ../../
pip install -e .
```

## API Reference

### NotebookManager

```python
manager = NotebookManager(notebook_path="my_notebook.ipynb")

# Load notebook
manager.load("path/to/notebook.ipynb")

# Create new notebook
manager.create_new(title="My Notebook")

# Add cells
manager.add_cell(CellType.CODE, "print('Hello')", position=0)
manager.add_cell(CellType.MARKDOWN, "# Title")

# Modify cells
manager.update_cell(0, "print('Updated')")
manager.delete_cell(0)

# Save
manager.save("output.ipynb")

# Query
structure = manager.get_structure()
empty_cells = manager.find_empty_cells()
analysis = manager.count_by_type()
```

### NotebookAgent

```python
agent = NotebookAgent(
    provider="ollama",
    model="llama3.2:latest",
    notebook_path="my_notebook.ipynb"
)

# Chat
response = agent.chat("How do I load a CSV?")

# Notebook operations
agent.add_code_cell("import pandas as pd")
agent.add_markdown_cell("# Analysis")
agent.update_cell(0, "new content")
agent.delete_cell(0)

# Analysis
info = agent.get_notebook_info()
analysis = agent.analyze_notebook()
suggestions = agent.suggest_next_steps()

# Save
agent.save_notebook()
```

## Examples

### Programmatic Usage

```python
#!/usr/bin/env python3
from notebook_agent import NotebookAgent

# Create agent
agent = NotebookAgent(provider="ollama", model="llama3.2:latest")

# Create notebook
agent.create_notebook("Data Analysis", save_path="analysis.ipynb")

# Add structure
agent.add_markdown_cell("# Data Analysis")
agent.add_code_cell("import pandas as pd\nimport numpy as np")

# Chat for guidance
response = agent.chat("I need to analyze customer churn. What should I add next?")
print(response)

# Save
agent.save_notebook()
```

### Custom Model Configuration

Create `models_config.json`:

```json
{
  "models": [
    {
      "provider": "ollama",
      "model": "codellama:latest",
      "name": "Code Llama (Local)"
    },
    {
      "provider": "openai",
      "model": "gpt-4-turbo",
      "name": "GPT-4 Turbo"
    },
    {
      "provider": "anthropic",
      "model": "claude-3-opus",
      "name": "Claude 3 Opus"
    }
  ]
}
```

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Add support for running notebook cells
- [ ] Integrate with Jupyter kernel for live execution
- [ ] Add RAG for domain-specific knowledge
- [ ] Support for collaborative editing
- [ ] Cell output preview
- [ ] Notebook templates library
- [ ] Export to different formats (PDF, HTML)

## License

Part of the Ceylon AI Framework.

## Related Examples

- `demo_react.py` - ReAct reasoning framework
- `demo_async_llm.py` - Async LLM operations
- `rag_web_app/` - RAG-based web application

## Support

For issues or questions:
- Check the [Ceylon documentation](../../docs/)
- Review existing examples in `bindings/python/examples/`
- Open an issue on GitHub

---

**Built with ❤️ using the Ceylon AI Framework**

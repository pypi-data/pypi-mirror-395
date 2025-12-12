#!/usr/bin/env python3
"""
Notebook Chat Application - Interactive UI for notebook creation with AI guidance

This Streamlit app provides:
1. Notebook loading and viewing
2. Chat interface with AI agent
3. Settings panel for model configuration
4. Cell manipulation tools
"""

import os
import sys
import json
import streamlit as st
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from notebook_agent import NotebookAgent
from notebook_manager import NotebookManager, CellType


# Page configuration
st.set_page_config(
    page_title="Notebook Chat Assistant",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_models_config():
    """Load model configurations from file"""
    config_path = Path(__file__).parent / "models_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "models": [
            {"provider": "ollama", "model": "llama3.2:latest", "name": "Llama 3.2 (Local)"},
            {"provider": "ollama", "model": "gemma2:latest", "name": "Gemma 2 (Local)"},
            {"provider": "openai", "model": "gpt-4", "name": "GPT-4"},
            {"provider": "anthropic", "model": "claude-3-sonnet", "name": "Claude 3 Sonnet"},
        ]
    }


def save_models_config(config):
    """Save model configurations to file"""
    config_path = Path(__file__).parent / "models_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'agent' not in st.session_state:
        st.session_state.agent = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'notebook_path' not in st.session_state:
        st.session_state.notebook_path = None

    if 'models_config' not in st.session_state:
        st.session_state.models_config = load_models_config()

    if 'selected_model_index' not in st.session_state:
        st.session_state.selected_model_index = 0


def render_sidebar():
    """Render the sidebar with settings and notebook controls"""
    with st.sidebar:
        st.title("⚙️ Settings")

        # Model selection
        st.subheader("🤖 Model Configuration")

        models = st.session_state.models_config['models']
        model_names = [m['name'] for m in models]

        selected = st.selectbox(
            "Select Model",
            range(len(model_names)),
            format_func=lambda i: model_names[i],
            index=st.session_state.selected_model_index
        )

        if selected != st.session_state.selected_model_index:
            st.session_state.selected_model_index = selected
            st.session_state.agent = None  # Reset agent with new model

        # Show model details
        current_model = models[selected]
        st.info(f"Provider: `{current_model['provider']}`\nModel: `{current_model['model']}`")

        # Model management
        with st.expander("📋 Manage Models"):
            st.write("Add new model:")

            new_name = st.text_input("Display Name", key="new_model_name")
            new_provider = st.text_input("Provider", "ollama", key="new_provider")
            new_model = st.text_input("Model", "llama3.2:latest", key="new_model")

            if st.button("➕ Add Model"):
                if new_name and new_provider and new_model:
                    models.append({
                        "provider": new_provider,
                        "model": new_model,
                        "name": new_name
                    })
                    save_models_config(st.session_state.models_config)
                    st.success(f"Added {new_name}")
                    st.rerun()

            st.divider()
            st.write("Remove models:")
            for i, model in enumerate(models):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(model['name'])
                with col2:
                    if st.button("🗑️", key=f"delete_{i}"):
                        if len(models) > 1:
                            models.pop(i)
                            save_models_config(st.session_state.models_config)
                            st.rerun()
                        else:
                            st.error("Must have at least one model")

        st.divider()

        # Notebook operations
        st.subheader("📓 Notebook")

        # Create new notebook
        if st.button("📝 New Notebook"):
            new_path = st.text_input("Save as:", "my_notebook.ipynb")
            if new_path:
                if st.session_state.agent is None:
                    model_config = models[st.session_state.selected_model_index]
                    st.session_state.agent = NotebookAgent(
                        provider=model_config['provider'],
                        model=model_config['model']
                    )
                result = st.session_state.agent.create_notebook(save_path=new_path)
                st.success(result)
                st.session_state.notebook_path = new_path

        # Load existing notebook
        uploaded_file = st.file_uploader("📂 Load Notebook", type=['ipynb'])
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = Path(__file__).parent / uploaded_file.name
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            if st.session_state.agent is None:
                model_config = models[st.session_state.selected_model_index]
                st.session_state.agent = NotebookAgent(
                    provider=model_config['provider'],
                    model=model_config['model']
                )

            result = st.session_state.agent.load_notebook(str(temp_path))
            st.success(result)
            st.session_state.notebook_path = str(temp_path)

        # Save notebook
        if st.session_state.agent and st.session_state.agent.notebook_manager.cells:
            if st.button("💾 Save Notebook"):
                result = st.session_state.agent.save_notebook()
                st.success(result)

            if st.button("⬇️ Download Notebook"):
                nb_path = st.session_state.agent.notebook_manager.notebook_path
                if nb_path and os.path.exists(nb_path):
                    with open(nb_path, 'r') as f:
                        st.download_button(
                            "Download",
                            f.read(),
                            file_name=os.path.basename(nb_path),
                            mime="application/json"
                        )

        st.divider()

        # Quick actions
        st.subheader("⚡ Quick Actions")

        if st.button("📊 Analyze Notebook"):
            if st.session_state.agent:
                analysis = st.session_state.agent.analyze_notebook()
                st.json(analysis)
            else:
                st.warning("No notebook loaded")

        if st.button("💡 Suggest Next Steps"):
            if st.session_state.agent:
                suggestions = st.session_state.agent.suggest_next_steps()
                st.info(suggestions)
            else:
                st.warning("No notebook loaded")

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


def render_notebook_viewer():
    """Render the notebook content viewer"""
    if st.session_state.agent is None:
        st.info("👈 Create or load a notebook to get started")
        return

    if not st.session_state.agent.notebook_manager.cells:
        st.info("Notebook is empty. Start chatting to add cells!")
        return

    st.subheader("📓 Notebook Preview")

    for i, cell in enumerate(st.session_state.agent.notebook_manager.cells):
        with st.container():
            col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

            with col1:
                st.write(f"**[{i}]**")

            with col2:
                if cell.cell_type == CellType.MARKDOWN:
                    with st.expander(f"📝 Markdown Cell {i}", expanded=True):
                        st.markdown(cell.source)
                else:
                    with st.expander(f"💻 Code Cell {i}", expanded=True):
                        st.code(cell.source, language='python')

            with col3:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state[f'editing_{i}'] = True

                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.agent.delete_cell(i)
                    st.rerun()

            # Edit mode
            if st.session_state.get(f'editing_{i}', False):
                new_content = st.text_area(
                    f"Edit Cell {i}",
                    value=cell.source,
                    key=f"edit_area_{i}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Save", key=f"save_{i}"):
                        st.session_state.agent.update_cell(i, new_content)
                        st.session_state[f'editing_{i}'] = False
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_{i}"):
                        st.session_state[f'editing_{i}'] = False
                        st.rerun()

            st.divider()


def render_chat_interface():
    """Render the chat interface"""
    st.subheader("💬 Chat with AI Assistant")

    # Initialize agent if needed
    if st.session_state.agent is None:
        model_config = st.session_state.models_config['models'][st.session_state.selected_model_index]
        st.session_state.agent = NotebookAgent(
            provider=model_config['provider'],
            model=model_config['model']
        )

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.write(message['content'])

    # Chat input
    user_input = st.chat_input("Ask me anything about your notebook...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })

        # Get agent response
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(user_input)

        # Add assistant response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })

        st.rerun()


def render_quick_add():
    """Render quick add cell interface"""
    with st.expander("➕ Quick Add Cell"):
        cell_type = st.radio("Cell Type", ["Code", "Markdown"], horizontal=True)

        content = st.text_area("Content", height=100)

        col1, col2 = st.columns([1, 3])
        with col1:
            position = st.number_input("Position", min_value=-1, value=-1, help="-1 to append at end")

        with col2:
            if st.button("Add Cell", use_container_width=True):
                if content and st.session_state.agent:
                    pos = None if position == -1 else position
                    if cell_type == "Code":
                        result = st.session_state.agent.add_code_cell(content, pos)
                    else:
                        result = st.session_state.agent.add_markdown_cell(content, pos)

                    st.success(result)
                    st.rerun()


def main():
    """Main application"""
    initialize_session_state()

    st.title("📓 Notebook Chat Assistant")
    st.markdown("*An AI-powered tool to help you create and fill Jupyter notebooks*")

    # Render sidebar
    render_sidebar()

    # Main content area with tabs
    tab1, tab2 = st.tabs(["💬 Chat", "📓 Notebook"])

    with tab1:
        render_chat_interface()
        st.divider()
        render_quick_add()

    with tab2:
        render_notebook_viewer()

    # Footer
    st.divider()
    st.markdown(
        "*Built with [Ceylon AI Framework](https://github.com/ceylonai/ceylon) | "
        "Powered by LLM agents*"
    )


if __name__ == "__main__":
    main()

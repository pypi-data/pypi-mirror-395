# Ceylon AI Documentation

This directory contains the comprehensive documentation for Ceylon AI Python bindings.

## Structure

- **`index.md`** - Homepage with overview and quick start
- **`getting-started/`** - Installation, quick start, first agent, core concepts
- **`guide/`** - Detailed guides for all components
  - `agents/` - Agent types and usage
  - `actions/` - Tools and actions system
  - `llm/` - LLM integration
  - `memory/` - Memory system
  - `mesh/` - Mesh networking
  - `async/` - Async programming
- **`examples/`** - Step-by-step tutorials and examples
  - `basic/` - Basic agent examples
  - `memory/` - Memory system examples
  - `async/` - Async examples
  - `rag/` - RAG system examples
- **`api/`** - API reference documentation
  - `core/` - Core classes (Agent, LlmAgent, LocalMesh)
  - `actions/` - Action system
  - `memory/` - Memory classes
- **`stylesheets/`** - Custom CSS for FastAPI-style documentation
- **`javascripts/`** - Custom JavaScript for enhanced interactivity

## Building the Documentation

### Install Dependencies

```bash
pip install mkdocs-material pymdown-extensions
```

### Build Documentation

```bash
# From project root
mkdocs build

# Serve locally for development
mkdocs serve
```

The documentation will be available at http://127.0.0.1:8000

### Build Output

Built site is generated in `/site` directory.

## Documentation Style

This documentation follows the style of FastAPI and PydanticAI:

- **Clear Examples**: Every concept has working code examples
- **Step-by-Step**: Tutorials progress from simple to advanced
- **Comprehensive**: Complete coverage of all features
- **Beautiful**: Material Design theme with custom styling
- **Interactive**: Code copy buttons, search, and navigation

## Contributing

To add or update documentation:

1. Edit markdown files in the `docs/` directory
2. Run `mkdocs serve` to preview changes locally
3. Submit a pull request with your changes

### Style Guidelines

- Use clear, concise language
- Include code examples for every concept
- Add type hints to all code examples
- Link to related documentation
- Include troubleshooting sections

## Features

- ✅ Material Design theme
- ✅ Syntax highlighting for Python, Rust, JSON, etc.
- ✅ Code copy buttons
- ✅ Search functionality
- ✅ Mobile-responsive design
- ✅ Dark mode support
- ✅ Mermaid diagrams
- ✅ Tabbed content
- ✅ Admonitions (notes, warnings, etc.)
- ✅ Custom CSS and JavaScript
- ✅ FastAPI-style API documentation

## Live Documentation

Visit the live documentation at: https://ceylon.ai/docs (when deployed)

## License

MIT License - Same as Ceylon AI

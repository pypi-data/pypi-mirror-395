# Installation

Ceylon AI can be installed via pip or built from source. This guide covers both methods.

## Requirements

- **Python**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **Optional**: Rust toolchain (only if building from source)

## Install via pip

The easiest way to install Ceylon AI is using pip:

```bash
pip install ceylonai-next
```

### Verify Installation

```python
import ceylonai_next

print(ceylonai_next.__version__)  # Should print the installed version
```

!!! tip "Import Alias"
    For convenience, you can use a shorter import alias:
    ```python
    import ceylonai_next as ceylon

    print(ceylon.__version__)
    ```

### Create Your First Agent

```python
from ceylonai_next import Agent

agent = Agent("my_first_agent")
response = agent.send_message("Hello, Ceylon!")
print(response)
```

## Install from Source

If you want the latest development version or need to modify the source code:

### Step 1: Clone the Repository

```bash
git clone https://github.com/ceylonai/next-processor.git
cd next-processor/bindings/python
```

### Step 2: Install Rust (if not already installed)

Ceylon AI uses Rust for its high-performance core. Install Rust using rustup:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Follow the on-screen instructions and restart your terminal.

### Step 3: Install Maturin

Maturin is the build tool used for Rust Python bindings:

```bash
pip install maturin
```

### Step 4: Build and Install

#### Development Mode (Editable Install)

For development, install in editable mode:

```bash
# From bindings/python directory
maturin develop

# Or use pip
pip install -e .
```

This allows you to make changes to the Python code without reinstalling.

#### Production Build

For a production build:

```bash
maturin build --release
pip install target/wheels/ceylonai_next-*.whl
```

### Step 5: Verify Installation

```python
import ceylonai_next as ceylon

# Create a test agent
agent = ceylon.Agent("test")
print(f"Ceylon AI installed successfully! Version: {ceylon.__version__}")
```

## Installing Optional Dependencies

Ceylon AI has minimal dependencies by default, but you can install additional packages for development and testing:

### Development Dependencies

```bash
pip install ceylonai-next[dev]
```

This includes:

- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support

### All Dependencies

```bash
pip install ceylonai-next[dev]
```

## Platform-Specific Notes

### Linux

On Linux, you may need to install additional dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential python3-dev

# Fedora/RHEL
sudo dnf install gcc python3-devel
```

### macOS

On macOS, ensure you have Xcode command line tools:

```bash
xcode-select --install
```

### Windows

On Windows, you need:

1. **Microsoft C++ Build Tools** - Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. **Rust** - Install via [rustup](https://rustup.rs/)

## LLM Provider Setup

To use Ceylon AI with LLMs, you need to set up at least one provider:

### Ollama (Local LLMs)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:

```bash
ollama pull llama3.2:latest
```

3. Use in Ceylon:

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "ollama::llama3.2:latest")
agent.build()
```

### OpenAI

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Set environment variable or pass directly:

```python
from ceylonai_next import LlmAgent
import os

# Option 1: Environment variable
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Option 2: Pass directly
agent = LlmAgent("assistant", "openai::gpt-4")
agent.with_api_key("your-api-key")
agent.build()
```

### Anthropic Claude

```python
from ceylonai_next import LlmAgent

agent = LlmAgent("assistant", "anthropic::claude-3-sonnet")
agent.with_api_key("your-anthropic-key")
agent.build()
```

## Troubleshooting

### Import Error: No module named 'ceylonai_next'

Make sure Ceylon AI is installed:

```bash
pip list | grep ceylonai
```

If not listed, reinstall:

```bash
pip install --force-reinstall ceylonai-next
```

!!! note "Package Name"
    The package name is `ceylonai-next` (with hyphen) but import as `ceylonai_next` (with underscore):
    ```python
    # Install
    pip install ceylonai-next

    # Import
    import ceylonai_next
    # Or use alias
    import ceylonai_next as ceylon
    ```

### Build Errors (from source)

If you encounter build errors:

1. **Update Rust**: `rustup update`
2. **Clean build**: `cargo clean && maturin develop`
3. **Check Python version**: `python --version` (must be 3.9+)

### Rust Linker Errors

On Linux, install development tools:

```bash
# Ubuntu/Debian
sudo apt-get install build-essential pkg-config libssl-dev

# Fedora/RHEL
sudo dnf install gcc pkg-config openssl-devel
```

### Windows Build Issues

Ensure you have:

1. Microsoft C++ Build Tools installed
2. Added Rust to PATH: `rustup default stable`
3. Restarted your terminal after installation

## Updating Ceylon AI

To update to the latest version:

```bash
pip install --upgrade ceylonai-next
```

## Uninstalling

To remove Ceylon AI:

```bash
pip uninstall ceylonai-next
```

## Next Steps

Now that you have Ceylon AI installed:

- [Quick Start Guide](quickstart.md) - Get started with basic examples
- [Your First Agent](first-agent.md) - Build a simple agent
- [Core Concepts](concepts.md) - Understand Ceylon's architecture

## Getting Help

- **Documentation**: [ceylon.ai/docs](https://ceylon.ai/docs)
- **GitHub Issues**: [github.com/ceylonai/next-processor/issues](https://github.com/ceylonai/next-processor/issues)
- **PyPI**: [pypi.org/project/ceylonai-next](https://pypi.org/project/ceylonai-next)

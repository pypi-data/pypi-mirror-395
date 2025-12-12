# RAG Web Application

A simple web app to upload markdown files and chat with them using RAG (Retrieval-Augmented Generation).

## Features

- 📤 Upload markdown files
- 🔍 Semantic search using embeddings
- 💬 Chat interface powered by Ollama
- 🎨 Clean UI with TailwindCSS and HTMX

## Quick Start

### 1. Install Dependencies

```bash
cd rag_web_app
pip install -r requirements.txt
```

### 2. Setup Ollama

```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull gemma3:latest
```

### 3. Run the App

```bash
python app.py
```

Open http://localhost:8000 in your browser.

## How It Works

### Simple Architecture

```
User Question
    ↓
Knowledge Base Search (embeddings)
    ↓
Top 3 Most Relevant Chunks
    ↓
LLM (Ollama) + Context
    ↓
Answer with Sources
```

### Code Structure

```
rag_web_app/
├── app.py              # Main FastAPI app (150 lines)
├── kb_manager.py       # Knowledge base + search (100 lines)
├── rag_agent.py        # RAG logic (60 lines)
├── requirements.txt    # Dependencies
└── templates/
    └── index.html     # Simple UI
```

## Code Overview

### app.py
- FastAPI web server
- File upload endpoint
- Chat endpoint
- Serves HTML templates

### kb_manager.py
- Reads markdown files
- Splits into chunks (paragraphs)
- Creates embeddings
- Semantic search

### rag_agent.py
- Takes user question
- Searches knowledge base
- Sends context + question to LLM
- Returns answer with sources

## Usage

1. **Upload Files**: Click "Upload Files" and select .md files
2. **Wait**: Files are indexed automatically
3. **Chat**: Type questions and get answers with sources

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `gemma3:latest` | Ollama model to use |

## Example

```bash
# Upload: product_docs.md
# Ask: "What are the main features?"
# Get: Answer based on your docs with source citations
```

## Customization

### Change Embedding Model
Edit `kb_manager.py`:
```python
self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Change this
```

### Change Chunk Size
Edit `kb_manager.py`:
```python
if len(paragraph) > 50:  # Adjust minimum chunk size
```

### Change Retrieved Chunks
Edit `rag_agent.py`:
```python
results = self.kb.search(question, top_k=3)  # Change top_k
```

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: HTMX + TailwindCSS
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Ollama (gemma3:latest)
- **Search**: Cosine similarity

## Troubleshooting

**Chat button disabled?**
- Make sure files are uploaded
- Check Ollama is running: `ollama list`
- Pull the model: `ollama pull gemma3:latest`

**No results found?**
- Make sure markdown files have content
- Try different questions
- Check the stats panel shows files indexed

## Simple, Not Complex

This is intentionally kept simple:
- ~300 lines of Python total
- No complex chunking strategies
- No vector databases
- No session management
- Easy to understand and modify

Perfect for learning RAG basics! 🚀

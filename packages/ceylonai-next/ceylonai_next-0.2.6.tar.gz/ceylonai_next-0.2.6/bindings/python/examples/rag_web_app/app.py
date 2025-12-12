"""
Simple RAG Web Application
Upload markdown files and chat with them using Ollama
"""

import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from kb_manager import KnowledgeBase
from rag_agent import RAGAgent


# Setup
app = FastAPI(title="RAG Web App")
BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "knowledge_base"
KB_DIR.mkdir(exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Global state
kb = None
agent = None


def init_kb():
    """Initialize knowledge base and agent"""
    global kb, agent

    # Create knowledge base
    kb = KnowledgeBase(str(KB_DIR))
    kb.index_files()

    # Only create agent if we have files
    if kb.chunks:
        try:
            model = os.getenv('OLLAMA_MODEL', 'gemma3:latest')
            agent = RAGAgent(kb, ollama_model=model)
        except Exception as e:
            print(f"Failed to create agent: {e}")
            agent = None
    else:
        agent = None


@app.on_event("startup")
async def startup():
    """Initialize on startup"""
    init_kb()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page"""
    stats = kb.get_stats() if kb and kb.chunks else None
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stats": stats,
        "has_kb": kb is not None and len(kb.chunks) > 0,
        "has_agent": agent is not None
    })


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    """Upload markdown files"""
    uploaded = []

    for file in files:
        if not file.filename.endswith('.md'):
            continue

        # Save file
        path = KB_DIR / file.filename
        with open(path, 'wb') as f:
            content = await file.read()
            f.write(content)

        uploaded.append(file.filename)

    # Re-initialize knowledge base
    if uploaded:
        init_kb()

    stats = kb.get_stats() if kb else None

    return HTMLResponse(f"""
        <div class="alert success">
            Uploaded {len(uploaded)} file(s)
        </div>
        {f'''<div class="stats">
            Files: {stats['total_files']} | Chunks: {stats['total_chunks']}
        </div>''' if stats else ''}
    """)


@app.post("/chat")
async def chat(message: str = Form(...)):
    """Chat endpoint"""
    if not kb or not kb.chunks:
        return HTMLResponse("""
            <div class="message assistant error">
                Please upload some markdown files first.
            </div>
        """)

    if not agent:
        return HTMLResponse("""
            <div class="message assistant error">
                Ollama not available. Run: ollama pull gemma3:latest
            </div>
        """)

    # User message
    html = f"""
        <div class="message user">
            <strong>You:</strong> {message}
        </div>
    """

    try:
        # Get answer
        result = agent.answer(message)

        # Format sources
        sources_html = ""
        if result['sources']:
            sources_html = "<div class='sources'><small>Sources: "
            sources_html += ", ".join([
                f"{s['file']} ({s['score']:.2f})"
                for s in result['sources']
            ])
            sources_html += "</small></div>"

        # Assistant message
        html += f"""
            <div class="message assistant">
                <strong>Assistant:</strong>
                <p>{result['answer']}</p>
                {sources_html}
            </div>
        """
    except Exception as e:
        html += f"""
            <div class="message assistant error">
                Error: {str(e)}
            </div>
        """

    return HTMLResponse(html)


if __name__ == "__main__":
    print("Starting RAG Web App on http://localhost:8000")
    print(f"Ollama model: {os.getenv('OLLAMA_MODEL', 'gemma3:latest')}")
    uvicorn.run(app, host="0.0.0.0", port=8000)

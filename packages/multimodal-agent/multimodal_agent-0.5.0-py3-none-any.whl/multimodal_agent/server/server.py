import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from multimodal_agent import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

agent = MultiModalAgent(enable_rag=True)

app = FastAPI(title="Multimodal Agent Server")

# CORS for VS Code / Flutter IDE plugins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class AskRequest(BaseModel):
    prompt: str
    response_format: str | None = None
    session_id: str | None = None
    no_rag: bool = False


class GenerateRequest(BaseModel):
    prompt: str
    language: str | None = None
    json: bool = True


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5


# Endpoints
@app.post("/ask")
async def ask(request: AskRequest):
    response = agent.ask(
        request.prompt,
        response_format=request.response_format,
        session_id=request.session_id,
        rag_enabled=not request.no_rag,
    )
    return {
        "text": response.text,
        "data": response.data,
        "usage": response.usage,
    }


@app.post("/ask_with_image")
async def ask_with_image(
    prompt: str = Form(...),
    file: UploadFile = File(...),
):
    contents = await file.read()

    # Write image to temporary file
    suffix = Path(file.filename).suffix or ".jpg"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as temp:
        temp.write(contents)
        temp.flush()
        image_part = load_image_as_part(temp.name)

    response = agent.ask_with_image(prompt, image_part)

    return {
        "text": response.text,
        "data": response.data,
        "usage": response.usage,
    }


@app.post("/generate")
async def generate(request: GenerateRequest):
    response = agent.ask(
        request.prompt,
        response_format="json" if request.json else "text",
    )

    if response.data:
        return {
            "data": response.data,
            "text": response.text,
        }

    return {"raw": response.text}


@app.post("/memory/search")
async def memory_search(request: MemorySearchRequest):
    if not agent.enable_rag or agent.rag_store is None:
        return {"results": [], "error": "RAG disabled"}

    results = agent.rag_store.search_similar(
        request.query,
        model=agent.embedding_model,
        top_k=request.limit,
    )
    return {"results": results}


@app.post("/memory/summary")
async def memory_summary(limit: int = 50):
    if not hasattr(agent, "summarize_history"):
        return {"summary": "Memory summarization not available."}

    summary = agent.summarize_history(limit=limit)
    return {"summary": summary}

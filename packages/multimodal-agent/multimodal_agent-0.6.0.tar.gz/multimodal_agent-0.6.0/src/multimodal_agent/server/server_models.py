from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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


class LearnProjectRequest(BaseModel):
    path: str
    project_id: Optional[str] = None
    auto_scan: bool = True
    store_profile: bool = True
    override_existing: bool = False


class ChatRequest(BaseModel):
    # Designed so your earlier curl works:
    # curl -X POST /chat -d '{"message":"hello"}'
    message: str
    session_id: Optional[str] = None
    no_rag: bool = False
    response_format: Optional[str] = None


class ChatResponse(BaseModel):
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    role: str
    session_id: Optional[str]
    content: str
    created_at: str
    source: Optional[str] = None


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    limit: int
    session: Optional[str] = None


class SummaryResponse(BaseModel):
    summary: str
    limit: int
    session: Optional[str] = None

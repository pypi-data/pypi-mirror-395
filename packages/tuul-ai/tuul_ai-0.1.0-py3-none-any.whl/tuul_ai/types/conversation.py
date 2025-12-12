from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Message(BaseModel):
    role: str  # e.g., "user", "agent"
    content: str
    created_at: Optional[int] = None

class ConversationRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ConversationResponse(BaseModel):
    session_id: str
    message: Message
    metadata: Optional[Dict[str, Any]] = None

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Message]
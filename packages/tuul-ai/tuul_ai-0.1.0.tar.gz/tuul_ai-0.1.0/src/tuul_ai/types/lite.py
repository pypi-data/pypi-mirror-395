from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Characteristic(BaseModel):
    """Model for custom characteristic key-value pairs."""
    key: str
    value: str

class LiteRequest(BaseModel):
    """The complete request body for the Lite Mode API."""
    prompt: str
    sessionId: str
    characteristics: List[Characteristic] = Field(default_factory=list)
    cacheSession: bool = False # Explicitly required boolean field


class LiteData(BaseModel):
    sessionId: str
    messages: List[str]
    projectId: str
    reply: str
    totalMessages: int

class FullLiteResponse(BaseModel):
    """Simplified response model for Lite Mode."""
    status: bool
    message: str
    data: LiteData
    error: Optional[Dict[str, Any]] = None

class LiteResponse(BaseModel):
    """Simplified response model for Lite Mode."""
    content: str
    latency_ms: Optional[float] = None
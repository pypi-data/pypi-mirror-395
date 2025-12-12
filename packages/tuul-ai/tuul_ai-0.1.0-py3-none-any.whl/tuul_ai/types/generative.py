from pydantic import BaseModel, Field
from typing import Optional, List, Union

# Helper for file/image input
class ImageOptions(BaseModel):
    file: Union[str, bytes] 
    filename: str
    mediaType: Optional[str] = None
    type: str # "file" or "image"
    url: Optional[str] = None


# Nested Models
class PromptOptions(BaseModel):
    prompt: str
    files: Optional[List[ImageOptions]] = None

class AgentOptions(BaseModel):
    agentId: str
    agentVersion: Optional[str] = None

class SessionOptions(BaseModel):
    sessionId: str
    conversationId: Optional[str] = None

class StateOptions(BaseModel):
    newConversation: Optional[bool] = None
    cancelGeneration: bool = False

class AbilityOptions(BaseModel):
    reasoning: bool
    webSearch: bool

    
# Primary Payload Model
class OpenaiPayload(BaseModel):
    promptOptions: PromptOptions
    stateOptions: StateOptions
    sessionOptions: SessionOptions
    agentOptions: AgentOptions
    abilityOptions: AbilityOptions


class GenerateResponse(BaseModel):
    id: str
    content: str
    usage: dict
    created_at: int
from typing import Optional, List, Dict, Any
from ..types.lite import LiteRequest, LiteResponse, FullLiteResponse, Characteristic

class LiteResource:
    def __init__(self, client):
        self._client = client

    def generate(
        self, 
        prompt: str, 
        session_id: str,
        characteristics: Optional[List[Dict[str, str]]] = None,
        cache_session: bool = False,
        **kwargs
    ) -> FullLiteResponse:
        """
        Low-latency generation request with specific session characteristics.
        
        Args:
            prompt: The text prompt for the Lite model.
            session_id: Optional existing session ID.
            characteristics: List of {'key': str, 'value': str} dictionaries.
            cache_session: Whether to cache the session state.
        """
        
        # Pydantic requires fields to match snake_case arguments to camelCase fields
        payload = LiteRequest(
            prompt=prompt,
            sessionId=session_id,
            characteristics=characteristics or [],
            cacheSession=cache_session,
            **kwargs
        ).model_dump(by_alias=True, exclude_none=True)
        
        # Adjusting the endpoint path based on common practice (assuming /lite/generate is correct)
        data = self._client.post("/v1beta/models/litegen", json=payload)
        
        full_response = FullLiteResponse(**data)
        
        final_content = full_response.data.reply

        return LiteResponse(
            content=final_content,
            latency_ms=None
        )

class AsyncLiteResource:
    def __init__(self, client):
        self._client = client

    async def generate(
        self, 
        prompt: str, 
        session_id: str, 
        characteristics: Optional[List[Dict[str, str]]] = None,
        cache_session: bool = False,
        **kwargs
    ) -> LiteResponse:
        
        payload = LiteRequest(
            prompt=prompt,
            sessionId=session_id,
            characteristics=characteristics or [],
            cacheSession=cache_session,
            **kwargs
        ).model_dump(by_alias=True, exclude_none=True)
        
        data = await self._client.post("/v1beta/models/litegen", json=payload)

        full_response = FullLiteResponse(**data)
        
        final_content = full_response.data.reply

        return LiteResponse(
            content=final_content,
            latency_ms=None
        )
from typing import Optional
import httpx
import time
import asyncio
from ._base import BaseClient
from .exceptions import APIConnectionError
from .resources.generative import GenerativeResource, AsyncGenerativeResource
from .resources.conversation import ConversationResource, AsyncConversationResource # Assumed exists
from .resources.lite import LiteResource, AsyncLiteResource # Assumed exists

class TuulClient(BaseClient):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self._client = httpx.Client(
            base_url=self.base_url, 
            headers=self._headers, 
            timeout=self.timeout
        )
        
        # Resources
        self.generative = GenerativeResource(self)
        self.conversation = ConversationResource(self) # Implementation implied
        self.lite = LiteResource(self) # Implementation implied

    def post(self, path: str, json: dict) -> dict:
        retries = 0
        while True:
            try:
                response = self._client.post(path, json=json)
                if response.is_success:
                    return response.json()
                
                # Check retry logic for 5xx/429
                if retries < self.max_retries and self._should_retry(response, None):
                    retries += 1
                    time.sleep(0.5 * (2 ** retries)) # Exponential backoff
                    continue
                
                self._handle_error(response)
            
            except httpx.RequestError as e:
                if retries < self.max_retries:
                    retries += 1
                    time.sleep(0.5 * (2 ** retries))
                    continue
                raise APIConnectionError("Connection failed") from e
    
    def close(self):
        self._client.close()

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self.close()


class AsyncTuulClient(BaseClient):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self._client = httpx.AsyncClient(
            base_url=self.base_url, 
            headers=self._headers, 
            timeout=self.timeout
        )
        self.generative = AsyncGenerativeResource(self)
        self.conversation = AsyncConversationResource(self)
        self.lite = AsyncLiteResource(self)

    async def post(self, path: str, json: dict) -> dict:
        retries = 0
        while True:
            try:
                response = await self._client.post(path, json=json)
                if response.is_success:
                    return response.json()
                
                if retries < self.max_retries and self._should_retry(response, None):
                    retries += 1
                    await asyncio.sleep(0.5 * (2 ** retries))
                    continue
                
                self._handle_error(response)

            except httpx.RequestError as e:
                if retries < self.max_retries:
                    retries += 1
                    await asyncio.sleep(0.5 * (2 ** retries))
                    continue
                raise APIConnectionError("Connection failed") from e

    # Add inside TuulClient class
    async def get(self, path: str, params: Optional[dict] = None) -> dict:
        # Simplified GET with error handling
        response = self._client.get(path, params=params)
        if response.is_success:
            return response.json()
        self._handle_error(response)
        
        
    async def close(self):
        await self._client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *_):
        await self.close()
import httpx
import time
import logging
from typing import Dict, Optional, Any
from .exceptions import (
    TuulError, APIConnectionError, AuthenticationError, 
    PermissionError, RateLimitError, APIStatusError
)

logger = logging.getLogger("tuul")

DEFAULT_BASE_URL = "https://api.tuul.digitwhale.com"

class BaseClient:
    def __init__(
        self, 
        api_key: str, 
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._headers = {
            "tuul_api_key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "tuul-sdk/0.1.0"
        }

    def _handle_error(self, response: httpx.Response):
        """Maps HTTP status codes to Tuul exceptions."""
        try:
            data = response.json()
            msg = data.get("error", {}).get("message", response.text)
        except Exception:
            msg = response.text

        if response.status_code == 401:
            raise AuthenticationError(msg, status_code=401, body=data)
        if response.status_code == 403:
            raise PermissionError(msg, status_code=403, body=data)
        if response.status_code == 429:
            raise RateLimitError(msg, status_code=429, body=data)
        if 400 <= response.status_code < 500:
            raise APIStatusError(msg, status_code=response.status_code, body=data)
        if response.status_code >= 500:
            raise APIStatusError("Internal Server Error", status_code=response.status_code, body=data)

    def _should_retry(self, response: Optional[httpx.Response], exception: Optional[Exception]) -> bool:
        if exception and isinstance(exception, (httpx.TimeoutException, httpx.NetworkError)):
            return True
        if response is not None and response.status_code in [408, 429, 500, 502, 503, 504]:
            return True
        return False
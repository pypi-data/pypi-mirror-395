from typing import Optional, Any

class TuulError(Exception):
    """Base exception for all Tuul SDK errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

class APIConnectionError(TuulError):
    """Network transport errors (timeout, DNS)."""

class AuthenticationError(TuulError):
    """401 - Invalid API Key."""
    

class PermissionError(TuulError):
    """403 - Often related to IP Whitelisting in Tuul."""
    def __init__(self, message: str, **kwargs):
        msg_lower = message.lower()

        if "api key" in msg_lower or "apikey" in msg_lower:
            hint = "(Check if your API Key is valid and belongs to this Tuul project)"
        else:
            hint = "(Check if your IP is whitelisted in Tuul Configuration Settings)"

        super().__init__(f"{message} {hint}", **kwargs)

class RateLimitError(TuulError):
    """429 - Rate limit exceeded."""

class APIStatusError(TuulError):
    """4xx/5xx errors not covered by specific exceptions."""
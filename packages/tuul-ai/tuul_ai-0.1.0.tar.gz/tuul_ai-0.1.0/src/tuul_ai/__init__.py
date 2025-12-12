# src/tuul_ai/__init__.py

# Expose the core client classes
from .client import TuulClient, AsyncTuulClient

# Expose the custom exceptions
from .exceptions import (
    TuulError,
    APIConnectionError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    APIStatusError,
)

# Define the package version
__version__ = "0.1.0"

# Optionally, you can define __all__ for explicit exports
__all__ = [
    "TuulClient",
    "AsyncTuulClient",
    "TuulError",
    "APIConnectionError",
    "AuthenticationError",
    "PermissionError",
    "RateLimitError",
    "APIStatusError",
]
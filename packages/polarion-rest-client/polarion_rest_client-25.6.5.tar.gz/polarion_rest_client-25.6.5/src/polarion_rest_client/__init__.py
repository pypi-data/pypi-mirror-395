"""
polarion_rest_client (high-level layer)

Exports:
- __version__          : installed distribution version
- PolarionClient       : HL wrapper holding the generated client (Sync)
- PolarionAsyncClient  : HL wrapper holding the generated client (Async)
- get_env_vars()       : read env vars and return kwargs for Client
"""

from .client import PolarionClient, PolarionAsyncClient
from .error import (
    PolarionError,
    HTTPStatusError,
    JSONAPIError,
    Unauthorized,
    Forbidden,
    NotFound,
    Conflict,
    ServerError,
    raise_jsonapi_error,
    raise_from_response,
)
from .session import get_env_vars

from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version("polarion-rest-client")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["__version__", "PolarionClient", "PolarionAsyncClient", "get_env_vars"]
__all__ += [
    "PolarionError",
    "HTTPStatusError",
    "JSONAPIError",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "Conflict",
    "ServerError",
    "raise_jsonapi_error",
    "raise_from_response",
]

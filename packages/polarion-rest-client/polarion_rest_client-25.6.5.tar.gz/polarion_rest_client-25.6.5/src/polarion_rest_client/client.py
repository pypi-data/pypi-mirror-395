"""
High-level client wrapper for the generated Polarion REST client.
Refactored to share common logic between Sync and Async clients.
"""
from __future__ import annotations
from typing import Optional, Mapping, Dict
import base64
import re
import ssl
import truststore

try:
    from polarion_rest_client.openapi.client import AuthenticatedClient
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "The generated package 'polarion_rest_client.openapi' is not available. "
        "Run 'pdm run regenerate-client' and rebuild."
    ) from exc

DEFAULT_TIMEOUT = 30.0
_REST_BASE_PATTERN = re.compile(r"/polarion/rest(/v\d+)?/?$")


def _merge_headers(h: Optional[Mapping[str, str]]) -> Dict[str, str]:
    return dict(h or {})


def _normalize_base_url(base_url: str, rest_version: str = "v1") -> str:
    base = base_url.rstrip("/")

    # Use regex properly: apply it to the string
    if _REST_BASE_PATTERN.search(base):
        return base

    return f"{base}/polarion/rest/{rest_version}"


class PolarionBaseClient:
    """
    Base client containing common logic for initialization, auth, and URL handling.
    """
    def __init__(
        self,
        *,
        base_url: str,
        token: Optional[str] = None,
        token_prefix: str = "Bearer",
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        verify_ssl: bool = True,
        headers: Optional[Mapping[str, str]] = None,
        rest_version: str = "v1",
        normalize_rest_base: bool = True,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required")

        if normalize_rest_base:
            base_url = _normalize_base_url(base_url, rest_version=rest_version)

        hdrs = _merge_headers(headers)
        flag_or_ssl_context = (
            truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            if verify_ssl is True
            else verify_ssl
        )

        if token and (username or password):
            raise ValueError("Provide either token or username+password, not both.")

        if token:
            self._gen = AuthenticatedClient(
                base_url=base_url,
                token=token,
                prefix=token_prefix,
                timeout=timeout,
                verify_ssl=flag_or_ssl_context,
                headers=hdrs,
            )
        elif username and password:
            basic = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
            hdrs = {"Authorization": f"Basic {basic}", **hdrs}
            self._gen = AuthenticatedClient(
                base_url=base_url,
                token=None,
                timeout=timeout,
                verify_ssl=flag_or_ssl_context,
                headers=hdrs,
            )
        else:
            raise ValueError("Provide either token or username+password")

    @property
    def gen(self) -> AuthenticatedClient:
        """Return the underlying generated client."""
        return self._gen

    @property
    def base_url(self) -> str:
        """Expose the underlying base_url from the generated client."""
        if hasattr(self._gen, "base_url"):
            return self._gen.base_url  # type: ignore[attr-defined]
        if hasattr(self._gen, "_base_url"):
            return self._gen._base_url  # type: ignore[attr-defined]
        if hasattr(self._gen, "get_base_url"):
            return self._gen.get_base_url()  # type: ignore[attr-defined]
        raise AttributeError("Generated client has no base_url/_base_url/get_base_url")


class PolarionClient(PolarionBaseClient):
    """
    Synchronous Client Wrapper.
    """
    @property
    def is_async(self) -> bool:
        return False

    def httpx(self):
        return self._gen.get_httpx_client()


class PolarionAsyncClient(PolarionBaseClient):
    """
    Asynchronous Client Wrapper.
    Wraps the same AuthenticatedClient but uses its async capabilities.
    """
    @property
    def is_async(self) -> bool:
        return True

    async def __aenter__(self) -> PolarionAsyncClient:
        await self._gen.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._gen.__aexit__(exc_type, exc_value, traceback)

    def httpx(self):
        return self._gen.get_async_httpx_client()

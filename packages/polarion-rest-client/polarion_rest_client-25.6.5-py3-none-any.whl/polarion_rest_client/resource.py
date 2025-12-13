from __future__ import annotations
from typing import Any, Callable, Dict, List, Union, Optional, Awaitable, Iterator, AsyncIterator
from .client import PolarionClient, PolarionAsyncClient
from .error import raise_from_response
from .paging import list_items, list_items_async, paged, paged_async, extract_items


class PolarionResource:
    """
    Base class for high-level resources.
    Handles unified dispatch to sync or async generated endpoints based on the client type.
    """
    def __init__(self, client: Union[PolarionClient, PolarionAsyncClient]):
        self.client = client

    def _to_dict(self, resp) -> Dict[str, Any]:
        """Normalize a generated Response to a plain dict payload."""
        if resp is None or getattr(resp, "parsed", None) is None:
            return {}
        try:
            return resp.parsed.to_dict()
        except Exception:
            return resp.parsed

    def _process_response(self, resp) -> Dict[str, Any]:
        """Validate status and return dict."""
        if 200 <= resp.status_code < 300:
            return self._to_dict(resp)
        raise_from_response(resp)

    # --- Request Dispatchers ---

    def _request(
        self,
        sync_fn: Callable,
        async_fn: Callable,
        **kwargs
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        Execute a request. Returns Dict (sync) or Awaitable[Dict] (async).
        """
        if self.client.is_async:
            async def _do_async():
                resp = await async_fn(client=self.client.gen, **kwargs)
                return self._process_response(resp)
            return _do_async()
        else:
            resp = sync_fn(client=self.client.gen, **kwargs)
            return self._process_response(resp)

    def _request_no_content(
        self,
        sync_fn: Callable,
        async_fn: Callable,
        **kwargs
    ) -> Union[None, Awaitable[None]]:
        """
        Execute a request expecting 204 (void).
        """
        if self.client.is_async:
            async def _do_async():
                resp = await async_fn(client=self.client.gen, **kwargs)
                if not (200 <= resp.status_code < 300):
                    raise_from_response(resp)
            return _do_async()
        else:
            resp = sync_fn(client=self.client.gen, **kwargs)
            if not (200 <= resp.status_code < 300):
                raise_from_response(resp)

    # --- Paging Dispatchers ---

    def _list_items(
        self,
        sync_fn: Callable,
        async_fn: Callable,
        *,
        page_param: str,
        size_param: str,
        page_number: int,
        page_size: int,
        chunk_size: int,
        max_pages: Optional[int] = None,
        **kwargs
    ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
        """
        Fetch list of items. Handles 'page_size=-1' logic via paging utils.
        """
        if self.client.is_async:
            return list_items_async(
                async_fn,
                page_param=page_param,
                size_param=size_param,
                page_number=page_number,
                page_size=page_size,
                chunk_size=chunk_size,
                max_pages=max_pages,
                on_error=raise_from_response,
                client=self.client.gen,
                **kwargs
            )
        else:
            return list_items(
                sync_fn,
                page_param=page_param,
                size_param=size_param,
                page_number=page_number,
                page_size=page_size,
                chunk_size=chunk_size,
                max_pages=max_pages,
                on_error=raise_from_response,
                client=self.client.gen,
                **kwargs
            )

    def _iter_items(
        self,
        sync_fn: Callable,
        async_fn: Callable,
        *,
        page_param: str,
        size_param: str,
        page_size: int,
        start_page: int,
        **kwargs
    ) -> Union[Iterator[Dict[str, Any]], AsyncIterator[Dict[str, Any]]]:
        """
        Returns an iterator (sync) or async iterator (async) over items.
        """
        def _get_kwargs(p_idx, p_size):
            kw = {"client": self.client.gen, size_param: p_size, **kwargs}
            if page_param:
                kw[page_param] = p_idx
            return kw

        if self.client.is_async:
            async def _one_page_async(**kw):
                return await async_fn(**_get_kwargs(kw.get("page_index"), kw.get("page_size")))

            async def _generator():
                async for page_obj in paged_async(
                    _one_page_async,
                    page_param=("page_index" if page_param else None),
                    size_param="page_size",
                    start=start_page, page_size=page_size
                ):
                    for item in extract_items(page_obj):
                        yield item
            return _generator()

        else:
            def _one_page_sync(**kw):
                return sync_fn(**_get_kwargs(kw.get("page_index"), kw.get("page_size")))

            def _generator():
                for page_obj in paged(
                    _one_page_sync,
                    page_param=("page_index" if page_param else None),
                    size_param="page_size",
                    start=start_page, page_size=page_size
                ):
                    for item in extract_items(page_obj):
                        yield item
            return _generator()


class DeepFields:
    """
    Helper that encodes deep-object fields exactly as:
      {'fields[<resource>]': '<value or comma-joined list>'}
    """
    def __init__(self, resource: str, value: Union[str, List[str]]):
        self.resource = resource
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        v = self.value
        if isinstance(v, list):
            v = ",".join(v)
        return {f"fields[{self.resource}]": v}

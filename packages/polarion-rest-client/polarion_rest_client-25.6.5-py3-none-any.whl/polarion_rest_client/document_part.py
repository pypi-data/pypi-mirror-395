from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Union, Awaitable, AsyncIterator

from .client import PolarionClient, PolarionAsyncClient
from .resource import PolarionResource, DeepFields
from .paging import resolve_page_params

# Generated client bits
from polarion_rest_client.openapi.types import UNSET, Unset

# Low-level endpoints
from polarion_rest_client.openapi.api.document_parts.get_document_parts import (
    sync_detailed as _get_document_parts,
    asyncio_detailed as _get_document_parts_async,
)
from polarion_rest_client.openapi.api.document_parts.get_document_part import (
    sync_detailed as _get_document_part,
    asyncio_detailed as _get_document_part_async,
)

# TODO : implement when Polarion 25.12 is available
# The OpenAPI in your environment currently exposes GET only for Document Parts.
# If POST/PATCH/DELETE for parts appear in a newer server (e.g., 25.12),
# add the corresponding imports and high-level wrappers here, mirroring WorkItem.


class _DeepFields:
    """
    Small helper that encodes deep-object fields exactly as:
      {'fields[<resource>]': '<value or comma-joined list>'}

    The generated client calls `.to_dict()` on whatever object is passed as `fields`,
    so this works as a drop-in replacement for `SparseFields` while producing
    the correct deep-object query key that some servers require.
    """

    def __init__(self, resource: str, value: Union[str, List[str]]):
        self.resource = resource
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        v = self.value
        if isinstance(v, list):
            # Most servers accept comma-joined string for sparse field lists
            v = ",".join(v)
        return {f"fields[{self.resource}]": v}


def _build_fields_param_for_parts(
    fields_parts: Optional[Union[str, List[str]]],
) -> Union[Unset, DeepFields]:
    """
    Turn `fields_parts` into a deep-object fields parameter for 'document_parts'.

    - None/empty → UNSET (omit the query param entirely)
    - str or list → fields[document_parts]=<value> (list joined by comma)
    """
    if not fields_parts:
        return UNSET
    return DeepFields(
        "document_parts",
        fields_parts if isinstance(fields_parts, str) else list(fields_parts),
    )


class DocumentPart(PolarionResource):
    """
    High-level wrapper for Document Parts (read/list only as per current OpenAPI).
    Supports both Synchronous and Asynchronous clients.

    Endpoints used (GET only):
      - /projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts         (list)
      - /projects/{projectId}/spaces/{spaceId}/documents/{documentName}/parts/{id}   (get)
    """

    def __init__(self, pc: Union[PolarionClient, PolarionAsyncClient]):
        super().__init__(pc)
        self._c = pc.gen
        # Resolve the exact paging param names on your generated function.
        self._page_param, self._size_param = resolve_page_params(_get_document_parts)

    # ---------------------------- LIST (items) ----------------------------
    def list(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        *,
        page_number: int = 1,
        page_size: int = 100,
        # Accept either "@all" as a string or a list of attribute names
        fields_parts: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None,
        # When page_size == -1 we fetch-all client-side with this per-request chunk
        chunk_size: int = 200,
        # Optional local filtering helpers (no server-side querying exists for parts)
        title_contains: Optional[str] = None,
        max_pages: int = 5000,
    ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
        """
        Return document parts as a list of JSON:API resource objects.
        Supports Sync and Async execution.

        Notes:
          * If page_size == -1: fetch ALL pages client-side; we never send “-1” to the server.
          * fields_parts: if provided, encoded as deep-object fields[document_parts]=...
          * There is no query parameter for parts in the current API, so we optionally
            filter locally by `title_contains` after retrieval.
        """
        fields = _build_fields_param_for_parts(fields_parts)

        # Closure for filtering logic, applied after fetching
        def _filter(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            if not title_contains:
                return items
            t = title_contains.lower()
            return [
                it for it in items
                if str((it.get("attributes") or {}).get("title", "")).lower().find(t) >= 0
            ]

        if self.client.is_async:
            async def _do_async():
                items = await self._list_items(
                    _get_document_parts,
                    _get_document_parts_async,
                    page_param=self._page_param,
                    size_param=self._size_param,
                    page_number=page_number,
                    page_size=page_size,
                    chunk_size=chunk_size,
                    max_pages=max_pages,
                    project_id=project_id,
                    space_id=space_id,
                    document_name=document_name,
                    fields=fields,
                    include=include if include is not None else UNSET,
                    revision=revision if revision is not None else UNSET,
                )
                return _filter(items)
            return _do_async()
        else:
            items = self._list_items(
                _get_document_parts,
                _get_document_parts_async,
                page_param=self._page_param,
                size_param=self._size_param,
                page_number=page_number,
                page_size=page_size,
                chunk_size=chunk_size,
                max_pages=max_pages,
                project_id=project_id,
                space_id=space_id,
                document_name=document_name,
                fields=fields,
                include=include if include is not None else UNSET,
                revision=revision if revision is not None else UNSET,
            )
            return _filter(items)

    # ------------------------------ GET ------------------------------
    def get(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        part_id: str,
        *,
        fields_parts: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        Return a single Document Part by ID.
        Supports Sync and Async execution.

        Pass `fields_parts="@all"` to ensure the server returns the full content.
        """
        fields = _build_fields_param_for_parts(fields_parts)

        return self._request(
            _get_document_part,
            _get_document_part_async,
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            part_id=part_id,
            fields=fields,
            include=include if include is not None else UNSET,
            revision=revision if revision is not None else UNSET,
        )

    # ------------------------------ ITER ------------------------------
    def iter(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        *,
        page_size: int = 100,
        start_page: int = 1,
        fields_parts: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None,
    ) -> Union[Iterator[Dict[str, Any]], AsyncIterator[Dict[str, Any]]]:
        """
        Iterate all parts for a given document.
        Returns an Iterator (Sync) or AsyncIterator (Async).
        """
        fields = _build_fields_param_for_parts(fields_parts)

        return self._iter_items(
            _get_document_parts,
            _get_document_parts_async,
            page_param=self._page_param,
            size_param=self._size_param,
            page_size=page_size,
            start_page=start_page,
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            fields=fields,
            include=include if include is not None else UNSET,
            revision=revision if revision is not None else UNSET,
        )

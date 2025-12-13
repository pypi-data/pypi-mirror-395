from __future__ import annotations

from typing import Any, Dict, Iterator, List, Mapping, Optional, Union, Awaitable, AsyncIterator

from .client import PolarionClient, PolarionAsyncClient
from .resource import PolarionResource
from .error import raise_from_response
from .paging import resolve_page_params

# Low-level API (generated)
from polarion_rest_client.openapi.api.work_items.get_work_items import (
    sync_detailed as _get_work_items,
    asyncio_detailed as _get_work_items_async,
)
from polarion_rest_client.openapi.api.work_items.get_work_item import (
    sync_detailed as _get_work_item,
    asyncio_detailed as _get_work_item_async,
)
from polarion_rest_client.openapi.api.work_items.post_work_items import (
    sync_detailed as _post_work_items,
    asyncio_detailed as _post_work_items_async,
)
from polarion_rest_client.openapi.api.work_items.patch_work_item import (
    sync_detailed as _patch_work_item,
    asyncio_detailed as _patch_work_item_async,
)
from polarion_rest_client.openapi.api.work_items.delete_work_items import (
    sync_detailed as _delete_work_items,
    asyncio_detailed as _delete_work_items_async,
)
from polarion_rest_client.openapi.api.work_items.patch_work_items import (
    sync_detailed as _patch_work_items,
    asyncio_detailed as _patch_work_items_async,
)

# Request models
from polarion_rest_client.openapi.models.workitems_list_post_request import (
    WorkitemsListPostRequest,
)
from polarion_rest_client.openapi.models.workitems_single_patch_request import (
    WorkitemsSinglePatchRequest,
)
from polarion_rest_client.openapi.models.workitems_list_delete_request import (
    WorkitemsListDeleteRequest,
)
from polarion_rest_client.openapi.models.workitems_list_patch_request import (
    WorkitemsListPatchRequest,
)
from polarion_rest_client.openapi.models.sparse_fields import SparseFields
from polarion_rest_client.openapi.types import UNSET


def _build_fields_param(fields: Optional[Union[str, List[str]]]) -> Any:
    """Convert list/string fields to SparseFields object expected by generated client."""
    if not fields:
        return UNSET
    if isinstance(fields, str):
        return SparseFields(workitems=fields)
    return SparseFields(workitems=",".join(fields))


class WorkItem(PolarionResource):
    """
    High-level Work Item operations built strictly on the current generated client API.
    Supports both Synchronous and Asynchronous clients.
    """

    def __init__(self, pc: Union[PolarionClient, PolarionAsyncClient]):
        super().__init__(pc)
        self._c = pc.gen  # AuthenticatedClient
        # Resolve paging parameter names from the generated list endpoint (exact names, no guessing)
        self._page_param, self._size_param = resolve_page_params(_get_work_items)

    # ---------------------------- CREATE ----------------------------
    def create(
        self,
        project_id: str,
        *,
        wi_type: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        description_type: str = "text/plain",
        attributes: Optional[Mapping[str, Any]] = None,
        relationships: Optional[Mapping[str, Any]] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        POST /projects/{projectId}/workitems
        Returns the first created resource reference (JSON:API resource object).
        """
        attrs: Dict[str, Any] = {"type": wi_type}
        if title is not None:
            attrs["title"] = title
        if description is not None:
            attrs["description"] = {"type": description_type, "value": description}
        if attributes:
            attrs.update(attributes)

        item: Dict[str, Any] = {"type": "workitems", "attributes": attrs}
        if relationships:
            item["relationships"] = dict(relationships)

        body = WorkitemsListPostRequest.from_dict({"data": [item]})

        def _process_create_response(resp):
            if resp.status_code == 201 and resp.parsed:
                payload = self._to_dict(resp)
                created = (payload.get("data") or [])
                return created[0] if created else payload
            raise_from_response(resp)

        if self.client.is_async:
            async def _do_async():
                resp = await _post_work_items_async(
                    client=self._c, project_id=project_id, body=body
                )
                return _process_create_response(resp)
            return _do_async()
        else:
            resp = _post_work_items(client=self._c, project_id=project_id, body=body)
            return _process_create_response(resp)

    # ------------------------------ GET ------------------------------
    def get(
        self,
        project_id: str,
        work_item_id: str,
        *,
        include: Optional[str] = None,
        revision: Optional[str] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """GET /projects/{projectId}/workitems/{workItemId}"""
        return self._request(
            _get_work_item,
            _get_work_item_async,
            project_id=project_id,
            work_item_id=work_item_id,
            include=include,
            revision=revision,
        )

    # ----------------------------- UPDATE -----------------------------
    def update(
        self,
        project_id: str,
        work_item_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        description_type: str = "text/plain",
        attributes: Optional[Mapping[str, Any]] = None,
        relationships: Optional[Mapping[str, Any]] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        PATCH /projects/{projectId}/workitems/{workItemId}
        Sends only provided fields.
        """
        attrs: Dict[str, Any] = {}
        if title is not None:
            attrs["title"] = title
        if description is not None:
            attrs["description"] = {"type": description_type, "value": description}
        if attributes:
            attrs.update(attributes)

        data: Dict[str, Any] = {
            "type": "workitems",
            "id": f"{project_id}/{work_item_id}",
        }
        if attrs:
            data["attributes"] = attrs
        if relationships:
            data["relationships"] = dict(relationships)

        body = WorkitemsSinglePatchRequest.from_dict({"data": data})

        # PATCH normally returns 200/204. _request handles returning the body if available.
        def _process_update_response(resp):
            if resp.status_code in (200, 204):
                return self._to_dict(resp)
            raise_from_response(resp)

        if self.client.is_async:
            async def _do_async():
                resp = await _patch_work_item_async(
                    client=self._c,
                    project_id=project_id,
                    work_item_id=work_item_id,
                    body=body,
                )
                return _process_update_response(resp)
            return _do_async()
        else:
            resp = _patch_work_item(
                client=self._c,
                project_id=project_id,
                work_item_id=work_item_id,
                body=body,
            )
            return _process_update_response(resp)

    # ----------------------------- BATCH UPDATE -----------------------------
    def update_many(
        self,
        project_id: str,
        items: List[Mapping[str, Any]],
        *,
        workflow_action: Optional[str] = None,
        change_type_to: Optional[str] = None,
    ) -> Union[None, Awaitable[None]]:
        """
        PATCH /projects/{projectId}/workitems  (batch update)

        Each item may contain:
          {
            "id": "<short-id or 'project/workitem'>",   # required
            "attributes": {...},                         # optional
            "relationships": {...}                       # optional
          }
        """
        if not items:
            if self.client.is_async:
                async def _noop(): return None  # noqa: E704
                return _noop()
            return None

        payload_items: List[Dict[str, Any]] = []
        for it in items:
            wid = it.get("id") or it.get("work_item_id")
            if not wid:
                raise ValueError("Each item must contain 'id' (short or project-qualified)")
            full_id = wid if "/" in str(wid) else f"{project_id}/{wid}"

            entry: Dict[str, Any] = {"type": "workitems", "id": full_id}
            attrs = it.get("attributes")
            rels = it.get("relationships")
            if attrs:
                entry["attributes"] = dict(attrs)
            if rels:
                entry["relationships"] = dict(rels)
            payload_items.append(entry)

        body = WorkitemsListPatchRequest.from_dict({"data": payload_items})

        return self._request_no_content(
            _patch_work_items,
            _patch_work_items_async,
            project_id=project_id,
            body=body,
            workflow_action=workflow_action,
            change_type_to=change_type_to,
        )

    # ----------------------- BATCH UPDATE (same attrs) -----------------------
    def update_many_same_attrs(
        self,
        project_id: str,
        work_item_ids: List[str],
        *,
        attributes: Optional[Mapping[str, Any]] = None,
        relationships: Optional[Mapping[str, Any]] = None,
        workflow_action: Optional[str] = None,
        change_type_to: Optional[str] = None,
    ) -> Union[None, Awaitable[None]]:
        """
        Convenience wrapper over update_many() when all items share the same change.
        """
        if not work_item_ids:
            if self.client.is_async:
                async def _noop(): return None  # noqa: E704
                return _noop()
            return None

        items = []
        for wid in work_item_ids:
            full_id = wid if "/" in str(wid) else f"{project_id}/{wid}"
            entry: Dict[str, Any] = {"type": "workitems", "id": full_id}
            if attributes:
                entry["attributes"] = dict(attributes)
            if relationships:
                entry["relationships"] = dict(relationships)
            items.append(entry)

        # Delegate to the canonical batch endpoint
        return self.update_many(
            project_id,
            items=items,
            workflow_action=workflow_action,
            change_type_to=change_type_to,
        )

    # ----------------------------- DELETE -----------------------------
    def delete(
        self, project_id: str, work_item_ids: List[str]
    ) -> Union[None, Awaitable[None]]:
        """DELETE /projects/{projectId}/workitems (list delete)"""
        body = WorkitemsListDeleteRequest.from_dict(
            {"data": [{"type": "workitems", "id": f"{project_id}/{wid}"} for wid in work_item_ids]}
        )
        return self._request_no_content(
            _delete_work_items,
            _delete_work_items_async,
            project_id=project_id,
            body=body,
        )

    def delete_one(
        self, project_id: str, work_item_id: str
    ) -> Union[None, Awaitable[None]]:
        return self.delete(project_id, [work_item_id])

    # ------------------------------ LIST ------------------------------
    def list(
        self,
        project_id: str,
        *,
        page_number: int = 1,
        page_size: int = 100,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        revision: Optional[str] = None,
        fields: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        chunk_size: int = 200,
    ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
        """
        Return work items as *items* (not the full page doc).

        - If page_size == -1: fetches *all pages* client-side (using `chunk_size` per request).
        - Otherwise: returns the items from the requested single page (page_number/page_size).
        """
        fields_arg = _build_fields_param(fields)

        return self._list_items(
            _get_work_items,
            _get_work_items_async,
            page_param=self._page_param,
            size_param=self._size_param,
            page_number=page_number,
            page_size=page_size,
            chunk_size=chunk_size,
            project_id=project_id,
            query=query,
            sort=sort,
            revision=revision,
            fields=fields_arg,
            include=include,
        )

    # ------------------------------ ITERATE ------------------------------
    def iter(
        self,
        project_id: str,
        *,
        page_size: int = 100,
        query: Optional[str] = None,
        sort: Optional[str] = None,
        revision: Optional[str] = None,
        fields: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        start_page: int = 1,
    ) -> Union[Iterator[Dict[str, Any]], AsyncIterator[Dict[str, Any]]]:
        """
        Iterate all work items using the shared pager; yields JSON:API resource objects.
        """
        fields_arg = _build_fields_param(fields)

        return self._iter_items(
            _get_work_items,
            _get_work_items_async,
            page_param=(self._page_param if self._page_param else None),
            size_param=self._size_param,
            page_size=page_size,
            start_page=start_page,
            project_id=project_id,
            query=query,
            sort=sort,
            revision=revision,
            fields=fields_arg,
            include=include,
        )

    # ------------------------ FIND BY TITLE ------------------------
    def find_by_title(
        self,
        project_id: str,
        title: str,
        *,
        limit: int = 1,
        page_size: int = 100,
        start_page: int = 1,
        query_via_server: bool = True,
        strict_match: bool = False,
        fields: Optional[Union[str, List[str]]] = None,
    ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
        """
        Find work items by title.
        Supports Sync and Async execution.
        """
        q = f'title:"{title}"'
        t_lower = title.lower()

        # If filtering locally (strict_match), we MUST have the 'title' field.
        # If the user didn't provide specific fields, we default to fetching ID and Title.
        eff_fields = fields
        if strict_match and not eff_fields:
            eff_fields = ["id", "type", "title"]

        def _matches(item):
            attrs = item.get("attributes") or {}
            val = str(attrs.get("title", "")).lower()
            return val == t_lower if strict_match else (t_lower in val)

        if self.client.is_async:
            async def _do_async():
                results: List[Dict[str, Any]] = []
                if query_via_server and page_size == -1:
                    items = await self.list(
                        project_id,
                        page_number=start_page,
                        page_size=-1,
                        query=q,
                        fields=eff_fields,
                    )
                    if strict_match:
                        items = [it for it in items if _matches(it)]
                    return items[:limit] if limit > 0 else items

                # Stream via iter() until we collect `limit`
                # If query_via_server is False, we scan everything.
                query_arg = q if query_via_server else None

                async for it in self.iter(
                    project_id, page_size=page_size, start_page=start_page, query=query_arg, fields=eff_fields
                ):
                    # If server did the query, we trust it unless strict_match is requested
                    # If client side query, we must match
                    must_check = strict_match or (not query_via_server)
                    if must_check and not _matches(it):
                        continue
                    results.append(it)
                    if 0 < limit <= len(results):
                        break
                return results
            return _do_async()

        else:
            results: List[Dict[str, Any]] = []
            if query_via_server and page_size == -1:
                items = self.list(
                    project_id,
                    page_number=start_page,
                    page_size=-1,
                    query=q,
                    fields=eff_fields,
                )
                if strict_match:
                    items = [it for it in items if _matches(it)]
                return items[:limit] if limit > 0 else items

            query_arg = q if query_via_server else None
            for it in self.iter(
                project_id, page_size=page_size, start_page=start_page, query=query_arg, fields=eff_fields
            ):
                must_check = strict_match or (not query_via_server)
                if must_check and not _matches(it):
                    continue
                results.append(it)
                if 0 < limit <= len(results):
                    break
            return results

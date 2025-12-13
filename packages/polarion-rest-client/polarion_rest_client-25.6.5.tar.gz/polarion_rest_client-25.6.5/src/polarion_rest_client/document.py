from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Union, Awaitable

from .client import PolarionClient, PolarionAsyncClient
from .resource import PolarionResource, DeepFields
from .error import raise_from_response

# Low-level API from the generated client (present in current OpenAPI)
from polarion_rest_client.openapi.api.documents.post_documents import (
    sync_detailed as _post_documents,
    asyncio_detailed as _post_documents_async,
)
from polarion_rest_client.openapi.api.documents.get_document import (
    sync_detailed as _get_document,
    asyncio_detailed as _get_document_async,
)
from polarion_rest_client.openapi.api.documents.patch_document import (
    sync_detailed as _patch_document,
    asyncio_detailed as _patch_document_async,
)

# Models / helpers from the generated client
# We keep SparseFields for the commented-out 25.12 stubs
from polarion_rest_client.openapi.models.documents_list_post_request import (
    DocumentsListPostRequest,
)
from polarion_rest_client.openapi.models.documents_single_patch_request import (
    DocumentsSinglePatchRequest,
)
from polarion_rest_client.openapi.types import UNSET, Unset


# --- Re-implementation of _DeepFields, as used in document_part.py ---
# This is needed because the standard SparseFields model does not
# serialize to the "deepObject" format (fields[resource]=...)
# that the Polarion API expects.
class _DeepFields:
    """
    Small helper that encodes deep-object fields exactly as:
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


def _build_fields_param_for_documents(
    fields_documents: Optional[Union[str, List[str]]],
) -> Union[Unset, DeepFields]:
    """
    Turn `fields_documents` into a deep-object fields parameter
    for the 'documents' resource.
    """
    if not fields_documents:
        return UNSET
    return DeepFields(
        "documents",
        fields_documents
        if isinstance(fields_documents, str)
        else list(fields_documents),
    )


class Document(PolarionResource):
    """
    High-level Document operations built strictly on the current generated client API.
    Supports both synchronous and asynchronous clients.

    Available (current spec):
      • create (POST /projects/{projectId}/spaces/{spaceId}/documents)
      • get    (GET  /projects/{projectId}/spaces/{spaceId}/documents/{documentName})
      • update (PATCH /projects/{projectId}/spaces/{spaceId}/documents/{documentName})

    Not yet available in current spec (planned for 25.12):
      • list/iter/find_by_title (see commented stubs below)
    """

    def __init__(self, pc: Union[PolarionClient, PolarionAsyncClient]):
        super().__init__(pc)
        self._c = pc.gen  # AuthenticatedClient

        # -------------------------------------------------------------------
        # TODO: implement when Polarion 25.12 is available
        # Enable paging param resolution when list endpoint exists.
        # self._page_param, self._size_param = resolve_page_params(_get_documents)
        # -------------------------------------------------------------------

    # ---------------------------- CREATE ----------------------------
    def create(
        self,
        project_id: str,
        space_id: str,
        *,
        module_name: str,  # documentName to create
        title: Optional[str] = None,
        doc_type: Optional[str] = None,  # e.g. 'req_specification'
        status: Optional[str] = None,    # e.g. 'draft'
        home_page_content: Optional[str] = None,
        home_page_content_type: str = "text/plain",
        auto_suspect: Optional[bool] = None,
        uses_outline_numbering: Optional[bool] = None,
        outline_numbering_prefix: Optional[str] = None,
        rendering_layouts: Optional[List[Mapping[str, Any]]] = None,
        structure_link_role: Optional[str] = None,
        attributes: Optional[Mapping[str, Any]] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        POST /projects/{projectId}/spaces/{spaceId}/documents
        Required: module_name (documentName). Other attributes are optional.
        """
        attrs: Dict[str, Any] = {"moduleName": module_name}
        if title is not None:
            attrs["title"] = title
        if doc_type is not None:
            attrs["type"] = doc_type
        if status is not None:
            attrs["status"] = status
        if home_page_content is not None:
            attrs["homePageContent"] = {
                "type": home_page_content_type,
                "value": home_page_content,
            }
        if auto_suspect is not None:
            attrs["autoSuspect"] = bool(auto_suspect)
        if uses_outline_numbering is not None:
            attrs["usesOutlineNumbering"] = bool(uses_outline_numbering)
        if outline_numbering_prefix is not None:
            attrs["outlineNumbering"] = {"prefix": outline_numbering_prefix}
        if rendering_layouts:
            attrs["renderingLayouts"] = list(rendering_layouts)
        if structure_link_role is not None:
            attrs["structureLinkRole"] = structure_link_role
        if attributes:
            attrs.update(attributes)

        body = DocumentsListPostRequest.from_dict(
            {"data": [{"type": "documents", "attributes": attrs}]}
        )

        # Helper to process response specifically for create return structure
        def _extract_created_doc(resp) -> Dict[str, Any]:
            if resp.status_code in (200, 201) and resp.parsed:
                doc = self._to_dict(resp)
                data = doc.get("data") or []
                return data[0] if isinstance(data, list) and data else doc
            raise_from_response(resp)

        if self.client.is_async:
            async def _do_async():
                resp = await _post_documents_async(
                    client=self._c, project_id=project_id, space_id=space_id, body=body
                )
                return _extract_created_doc(resp)
            return _do_async()
        else:
            resp = _post_documents(
                client=self._c, project_id=project_id, space_id=space_id, body=body
            )
            return _extract_created_doc(resp)

    # ------------------------------ GET ------------------------------
    def get(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        *,
        fields_documents: Optional[Union[str, List[str]]] = None,
        include: Optional[str] = None,
        revision: Optional[str] = None,
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """GET /projects/{projectId}/spaces/{spaceId}/documents/{documentName}"""
        # Use the custom _DeepFields helper instead of SparseFields
        fields = _build_fields_param_for_documents(fields_documents)

        return self._request(
            _get_document,
            _get_document_async,
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            fields=fields,
            include=include if include is not None else UNSET,
            revision=revision if revision is not None else UNSET,
        )

    # ----------------------------- UPDATE -----------------------------
    def update(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        *,
        title: Optional[str] = None,
        doc_type: Optional[str] = None,
        status: Optional[str] = None,
        home_page_content: Optional[str] = None,
        home_page_content_type: str = "text/plain",
        auto_suspect: Optional[bool] = None,
        uses_outline_numbering: Optional[bool] = None,
        outline_numbering_prefix: Optional[str] = None,
        rendering_layouts: Optional[List[Mapping[str, Any]]] = None,
        workflow_action: Optional[str] = None,  # maps to query param 'workflowAction'
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        PATCH /projects/{projectId}/spaces/{spaceId}/documents/{documentName}
        Sends only provided fields.
        """
        attrs: Dict[str, Any] = {}
        if title is not None:
            attrs["title"] = title
        if doc_type is not None:
            attrs["type"] = doc_type
        if status is not None:
            attrs["status"] = status
        if home_page_content is not None:
            attrs["homePageContent"] = {"type": home_page_content_type, "value": home_page_content}
        if auto_suspect is not None:
            attrs["autoSuspect"] = bool(auto_suspect)
        if uses_outline_numbering is not None:
            attrs["usesOutlineNumbering"] = bool(uses_outline_numbering)
        if outline_numbering_prefix is not None:
            attrs["outlineNumbering"] = {"prefix": outline_numbering_prefix}
        if rendering_layouts:
            attrs["renderingLayouts"] = list(rendering_layouts)

        data: Dict[str, Any] = {
            "type": "documents",
            "id": f"{project_id}/{space_id}/{document_name}",
        }
        if attrs:
            data["attributes"] = attrs

        body = DocumentsSinglePatchRequest.from_dict({"data": data})

        # PATCH normally returns 200/204. _request handles returning the body if available.
        return self._request(
            _patch_document,
            _patch_document_async,
            project_id=project_id,
            space_id=space_id,
            document_name=document_name,
            body=body,
            workflow_action=workflow_action if workflow_action is not None else UNSET,
        )

    # -------------------------------------------------------------------
    # TODO: implement when Polarion 25.12 is available
    #       (Requires _get_documents, _get_documents_async to be imported)
    #
    # def list(
    #     self,
    #     project_id: str,
    #     space_id: str,
    #     *,
    #     page_number: int = 1,
    #     page_size: int = 100,
    #     query: Optional[str] = None,
    #     sort: Optional[str] = None,
    #     revision: Optional[str] = None,
    #     fields_documents: Optional[Union[str, List[str]]] = None,
    #     include: Optional[str] = None,
    #     chunk_size: int = 200,
    # ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
    #     """
    #     List documents with pagination support.
    #     If page_size=-1, fetches all pages.
    #     """
    #     fields = _build_fields_param_for_documents(fields_documents)
    #     return self._list_items(
    #         _get_documents,
    #         _get_documents_async,
    #         page_param=self._page_param,
    #         size_param=self._size_param,
    #         page_number=page_number,
    #         page_size=page_size,     # -1 => handled client-side
    #         chunk_size=chunk_size,
    #         project_id=project_id,
    #         space_id=space_id,
    #         query=query,
    #         sort=sort,
    #         revision=revision,
    #         fields=fields,
    #         include=include,
    #     )
    #
    # def iter(
    #     self,
    #     project_id: str,
    #     space_id: str,
    #     *,
    #     page_size: int = 100,
    #     query: Optional[str] = None,
    #     sort: Optional[str] = None,
    #     revision: Optional[str] = None,
    #     start_page: int = 1,
    #     fields_documents: Optional[Union[str, List[str]]] = None,
    #     include: Optional[str] = None,
    # ) -> Union[Iterator[Dict[str, Any]], AsyncIterator[Dict[str, Any]]]:
    #     """
    #     Iterate over documents page by page.
    #     """
    #     fields = _build_fields_param_for_documents(fields_documents)
    #     return self._iter_items(
    #         _get_documents,
    #         _get_documents_async,
    #         page_param=(self._page_param if self._page_param else None),
    #         size_param=self._size_param,
    #         page_size=page_size,
    #         start_page=start_page,
    #         project_id=project_id,
    #         space_id=space_id,
    #         query=query,
    #         sort=sort,
    #         revision=revision,
    #         fields=fields,
    #         include=include,
    #     )
    #
    # def find_by_title(
    #     self,
    #     project_id: str,
    #     space_id: str,
    #     title: str,
    #     *,
    #     limit: int = 1,
    #     page_size: int = 100,
    #     start_page: int = 1,
    #     query_via_server: bool = True,
    #     strict_match: bool = False,
    #     fields_documents: Optional[Union[str, List[str]]] = None,
    #     include: Optional[str] = None,
    # ) -> Union[List[Dict[str, Any]], Awaitable[List[Dict[str, Any]]]]:
    #     """
    #     Find documents by title.
    #     """
    #     q = f'title:"{title}"' if query_via_server else None
    #     t_lower = title.lower()
    #
    #     # Ensure we have title field for strict match
    #     eff_fields = fields_documents
    #     if strict_match and not eff_fields:
    #          eff_fields = ["id", "type", "title"]
    #
    #     def _matches(item: Dict[str, Any]) -> bool:
    #         val = str((item.get("attributes") or {}).get("title", "")).lower()
    #         return val == t_lower if strict_match else (t_lower in val)
    #
    #     if self.client.is_async:
    #         async def _do_async():
    #             if page_size == -1:
    #                 items = await self.list(
    #                     project_id, space_id, page_number=start_page, page_size=-1,
    #                     query=q, fields_documents=eff_fields, include=include
    #                 )
    #                 if strict_match:
    #                     items = [x for x in items if _matches(x)]
    #                 return items[:limit] if limit > 0 else items
    #
    #             out = []
    #             async for it in self.iter(
    #                 project_id, space_id, page_size=page_size, start_page=start_page,
    #                 query=q, fields_documents=eff_fields, include=include
    #             ):
    #                 # If server did the query, we trust it unless strict_match is requested
    #                 must_check = strict_match or (not query_via_server)
    #                 if must_check and not _matches(it):
    #                     continue
    #                 out.append(it)
    #                 if 0 < limit <= len(out):
    #                     break
    #             return out
    #         return _do_async()
    #
    #     else:
    #         if page_size == -1:
    #             items = self.list(
    #                 project_id, space_id, page_number=start_page, page_size=-1,
    #                 query=q, fields_documents=eff_fields, include=include
    #             )
    #             if strict_match:
    #                 items = [x for x in items if _matches(x)]
    #             return items[:limit] if limit > 0 else items
    #
    #         out = []
    #         for it in self.iter(
    #             project_id, space_id, page_size=page_size, start_page=start_page,
    #             query=q, fields_documents=eff_fields, include=include
    #         ):
    #             must_check = strict_match or (not query_via_server)
    #             if must_check and not _matches(it):
    #                 continue
    #             out.append(it)
    #             if 0 < limit <= len(out):
    #                 break
    #         return out
    # -------------------------------------------------------------------

"""
Generic paging utilities for Polarion REST (JSON:API) endpoints.

These helpers work with:
  - OpenAPI-generated Response objects (from openapi-python-client) that have
    `.status_code`, `.parsed`, `.content`
  - Plain JSON:API dictionaries like: {"data": [...], "links": {...}}

Also provides "fetch-all" conveniences:
  - list_items(..., page_size=-1)
  - collect_all(...)
"""

from __future__ import annotations

from typing import Any, Dict, Iterator, AsyncIterator, Optional, Sequence, Tuple
import inspect
import time


# ----------------------------- Normalization --------------------------------

def to_plain_dict(obj: Any) -> Optional[Dict[str, Any]]:
    """Best-effort conversion to a plain Python dict."""
    parsed = getattr(obj, "parsed", None)
    if parsed is not None:
        try:
            return parsed.to_dict()  # most generated models
        except Exception:
            if isinstance(parsed, dict):
                return parsed

    if isinstance(obj, dict):
        return obj

    try:
        return obj.to_dict()  # generic model
    except Exception:
        return None


def _items_from_dict(payload: Dict[str, Any]) -> Optional[Sequence[Any]]:
    """Extract JSON:API items (payload['data']) if present and list-like."""
    data = payload.get("data", None)
    if isinstance(data, list):
        return data
    return None


def _has_next_link(payload: Dict[str, Any]) -> Optional[bool]:
    """
    Inspect JSON:API `links.next`. Return:
      - True / False if we can tell whether there is a next page,
      - None if unknown (endpoint doesn't expose links).
    """
    links = payload.get("links")
    if isinstance(links, dict):
        return bool(links.get("next"))
    return None


# ------------------------------- Introspection ---------------------------------

def _fn_param_names(fn) -> Dict[str, inspect.Parameter]:
    real_fn = fn
    while hasattr(real_fn, "__wrapped__"):
        real_fn = real_fn.__wrapped__
    return inspect.signature(real_fn).parameters


def resolve_page_params(fn) -> Tuple[Optional[str], str]:
    """
    Inspect the generated list function signature and return:
        (page_param_name_or_None, size_param_name)

    The names MUST exist in the function signature.
    If no page-index parameter exists, we return (None, size_param).
    """
    params = _fn_param_names(fn)
    names = set(params.keys())
    names_lower = {n.lower(): n for n in names}  # lower→original

    # Detect size param (must exist)
    for cand in ("page_size", "pagesize", "limit", "per_page", "perpage",
                 "count", "size", "max_results", "maxresults"):
        if cand in names_lower:
            size_param = names_lower[cand]
            break
    else:
        # Fallback: any param containing size/limit/count/perpage
        size_param = None
        for original in names:
            lw = original.lower()
            if "size" in lw or "limit" in lw or "perpage" in lw or lw == "count":
                size_param = original
                break
        if size_param is None:
            raise RuntimeError(
                f"Could not resolve a page-size param for {getattr(fn, '__name__', fn)}; "
                f"available params: {sorted(names)}"
            )

    # Detect page index param (may be missing; then we return None)
    page_param = None
    for cand in ("page_number", "page", "pagenumber", "pageindex", "page_index",
                 "pageno", "page_no", "p", "offset", "start"):
        if cand in names_lower and names_lower[cand] != size_param:
            page_param = names_lower[cand]
            break

    return page_param, size_param


def _filter_kwargs_for_fn(fn, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Return kwargs restricted to the parameters accepted by fn."""
    params = _fn_param_names(fn)
    return {k: v for k, v in kwargs.items() if k in params}


# ------------------------------- Public API ---------------------------------

def extract_items(page_obj: Any) -> Sequence[Any]:
    """
    Return the items contained in a page object, trying (in order):
      1) JSON:API dict → payload['data']
      2) object with .items or .data (list/tuple)
      3) empty list
    """
    payload = to_plain_dict(page_obj)
    if payload is not None:
        items = _items_from_dict(payload)
        if items is not None:
            return items

    items_attr = getattr(page_obj, "items", None) or getattr(page_obj, "data", None)
    if isinstance(items_attr, (list, tuple)):
        return items_attr

    return []


def _page_marker(obj: Any) -> Optional[Tuple[Any, int]]:
    """
    Produce a simple 'progress marker' for a page to detect stalls:
      - (first_item_id, item_count) if JSON:API payload with data list
      - otherwise None (no marker available)
    """
    payload = to_plain_dict(obj)
    if not isinstance(payload, dict):
        return None
    items = _items_from_dict(payload)
    if not items:
        return ("__empty__", 0)
    first = items[0]
    if isinstance(first, dict):
        return (first.get("id"), len(items))
    # Fallback to string representation
    return (str(first), len(items))


def _process_page_result(result, prev_marker, page_index, max_pages, pages_seen) -> Tuple[bool, Any, int]:
    payload = to_plain_dict(result)
    if payload is not None:
        items = _items_from_dict(payload)
        next_link = _has_next_link(payload)

        # Explicit 'no next' → stop
        if next_link is False:
            return True, prev_marker, page_index

        # Known items and empty → stop
        if items is not None and len(items) == 0:
            return True, prev_marker, page_index

        # Stall detection
        marker = _page_marker(result)
        if marker is not None and prev_marker is not None and marker == prev_marker and next_link is None:
            return True, prev_marker, page_index
        return False, marker, page_index + 1

    # Fallback: inspect attributes
    try:
        items_attr = getattr(result, "items", None) or getattr(result, "data", None)
        if items_attr is not None and len(items_attr) == 0:
            return True, prev_marker, page_index
    except Exception:
        return True, prev_marker, page_index

    # If we can't inspect content, apply a safety cap
    if max_pages is not None and pages_seen >= max_pages:
        return True, prev_marker, page_index

    return False, prev_marker, page_index + 1


def paged(
    fn,
    *,
    page_param: Optional[str] = "page_number",
    size_param: str = "page_size",
    start: int = 1,
    page_size: int = 100,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> Iterator[Any]:
    """
    Iterate pages from a list endpoint (e.g., generated `sync_detailed`).
    """
    # No page index available → fetch one page and stop (cannot advance).
    if page_param is None:
        call_kwargs: Dict[str, Any] = dict(kwargs)
        call_kwargs[size_param] = page_size
        call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)
        result = fn(**call_kwargs)
        if result is not None:
            yield result
        return

    page_index = start
    pages_seen = 0
    prev_marker: Optional[Tuple[Any, int]] = None

    deadline: Optional[float] = (
        (time.monotonic() + timeout_s) if timeout_s is not None else None
    )

    while True:
        if max_pages is not None and pages_seen >= max_pages:
            break

        if deadline is not None and time.monotonic() >= deadline:
            raise TimeoutError(
                f"Paging operation timed out after {timeout_s} seconds "
                f"(fetched {pages_seen} pages)."
            )

        call_kwargs: Dict[str, Any] = dict(kwargs)
        call_kwargs[page_param] = page_index
        call_kwargs[size_param] = page_size
        call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)

        result = fn(**call_kwargs)
        if result is None:
            break

        yield result
        pages_seen += 1

        stop, prev_marker, page_index = _process_page_result(
            result, prev_marker, page_index, max_pages, pages_seen
        )
        if stop:
            break


async def paged_async(
    fn,
    *,
    page_param: Optional[str] = "page_number",
    size_param: str = "page_size",
    start: int = 1,
    page_size: int = 100,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> AsyncIterator[Any]:
    """
    Async version of paged().
    """
    if page_param is None:
        call_kwargs: Dict[str, Any] = dict(kwargs)
        call_kwargs[size_param] = page_size
        call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)
        result = await fn(**call_kwargs)
        if result is not None:
            yield result
        return

    page_index = start
    pages_seen = 0
    prev_marker: Optional[Tuple[Any, int]] = None
    deadline: Optional[float] = (
        (time.monotonic() + timeout_s) if timeout_s is not None else None
    )

    while True:
        if max_pages is not None and pages_seen >= max_pages:
            break

        if deadline is not None and time.monotonic() >= deadline:
            raise TimeoutError(
                f"Paging operation timed out after {timeout_s} seconds "
                f"(fetched {pages_seen} pages)."
            )

        call_kwargs: Dict[str, Any] = dict(kwargs)
        call_kwargs[page_param] = page_index
        call_kwargs[size_param] = page_size
        call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)

        result = await fn(**call_kwargs)
        if result is None:
            break

        yield result
        pages_seen += 1

        stop, prev_marker, page_index = _process_page_result(
            result, prev_marker, page_index, max_pages, pages_seen
        )
        if stop:
            break


def list_page(
    fn,
    *,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
    page_param: Optional[str] = "page_number",
    size_param: str = "page_size",
    on_error=None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Call a list endpoint once and return a normalized JSON:API dict.
    Only passes parameters that the endpoint truly accepts.
    """
    call_kwargs: Dict[str, Any] = dict(kwargs)
    if page_size is not None and size_param is not None:
        if page_size < 0:
            msg = "page_size must be >= 0 for a single-page call; use collect_all/list_items with page_size=-1"
            raise ValueError(msg)
        call_kwargs[size_param] = page_size
    if page_param is not None and page_number is not None:
        call_kwargs[page_param] = page_number

    call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)
    result = fn(**call_kwargs)

    status = getattr(result, "status_code", None)
    status_int = int(status) if status is not None else None
    payload = to_plain_dict(result)

    if status_int is not None and not (200 <= status_int < 300):
        if on_error:
            on_error(result)
        raise RuntimeError(f"Unexpected list_page status: {status_int}")

    if payload is None:
        if on_error:
            on_error(result)
        return {}

    return payload


# --------------------------- Fetch-all conveniences ---------------------------

def collect_all(
    fn,
    *,
    page_param: Optional[str],
    size_param: str,
    chunk_size: int = 100,
    start: int = 1,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> list:
    """
    Fetch *all* items from a paginated endpoint and return them as a single list.
    """
    items: list = []
    for page in paged(
        fn,
        page_param=page_param,
        size_param=size_param,
        start=start,
        page_size=chunk_size,
        max_pages=max_pages,
        timeout_s=timeout_s,
        **kwargs,
    ):
        items.extend(extract_items(page))
    return items


async def collect_all_async(
    fn,
    *,
    page_param: Optional[str],
    size_param: str,
    chunk_size: int = 100,
    start: int = 1,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> list:
    """
    Async version of collect_all.
    """
    items: list = []
    async for page in paged_async(
        fn,
        page_param=page_param,
        size_param=size_param,
        start=start,
        page_size=chunk_size,
        max_pages=max_pages,
        timeout_s=timeout_s,
        **kwargs,
    ):
        items.extend(extract_items(page))
    return items


def list_items(
    fn,
    *,
    page_param: Optional[str],
    size_param: str,
    page_number: int = 1,
    page_size: int = 100,
    on_error=None,
    chunk_size: int = 200,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> list:
    """
    Convenience to return items (not the full page document).

    - If page_size == -1: fetches *all pages* client-side
    - Otherwise: returns the items from a single page.
    """
    if page_size == -1:
        return collect_all(
            fn,
            page_param=page_param,
            size_param=size_param,
            chunk_size=chunk_size,
            start=page_number,
            max_pages=max_pages,
            timeout_s=timeout_s,
            **kwargs,
        )

    payload = list_page(
        fn,
        page_param=page_param,
        size_param=size_param,
        page_number=page_number,
        page_size=page_size,
        on_error=on_error,
        **kwargs,
    )
    return list(extract_items(payload))


async def list_items_async(
    fn,
    *,
    page_param: Optional[str],
    size_param: str,
    page_number: int = 1,
    page_size: int = 100,
    on_error=None,
    chunk_size: int = 200,
    max_pages: Optional[int] = None,
    timeout_s: Optional[float] = None,
    **kwargs: Any,
) -> list:
    """
    Async version of list_items.
    """
    if page_size == -1:
        return await collect_all_async(
            fn,
            page_param=page_param,
            size_param=size_param,
            chunk_size=chunk_size,
            start=page_number,
            max_pages=max_pages,
            timeout_s=timeout_s,
            **kwargs,
        )

    call_kwargs: Dict[str, Any] = dict(kwargs)
    if size_param is not None:
        if page_size < 0:
            raise ValueError("page_size must be >= 0 for single-page call")
        call_kwargs[size_param] = page_size
    if page_param is not None:
        call_kwargs[page_param] = page_number

    call_kwargs = _filter_kwargs_for_fn(fn, call_kwargs)
    result = await fn(**call_kwargs)

    status = getattr(result, "status_code", None)
    status_int = int(status) if status is not None else None
    payload = to_plain_dict(result)

    if status_int is not None and not (200 <= status_int < 300):
        if on_error:
            on_error(result)
        raise RuntimeError(f"Unexpected list_page status: {status_int}")

    if payload is None:
        if on_error:
            on_error(result)
        return []

    return list(extract_items(payload))

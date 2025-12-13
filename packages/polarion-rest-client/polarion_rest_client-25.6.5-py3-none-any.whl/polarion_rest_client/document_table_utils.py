from __future__ import annotations

import re
from typing import Iterable, List, Optional, Sequence, Tuple, Union, AsyncIterable

from bs4 import BeautifulSoup  # type: ignore
try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

from .client import PolarionClient, PolarionAsyncClient
from .document_part import DocumentPart


_WS_RE = re.compile(r"\s+", re.UNICODE)


def _clean(s: str) -> str:
    """Normalize whitespace and non-breaking spaces."""
    return _WS_RE.sub(" ", (s or "").replace("\xa0", " ")).strip()


def extract_cell_text(cell) -> str:
    """Return the text content of a <td>/<th> cell with normalized whitespace."""
    return _clean(cell.get_text(" ", strip=True))


def _headers_match(
    found: Sequence[str], expected: Sequence[str], order_sensitive: bool = True
) -> bool:
    """
    Case-insensitive header match (trimmed/normalized).
    We still return DataFrames with the original header text.
    """
    f = [_clean(x).lower() for x in found]
    e = [_clean(x).lower() for x in expected]
    if not order_sensitive:
        return sorted(f) == sorted(e)
    return f == e


# --------------------------- HTML → DataFrame parsers (unit-tested) ---------------------------

def parse_first_table_matching_columns(
    html: str, expected_columns: Sequence[str], order_sensitive: bool = True
) -> Optional["pd.DataFrame"]:
    """
    Parse the first <table> whose header row matches `expected_columns` (case-insensitive).
    Returns a DataFrame or None if not found.
    """
    if pd is None:  # pragma: no cover
        raise ImportError("pandas is required for table extraction")

    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        thead = table.find("thead")
        first_row = thead.find("tr") if thead else table.find("tr")
        if not first_row:
            continue

        header_cells = first_row.find_all("th")
        if header_cells:
            headers = [extract_cell_text(th) for th in header_cells]
            data_rows = table.find_all("tr")[1:]
        else:
            td_cells = first_row.find_all("td")
            headers = [extract_cell_text(td) for td in td_cells]
            data_rows = table.find_all("tr")[1:]

        if not headers or not _headers_match(
            headers, expected_columns, order_sensitive=order_sensitive
        ):
            continue

        rows: List[List[str]] = []
        for tr in data_rows:
            cells = tr.find_all(["td", "th"])
            row = [extract_cell_text(c) for c in cells]
            if len(row) < len(headers):
                row += [""] * (len(headers) - len(row))
            elif len(row) > len(headers):
                row = row[: len(headers)]
            rows.append(row)

        return pd.DataFrame(rows, columns=list(headers))
    return None


def parse_all_tables_matching_columns(
    html: str, expected_columns: Sequence[str], order_sensitive: bool = True
) -> List["pd.DataFrame"]:
    """
    Parse all <table> elements in the HTML whose headers match `expected_columns`.
    Returns a list of DataFrames (possibly empty).
    """
    if pd is None:  # pragma: no cover
        raise ImportError("pandas is required for table extraction")

    soup = BeautifulSoup(html, "html.parser")
    dfs: List["pd.DataFrame"] = []
    for table in soup.find_all("table"):
        thead = table.find("thead")
        first_row = thead.find("tr") if thead else table.find("tr")
        if not first_row:
            continue

        header_cells = first_row.find_all("th")
        if header_cells:
            headers = [extract_cell_text(th) for th in header_cells]
            data_rows = table.find_all("tr")[1:]
        else:
            td_cells = first_row.find_all("td")
            headers = [extract_cell_text(td) for td in td_cells]
            data_rows = table.find_all("tr")[1:]

        if not headers or not _headers_match(
            headers, expected_columns, order_sensitive=order_sensitive
        ):
            continue

        rows: List[List[str]] = []
        for tr in data_rows:
            cells = tr.find_all(["td", "th"])
            row = [extract_cell_text(c) for c in cells]
            if len(row) < len(headers):
                row += [""] * (len(headers) - len(row))
            elif len(row) > len(headers):
                row = row[: len(headers)]
            rows.append(row)

        dfs.append(pd.DataFrame(rows, columns=list(headers)))
    return dfs


# --------------------------- Server helpers (uses DocumentPart) ---------------------------

def _extract_html_from_attrs(attrs: dict) -> Optional[str]:
    """
    Best-effort extraction of HTML from a part's attributes across server variants.
    """
    keys = ("content", "contentHtml", "content_html", "html")
    for k in keys:
        v = attrs.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            if isinstance(v.get("value"), str):
                return v["value"]
            if isinstance(v.get("html"), str):
                return v["html"]
    v = attrs.get("value")
    if isinstance(v, str):
        return v
    return None


# --- Synchronous Helpers ---

def _iter_document_parts(
    pc: PolarionClient,
    project_id: str,
    space_id: str,
    document_name: str,
) -> Iterable[Tuple[str, dict]]:
    dp = DocumentPart(pc)
    for item in dp.iter(project_id, space_id, document_name, page_size=100):
        part_id = item.get("id", "")
        if part_id:
            yield part_id, item


def _iter_document_parts_filtered_by_type(
    pc: PolarionClient,
    project_id: str,
    space_id: str,
    document_name: str,
    *,
    type_value: str = "table",
) -> Iterable[Tuple[str, dict]]:
    dp = DocumentPart(pc)
    parts = dp.list(
        project_id,
        space_id,
        document_name,
        page_number=1,
        page_size=-1,
        fields_parts=["type", "title"],
    )
    for it in parts:
        attrs = it.get("attributes") or {}
        if (attrs.get("type") or "").lower() == type_value:
            yield it.get("id", ""), it


def _fetch_part_html(
    pc: PolarionClient,
    project_id: str,
    space_id: str,
    document_name: str,
    part_id: str,
) -> Optional[str]:
    dp = DocumentPart(pc)
    part = dp.get(
        project_id,
        space_id,
        document_name,
        part_id.split("/")[-1],
        fields_parts="@all",
    )
    data = part.get("data") or {}
    attrs = data.get("attributes") or {}
    return _extract_html_from_attrs(attrs)


# --- Asynchronous Helpers ---

async def _iter_document_parts_async(
    pc: PolarionAsyncClient,
    project_id: str,
    space_id: str,
    document_name: str,
) -> AsyncIterable[Tuple[str, dict]]:
    dp = DocumentPart(pc)
    async for item in dp.iter(project_id, space_id, document_name, page_size=100):
        part_id = item.get("id", "")
        if part_id:
            yield part_id, item


async def _iter_document_parts_filtered_by_type_async(
    pc: PolarionAsyncClient,
    project_id: str,
    space_id: str,
    document_name: str,
    *,
    type_value: str = "table",
) -> AsyncIterable[Tuple[str, dict]]:
    dp = DocumentPart(pc)
    parts = await dp.list(
        project_id,
        space_id,
        document_name,
        page_number=1,
        page_size=-1,
        fields_parts=["type", "title"],
    )
    for it in parts:
        attrs = it.get("attributes") or {}
        if (attrs.get("type") or "").lower() == type_value:
            yield it.get("id", ""), it


async def _fetch_part_html_async(
    pc: PolarionAsyncClient,
    project_id: str,
    space_id: str,
    document_name: str,
    part_id: str,
) -> Optional[str]:
    dp = DocumentPart(pc)
    part = await dp.get(
        project_id,
        space_id,
        document_name,
        part_id.split("/")[-1],
        fields_parts="@all",
    )
    data = part.get("data") or {}
    attrs = data.get("attributes") or {}
    return _extract_html_from_attrs(attrs)


# --------------------------- Public high-level API ---------------------------

def extract_document_tables_by_columns(
    pc: PolarionClient,
    project_id: str,
    space_id: str,
    document_name: str,
    expected_columns: Sequence[str],
    *,
    all_matches: bool = False,
    prefer_type_filter: bool = True,
    order_sensitive: bool = True,
) -> Union["pd.DataFrame", List["pd.DataFrame"], None]:
    """
    List parts → (optionally) pre-filter by type='table' → fetch HTML → parse + match headers.
    Returns one DataFrame (default), all matches (list), or None/[] if none match.
    """
    if pd is None:  # pragma: no cover
        raise ImportError("pandas is required for table extraction")

    def _parse_selected(candidates: Iterable[Tuple[str, dict]]):
        if all_matches:
            out: List["pd.DataFrame"] = []
            for part_id, _ in candidates:
                html = _fetch_part_html(
                    pc, project_id, space_id, document_name, part_id
                )
                if not html:
                    continue
                df = parse_first_table_matching_columns(
                    html, expected_columns, order_sensitive=order_sensitive
                )
                if df is not None:
                    out.append(df)
            return out
        else:
            for part_id, _ in candidates:
                html = _fetch_part_html(
                    pc, project_id, space_id, document_name, part_id
                )
                if not html:
                    continue
                df = parse_first_table_matching_columns(
                    html, expected_columns, order_sensitive=order_sensitive
                )
                if df is not None:
                    return df
            return None

    # 1) Fast path: type filter (table)
    if prefer_type_filter:
        candidates = list(
            _iter_document_parts_filtered_by_type(
                pc, project_id, space_id, document_name
            )
        )
        result = _parse_selected(candidates)
        # Found something? return now.
        if (isinstance(result, list) and result) or (
            result is not None and not isinstance(result, list)
        ):
            return result

    # 2) Fallback: scan all parts (covers embedded tables in non-'table' parts)
    candidates_all = list(
        _iter_document_parts(pc, project_id, space_id, document_name)
    )
    return _parse_selected(candidates_all)


async def extract_document_tables_by_columns_async(
    pc: PolarionAsyncClient,
    project_id: str,
    space_id: str,
    document_name: str,
    expected_columns: Sequence[str],
    *,
    all_matches: bool = False,
    prefer_type_filter: bool = True,
    order_sensitive: bool = True,
) -> Union["pd.DataFrame", List["pd.DataFrame"], None]:
    """
    Asynchronous version of extract_document_tables_by_columns.
    """
    if pd is None:  # pragma: no cover
        raise ImportError("pandas is required for table extraction")

    async def _parse_selected(candidates_list: List[Tuple[str, dict]]):
        if all_matches:
            out: List["pd.DataFrame"] = []
            for part_id, _ in candidates_list:
                html = await _fetch_part_html_async(
                    pc, project_id, space_id, document_name, part_id
                )
                if not html:
                    continue
                df = parse_first_table_matching_columns(
                    html, expected_columns, order_sensitive=order_sensitive
                )
                if df is not None:
                    out.append(df)
            return out
        else:
            for part_id, _ in candidates_list:
                html = await _fetch_part_html_async(
                    pc, project_id, space_id, document_name, part_id
                )
                if not html:
                    continue
                df = parse_first_table_matching_columns(
                    html, expected_columns, order_sensitive=order_sensitive
                )
                if df is not None:
                    return df
            return None

    # 1) Fast path: type filter (table)
    if prefer_type_filter:
        # Collect all candidates first (async iter -> list)
        candidates = []
        async for c in _iter_document_parts_filtered_by_type_async(
            pc, project_id, space_id, document_name
        ):
            candidates.append(c)

        result = await _parse_selected(candidates)
        # Found something? return now.
        if (isinstance(result, list) and result) or (
            result is not None and not isinstance(result, list)
        ):
            return result

    # 2) Fallback: scan all parts
    candidates_all = []
    async for c in _iter_document_parts_async(pc, project_id, space_id, document_name):
        candidates_all.append(c)

    return await _parse_selected(candidates_all)

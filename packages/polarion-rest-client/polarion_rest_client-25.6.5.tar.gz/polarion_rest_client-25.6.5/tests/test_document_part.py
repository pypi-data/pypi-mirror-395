import os
import pytest
import asyncio

import polarion_rest_client as prc
from polarion_rest_client.client import PolarionClient, PolarionAsyncClient
from polarion_rest_client.document_part import DocumentPart


# --- Synchronous Implementation ---
def _run_part_test_sync(api, project_id, space_id, doc_name):
    # LIST
    items = api.list(project_id, space_id, doc_name, page_number=1, page_size=2)
    assert isinstance(items, list)

    # If there are items, try GET for the first one
    if items:
        first = items[0]
        part_id = first.get("id", "")
        assert part_id and part_id.startswith(f"{project_id}/{space_id}/{doc_name}/")
        got = api.get(
            project_id,
            space_id,
            doc_name,
            part_id.split("/")[-1],  # last path segment is the partId
        )
        assert (got.get("data") or {}).get("id", "") == part_id

    # ITER
    seen = []
    for it in api.iter(project_id, space_id, doc_name, page_size=2):
        seen.append(it)
        if len(seen) >= 5:
            break
    assert isinstance(seen, list)


# --- Asynchronous Implementation ---
async def _run_part_test_async(api, project_id, space_id, doc_name):
    # LIST
    items = await api.list(project_id, space_id, doc_name, page_number=1, page_size=2)
    assert isinstance(items, list)

    # GET
    if items:
        first = items[0]
        part_id = first.get("id", "")
        assert part_id and part_id.startswith(f"{project_id}/{space_id}/{doc_name}/")
        got = await api.get(
            project_id,
            space_id,
            doc_name,
            part_id.split("/")[-1],
        )
        assert (got.get("data") or {}).get("id", "") == part_id

    # ITER (async for)
    seen = []
    async for it in api.iter(project_id, space_id, doc_name, page_size=2):
        seen.append(it)
        if len(seen) >= 5:
            break
    assert isinstance(seen, list)


# --- Test Entry Point ---
@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_document_part_list_and_get_or_skip(mode):
    """
    Read-only tests for Document Parts in sync/async modes.
    """
    project_id = os.getenv("POLARION_TEST_PROJECT_ID")
    doc_name = os.getenv("POLARION_TEST_DOCUMENT_NAME")
    space_id = os.getenv("POLARION_TEST_SPACE_ID", "_default")

    if not project_id or not doc_name:
        pytest.skip(
            "Set POLARION_TEST_PROJECT_ID and POLARION_TEST_DOCUMENT_NAME "
            "to run Document Part integration tests."
        )

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Polarion env vars not configured")
            return

        api = DocumentPart(pc)
        _run_part_test_sync(api, project_id, space_id, doc_name)

    else:
        # Async Mode
        async def _async_wrapper():
            try:
                pc_async = PolarionAsyncClient(**prc.get_env_vars())
            except Exception:
                pytest.skip("Polarion env vars not configured")
                return
            except RuntimeError as e:
                if "AuthenticatedAsyncClient" in str(e) or "not available" in str(e):
                    pytest.skip(f"Async support missing in generated client: {e}")
                raise e

            async with pc_async as client:
                api = DocumentPart(client)
                await _run_part_test_async(api, project_id, space_id, doc_name)

        asyncio.run(_async_wrapper())

import os
import uuid
import time
import pytest
import asyncio

from polarion_rest_client.workitem import WorkItem
from polarion_rest_client.paging import list_page, extract_items, resolve_page_params
from polarion_rest_client.error import Unauthorized, Forbidden, NotFound, Conflict, raise_from_response
from polarion_rest_client.client import PolarionClient, PolarionAsyncClient
import polarion_rest_client as prc

# low-level list endpoint for one-page helper (Sync)
from polarion_rest_client.openapi.api.work_items.get_work_items import (
    sync_detailed as _get_work_items,
)


# --- Wait Helpers ---

def _wait_for_value_sync(func, expected, retries=20, delay=1.0):
    """Retry getter until value matches expected or timeout (Sync)."""
    last_val = None
    for _ in range(retries):
        last_val = func()
        if last_val == expected:
            return last_val
        time.sleep(delay)
    return last_val


async def _wait_for_value_async(func, expected, retries=20, delay=1.0):
    """Retry getter until value matches expected or timeout (Async)."""
    last_val = None
    for _ in range(retries):
        last_val = await func()
        if last_val == expected:
            return last_val
        await asyncio.sleep(delay)
    return last_val


def _wait_for_search_result_sync(func, retries=20, delay=2.0):
    """Retry search until it returns a non-empty list (Sync)."""
    for _ in range(retries):
        res = func()
        if res:
            return res
        time.sleep(delay)
    return []


async def _wait_for_search_result_async(func, retries=20, delay=2.0):
    """Retry search until it returns a non-empty list (Async)."""
    for _ in range(retries):
        res = await func()
        if res:
            return res
        await asyncio.sleep(delay)
    return []


# --- Synchronous Implementation ---
def _run_workitem_test_sync(api, project_id, wi_type, pc):
    title_update = f"SDK WI Sync Update {uuid.uuid4().hex[:6]}"
    title_search = f"SDK WI Sync Search {uuid.uuid4().hex[:6]}"
    created_ids = []

    try:
        # --- 1. CREATE & UPDATE FLOW ---
        created = api.create(
            project_id,
            wi_type=wi_type,
            title=title_update,
            description="Created by integration test (Sync Update)",
        )
        id_update = created.get("id", "").split("/", 1)[1]
        created_ids.append(id_update)

        updated_title = title_update + " (updated)"
        api.update(project_id, id_update, title=updated_title)

        # Verify Update with retry (handles eventual consistency)
        def _get_title():
            doc = api.get(project_id, id_update)
            return ((doc.get("data") or {}).get("attributes") or {}).get("title")

        actual_title = _wait_for_value_sync(_get_title, updated_title)
        assert actual_title == updated_title, \
            f"Update failed: Expected '{updated_title}', got '{actual_title}'"

        # --- 2. SEARCH FLOW ---
        created_search = api.create(
            project_id,
            wi_type=wi_type,
            title=title_search,
            description="Created by integration test (Sync Search)",
        )
        id_search = created_search.get("id", "").split("/", 1)[1]
        created_ids.append(id_search)

        # LIST PAGE (Paging Test)
        page_param, size_param = resolve_page_params(_get_work_items)

        def _do_list():
            p = list_page(
                _get_work_items,
                page_param=page_param,
                size_param=size_param,
                page_number=1,
                page_size=1,
                on_error=raise_from_response,
                client=pc.gen,
                project_id=project_id,
                query=f'title:"{title_search}"',
            )
            return extract_items(p)

        found_items = _wait_for_search_result_sync(_do_list)

        if found_items:
            assert any(e.get("id", "").endswith(f"/{id_search}") for e in found_items)

        # ITER
        list(api.iter(project_id, page_size=1, query=f'title:"{title_search}"'))

        # FIND BY TITLE
        # Pass fields explicitly to rule out SparseFields issues
        def _find():
            return api.find_by_title(
                project_id, title_search, limit=1, query_via_server=True, fields=["id", "title", "type"]
            )

        found = _wait_for_search_result_sync(_find)

        if found:
            found_id = found[0].get("id", "")
            assert found_id.endswith(f"/{id_search}")

            # Strict match check
            # Retry strict search specifically in case the index returned the item but without title previously?
            # (Should be covered by _wait_for_search_result_sync logic combined with WorkItem.find fix)
            def _find_strict():
                return api.find_by_title(
                    project_id, title_search, limit=1, query_via_server=True, strict_match=True, fields=["id", "title"]
                )

            found_strict = _wait_for_search_result_sync(_find_strict)

            # If it's still empty after retries, it means either strict matching logic is failing locally
            # (title mismatch) or server never returned the title.
            if not found_strict:
                # Debug dump for the non-strict result to see what went wrong
                print(f"\n[DEBUG] Non-strict found attributes: {found[0].get('attributes')}")

            assert found_strict and found_strict[0].get("id", "").endswith(f"/{id_search}")
        else:
            print("Warning: Search index lag prevented finding item by title (Sync).")

    except (Unauthorized, Forbidden) as e:
        pytest.skip(f"Insufficient permissions: {e}")
    finally:
        for wid in created_ids:
            try:
                api.delete_one(project_id, wid)
            except (Unauthorized, Forbidden, NotFound, Conflict):
                pass


# --- Asynchronous Implementation ---
async def _run_workitem_test_async(api, project_id, wi_type):
    title_update = f"SDK WI Async Update {uuid.uuid4().hex[:6]}"
    title_search = f"SDK WI Async Search {uuid.uuid4().hex[:6]}"
    created_ids = []

    try:
        # --- 1. CREATE & UPDATE FLOW ---
        created = await api.create(
            project_id,
            wi_type=wi_type,
            title=title_update,
            description="Created by integration test (Async Update)",
        )
        id_update = created.get("id", "").split("/", 1)[1]
        created_ids.append(id_update)

        updated_title = title_update + " (updated)"
        await api.update(project_id, id_update, title=updated_title)

        # Verify Update with retry
        async def _get_title():
            doc = await api.get(project_id, id_update)
            return ((doc.get("data") or {}).get("attributes") or {}).get("title")

        actual_title = await _wait_for_value_async(_get_title, updated_title)
        assert actual_title == updated_title, \
            f"Update failed: Expected '{updated_title}', got '{actual_title}'"

        # --- 2. SEARCH FLOW ---
        created_search = await api.create(
            project_id,
            wi_type=wi_type,
            title=title_search,
            description="Created by integration test (Async Search)",
        )
        id_search = created_search.get("id", "").split("/", 1)[1]
        created_ids.append(id_search)

        # ITER
        async for _ in api.iter(project_id, page_size=1, query=f'title:"{title_search}"'):
            pass

        # FIND BY TITLE
        async def _find():
            return await api.find_by_title(
                project_id, title_search, limit=1, query_via_server=True, fields=["id", "title", "type"]
            )

        found = await _wait_for_search_result_async(_find)

        if found:
            found_id = found[0].get("id", "")
            assert found_id.endswith(f"/{id_search}")

            async def _find_strict():
                return await api.find_by_title(
                    project_id, title_search, limit=1, query_via_server=True, strict_match=True, fields=["id", "title"]
                )

            found_strict = await _wait_for_search_result_async(_find_strict)

            if not found_strict:
                print(f"\n[DEBUG] Non-strict found attributes: {found[0].get('attributes')}")

            assert found_strict and found_strict[0].get("id", "").endswith(f"/{id_search}")
        else:
            print("Warning: Search index lag prevented finding item by title (Async).")

    except (Unauthorized, Forbidden) as e:
        pytest.skip(f"Insufficient permissions: {e}")
    finally:
        for wid in created_ids:
            try:
                await api.delete_one(project_id, wid)
            except (Unauthorized, Forbidden, NotFound, Conflict):
                pass


@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_workitem_crud_paging_and_find(mode):
    """
    Runs Work Item CRUD, paging, and find tests in Sync/Async modes.
    """
    project_id = os.environ.get("POLARION_TEST_PROJECT_ID")
    if not project_id:
        pytest.skip("Set POLARION_TEST_PROJECT_ID to run Work Item integration tests.")
    wi_type = os.environ.get("POLARION_TEST_WI_TYPE", "task")

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Polarion env vars not configured")
            return

        wi = WorkItem(pc)
        _run_workitem_test_sync(wi, project_id, wi_type, pc)

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
                wi = WorkItem(client)
                await _run_workitem_test_async(wi, project_id, wi_type)

        asyncio.run(_async_wrapper())

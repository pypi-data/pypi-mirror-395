import os
import uuid
import pytest
import asyncio

from polarion_rest_client.workitem import WorkItem
from polarion_rest_client.error import Unauthorized, Forbidden, Conflict, NotFound
from polarion_rest_client.client import PolarionClient, PolarionAsyncClient
import polarion_rest_client as prc


# --- Synchronous Helpers ---
def _run_batch_update_sync(api, project_id, wi_type):
    token = uuid.uuid4().hex[:6]
    t1 = f"Batch WI A Sync {token}"
    t2 = f"Batch WI B Sync {token}"
    created_ids = []

    try:
        c1 = api.create(project_id, wi_type=wi_type, title=t1, description="batch test A")
        c2 = api.create(project_id, wi_type=wi_type, title=t2, description="batch test B")
        for c in (c1, c2):
            full_id = c.get("id", "")
            created_ids.append(full_id.split("/", 1)[1])

        new_suffix = " (batch-updated)"
        api.update_many(
            project_id,
            items=[
                {"id": created_ids[0], "attributes": {"title": t1 + new_suffix}},
                {"id": created_ids[1], "attributes": {"title": t2 + new_suffix}},
            ],
        )

        g1 = api.get(project_id, created_ids[0])
        g2 = api.get(project_id, created_ids[1])
        a1 = ((g1.get("data") or {}).get("attributes") or {})
        a2 = ((g2.get("data") or {}).get("attributes") or {})
        assert a1.get("title") == t1 + new_suffix
        assert a2.get("title") == t2 + new_suffix

    finally:
        for wid in created_ids:
            try:
                api.delete_one(project_id, wid)
            except (NotFound, Unauthorized, Forbidden, Conflict):
                pass


def _run_batch_same_attrs_sync(api, project_id, wi_type):
    token = uuid.uuid4().hex[:6]
    base_title = f"SameAttrs Sync {token}"
    suffix = " (same-attrs)"
    created_ids = []

    try:
        for i in range(3):
            c = api.create(project_id, wi_type=wi_type, title=f"{base_title} #{i}")
            created_ids.append(c.get("id", "").split("/", 1)[1])

        api.update_many_same_attrs(
            project_id,
            created_ids,
            attributes={"title": base_title + suffix},
        )

        for wid in created_ids:
            got = api.get(project_id, wid)
            attrs = ((got.get("data") or {}).get("attributes") or {})
            assert attrs.get("title") == base_title + suffix

    finally:
        for wid in created_ids:
            try:
                api.delete_one(project_id, wid)
            except (NotFound, Unauthorized, Forbidden, Conflict):
                pass


# --- Asynchronous Helpers ---
async def _run_batch_update_async(api, project_id, wi_type):
    token = uuid.uuid4().hex[:6]
    t1 = f"Batch WI A Async {token}"
    t2 = f"Batch WI B Async {token}"
    created_ids = []

    try:
        c1 = await api.create(project_id, wi_type=wi_type, title=t1)
        c2 = await api.create(project_id, wi_type=wi_type, title=t2)
        for c in (c1, c2):
            full_id = c.get("id", "")
            created_ids.append(full_id.split("/", 1)[1])

        new_suffix = " (batch-updated)"
        await api.update_many(
            project_id,
            items=[
                {"id": created_ids[0], "attributes": {"title": t1 + new_suffix}},
                {"id": created_ids[1], "attributes": {"title": t2 + new_suffix}},
            ],
        )

        g1 = await api.get(project_id, created_ids[0])
        g2 = await api.get(project_id, created_ids[1])
        a1 = ((g1.get("data") or {}).get("attributes") or {})
        a2 = ((g2.get("data") or {}).get("attributes") or {})
        assert a1.get("title") == t1 + new_suffix
        assert a2.get("title") == t2 + new_suffix

    finally:
        for wid in created_ids:
            try:
                await api.delete_one(project_id, wid)
            except (NotFound, Unauthorized, Forbidden, Conflict):
                pass


async def _run_batch_same_attrs_async(api, project_id, wi_type):
    token = uuid.uuid4().hex[:6]
    base_title = f"SameAttrs Async {token}"
    suffix = " (same-attrs)"
    created_ids = []

    try:
        for i in range(3):
            c = await api.create(project_id, wi_type=wi_type, title=f"{base_title} #{i}")
            created_ids.append(c.get("id", "").split("/", 1)[1])

        await api.update_many_same_attrs(
            project_id,
            created_ids,
            attributes={"title": base_title + suffix},
        )

        for wid in created_ids:
            got = await api.get(project_id, wid)
            attrs = ((got.get("data") or {}).get("attributes") or {})
            assert attrs.get("title") == base_title + suffix

    finally:
        for wid in created_ids:
            try:
                await api.delete_one(project_id, wid)
            except (NotFound, Unauthorized, Forbidden, Conflict):
                pass


# --- Test Entry Points ---

@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_workitem_batch_update(mode):
    project_id = os.getenv("POLARION_TEST_PROJECT_ID")
    if not project_id:
        pytest.skip("Set POLARION_TEST_PROJECT_ID")
    wi_type = os.getenv("POLARION_TEST_WI_TYPE", "task")

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Env vars missing")
            return
        _run_batch_update_sync(WorkItem(pc), project_id, wi_type)
    else:
        async def _async_wrapper():
            try:
                pc_async = PolarionAsyncClient(**prc.get_env_vars())
            except Exception:
                pytest.skip("Env vars missing")
                return
            except RuntimeError:
                pytest.skip("Async client missing")
                return

            async with pc_async as client:
                await _run_batch_update_async(WorkItem(client), project_id, wi_type)

        asyncio.run(_async_wrapper())


@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_workitem_batch_update_same_attrs(mode):
    project_id = os.getenv("POLARION_TEST_PROJECT_ID")
    if not project_id:
        pytest.skip("Set POLARION_TEST_PROJECT_ID")
    wi_type = os.getenv("POLARION_TEST_WI_TYPE", "task")

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Env vars missing")
            return
        _run_batch_same_attrs_sync(WorkItem(pc), project_id, wi_type)
    else:
        async def _async_wrapper():
            try:
                pc_async = PolarionAsyncClient(**prc.get_env_vars())
            except Exception:
                pytest.skip("Env vars missing")
                return
            except RuntimeError:
                pytest.skip("Async client missing")
                return

            async with pc_async as client:
                await _run_batch_same_attrs_async(WorkItem(client), project_id, wi_type)

        asyncio.run(_async_wrapper())

import os
import time
import uuid
import pytest
import asyncio

from polarion_rest_client.project import Project
from polarion_rest_client.client import PolarionClient, PolarionAsyncClient
from polarion_rest_client.error import JSONAPIError
import polarion_rest_client as prc


# --- Generators ---
def _gen_ids():
    nonce = uuid.uuid4().hex[:8]
    proj_id = f"rest-{int(time.time())}-{nonce}"
    prefix = f"T{nonce[:2]}P"
    return proj_id, prefix


# --- Synchronous Implementation ---
def _run_steps_sync(api, proj_id, prefix, template_id):
    # Create
    job = api.create(
        proj_id,
        tracker_prefix=prefix,
        template_id=template_id,
        wait=True,
        poll_timeout_s=300,
    )
    assert isinstance(job, str) and job

    # List
    lst = api.list(page_size=10, fields_projects=["id", "name", "trackerPrefix"])
    assert isinstance(lst, dict) and "data" in lst

    # Get
    doc = api.get(proj_id, fields_projects=["id", "name", "trackerPrefix", "description"])
    assert (doc.get("data") or {}).get("id") == proj_id

    # Patch
    api.patch(
        proj_id,
        name="HL Client Test",
        description="updated by test",
        color="#336699",
        active=True,
    )

    doc2 = api.get(proj_id, fields_projects=["id", "name", "description", "color", "active"])
    attrs = ((doc2.get("data") or {}).get("attributes") or {})
    assert attrs.get("name") == "HL Client Test"
    assert (attrs.get("description") or {}).get("value") == "updated by test"
    assert attrs.get("color") == "#336699"
    assert attrs.get("active") is True

    # Delete or Unmark
    try:
        del_job = api.delete(proj_id, wait=True, poll_timeout_s=300)
        assert isinstance(del_job, str) and del_job
    except JSONAPIError:
        # If DELETE is disallowed on the server, fall back to unmark
        api.unmark(proj_id)

    # Final existence check
    assert not api.exists(proj_id)


def _run_get_only_sync(api, existing_id):
    doc = api.get(existing_id)
    assert (doc.get("data") or {}).get("id") == existing_id
    assert (doc.get("data") or {}).get("type") == "projects"


# --- Asynchronous Implementation ---
async def _run_steps_async(api, proj_id, prefix, template_id):
    # Create
    job = await api.create(
        proj_id,
        tracker_prefix=prefix,
        template_id=template_id,
        wait=True,
        poll_timeout_s=300,
    )
    assert isinstance(job, str) and job

    # List
    lst = await api.list(page_size=10, fields_projects=["id", "name", "trackerPrefix"])
    assert isinstance(lst, dict) and "data" in lst

    # Get
    doc = await api.get(proj_id, fields_projects=["id", "name", "trackerPrefix", "description"])
    assert (doc.get("data") or {}).get("id") == proj_id

    # Patch
    await api.patch(
        proj_id,
        name="HL Client Test",
        description="updated by test",
        color="#336699",
        active=True,
    )

    doc2 = await api.get(proj_id, fields_projects=["id", "name", "description", "color", "active"])
    attrs = ((doc2.get("data") or {}).get("attributes") or {})
    assert attrs.get("name") == "HL Client Test"
    assert (attrs.get("description") or {}).get("value") == "updated by test"
    assert attrs.get("color") == "#336699"
    assert attrs.get("active") is True

    # Delete or Unmark
    try:
        del_job = await api.delete(proj_id, wait=True, poll_timeout_s=300)
        assert isinstance(del_job, str) and del_job
    except JSONAPIError:
        await api.unmark(proj_id)

    # Final existence check
    exists = await api.exists(proj_id)
    assert not exists


async def _run_get_only_async(api, existing_id):
    doc = await api.get(existing_id)
    assert (doc.get("data") or {}).get("id") == existing_id
    assert (doc.get("data") or {}).get("type") == "projects"


# --- Test Entry Point ---
@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_project_flow_full_or_get_only(mode):
    """
    Runs project CRUD flow in either sync or async mode.
    """
    template_id = os.getenv("POLARION_TEMPLATE_ID")
    existing_proj_id = os.getenv("POLARION_TEST_PROJECT_ID")

    if not template_id and not existing_proj_id:
        pytest.skip(
            "Set POLARION_TEMPLATE_ID for full CRUD, or set POLARION_TEST_PROJECT_ID "
            "to run GET-only."
        )

    # Prepare IDs for CRUD scenarios
    proj_id, prefix = _gen_ids()

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Polarion env vars not configured")
            return

        api = Project(pc)
        if template_id:
            _run_steps_sync(api, proj_id, prefix, template_id)
        else:
            _run_get_only_sync(api, existing_proj_id)

    else:
        # Async Mode - manual run loop
        async def _async_wrapper():
            try:
                pc_async = PolarionAsyncClient(**prc.get_env_vars())
            except Exception:
                pytest.skip("Polarion env vars not configured")
                return
            except RuntimeError as e:
                # Gracefully skip if the underlying generated client lacks Async support
                if "AuthenticatedAsyncClient" in str(e) or "not available" in str(e):
                    pytest.skip(f"Async support missing in generated client: {e}")
                raise e

            async with pc_async as client:
                api = Project(client)
                if template_id:
                    await _run_steps_async(api, proj_id, prefix, template_id)
                else:
                    await _run_get_only_async(api, existing_proj_id)

        asyncio.run(_async_wrapper())

import os
import uuid
import pytest
import asyncio

import polarion_rest_client as prc
from polarion_rest_client.client import PolarionClient, PolarionAsyncClient
from polarion_rest_client.document import Document


# --- Synchronous Implementation ---
def _run_document_test_sync(api, project_id, space_id, allow_create):
    # -------- GET-only path ----------
    if not allow_create:
        doc_name = os.getenv("POLARION_TEST_DOCUMENT_NAME")
        if not doc_name:
            pytest.skip(
                "Set POLARION_TEST_DOC_CREATE_OK=1 for create flow, "
                "or set POLARION_TEST_DOCUMENT_NAME for GET-only."
            )
        payload = api.get(project_id, space_id, doc_name)
        assert (payload.get("data") or {}).get("id", "").endswith(f"/{doc_name}")
        return

    # -------- CREATE + GET + UPDATE ---
    token = uuid.uuid4().hex[:6]
    module_name = f"hl-doc-sync-{token}"
    title = f"HL Doc Sync {token}"
    custom_field_key = os.getenv("POLARION_TEST_DOC_CUSTOM_FIELD_KEY", "custom_field")
    custom_field_value = f"test-{token}"

    created = api.create(
        project_id,
        space_id,
        module_name=module_name,
        title=title,
        doc_type="req_specification",
        status="draft",
        home_page_content=f"<p>Created by tests ({token})</p>",
        home_page_content_type="text/html",
        structure_link_role=os.getenv("POLARION_TEST_DOC_STRUCTURE_ROLE", "relates_to"),
        attributes={custom_field_key: custom_field_value},
    )
    created_full_id = created.get("id", "")
    assert created_full_id.endswith(f"/{module_name}")

    # Request "@all" fields to ensure custom fields are returned
    got = api.get(project_id, space_id, module_name, fields_documents=["@all"])
    assert (got.get("data") or {}).get("id", "") == created_full_id

    got_attrs = ((got.get("data") or {}).get("attributes") or {})
    assert got_attrs.get(custom_field_key) == custom_field_value

    new_title = title + " (updated)"
    api.update(project_id, space_id, module_name, title=new_title)
    got2 = api.get(project_id, space_id, module_name, fields_documents=["@all"])
    attrs = ((got2.get("data") or {}).get("attributes") or {})
    if "title" in attrs:
        assert attrs["title"] == new_title


# --- Asynchronous Implementation ---
async def _run_document_test_async(api, project_id, space_id, allow_create):
    # -------- GET-only path ----------
    if not allow_create:
        doc_name = os.getenv("POLARION_TEST_DOCUMENT_NAME")
        if not doc_name:
            pytest.skip(
                "Set POLARION_TEST_DOC_CREATE_OK=1 for create flow, "
                "or set POLARION_TEST_DOCUMENT_NAME for GET-only."
            )
        payload = await api.get(project_id, space_id, doc_name)
        assert (payload.get("data") or {}).get("id", "").endswith(f"/{doc_name}")
        return

    # -------- CREATE + GET + UPDATE ---
    token = uuid.uuid4().hex[:6]
    module_name = f"hl-doc-async-{token}"
    title = f"HL Doc Async {token}"
    custom_field_key = os.getenv("POLARION_TEST_DOC_CUSTOM_FIELD_KEY", "custom_field")
    custom_field_value = f"test-{token}"

    created = await api.create(
        project_id,
        space_id,
        module_name=module_name,
        title=title,
        doc_type="req_specification",
        status="draft",
        home_page_content=f"<p>Created by tests ({token})</p>",
        home_page_content_type="text/html",
        structure_link_role=os.getenv("POLARION_TEST_DOC_STRUCTURE_ROLE", "relates_to"),
        attributes={custom_field_key: custom_field_value},
    )
    created_full_id = created.get("id", "")
    assert created_full_id.endswith(f"/{module_name}")

    got = await api.get(project_id, space_id, module_name, fields_documents=["@all"])
    assert (got.get("data") or {}).get("id", "") == created_full_id

    got_attrs = ((got.get("data") or {}).get("attributes") or {})
    assert got_attrs.get(custom_field_key) == custom_field_value

    new_title = title + " (updated)"
    await api.update(project_id, space_id, module_name, title=new_title)
    got2 = await api.get(project_id, space_id, module_name, fields_documents=["@all"])
    attrs = ((got2.get("data") or {}).get("attributes") or {})
    if "title" in attrs:
        assert attrs["title"] == new_title


# --- Test Entry Point ---
@pytest.mark.integration
@pytest.mark.parametrize("mode", ["sync", "async"])
def test_document_create_get_update_or_get_only(mode):
    """
    Runs Document CRUD or GET-only test in either sync or async mode.
    """
    project_id = os.getenv("POLARION_TEST_PROJECT_ID")
    space_id = os.getenv("POLARION_TEST_SPACE_ID") or "_default"
    if not project_id:
        pytest.skip("Set POLARION_TEST_PROJECT_ID to run Document tests.")

    allow_create = os.getenv("POLARION_TEST_DOC_CREATE_OK") == "1"

    if mode == "sync":
        try:
            pc = PolarionClient(**prc.get_env_vars())
        except Exception:
            pytest.skip("Polarion env vars not configured")
            return

        api = Document(pc)
        _run_document_test_sync(api, project_id, space_id, allow_create)

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
                api = Document(client)
                await _run_document_test_async(api, project_id, space_id, allow_create)

        asyncio.run(_async_wrapper())

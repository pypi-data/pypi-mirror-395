import pytest
import polarion_rest_client as hl


def test_version_exposed():
    assert isinstance(hl.__version__, str)


@pytest.mark.parametrize("ClientClass", [hl.PolarionClient, hl.PolarionAsyncClient])
def test_client_requires_auth(ClientClass):
    # constructing without token or username+password must fail
    with pytest.raises(ValueError):
        ClientClass(base_url="https://example.invalid")


@pytest.mark.parametrize("ClientClass", [hl.PolarionClient, hl.PolarionAsyncClient])
def test_get_env_vars_and_client(monkeypatch, ClientClass):
    # Disable dotenv loading for this test to ensure isolation
    monkeypatch.setattr("polarion_rest_client.session.load_dotenv", None)

    # Missing URL should fail
    monkeypatch.delenv("POLARION_TEST_URL", raising=False)
    monkeypatch.delenv("POLARION_TOKEN", raising=False)
    monkeypatch.delenv("POLARION_USERNAME", raising=False)
    monkeypatch.delenv("POLARION_PASSWORD", raising=False)

    with pytest.raises(ValueError, match="POLARION_TEST_URL is required"):
        hl.get_env_vars(base_url_var="POLARION_TEST_URL")

    # Token path
    monkeypatch.setenv("POLARION_TEST_URL", "https://example.invalid")
    monkeypatch.setenv("POLARION_TOKEN", "dummy-token")

    kwargs = hl.get_env_vars(base_url_var="POLARION_TEST_URL")
    pc = ClientClass(**kwargs)
    assert pc.gen is not None
    assert pc.base_url.endswith("/polarion/rest/v1")

    # Basic auth path
    monkeypatch.delenv("POLARION_TOKEN", raising=False)
    monkeypatch.setenv("POLARION_USERNAME", "u")
    monkeypatch.setenv("POLARION_PASSWORD", "p")

    kwargs = hl.get_env_vars(base_url_var="POLARION_TEST_URL")
    pc = ClientClass(**kwargs)
    assert pc.gen is not None


def test_get_env_vars_loads_dotenv(monkeypatch, tmp_path):
    # Check if dotenv is installed, skip if not
    try:
        import dotenv  # noqa
    except ImportError:
        pytest.skip("python-dotenv not installed, skipping .env test")

    # Create a dummy .env file
    p = tmp_path / ".env"
    p.write_text(
        'POLARION_TEST_URL="https://from.dotenv/test"\n'
        'POLARION_TOKEN="dotenv-token"\n'
    )

    # Change directory to where the .env file is
    monkeypatch.chdir(tmp_path)

    # Clear any existing env vars that might conflict
    monkeypatch.delenv("POLARION_TEST_URL", raising=False)
    monkeypatch.delenv("POLARION_TOKEN", raising=False)
    monkeypatch.delenv("POLARION_USERNAME", raising=False)
    monkeypatch.delenv("POLARION_PASSWORD", raising=False)

    # Run get_env_vars, pointing it explicitly to our test .env file
    kwargs = hl.get_env_vars(
        _dotenv_path=str(p),
        base_url_var="POLARION_TEST_URL",
        token_var="POLARION_TOKEN"
    )

    assert kwargs["base_url"] == "https://from.dotenv/test"
    assert kwargs["token"] == "dotenv-token"

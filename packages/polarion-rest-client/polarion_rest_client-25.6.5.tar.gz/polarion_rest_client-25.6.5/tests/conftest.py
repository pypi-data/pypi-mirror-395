import dotenv
import pytest

import polarion_rest_client as prc


@pytest.fixture
def dotenv_test_env():
    """
    Load environment variables from .env.test.
    If file is missing, checks if variables are already set (e.g. CI/CD).
    """
    if not dotenv.load_dotenv(".env.test"):
        try:
            prc.get_env_vars()
        except ValueError:
            pytest.skip("Polarion env not configured for integration tests")


@pytest.fixture
def polarion_test_client(dotenv_test_env):
    """
    Provides a synchronous PolarionClient.
    """
    try:
        return prc.PolarionClient(**prc.get_env_vars())
    except Exception as e:
        raise ValueError(f"Invalid test env configuration: {e}") from e


@pytest.fixture
async def polarion_test_async_client(dotenv_test_env):
    """
    Provides an asynchronous PolarionAsyncClient.
    Yields the client within an active async context.
    """
    try:
        async with prc.PolarionAsyncClient(**prc.get_env_vars()) as client:
            yield client
    except RuntimeError as e:
        # Gracefully skip if the underlying generated client lacks Async support
        if "AuthenticatedAsyncClient" in str(e) or "not available" in str(e):
            pytest.skip(f"Async support missing in generated client: {e}")
        raise e
    except Exception as e:
        raise ValueError(f"Invalid test env configuration: {e}") from e

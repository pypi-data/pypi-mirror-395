import copy
import logging
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

from edison_client import EdisonClient
from edison_client.models.app import AuthType, RuntimeConfig, TaskRequest, TaskResponse
from edison_client.utils.auth import RefreshingJWT


@pytest.fixture(name="mock_client")
def fixture_mock_client():
    """Create a mock synchronous HTTP client that returns success on first auth attempt."""
    client = MagicMock(spec=httpx.Client)
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "access_token": "test_token_from_api",
        "expires_in": 300,
    }
    client.post.return_value = response
    return client


@pytest.fixture(name="failing_then_success_client")
def fixture_failing_then_success_client():
    """Create a client that fails with 401 on first call, then succeeds on retry."""
    client = MagicMock(spec=httpx.Client)

    first_response = MagicMock(status_code=401)
    success_response = MagicMock()
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {
        "access_token": "refreshed_token",
        "expires_in": 300,
    }

    client.post.return_value = success_response

    return client, first_response


def test_refreshing_jwt_with_api_key(mock_client):
    """Test that RefreshingJWT works with API key authentication."""
    api_key = "mock_api_key_12345"

    auth = RefreshingJWT(
        auth_client=mock_client, auth_type=AuthType.API_KEY, api_key=api_key
    )

    assert auth._jwt == "test_token_from_api"

    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert args[0] == "/auth/login"
    assert "json" in kwargs
    assert kwargs["json"] == {"api_key": api_key}


def test_refreshing_jwt_with_jwt_token():
    """Test that RefreshingJWT works with JWT authentication."""
    jwt_token = "mock.jwt.token"

    auth = RefreshingJWT(auth_client=MagicMock(), auth_type=AuthType.JWT, jwt=jwt_token)

    assert auth._jwt == jwt_token


def test_refreshing_jwt_refresh_token(mock_client):
    """Test that refresh_token method correctly gets a new token."""
    api_key = "mock_api_key_12345"

    auth = RefreshingJWT(
        auth_client=mock_client, auth_type=AuthType.API_KEY, api_key=api_key
    )

    original_token = auth._jwt

    new_response = MagicMock()
    new_response.raise_for_status.return_value = None
    new_response.json.return_value = {
        "access_token": "new_refreshed_token",
        "expires_in": 300,
    }
    mock_client.post.return_value = new_response

    auth.refresh_token()

    assert auth._jwt == "new_refreshed_token"
    assert auth._jwt != original_token

    assert mock_client.post.call_count == 2  # Initial auth + refresh


def test_refreshing_jwt_refresh_token_jwt_auth_fails():
    """Test that refresh_token raises an error with JWT auth type."""
    jwt_token = "mock.jwt.token"

    auth = RefreshingJWT(auth_client=MagicMock(), auth_type=AuthType.JWT, jwt=jwt_token)

    with pytest.raises(ValueError) as excinfo:  # noqa: PT011
        auth.refresh_token()

    assert "API key auth is required to refresh auth tokens" in str(excinfo.value)


def test_auth_flow_with_retry(failing_then_success_client, caplog):
    """Test that auth_flow retries with new token after receiving a 401."""
    caplog.set_level(logging.INFO, logger="edison_client.utils.auth")

    client, first_response = failing_then_success_client
    api_key = "mock_api_key_12345"
    auth = RefreshingJWT(
        auth_client=client, auth_type=AuthType.API_KEY, api_key=api_key
    )
    request = httpx.Request("GET", "https://fh.org/api/v1/trajectories?status=pending")

    flow = auth.auth_flow(request)
    first_request = next(flow)
    assert first_request.headers["Authorization"] == f"Bearer {auth._jwt}"

    second_request = flow.send(first_response)
    assert auth._jwt == "refreshed_token"
    assert second_request.headers["Authorization"] == "Bearer refreshed_token"
    success_response = httpx.Response(200)

    try:
        flow.send(success_response)
        pytest.fail("Generator should have exited after processing the response")
    except StopIteration:
        pass

    client.post.assert_called_with("/auth/login", json={"api_key": api_key})

    assert any(
        "Received 401 for request [GET https://fh.org/api/v1/trajectories?status=pending]"
        in record.message
        for record in caplog.records
    )


def test_task_response_does_not_mutate_original_data():
    """Test that TaskResponse doesn't mutate the original data when creating an instance."""
    original_data: dict[str, Any] = {
        "crow": "test-crow",
        "task": "test task",
        "metadata": {
            "environment_name": "test-env",
            "agent_name": "test-agent",
            "some_other_field": "should not be modified",
        },
        "status": "success",
        "created_at": datetime.now(),
        "share_status": "PUBLIC",
    }

    original_data_copy = copy.deepcopy(original_data)

    task_response = TaskResponse(**original_data)

    assert original_data == original_data_copy, "Original data was mutated"

    # Assert the fields are set correctly
    assert task_response.job_name == original_data["crow"]
    assert task_response.query == original_data["task"]
    metadata = original_data.get("metadata", {})
    assert task_response.environment_name == metadata.get("environment_name")
    assert task_response.agent_name == metadata.get("agent_name")


def test_create_task_raises_error_with_both_files_parameter_and_env_config():
    """Test that create_task raises ValueError when both files parameter and environment config files are provided."""
    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(api_key="test_key")

    task_data = TaskRequest(
        name="test-job",
        query="Test query",
        runtime_config=RuntimeConfig(
            environment_config={"data_storage_uris": ["data_entry:existing-uri"]}
        ),
    )

    files = ["data_entry:new-uri"]

    with pytest.raises(
        ValueError,
        match="Please provide file uris either in the files parameter or within the environment configuration, not both",
    ):
        client.create_task(task_data, files=files)


@pytest.mark.asyncio
async def test_acreate_task_raises_error_with_both_files_parameter_and_env_config():
    """Test that acreate_task raises ValueError when both files parameter and environment config files are provided."""
    with patch(
        "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
        return_value=["test-org"],
    ):
        client = EdisonClient(api_key="test_key")

    task_data = TaskRequest(
        name="test-job",
        query="Test query",
        runtime_config=RuntimeConfig(
            environment_config={"data_storage_uris": ["data_entry:existing-uri"]}
        ),
    )

    files = ["data_entry:new-uri"]

    with pytest.raises(
        ValueError,
        match="Please provide file uris either in the files parameter or within the environment configuration, not both",
    ):
        await client.acreate_task(task_data, files=files)

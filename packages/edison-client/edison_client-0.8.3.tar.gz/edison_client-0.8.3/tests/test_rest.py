import asyncio
import datetime
import os
import time
from typing import cast
from unittest.mock import MagicMock, Mock, patch
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import (
    CloseError,
    ConnectError,
    ConnectTimeout,
    HTTPStatusError,
    NetworkError,
    ReadError,
    ReadTimeout,
    RemoteProtocolError,
)
from pytest_subtests import SubTests
from requests.exceptions import RequestException, Timeout

from edison_client.clients import (
    JobNames,
)
from edison_client.clients.rest_client import (
    FileUploadError,
    JobEventBatchCreationError,
    JobEventCreationError,
    JobEventUpdateError,
    ProjectError,
    RestClient,
    UserAgentRequestCreationError,
    UserAgentRequestFetchError,
)
from edison_client.models.app import (
    LiteTaskResponse,
    PhoenixTaskResponse,
    PQATaskResponse,
    Stage,
    TaskRequest,
    TaskResponse,
    TaskResponseVerbose,
)
from edison_client.models.job_event import (
    CostComponent,
    ExecutionType,
    JobEventBatchCreateRequest,
    JobEventBatchItemRequest,
    JobEventCreateRequest,
    JobEventUpdateRequest,
)
from edison_client.models.rest import (
    ExecutionStatus,
    UserAgentRequestPostPayload,
    UserAgentRequestStatus,
    UserAgentResponsePayload,
    WorldModel,
)
from edison_client.utils.general import create_retry_if_connection_error

TEST_MAX_POLLS = 100
ADMIN_API_KEY = os.environ.get("PLAYWRIGHT_ADMIN_API_KEY", "")
PUBLIC_API_KEY = os.environ.get("PLAYWRIGHT_PUBLIC_API_KEY", "")


@pytest_asyncio.fixture(name="admin_client")
async def fixture_admin_client():
    """Create a RestClient for testing; using a admin user key with full access."""
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )
    try:
        yield client
    finally:
        await client.aclose()
        client.close()


@pytest_asyncio.fixture(name="pub_client")
async def fixture_pub_client():
    """Create a RestClient for testing; using a public user key with limited access."""
    client = RestClient(
        stage=Stage.DEV,
        api_key=PUBLIC_API_KEY,
    )
    try:
        yield client
    finally:
        await client.aclose()
        client.close()


@pytest.fixture(name="task_req")
def fixture_task_req():
    """Create a sample task request."""
    return TaskRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )


@pytest.fixture(name="pqa_task_req")
def fixture_pqa_task_req():
    return TaskRequest(
        name=JobNames.from_string("crow"),
        query="How many moons does earth have?",
    )


@pytest.fixture(name="phoenix_task_req")
def fixture_phoenix_task_req():
    return TaskRequest(
        name=JobNames.from_string("phoenix"),
        query="What is the molecular weight of ascorbic acids?",
    )


@pytest.fixture(name="running_trajectory_id")
def fixture_running_trajectory_id(
    admin_client: RestClient, task_req: TaskRequest
) -> str:
    return admin_client.create_task(task_req)


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_futurehouse_dummy_env_crow(admin_client: RestClient, task_req: TaskRequest):
    admin_client.create_task(task_req)
    while (task_status := admin_client.get_task().status) in {"queued", "in progress"}:
        time.sleep(5)
    assert task_status == "success"


def test_insufficient_permissions_request(
    pub_client: RestClient, task_req: TaskRequest
):
    # Create a new instance so that cached credentials aren't reused
    with pytest.raises(PermissionError) as exc_info:
        pub_client.create_task(task_req)

    assert "Error creating task" in str(exc_info.value)


@pytest.mark.timeout(350)
@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping due to buggy pqa on dev")
async def test_job_response(  # noqa: PLR0915
    subtests: SubTests,
    admin_client: RestClient,
    pqa_task_req: TaskRequest,
    phoenix_task_req: TaskRequest,
):
    task_id = admin_client.create_task(pqa_task_req)
    atask_id = await admin_client.acreate_task(pqa_task_req)
    phoenix_task_id = admin_client.create_task(phoenix_task_req)
    aphoenix_task_id = await admin_client.acreate_task(phoenix_task_req)

    with subtests.test("Test TaskResponse with queued task"):
        task_response = admin_client.get_task(task_id)
        assert task_response.status in {"queued", "in progress"}
        assert not isinstance(task_response, LiteTaskResponse)
        assert task_response.job_name == pqa_task_req.name
        assert task_response.query == pqa_task_req.query
        task_response = await admin_client.aget_task(atask_id)
        assert task_response.status in {"queued", "in progress"}
        assert not isinstance(task_response, LiteTaskResponse)
        assert task_response.job_name == pqa_task_req.name
        assert task_response.query == pqa_task_req.query

    for _ in range(TEST_MAX_POLLS):
        task_response = admin_client.get_task(task_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    for _ in range(TEST_MAX_POLLS):
        task_response = await admin_client.aget_task(atask_id)
        if task_response.status in ExecutionStatus.terminal_states():
            break
        await asyncio.sleep(5)

    with subtests.test("Test PQA job response"):
        task_response = admin_client.get_task(task_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert pqa_task_req.name in task_response.job_name
        assert pqa_task_req.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test async PQA job response"):
        task_response = await admin_client.aget_task(atask_id)
        assert isinstance(task_response, PQATaskResponse)
        # assert it has general fields
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert pqa_task_req.name in task_response.job_name
        assert pqa_task_req.query in task_response.query
        # assert it has PQA specific fields
        assert task_response.answer is not None
        # assert it's not verbose
        assert not hasattr(task_response, "environment_frame")
        assert not hasattr(task_response, "agent_state")

    with subtests.test("Test Phoenix job response"):
        task_response = admin_client.get_task(phoenix_task_id)
        assert isinstance(task_response, PhoenixTaskResponse)
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert phoenix_task_req.name in task_response.job_name
        assert phoenix_task_req.query in task_response.query

    with subtests.test("Test async Phoenix job response"):
        task_response = await admin_client.aget_task(aphoenix_task_id)
        assert isinstance(task_response, PhoenixTaskResponse)
        assert task_response.status == "success"
        assert task_response.task_id is not None
        assert phoenix_task_req.name in task_response.job_name
        assert phoenix_task_req.query in task_response.query

    with subtests.test("Test task response with verbose"):
        task_response = admin_client.get_task(task_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None

    with subtests.test("Test task async response with verbose"):
        task_response = await admin_client.aget_task(atask_id, verbose=True)
        assert isinstance(task_response, TaskResponseVerbose)
        assert task_response.status == "success"
        assert task_response.environment_frame is not None
        assert task_response.agent_state is not None


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_run_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    results = admin_client.run_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_run_until_done_returns_task_response(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test that run_tasks_until_done returns TaskResponse instead of LiteTaskResponse."""
    tasks_to_do = [task_req, task_req]

    results = admin_client.run_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)

    for task in results:
        assert isinstance(task, TaskResponse), (
            f"Expected TaskResponse, got {type(task)}"
        )


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_arun_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    results = await admin_client.arun_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_arun_until_done_returns_task_response(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test that arun_tasks_until_done returns TaskResponse instead of LiteTaskResponse."""
    tasks_to_do = [task_req, task_req]

    results = await admin_client.arun_tasks_until_done(tasks_to_do)

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status == "success" for task in results)

    for task in results:
        assert isinstance(task, TaskResponse), (
            f"Expected TaskResponse, got {type(task)}"
        )


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_timeout_run_until_done_futurehouse_dummy_env_crow(
    admin_client: RestClient, task_req: TaskRequest
):
    tasks_to_do = [task_req, task_req]

    results = await admin_client.arun_tasks_until_done(
        tasks_to_do, verbose=True, timeout=5, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status != "success" for task in results), "Should not be success."
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )

    results = admin_client.run_tasks_until_done(
        tasks_to_do, verbose=True, timeout=5, progress_bar=True
    )

    assert len(results) == len(tasks_to_do), "Should return 2 tasks."
    assert all(task.status != "success" for task in results), "Should not be success."
    assert all(not isinstance(task, PQATaskResponse) for task in results), (
        "Should be verbose."
    )


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_cancel_task(admin_client: RestClient):
    """Test successful task cancellation using MagicMock."""
    task_id = "1c28bb94-efbf-442f-954c-f0d8ddb0cff5"

    with (
        patch.object(admin_client.client, "post") as mock_post,
        patch.object(admin_client, "get_task") as mock_get_task,
    ):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        mock_task_response_running = MagicMock()
        mock_task_response_running.status = "in progress"

        mock_task_response_cancelled = MagicMock()
        mock_task_response_cancelled.status = ExecutionStatus.CANCELLED.value

        mock_get_task.side_effect = [
            mock_task_response_running,
            mock_task_response_cancelled,
        ]

        result = admin_client.cancel_task(task_id)

        assert result is True

        expected_url = f"/v0.1/trajectories/{task_id}/cancel"
        mock_post.assert_called_once_with(expected_url)

        assert mock_get_task.call_count == 2


@pytest.mark.asyncio
async def test_world_model_acreate_and_aget(admin_client: RestClient):
    model = WorldModel(
        content="test content",
        name="Test Model",
        description="This is a test model.",
    )
    model_id = await admin_client.acreate_world_model(model)

    # try getting the newly created model by id
    model_by_id = await admin_client.aget_world_model(model_id)

    assert str(model_by_id.id) == str(model_id)
    assert model_by_id.content == model.content

    updated_model = WorldModel(
        content="updated test content",
        prior=model_id,
    )

    updated_model_id = await admin_client.acreate_world_model(updated_model)

    # try getting the newly created model by id
    updated_model_by_id = await admin_client.aget_world_model(updated_model_id)

    assert updated_model_by_id.name == model.name
    assert updated_model_by_id.content != model.content


def test_world_model_create_and_get(admin_client: RestClient):
    model = WorldModel(
        content="test content",
        name="Test Model",
        description="This is a test model.",
    )
    model_id = admin_client.create_world_model(model)

    # try getting the newly created model by id
    model_by_id = admin_client.get_world_model(model_id)

    assert str(model_by_id.id) == str(model_id)
    assert model_by_id.content == model.content

    updated_model = WorldModel(
        content="updated test content",
        prior=model_id,
    )

    updated_model_id = admin_client.create_world_model(updated_model)

    # try getting the newly created model by id
    updated_model_by_id = admin_client.get_world_model(updated_model_id)

    assert updated_model_by_id.name == model.name
    assert updated_model_by_id.content != model.content


class TestProjectOperations:
    @pytest.fixture
    def test_project_name(self):
        return f"test-project-{uuid4()}"

    def test_create_project_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        project_id = admin_client.create_project(test_project_name)
        assert isinstance(project_id, UUID)

    def test_get_project_by_name_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        created_project_id = admin_client.create_project(test_project_name)
        retrieved_project_id = admin_client.get_project_by_name(test_project_name)
        assert retrieved_project_id == created_project_id

    def test_get_project_by_name_not_found(self, admin_client: RestClient):
        with pytest.raises(ProjectError, match="No project found with name"):
            admin_client.get_project_by_name("non-existent-project-12345")

    def test_get_project_by_name_multiple_found(self, admin_client: RestClient):
        with patch.object(admin_client.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = [
                {"id": str(uuid4()), "name": "test"},
                {"id": str(uuid4()), "name": "test"},
            ]
            mock_get.return_value = mock_response

            projects = admin_client.get_project_by_name("test")
            assert isinstance(projects, list)
            assert len(projects) == 2

    def test_add_task_to_project_success(
        self, admin_client: RestClient, test_project_name: str, task_req: TaskRequest
    ):
        project_id = admin_client.create_project(test_project_name)
        trajectory_id = admin_client.create_task(task_req)
        admin_client.add_task_to_project(project_id, trajectory_id)

    def test_add_task_to_project_not_found(self, admin_client: RestClient):
        fake_project_id = uuid4()
        fake_trajectory_id = str(uuid4())

        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("404 Not Found")
            mock_post.return_value = mock_response

            with pytest.raises(
                ProjectError, match="Error adding trajectory to project"
            ):
                admin_client.add_task_to_project(fake_project_id, fake_trajectory_id)

    def test_create_project_with_http_error(self, admin_client: RestClient):
        with patch.object(admin_client.client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("400 Bad Request")
            mock_response.status_code = 400
            mock_response.text = "Invalid project name"
            mock_post.return_value = mock_response

            with pytest.raises(ProjectError, match="Error creating project"):
                admin_client.create_project("invalid project name")


class TestAsyncProjectOperations:
    @pytest.fixture
    def test_project_name(self):
        return f"test-async-project-{uuid4()}"

    @pytest.mark.asyncio
    async def test_acreate_project_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        project_id = await admin_client.acreate_project(test_project_name)
        assert isinstance(project_id, UUID)

    @pytest.mark.asyncio
    async def test_aget_project_by_name_success(
        self, admin_client: RestClient, test_project_name: str
    ):
        created_project_id = await admin_client.acreate_project(test_project_name)
        retrieved_project_id = await admin_client.aget_project_by_name(
            test_project_name
        )
        assert retrieved_project_id == created_project_id

    @pytest.mark.asyncio
    async def test_aget_project_by_name_not_found(self, admin_client: RestClient):
        with pytest.raises(ProjectError, match="No project found with name"):
            await admin_client.aget_project_by_name("non-existent-async-project-12345")

    @pytest.mark.asyncio
    async def test_aadd_task_to_project_success(
        self, admin_client: RestClient, test_project_name: str, task_req: TaskRequest
    ):
        project_id = await admin_client.acreate_project(test_project_name)
        trajectory_id = await admin_client.acreate_task(task_req)
        await admin_client.aadd_task_to_project(project_id, trajectory_id)

    @pytest.mark.asyncio
    async def test_aadd_task_to_project_permission_denied(
        self, admin_client: RestClient
    ):
        fake_project_id = uuid4()
        fake_trajectory_id = str(uuid4())

        with patch.object(admin_client.async_client, "post") as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = Exception("403 Forbidden")
            mock_response.status_code = 403
            mock_post.return_value = mock_response

            with pytest.raises(
                ProjectError, match="Error adding trajectory to project: 403 Forbidden"
            ):
                await admin_client.aadd_task_to_project(
                    fake_project_id, fake_trajectory_id
                )


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_get_tasks_with_project_filter(admin_client: RestClient, task_req: TaskRequest):
    """Test retrieving trajectories filtered by project_id using real API calls."""
    project_name = f"e2e-trajectories-fetch-{uuid4()}"
    project_id = admin_client.create_project(project_name)

    trajectory_id = admin_client.create_task(task_req)
    admin_client.add_task_to_project(project_id, trajectory_id)

    while (task_status := admin_client.get_task(trajectory_id).status) in {
        "queued",
        "in progress",
    }:
        time.sleep(5)

    trajectories = admin_client.get_tasks(project_id=project_id)

    trajectory_ids = [t["id"] for t in trajectories]
    assert trajectory_id in trajectory_ids


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.asyncio
async def test_aget_tasks_with_project_filter(
    admin_client: RestClient, task_req: TaskRequest
):
    """Test async retrieving trajectories filtered by project_id using real API calls."""
    project_name = f"e2e-trajectories-async-fetch-{uuid4()}"
    project_id = await admin_client.acreate_project(project_name)

    trajectory_id = await admin_client.acreate_task(task_req)
    await admin_client.aadd_task_to_project(project_id, trajectory_id)

    while True:
        task = await admin_client.aget_task(trajectory_id)
        if task.status not in {"queued", "in progress"}:
            break
        await asyncio.sleep(5)

    trajectories = await admin_client.aget_tasks(project_id=project_id)

    trajectory_ids = [t["id"] for t in trajectories]
    assert trajectory_id in trajectory_ids


class TestUserAgentRequestOperations:
    """Test suite for synchronous User Agent Request operations."""

    @pytest.mark.flaky(reruns=3)
    def test_e2e_user_agent_request_flow(
        self,
        admin_client: RestClient,
        running_trajectory_id: str,
    ):
        """Tests the full lifecycle: create, get, list, and respond."""
        payload = UserAgentRequestPostPayload(
            trajectory_id=running_trajectory_id,
            request={"question": "Do you approve?"},
            notify_user={"email": False, "sms": False},  # avoid sending notifications
        )
        request_id = admin_client.create_user_agent_request(payload)
        assert isinstance(request_id, UUID)

        # 2. GET the created request
        retrieved_req = admin_client.get_user_agent_request(request_id)
        assert retrieved_req.id == request_id
        assert str(retrieved_req.trajectory_id) == str(payload.trajectory_id)
        assert retrieved_req.status == UserAgentRequestStatus.PENDING
        assert retrieved_req.request == payload.request

        # 3. LIST requests and find the created one
        request_list = admin_client.list_user_agent_requests(
            trajectory_id=UUID(running_trajectory_id),
            request_status=UserAgentRequestStatus.PENDING,
        )
        assert isinstance(request_list, list)
        assert any(req.id == request_id for req in request_list)

        # 4. RESPOND to the request
        response_payload = UserAgentResponsePayload(response={"answer": "Yes"})
        admin_client.respond_to_user_agent_request(request_id, response_payload)

        # 5. GET the request again to verify the response
        responded_req = admin_client.get_user_agent_request(request_id)
        assert responded_req.status == UserAgentRequestStatus.RESPONDED
        assert responded_req.response == response_payload.response

    def test_get_nonexistent_request_fails(self, admin_client: RestClient):
        """Verifies that fetching a non-existent request raises an error."""
        non_existent_id = uuid4()
        with pytest.raises(UserAgentRequestFetchError):
            admin_client.get_user_agent_request(non_existent_id)

    def test_unauthorized_access_fails(self, pub_client: RestClient):
        """Ensures a client with insufficient permissions cannot perform actions."""
        # Using a public client that shouldn't have access
        with pytest.raises((UserAgentRequestCreationError, PermissionError)):  # noqa: PT012
            payload = UserAgentRequestPostPayload(
                trajectory_id=uuid4(),
                request={"data": "test"},
            )
            pub_client.create_user_agent_request(payload)

        with pytest.raises((UserAgentRequestFetchError, PermissionError)):
            # Attempt to fetch a request that the user doesn't own
            pub_client.get_user_agent_request(uuid4())


class TestAsyncUserAgentRequestOperations:
    """Test suite for asynchronous User Agent Request operations."""

    @pytest.mark.asyncio
    async def test_async_expiring_e2e_user_agent_request_flow(
        self,
        admin_client: RestClient,
        running_trajectory_id: str,
    ):
        """Tests the full async lifecycle: acreate, aget, alist, and arespond."""
        payload = UserAgentRequestPostPayload(
            trajectory_id=running_trajectory_id,
            request={"question": "Async: Do you approve?"},
            user_response_task=TaskRequest(
                name=JobNames.from_string("dummy"),
                query="Why would I follow up on this query?",
            ).model_dump(mode="json"),
            expires_in_seconds=10,
            notify_user={"email": False, "sms": False},  # avoid sending notifications
        )

        request_id = await admin_client.acreate_user_agent_request(payload)
        assert isinstance(request_id, UUID)

        retrieved_req = await admin_client.aget_user_agent_request(request_id)
        assert retrieved_req.id == request_id
        assert str(retrieved_req.trajectory_id) == str(payload.trajectory_id)
        assert retrieved_req.status == UserAgentRequestStatus.PENDING

        request_list = await admin_client.alist_user_agent_requests(
            trajectory_id=UUID(running_trajectory_id)
        )
        assert isinstance(request_list, list)
        assert any(req.id == request_id for req in request_list)

        # ensure we allow it to expire so auto response can happen
        await asyncio.sleep(10)

        # now this should be expired
        retrieved_req = await admin_client.aget_user_agent_request(request_id)
        assert retrieved_req.status == UserAgentRequestStatus.EXPIRED

        # we should also see the job having started -- along with the registration of the job in the
        job_data = await admin_client.aget_task(
            cast(str, retrieved_req.response_trajectory_id)
        )
        assert job_data.status in {"queued", "in progress"}

        # 4. RESPOND to the request -- ensure nothing changes
        ignored_response = {"answer": "Async Yes"}
        response_payload = UserAgentResponsePayload(response=ignored_response)
        await admin_client.arespond_to_user_agent_request(request_id, response_payload)

        retrieved_req = await admin_client.aget_user_agent_request(request_id)
        assert retrieved_req.response != ignored_response

    @pytest.mark.asyncio
    async def test_async_e2e_user_agent_request_flow(
        self,
        admin_client: RestClient,
        running_trajectory_id: str,
    ):
        """Tests the full async lifecycle: acreate, aget, alist, and arespond."""
        # 1. CREATE a request
        payload = UserAgentRequestPostPayload(
            trajectory_id=running_trajectory_id,
            request={"question": "Async: Do you approve?"},
            user_response_task=TaskRequest(
                name=JobNames.from_string("dummy"),
                query="Why would I follow up on this query?",
            ).model_dump(mode="json"),
            notify_user={"email": False, "sms": False},  # avoid sending notifications
        )

        request_id = await admin_client.acreate_user_agent_request(payload)
        assert isinstance(request_id, UUID)

        # 2. GET the created request
        retrieved_req = await admin_client.aget_user_agent_request(request_id)
        assert retrieved_req.id == request_id
        assert str(retrieved_req.trajectory_id) == str(payload.trajectory_id)
        assert retrieved_req.status == UserAgentRequestStatus.PENDING

        # 3. LIST requests and find the created one
        request_list = await admin_client.alist_user_agent_requests(
            trajectory_id=UUID(running_trajectory_id)
        )
        assert isinstance(request_list, list)
        assert any(req.id == request_id for req in request_list)

        # 4. RESPOND to the request
        response_payload = UserAgentResponsePayload(response={"answer": "Async Yes"})
        await admin_client.arespond_to_user_agent_request(request_id, response_payload)

        # 5. GET the request again to verify the response
        responded_req = await admin_client.aget_user_agent_request(request_id)
        assert responded_req.status == UserAgentRequestStatus.RESPONDED
        assert responded_req.response == response_payload.response

    @pytest.mark.asyncio
    async def test_aget_nonexistent_request_fails(self, admin_client: RestClient):
        """Verifies fetching a non-existent request asynchronously raises an error."""
        non_existent_id = uuid4()
        with pytest.raises(UserAgentRequestFetchError):
            await admin_client.aget_user_agent_request(non_existent_id)

    @pytest.mark.asyncio
    async def test_async_unauthorized_access_fails(self, pub_client: RestClient):
        """Ensures an unauthorized client fails on async methods."""
        with pytest.raises((UserAgentRequestCreationError, PermissionError)):  # noqa: PT012
            payload = UserAgentRequestPostPayload(
                trajectory_id=uuid4(),
                request={"data": "test"},
            )
            await pub_client.acreate_user_agent_request(payload)

        with pytest.raises((UserAgentRequestFetchError, PermissionError)):
            await pub_client.aget_user_agent_request(uuid4())


def create_mock_http_status_error(message: str, status_code: int) -> HTTPStatusError:
    """Create a properly mocked HTTPStatusError for testing."""
    mock_request = Mock()
    mock_response = Mock()
    mock_response.status_code = status_code

    return HTTPStatusError(message, request=mock_request, response=mock_response)


@pytest.mark.parametrize(
    ("exception", "should_retry", "test_description"),
    [
        (ConnectionError("Connection failed"), True, "connection error"),
        (Timeout("Request timed out"), True, "timeout error"),
        (RequestException("Request exception"), True, "request exception"),
        (ConnectError("Connect error"), True, "httpx connect error"),
        (ConnectTimeout("Connect timeout"), True, "httpx connect timeout"),
        (ReadTimeout("Read timeout"), True, "httpx read timeout"),
        (ReadError("Read error"), True, "httpx read error"),
        (NetworkError("Network error"), True, "httpx network error"),
        (RemoteProtocolError("Protocol error"), True, "httpx protocol error"),
        (CloseError("Close error"), True, "httpx close error"),
        (FileUploadError("Upload failed"), True, "custom FileUploadError"),
        (
            create_mock_http_status_error("Too many requests", 429),
            True,
            "429 too many requests",
        ),
        (
            create_mock_http_status_error("Internal server error", 500),
            True,
            "500 internal server error",
        ),
        (create_mock_http_status_error("Bad gateway", 502), True, "502 bad gateway"),
        (
            create_mock_http_status_error("Service unavailable", 503),
            True,
            "503 service unavailable",
        ),
        (
            create_mock_http_status_error("Gateway timeout", 504),
            True,
            "504 gateway timeout",
        ),
        (create_mock_http_status_error("Bad request", 400), False, "400 bad request"),
        (create_mock_http_status_error("Unauthorized", 401), False, "401 unauthorized"),
        (create_mock_http_status_error("Forbidden", 403), False, "403 forbidden"),
        (create_mock_http_status_error("Not found", 404), False, "404 not found"),
        (ValueError("Invalid value"), False, "value error"),
        (KeyError("Missing key"), False, "key error"),
        (RuntimeError("Runtime error"), False, "runtime error"),
    ],
)
def test_retry_logic_conditions(exception, should_retry, test_description):
    retry_condition = create_retry_if_connection_error(FileUploadError)

    mock_retry_state = Mock()
    mock_retry_state.outcome = Mock()
    mock_retry_state.outcome.exception.return_value = exception

    result = retry_condition(mock_retry_state)

    assert result == should_retry, (
        f"Expected {should_retry} for {test_description}, got {result}"
    )


class TestJobEventOperations:
    @pytest.fixture
    def test_trajectory_id(
        self, admin_client: RestClient, task_req: TaskRequest
    ) -> str:
        """Create a real trajectory for job event testing."""
        return admin_client.create_task(task_req)

    @pytest.fixture
    def job_event_create_request(self, test_trajectory_id: str):
        return JobEventCreateRequest(
            execution_id=UUID(test_trajectory_id),
            execution_type=ExecutionType.TRAJECTORY,
            cost_component=CostComponent.LLM_USAGE,
            started_at=datetime.datetime.now(),
            ended_at=datetime.datetime.now(),
            amount_usd=0.005,
            rate=0.0001,
            input_token_count=100,
            completion_token_count=50,
            metadata={"model": "gpt-4o", "temperature": 0.7},
        )

    @pytest.fixture
    def job_event_update_request(self):
        return JobEventUpdateRequest(
            amount_usd=0.007,
            rate=0.00015,
            input_token_count=120,
            completion_token_count=60,
            metadata={"model": "gpt-4o", "temperature": 0.5, "updated": True},
        )

    @pytest.mark.timeout(300)
    def test_create_job_event_success(
        self, admin_client: RestClient, job_event_create_request
    ):
        response = admin_client.create_job_event(job_event_create_request)
        assert response.id is not None
        assert isinstance(response.id, UUID)

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_acreate_job_event_success(
        self, admin_client: RestClient, job_event_create_request
    ):
        response = await admin_client.acreate_job_event(job_event_create_request)
        assert response.id is not None
        assert isinstance(response.id, UUID)

    def test_create_job_event_execution_not_found(
        self, admin_client: RestClient, job_event_create_request
    ):
        # Create a new request with a non-existent execution ID
        invalid_request = JobEventCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_create_request.execution_type,
            cost_component=job_event_create_request.cost_component,
            started_at=job_event_create_request.started_at,
            ended_at=job_event_create_request.ended_at,
            amount_usd=job_event_create_request.amount_usd,
            rate=job_event_create_request.rate,
            input_token_count=job_event_create_request.input_token_count,
            completion_token_count=job_event_create_request.completion_token_count,
            metadata=job_event_create_request.metadata,
        )
        with pytest.raises(JobEventCreationError, match="Execution not found"):
            admin_client.create_job_event(invalid_request)

    @pytest.mark.asyncio
    async def test_acreate_job_event_execution_not_found(
        self, admin_client: RestClient, job_event_create_request
    ):
        # Create a new request with a non-existent execution ID
        invalid_request = JobEventCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_create_request.execution_type,
            cost_component=job_event_create_request.cost_component,
            started_at=job_event_create_request.started_at,
            ended_at=job_event_create_request.ended_at,
            amount_usd=job_event_create_request.amount_usd,
            rate=job_event_create_request.rate,
            input_token_count=job_event_create_request.input_token_count,
            completion_token_count=job_event_create_request.completion_token_count,
            metadata=job_event_create_request.metadata,
        )
        with pytest.raises(JobEventCreationError, match="Execution not found"):
            await admin_client.acreate_job_event(invalid_request)

    @pytest.mark.timeout(300)
    def test_update_job_event_success(
        self,
        admin_client: RestClient,
        job_event_create_request,
        job_event_update_request,
    ):
        create_response = admin_client.create_job_event(job_event_create_request)
        job_event_id = create_response.id

        # Should not raise an exception and return None
        result = admin_client.update_job_event(job_event_id, job_event_update_request)
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_aupdate_job_event_success(
        self,
        admin_client: RestClient,
        job_event_create_request,
        job_event_update_request,
    ):
        create_response = await admin_client.acreate_job_event(job_event_create_request)
        job_event_id = create_response.id

        await admin_client.aupdate_job_event(job_event_id, job_event_update_request)

    def test_update_job_event_not_found(
        self, admin_client: RestClient, job_event_update_request
    ):
        job_event_id = uuid4()
        with pytest.raises(
            JobEventUpdateError, match=r"Job event with ID .* not found"
        ):
            admin_client.update_job_event(job_event_id, job_event_update_request)

    @pytest.mark.asyncio
    async def test_aupdate_job_event_not_found(
        self, admin_client: RestClient, job_event_update_request
    ):
        job_event_id = uuid4()
        with pytest.raises(
            JobEventUpdateError, match=r"Job event with ID .* not found"
        ):
            await admin_client.aupdate_job_event(job_event_id, job_event_update_request)

    @pytest.fixture
    def job_event_batch_create_request(self, test_trajectory_id: str):
        return JobEventBatchCreateRequest(
            execution_id=UUID(test_trajectory_id),
            execution_type=ExecutionType.TRAJECTORY,
            job_events=[
                JobEventBatchItemRequest(
                    cost_component=CostComponent.LLM_USAGE,
                    started_at=datetime.datetime.now(),
                    ended_at=datetime.datetime.now(),
                    amount_usd=0.005,
                    rate=0.0001,
                    input_token_count=100,
                    completion_token_count=50,
                    metadata={"model": "gpt-4o", "temperature": 0.7},
                ),
                JobEventBatchItemRequest(
                    cost_component=CostComponent.STEP,
                    started_at=datetime.datetime.now(),
                    ended_at=datetime.datetime.now(),
                    amount_usd=0.001,
                ),
            ],
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_acreate_job_events_batch_success(
        self, admin_client: RestClient, job_event_batch_create_request
    ):
        response = await admin_client.acreate_job_events_batch(
            job_event_batch_create_request
        )
        assert response.ids is not None
        assert len(response.ids) == 2
        assert response.created_count == 2
        assert all(isinstance(job_id, UUID) for job_id in response.ids)

    @pytest.mark.asyncio
    async def test_acreate_job_events_batch_execution_not_found(
        self, admin_client: RestClient, job_event_batch_create_request
    ):
        invalid_request = JobEventBatchCreateRequest(
            execution_id=uuid4(),  # Non-existent ID
            execution_type=job_event_batch_create_request.execution_type,
            job_events=job_event_batch_create_request.job_events,
        )

        with pytest.raises(
            JobEventBatchCreationError, match=r"Trajectory with ID .* not found"
        ):
            await admin_client.acreate_job_events_batch(invalid_request)

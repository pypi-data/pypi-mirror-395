"""Live test to upload a file, run an analysis task, and download output files."""
# pylint: disable=redefined-outer-name  # Variables reused in __main__ block for manual testing

import os
import tempfile
from contextlib import closing
from pathlib import Path
from uuid import UUID

import pytest
from dotenv import load_dotenv

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import JobNames, RuntimeConfig, Stage, TaskRequest
from edison_client.models.data_storage_methods import RawFetchResponse

# Load .env file from tests directory
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Get API key from environment or use a placeholder for local testing
API_KEY = os.environ.get("PLAYWRIGHT_ADMIN_API_KEY", "")


@pytest.fixture(name="client")
def fixture_client():
    """Create a RestClient for testing."""
    with closing(
        RestClient(
            stage=Stage.DEV,
            api_key=API_KEY,
        )
    ) as client:
        yield client


@pytest.mark.live
@pytest.mark.skipif(
    not API_KEY, reason="Skipping live test: PLAYWRIGHT_ADMIN_API_KEY not set"
)
@pytest.mark.timeout(900)  # 15 minutes for task completion
def test_upload_and_run_analysis_task(client: RestClient):  # noqa: PLR0915
    """Test uploading a file with prompt, running analysis task, and downloading outputs."""
    # Create a temporary file with the prompt
    prompt_content = "draw a blue square"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as temp_file:
        temp_file.write(prompt_content)
        temp_file_path = Path(temp_file.name)

    output_dir = None

    try:
        print("\n=== Step 1: Upload file with prompt ===")
        # Upload the file using upload_file which returns data_entry URI
        data_entry_uri = client.upload_file(
            file_path=temp_file_path,
            name="blue_square_prompt",
            description="A prompt to draw a blue square",
        )

        print("✓ File uploaded successfully!")
        print(f"  - Data entry URI: {data_entry_uri}")

        # Verify the upload by extracting the ID and fetching
        data_storage_id = data_entry_uri.split(":", 1)[1]
        fetch_response = client.fetch_data_from_storage(UUID(data_storage_id))
        assert isinstance(fetch_response, RawFetchResponse)
        assert fetch_response.content == prompt_content
        print(f"✓ File content verified: '{fetch_response.content}'")

        print("\n=== Step 2: Submit analysis task with file ===")
        # Create a task request - files are passed via run_tasks_until_done
        task_request = TaskRequest(
            name=JobNames.ANALYSIS,  # Use the data analysis crow
            query="Open the attached file and follow the instructions in it. Create an image as specified.",
            runtime_config=RuntimeConfig(
                timeout=600,  # 10 minute timeout for task
            ),
        )

        print(f"  Task: {task_request.query}")
        print(f"  Crow: {task_request.name}")
        print(f"  Attached files: {[data_entry_uri]}")

        print("\n=== Step 3: Run task until completion ===")
        # Run the task and wait for completion - files passed here!
        results = client.run_tasks_until_done(
            task_data=task_request,
            files=[data_entry_uri],  # Simple file attachment!
            verbose=True,
            progress_bar=True,
            timeout=600,  # 10 minute timeout
        )

        assert len(results) == 1
        task_result = results[0]

        print("✓ Task completed!")
        print(f"  - Task ID: {task_result.task_id}")
        print(f"  - Status: {task_result.status}")

        print("\n=== Step 4: List output files ===")
        # List files created by the task
        output_files = client.list_files(str(task_result.task_id))

        print(f"✓ Found {len(output_files)} output file(s):")
        for file_entry in output_files:
            data_storage = file_entry["data_storage"]
            print(f"  - {data_storage['name']} (ID: {data_storage['id']})")

        assert len(output_files) > 0, (
            "Task should have created at least one output file"
        )

        print("\n=== Step 5: Download output files ===")
        # Create a temporary directory for downloads
        output_dir = Path(tempfile.mkdtemp())
        print(f"  Download directory: {output_dir}")

        for file_entry in output_files:
            data_storage = file_entry["data_storage"]
            file_id = data_storage["id"]
            file_name = data_storage["name"]

            print(f"  Downloading: {file_name}")
            result = client.fetch_data_from_storage(UUID(file_id))

            # Save the file content
            if isinstance(result, RawFetchResponse):
                downloaded_path = output_dir / (
                    result.filename.name if result.filename else result.entry_name
                )
                downloaded_path.write_text(result.content)
            elif isinstance(result, Path):
                downloaded_path = result
            else:
                raise TypeError(f"Unexpected result type: {type(result)}")

            assert downloaded_path.exists()
            assert downloaded_path.stat().st_size > 0
            print(f"    ✓ Saved to: {downloaded_path}")
            print(f"    ✓ Size: {downloaded_path.stat().st_size} bytes")

        print("\n=== Step 6: Cleanup ===")
        # Clean up the uploaded input file
        client.delete_data_storage_entry(UUID(data_storage_id))
        print("✓ Input file cleaned up")

    finally:
        # Clean up the temporary files
        if temp_file_path.exists():
            temp_file_path.unlink()
            print("✓ Temporary input file removed")

        # Note: We leave output files for manual inspection
        # They can be manually deleted from output_dir if needed
        if output_dir is not None and output_dir.exists():
            print(f"✓ Output files available at: {output_dir}")

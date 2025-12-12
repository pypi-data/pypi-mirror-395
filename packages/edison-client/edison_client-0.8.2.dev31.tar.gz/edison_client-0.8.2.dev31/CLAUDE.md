# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

**Development Setup:**

```bash
# Install with dev dependencies (from repo root)
uv pip install -e packages/edison-client[dev]
```

**Testing:**

```bash
# Run all tests with parallel execution (from repo root)
uv run --no-project pytest packages/edison-client/tests -n auto -W ignore

# Run specific tests
pytest tests/test_client.py -k "test_create_task"
pytest tests/ -v                # Verbose output
pytest tests/ -s                # Show print statements
```

**Code Quality:**

```bash
# Linting and type checking (from repo root)
uv run --no-project pylint packages/edison-client
ruff check --fix packages/edison-client/
mypy packages/edison-client/

# From package directory
pylint edison_client/           # Lint source code
ruff check --fix .              # Auto-fix linting issues
mypy src/                       # Type checking
```

**Development Tools:**

```bash
# Jupyter notebook development
jupyter lab                     # Start JupyterLab
jupyter notebook               # Start Jupyter Notebook
ipython                        # Interactive Python shell
```

## Architecture Overview

**Python Client Library:**

- **REST API Client** for Edison Scientific platform services
- **Async/Sync Support** with both sync and async method variants
- **Type Safety** with Pydantic models and full type annotations
- **Authentication** via API key (environment variable or parameter)

**Core Components:**

- `src/edison_client/`: Main client library source code
  - `clients/`: Client implementations (REST client, job client, data storage)
  - `models/`: Pydantic models for requests/responses
  - `utils/`: Authentication, monitoring, and utility functions
- `docs/`: Documentation and tutorials including Jupyter notebooks
- `tests/`: Comprehensive test suite with async testing support
- `data_storage.md`: Documentation for data storage functionality

**Available Jobs (JobNames enum):**

- **LITERATURE**: `job-futurehouse-paperqa2` - Literature Search with PaperQA2 (formerly Crow)
- **ANALYSIS**: `job-futurehouse-data-analysis-crow-high` - Data Analysis for biological datasets
- **PRECEDENT**: `job-futurehouse-paperqa3-precedent` - Precedent Search (formerly HasAnyone/Owl)
- **MOLECULES**: `job-futurehouse-phoenix` - Chemistry Tasks with cheminformatics (formerly Phoenix)
- **DUMMY**: `job-futurehouse-dummy` - Testing and development

**Key Dependencies:**

- **httpx**: Async/sync HTTP client for API communication
- **pydantic**: Data validation and serialization
- **ldp**: Agent and environment framework (>=0.22.0)
- **litellm** + **openai**: LLM integration and API client
- **tenacity**: Retry logic and error handling
- **tqdm**: Progress bars with async support (>=4.62)
- **fhaviary**: Internal Future House library

## Development Patterns

**Client Usage Patterns:**

```python
# Basic synchronous usage
from edison_client import EdisonClient, JobNames

client = EdisonClient()  # Uses EDISON_API_KEY env var
(response,) = client.run_tasks_until_done(
    {"name": JobNames.LITERATURE, "query": "Your research question here"}
)


# Asynchronous usage
async def main():
    client = EdisonClient(api_key="your_key")
    (response,) = await client.arun_tasks_until_done(
        {"name": JobNames.ANALYSIS, "query": "Deep research question"}
    )
```

**Task Management:**

- **Batch Processing**: Submit multiple tasks at once via list of TaskRequest objects
- **Task Continuation**: Follow-up questions using `continued_task_id` in runtime_config
- **Async Patterns**: Create tasks with `create_task()` and poll status later with `get_task()`
- **Runtime Configuration**: Custom agent settings, timeouts, and max_steps via RuntimeConfig

**Response Handling:**

- **PQATaskResponse**: For Literature, Precedent, and Analysis jobs with structured answers
  - `answer`: Direct answer to query
  - `formatted_answer`: Answer with formatted references
  - `has_successful_answer`: Success flag
- **TaskResponseVerbose**: Detailed response with agent states and environment data (use `verbose=True`)
  - `agent_state`: All agent states during task execution
  - `environment_frame`: Environment data including contexts and metadata
  - `metadata`: Extra metadata about the query

**Authentication:**

- Environment variable: `EDISON_API_KEY`
- Parameter: `EdisonClient(api_key="your_key")`
- API key obtained from profile page: `https://platform.edisonscientific.com/profile`

## Testing Strategy

**Test Organization:**

- **Unit Tests**: Individual component testing
- **Integration Tests**: Full client workflow testing
- **Async Testing**: pytest-asyncio for async method testing
- **Mocking**: HTTP responses and external dependencies

**Test Configuration:**

- **Parallel Execution**: pytest-xdist with `-n auto`
- **Retry Logic**: pytest-rerunfailures for flaky tests
- **Timeouts**: pytest-timeout for long-running tests
- **Subtests**: pytest-subtests for parameterized testing

**Test Coverage:**

- Source code testing in `src/edison_client/`
- Documentation testing with doctest integration
- End-to-end workflow testing with real API calls (when configured)

**CI Integration:**

- Tests run in GitHub Actions workflow: `edison-client-lint-and-tests`
- Requires secrets: `SERVICE_ACCOUNT_JSON`, `PLAYWRIGHT_ADMIN_API_KEY`, `PLAYWRIGHT_PUBLIC_API_KEY`
- Uses `large-runner` for CI execution

## Important Development Notes

**Package Structure:**

- **Source Layout**: Code in `src/edison_client/` directory
- **Dynamic Versioning**: Version managed by setuptools_scm from git tags in root
- **Namespace Package**: Part of uv workspace configuration in root pyproject.toml
- **Workspace Member**: Defined in root `[tool.uv.workspace]` section

**Code Quality Standards:**

- **Ruff**: Extends root configuration for linting and formatting
- **MyPy**: Type checking with additional stubs for dependencies
- **Pylint**: Code analysis with Pydantic plugin support
- **Pre-commit**: Automated quality checks before commits

**Release Process:**

- **Git Tags**: Version tags trigger automated PyPI releases via GitHub Actions
- **Workflow**: "Deploy Edison - Client" workflow in `.github/workflows/deploy-edison-client.yaml`
- **TestPyPI**: Configured for testing package releases
- **License**: MIT License included in package distribution
- **Process**: Tag on dev branch → Push tags → Trigger workflow → Publishes to PyPI

**Development Environment:**

- **Python Version**: Supports 3.11-3.13
- **Jupyter Integration**: Full support for notebook development with ipykernel
- **Async Development**: Both sync and async patterns supported throughout
- **Monitoring**: Optional NewRelic integration for production use (monitoring optional dependency)

**API Integration:**

- **Rate Limiting**: Built into platform API
- **Error Handling**: Comprehensive error handling with tenacity retry logic
- **Timeout Management**: Configurable timeouts for long-running tasks via RuntimeConfig
- **Verbose Mode**: Detailed response data for debugging and analysis
- **Task Continuation**: Use `continued_task_id` for follow-up questions

**Key Modules:**

- `clients/rest_client.py`: Main EdisonClient implementation with sync/async methods
- `clients/job_client.py`: Job-specific client functionality
- `clients/data_storage_methods.py`: Data storage integration
- `models/app.py`: TaskRequest, TaskResponse, RuntimeConfig models
- `models/client.py`: Client-specific models
- `utils/auth.py`: Authentication utilities
- `utils/monitoring.py`: NewRelic monitoring integration

**Documentation:**

- Comprehensive README.md with code examples
- Jupyter notebooks in docs/ directory
- Client cookbook: <https://edisonscientific.gitbook.io/edisonscientific-cookbook/edison-client/docs/client_notebook>

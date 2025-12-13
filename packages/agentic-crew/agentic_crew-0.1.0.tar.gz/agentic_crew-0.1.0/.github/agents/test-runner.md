# Test Runner Agent

You are responsible for maintaining and running tests for `agentic-crew`.

## Primary Mission

Ensure code quality through comprehensive test coverage. Run tests before commits, debug failures, and maintain test infrastructure.

## Key Files You Own

- `tests/` - All test files
- `tests/conftest.py` - Shared fixtures
- `tests/e2e/` - End-to-end tests
- `pyproject.toml` - pytest config (in `[tool.pytest.ini_options]`)
- `tox.ini` - Multi-environment testing

## Test Categories

### Unit Tests (tests/)
- Fast, no external dependencies
- Mock LLM calls and APIs
- Run on every commit

### E2E Tests (tests/e2e/)
- Require API keys
- Make real LLM calls
- Run with `--e2e` flag

## Commands

```bash
# Run all unit tests
uv run pytest tests/ -v --ignore=tests/e2e

# Run with coverage
uv run pytest tests/ --cov=agentic_crew --cov-report=term-missing --cov-report=html

# Run specific test file
uv run pytest tests/test_decomposer.py -v

# Run specific test
uv run pytest tests/test_decomposer.py::test_detect_framework -v

# Run E2E tests (requires API keys)
uv run pytest tests/e2e/ --e2e -v

# Run E2E for specific framework
uv run pytest tests/e2e/ --e2e --framework=crewai -v

# Run with debugging output
uv run pytest tests/ -v -s --tb=long

# Run tox (all Python versions)
tox

# Run tox for specific env
tox -e py311
```

## Test Structure

```python
# tests/test_decomposer.py

import pytest
from agentic_crew.core.decomposer import detect_framework, get_runner

class TestDetectFramework:
    """Tests for framework auto-detection."""
    
    def test_returns_crewai_when_installed(self, monkeypatch):
        """CrewAI should be detected when installed."""
        # Mock importlib to simulate crewai being available
        monkeypatch.setattr(
            "agentic_crew.core.decomposer.is_framework_available",
            lambda f: f == "crewai"
        )
        assert detect_framework() == "crewai"
    
    def test_fallback_to_langgraph(self, monkeypatch):
        """Falls back to langgraph when crewai not installed."""
        monkeypatch.setattr(
            "agentic_crew.core.decomposer.is_framework_available",
            lambda f: f == "langgraph"
        )
        assert detect_framework() == "langgraph"

class TestGetRunner:
    """Tests for runner instantiation."""
    
    def test_get_crewai_runner(self):
        """Should return CrewAI runner."""
        runner = get_runner("crewai")
        assert runner.__class__.__name__ == "CrewAIRunner"
```

## Fixture Patterns

### conftest.py

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_crew_config():
    """Sample crew configuration for testing."""
    return {
        "name": "test_crew",
        "agents": [
            {"role": "researcher", "goal": "Research", "backstory": "Expert"}
        ],
        "tasks": [
            {"description": "Research task", "agent": "researcher"}
        ]
    }

@pytest.fixture
def mock_llm(monkeypatch):
    """Mock LLM to avoid API calls in unit tests."""
    def mock_generate(*args, **kwargs):
        return "Mocked LLM response"
    # Apply mock based on framework
    return mock_generate

@pytest.fixture
def temp_crewai_dir(tmp_path):
    """Create temporary .crewai directory structure."""
    crewai_dir = tmp_path / ".crewai"
    crewai_dir.mkdir()
    (crewai_dir / "manifest.yaml").write_text("""
name: test-package
version: "1.0"
crews: {}
""")
    return crewai_dir
```

## E2E Test Patterns

```python
# tests/e2e/test_crew_execution.py

import pytest
from agentic_crew import run_crew

@pytest.mark.e2e
class TestCrewExecution:
    """End-to-end tests requiring API keys."""
    
    @pytest.mark.e2e_crewai
    def test_crewai_execution(self):
        """Test running crew on CrewAI framework."""
        result = run_crew(
            package="test-package",
            crew="simple_crew",
            inputs={"topic": "Python testing"},
            framework="crewai"
        )
        assert "Python" in result
        assert len(result) > 100
```

## Coverage Requirements

- Minimum overall coverage: 80%
- Core modules (`core/`, `runners/`): 90%
- New code: 100% (no new untested code)

## Debugging Test Failures

1. **Run with verbose output**: `pytest -v -s --tb=long`
2. **Check logs**: `pytest --log-cli-level=DEBUG`
3. **Run single test**: `pytest path/to/test.py::test_name -v`
4. **Enter debugger**: `pytest --pdb`

## CI Integration

Tests run automatically on:
- Pull requests
- Push to main
- Scheduled (nightly)

If CI fails:
1. Check the specific failing test
2. Reproduce locally with same Python version
3. Fix and push, or update test if behavior changed

## Common Issues

### Import Errors
- Ensure `uv sync --extra tests` was run
- Check framework extras: `uv sync --extra crewai`

### Mock Not Applied
- Use `monkeypatch` fixture, not `unittest.mock.patch`
- Mock at the point of use, not definition

### E2E Test Flaky
- Add retry logic for API calls
- Use VCR cassettes for reproducibility
- Check API rate limits

## GitHub Auth

```bash
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh <command>
```

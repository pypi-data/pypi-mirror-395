# GitHub Copilot Instructions for agentic-crew

## Overview

`agentic-crew` is a **framework-agnostic AI crew orchestration library** that enables declaring crews once and running them on **CrewAI**, **LangGraph**, or **AWS Strands** depending on what's installed.

## Critical: GitHub Authentication

```bash
# ALWAYS use GITHUB_JBCOM_TOKEN for jbcom repos
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh <command>
```

## Quick Reference

```bash
# Install dependencies
uv sync --extra dev --extra tests --extra crewai

# Run tests
uv run pytest tests/ -v --ignore=tests/e2e

# Lint and format
uvx ruff check src/ tests/ --fix
uvx ruff format src/ tests/

# Type check
uv run mypy src/

# Run a crew
uv run agentic-crew run <package> <crew> --input "..."
```

## Architecture

### Core Concept: Framework Decomposition

```
┌─────────────────────────────────────────────────────────────────┐
│                    agentic-crew                                  │
│                                                                  │
│  manifest.yaml → Loader → Decomposer → Runner                    │
│                               │                                  │
│              ┌────────────────┼────────────────┐                │
│              ▼                ▼                ▼                │
│         CrewAI            LangGraph         Strands             │
│         Runner             Runner            Runner             │
└─────────────────────────────────────────────────────────────────┘
```

**Key insight**: Declare crews once in YAML, run on any framework based on what's installed.

### Directory Structure

```
src/agentic_crew/
├── core/                    # Framework-agnostic core
│   ├── discovery.py         # Find .crewai/ directories
│   ├── loader.py            # Load YAML configs
│   ├── runner.py            # Execute crews
│   └── decomposer.py        # Framework auto-detection
├── runners/                 # Framework-specific runners
│   ├── base.py              # Abstract base runner
│   ├── crewai_runner.py     # CrewAI implementation
│   ├── langgraph_runner.py  # LangGraph implementation
│   └── strands_runner.py    # Strands implementation
├── base/
│   └── archetypes.yaml      # Reusable agent templates
├── tools/
│   └── file_tools.py        # Shared file tools
└── crews/                   # Built-in example crews
```

### Manifest Format (.crewai/manifest.yaml)

```yaml
name: my-package
version: "1.0"
description: Package description

llm:
  provider: anthropic
  model: claude-sonnet-4-20250514

crews:
  my_crew:
    description: What this crew does
    agents: crews/my_crew/agents.yaml
    tasks: crews/my_crew/tasks.yaml
    knowledge:
      - knowledge/domain_docs
    preferred_framework: auto  # or crewai, langgraph, strands
```

## Key Files

| File | Purpose |
|------|---------|
| `src/agentic_crew/core/decomposer.py` | Framework detection and runner selection |
| `src/agentic_crew/runners/base.py` | Abstract runner interface |
| `src/agentic_crew/runners/crewai_runner.py` | CrewAI implementation |
| `src/agentic_crew/runners/langgraph_runner.py` | LangGraph implementation |
| `src/agentic_crew/runners/strands_runner.py` | Strands implementation |
| `src/agentic_crew/core/loader.py` | YAML config to crew objects |
| `AGENTS.md` | Comprehensive agent documentation |

## Code Style

- **Python**: 3.11+ required
- **Linting**: Ruff (100 char line length)
- **Type hints**: Required on all public functions
- **Docstrings**: Google style
- **Imports**: Absolute, organized by stdlib/third-party/local

## Commit Messages

Use conventional commits:
- `feat(runners): add new runner` → minor version bump
- `fix(decomposer): handle edge case` → patch version bump
- `docs: update README` → no version bump
- `refactor(loader): simplify parsing` → no version bump
- `test: add runner tests` → no version bump
- `chore: update deps` → no version bump

## Common Tasks

### Adding a New Framework Runner

1. Create `src/agentic_crew/runners/{framework}_runner.py`
2. Implement `BaseRunner` interface (see `runners/base.py`)
3. Register in `core/decomposer.py`:
   - Add to `FRAMEWORK_PRIORITY`
   - Add detection in `is_framework_available()`
   - Add creation in `get_runner()`
4. Add tests in `tests/test_runners.py`
5. Update documentation

### Adding a New Built-in Crew

1. Create directory: `src/agentic_crew/crews/{crew_name}/`
2. Add `config/agents.yaml` with agent definitions
3. Add `config/tasks.yaml` with task definitions
4. Add `{crew_name}_crew.py` with Crew class
5. Export in `crews/__init__.py`
6. Add tests

### Testing Framework Decomposition

```python
from agentic_crew.core.decomposer import detect_framework, get_runner

# Check what's available
print(detect_framework())  # "crewai", "langgraph", or "strands"

# Get runner for specific framework
runner = get_runner("langgraph")
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Required for Claude LLM |
| `GITHUB_JBCOM_TOKEN` | Required for GitHub operations |
| `MESHY_API_KEY` | For Meshy-related crews (optional) |
| `OPENROUTER_API_KEY` | Fallback LLM provider |

## Testing

```bash
# Unit tests (fast, no API calls)
uv run pytest tests/ -v --ignore=tests/e2e

# With coverage
uv run pytest tests/ --cov=agentic_crew --cov-report=term-missing

# Specific test file
uv run pytest tests/test_decomposer.py -v

# E2E tests (requires API keys, slow)
uv run pytest tests/e2e/ --e2e -v
```

## Related Repositories

- [vendor-connectors](https://github.com/jbcom/vendor-connectors) - HTTP connector library (uses agentic-crew for dev)
- [CrewAI](https://github.com/crewAIInc/crewAI) - Original crew framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based agents
- [Strands](https://github.com/strands-agents/strands-agents-python) - AWS agent framework

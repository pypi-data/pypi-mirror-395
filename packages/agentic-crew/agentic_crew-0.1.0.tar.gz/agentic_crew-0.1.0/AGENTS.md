# Agent Instructions for agentic-crew

> **CRITICAL**: Read this file completely before making ANY changes. This is the definitive guide for AI agents working on this repository.

## Overview

`agentic-crew` is a **framework-agnostic AI crew orchestration library** that enables declaring crews once and running them on **CrewAI**, **LangGraph**, or **AWS Strands** depending on what's installed.

**Key Insight**: Define crews in YAML, run on any framework. No vendor lock-in.

## Critical: GitHub Authentication

```bash
# ALWAYS use GITHUB_JBCOM_TOKEN for jbcom repos - NEVER plain GITHUB_TOKEN
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh <command>

# Examples
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh pr create --title "feat: add X"
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh issue list
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh repo view
```

## Quick Start

```bash
# 1. Install dependencies
uv sync --extra dev --extra tests

# 2. Install framework(s) you want
uv sync --extra crewai      # For CrewAI support
uv sync --extra langgraph   # For LangGraph support
uv sync --extra strands     # For Strands support

# 3. Run tests
uv run pytest tests/ -v --ignore=tests/e2e

# 4. Lint and format
uvx ruff check src/ tests/ --fix
uvx ruff format src/ tests/

# 5. Type check
uv run mypy src/
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

**Framework Priority** (auto-detection order): `crewai` > `langgraph` > `strands`

### How It Works

1. **Define** crews in YAML (agents, tasks, knowledge)
2. **Load** configuration via `agentic_crew.core.loader`
3. **Detect** available frameworks via `agentic_crew.core.decomposer`
4. **Build** framework-specific crew via appropriate Runner
5. **Execute** and return results

### Directory Structure

```
src/agentic_crew/
├── core/                    # Framework-agnostic core
│   ├── discovery.py         # Find .crewai/ directories
│   ├── loader.py            # Load YAML configs (requires crewai)
│   ├── runner.py            # Legacy runner (requires crewai, prefer decomposer)
│   └── decomposer.py        # Framework auto-detection & selection (recommended)
├── runners/                 # Framework-specific implementations
│   ├── __init__.py
│   ├── base.py              # Abstract base runner interface
│   ├── crewai_runner.py     # CrewAI implementation
│   ├── langgraph_runner.py  # LangGraph implementation
│   └── strands_runner.py    # Strands implementation
├── base/
│   └── archetypes.yaml      # Reusable agent templates
├── tools/
│   └── file_tools.py        # Shared file operation tools
└── crews/                   # Built-in example crews
    └── connector_builder/   # HTTP connector generation crew
```

### Configuration Directories

agentic-crew supports multiple configuration directory types:

| Directory | Framework | Description |
|-----------|-----------|-------------|
| `.crew/` | Auto-detect | Framework-agnostic, runs on any available framework |
| `.crewai/` | CrewAI | CrewAI-specific features required |
| `.langgraph/` | LangGraph | LangGraph-specific features required |
| `.strands/` | Strands | Strands-specific features required |

Use `.crew/` when your crews don't need framework-specific features.
Use framework-specific directories when you need features unique to that framework.

### Manifest Format

Crews are defined in `manifest.yaml` (e.g., `.crew/manifest.yaml`):

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

## Development Commands

```bash
# Install with specific extras
uv sync --extra dev --extra tests --extra crewai --extra scraping

# Run specific test file
uv run pytest tests/test_decomposer.py -v

# Run with coverage
uv run pytest tests/ --cov=agentic_crew --cov-report=term-missing

# Run E2E tests (requires API keys)
uv run pytest tests/e2e/ --e2e -v

# Run E2E for specific framework
uv run pytest tests/e2e/ --e2e --framework=crewai -v

# Type checking
uv run mypy src/

# Format code
uvx ruff format src/ tests/

# Lint with auto-fix
uvx ruff check src/ tests/ --fix

# Build package
uv build

# Run tox (all Python versions)
tox
```

## Code Style

| Aspect | Standard |
|--------|----------|
| Python version | 3.11+ required |
| Line length | 100 characters |
| Linter | Ruff |
| Formatter | Ruff |
| Type hints | Required on all public functions |
| Docstrings | Google style |
| Imports | Absolute, organized by stdlib/third-party/local |

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | When | Version Bump |
|--------|------|--------------|
| `feat(scope):` | New feature | Minor |
| `fix(scope):` | Bug fix | Patch |
| `docs:` | Documentation only | None |
| `refactor(scope):` | Code change (no behavior change) | None |
| `test:` | Adding/updating tests | None |
| `chore:` | Maintenance, deps | None |

Examples:
```bash
git commit -m "feat(runners): add AWS Bedrock runner"
git commit -m "fix(decomposer): handle missing framework gracefully"
git commit -m "docs: update architecture diagram"
```

## Key Patterns

### 1. Framework Detection

```python
from agentic_crew.core.decomposer import (
    detect_framework,
    get_runner,
    get_available_frameworks
)

# Auto-detect best available framework
framework = detect_framework()  # Returns "crewai", "langgraph", or "strands"

# List all available
available = get_available_frameworks()  # ["crewai", "langgraph"]

# Get specific runner
runner = get_runner("langgraph")
```

### 2. Running a Crew

```python
from agentic_crew import run_crew

# Auto-detect framework and run
result = run_crew(
    package="vendor-connectors",
    crew="connector_builder",
    inputs={"api_docs_url": "https://docs.meshy.ai/en"}
)

# Force specific framework
result = run_crew(
    package="my-package",
    crew="my_crew",
    inputs={"topic": "Python testing"},
    framework="crewai"  # Explicit framework choice
)
```

### 3. Implementing a Runner

```python
from agentic_crew.runners.base import BaseRunner

class MyFrameworkRunner(BaseRunner):
    def build_crew(self, config: dict) -> Any:
        """Build framework-specific crew from config."""
        # Convert config to framework's native types
        pass
    
    def run(self, crew: Any, inputs: dict[str, Any]) -> str:
        """Execute crew and return result."""
        pass
    
    def build_agent(self, config: dict) -> Any:
        """Build framework-specific agent."""
        pass
    
    def build_task(self, config: dict, agent: Any) -> Any:
        """Build framework-specific task."""
        pass
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Claude LLM access |
| `GITHUB_JBCOM_TOKEN` | Yes | GitHub operations for jbcom repos |
| `OPENROUTER_API_KEY` | No | Fallback LLM provider |
| `MESHY_API_KEY` | No | For Meshy-related crews |
| `AWS_*` | No | For Strands with Bedrock |

## Specialized Agent Documentation

For specific tasks, consult the specialist docs in `.github/agents/`:

| Task | Read |
|------|------|
| Implementing runners | `.github/agents/runner-developer.md` |
| Creating crews | `.github/agents/crew-builder.md` |
| Updating documentation | `.github/agents/documentation.md` |
| Writing/running tests | `.github/agents/test-runner.md` |
| Using connector_builder | `.github/agents/connector-builder.md` |

## Testing

### Unit Tests
```bash
uv run pytest tests/ -v --ignore=tests/e2e
```

### E2E Tests (requires API keys)
```bash
# Run all E2E
uv run pytest tests/e2e/ --e2e -v

# Framework-specific
uv run pytest tests/e2e/ --e2e --framework=crewai -v
uv run pytest tests/e2e/ --e2e --framework=langgraph -v
```

### Coverage
```bash
uv run pytest tests/ --cov=agentic_crew --cov-report=html
open htmlcov/index.html
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/agentic_crew/core/decomposer.py` | Framework detection and runner selection |
| `src/agentic_crew/runners/base.py` | Abstract runner interface |
| `src/agentic_crew/runners/crewai_runner.py` | CrewAI implementation |
| `src/agentic_crew/runners/langgraph_runner.py` | LangGraph implementation |
| `src/agentic_crew/runners/strands_runner.py` | Strands implementation |
| `src/agentic_crew/core/loader.py` | YAML config loading |
| `pyproject.toml` | Package config, dependencies, extras |
| `tox.ini` | Multi-version testing |

## Related Repositories

| Repository | Relationship |
|------------|--------------|
| [vendor-connectors](https://github.com/jbcom/vendor-connectors) | Uses agentic-crew for HTTP connector generation |
| [otterfall](https://github.com/jbcom/otterfall) | Game project using agentic crews |
| [directed-inputs-class](https://github.com/jbcom/directed-inputs-class) | Credential management |

## Session Management

```bash
# Start of session - check context
cat memory-bank/activeContext.md 2>/dev/null || echo "No memory bank"

# End of session - update context
echo "## Session: $(date +%Y-%m-%d)" >> memory-bank/activeContext.md
echo "- Work done summary" >> memory-bank/activeContext.md
```

## Common Operations

### Adding a New Framework Support

1. Create `src/agentic_crew/runners/{framework}_runner.py`
2. Implement `BaseRunner` interface
3. Add to `core/decomposer.py`:
   - `FRAMEWORK_PRIORITY`
   - `is_framework_available()`
   - `get_runner()`
4. Add optional dependency in `pyproject.toml`
5. Add tests in `tests/test_runners.py`
6. Update this documentation

### Creating a New Crew

1. Create `.crewai/crews/{crew_name}/config/`
2. Add `agents.yaml` with agent definitions
3. Add `tasks.yaml` with task definitions
4. Register in `.crewai/manifest.yaml`
5. Test: `uv run agentic-crew run <package> {crew_name}`

### PR Workflow

1. Create branch: `git checkout -b feat/my-feature`
2. Make changes, commit with conventional commits
3. Run tests: `uv run pytest tests/ -v`
4. Run lints: `uvx ruff check src/ tests/`
5. Push: `git push -u origin feat/my-feature`
6. Create PR: `GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh pr create`

---

**Remember**: When in doubt, read the code. The implementation in `src/agentic_crew/` is the source of truth.

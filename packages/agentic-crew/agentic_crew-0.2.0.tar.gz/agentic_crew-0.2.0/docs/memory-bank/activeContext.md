# Active Context - agentic-crew

## Current State (December 2024)

### Core Mission

`agentic-crew` is a **framework-agnostic AI crew orchestration library** that enables:
- Declaring crews once in YAML
- Running them on **CrewAI**, **LangGraph**, or **AWS Strands**
- Auto-detecting available frameworks

### Architecture

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

**Framework Priority**: CrewAI > LangGraph > Strands

### Implementation Status

#### Core Components ✅
- `core/decomposer.py` - Framework detection and runner selection
- `runners/base.py` - Abstract runner interface
- `runners/crewai_runner.py` - CrewAI implementation
- `runners/langgraph_runner.py` - LangGraph implementation (basic)
- `runners/strands_runner.py` - Strands implementation

#### Documentation ✅
- `AGENTS.md` - Comprehensive agent bootstrap doc
- `.github/agents/` - Specialized agent instructions
- `.cursor/rules/` - Cursor-specific rules
- `CLAUDE.md` - Claude guidance
- `.github/copilot-instructions.md` - Copilot guidance

#### CI/CD ✅
- `.github/workflows/ci.yml` - Build, test, lint, release
- `.github/workflows/codeql.yml` - Security analysis
- `.cursor/Dockerfile` - Development container

#### Pending ⏳
- Unit tests for decomposer (#3)
- Unit tests for runners (#4)
- connector_builder crew (#5)
- E2E tests (#6)
- CLI implementation (#7)

### Active Issues

| Issue | Description | Priority |
|-------|-------------|----------|
| #2 | EPIC: Framework Decomposition | High |
| #3 | Tests for decomposer | High |
| #4 | Tests for runners | High |
| #5 | connector_builder crew | Medium |
| #6 | E2E tests | Medium |
| #7 | CLI implementation | Medium |
| #8 | vendor-connectors integration | Medium |

### Key Use Case: Connector Generation

The `connector_builder` crew will:
1. Scrape API documentation (e.g., https://docs.meshy.ai/en)
2. Extract endpoint information
3. Generate typed Python HTTP client code
4. Output to vendor-connectors format

### Related Repositories

| Repository | Purpose | Relationship |
|------------|---------|--------------|
| [vendor-connectors](https://github.com/jbcom/vendor-connectors) | HTTP connectors | Uses agentic-crew for connector generation |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Original framework | Target runtime |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Graph agents | Target runtime |
| [Strands](https://github.com/strands-agents/strands-agents-python) | AWS agents | Target runtime |

### GitHub Project

Tracked in: [jbcom Ecosystem Integration](https://github.com/users/jbcom/projects/2)

---

## Session History

### Session: 2024-12-07
- Created repository and initial framework decomposition architecture
- Implemented core decomposer and runners for all three frameworks
- Created comprehensive documentation structure
- Set up CI/CD and development environment
- Created issues for planned work
- Opened PR #1 with all foundational work

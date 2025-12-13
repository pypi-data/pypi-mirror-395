# CLAUDE.md

This file provides guidance to Claude Code when working with agentic-crew.

## CRITICAL: Read AGENTS.md First

**ALWAYS read `AGENTS.md` for comprehensive instructions including:**
- GitHub authentication (`GITHUB_JBCOM_TOKEN`)
- Development commands
- Architecture overview
- Code style guidelines

## Quick Reference

```bash
# GitHub operations
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh <command>

# Development
uv sync --extra dev --extra tests --extra crewai
uv run pytest tests/ -v
uvx ruff check src/ tests/ --fix

# Run a crew
uv run agentic-crew run <package> <crew> --input "..."
```

## Overview

agentic-crew is a **framework-agnostic AI crew orchestration library**.

Key innovation: **Declare once, run anywhere**
- Define crews in YAML
- Run on CrewAI, LangGraph, or Strands
- Auto-detects best available framework

## Architecture

```
manifest.yaml → Loader → Decomposer → Runner
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          CrewAI          LangGraph        Strands
```

## Key Files

| File | Purpose |
|------|---------|
| `core/decomposer.py` | Framework detection and selection |
| `runners/base.py` | Abstract runner interface |
| `runners/crewai_runner.py` | CrewAI implementation |
| `runners/langgraph_runner.py` | LangGraph implementation |
| `runners/strands_runner.py` | Strands implementation |
| `core/loader.py` | YAML to crew objects |

## Commit Messages

Use conventional commits:
- `feat(runners): add LangGraph support` → minor
- `fix(decomposer): handle missing framework` → patch
- `docs: update architecture` → no release

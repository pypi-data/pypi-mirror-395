# Agent Directory

This directory contains specialized agent instructions. Read the root `AGENTS.md` first, then consult the relevant specialist.

## Available Specialists

| Agent | File | When to Use |
|-------|------|-------------|
| **Runner Developer** | `runner-developer.md` | Implementing/fixing framework runners |
| **Crew Builder** | `crew-builder.md` | Creating new crew definitions |
| **Documentation** | `documentation.md` | Updating docs, AGENTS.md, README |
| **Test Runner** | `test-runner.md` | Writing/running tests, debugging failures |
| **Connector Builder** | `connector-builder.md` | Using agentic-crew to generate HTTP connectors |

## Reading Order

1. **Always first**: `/AGENTS.md` (root project documentation)
2. **Then**: Specialist doc for your task
3. **Reference**: `.cursor/rules/*.mdc` for Cursor-specific rules

## Quick Links

- Root docs: `AGENTS.md`, `README.md`, `CLAUDE.md`
- Cursor rules: `.cursor/rules/`
- Copilot: `.github/copilot-instructions.md`
- CI/CD: `.github/workflows/`

## GitHub Authentication

All agents must use:

```bash
GH_TOKEN="$GITHUB_JBCOM_TOKEN" gh <command>
```

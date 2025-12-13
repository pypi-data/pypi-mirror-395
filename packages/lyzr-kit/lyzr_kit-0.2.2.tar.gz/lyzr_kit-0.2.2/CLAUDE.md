# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Project Overview

lyzr-kit is a Python SDK for managing AI agents via the Lyzr platform.

## CLI Commands

```bash
lk auth                    # Configure API credentials
lk ls                      # List agents (two tables)
lk get <source> [new-id]   # Clone and deploy agent
lk set <identifier>        # Update agent on platform
lk chat <identifier>       # Interactive chat session
```

**Note**: `agent` resource is optional. `lk ls` = `lk agent ls` = `lk a ls`

**Serial numbers**: Context-aware
- `get` → Built-in agents
- `set`/`chat` → Your agents

## Storage

| Location | Purpose |
|----------|---------|
| `src/lyzr_kit/collection/agents/` | Built-in agents (bundled) |
| `agents/` | User agents (via `lk agent get`) |

## Project Structure

```
src/lyzr_kit/
├── main.py              # CLI entry point
├── schemas/             # Pydantic models (agent.py, tool.py, feature.py)
├── collection/agents/   # Built-in agent YAMLs
├── commands/            # CLI implementations
│   ├── _console.py      # Shared Rich console
│   ├── _resolver.py     # Serial number resolver
│   ├── _websocket.py    # WebSocket event streaming
│   ├── agent.py         # Agent Typer app
│   ├── agent_list.py    # ls command
│   ├── agent_get.py     # get command
│   ├── agent_set.py     # set command
│   ├── agent_chat.py    # chat command (SSE + WebSocket)
│   ├── auth.py          # auth command
│   ├── tool.py          # stub
│   └── feature.py       # stub
├── storage/             # StorageManager, serialization, validation
└── utils/               # auth.py, platform.py

tests/
├── unit/commands/       # Command tests
├── unit/storage/        # Storage tests
└── integration/         # E2E tests
```

## Chat Implementation

Key files for chat functionality:
- `commands/agent_chat.py` - Main chat loop, UI boxes, SSE streaming
- `commands/_websocket.py` - WebSocket client, event parsing

Features:
- Session box (agent info, model, session ID, timestamp)
- Real-time WebSocket events (tool calls, memory, artifacts)
- SSE streaming for responses
- Metrics footer (latency, tokens)
- prompt_toolkit for keyboard shortcuts

## Build Commands

```bash
pip install -e .        # Install dev mode
pytest tests/ -v        # Run tests
ruff check src/         # Lint
mypy src/               # Type check
```

## Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Agents, CLI, storage | ✅ Done |
| 2 | Chat experience, WebSocket | ✅ Done |
| 3 | Sub-agents | Pending |
| 4 | Tools | Stub |
| 5 | Features | Stub |

## Specs

- `specs/concepts/` - Entity definitions
- `specs/implementation/` - Technical details
- `specs/phases/` - Roadmap

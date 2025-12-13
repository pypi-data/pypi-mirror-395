# Lyzr Kit

Python SDK for managing AI agents via the Lyzr platform.

## Installation

```bash
pip install lyzr-kit
```

## Quick Start

```bash
# 1. Authenticate
lk auth

# 2. List agents (two tables: Built-in + Your Agents)
lk ls

# 3. Deploy an agent
lk get chat-agent my-assistant

# 4. Chat with your agent
lk chat my-assistant

# 5. Modify and update
# Edit agents/my-assistant.yaml, then:
lk set my-assistant
```

## Chat Experience

- **Session box** - Shows agent name, model, session ID, timestamp
- **Real-time activity** - WebSocket events stream inline (tool calls, memory, artifacts)
- **Streaming responses** - Live markdown-rendered output
- **Metrics footer** - Latency and token usage per response
- **Keyboard shortcuts** - Full readline support (Option/Ctrl + arrows, history)
- **Exit** - Type `/exit` or press `Ctrl+C`

## CLI Commands

| Command | Description |
|---------|-------------|
| `lk auth` | Configure API credentials |
| `lk ls` | List all agents |
| `lk get <source> [id]` | Clone and deploy agent |
| `lk set <id>` | Update agent on platform |
| `lk chat <id>` | Interactive chat session |

**Note**: `agent` resource is optional. `lk ls` = `lk agent ls` = `lk a ls`

**Serial numbers**: Context-aware lookup
- `get` → Built-in agents (`lk get 1`)
- `set`/`chat` → Your agents (`lk chat 1`)

## Built-in Agents

| # | ID | Category |
|---|-----|----------|
| 1 | `chat-agent` | chat |
| 2 | `qa-agent` | qa |
| 3 | `code-reviewer` | qa |
| 4 | `content-writer` | chat |
| 5 | `customer-support` | chat |
| 6 | `data-analyst` | qa |
| 7 | `email-composer` | chat |
| 8 | `research-assistant` | chat |
| 9 | `sql-expert` | qa |
| 10 | `summarizer` | qa |
| 11 | `task-planner` | chat |
| 12 | `translator` | qa |

## Environment Variables

| Variable | Required |
|----------|----------|
| `LYZR_API_KEY` | Yes |
| `LYZR_USER_ID` | No |
| `LYZR_ORG_ID` | No |
| `LYZR_MEMBERSTACK_TOKEN` | No |

## Storage

- `agents/` - Your deployed agent configs
- `.env` - API credentials

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check src/
mypy src/
```

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Agents, CLI, storage | ✅ Done |
| 2 | Chat experience, WebSocket events | ✅ Done |
| 3 | Sub-agents | Pending |
| 4 | Tools | Pending |
| 5 | Features | Pending |

## License

MIT

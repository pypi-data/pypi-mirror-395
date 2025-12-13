# Lyzr Kit Specifications

Design specifications for the Lyzr Kit SDK.

## Structure

```
specs/
├── concepts/           # Entity definitions (agent, tool, feature)
├── implementation/     # Technical details (commands, storage, schema)
└── phases/             # Implementation roadmap (phase-1 through phase-5)
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `lk auth` | Configure API credentials |
| `lk ls` | List agents (two tables) |
| `lk get <source> [id]` | Clone and deploy agent |
| `lk set <id>` | Update agent on platform |
| `lk chat <id>` | Interactive chat session |

`agent` resource is optional. Serial numbers are context-aware (get → built-in, set/chat → local).

## Key Decisions

| Decision | Choice |
|----------|--------|
| Package name | `lyzr-kit` |
| CLI command | `lk` |
| Config format | YAML |
| Schema validation | Pydantic |

## Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Agents, CLI, storage | ✅ Done |
| 2 | Chat experience, WebSocket | ✅ Done |
| 3 | Sub-agents | Pending |
| 4 | Tools | Stub |
| 5 | Features | Stub |

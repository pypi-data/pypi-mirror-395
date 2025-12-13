# CLI Commands Specification

## Command Structure

```
lk [resource] <action> [args...]
```

`agent` resource is optional (default). All equivalent:
- `lk ls` = `lk agent ls` = `lk a ls`

| Resource | Short | Actions |
|----------|-------|---------|
| `agent` | `a` | `ls`, `get`, `set`, `chat` (default) |
| `tool` | `t` | stub (Phase 4) |
| `feature` | `f` | stub (Phase 5) |

## Agent Commands

| Command | Description |
|---------|-------------|
| `lk ls` | List agents in two tables |
| `lk get <source> [id]` | Clone and deploy to platform |
| `lk set <id>` | Update from local YAML |
| `lk chat <id>` | Interactive chat session |

### Serial Number Context

| Command | Context |
|---------|---------|
| `get` | Built-in agents |
| `set`/`chat` | Local agents |

## Chat Command

### Features
- **Session box** - Agent name, model, session ID, timestamp
- **WebSocket events** - Real-time activity (tool calls, memory, artifacts)
- **SSE streaming** - Live response rendering
- **Metrics footer** - Latency, token usage
- **Keyboard shortcuts** - Full readline (Option/Ctrl + arrows, history)
- **Exit** - `/exit` or `Ctrl+C`

### Display Format

```
╭─ Session ────────────────────────────────────────╮
│ Agent: My Assistant        Model: gpt-4         │
│ Session: abc123            Started: 14:32:15    │
╰──────────────────────────────────────────────────╯

You: What is the capital of France?

╭─ Agent ──────────────────────────────────────────╮
│ [Tool] Calling search_web...                    │
│ [Tool] search_web → {"results": [...]}          │
│ [Memory] Context updated                        │
│                                                  │
│ The capital of France is Paris.                 │
│──────────────────────────────────────────────────│
│ 1.23s                              45 → 128 tok │
╰──────────────────────────────────────────────────╯
```

### Event Types

| Event | Display |
|-------|---------|
| `tool_call_prepare` | `[Tool] Calling {name}...` |
| `tool_response` | `[Tool] {name} → {response}` |
| `context_memory_updated` | `[Memory] Context updated` |
| `artifact_create_success` | `[Artifact] Created: {name}` |
| `messages_retrieved` | `[Memory] Retrieved {count} messages` |

## Auth Command

```bash
lk auth
```

Prompts for:
- API key (required)
- User ID, Org ID, Memberstack token (optional)

Saves to `.env` and initializes `agents/` directory.

## Error Handling

| Error | Resolution |
|-------|------------|
| Serial not found | Shows agent list |
| ID exists | Use different ID |
| Not authenticated | Run `lk auth` |
| Agent not active | Run `lk agent get` first |

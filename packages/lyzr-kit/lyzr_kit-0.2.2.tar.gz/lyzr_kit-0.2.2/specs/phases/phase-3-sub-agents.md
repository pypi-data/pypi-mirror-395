# Phase 3: Sub-agents

## Overview

Phase 3 implements sub-agent orchestration, enabling agents to delegate tasks to other agents via the `sub_agents` array.

## Goals

- Enable agents to reference other agents as sub-agents
- Handle sub-agent resolution (local, built-in, missing)
- Implement circular dependency detection
- Support recursive deployment of sub-agents

## Deliverables

### 1. Sub-agent Resolution

When an agent references sub-agents, the system must resolve each sub-agent ID:

```python
def resolve_sub_agent(agent_id: str) -> Agent | None:
    """Resolve a sub-agent by ID.

    Resolution order:
    1. Local (local-kit/agents/<id>.yaml)
    2. Built-in (collection/agents/<id>.yaml)
    3. None (not found)
    """
    ...
```

### 2. Agent Schema Integration

```yaml
# Agent with sub-agents
id: "orchestrator-agent"
name: "Orchestrator"
category: "chat"
model:
  provider: "openai"
  name: "gpt-4"
  credential_id: "lyzr_openai"
sub_agents:
  - "research-assistant"
  - "summarizer"
  - "content-writer"
```

### 3. Cases to Handle

| Case | Behavior |
|------|----------|
| Sub-agent exists locally | Use local config |
| Sub-agent exists in built-in | Use built-in config |
| Sub-agent does not exist | Error with helpful message |
| Circular dependency (A → B → A) | Error with dependency chain |
| Sub-agent not deployed | Prompt to run `lk agent get` first |

### 4. Circular Dependency Detection

```python
def detect_circular_dependency(
    agent_id: str,
    visited: set[str] | None = None
) -> list[str] | None:
    """Detect circular dependencies in sub-agent graph.

    Returns:
        None if no cycle, or list of IDs forming the cycle.
    """
    ...
```

### 5. Recursive Deployment

When running `lk agent get parent-agent`:

1. Check if parent has sub-agents
2. For each sub-agent:
   - If not deployed, prompt user to deploy first
   - Or auto-deploy with `--recursive` flag
3. Deploy parent agent with sub-agent references

```bash
# Deploy with sub-agents recursively
lk agent get orchestrator-agent --recursive
```

### 6. CLI Enhancements

| Command | Enhancement |
|---------|-------------|
| `lk agent get <id>` | Validate sub-agents exist |
| `lk agent get <id> --recursive` | Deploy sub-agents first |
| `lk agent ls` | Show sub-agent count column |

### 7. Validation on Set

When running `lk agent set`:

- Validate all referenced sub-agents exist
- Check for circular dependencies
- Warn if sub-agents are not deployed

## Success Criteria

- Agent with `sub_agents` array deploys successfully
- Missing sub-agent shows clear error message
- Circular dependencies are detected and reported
- `--recursive` flag deploys sub-agents automatically
- Sub-agent validation runs on both `get` and `set`

## Dependencies

Requires Phase 1 and Phase 2 completion

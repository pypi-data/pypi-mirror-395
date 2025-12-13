"""Agent chat command implementation with real-time event streaming."""

import asyncio
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import httpx
import typer
from rich.box import ROUNDED
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from lyzr_kit.commands._auth_helper import require_auth
from lyzr_kit.commands._console import console
from lyzr_kit.commands._resolver import resolve_local_agent_id
from lyzr_kit.commands._websocket import WEBSOCKET_BASE_URL, ChatEvent, parse_event
from lyzr_kit.schemas.agent import Agent
from lyzr_kit.storage import StorageManager, format_schema_errors, validate_agent_yaml_file
from lyzr_kit.utils.auth import AuthConfig

# Chat API endpoints
STREAM_API_ENDPOINT = "https://agent-prod.studio.lyzr.ai/v3/inference/stream/"


@dataclass
class StreamState:
    """State for streaming chat session."""

    content: str = ""
    events: list[ChatEvent] = field(default_factory=list)
    is_streaming: bool = False
    start_time: float = 0.0
    first_chunk_time: float = 0.0
    end_time: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    error: str | None = None

    @property
    def latency_ms(self) -> float:
        """Calculate latency to first chunk in milliseconds."""
        if self.first_chunk_time > 0 and self.start_time > 0:
            return (self.first_chunk_time - self.start_time) * 1000
        return 0.0

    @property
    def total_time_ms(self) -> float:
        """Calculate total response time in milliseconds."""
        if self.end_time > 0 and self.start_time > 0:
            return (self.end_time - self.start_time) * 1000
        return 0.0

    def add_event(self, event: ChatEvent) -> None:
        """Add an event to the list."""
        self.events.append(event)

    def clear(self) -> None:
        """Clear state for next message."""
        self.content = ""
        self.events.clear()
        self.is_streaming = False
        self.start_time = 0.0
        self.first_chunk_time = 0.0
        self.end_time = 0.0
        self.tokens_in = 0
        self.tokens_out = 0
        self.error = None


def _format_timestamp(dt: datetime | None = None) -> str:
    """Format timestamp for display."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%H:%M:%S")


def _build_session_box(agent: Agent, session_id: str, start_time: str) -> Panel:
    """Build the session header box displayed at chat start."""
    # Create a simple table for session info (no borders)
    info_table = Table.grid(padding=(0, 2))
    info_table.add_column(style="dim", justify="right")
    info_table.add_column(style="bold")

    # Extract model name from ModelConfig object
    model_name = "default"
    if agent.model:
        model_name = agent.model.name if hasattr(agent.model, "name") else str(agent.model)

    info_table.add_row("Agent", agent.name)
    info_table.add_row("Model", model_name)
    info_table.add_row("Session", session_id[:8])
    info_table.add_row("Started", start_time)

    return Panel(
        info_table,
        title="[bold]Session[/bold]",
        title_align="center",
        border_style="blue",
        box=ROUNDED,
        padding=(0, 1),
    )


def _build_user_box(message: str, timestamp: str) -> Panel:
    """Build the user message box."""
    return Panel(
        Text(message),
        title="[cyan]You[/cyan]",
        title_align="left",
        subtitle=f"[dim]{timestamp}[/dim]",
        subtitle_align="right",
        border_style="cyan",
        box=ROUNDED,
        padding=(0, 1),
    )


def _decode_sse_data(data: str) -> str:
    """Decode escape sequences from SSE data."""
    return (
        data.replace("\\n", "\n")
        .replace('\\"', '"')
        .replace("\\'", "'")
        .replace("\\&", "&")
        .replace("\\r", "\r")
        .replace("\\\\", "\\")
        .replace("\\t", "\t")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
    )


def _separate_thinking_content(content: str) -> tuple[str | None, str]:
    """Extract thinking content from <think> tags."""
    think_match = re.search(r"<think>([\s\S]*?)</think>", content)
    if think_match:
        thinking = think_match.group(1).strip()
        actual_content = re.sub(r"<think>[\s\S]*?</think>", "", content).strip()
        return thinking, actual_content
    return None, content


def _build_agent_box(state: StreamState, timestamp: str) -> Panel:
    """Build the agent response box with 4-corner layout.

    Layout:
    - Top-left: "Agent" label
    - Top-right: Timestamp (shown via title formatting)
    - Bottom-left: Latency
    - Bottom-right: Token usage
    """
    content_parts = []

    # Events section (if any)
    if state.events:
        events_text = Text()
        for i, event in enumerate(state.events):
            prefix = "└─" if i == len(state.events) - 1 and not state.content else "├─"
            events_text.append(f"{prefix} ", style="dim")
            events_text.append(event.format_display(), style="dim cyan")
            if i < len(state.events) - 1 or state.content:
                events_text.append("\n")
        content_parts.append(events_text)

    # Response content
    if state.content:
        response_text = Text()
        if state.events:
            response_text.append("\n\n")
        response_text.append(state.content)
        content_parts.append(response_text)
    elif state.is_streaming and not state.events:
        content_parts.append(Text("Waiting for response...", style="dim italic"))

    # Error display (inside content area)
    if state.error:
        error_text = Text()
        if content_parts:
            error_text.append("\n\n")
        error_text.append(f"Error: {state.error}", style="bold red")
        content_parts.append(error_text)

    # Combine all parts
    if content_parts:
        combined = Group(*content_parts)
    else:
        combined = Text("...", style="dim")

    # Determine border style based on error state
    is_error_only = state.error and not state.content
    border_style = "red" if is_error_only else "green"
    title_label = "Error" if is_error_only else "Agent"
    title_style = "red" if is_error_only else "green"

    # Build title: "Agent" on left, timestamp on right
    # Rich doesn't support dual titles, so we embed timestamp in title string
    title = f"[{title_style}]{title_label}[/{title_style}] [dim]{timestamp}[/dim]"

    # Build subtitle with metrics (bottom edge) - only after streaming completes
    if not state.is_streaming and (state.content or state.error):
        # Format latency
        if state.total_time_ms > 0:
            latency_sec = state.total_time_ms / 1000
            latency_str = f"[bold]{latency_sec:.2f}s[/bold]"
        else:
            latency_str = "[dim]-[/dim]"

        # Format token usage
        if state.tokens_in > 0 or state.tokens_out > 0:
            tokens_str = f"[dim]{state.tokens_in} → {state.tokens_out} tokens[/dim]"
            subtitle = f"{latency_str}                                        {tokens_str}"
        else:
            subtitle = latency_str
    else:
        subtitle = None

    return Panel(
        combined,
        title=title,
        title_align="left",
        subtitle=subtitle,
        subtitle_align="left",
        border_style=border_style,
        box=ROUNDED,
        padding=(0, 1),
    )


def _stream_chat_message(
    auth: AuthConfig,
    agent: Agent,
    session_id: str,
    message: str,
    state: StreamState,
    user_timestamp: str | None = None,
) -> None:
    """Stream message from inference API with live display and WebSocket events.

    Args:
        auth: Authentication config
        agent: Agent to chat with
        session_id: Chat session ID
        message: User message
        state: Streaming state
        user_timestamp: Timestamp when user submitted the message
    """
    import json
    import threading

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "x-api-key": auth.api_key,
    }

    payload = {
        "agent_id": agent.platform_agent_id,
        "session_id": session_id,
        "user_id": auth.user_id or "default_user",
        "message": message,
    }

    # Clear state for new message
    state.clear()
    state.is_streaming = True
    state.start_time = time.time()

    # Use provided timestamp or generate new one
    timestamp = user_timestamp or _format_timestamp()
    buffer = ""

    # WebSocket event handling
    ws_events: list[ChatEvent] = []
    ws_stop_event = threading.Event()

    def receive_ws_events() -> None:
        """Receive events from WebSocket in a daemon thread."""
        try:
            import websockets

            async def _ws_loop():
                try:
                    url = f"{WEBSOCKET_BASE_URL}/ws/{session_id}?x-api-key={auth.api_key}"
                    async with websockets.connect(url, close_timeout=2) as ws:
                        while not ws_stop_event.is_set():
                            try:
                                msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                                data = json.loads(msg)
                                event = parse_event(data)
                                if event:
                                    ws_events.append(event)
                            except asyncio.TimeoutError:
                                continue
                            except Exception:
                                break
                except Exception:
                    pass

            asyncio.run(_ws_loop())
        except Exception:
            # WebSocket is optional - continue without it
            pass

    # Start WebSocket in daemon thread (will be killed when main thread exits)
    ws_thread = threading.Thread(target=receive_ws_events, daemon=True)
    ws_thread.start()

    try:
        with httpx.stream(
            "POST",
            STREAM_API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=120.0,
        ) as response:
            if response.status_code != 200:
                state.error = f"API returned status {response.status_code}"
                state.is_streaming = False
                state.end_time = time.time()
                console.print(_build_agent_box(state, timestamp))
                return

            with Live(_build_agent_box(state, timestamp), console=console, refresh_per_second=10) as live:
                for line in response.iter_lines():
                    # Merge WebSocket events
                    while ws_events:
                        event = ws_events.pop(0)
                        state.add_event(event)
                        live.update(_build_agent_box(state, timestamp))

                    if not line:
                        continue

                    if line.startswith("data: "):
                        data = line[6:]

                        if data == "[DONE]":
                            break

                        if data.startswith("[ERROR]"):
                            state.error = data[7:].strip()
                            break

                        decoded_data = _decode_sse_data(data)
                        if not decoded_data:
                            continue

                        # Mark first chunk time
                        if state.first_chunk_time == 0:
                            state.first_chunk_time = time.time()

                        buffer += decoded_data
                        thinking, content = _separate_thinking_content(buffer)

                        # If we have thinking content, add it as an event
                        if thinking and not any(e.event_type == "thinking" for e in state.events):
                            state.add_event(
                                ChatEvent(
                                    event_type="thinking",
                                    timestamp=datetime.now(),
                                    message=thinking[:100] + "..." if len(thinking) > 100 else thinking,
                                )
                            )

                        state.content = content
                        live.update(_build_agent_box(state, timestamp))

                # Drain remaining WebSocket events
                while ws_events:
                    event = ws_events.pop(0)
                    state.add_event(event)

                state.is_streaming = False
                state.end_time = time.time()
                live.update(_build_agent_box(state, timestamp))

    except httpx.TimeoutException:
        state.error = "Request timed out. The agent may be processing a complex query."
        state.is_streaming = False
        state.end_time = time.time()
    except Exception as e:
        state.error = str(e)
        state.is_streaming = False
        state.end_time = time.time()
    finally:
        # Signal WebSocket thread to stop
        ws_stop_event.set()
        # Give the thread a moment to clean up (but don't wait forever)
        ws_thread.join(timeout=0.5)

    console.print()


def chat_with_agent(identifier: str) -> None:
    """Start interactive chat session with an agent.

    Args:
        identifier: Agent ID or serial number.
    """
    from rich.status import Status

    auth = require_auth()

    # Validate all .env tokens are present
    if not auth.user_id or not auth.memberstack_token:
        console.print("[red]Error: Missing required .env tokens[/red]")
        console.print("[dim]LYZR_USER_ID and LYZR_MEMBERSTACK_TOKEN are required for chat.[/dim]")
        console.print("[dim]Run 'lk auth' to configure all tokens.[/dim]")
        raise typer.Exit(1)

    # Initialize with loading indicator
    with Status("[bold cyan]Loading agent...[/bold cyan]", console=console):
        # Resolve identifier (could be serial number or agent ID)
        # For 'chat' command, we only look up local agents
        storage = StorageManager()
        agent_id = resolve_local_agent_id(identifier, storage)
        if agent_id is None:
            raise typer.Exit(1)

        # Validate agent exists
        yaml_path = Path(storage.local_path) / "agents" / f"{agent_id}.yaml"

        if not yaml_path.exists():
            console.print(f"[red]Error: Agent '{agent_id}' not found in agents/[/red]")
            console.print("[dim]Run 'lk agent get <source> <id>' first to clone the agent[/dim]")
            raise typer.Exit(1)

        # Validate YAML and schema
        agent, schema_error, yaml_error = validate_agent_yaml_file(yaml_path)

        if yaml_error:
            console.print(f"[red]Error: {yaml_error}[/red]")
            raise typer.Exit(1)

        if schema_error:
            console.print(format_schema_errors(schema_error, agent_id))
            raise typer.Exit(1)

        if not agent:
            console.print(f"[red]Error: Failed to load agent '{agent_id}'[/red]")
            raise typer.Exit(1)

        # Validate agent is active
        if not agent.is_active:
            console.print(f"[red]Error: Agent '{agent_id}' is not active[/red]")
            console.print("[dim]Run 'lk agent get <source> <id>' to deploy the agent first[/dim]")
            raise typer.Exit(1)

        # Validate platform IDs exist
        if not agent.platform_agent_id:
            console.print(f"[red]Error: Agent '{agent_id}' has no platform ID[/red]")
            console.print("[dim]Delete the agent and run 'lk agent get' again[/dim]")
            raise typer.Exit(1)

    # Generate session ID
    import uuid

    session_id = str(uuid.uuid4())
    state = StreamState()

    # Session header box
    session_time = _format_timestamp()
    console.print()
    console.print(_build_session_box(agent, session_id, session_time))
    console.print("[dim]Type your message and press Enter. Use /exit to end.[/dim]\n")

    # Set up prompt_toolkit for better input handling
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.keys import Keys
    from prompt_toolkit.styles import Style

    # Create custom key bindings for Option/Cmd/Ctrl + arrow keys
    bindings = KeyBindings()

    @bindings.add(Keys.ControlLeft)  # Ctrl+Left - move word backward
    @bindings.add("escape", "b")  # Option+Left on macOS (sends Escape+b)
    def _(event):
        """Move cursor to the beginning of the previous word."""
        buff = event.current_buffer
        buff.cursor_position += buff.document.find_previous_word_beginning() or 0

    @bindings.add(Keys.ControlRight)  # Ctrl+Right - move word forward
    @bindings.add("escape", "f")  # Option+Right on macOS (sends Escape+f)
    def _(event):
        """Move cursor to the end of the next word."""
        buff = event.current_buffer
        buff.cursor_position += buff.document.find_next_word_ending() or 0

    @bindings.add("escape", Keys.Backspace)  # Option+Backspace - delete word backward
    def _(event):
        """Delete the word before the cursor."""
        buff = event.current_buffer
        pos = buff.document.find_previous_word_beginning() or 0
        if pos:
            buff.delete_before_cursor(count=-pos)

    @bindings.add("escape", "d")  # Option+Delete / Alt+D - delete word forward
    def _(event):
        """Delete the word after the cursor."""
        buff = event.current_buffer
        pos = buff.document.find_next_word_ending() or 0
        if pos:
            buff.delete(count=pos)

    # Create a prompt session with history and key bindings
    prompt_style = Style.from_dict({
        "prompt": "cyan",
    })
    history = InMemoryHistory()
    session = PromptSession(
        history=history,
        style=prompt_style,
        key_bindings=bindings,
        enable_system_prompt=False,
        enable_open_in_editor=False,
    )

    # Chat loop
    while True:
        try:
            # Get user input with full readline support (arrow keys, history, etc.)
            user_input = session.prompt([("class:prompt", "> ")])

            # Record timestamp immediately on submit
            timestamp = _format_timestamp()

            if user_input.strip().lower() == "/exit":
                console.print("\n[dim]Chat session ended.[/dim]")
                break

            if not user_input.strip():
                continue

            # Stream agent response (no separate user box - prompt line already shows input)
            _stream_chat_message(auth, agent, session_id, user_input, state, timestamp)

        except KeyboardInterrupt:
            console.print("\n\n[dim]Chat session ended.[/dim]")
            break
        except EOFError:
            # Ctrl+D pressed
            console.print("\n[dim]Chat session ended.[/dim]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}\n")

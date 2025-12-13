"""Watch command for ThreatWinds Pentest CLI.

Allows users to watch an already-running pentest and stream real-time updates.
This is the "late-join" feature that enables monitoring pentests that were started earlier.

Now supports interactive context injection - users can type hints/context while
watching that will be incorporated into the AI agent's reasoning.
"""

import sys
import asyncio
from typing import Dict, Any

import click
from rich.console import Console

from twpt_cli.config import load_credentials, get_grpc_endpoint
from twpt_cli.sdk import GRPCClient
from twpt_cli.sdk.models import UpdateType

console = Console()


@click.command()
@click.argument('pentest_id')
@click.option(
    '--no-history',
    is_flag=True,
    help='Skip replaying historical events (only show live updates)'
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Only show important status updates (hide debug messages)'
)
@click.option(
    '--interactive', '-i',
    is_flag=True,
    help='Enable interactive mode to inject context/hints during execution'
)
def watch(pentest_id: str, no_history: bool, quiet: bool, interactive: bool):
    """Watch a running pentest and stream real-time updates.

    This command allows you to connect to a pentest that is already running
    and receive live updates. By default, it will replay historical events
    that occurred before you connected.

    PENTEST_ID: The unique identifier of the pentest to watch (e.g., swift-falcon-strikes).

    In interactive mode (-i), you can type hints/context that will be
    incorporated into the AI agent's reasoning in real-time.

    Examples:
        twpt-cli watch swift-falcon-strikes                    # Watch with history
        twpt-cli watch dark-storm-rises --no-history           # Only live updates
        twpt-cli watch cyber-hawk-hunts -q                     # Quiet mode (no debug)
        twpt-cli watch bold-titan-guards -i                    # Interactive mode
    """
    # Load credentials
    creds = load_credentials()
    if not creds:
        console.print("[red]Not configured. Please run: twpt-cli configure[/red]")
        sys.exit(1)

    console.print(f"\n[cyan]Watching pentest {pentest_id}...[/cyan]\n")

    if not no_history:
        console.print("[dim]Replaying historical events...[/dim]\n")

    if interactive:
        console.print("[green bold]Interactive mode enabled[/green bold]")
        console.print("[dim]Type a hint and press Enter to inject context into the agent.[/dim]")
        console.print("[dim]Prefix with '!' for HIGH priority, '!!' for IMMEDIATE priority.[/dim]")
        console.print("[dim]Press Ctrl+C to stop watching.[/dim]\n")

    # Run the async streaming
    try:
        if interactive:
            asyncio.run(stream_pentest_interactive(
                pentest_id, creds,
                include_history=not no_history,
                quiet=quiet
            ))
        else:
            asyncio.run(stream_pentest(
                pentest_id, creds,
                include_history=not no_history,
                quiet=quiet
            ))
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Stopped watching pentest[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


async def stream_pentest(pentest_id: str, creds, include_history: bool, quiet: bool):
    """Stream pentest updates via gRPC subscribe (non-interactive).

    Args:
        pentest_id: Pentest identifier
        creds: API credentials
        include_history: Whether to replay historical events
        quiet: Whether to suppress debug messages
    """
    client = GRPCClient(get_grpc_endpoint(), creds)
    completed = False

    try:
        console.print("[dim]Streaming pentest updates (Ctrl+C to stop)...[/dim]\n")

        async for response in client.subscribe_pentest_stream(pentest_id, include_history):
            # Check for completion
            if response.get('type') == 'pentest_data':
                if response.get('status') == 'COMPLETED':
                    completed = True

            handle_stream_response(response, quiet)

    except Exception as e:
        raise e
    finally:
        await client.close()

    # Auto-download on completion
    if completed:
        console.print("\n[cyan]Auto-downloading evidence...[/cyan]")
        try:
            from twpt_cli.commands.download_evidence import download_pentest_evidence
            download_pentest_evidence(pentest_id, creds)
        except Exception as e:
            console.print(f"[yellow]Auto-download failed: {e}[/yellow]")


async def stream_pentest_interactive(pentest_id: str, creds, include_history: bool, quiet: bool):
    """Stream pentest updates with interactive context injection support.

    This mode enables users to type hints/context while watching. The input is
    sent to the agent and incorporated into its reasoning at the next step.

    Args:
        pentest_id: Pentest identifier
        creds: API credentials
        include_history: Whether to replay historical events
        quiet: Whether to suppress debug messages
    """
    client = GRPCClient(get_grpc_endpoint(), creds)
    completed = False

    try:
        console.print("[dim]Streaming pentest updates (type hints to inject context)...[/dim]\n")

        # Get interactive stream with request queue
        request_queue, response_stream, cleanup = await client.subscribe_pentest_stream_interactive(
            pentest_id, include_history
        )

        # Create tasks for concurrent input and output handling
        input_task = asyncio.create_task(
            handle_user_input(pentest_id, request_queue, client)
        )
        output_task = asyncio.create_task(
            handle_stream_output(response_stream, quiet, lambda: completed)
        )

        # Wait for either task to complete (output finishes on pentest complete or error)
        done, pending = await asyncio.wait(
            [input_task, output_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        # Check if pentest completed
        for task in done:
            result = task.result()
            if result == 'completed':
                completed = True

        # Cancel pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Cleanup
        await cleanup()

    except Exception as e:
        raise e
    finally:
        await client.close()

    # Auto-download on completion
    if completed:
        console.print("\n[cyan]Auto-downloading evidence...[/cyan]")
        try:
            from twpt_cli.commands.download_evidence import download_pentest_evidence
            download_pentest_evidence(pentest_id, creds)
        except Exception as e:
            console.print(f"[yellow]Auto-download failed: {e}[/yellow]")


async def handle_user_input(pentest_id: str, request_queue: asyncio.Queue, client: GRPCClient):
    """Handle user input for context injection.

    Runs in a separate task, reading from stdin and sending inject requests.

    Args:
        pentest_id: Pentest identifier
        request_queue: Queue for sending requests to gRPC stream
        client: GRPCClient for creating request messages
    """
    loop = asyncio.get_event_loop()

    while True:
        try:
            # Read input in a thread-safe way
            line = await loop.run_in_executor(None, sys.stdin.readline)

            if not line:
                # EOF
                break

            line = line.strip()
            if not line:
                continue

            # Parse priority from prefix
            priority = "NORMAL"
            context = line

            if line.startswith("!!"):
                priority = "IMMEDIATE"
                context = line[2:].strip()
            elif line.startswith("!"):
                priority = "HIGH"
                context = line[1:].strip()

            if not context:
                continue

            # Create and send inject request
            inject_request = client.create_inject_context_request(
                pentest_id=pentest_id,
                context=context,
                priority=priority
            )

            await request_queue.put(inject_request)
            console.print(f"[green]→ Hint queued ({priority})[/green]", style="dim")

        except Exception as e:
            console.print(f"[red]Input error: {e}[/red]", style="dim")


async def handle_stream_output(response_stream, quiet: bool, is_completed_check):
    """Handle streaming output from gRPC.

    Args:
        response_stream: Async iterator of responses
        quiet: Whether to suppress debug messages
        is_completed_check: Callable that returns completion status

    Returns:
        'completed' if pentest completed, None otherwise
    """
    try:
        async for response in response_stream:
            # Check for completion
            if response.get('type') == 'pentest_data':
                if response.get('status') == 'COMPLETED':
                    handle_stream_response(response, quiet)
                    return 'completed'

            handle_stream_response(response, quiet)

    except asyncio.CancelledError:
        pass
    except Exception as e:
        console.print(f"[red]Stream error: {e}[/red]")

    return None


def handle_stream_response(response: Dict[str, Any], quiet: bool = False):
    """Handle a streaming response from gRPC.

    Args:
        response: Parsed response dictionary
        quiet: Whether to suppress debug messages
    """
    response_type = response.get('type')

    if response_type == 'subscribe_response':
        # Subscription confirmation
        is_running = response.get('is_running', False)
        status = "[green]running[/green]" if is_running else "[yellow]completed/stopped[/yellow]"
        console.print(f"[green bold]Watching pentest: {response['pentest_id']}[/green bold]")
        console.print(f"  Status: {status}")
        console.print(f"  {response.get('message', '')}", style="dim")
        console.print()

    elif response_type == 'pentest_data':
        # Full pentest state update
        display_pentest_status(response)

    elif response_type == 'status_update':
        update_type = response.get('update_type')
        message = response.get('message', '')

        # Skip debug messages in quiet mode
        if quiet and update_type == UpdateType.DEBUG.value:
            return

        # Only display if there's a message
        if message:
            # Map update types to symbols and colors
            type_map = {
                UpdateType.INFO.value: ('ℹ', 'blue'),
                UpdateType.ERROR.value: ('✗', 'red'),
                UpdateType.STATUS.value: ('◆', 'cyan'),
                UpdateType.DEBUG.value: ('⚙', 'dim'),
            }

            symbol, color = type_map.get(update_type, ('•', 'white'))
            console.print(f"{symbol} {message}", style=color)

        # If there's pentest data in the status update, display it
        if response.get('data'):
            display_pentest_status(response['data'])

    elif response_type == 'context_ack':
        # Context injection acknowledgement
        accepted = response.get('accepted', False)
        message = response.get('message', '')
        if accepted:
            console.print(f"[green]✓ Context accepted: {message}[/green]", style="dim")
        else:
            console.print(f"[yellow]✗ Context rejected: {message}[/yellow]")

    elif response_type == 'error':
        console.print(f"[red]Error: {response['error']}[/red]")
        if response.get('details'):
            console.print(f"  [dim red]Details: {response['details']}[/dim red]")

    elif response_type == 'pong':
        # Keepalive response - ignore silently
        pass

    else:
        if not quiet:
            console.print(f"[dim]Unknown response: {response}[/dim]")


def display_pentest_status(data: Dict[str, Any]):
    """Display pentest status information.

    Args:
        data: Pentest data dictionary
    """
    status = data.get('status', 'UNKNOWN')
    status_colors = {
        "PENDING": "yellow",
        "IN_PROGRESS": "cyan",
        "COMPLETED": "green",
        "FAILED": "red",
    }
    status_color = status_colors.get(status, "white")

    console.print(f"\n[cyan bold]◆ Pentest Status[/cyan bold]")
    console.print(f"  ID: {data.get('id', 'N/A')}")
    console.print(f"  Status: [{status_color}]{status}[/{status_color}]")

    severity = data.get('severity')
    if severity and severity != 'NONE' and severity != 'SEVERITY_UNSPECIFIED':
        severity_colors = {
            "LOW": "blue",
            "MEDIUM": "yellow",
            "HIGH": "orange1",
            "CRITICAL": "red",
        }
        sev_color = severity_colors.get(severity, "white")
        console.print(f"  Severity: [{sev_color}]{severity}[/{sev_color}]")

    findings = data.get('findings', 0)
    if findings:
        console.print(f"  Findings: {findings}")

    # Display target statuses
    targets = data.get('targets', [])
    if targets:
        console.print(f"  Targets ({len(targets)}):")
        for target in targets:
            target_status = target.get('status', 'UNKNOWN')
            target_color = status_colors.get(target_status, "white")
            phase = target.get('phase', '')

            # Format phase nicely
            if phase and phase != 'PHASE_UNSPECIFIED':
                phase_display = f" → {phase}"
            else:
                phase_display = ""

            console.print(
                f"    • {target.get('target', 'N/A')}: "
                f"[{target_color}]{target_status}[/{target_color}]{phase_display}"
            )

    console.print()

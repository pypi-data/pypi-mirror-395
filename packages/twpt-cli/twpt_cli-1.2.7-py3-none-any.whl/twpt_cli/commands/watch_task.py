"""Watch task command for ThreatWinds Pentest CLI.

This command allows users to monitor a running custom task with real-time
streaming updates, similar to the --watch flag on the run command.
"""

import sys
import asyncio
from typing import Dict, Any

import click
from rich.console import Console

from twpt_cli.config import load_credentials, get_grpc_endpoint
from twpt_cli.sdk.grpc_client import GRPCClient
from twpt_cli.sdk.models import UpdateType

console = Console()


def _truncate_id(task_id: str, max_length: int = 20) -> str:
    """Truncate task/pentest ID for display, handling both UUID and friendly formats."""
    if not task_id or len(task_id) <= max_length:
        return task_id or ""

    parts = task_id.split('-')

    # UUID: show first 8 + last 4
    if len(parts) == 5 and len(task_id) == 36:
        return f"{task_id[:8]}...{task_id[-4:]}"

    # Friendly ID: show first 2 words
    if len(parts) >= 3 and all(p.isalpha() for p in parts[:3]):
        short = f"{parts[0]}-{parts[1]}..."
        return short if len(short) <= max_length else f"{task_id[:max_length-3]}..."

    return f"{task_id[:max_length-3]}..."


def handle_stream_response(response: Dict[str, Any]):
    """Handle a streaming response from gRPC."""
    from twpt_cli.sdk import pentest_pb2

    response_type = response.get('type')

    if response_type == 'custom_task_data':
        status = response.get('status', 'PENDING')
        if isinstance(status, int):
            status = pentest_pb2.Status.Name(status)

        status_colors = {
            "PENDING": "yellow",
            "IN_PROGRESS": "blue",
            "COMPLETED": "green",
            "FAILED": "red"
        }
        status_color = status_colors.get(status, "white")

        console.print(f"\n[cyan]◆ Task Status Update[/cyan]")
        console.print(f"  ID: {response.get('id', 'N/A')}")
        console.print(f"  Status: [{status_color}]{status}[/{status_color}]")
        console.print(f"  Target: {response.get('target', 'N/A')}")
        console.print(f"  Description: {response.get('description', 'N/A')}")

        if response.get('findings'):
            console.print(f"  Findings: {response.get('findings', 0)}")
        if response.get('severity'):
            severity = response.get('severity')
            if isinstance(severity, int):
                severity = pentest_pb2.Severity.Name(severity)
            console.print(f"  Severity: {severity}")

    elif response_type == 'subscribe_custom_task_response':
        task_id = response.get('task_id')
        is_running = response.get('is_running', False)
        status = "running" if is_running else "completed"
        display_id = _truncate_id(task_id)
        console.print(f"[cyan]◆[/cyan] Subscribed to task [cyan]{display_id}[/cyan] ({status})")

    elif response_type == 'status_update':
        update_type = response.get('update_type')
        message = response.get('message', '')

        if message:
            type_map = {
                UpdateType.INFO.value: ('ℹ', 'blue'),
                UpdateType.ERROR.value: ('✗', 'red'),
                UpdateType.STATUS.value: ('◆', 'cyan'),
                UpdateType.DEBUG.value: ('⚙', 'dim'),
            }

            symbol, color = type_map.get(update_type, ('•', 'white'))
            console.print(f"{symbol} {message}", style=color)

    elif response_type == 'error':
        console.print(f"[red]✗ Error:[/red] {response.get('error')}")
        if response.get('details'):
            console.print(f"  [dim]{response['details']}[/dim]")


async def watch_task_async(task_id: str, grpc_address: str, credentials, include_history: bool):
    """Watch a running task with real-time streaming."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        console.print(f"\n[cyan]Streaming task updates[/cyan] (Ctrl+C to exit)...\n")

        async for response in grpc_client.subscribe_custom_task_stream(
            task_id=task_id,
            include_history=include_history
        ):
            handle_stream_response(response)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Stream interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]✗ Streaming error:[/red] {str(e)}")
    finally:
        if grpc_client:
            try:
                await grpc_client.close()
            except Exception:
                pass


@click.command()
@click.argument('task_id')
@click.option(
    '--no-history',
    is_flag=True,
    help='Skip replaying historical events, only show new updates'
)
def watch_task(task_id: str, no_history: bool):
    """Watch a custom task in real-time.

    Connect to a running or completed task to stream progress updates.
    Works like the --watch flag on the run command.

    Examples:
        twpt-cli watch-task abc123-def456
        twpt-cli watch-task abc123-def456 --no-history
    """
    # Load credentials
    creds = load_credentials()
    if not creds:
        console.print("[red]✗ Not configured.[/red] Please run: twpt-cli configure")
        sys.exit(1)

    grpc_address = get_grpc_endpoint()

    try:
        asyncio.run(watch_task_async(
            task_id=task_id,
            grpc_address=grpc_address,
            credentials=creds,
            include_history=not no_history
        ))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        sys.exit(1)

"""Custom task command for ThreatWinds Pentest CLI.

This command allows users to run ad-hoc pentesting tasks using natural
language descriptions. Works like regular pentests with:
- Non-blocking execution (task runs in background)
- Task ID returned immediately
- Optional --watch for real-time streaming
- Target extraction similar to run command
"""

import sys
import asyncio
import ipaddress
from typing import Optional, List, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.markdown import Markdown

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


def is_public_target(target: str) -> bool:
    """Determine if a target is a public IP or domain.

    Private targets include:
    - Private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
    - Loopback (127.0.0.0/8)
    - Link-local (169.254.0.0/16)
    - localhost and .local domains

    Args:
        target: IP address or domain name

    Returns:
        True if the target is public, False if private
    """
    # Strip protocol and path if present
    target_clean = target.split('://')[1] if '://' in target else target
    target_clean = target_clean.split('/')[0]  # Remove path
    target_clean = target_clean.split(':')[0]  # Remove port

    # Check if it's localhost or .local domain
    if target_clean.lower() in ('localhost', 'localhost.localdomain'):
        return False
    if target_clean.lower().endswith('.local'):
        return False

    # Try to parse as IP address
    try:
        ip = ipaddress.ip_address(target_clean)
        return not ip.is_private and not ip.is_loopback and not ip.is_link_local and not ip.is_reserved
    except ValueError:
        # Not a valid IP, treat as domain - assume public
        return True


def display_task_summary(description: str, target: str, parameters: List[str]):
    """Display a summary of the task request (like pentest summary)."""
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║            Custom Task Request               ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    console.print(f"Description: [white]{description}[/white]")
    console.print(f"Target: [cyan]{target}[/cyan]")
    if parameters:
        console.print(f"Parameters: [dim]{', '.join(parameters)}[/dim]")


async def schedule_task(
    description: str,
    target: str,
    parameters: List[str],
    grpc_address: str,
    credentials,
    task_id: Optional[str] = None
) -> Optional[str]:
    """Schedule a custom task (non-blocking) and return task ID."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        # Get first response only (non-blocking)
        async for response in grpc_client.submit_custom_task_stream(
            description=description,
            target=target,
            parameters=parameters,
            task_id=task_id
        ):
            response_type = response.get('type', 'unknown')

            if response_type == 'custom_task_response':
                returned_task_id = response.get('task_id')
                message = response.get('message', '')
                console.print(f"\n[green]✓[/green] {message}", style="green bold")
                console.print(f"Task ID: [cyan]{returned_task_id}[/cyan]")
                return returned_task_id

            elif response_type == 'error':
                error_msg = response.get('error', 'Unknown error')
                details = response.get('details', '')
                console.print(f"\n[red]✗ Error:[/red] {error_msg}")
                if details:
                    console.print(f"[dim]{details}[/dim]")
                return None

    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        return None

    finally:
        if grpc_client:
            try:
                await grpc_client.close()
            except Exception:
                pass


async def watch_task(
    task_id: str,
    grpc_address: str,
    credentials,
    include_history: bool = True
):
    """Watch a running task with real-time streaming."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        console.print(f"\nStreaming task updates (Ctrl+C to exit)...\n", style="dim")

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


async def schedule_and_watch_task(
    description: str,
    target: str,
    parameters: List[str],
    grpc_address: str,
    credentials,
    task_id: Optional[str] = None
):
    """Schedule a task and stream real-time updates."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        console.print(f"\n[cyan]⚙ Starting task with real-time streaming...[/cyan]\n")

        async for response in grpc_client.submit_custom_task_stream(
            description=description,
            target=target,
            parameters=parameters,
            task_id=task_id
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


def handle_stream_response(response: Dict[str, Any]):
    """Handle a streaming response from gRPC."""
    response_type = response.get('type')

    if response_type == 'custom_task_response':
        task_id = response.get('task_id')
        message = response.get('message', '')
        console.print(f"[green]✓[/green] Task scheduled: [cyan]{task_id}[/cyan]")
        if message:
            console.print(f"  [dim]{message}[/dim]")

    elif response_type == 'custom_task_data':
        display_task_status(response)

    elif response_type == 'pentest_data':
        # Handle guided pentest data (uses pentest_data format)
        display_guided_pentest_status(response)

    elif response_type == 'subscribe_custom_task_response':
        task_id = response.get('task_id')
        is_running = response.get('is_running', False)
        status = "running" if is_running else "completed"
        display_id = _truncate_id(task_id)
        console.print(f"[cyan]◆[/cyan] Subscribed to task [cyan]{display_id}[/cyan] ({status})")

    elif response_type == 'status_update':
        update_type = response.get('update_type')
        message = response.get('message', '')
        task_complete = response.get('task_complete', False)

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

        # Show task complete indicator
        if task_complete:
            console.print()
            console.print("[green]━" * 50 + "[/green]")

    elif response_type == 'error':
        console.print(f"[red]✗ Error:[/red] {response.get('error')}")
        if response.get('details'):
            console.print(f"  [dim]{response['details']}[/dim]")

    else:
        # Unknown response type - ignore silently
        pass


def display_guided_pentest_status(data: Dict[str, Any]):
    """Display guided pentest status update (from pentest_data format)."""
    from twpt_cli.sdk import pentest_pb2

    status = data.get('status', 'PENDING')
    if isinstance(status, int):
        status = pentest_pb2.Status.Name(status)

    # For guided pentests, the target is in targets[0].target
    targets = data.get('targets', [])
    target = targets[0].get('target', 'N/A') if targets else 'N/A'
    summary = data.get('summary', '')
    description = data.get('description', '')

    # Convert to the format expected by display_task_status
    converted_data = {
        'id': data.get('id', 'N/A'),
        'status': status,
        'target': target,
        'summary': summary,
        'description': description,
        'findings': data.get('findings', 0),
        'severity': data.get('severity'),
    }

    display_task_status(converted_data)


def display_task_status(data: Dict[str, Any]):
    """Display task status update."""
    from twpt_cli.sdk import pentest_pb2

    status = data.get('status', 'PENDING')
    if isinstance(status, int):
        status = pentest_pb2.Status.Name(status)

    status_colors = {
        "PENDING": "yellow",
        "IN_PROGRESS": "blue",
        "COMPLETED": "green",
        "FAILED": "red"
    }
    status_color = status_colors.get(status, "white")

    # For completed tasks, show a nice summary box
    if status == "COMPLETED":
        task_id = data.get('id', 'N/A')
        target = data.get('target', 'N/A')
        summary = data.get('summary', '')

        console.print()
        console.print("╔══════════════════════════════════════════════╗", style="green")
        console.print("║            Task Completed                    ║", style="green")
        console.print("╚══════════════════════════════════════════════╝", style="green")
        console.print()
        console.print(f"  [green]✓[/green] Target: {target}")
        console.print(f"  [green]✓[/green] Status: [green]COMPLETED[/green]")

        if data.get('findings'):
            console.print(f"  [green]✓[/green] Findings: {data.get('findings', 0)}")

        if summary:
            console.print()
            console.print("  [bold]Summary:[/bold]")
            # Display summary in a cleaner way (first 300 chars)
            display_summary = summary[:300] + "..." if len(summary) > 300 else summary
            for line in display_summary.split('\n')[:10]:
                if line.strip():
                    console.print(f"    {line.strip()}")

        console.print()
        # Show full task ID for copy/paste since friendly IDs are short enough
        console.print(f"  [dim]View details: task --get {task_id}[/dim]")
        console.print(f"  [dim]Download evidence: download-task {task_id}[/dim]")
        console.print()

    elif status == "FAILED":
        console.print()
        console.print("╔══════════════════════════════════════════════╗", style="red")
        console.print("║              Task Failed                     ║", style="red")
        console.print("╚══════════════════════════════════════════════╝", style="red")
        console.print()
        console.print(f"  [red]✗[/red] Target: {data.get('target', 'N/A')}")
        console.print(f"  [red]✗[/red] Status: [red]FAILED[/red]")
        if data.get('summary'):
            console.print(f"  [red]✗[/red] Error: {data.get('summary', '')[:200]}")
        console.print()

    else:
        # For in-progress updates, keep it minimal
        console.print(f"\n[cyan]◆ Task Status Update[/cyan]")
        console.print(f"  ID: {data.get('id', 'N/A')}")
        console.print(f"  Status: [{status_color}]{status}[/{status_color}]")
        console.print(f"  Target: {data.get('target', 'N/A')}")
        console.print(f"  Description: {data.get('description', 'N/A')}")

        if data.get('findings'):
            console.print(f"  Findings: {data.get('findings', 0)}")
        if data.get('severity'):
            severity = data.get('severity')
            if isinstance(severity, int):
                severity = pentest_pb2.Severity.Name(severity)
            console.print(f"  Severity: {severity}")


@click.command()
@click.argument('description', required=False)
@click.option(
    '--target', '-t',
    required=False,
    help='Target to test (IP, domain, or URL)'
)
@click.option(
    '--param', '-p',
    multiple=True,
    help='Additional parameters (can be used multiple times)'
)
@click.option(
    '--watch', '-w',
    is_flag=True,
    help='Watch task progress in real-time (streaming mode)'
)
@click.option(
    '--session', '-s',
    required=False,
    help='Continue an existing task session'
)
@click.option(
    '--list', 'list_tasks',
    is_flag=True,
    help='List all custom task sessions'
)
@click.option(
    '--get',
    'get_task',
    required=False,
    help='Get details of a specific task'
)
@click.option(
    '--close',
    required=False,
    help='Close a task session by ID'
)
def custom_task(
    description: Optional[str],
    target: Optional[str],
    param: tuple,
    watch: bool,
    session: Optional[str],
    list_tasks: bool,
    get_task: Optional[str],
    close: Optional[str]
):
    """Execute a custom penetration testing task.

    By default, tasks run in the background (non-blocking).
    Use --watch to stream real-time progress like regular pentests.

    Examples:
        twpt-cli task "port scan" --target 192.168.1.1
        twpt-cli task "port scan" -t 192.168.1.1 --watch
        twpt-cli task "web vulnerability scan" -t example.com -w
        twpt-cli task "check for SQL injection" -t http://example.com/login
        twpt-cli task --list
        twpt-cli task --get <task-id>
        twpt-cli task --close <task-id>

    Continue a session:
        twpt-cli task "now check for XSS" -t example.com --session <task-id>
    """
    # Load credentials
    creds = load_credentials()
    if not creds:
        console.print("[red]✗ Not configured.[/red] Please run: twpt-cli configure")
        sys.exit(1)

    grpc_address = get_grpc_endpoint()

    # Handle --list
    if list_tasks:
        asyncio.run(list_custom_tasks_async(grpc_address, creds))
        return

    # Handle --get
    if get_task:
        asyncio.run(get_custom_task_async(get_task, grpc_address, creds))
        return

    # Handle --close
    if close:
        asyncio.run(close_custom_task_async(close, grpc_address, creds))
        return

    # Validate required args for task submission
    if not description:
        console.print("[red]✗ Error:[/red] Please provide a task description.")
        console.print("\nExample: twpt-cli task \"port scan\" --target 192.168.1.1")
        sys.exit(1)

    if not target:
        console.print("[red]✗ Error:[/red] Please provide a target with --target.")
        console.print("\nExample: twpt-cli task \"port scan\" --target 192.168.1.1")
        sys.exit(1)

    parameters = list(param) if param else []

    # Display task summary (like pentest summary)
    display_task_summary(description, target, parameters)

    try:
        if watch:
            # Streaming mode - schedule and watch
            asyncio.run(schedule_and_watch_task(
                description=description,
                target=target,
                parameters=parameters,
                grpc_address=grpc_address,
                credentials=creds,
                task_id=session
            ))
        else:
            # Non-blocking mode - schedule and return
            task_id = asyncio.run(schedule_task(
                description=description,
                target=target,
                parameters=parameters,
                grpc_address=grpc_address,
                credentials=creds,
                task_id=session
            ))

            if task_id:
                console.print("\nYou can check the status with:", style="dim")
                console.print(f"  twpt-cli task --get {task_id}", style="white")
                console.print("\nOr watch real-time progress with:", style="dim")
                console.print(f"  twpt-cli watch-task {task_id}", style="white")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {str(e)}")
        sys.exit(1)


async def list_custom_tasks_async(grpc_address: str, credentials):
    """List all custom task sessions."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        response = await grpc_client.list_custom_tasks(page=1, page_size=50)

        if response.get('type') == 'error':
            console.print(f"[red]✗ Error:[/red] {response.get('error')}")
            return

        if response.get('type') == 'custom_task_list':
            tasks = response.get('tasks', [])
            total = response.get('total', 0)

            if not tasks:
                console.print("[yellow]No custom task sessions found.[/yellow]")
                return

            console.print(f"\n[bold cyan]Custom Tasks ({total} total)[/bold cyan]")
            console.print("─" * 90)

            # Table display like pentest list
            table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 1))
            table.add_column("ID", style="white", no_wrap=True)
            table.add_column("Status", style="white")
            table.add_column("Target", style="white")
            table.add_column("Description", style="white", max_width=30)
            table.add_column("Findings", justify="center")

            status_colors = {
                "PENDING": "yellow",
                "IN_PROGRESS": "blue",
                "COMPLETED": "green",
                "FAILED": "red"
            }

            for task in tasks:
                status = task.get('status', 'PENDING')
                # Handle protobuf enum
                if isinstance(status, int):
                    from twpt_cli.sdk import pentest_pb2
                    status = pentest_pb2.Status.Name(status)

                status_style = status_colors.get(status, "white")
                target = task.get('target', '-')[:20]
                desc = task.get('description', '-')[:30]

                table.add_row(
                    task.get('id', 'N/A'),
                    f"[{status_style}]{status}[/{status_style}]",
                    target,
                    desc,
                    str(task.get('findings', 0))
                )

            console.print(table)
            console.print()
            console.print("[dim]task --get <id>[/dim] details  •  [dim]watch-task <id>[/dim] monitor  •  [dim]download-task <id>[/dim] evidence")
            console.print()

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")

    finally:
        if grpc_client:
            try:
                await grpc_client.close()
            except Exception:
                pass


async def get_custom_task_async(task_id: str, grpc_address: str, credentials):
    """Get details of a specific custom task."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        response = await grpc_client.get_custom_task(task_id)

        if response.get('type') == 'error':
            console.print(f"[red]✗ Error:[/red] {response.get('error')}")
            return

        if response.get('type') == 'custom_task_data':
            display_task_details(response)

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")

    finally:
        if grpc_client:
            try:
                await grpc_client.close()
            except Exception:
                pass


def display_task_details(task: Dict[str, Any]):
    """Display detailed task information."""
    from twpt_cli.sdk import pentest_pb2

    status = task.get('status', 'PENDING')
    if isinstance(status, int):
        status = pentest_pb2.Status.Name(status)

    status_colors = {
        "PENDING": "yellow",
        "IN_PROGRESS": "blue",
        "COMPLETED": "green",
        "FAILED": "red"
    }
    status_color = status_colors.get(status, "white")

    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║              Custom Task Details             ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    console.print(f"Task ID: [cyan]{task.get('id', 'N/A')}[/cyan]")
    console.print(f"Status: [{status_color}]{status}[/{status_color}]")
    console.print(f"Target: [white]{task.get('target', 'N/A')}[/white]")
    console.print(f"Description: [white]{task.get('description', 'N/A')}[/white]")

    if task.get('created_at'):
        console.print(f"Created: [dim]{task.get('created_at')}[/dim]")
    if task.get('started_at'):
        console.print(f"Started: [dim]{task.get('started_at')}[/dim]")
    if task.get('finished_at'):
        console.print(f"Finished: [dim]{task.get('finished_at')}[/dim]")

    console.print(f"Requests: {task.get('request_count', 0)}")

    if task.get('findings'):
        console.print(f"Findings: {task.get('findings', 0)}")
    if task.get('severity'):
        severity = task.get('severity')
        if isinstance(severity, int):
            severity = pentest_pb2.Severity.Name(severity)
        console.print(f"Severity: {severity}")

    if task.get('summary'):
        console.print("\n[bold]Summary:[/bold]")
        console.print(Panel(
            Markdown(task.get('summary', '')),
            border_style="dim"
        ))

    console.print()


async def close_custom_task_async(task_id: str, grpc_address: str, credentials):
    """Close a custom task session."""
    grpc_client = None
    try:
        grpc_client = GRPCClient(grpc_address, credentials)
        await grpc_client.connect()

        response = await grpc_client.close_custom_task(task_id)

        if response.get('type') == 'error':
            console.print(f"[red]✗ Error:[/red] {response.get('error')}")
            return

        if response.get('type') == 'close_custom_task_response':
            console.print(f"[green]✓ Task closed:[/green] {task_id}")
            if response.get('message'):
                console.print(f"[dim]{response.get('message')}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")

    finally:
        if grpc_client:
            try:
                await grpc_client.close()
            except Exception:
                pass

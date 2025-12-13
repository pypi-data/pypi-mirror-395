"""Version command for ThreatWinds Pentest CLI."""

import sys
import platform

import click
from rich.console import Console
from rich.table import Table

from twpt_cli import __version__
from twpt_cli.config import load_credentials, get_api_endpoint, load_endpoint_config, API_PORT, GRPC_PORT, IS_KALI_LINUX
from twpt_cli.sdk import HTTPClient

console = Console()


@click.command()
@click.option(
    '--detailed',
    is_flag=True,
    help='Show detailed version information'
)
def version(detailed: bool):
    """Display version information for CLI and agent.

    Shows the version of:
    - ThreatWinds Pentest CLI
    - Pentest Agent (if connected)
    - System information (with --detailed)
    """
    # Basic version info
    console.print(f"\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print(f"║       ThreatWinds Pentest Version Info        ║", style="cyan")
    console.print(f"╚══════════════════════════════════════════════╝\n", style="cyan")

    # Create version table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Component", style="white")
    table.add_column("Version", style="green")
    table.add_column("Status", style="yellow")

    # CLI version
    table.add_row(
        "ThreatWinds Pentest CLI",
        __version__,
        "✓ Installed"
    )

    # Agent version (if connected)
    agent_version = get_agent_version()
    if agent_version:
        table.add_row(
            "Pentest Agent",
            agent_version,
            "✓ Connected"
        )
    else:
        endpoint_config = load_endpoint_config()
        if endpoint_config and endpoint_config.get("use_remote"):
            table.add_row(
                "Pentest Agent",
                "Unknown",
                "⚠ Not reachable"
            )
        elif IS_KALI_LINUX:
            table.add_row(
                "Pentest Agent",
                "Local",
                "⚠ Check if running"
            )
        else:
            table.add_row(
                "Pentest Agent",
                "Not configured",
                "✗ Use 'init' to connect"
            )

    console.print(table)

    # Detailed information if requested
    if detailed:
        console.print("\n═══════════════════════════════════════════════", style="dim")
        console.print("System Information:", style="cyan bold")
        console.print(f"  Platform: {platform.system()} {platform.release()}")
        console.print(f"  Architecture: {platform.machine()}")
        console.print(f"  Python: {platform.python_version()}")
        console.print(f"  Kali Linux: {'Yes' if IS_KALI_LINUX else 'No'}")

        # Configuration info
        console.print(f"\nConfiguration:", style="cyan bold")
        creds = load_credentials()
        if creds:
            console.print(f"  Configured: ✓ Yes")
            console.print(f"  Config Path: ~/.twpt/config.json")
        else:
            console.print(f"  Configured: ✗ No")

        # Endpoint configuration
        endpoint_config = load_endpoint_config()
        console.print(f"\nServer Configuration:", style="cyan bold")
        if endpoint_config and endpoint_config.get("use_remote"):
            console.print(f"  Mode: Remote Server")
            console.print(f"  API Endpoint: {endpoint_config['api_host']}:{endpoint_config['api_port']}")
            console.print(f"  gRPC Endpoint: {endpoint_config['grpc_host']}:{endpoint_config['grpc_port']}")
        elif IS_KALI_LINUX:
            console.print(f"  Mode: Local Agent")
            console.print(f"  API Port: {API_PORT}")
            console.print(f"  gRPC Port: {GRPC_PORT}")
        else:
            console.print(f"  Mode: Not configured")
            console.print(f"  Run 'twpt-cli init --host <server-ip>' to connect")

    # Check for updates hint
    console.print("\n" + "─"*50, style="dim")
    console.print("To update:", style="dim")
    console.print("  twpt-cli update", style="white")


def get_agent_version() -> str:
    """Get the version of the connected agent.

    Returns:
        Version string if agent is reachable, None otherwise
    """
    try:
        creds = load_credentials()
        if not creds:
            return None

        client = HTTPClient(get_api_endpoint(), creds)
        version = client.get_current_version()
        client.close()
        return version

    except:
        return None
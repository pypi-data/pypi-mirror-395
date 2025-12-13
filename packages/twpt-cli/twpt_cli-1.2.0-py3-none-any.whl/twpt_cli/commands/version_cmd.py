"""Version command for ThreatWinds Pentest CLI."""

import sys
import platform

import click
from rich.console import Console
from rich.table import Table

from twpt_cli import __version__
from twpt_cli.config import load_credentials, get_api_endpoint, load_endpoint_config, DOCKER_IMAGE, API_PORT, GRPC_PORT
from twpt_cli.sdk import HTTPClient
from twpt_cli.docker import container_exists, is_container_running, get_docker_client

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
    - Pentest Agent (if running)
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

    # Agent version (if container is running)
    agent_version = get_agent_version()
    if agent_version:
        table.add_row(
            "Pentest Agent",
            agent_version,
            "✓ Running"
        )
    elif container_exists():
        table.add_row(
            "Pentest Agent",
            "Unknown",
            "⚠ Container exists but not running"
        )
    else:
        table.add_row(
            "Pentest Agent",
            "Not installed",
            "✗ Container not found"
        )

    # Docker image info
    docker_image_info = get_docker_image_info()
    if docker_image_info:
        table.add_row(
            "Docker Image",
            docker_image_info['tag'],
            f"ID: {docker_image_info['id'][:12]}"
        )

    console.print(table)

    # Detailed information if requested
    if detailed:
        console.print("\n═══════════════════════════════════════════════", style="dim")
        console.print("System Information:", style="cyan bold")
        console.print(f"  Platform: {platform.system()} {platform.release()}")
        console.print(f"  Architecture: {platform.machine()}")
        console.print(f"  Python: {platform.python_version()}")

        # Docker information
        docker_info = get_docker_info()
        if docker_info:
            console.print(f"\nDocker Information:", style="cyan bold")
            console.print(f"  Version: {docker_info['version']}")
            console.print(f"  API Version: {docker_info['api_version']}")

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
        console.print(f"\nEndpoint Configuration:", style="cyan bold")
        if endpoint_config and endpoint_config.get("use_remote"):
            console.print(f"  Mode: Remote")
            console.print(f"  API Endpoint: {endpoint_config['api_host']}:{endpoint_config['api_port']}")
            console.print(f"  gRPC Endpoint: {endpoint_config['grpc_host']}:{endpoint_config['grpc_port']}")
        else:
            console.print(f"  Mode: Local (Docker)")
            console.print(f"  API Port: {API_PORT}")
            console.print(f"  gRPC Port: {GRPC_PORT}")

        console.print(f"\nDocker Settings:", style="cyan bold")
        console.print(f"  Image: {DOCKER_IMAGE}")

    # Check for updates hint
    console.print("\n" + "─"*50, style="dim")
    console.print("To update to the latest version:", style="dim")
    console.print("  CLI:   pip install --upgrade twpt-cli", style="white")
    console.print("  Agent: twpt-cli update-latest", style="white")


def get_agent_version() -> str:
    """Get the version of the running agent.

    Returns:
        Version string if agent is running, None otherwise
    """
    if not is_container_running():
        return None

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


def get_docker_image_info() -> dict:
    """Get Docker image information.

    Returns:
        Dictionary with image info, None if not found
    """
    try:
        client = get_docker_client()
        image = client.images.get(DOCKER_IMAGE)

        # Extract tag
        tags = image.tags
        tag = tags[0].split(':')[-1] if tags else "unknown"

        return {
            'id': image.short_id.replace('sha256:', ''),
            'tag': tag,
            'size': format_size(image.attrs.get('Size', 0)),
        }
    except:
        return None


def get_docker_info() -> dict:
    """Get Docker daemon information.

    Returns:
        Dictionary with Docker info, None if not available
    """
    try:
        client = get_docker_client()
        version_info = client.version()

        return {
            'version': version_info.get('Version', 'Unknown'),
            'api_version': version_info.get('ApiVersion', 'Unknown'),
        }
    except:
        return None


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
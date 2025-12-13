"""Install ThreatWinds Web UI/Frontend command."""

import sys
import click
from rich.console import Console

console = Console()


def _check_docker_available():
    """Check if Docker is available for frontend installation."""
    try:
        from twpt_cli.docker.frontend import is_frontend_running
        return True
    except ImportError:
        return False


@click.command()
@click.option(
    '--port',
    default='80',
    help='Port to expose frontend on (default: 80)'
)
@click.option(
    '--reinstall',
    is_flag=True,
    help='Reinstall frontend even if already installed'
)
def install_frontend(port: str, reinstall: bool):
    """Install and start the ThreatWinds Web UI/Frontend.

    The frontend provides a web-based interface for managing pentests.
    It runs as a Docker container and connects to your configured agent
    (local or remote).

    Note: This command requires Docker to be installed.

    By default, the frontend is accessible at http://localhost

    Examples:
        twpt-cli install-frontend                 # Install on port 80
        twpt-cli install-frontend --port 8080     # Install on port 8080
        twpt-cli install-frontend --reinstall     # Reinstall if already exists
    """
    console.print("\n╔════════════════════════════════════════════╗", style="cyan")
    console.print("║   ThreatWinds Frontend Installation        ║", style="cyan")
    console.print("╚════════════════════════════════════════════╝\n", style="cyan")

    # Check if Docker module is available
    if not _check_docker_available():
        console.print("✗ Docker is required for frontend installation", style="red")
        console.print("\nPlease install Docker first:", style="yellow")
        console.print("  https://docs.docker.com/get-docker/", style="dim")
        sys.exit(1)

    # Import Docker functions
    from twpt_cli.docker.frontend import (
        setup_frontend_container,
        is_frontend_running,
        stop_frontend_container,
        remove_frontend_container,
    )

    # Check if frontend is already running
    if is_frontend_running() and not reinstall:
        console.print("✓ Frontend is already running", style="green")
        frontend_url = f"http://localhost:{port}" if port != "80" else "http://localhost"
        console.print(f"  Access it at: {frontend_url}", style="cyan")
        console.print("\nUse --reinstall to reinstall", style="dim")
        return

    if is_frontend_running():
        console.print("Stopping existing frontend...", style="yellow")
        stop_frontend_container()
        remove_frontend_container()

    console.print("Installing ThreatWinds Web UI...\n", style="cyan")

    # Setup frontend container
    success = setup_frontend_container(port)

    if success:
        console.print("\n╔════════════════════════════════════════════╗", style="green")
        console.print("║     Frontend Installation Complete!        ║", style="green")
        console.print("╚════════════════════════════════════════════╝\n", style="green")

        frontend_url = f"http://localhost:{port}" if port != "80" else "http://localhost"
        console.print(f"✓ Frontend is running at: {frontend_url}", style="cyan bold")
        console.print("\nYou can now manage your pentests through the web interface!", style="white")
    else:
        console.print("\n✗ Frontend installation failed", style="red")
        console.print("Please check Docker is installed and running", style="yellow")
        sys.exit(1)

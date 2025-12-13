"""Update command for ThreatWinds Pentest CLI."""

import sys

import click
from rich.console import Console

from twpt_cli.docker import (
    stop_container,
    remove_container,
    pull_pentest_image,
    setup_container,
    is_container_running,
    container_exists,
)
from twpt_cli.config import load_endpoint_config

console = Console()


@click.command()
@click.option(
    '--force',
    is_flag=True,
    help='Force update even if container is running'
)
def update_latest(force: bool):
    """Update the pentest toolkit to the latest version.

    This command will:
    1. Stop the running container
    2. Remove the existing container
    3. Pull the latest Docker image
    4. Create and start a new container

    Note: This command only works with local Docker installations.
    Use --force to update even if the container is currently running.
    """
    # Check if using remote endpoint
    endpoint_config = load_endpoint_config()
    if endpoint_config and endpoint_config.get("use_remote"):
        console.print("\n✗ Update command only works with local Docker installations", style="red")
        console.print("You are currently configured to use a remote endpoint.", style="yellow")
        console.print("To update a remote server, please contact your administrator.", style="yellow")
        sys.exit(1)

    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║       ThreatWinds Pentest Toolkit Update      ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    # Check if container exists
    if not container_exists():
        console.print("✗ No container found to update", style="red")
        console.print("Please run: twpt-cli configure", style="yellow")
        sys.exit(1)

    # Check if container is running
    if is_container_running() and not force:
        console.print("⚠ Container is currently running", style="yellow")
        console.print("Use --force to update anyway, or stop the container first", style="yellow")
        response = console.input("Do you want to force update? [y/N]: ")
        if response.lower() != 'y':
            console.print("Update cancelled", style="yellow")
            sys.exit(0)

    # Step 1: Stop container
    console.print("Step 1: Stopping container...", style="blue")
    if not stop_container():
        if not force:
            console.print("✗ Failed to stop container", style="red")
            sys.exit(1)

    # Step 2: Remove container
    console.print("\nStep 2: Removing old container...", style="blue")
    if not remove_container():
        console.print("✗ Failed to remove container", style="red")
        sys.exit(1)

    # Step 3: Pull latest image
    console.print("\nStep 3: Pulling latest Docker image...", style="blue")
    if not pull_pentest_image(force=True):
        console.print("✗ Failed to pull latest image", style="red")
        sys.exit(1)

    # Step 4: Setup new container
    console.print("\nStep 4: Setting up new container...", style="blue")
    if not setup_container():
        console.print("✗ Failed to setup new container", style="red")
        sys.exit(1)

    # Success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Update complete!", style="green bold")
    console.print("="*50 + "\n", style="green")
    console.print("The pentest toolkit has been updated to the latest version.", style="cyan")
    console.print("Container is running with the new image.", style="cyan")
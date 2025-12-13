"""Uninstall command for ThreatWinds Pentest CLI."""

import sys
import shutil
from pathlib import Path

import click
from rich.console import Console

from twpt_cli.config import DEFAULT_PT_PATH, USER_CONFIG_PATH, clear_credentials

console = Console()


def _docker_available():
    """Check if Docker module is available and container exists."""
    try:
        from twpt_cli.docker import container_exists
        return container_exists()
    except Exception:
        return False


@click.command()
@click.option(
    '--remove-data',
    is_flag=True,
    help='Also remove configuration and data files'
)
@click.option(
    '--yes',
    is_flag=True,
    help='Skip confirmation prompt'
)
def uninstall(remove_data: bool, yes: bool):
    """Uninstall the ThreatWinds pentest toolkit.

    This command will:
    1. Stop and remove the Docker container (if exists)
    2. Optionally remove configuration and data files
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║     ThreatWinds Pentest Toolkit Uninstall     ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    docker_exists = _docker_available()

    if not docker_exists:
        console.print("No installation found to uninstall.", style="yellow")
        if remove_data:
            console.print("\nRemoving configuration and data files...", style="blue")
            remove_configuration_data()
        else:
            console.print("\nUse --remove-data to remove configuration files.", style="dim")
        return

    # Confirm uninstall
    if not yes:
        if docker_exists:
            console.print("⚠ This will remove the Docker container", style="yellow bold")
        if remove_data:
            console.print("⚠ This will also remove all configuration and data files", style="yellow bold")

        response = console.input("\nDo you want to continue? [y/N]: ")
        if response.lower() != 'y':
            console.print("Uninstall cancelled", style="yellow")
            sys.exit(0)

    step = 1

    # Handle Docker container
    if docker_exists:
        try:
            from twpt_cli.docker import (
                stop_container,
                remove_container,
                is_container_running,
            )
            console.print(f"\nStep {step}: Removing Docker container...", style="blue")

            if is_container_running():
                console.print("  Stopping container...", style="dim")
                if not stop_container():
                    console.print("  ⚠ Failed to stop container gracefully", style="yellow")

            if remove_container():
                console.print("  ✓ Docker container removed", style="green")
            else:
                console.print("  ⚠ Failed to remove container", style="yellow")
            step += 1
        except Exception as e:
            console.print(f"  ⚠ Error with Docker: {e}", style="yellow")

    # Remove data if requested
    if remove_data:
        console.print(f"\nStep {step}: Removing configuration and data...", style="blue")
        remove_configuration_data()

    # Success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Uninstall complete!", style="green bold")
    console.print("="*50 + "\n", style="green")

    console.print("The following items have been removed:", style="cyan")
    if docker_exists:
        console.print("  Docker container", style="white")
    if remove_data:
        console.print("  Configuration files", style="white")
        console.print("  Data directory", style="white")

    console.print("\nThe following items were NOT removed:", style="yellow")
    console.print("  twpt-cli command (use: pip uninstall twpt-cli)", style="white")
    if docker_exists:
        console.print("  Docker image (use: docker image rm ghcr.io/threatwinds/twpt-agent:latest)", style="white")


def remove_configuration_data():
    """Remove configuration and data files."""
    try:
        # Clear credentials
        clear_credentials()
        console.print("  ✓ Credentials removed", style="green")

        # Remove data directory (for Docker installations)
        data_dir = DEFAULT_PT_PATH / "data"
        if data_dir.exists():
            shutil.rmtree(data_dir)
            console.print("  ✓ Data directory removed", style="green")

        # Remove base path if empty (for service installations)
        if DEFAULT_PT_PATH.exists():
            try:
                if not any(DEFAULT_PT_PATH.iterdir()):
                    DEFAULT_PT_PATH.rmdir()
                    console.print(f"  ✓ Directory {DEFAULT_PT_PATH} removed", style="green")
            except OSError:
                pass  # Directory not empty

        # Remove user config directory if it exists and is empty
        if USER_CONFIG_PATH.exists() and USER_CONFIG_PATH != DEFAULT_PT_PATH:
            try:
                if not any(USER_CONFIG_PATH.iterdir()):
                    USER_CONFIG_PATH.rmdir()
                    console.print(f"  ✓ Config directory {USER_CONFIG_PATH} removed", style="green")
            except OSError:
                pass  # Directory not empty

    except Exception as e:
        console.print(f"  ⚠ Error removing data: {e}", style="yellow")
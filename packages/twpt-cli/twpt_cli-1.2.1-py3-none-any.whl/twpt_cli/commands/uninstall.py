"""Uninstall command for ThreatWinds Pentest CLI."""

import sys
import shutil
from pathlib import Path

import click
from rich.console import Console

from twpt_cli.config import USER_CONFIG_PATH, LOCAL_AGENT_DATA_PATH, clear_credentials, IS_KALI_LINUX

console = Console()


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
    """Uninstall the ThreatWinds Pentest CLI.

    This command will:
    1. Remove configuration files (~/.twpt/)
    2. Optionally remove local agent data (if on Kali Linux)

    Note: To fully uninstall, also run: pip uninstall twpt-cli
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║     ThreatWinds Pentest CLI Uninstall         ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    # Check what exists
    config_exists = USER_CONFIG_PATH.exists()
    agent_data_exists = LOCAL_AGENT_DATA_PATH.exists()

    if not config_exists and not agent_data_exists:
        console.print("No configuration or data found to remove.", style="yellow")
        console.print("\nTo uninstall the CLI tool:", style="dim")
        console.print("  pip uninstall twpt-cli", style="white")
        return

    # Confirm uninstall
    if not yes:
        console.print("This will remove:", style="yellow bold")
        if config_exists:
            console.print(f"  • Configuration directory: {USER_CONFIG_PATH}", style="white")
        if agent_data_exists and remove_data:
            console.print(f"  • Agent data directory: {LOCAL_AGENT_DATA_PATH}", style="white")

        response = console.input("\nDo you want to continue? [y/N]: ")
        if response.lower() != 'y':
            console.print("Uninstall cancelled", style="yellow")
            sys.exit(0)

    step = 1

    # Remove configuration
    if config_exists:
        console.print(f"\nStep {step}: Removing configuration...", style="blue")
        remove_configuration_data(remove_agent_data=remove_data)
        step += 1

    # Success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Uninstall complete!", style="green bold")
    console.print("="*50 + "\n", style="green")

    console.print("The CLI configuration has been removed.", style="cyan")
    console.print("\nTo fully uninstall, also run:", style="yellow")
    console.print("  pip uninstall twpt-cli", style="white")


def remove_configuration_data(remove_agent_data: bool = False):
    """Remove configuration and optionally agent data files."""
    try:
        # Clear credentials
        clear_credentials()
        console.print("  ✓ Credentials removed", style="green")

        # Remove agent data directory (only on Kali Linux with local agent)
        if remove_agent_data and LOCAL_AGENT_DATA_PATH.exists():
            shutil.rmtree(LOCAL_AGENT_DATA_PATH)
            console.print("  ✓ Agent data directory removed", style="green")

        # Remove user config directory if it exists and is empty
        if USER_CONFIG_PATH.exists():
            try:
                # Remove all files in config dir
                for item in USER_CONFIG_PATH.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)

                # Remove the directory itself
                USER_CONFIG_PATH.rmdir()
                console.print(f"  ✓ Config directory {USER_CONFIG_PATH} removed", style="green")
            except OSError as e:
                console.print(f"  ⚠ Could not fully remove config directory: {e}", style="yellow")

    except Exception as e:
        console.print(f"  ⚠ Error removing data: {e}", style="yellow")
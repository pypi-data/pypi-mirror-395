"""Update command for ThreatWinds Pentest CLI."""

import subprocess
import sys

import click
from rich.console import Console

from twpt_cli.config import load_endpoint_config, IS_KALI_LINUX

console = Console()


@click.command()
@click.option(
    '--force',
    is_flag=True,
    help='Force update even if already at latest version'
)
def update_latest(force: bool):
    """Update the ThreatWinds Pentest CLI to the latest version.

    This command updates the CLI tool itself via pip.
    For local agent updates on Kali Linux, use 'twpt-cli install --update'.
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║       ThreatWinds Pentest CLI Update          ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    # Update CLI via pip
    console.print("Updating ThreatWinds Pentest CLI...", style="blue")

    try:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "twpt-cli"]
        if force:
            cmd.append("--force-reinstall")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            console.print("✓ CLI updated successfully", style="green")
            if result.stdout:
                # Show relevant pip output
                for line in result.stdout.split('\n'):
                    if 'Successfully' in line or 'Requirement' in line:
                        console.print(f"  {line}", style="dim")
        else:
            console.print("✗ Failed to update CLI", style="red")
            if result.stderr:
                console.print(f"  {result.stderr}", style="dim")
            sys.exit(1)

    except Exception as e:
        console.print(f"✗ Update failed: {e}", style="red")
        sys.exit(1)

    # Check endpoint configuration
    endpoint_config = load_endpoint_config()

    # Success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Update complete!", style="green bold")
    console.print("="*50 + "\n", style="green")

    if endpoint_config and endpoint_config.get("use_remote"):
        console.print("You are using a remote agent server.", style="cyan")
        console.print("Contact your server administrator for agent updates.", style="dim")
    elif IS_KALI_LINUX:
        console.print("To update local agent on Kali Linux:", style="cyan")
        console.print("  twpt-cli install --update", style="white")
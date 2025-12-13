"""Configure command for ThreatWinds Pentest CLI."""

import sys

import click
from rich.console import Console

from twpt_cli.config import (
    save_credentials,
    validate_credentials,
    IS_KALI_LINUX,
)

console = Console()


@click.command()
@click.option(
    '--api-key', '--pentest-key',
    prompt='API/Pentest Key',
    hide_input=False,
    help='ThreatWinds API/Pentest Key'
)
@click.option(
    '--api-secret', '--pentest-secret',
    prompt='API/Pentest Secret',
    hide_input=True,
    help='ThreatWinds API/Pentest Secret'
)
@click.option(
    '--skip-validation',
    is_flag=True,
    help='Skip credential validation (for testing)'
)
def configure(api_key: str, api_secret: str, skip_validation: bool):
    """Configure ThreatWinds Pentest CLI with API credentials.

    This command will:
    1. Validate your API credentials with ThreatWinds servers
    2. Save credentials securely to ~/.twpt/config.json

    After configuring credentials, use 'twpt-cli init' to connect to a remote
    agent server, or on Kali Linux use 'twpt-cli install' for local agent setup.
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║     ThreatWinds Pentest CLI Configuration     ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    # Step 1: Validate credentials (unless skipped)
    if not skip_validation:
        console.print("Step 1: Validating API credentials...", style="blue")
        try:
            if validate_credentials(api_key, api_secret):
                console.print("✓ API credentials are valid", style="green")
            else:
                console.print("✗ Invalid API credentials", style="red")
                console.print(
                    "Please check your API key and secret at: https://threatwinds.com/account",
                    style="yellow"
                )
                console.print(
                    "Or use --skip-validation to bypass validation for testing",
                    style="yellow"
                )
                sys.exit(1)
        except Exception as e:
            console.print(f"✗ Failed to validate credentials: {e}", style="red")
            sys.exit(1)
    else:
        console.print("Step 1: Skipping credential validation (testing mode)", style="yellow")

    # Step 2: Save credentials
    console.print("\nStep 2: Saving credentials...", style="blue")
    try:
        save_credentials(api_key, api_secret)
        console.print("✓ Credentials saved to ~/.twpt/config.json", style="green")
    except Exception as e:
        console.print(f"✗ Failed to save credentials: {e}", style="red")
        sys.exit(1)

    # Final success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Credentials configured!", style="green bold")
    console.print("="*50 + "\n", style="green")

    # Show next steps based on platform
    console.print("Next steps:", style="cyan")
    console.print("  1. Connect to a remote agent server:", style="white")
    console.print("     twpt-cli init --host <server-ip> --api-port 9741", style="dim")

    if IS_KALI_LINUX:
        console.print("\n  2. Or install local agent (Kali Linux only):", style="white")
        console.print("     twpt-cli install", style="dim")

    console.print("\nAfter setup, you can use:", style="cyan")
    console.print("  • twpt-cli run example.com", style="white")
    console.print("  • twpt-cli get <pentest-id>", style="white")
    console.print("  • twpt-cli download <pentest-id>", style="white")
    console.print("\nFor help: twpt-cli --help\n", style="dim")
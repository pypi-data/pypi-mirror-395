"""Configure command for ThreatWinds Pentest CLI."""

import platform
import sys

import click
from rich.console import Console

from twpt_cli.config import (
    save_credentials,
    validate_credentials,
    check_configured,
)
from twpt_cli.docker import (
    install_docker_if_needed,
    pull_pentest_image,
    setup_container,
    stop_and_remove_existing,
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
    '--skip-docker',
    is_flag=True,
    help='Skip Docker setup (not recommended)'
)
@click.option(
    '--skip-validation',
    is_flag=True,
    help='Skip credential validation (for testing)'
)
def configure(api_key: str, api_secret: str, skip_docker: bool, skip_validation: bool):
    """Configure ThreatWinds Pentest CLI with API credentials and Docker setup.

    This command will:
    1. Validate your API credentials with ThreatWinds servers
    2. Save credentials securely to ~/.twpt/config.json
    3. Install Docker if needed (Linux only)
    4. Pull the pentest Docker image
    5. Set up and start the pentest container
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

    # Step 3: Docker setup (Linux only)
    if not skip_docker:
        if platform.system() == "Linux":
            console.print("\nStep 3: Setting up Docker environment...", style="blue")

            # Install Docker if needed
            if not install_docker_if_needed():
                console.print(
                    "\n⚠ Docker installation failed or was cancelled.",
                    style="yellow"
                )
                console.print(
                    "You can manually install Docker and run 'twpt-cli configure' again.",
                    style="yellow"
                )
                console.print(
                    "Or use --skip-docker flag to skip Docker setup.",
                    style="yellow"
                )
                sys.exit(1)

            # Pull Docker image
            console.print("\nStep 4: Pulling pentest Docker image...", style="blue")
            if not pull_pentest_image():
                console.print("✗ Failed to pull Docker image", style="red")
                sys.exit(1)

            # Stop and remove existing container if any
            console.print("\nStep 5: Setting up pentest container...", style="blue")
            if not stop_and_remove_existing():
                console.print("✗ Failed to clean up existing container", style="red")
                sys.exit(1)

            # Create and start new container
            if not setup_container():
                console.print("✗ Failed to setup container", style="red")
                sys.exit(1)

        else:
            console.print(
                f"\n⚠ Docker setup is only supported on Linux. Current platform: {platform.system()}",
                style="yellow"
            )
            console.print(
                "Please install Docker manually and ensure the container is running.",
                style="yellow"
            )
            console.print(
                "Docker Desktop: https://docs.docker.com/get-docker/",
                style="yellow"
            )
    else:
        console.print("\n⚠ Skipping Docker setup as requested", style="yellow")
        console.print(
            "Make sure Docker is installed and the pentest container is running.",
            style="yellow"
        )

    # Final success message
    console.print("\n" + "="*50, style="green")
    console.print("✓ Configuration complete!", style="green bold")
    console.print("="*50 + "\n", style="green")

    console.print("You can now use the following commands:", style="cyan")
    console.print("  • twpt-cli run example.com", style="white")
    console.print("  • twpt-cli get <pentest-id>", style="white")
    console.print("  • twpt-cli download <pentest-id>", style="white")
    console.print("\nFor help: twpt-cli --help\n", style="dim")
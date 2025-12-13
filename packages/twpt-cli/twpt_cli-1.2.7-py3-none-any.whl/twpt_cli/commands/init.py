"""Init command for configuring remote endpoints."""

import sys

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from twpt_cli.config import (
    save_endpoint_config,
    load_endpoint_config,
    clear_endpoint_config,
    test_endpoint,
    get_api_endpoint,
    get_grpc_endpoint,
    save_credentials,
    load_credentials,
    IS_KALI_LINUX,
)

console = Console()


@click.command()
@click.option(
    '--host',
    prompt='Remote host/IP address',
    help='Remote host IP address or hostname'
)
@click.option(
    '--api-port',
    prompt='API port',
    default='9741',
    help='API service port (default: 9741)'
)
@click.option(
    '--grpc-port',
    prompt='gRPC port',
    default='9742',
    help='gRPC service port (default: 9742)'
)
@click.option(
    '--api-key', '--pentest-key',
    help='API/Pentest key (will prompt if not provided)'
)
@click.option(
    '--api-secret', '--pentest-secret',
    help='API/Pentest secret (will prompt if not provided)'
)
@click.option(
    '--skip-test',
    is_flag=True,
    help='Skip connection testing'
)
@click.option(
    '--local',
    is_flag=True,
    help='Reset to local agent configuration (Kali Linux only)'
)
def init(host: str, api_port: str, grpc_port: str, api_key: str, api_secret: str, skip_test: bool, local: bool):
    """Initialize connection to a remote agent server.

    This command configures the CLI to connect to a remote ThreatWinds
    pentest agent server.

    Examples:
        # Configure remote endpoint
        twpt-cli init --host 15.235.4.158 --api-port 9741

        # Reset to local agent (Kali Linux only)
        twpt-cli init --local
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║     ThreatWinds Agent Server Connection       ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    # Handle local reset
    if local:
        if not IS_KALI_LINUX:
            console.print("✗ Local agent mode is only available on Kali Linux", style="red")
            console.print("\nOn other platforms, you must connect to a remote agent server:", style="yellow")
            console.print("  twpt-cli init --host <server-ip> --api-port 9741", style="dim")
            sys.exit(1)

        console.print("Resetting to local agent configuration...", style="blue")
        clear_endpoint_config()
        console.print("✓ Configuration reset to use local agent (localhost)", style="green")

        # Show current configuration
        display_current_config()
        return

    # Validate inputs
    try:
        port_num = int(api_port)
        if port_num < 1 or port_num > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as e:
        console.print(f"✗ Invalid API port: {e}", style="red")
        sys.exit(1)

    try:
        grpc_port_num = int(grpc_port)
        if grpc_port_num < 1 or grpc_port_num > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as e:
        console.print(f"✗ Invalid gRPC port: {e}", style="red")
        sys.exit(1)

    # Test connection if not skipped
    if not skip_test:
        console.print(f"\nTesting connection to {host}:{api_port}...", style="blue")

        if test_endpoint(host, api_port):
            console.print(f"✓ Successfully connected to API endpoint", style="green")
        else:
            console.print(f"⚠ Could not connect to {host}:{api_port}", style="yellow")
            console.print("  The endpoint might be unreachable or the service is not running", style="dim")

            response = console.input("\nDo you want to save this configuration anyway? [y/N]: ")
            if response.lower() != 'y':
                console.print("Configuration cancelled", style="yellow")
                sys.exit(0)

        # Also test gRPC if different port
        if grpc_port != api_port:
            console.print(f"\nTesting gRPC connection to {host}:{grpc_port}...", style="blue")

            if test_endpoint(host, grpc_port):
                console.print(f"✓ Successfully connected to gRPC endpoint", style="green")
            else:
                console.print(f"⚠ Could not connect to gRPC endpoint", style="yellow")

    # Save endpoint configuration
    console.print("\nSaving endpoint configuration...", style="blue")
    try:
        save_endpoint_config(
            api_host=host,
            api_port=api_port,
            grpc_host=host,  # Use same host for both
            grpc_port=grpc_port
        )
        console.print("✓ Endpoint configuration saved", style="green")
    except Exception as e:
        console.print(f"✗ Failed to save configuration: {e}", style="red")
        sys.exit(1)

    # Handle API credentials
    existing_creds = load_credentials()

    # Only prompt for credentials if explicitly provided via flags OR if no credentials exist
    if api_key or api_secret:
        # User explicitly provided credentials, so configure them
        console.print("\n" + "="*50, style="cyan")
        console.print("API Credentials Configuration", style="cyan bold")
        console.print("="*50 + "\n", style="cyan")

        # Prompt for missing credential if one was provided
        if not api_key:
            api_key = console.input("Enter API/Pentest Key: ")
        if not api_secret:
            from rich.prompt import Prompt
            api_secret = Prompt.ask("Enter API/Pentest Secret", password=True, console=console)

        # Save credentials
        try:
            save_credentials(api_key, api_secret)
            console.print("✓ API credentials saved", style="green")
        except Exception as e:
            console.print(f"✗ Failed to save credentials: {e}", style="red")
            console.print("You can configure them later with: twpt-cli configure --skip-docker", style="yellow")
    elif not existing_creds:
        # No credentials exist and none provided - prompt user
        console.print("\n" + "="*50, style="cyan")
        console.print("API Credentials Configuration", style="cyan bold")
        console.print("="*50 + "\n", style="cyan")
        console.print("[yellow]No API credentials found. Please configure them now.[/yellow]\n")

        # Prompt for credentials
        api_key = console.input("Enter API/Pentest Key: ")
        from rich.prompt import Prompt
        api_secret = Prompt.ask("Enter API/Pentest Secret", password=True, console=console)

        # Save credentials
        try:
            save_credentials(api_key, api_secret)
            console.print("✓ API credentials saved", style="green")
        except Exception as e:
            console.print(f"✗ Failed to save credentials: {e}", style="red")
            console.print("You can configure them later with: twpt-cli configure --skip-docker", style="yellow")
    else:
        # Credentials already exist and none provided - use existing
        console.print("\n✓ Using existing API credentials", style="green")
        console.print("[dim]Use 'twpt-cli configure' to update credentials[/dim]")

    # Display summary
    console.print("\n" + "="*50, style="green")
    console.print("✓ Configuration complete!", style="green bold")
    console.print("="*50 + "\n", style="green")

    display_current_config()

    # Check if credentials are now configured
    final_creds = load_credentials()

    if not final_creds:
        console.print("\nNext steps:", style="cyan")
        console.print("  1. Configure API credentials: twpt-cli configure --skip-docker", style="white")
        console.print("  2. Start using the service: twpt-cli", style="white")
    else:
        console.print("\nYou're all set! Start using the CLI:", style="cyan")
        console.print("  twpt-cli", style="white")
        console.print("  twpt-cli run --target example.com", style="white")
        console.print("  twpt-cli list", style="white")

    console.print("\nTo switch back to local:", style="dim")
    console.print("  twpt-cli init --local", style="white")


def display_current_config():
    """Display the current endpoint configuration."""
    endpoint_config = load_endpoint_config()
    creds = load_credentials()

    # Create configuration table
    table = Table(title="Current Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Setting", style="white")
    table.add_column("Value", style="green")

    # Show credentials status
    if creds:
        table.add_row("API Credentials", "✓ Configured")
    else:
        table.add_row("API Credentials", "✗ Not configured")

    if endpoint_config and endpoint_config.get("use_remote"):
        table.add_row("Mode", "Remote Server")
        table.add_row("API Endpoint", f"{endpoint_config['api_host']}:{endpoint_config['api_port']}")
        table.add_row("gRPC Endpoint", f"{endpoint_config['grpc_host']}:{endpoint_config['grpc_port']}")
        table.add_row("Full API URL", get_api_endpoint())
        table.add_row("Full gRPC Address", get_grpc_endpoint())
    else:
        mode_label = "Local Agent" if IS_KALI_LINUX else "Local (not configured)"
        table.add_row("Mode", mode_label)
        table.add_row("API Endpoint", f"localhost:{get_api_endpoint().split(':')[-1]}")
        table.add_row("gRPC Endpoint", f"localhost:{get_grpc_endpoint().split(':')[-1]}")
        table.add_row("Full API URL", get_api_endpoint())
        table.add_row("Full gRPC Address", get_grpc_endpoint())

    console.print(table)
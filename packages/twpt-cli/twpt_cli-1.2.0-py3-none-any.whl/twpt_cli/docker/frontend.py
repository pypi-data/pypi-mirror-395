"""Frontend container management for ThreatWinds Pentest CLI."""

import platform
import subprocess
from typing import Optional

import docker
from docker.errors import DockerException, NotFound, APIError
from rich.console import Console

from twpt_cli.config import load_endpoint_config

console = Console()

FRONTEND_IMAGE = "ghcr.io/threatwinds/twpt-frontend:latest"
FRONTEND_CONTAINER_NAME = "twpt-frontend"


def get_agent_url() -> str:
    """Get the agent URL for the frontend to connect to.

    Returns:
        Agent URL string
    """
    endpoint_config = load_endpoint_config()

    if endpoint_config and endpoint_config.get("use_remote"):
        # Remote mode
        host = endpoint_config.get("api_host", "localhost")
        port = endpoint_config.get("api_port", "9741")
        return f"http://{host}:{port}"
    else:
        # Local mode - need to get Docker host IP
        system = platform.system().lower()
        if system == "linux":
            # On Linux, try to get docker0 bridge IP
            try:
                result = subprocess.run(
                    ["sh", "-c", "ip -4 addr show docker0 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    return f"http://{result.stdout.strip()}:9741"
            except:
                pass
            # Fallback to common docker bridge IP
            return "http://172.17.0.1:9741"
        else:
            # macOS and Windows support host.docker.internal
            return "http://host.docker.internal:9741"


def get_docker_host_ip() -> str:
    """Get the Docker host IP for the current platform.

    Returns:
        Docker host IP string
    """
    system = platform.system().lower()
    if system == "linux":
        try:
            result = subprocess.run(
                ["sh", "-c", "ip -4 addr show docker0 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        return "172.17.0.1"
    else:
        return "host.docker.internal"


def pull_frontend_image() -> bool:
    """Pull the frontend Docker image.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = docker.from_env()

        # Check if image already exists
        try:
            client.images.get(FRONTEND_IMAGE)
            console.print(f"✓ Frontend image already exists", style="green")
            return True
        except NotFound:
            pass

        console.print(f"Pulling frontend image {FRONTEND_IMAGE}...")
        console.print("This may take a few minutes...", style="dim")

        client.images.pull(FRONTEND_IMAGE)
        console.print(f"✓ Successfully pulled frontend image", style="green")
        return True

    except APIError as e:
        console.print(f"✗ Failed to pull frontend image: {e}", style="red")
        return False
    except DockerException as e:
        console.print(f"✗ Docker error: {e}", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        return False


def frontend_container_exists() -> bool:
    """Check if frontend container exists.

    Returns:
        True if container exists, False otherwise
    """
    try:
        client = docker.from_env()
        try:
            client.containers.get(FRONTEND_CONTAINER_NAME)
            return True
        except NotFound:
            return False
    except:
        return False


def is_frontend_running() -> bool:
    """Check if frontend container is running.

    Returns:
        True if running, False otherwise
    """
    try:
        client = docker.from_env()
        try:
            container = client.containers.get(FRONTEND_CONTAINER_NAME)
            return container.status == "running"
        except NotFound:
            return False
    except:
        return False


def stop_frontend_container() -> bool:
    """Stop the frontend container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = docker.from_env()
        try:
            container = client.containers.get(FRONTEND_CONTAINER_NAME)
            console.print("Stopping frontend container...")
            container.stop()
            console.print("✓ Frontend container stopped", style="green")
            return True
        except NotFound:
            console.print("Frontend container not found", style="yellow")
            return False
    except Exception as e:
        console.print(f"✗ Failed to stop frontend container: {e}", style="red")
        return False


def remove_frontend_container() -> bool:
    """Remove the frontend container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = docker.from_env()
        try:
            container = client.containers.get(FRONTEND_CONTAINER_NAME)
            console.print("Removing frontend container...")
            container.remove(force=True)
            console.print("✓ Frontend container removed", style="green")
            return True
        except NotFound:
            return True  # Already removed
    except Exception as e:
        console.print(f"✗ Failed to remove frontend container: {e}", style="red")
        return False


def setup_frontend_container(port: str = "80") -> bool:
    """Setup and start the frontend container.

    Args:
        port: Port to expose frontend on (default: 80)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Pull image first
        if not pull_frontend_image():
            return False

        client = docker.from_env()

        # Stop and remove existing container if it exists
        if frontend_container_exists():
            stop_frontend_container()
            remove_frontend_container()

        # Get agent URL
        agent_url = get_agent_url()
        console.print(f"Configuring frontend to connect to: {agent_url}", style="dim")

        # Setup container configuration
        container_config = {
            "name": FRONTEND_CONTAINER_NAME,
            "image": FRONTEND_IMAGE,
            "detach": True,
            "ports": {f"80/tcp": int(port)},
            "environment": {
                "VITE_API_BASE": agent_url,
            },
            "restart_policy": {"Name": "unless-stopped"},
        }

        # Add extra host mapping for Linux
        if platform.system().lower() == "linux":
            container_config["extra_hosts"] = {"host.docker.internal": "host-gateway"}

        console.print(f"Starting frontend container on port {port}...")
        container = client.containers.run(**container_config)

        console.print(f"✓ Frontend container started successfully", style="green")

        # Display access URL
        frontend_url = f"http://localhost:{port}" if port != "80" else "http://localhost"
        console.print(f"\n Frontend is accessible at: {frontend_url}", style="cyan bold")

        return True

    except APIError as e:
        console.print(f"✗ Failed to create frontend container: {e}", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        return False

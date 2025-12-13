"""Docker container management for ThreatWinds Pentest CLI."""

import sys
from typing import Optional, Dict, Any

import docker
from docker.models.containers import Container
from docker.errors import DockerException, NotFound, APIError
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from twpt_cli.config.constants import (
    DOCKER_IMAGE,
    CONTAINER_NAME,
    CONTAINER_CONFIG,
    DEFAULT_PT_PATH,
)

console = Console()


def get_docker_client() -> docker.DockerClient:
    """Get Docker client instance.

    Returns:
        Docker client

    Raises:
        DockerException: If unable to connect to Docker
    """
    try:
        client = docker.from_env()
        # Test connection
        client.ping()
        return client
    except DockerException as e:
        raise DockerException(f"Unable to connect to Docker: {e}")


def pull_pentest_image(force: bool = False) -> bool:
    """Pull the pentest Docker image.

    Args:
        force: Force pull even if image exists

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()

        # Check if image already exists
        if not force:
            try:
                client.images.get(DOCKER_IMAGE)
                console.print(f"✓ Image {DOCKER_IMAGE} already exists", style="green")
                return True
            except NotFound:
                pass

        console.print(f"Pulling Docker image {DOCKER_IMAGE}...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Pulling image...", total=None)

            # Pull the image
            image = client.images.pull(DOCKER_IMAGE)
            progress.update(task, completed=True)

        console.print(f"✓ Successfully pulled {DOCKER_IMAGE}", style="green")
        return True

    except APIError as e:
        console.print(f"✗ Failed to pull image: {e}", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Unexpected error pulling image: {e}", style="red")
        return False


def setup_container() -> bool:
    """Create and start the pentest container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()

        # Ensure data directory exists
        data_dir = DEFAULT_PT_PATH / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        console.print(f"Creating container {CONTAINER_NAME}...")

        # Create and start container
        container = client.containers.run(
            **CONTAINER_CONFIG
        )

        console.print(f"✓ Container {CONTAINER_NAME} created and started", style="green")
        return True

    except APIError as e:
        if "Conflict" in str(e):
            console.print(f"Container {CONTAINER_NAME} already exists", style="yellow")
            return start_container()
        console.print(f"✗ Failed to create container: {e}", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Unexpected error creating container: {e}", style="red")
        return False


def stop_container() -> bool:
    """Stop the pentest container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)

        console.print(f"Stopping container {CONTAINER_NAME}...")
        container.stop(timeout=10)
        console.print(f"✓ Container {CONTAINER_NAME} stopped", style="green")
        return True

    except NotFound:
        console.print(f"Container {CONTAINER_NAME} not found", style="yellow")
        return True
    except Exception as e:
        console.print(f"✗ Failed to stop container: {e}", style="red")
        return False


def remove_container() -> bool:
    """Remove the pentest container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)

        console.print(f"Removing container {CONTAINER_NAME}...")
        container.remove(force=True)
        console.print(f"✓ Container {CONTAINER_NAME} removed", style="green")
        return True

    except NotFound:
        console.print(f"Container {CONTAINER_NAME} not found", style="yellow")
        return True
    except Exception as e:
        console.print(f"✗ Failed to remove container: {e}", style="red")
        return False


def start_container() -> bool:
    """Start the pentest container if it exists.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)

        if container.status == "running":
            console.print(f"Container {CONTAINER_NAME} is already running", style="yellow")
            return True

        console.print(f"Starting container {CONTAINER_NAME}...")
        container.start()
        console.print(f"✓ Container {CONTAINER_NAME} started", style="green")
        return True

    except NotFound:
        console.print(f"Container {CONTAINER_NAME} not found", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Failed to start container: {e}", style="red")
        return False


def is_container_running() -> bool:
    """Check if the pentest container is running.

    Returns:
        True if running, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)
        return container.status == "running"
    except:
        return False


def container_exists() -> bool:
    """Check if the pentest container exists.

    Returns:
        True if exists, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)
        return True
    except NotFound:
        return False
    except:
        return False


def stop_and_remove_existing() -> bool:
    """Stop and remove existing container if it exists.

    Returns:
        True if successful, False otherwise
    """
    if container_exists():
        console.print(f"Found existing container {CONTAINER_NAME}", style="yellow")
        if is_container_running():
            if not stop_container():
                return False
        if not remove_container():
            return False
    return True


def get_container_logs(lines: int = 100) -> Optional[str]:
    """Get logs from the pentest container.

    Args:
        lines: Number of log lines to retrieve

    Returns:
        Log output as string, or None if container not found
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)
        logs = container.logs(tail=lines, stream=False)
        return logs.decode('utf-8') if isinstance(logs, bytes) else str(logs)
    except NotFound:
        return None
    except Exception as e:
        console.print(f"✗ Failed to get container logs: {e}", style="red")
        return None


def restart_container() -> bool:
    """Restart the pentest container.

    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_docker_client()
        container = client.containers.get(CONTAINER_NAME)

        console.print(f"Restarting container {CONTAINER_NAME}...")
        container.restart(timeout=10)
        console.print(f"✓ Container {CONTAINER_NAME} restarted", style="green")
        return True

    except NotFound:
        console.print(f"Container {CONTAINER_NAME} not found", style="red")
        return False
    except Exception as e:
        console.print(f"✗ Failed to restart container: {e}", style="red")
        return False
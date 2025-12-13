"""Docker management for ThreatWinds Pentest CLI."""

from .container import (
    get_docker_client,
    pull_pentest_image,
    setup_container,
    stop_container,
    remove_container,
    start_container,
    is_container_running,
    container_exists,
    stop_and_remove_existing,
    get_container_logs,
)

from .docker_install import (
    install_docker_if_needed,
    is_docker_installed,
    detect_linux_distro,
)

from .frontend import (
    setup_frontend_container,
    pull_frontend_image,
    frontend_container_exists,
    is_frontend_running,
    stop_frontend_container,
    remove_frontend_container,
)

__all__ = [
    # Docker client
    "get_docker_client",
    # Container management
    "pull_pentest_image",
    "setup_container",
    "stop_container",
    "remove_container",
    "start_container",
    "is_container_running",
    "container_exists",
    "stop_and_remove_existing",
    "get_container_logs",
    # Docker installation
    "install_docker_if_needed",
    "is_docker_installed",
    "detect_linux_distro",
    # Frontend management
    "setup_frontend_container",
    "pull_frontend_image",
    "frontend_container_exists",
    "is_frontend_running",
    "stop_frontend_container",
    "remove_frontend_container",
]
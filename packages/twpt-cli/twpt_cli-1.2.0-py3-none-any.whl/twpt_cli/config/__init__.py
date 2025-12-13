"""Configuration management for ThreatWinds Pentest CLI."""

from .constants import (
    DEFAULT_PT_PATH,
    USER_CONFIG_PATH,
    CONFIG_FILE_NAME,
    ENDPOINT_FILE_NAME,
    AUTH_API_URL,
    DOCKER_IMAGE,
    CONTAINER_NAME,
    API_PORT,
    GRPC_PORT,
    DOWNLOAD_TIMEOUT,
    # Agent/Service constants
    AGENT_DOWNLOAD_URL,
    AGENT_DIR_NAME,
    SERVICE_NAME,
    SERVICE_DISPLAY_NAME,
    SERVICE_DESCRIPTION,
)

from .credentials import (
    save_credentials,
    load_credentials,
    validate_credentials,
    check_configured,
    clear_credentials,
    # Endpoint functions
    save_endpoint_config,
    load_endpoint_config,
    get_api_endpoint,
    get_grpc_endpoint,
    clear_endpoint_config,
    test_endpoint,
)

__all__ = [
    # Constants
    "DEFAULT_PT_PATH",
    "USER_CONFIG_PATH",
    "CONFIG_FILE_NAME",
    "ENDPOINT_FILE_NAME",
    "AUTH_API_URL",
    "DOCKER_IMAGE",
    "CONTAINER_NAME",
    "API_PORT",
    "GRPC_PORT",
    "DOWNLOAD_TIMEOUT",
    # Agent/Service constants
    "AGENT_DOWNLOAD_URL",
    "AGENT_DIR_NAME",
    "SERVICE_NAME",
    "SERVICE_DISPLAY_NAME",
    "SERVICE_DESCRIPTION",
    # Credential Functions
    "save_credentials",
    "load_credentials",
    "validate_credentials",
    "check_configured",
    "clear_credentials",
    # Endpoint Functions
    "save_endpoint_config",
    "load_endpoint_config",
    "get_api_endpoint",
    "get_grpc_endpoint",
    "clear_endpoint_config",
    "test_endpoint",
]
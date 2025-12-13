"""Credential management for ThreatWinds Pentest CLI."""

import json
import base64
import os
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from requests.exceptions import RequestException

from twpt_cli.sdk.models import Credentials
from .constants import (
    USER_CONFIG_PATH,
    CONFIG_FILE_NAME,
    ENDPOINT_FILE_NAME,
    AUTH_API_URL,
    DEFAULT_API_HOST,
    DEFAULT_GRPC_HOST,
    API_PORT,
    GRPC_PORT,
)


def get_config_path() -> Path:
    """Get the configuration file path.

    Returns:
        Path to the configuration file
    """
    config_dir = USER_CONFIG_PATH
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / CONFIG_FILE_NAME


def save_credentials(api_key: str, api_secret: str) -> None:
    """Save API credentials to configuration file.

    Args:
        api_key: ThreatWinds API key
        api_secret: ThreatWinds API secret

    Raises:
        IOError: If unable to save credentials
    """
    config_path = get_config_path()

    # Create credentials object
    creds = Credentials(api_key=api_key, api_secret=api_secret)

    # Convert to JSON and encode in base64 (matching Go implementation)
    creds_dict = {
        "APIKey": creds.api_key,
        "APISecret": creds.api_secret
    }
    creds_json = json.dumps(creds_dict)
    creds_b64 = base64.b64encode(creds_json.encode()).decode()

    # Save to file with restricted permissions
    try:
        with open(config_path, 'w') as f:
            f.write(creds_b64)

        # Set file permissions to 0600 (owner read/write only)
        os.chmod(config_path, 0o600)

    except Exception as e:
        raise IOError(f"Failed to save credentials: {e}")


def load_credentials() -> Optional[Credentials]:
    """Load API credentials from configuration file.

    Returns:
        Credentials object if found, None otherwise

    Raises:
        IOError: If unable to read credentials
        ValueError: If credentials are invalid
    """
    config_path = get_config_path()

    if not config_path.exists():
        return None

    try:
        with open(config_path, 'r') as f:
            creds_b64 = f.read().strip()

        # Decode from base64
        creds_json = base64.b64decode(creds_b64).decode()
        creds_dict = json.loads(creds_json)

        # Create credentials object
        return Credentials(
            api_key=creds_dict.get("APIKey", ""),
            api_secret=creds_dict.get("APISecret", "")
        )

    except Exception as e:
        raise ValueError(f"Failed to load credentials: {e}")


def validate_credentials(api_key: str, api_secret: str) -> bool:
    """Validate API credentials with ThreatWinds servers.

    Args:
        api_key: ThreatWinds API key
        api_secret: ThreatWinds API secret

    Returns:
        True if credentials are valid, False otherwise

    Raises:
        RequestException: If unable to contact auth server
    """
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "api-secret": api_secret,
    }

    try:
        response = requests.get(
            AUTH_API_URL,
            headers=headers,
            timeout=30
        )

        # Check if credentials are valid
        if response.status_code == 200:
            return True
        elif response.status_code in [401, 403]:
            return False
        else:
            # Unexpected status code
            response.raise_for_status()
            return False

    except requests.exceptions.Timeout:
        raise RequestException("Authentication server timeout")
    except requests.exceptions.ConnectionError:
        raise RequestException("Unable to connect to authentication server")
    except Exception as e:
        raise RequestException(f"Authentication failed: {e}")


def check_configured() -> bool:
    """Check if the CLI is configured with credentials.

    Returns:
        True if configured, False otherwise
    """
    try:
        creds = load_credentials()
        return creds is not None and creds.api_key and creds.api_secret
    except:
        return False


def clear_credentials() -> None:
    """Clear saved credentials.

    This removes the configuration file.
    """
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()


def get_endpoint_config_path() -> Path:
    """Get the endpoint configuration file path.

    Returns:
        Path to the endpoint configuration file
    """
    config_dir = USER_CONFIG_PATH
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / ENDPOINT_FILE_NAME


def save_endpoint_config(api_host: str, api_port: str, grpc_host: Optional[str] = None, grpc_port: Optional[str] = None) -> None:
    """Save endpoint configuration.

    Args:
        api_host: API host/IP address
        api_port: API port
        grpc_host: gRPC host/IP (defaults to api_host)
        grpc_port: gRPC port (defaults to 9742)

    Raises:
        IOError: If unable to save configuration
    """
    config_path = get_endpoint_config_path()

    # Use same host for gRPC if not specified
    if not grpc_host:
        grpc_host = api_host
    if not grpc_port:
        grpc_port = "9742"

    endpoint_config = {
        "api_host": api_host,
        "api_port": api_port,
        "grpc_host": grpc_host,
        "grpc_port": grpc_port,
        "use_remote": True
    }

    try:
        with open(config_path, 'w') as f:
            json.dump(endpoint_config, f, indent=2)

        # Set file permissions to 0600
        os.chmod(config_path, 0o600)

    except Exception as e:
        raise IOError(f"Failed to save endpoint configuration: {e}")


def load_endpoint_config() -> Optional[Dict[str, Any]]:
    """Load endpoint configuration.

    Returns:
        Dictionary with endpoint config if found, None otherwise
    """
    config_path = get_endpoint_config_path()

    if not config_path.exists():
        return None

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None


def get_api_endpoint() -> str:
    """Get the API endpoint URL.

    Returns:
        API endpoint URL (either remote or local)
    """
    # Check for endpoint configuration
    endpoint_config = load_endpoint_config()

    if endpoint_config and endpoint_config.get("use_remote"):
        host = endpoint_config.get("api_host", DEFAULT_API_HOST)
        port = endpoint_config.get("api_port", API_PORT)
    else:
        # Use environment variables or defaults
        host = os.getenv("PT_API_HOST", DEFAULT_API_HOST)
        port = os.getenv("PT_API_PORT", API_PORT)

    return f"http://{host}:{port}"


def get_grpc_endpoint() -> str:
    """Get the gRPC endpoint address.

    Returns:
        gRPC endpoint address (either remote or local)
    """
    # Check for endpoint configuration
    endpoint_config = load_endpoint_config()

    if endpoint_config and endpoint_config.get("use_remote"):
        host = endpoint_config.get("grpc_host", endpoint_config.get("api_host", DEFAULT_GRPC_HOST))
        port = endpoint_config.get("grpc_port", GRPC_PORT)
    else:
        # Use environment variables or defaults
        host = os.getenv("PT_GRPC_HOST", DEFAULT_GRPC_HOST)
        port = os.getenv("PT_GRPC_PORT", GRPC_PORT)

    return f"{host}:{port}"


def clear_endpoint_config() -> None:
    """Clear endpoint configuration to use local defaults."""
    config_path = get_endpoint_config_path()
    if config_path.exists():
        config_path.unlink()


def test_endpoint(host: str, port: str) -> bool:
    """Test if an endpoint is reachable.

    Args:
        host: Host/IP address
        port: Port number

    Returns:
        True if endpoint is reachable, False otherwise
    """
    import socket

    try:
        # Try to connect to the endpoint
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout
        result = sock.connect_ex((host, int(port)))
        sock.close()
        return result == 0
    except:
        return False
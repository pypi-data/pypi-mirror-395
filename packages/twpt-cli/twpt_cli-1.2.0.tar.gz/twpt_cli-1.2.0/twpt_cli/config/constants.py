"""Constants for ThreatWinds Pentest CLI."""

import os
import platform
from pathlib import Path

# Paths - platform-specific for service installation
if platform.system() == "Windows":
    DEFAULT_PT_PATH = Path(os.getenv("PROGRAMDATA", "C:\\ProgramData")) / "twpt"
else:
    DEFAULT_PT_PATH = Path("/opt/twpt")

# User config path (credentials, etc.)
USER_CONFIG_PATH = Path.home() / ".twpt"
CONFIG_FILE_NAME = "config.json"
ENDPOINT_FILE_NAME = "endpoint.json"

# API URLs
AUTH_API_URL = "https://inference.threatwinds.com/api/auth/v2/keypair"

# Agent configuration
AGENT_DOWNLOAD_URL = "https://storage.googleapis.com/twpt/agent/latest/twpt-agent.zip"
AGENT_DIR_NAME = "agent"
SERVICE_NAME = "TWAgent"
SERVICE_DISPLAY_NAME = "ThreatWinds Pentest Agent"
SERVICE_DESCRIPTION = "ThreatWinds Pentest Agent Service - Runs penetration testing operations"

# Docker configuration
DOCKER_IMAGE = "ghcr.io/threatwinds/twpt-agent:latest"
CONTAINER_NAME = "twpt-agent"

# Default endpoints (can be overridden by environment variables or config)
DEFAULT_API_HOST = "localhost"
DEFAULT_GRPC_HOST = "localhost"
API_PORT = os.getenv("PT_API_PORT", "9741")
GRPC_PORT = os.getenv("PT_GRPC_PORT", "9742")

# Container configuration
CONTAINER_CONFIG = {
    "name": CONTAINER_NAME,
    "image": DOCKER_IMAGE,
    "network_mode": "host",  # Full host network access for pentesting
    "privileged": True,  # Required for pentesting operations
    "volumes": {
        str(DEFAULT_PT_PATH / "data"): {
            "bind": "/app/data",
            "mode": "rw"
        }
    },
    "environment": {
        "API_PORT": API_PORT,
        "GRPC_PORT": GRPC_PORT,
    },
    "restart_policy": {
        "Name": "always",
        "MaximumRetryCount": 0
    },
    "detach": True,
}

# Timeout configurations
DOWNLOAD_TIMEOUT = 300  # 5 minutes for evidence download
REQUEST_TIMEOUT = 30  # 30 seconds for regular API requests
STREAM_TIMEOUT = 3600  # 1 hour for streaming operations
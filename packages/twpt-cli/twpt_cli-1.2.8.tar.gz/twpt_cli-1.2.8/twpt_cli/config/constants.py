"""Constants for ThreatWinds Pentest CLI."""

import os
import platform
from pathlib import Path

# Detect if running on Kali Linux
def is_kali_linux() -> bool:
    """Check if the current system is Kali Linux."""
    if platform.system() != "Linux":
        return False
    try:
        import distro
        return distro.id().lower() == "kali"
    except ImportError:
        # Fallback: check /etc/os-release
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                return "kali" in content
        except:
            return False

IS_KALI_LINUX = is_kali_linux()

# User config path (credentials, etc.) - always in user's home directory
# This ensures no sudo is required for config operations
USER_CONFIG_PATH = Path.home() / ".twpt"
CONFIG_FILE_NAME = "config.json"
ENDPOINT_FILE_NAME = "endpoint.json"

# API URLs
AUTH_API_URL = "https://inference.threatwinds.com/api/auth/v2/keypair"

# Agent configuration (for local install on Kali Linux only)
AGENT_DOWNLOAD_URL = "https://storage.googleapis.com/twpt/agent/latest/twpt-agent.zip"
AGENT_DIR_NAME = "agent"
SERVICE_NAME = "TWAgent"
SERVICE_DISPLAY_NAME = "ThreatWinds Pentest Agent"
SERVICE_DESCRIPTION = "ThreatWinds Pentest Agent Service - Runs penetration testing operations"

# Local agent data path (only used on Kali Linux for local install)
# Uses user's home directory to avoid permission issues
LOCAL_AGENT_DATA_PATH = USER_CONFIG_PATH / "agent-data"

# Default endpoints (can be overridden by environment variables or config)
DEFAULT_API_HOST = "localhost"
DEFAULT_GRPC_HOST = "localhost"
API_PORT = os.getenv("PT_API_PORT", "9741")
GRPC_PORT = os.getenv("PT_GRPC_PORT", "9742")

# Timeout configurations
DOWNLOAD_TIMEOUT = 300  # 5 minutes for evidence download
REQUEST_TIMEOUT = 30  # 30 seconds for regular API requests
STREAM_TIMEOUT = 3600  # 1 hour for streaming operations
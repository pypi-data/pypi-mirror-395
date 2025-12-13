"""ThreatWinds Pentest Client SDK - Python implementation."""

from .models import (
    HTTPPentestData,
    HTTPTargetData,
    HTTPSchedulePentestRequest,
    HTTPTargetRequest,
    HTTPPentestListResponse,
    Credentials,
    # Enums
    HTTPScope,
    HTTPType,
    HTTPStyle,
    HTTPStatus,
    HTTPPhase,
    HTTPSeverity,
)

from .http_client import HTTPClient
from .grpc_client import GRPCClient

__all__ = [
    # Models
    "HTTPPentestData",
    "HTTPTargetData",
    "HTTPSchedulePentestRequest",
    "HTTPTargetRequest",
    "HTTPPentestListResponse",
    "Credentials",
    # Enums
    "HTTPScope",
    "HTTPType",
    "HTTPStyle",
    "HTTPStatus",
    "HTTPPhase",
    "HTTPSeverity",
    # Clients
    "HTTPClient",
    "GRPCClient",
]
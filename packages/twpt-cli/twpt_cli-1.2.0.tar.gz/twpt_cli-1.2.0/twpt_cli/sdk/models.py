"""Data models and enums for ThreatWinds Pentest SDK."""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# HTTP String-based Enums
class HTTPScope(str, Enum):
    """Target scope enumeration."""
    HOLISTIC = "HOLISTIC"
    TARGETED = "TARGETED"


class HTTPType(str, Enum):
    """Pentest type enumeration."""
    BLACK_BOX = "BLACK_BOX"
    WHITE_BOX = "WHITE_BOX"


class HTTPStyle(str, Enum):
    """Pentest style enumeration."""
    AGGRESSIVE = "AGGRESSIVE"
    SAFE = "SAFE"


class HTTPStatus(str, Enum):
    """Pentest status enumeration."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class HTTPPhase(str, Enum):
    """Pentest phase enumeration."""
    PENDING = "PENDING"
    RECON = "RECON"
    INITIAL_EXPLOIT = "INITIAL_EXPLOIT"
    DEEP_EXPLOIT = "DEEP_EXPLOIT"
    LATERAL_MOVEMENT = "LATERAL_MOVEMENT"
    REPORT = "REPORT"
    FINISHED = "FINISHED"
    GUIDED = "GUIDED"


class HTTPMode(str, Enum):
    """Pentest mode enumeration."""
    AUTONOMOUS = "AUTONOMOUS"  # Fully automated
    GUIDED = "GUIDED"          # User-driven, interactive


class HTTPSeverity(str, Enum):
    """Finding severity enumeration."""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# gRPC Integer-based Enums (for protobuf compatibility)
class GRPCStatus(int, Enum):
    """gRPC status enumeration."""
    STATUS_UNSPECIFIED = 0
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4


class GRPCPhase(int, Enum):
    """gRPC phase enumeration."""
    PHASE_UNSPECIFIED = 0
    RECON = 1
    INITIAL_EXPLOIT = 2
    DEEP_EXPLOIT = 3
    LATERAL_MOVEMENT = 4
    REPORT = 5
    FINISHED = 6
    GUIDED = 7


class GRPCMode(int, Enum):
    """gRPC mode enumeration."""
    MODE_UNSPECIFIED = 0
    MODE_AUTONOMOUS = 1  # Fully automated
    MODE_GUIDED = 2      # User-driven, interactive


class GRPCScope(int, Enum):
    """gRPC scope enumeration."""
    SCOPE_UNSPECIFIED = 0
    HOLISTIC = 1
    TARGETED = 2


class GRPCType(int, Enum):
    """gRPC type enumeration."""
    TYPE_UNSPECIFIED = 0
    BLACK_BOX = 1
    WHITE_BOX = 2


class GRPCStyle(int, Enum):
    """gRPC style enumeration."""
    STYLE_UNSPECIFIED = 0
    AGGRESSIVE = 1
    SAFE = 2


class GRPCSeverity(int, Enum):
    """gRPC severity enumeration."""
    SEVERITY_UNSPECIFIED = 0
    NONE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class UpdateType(int, Enum):
    """Update type for streaming messages."""
    UPDATE_TYPE_UNSPECIFIED = 0
    INFO = 1
    ERROR = 2
    STATUS = 3
    DEBUG = 4


# Data Models
class Credentials(BaseModel):
    """API credentials for authentication."""
    api_key: str = Field(..., alias="APIKey")
    api_secret: str = Field(..., alias="APISecret")

    class Config:
        populate_by_name = True


class HTTPTargetRequest(BaseModel):
    """HTTP target request for scheduling pentests."""
    target: str = Field(...)
    scope: HTTPScope = Field(HTTPScope.TARGETED)
    type: HTTPType = Field(HTTPType.BLACK_BOX)
    credentials: Optional[Dict[str, Any]] = Field(None)

    class Config:
        use_enum_values = True


class HTTPSchedulePentestRequest(BaseModel):
    """HTTP request for scheduling a pentest."""
    style: HTTPStyle = Field(HTTPStyle.AGGRESSIVE)  # Default: AGGRESSIVE
    exploit: bool = Field(True)  # Default: Exploit enabled
    targets: List[HTTPTargetRequest] = Field(...)

    # Custom plan support
    custom_plan_content: Optional[str] = Field(None)
    plan_metadata: Optional[Dict[str, Any]] = Field(None)
    is_custom_plan: bool = Field(False)

    # Memory/context support
    memory_items: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Memory items to include in pentest (list of {name, content} dicts)"
    )

    class Config:
        use_enum_values = True


class HTTPTargetData(BaseModel):
    """HTTP target data in pentest results."""
    target: str
    scope: HTTPScope
    type: HTTPType
    status: HTTPStatus
    phase: Optional[str] = None  # Use str instead of enum to handle unknown values
    severity: HTTPSeverity = HTTPSeverity.NONE
    findings: int = 0

    class Config:
        populate_by_name = True
        use_enum_values = True


class HTTPPentestData(BaseModel):
    """HTTP pentest data structure."""
    id: str
    status: HTTPStatus
    style: HTTPStyle
    exploit: bool
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    severity: HTTPSeverity = HTTPSeverity.NONE
    findings: int = 0
    targets: List[HTTPTargetData] = Field(default_factory=list)
    mode: Optional[HTTPMode] = None  # AUTONOMOUS or GUIDED
    description: Optional[str] = None  # For guided pentests
    summary: Optional[str] = None  # Task summary for guided pentests

    # Custom plan tracking
    custom_plan_name: Optional[str] = None
    custom_plan_version: Optional[str] = None
    is_custom_plan: Optional[bool] = None

    class Config:
        populate_by_name = True
        use_enum_values = True


class HTTPPentestListResponse(BaseModel):
    """HTTP response for paginated pentest list."""
    total: int
    page: int
    page_size: int
    total_pages: int
    pentests: List[HTTPPentestData] = Field(default_factory=list)

    class Config:
        populate_by_name = True


# gRPC/Protobuf Models
class TargetRequest(BaseModel):
    """gRPC target request for scheduling pentests."""
    target: str
    scope: GRPCScope = GRPCScope.TARGETED
    type: GRPCType = GRPCType.BLACK_BOX
    credentials: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True


class SchedulePentestRequest(BaseModel):
    """gRPC request for scheduling a pentest."""
    style: GRPCStyle = GRPCStyle.AGGRESSIVE
    exploit: bool = True
    targets: List[TargetRequest]

    class Config:
        use_enum_values = True


class TargetData(BaseModel):
    """gRPC target data in pentest results."""
    target: str
    scope: GRPCScope
    type: GRPCType
    status: GRPCStatus
    phase: GRPCPhase
    severity: GRPCSeverity
    findings: int = 0

    class Config:
        use_enum_values = True


class PentestData(BaseModel):
    """gRPC pentest data structure."""
    id: str
    status: GRPCStatus
    style: GRPCStyle
    exploit: bool
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    severity: GRPCSeverity = GRPCSeverity.NONE
    findings: int = 0
    targets: List[TargetData] = Field(default_factory=list)

    class Config:
        use_enum_values = True


class StatusUpdate(BaseModel):
    """Status update message for streaming."""
    type: UpdateType
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        use_enum_values = True


class ScheduleResponse(BaseModel):
    """Response for pentest scheduling."""
    pentest_id: str
    message: str


class ErrorResponse(BaseModel):
    """Error response structure."""
    code: int
    message: str


# Helper functions to convert between HTTP and gRPC formats
def convert_http_to_grpc_request(http_req: HTTPSchedulePentestRequest) -> SchedulePentestRequest:
    """Convert HTTP request to gRPC format."""
    # Map string enum to int enum
    style_map = {
        HTTPStyle.AGGRESSIVE: GRPCStyle.AGGRESSIVE,
        HTTPStyle.SAFE: GRPCStyle.SAFE,
    }

    scope_map = {
        HTTPScope.HOLISTIC: GRPCScope.HOLISTIC,
        HTTPScope.TARGETED: GRPCScope.TARGETED,
    }

    type_map = {
        HTTPType.BLACK_BOX: GRPCType.BLACK_BOX,
        HTTPType.WHITE_BOX: GRPCType.WHITE_BOX,
    }

    grpc_targets = []
    for target in http_req.targets:
        grpc_targets.append(TargetRequest(
            target=target.target,
            scope=scope_map.get(target.scope, GRPCScope.SCOPE_UNSPECIFIED),
            type=type_map.get(target.type, GRPCType.TYPE_UNSPECIFIED),
            credentials=target.credentials
        ))

    return SchedulePentestRequest(
        style=style_map.get(http_req.style, GRPCStyle.STYLE_UNSPECIFIED),
        exploit=http_req.exploit,
        targets=grpc_targets
    )
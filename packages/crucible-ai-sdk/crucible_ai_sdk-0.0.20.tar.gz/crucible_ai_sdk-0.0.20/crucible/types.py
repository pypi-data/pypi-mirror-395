"""
Type definitions for Crucible SDK.
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class LogRequest:
    """Request data for logging to Crucible."""
    
    # Request metadata
    requested_at: int  # Unix timestamp in milliseconds
    received_at: int   # Unix timestamp in milliseconds
    
    # Request/Response data
    req_payload: Dict[str, Any]
    resp_payload: Optional[Dict[str, Any]] = None
    
    # Status information
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    
    # User metadata (from crucible_metadata parameter)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # System tags
    tags: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)
    model: Optional[str] = None
    completion_id: Optional[str] = None
    
    # SDK information
    sdk_version: str = "0.1.0"
    sdk_name: str = "python"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "requestedAt": self.requested_at,
            "receivedAt": self.received_at,
            "reqPayload": self.req_payload,
            "respPayload": self.resp_payload,
            "statusCode": self.status_code,
            "errorMessage": self.error_message,
            "metadata": self.metadata,
            "tags": self.tags,
            "model": self.model,
            "completionId": self.completion_id,
            "sdkVersion": self.sdk_version,
            "sdkName": self.sdk_name,
        }
    
    @classmethod
    def from_openai_call(
        cls,
        request_data: Dict[str, Any],
        response_data: Optional[Dict[str, Any]] = None,
        requested_at: Optional[int] = None,
        received_at: Optional[int] = None,
        status_code: Optional[int] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> "LogRequest":
        """Create LogRequest from OpenAI API call data."""
        
        now = int(time.time() * 1000)
        
        return cls(
            requested_at=requested_at or now,
            received_at=received_at or now,
            req_payload=request_data,
            resp_payload=response_data,
            status_code=status_code,
            error_message=error_message,
            metadata=metadata or {},
            tags=tags or {},
            model=request_data.get("model"),
            completion_id=response_data.get("id") if response_data else None,
        )
    
    @classmethod
    def from_genai_call(
        cls,
        request_data: Dict[str, Any],
        response_data: Optional[Dict[str, Any]] = None,
        requested_at: Optional[int] = None,
        received_at: Optional[int] = None,
        status_code: Optional[int] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, Union[str, int, float, bool]]] = None,
    ) -> "LogRequest":
        """Create LogRequest from GenAI API call data."""
        
        now = int(time.time() * 1000)
        
        # Extract model name from request
        model = request_data.get("model")
        
        # Extract completion ID from response (GenAI uses "id" field)
        completion_id = None
        if response_data:
            completion_id = response_data.get("id")
            if not completion_id and response_data.get("candidates"):
                # Try to get ID from first candidate if available
                first_candidate = response_data["candidates"][0] if response_data["candidates"] else {}
                completion_id = first_candidate.get("id")
        
        return cls(
            requested_at=requested_at or now,
            received_at=received_at or now,
            req_payload=request_data,
            resp_payload=response_data,
            status_code=status_code,
            error_message=error_message,
            metadata=metadata or {},
            tags=tags or {},
            model=model,
            completion_id=completion_id,
        )


@dataclass
class LogResponse:
    """Response from Crucible logging API."""
    
    id: str
    status: str  # "success", "error", "queued"
    message: Optional[str] = None
    status_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "message": self.message,
            "status_url": self.status_url
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogResponse":
        """Create LogResponse from API response."""
        return cls(
            id=data.get("id", "unknown"),
            status=data.get("status", "unknown"),
            message=data.get("message"),
            status_url=data.get("status_url")
        )


@dataclass
class Filter:
    """Filter for updating tags."""
    
    field: str
    equals: Union[str, int, float, bool]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "field": self.field,
            "equals": self.equals,
        }


@dataclass
class UpdateTagsRequest:
    """Request for updating tags."""
    
    filters: List[Filter]
    tags: Dict[str, Union[str, int, float, bool]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "filters": [f.to_dict() for f in self.filters],
            "tags": self.tags,
        }


@dataclass
class UpdateTagsResponse:
    """Response from tag update API."""
    
    success: bool
    matched_logs: int
    message: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateTagsResponse":
        """Create UpdateTagsResponse from API response."""
        return cls(
            success=data.get("success", False),
            matched_logs=data.get("matchedLogs", 0),
            message=data.get("message"),
        )


@dataclass
class BatchLogRequest:
    """Batch of log requests for efficient processing."""
    
    requests: List[LogRequest]
    batch_id: Optional[str] = None
    created_at: Optional[int] = None
    
    def __post_init__(self):
        """Set default values after initialization."""
        if self.created_at is None:
            self.created_at = int(time.time() * 1000)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "requests": [req.to_dict() for req in self.requests],
            "batchId": self.batch_id,
            "createdAt": self.created_at,
        }
    
    def add_request(self, request: LogRequest) -> None:
        """Add a request to the batch."""
        self.requests.append(request)
    
    def is_full(self, max_size: int) -> bool:
        """Check if batch is full."""
        return len(self.requests) >= max_size
    
    def is_empty(self) -> bool:
        """Check if batch is empty."""
        return len(self.requests) == 0
    
    def clear(self) -> None:
        """Clear all requests from the batch."""
        self.requests.clear()


# Type aliases for convenience
TagsDict = Dict[str, Union[str, int, float, bool]]
RequestData = Dict[str, Any]
ResponseData = Optional[Dict[str, Any]]

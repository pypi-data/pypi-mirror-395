"""
Data models for the Endpoint Reporter.

This module defines the core data structures used to represent
API endpoints, parameters, MCP tools, and complete API reports.
"""
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class ParameterInfo:
    """Information about an endpoint parameter."""
    
    name: str
    param_type: str  # "query", "path", "body", "header"
    python_type: str
    required: bool
    default: Any = None
    description: Optional[str] = None
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class EndpointInfo:
    """Information about a REST API endpoint."""
    
    path: str
    method: str
    operation_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    parameters: List[ParameterInfo] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    responses: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    deprecated: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['parameters'] = [p.to_dict() for p in self.parameters]
        return data


@dataclass
class MCPToolInfo:
    """Information about an MCP tool."""
    
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)
    mapped_endpoint: Optional[str] = None  # REST endpoint path
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class APIReport:
    """Complete API documentation report."""
    
    server_name: str
    server_version: str
    endpoints: List[EndpointInfo] = field(default_factory=list)
    mcp_tools: List[MCPToolInfo] = field(default_factory=list)
    openapi_spec: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "server_name": self.server_name,
            "server_version": self.server_version,
            "endpoints": [e.to_dict() for e in self.endpoints],
            "mcp_tools": [t.to_dict() for t in self.mcp_tools],
            "openapi_spec": self.openapi_spec,
            "generated_at": self.generated_at
        }

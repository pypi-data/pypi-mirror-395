"""
FastAPI Report - Universal FastAPI Documentation Generator

Automatically discover and document FastAPI endpoints and MCP tools.
"""
from .models import ParameterInfo, EndpointInfo, MCPToolInfo, APIReport
from .reporter import EndpointReporter

__version__ = "1.0.0"
__all__ = [
    "ParameterInfo",
    "EndpointInfo", 
    "MCPToolInfo",
    "APIReport",
    "EndpointReporter",
]

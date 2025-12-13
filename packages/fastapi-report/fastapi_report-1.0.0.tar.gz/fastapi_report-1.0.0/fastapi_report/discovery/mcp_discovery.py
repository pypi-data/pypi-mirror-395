"""
MCP tool discovery component.

Extracts MCP tool information from FastAPI-MCP applications.
"""
from typing import Any, Dict, List, Optional
import requests
from fastapi_report.models import MCPToolInfo


class MCPDiscovery:
    """Discovers and extracts MCP tool information from FastAPI-MCP applications."""
    
    def __init__(self, mcp_instance: Any = None, base_url: Optional[str] = None):
        """
        Initialize discovery with an MCP instance or base URL.
        
        Args:
            mcp_instance: FastAPI-MCP instance to analyze (for module mode)
            base_url: Base URL of running server (for URL mode)
        """
        self.mcp = mcp_instance
        self.base_url = base_url
        self.session_id = None
    
    def discover_tools(self) -> List[MCPToolInfo]:
        """
        Extract all MCP tools from FastAPI-MCP wrapper or remote server.
        
        Returns:
            List of MCPToolInfo objects representing all discovered tools
        """
        # If base_url is provided, use protocol-based discovery
        if self.base_url:
            return self.discover_tools_from_url()
        
        # Otherwise, use module-based discovery
        tools = []
        
        if self.mcp is None:
            return tools
        
        # Try to get tools from MCP instance
        try:
            # FastAPI-MCP stores tools in the 'tools' attribute as a list
            if hasattr(self.mcp, 'tools') and isinstance(self.mcp.tools, list):
                for tool in self.mcp.tools:
                    tool_info = self._extract_tool_info(tool)
                    tools.append(tool_info)
                            
        except Exception as e:
            # If MCP discovery fails, return what we have
            print(f"Warning: MCP tool discovery encountered error: {e}")
        
        return tools
    
    def discover_tools_from_url(self) -> List[MCPToolInfo]:
        """
        Discover MCP tools from running server using MCP protocol.
        
        Returns:
            List of MCPToolInfo objects discovered via protocol
        """
        tools = []
        
        try:
            # Step 1: Initialize MCP session
            session_id = self.initialize_mcp_session()
            if not session_id:
                print("Warning: Could not establish MCP session")
                return tools
            
            # Step 2: List tools using the session
            tools = self.list_tools_via_protocol(session_id)
            
        except Exception as e:
            print(f"Warning: MCP protocol discovery failed: {e}")
        
        return tools
    
    def initialize_mcp_session(self) -> Optional[str]:
        """
        Initialize MCP session and return session ID.
        
        Returns:
            Session ID from response headers, or None if failed
        """
        if not self.base_url:
            return None
        
        mcp_url = f"{self.base_url}/mcp"
        
        # Prepare initialize request
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "fastapi-report",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            response = requests.post(
                mcp_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=10
            )
            response.raise_for_status()
            
            # Extract session ID from response headers
            session_id = response.headers.get('Mcp-Session-Id')
            if session_id:
                self.session_id = session_id
                return session_id
            else:
                print("Warning: No Mcp-Session-Id in response headers")
                return None
                
        except requests.RequestException as e:
            print(f"Warning: MCP initialize request failed: {e}")
            return None
    
    def list_tools_via_protocol(self, session_id: str) -> List[MCPToolInfo]:
        """
        Call tools/list via MCP JSON-RPC protocol.
        
        Args:
            session_id: MCP session ID from initialize
            
        Returns:
            List of MCPToolInfo objects
        """
        if not self.base_url:
            return []
        
        mcp_url = f"{self.base_url}/mcp"
        
        # Prepare tools/list request
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {
                "cursor": None
            }
        }
        
        try:
            response = requests.post(
                mcp_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Mcp-Session-Id": session_id
                },
                timeout=10
            )
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Extract tools from result
            tools = []
            if 'result' in data and 'tools' in data['result']:
                for tool_data in data['result']['tools']:
                    tool_info = MCPToolInfo(
                        name=tool_data.get('name', ''),
                        description=tool_data.get('description'),
                        input_schema=tool_data.get('inputSchema', {}),
                        mapped_endpoint=None  # Cannot map without operation_map in URL mode
                    )
                    tools.append(tool_info)
            
            return tools
            
        except requests.RequestException as e:
            print(f"Warning: MCP tools/list request failed: {e}")
            return []
        except (KeyError, ValueError) as e:
            print(f"Warning: Failed to parse MCP tools/list response: {e}")
            return []
    
    def _extract_tool_info(self, tool: Any) -> MCPToolInfo:
        """
        Extract information from an MCP tool.
        
        Args:
            tool: MCP tool object
            
        Returns:
            MCPToolInfo object with extracted metadata
        """
        # Extract tool metadata
        if isinstance(tool, dict):
            name = tool.get('name', '')
            description = tool.get('description')
            input_schema = tool.get('inputSchema', {})
        else:
            # Tool is likely a Pydantic model or object with attributes
            name = getattr(tool, 'name', '')
            description = getattr(tool, 'description', None)
            # Try different attribute names for input schema
            input_schema = getattr(tool, 'inputSchema', None) or getattr(tool, 'input_schema', {})
        
        return MCPToolInfo(
            name=name,
            description=description,
            input_schema=input_schema if input_schema else {},
            mapped_endpoint=self.map_tool_to_endpoint(name)
        )
    
    def map_tool_to_endpoint(self, tool_name: str) -> Optional[str]:
        """
        Find the REST endpoint that corresponds to an MCP tool.
        
        Args:
            tool_name: Name of the MCP tool
            
        Returns:
            Endpoint path or None if no mapping found
        """
        # MCP tools in FastAPI-MCP typically map to operation IDs
        # The operation_map attribute contains the mapping
        
        if self.mcp is None:
            return None
        
        try:
            # Check for operation_map attribute (FastAPI-MCP)
            if hasattr(self.mcp, 'operation_map') and isinstance(self.mcp.operation_map, dict):
                operation_info = self.mcp.operation_map.get(tool_name)
                if operation_info and isinstance(operation_info, dict):
                    path = operation_info.get('path', '')
                    method = operation_info.get('method', 'get').upper()
                    return f"{method} {path}"
            
            # Fallback: try to find in FastAPI app routes by operation_id
            if hasattr(self.mcp, 'app') or hasattr(self.mcp, 'fastapi'):
                app = getattr(self.mcp, 'app', None) or getattr(self.mcp, 'fastapi', None)
                if app and hasattr(app, 'routes'):
                    for route in app.routes:
                        if hasattr(route, 'operation_id') and route.operation_id == tool_name:
                            if hasattr(route, 'path'):
                                # Get the HTTP method
                                methods = list(route.methods) if hasattr(route, 'methods') else []
                                method = methods[0] if methods else 'GET'
                                return f"{method} {route.path}"
            
            return None
        except Exception:
            return None
    
    def extract_tool_schema(self, tool: Any) -> Dict[str, Any]:
        """
        Extract input schema for MCP tool.
        
        Args:
            tool: MCP tool object
            
        Returns:
            Input schema dictionary
        """
        if isinstance(tool, dict):
            return tool.get('inputSchema', {})
        else:
            return getattr(tool, 'inputSchema', {})

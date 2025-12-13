"""
Property-based tests for MCP discovery.

Feature: endpoint-reporter, Property 6, 7, 42, 43: MCP Tool Discovery
Validates: Requirements 2.1, 2.2, 2.6, 2.7
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi_report.discovery.mcp_discovery import MCPDiscovery
from fastapi_report.models import MCPToolInfo


def test_discover_tools_from_mcp_instance():
    """
    Feature: endpoint-reporter, Property 6: MCP Tool Discovery Completeness
    For any FastAPI-MCP application, discovering tools should identify all registered tools.
    """
    # Create mock MCP instance
    mock_mcp = Mock()
    
    # Create mock tools with proper attribute access
    tool1 = Mock()
    tool1.name = "test_tool_1"
    tool1.description = "Test tool 1"
    tool1.inputSchema = {"type": "object", "properties": {"param1": {"type": "string"}}}
    
    tool2 = Mock()
    tool2.name = "test_tool_2"
    tool2.description = "Test tool 2"
    tool2.inputSchema = {"type": "object", "properties": {"param2": {"type": "integer"}}}
    
    mock_mcp.tools = [tool1, tool2]
    mock_mcp.operation_map = {}
    
    discovery = MCPDiscovery(mcp_instance=mock_mcp)
    tools = discovery.discover_tools()
    
    assert len(tools) == 2
    assert tools[0].name == "test_tool_1"
    assert tools[0].description == "Test tool 1"
    assert tools[1].name == "test_tool_2"
    assert tools[1].description == "Test tool 2"


def test_discover_tools_with_dict_format():
    """
    Feature: endpoint-reporter, Property 7: MCP Tool Metadata Extraction
    For any discovered MCP tool, the system should extract name, description, and input schema.
    """
    # Create mock MCP instance with dict-format tools
    mock_mcp = Mock()
    mock_mcp.tools = [
        {
            "name": "dict_tool",
            "description": "A tool in dict format",
            "inputSchema": {"type": "object"}
        }
    ]
    mock_mcp.operation_map = {}
    
    discovery = MCPDiscovery(mcp_instance=mock_mcp)
    tools = discovery.discover_tools()
    
    assert len(tools) == 1
    assert tools[0].name == "dict_tool"
    assert tools[0].description == "A tool in dict format"
    assert tools[0].input_schema == {"type": "object"}


def test_discover_tools_returns_empty_when_no_mcp():
    """
    Test that discovery returns empty list when MCP instance is None.
    """
    discovery = MCPDiscovery(mcp_instance=None)
    tools = discovery.discover_tools()
    
    assert len(tools) == 0


def test_tool_endpoint_mapping():
    """
    Feature: endpoint-reporter, Property 8: Tool-Endpoint Mapping
    For any MCP tool that maps to a REST endpoint, the relationship should be documented.
    """
    # Create mock MCP instance with operation_map
    mock_mcp = Mock()
    
    tool = Mock()
    tool.name = "mapped_tool"
    tool.description = "Tool with mapping"
    tool.inputSchema = {}
    
    mock_mcp.tools = [tool]
    mock_mcp.operation_map = {
        "mapped_tool": {
            "path": "/api/test",
            "method": "post"
        }
    }
    
    discovery = MCPDiscovery(mcp_instance=mock_mcp)
    tools = discovery.discover_tools()
    
    assert len(tools) == 1
    assert tools[0].mapped_endpoint == "POST /api/test"


@patch('fastapi_report.discovery.mcp_discovery.requests.post')
def test_initialize_mcp_session(mock_post):
    """
    Feature: endpoint-reporter, Property 42: MCP Protocol Session Initialization
    For any running MCP server, calling initialize should return a valid session ID.
    """
    # Mock successful initialize response
    mock_response = Mock()
    mock_response.headers = {'Mcp-Session-Id': 'test-session-123'}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response
    
    discovery = MCPDiscovery(base_url="http://localhost:8000")
    session_id = discovery.initialize_mcp_session()
    
    assert session_id == 'test-session-123'
    assert discovery.session_id == 'test-session-123'
    
    # Verify the request was made correctly
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args[0][0] == "http://localhost:8000/mcp"
    assert call_args[1]['json']['method'] == 'initialize'


@patch('fastapi_report.discovery.mcp_discovery.requests.post')
def test_list_tools_via_protocol(mock_post):
    """
    Feature: endpoint-reporter, Property 43: MCP Protocol Tool Discovery
    For any MCP server with registered tools, calling tools/list should return all tools.
    """
    # Mock successful tools/list response
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": {
            "tools": [
                {
                    "name": "protocol_tool_1",
                    "description": "Tool discovered via protocol",
                    "inputSchema": {"type": "object", "properties": {"arg1": {"type": "string"}}}
                },
                {
                    "name": "protocol_tool_2",
                    "description": "Another protocol tool",
                    "inputSchema": {"type": "object"}
                }
            ]
        }
    }
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response
    
    discovery = MCPDiscovery(base_url="http://localhost:8000")
    tools = discovery.list_tools_via_protocol("test-session-123")
    
    assert len(tools) == 2
    assert tools[0].name == "protocol_tool_1"
    assert tools[0].description == "Tool discovered via protocol"
    assert tools[1].name == "protocol_tool_2"
    
    # Verify the request was made correctly
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args[0][0] == "http://localhost:8000/mcp"
    assert call_args[1]['json']['method'] == 'tools/list'
    assert call_args[1]['headers']['Mcp-Session-Id'] == 'test-session-123'


@patch('fastapi_report.discovery.mcp_discovery.requests.post')
def test_discover_tools_from_url(mock_post):
    """
    Feature: endpoint-reporter, Property 42, 43: MCP Protocol Discovery
    Test complete URL-based discovery flow: initialize + tools/list.
    """
    # Mock initialize response
    init_response = Mock()
    init_response.headers = {'Mcp-Session-Id': 'session-456'}
    init_response.raise_for_status = Mock()
    
    # Mock tools/list response
    tools_response = Mock()
    tools_response.json.return_value = {
        "result": {
            "tools": [
                {
                    "name": "url_tool",
                    "description": "Tool from URL",
                    "inputSchema": {}
                }
            ]
        }
    }
    tools_response.raise_for_status = Mock()
    
    # Configure mock to return different responses
    mock_post.side_effect = [init_response, tools_response]
    
    discovery = MCPDiscovery(base_url="http://localhost:8000")
    tools = discovery.discover_tools()
    
    assert len(tools) == 1
    assert tools[0].name == "url_tool"
    assert tools[0].description == "Tool from URL"
    
    # Verify both requests were made
    assert mock_post.call_count == 2


@patch('fastapi_report.discovery.mcp_discovery.requests.post')
def test_initialize_session_handles_missing_header(mock_post):
    """
    Test that initialize handles missing Mcp-Session-Id header gracefully.
    """
    # Mock response without session ID header
    mock_response = Mock()
    mock_response.headers = {}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response
    
    discovery = MCPDiscovery(base_url="http://localhost:8000")
    session_id = discovery.initialize_mcp_session()
    
    assert session_id is None


@patch('fastapi_report.discovery.mcp_discovery.requests.post')
def test_protocol_discovery_handles_network_errors(mock_post):
    """
    Test that protocol discovery handles network errors gracefully.
    """
    import requests
    
    # Mock network error
    mock_post.side_effect = requests.RequestException("Connection failed")
    
    discovery = MCPDiscovery(base_url="http://localhost:8000")
    tools = discovery.discover_tools()
    
    # Should return empty list on error
    assert len(tools) == 0


def test_discover_tools_handles_exceptions():
    """
    Test that discovery handles exceptions gracefully.
    """
    # Create mock MCP instance that raises exception
    mock_mcp = Mock()
    mock_mcp.tools = Mock(side_effect=Exception("Test error"))
    
    discovery = MCPDiscovery(mcp_instance=mock_mcp)
    tools = discovery.discover_tools()
    
    # Should return empty list on error
    assert len(tools) == 0

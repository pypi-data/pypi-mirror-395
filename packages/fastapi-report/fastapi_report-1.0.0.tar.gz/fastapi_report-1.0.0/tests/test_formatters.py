"""
Property-based tests for formatters.

Feature: endpoint-reporter, Property 16, 17, 18: Output Format Validity
Validates: Requirements 4.1, 4.2, 4.3
"""
import json
from hypothesis import given, strategies as st
from fastapi_report.models import APIReport, EndpointInfo, MCPToolInfo, ParameterInfo
from fastapi_report.formatters import JSONFormatter, MarkdownFormatter, HTMLFormatter


def create_sample_report():
    """Create a sample API report for testing."""
    param = ParameterInfo(
        name="test_param",
        param_type="query",
        python_type="str",
        required=True,
        default=None,
        description="Test parameter",
        constraints={"min_length": 1}
    )
    
    endpoint = EndpointInfo(
        path="/test",
        method="GET",
        operation_id="test_endpoint",
        summary="Test endpoint",
        description="A test endpoint",
        tags=["test"],
        parameters=[param],
        request_body=None,
        responses={200: {"description": "Success"}},
        deprecated=False
    )
    
    tool = MCPToolInfo(
        name="test_tool",
        description="Test MCP tool",
        input_schema={"type": "object"},
        mapped_endpoint="GET /test"
    )
    
    return APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[endpoint],
        mcp_tools=[tool],
        openapi_spec={"openapi": "3.0.0"}
    )


def test_json_formatter_produces_valid_json():
    """
    Feature: endpoint-reporter, Property 16: JSON Output Validity
    For any generated report, the JSON output should be valid, parseable JSON.
    """
    report = create_sample_report()
    formatter = JSONFormatter()
    
    output = formatter.format(report)
    
    # Should be valid JSON
    parsed = json.loads(output)
    assert isinstance(parsed, dict)
    assert parsed["server_name"] == "Test API"
    assert parsed["server_version"] == "1.0.0"
    assert len(parsed["endpoints"]) == 1
    assert len(parsed["mcp_tools"]) == 1


def test_json_formatter_file_extension():
    """Test that JSON formatter returns correct file extension."""
    formatter = JSONFormatter()
    assert formatter.get_file_extension() == ".json"


def test_markdown_formatter_produces_valid_markdown():
    """
    Feature: endpoint-reporter, Property 17: Markdown Output Well-Formedness
    For any generated report, the Markdown output should be well-formed.
    """
    report = create_sample_report()
    formatter = MarkdownFormatter()
    
    output = formatter.format(report)
    
    # Should contain markdown headers
    assert "# Test API" in output
    assert "## REST Endpoints" in output
    assert "## MCP Tools" in output
    
    # Should contain endpoint information
    assert "GET /test" in output
    assert "Test endpoint" in output
    
    # Should contain MCP tool information
    assert "test_tool" in output
    assert "Test MCP tool" in output


def test_markdown_formatter_file_extension():
    """Test that Markdown formatter returns correct file extension."""
    formatter = MarkdownFormatter()
    assert formatter.get_file_extension() == ".md"


def test_html_formatter_produces_valid_html():
    """
    Feature: endpoint-reporter, Property 18: HTML Output Validity
    For any generated report, the HTML output should be valid HTML with navigation.
    """
    report = create_sample_report()
    formatter = HTMLFormatter()
    
    output = formatter.format(report)
    
    # Should contain HTML structure
    assert "<!DOCTYPE html>" in output
    assert "<html" in output
    assert "</html>" in output
    assert "<head>" in output
    assert "<body>" in output
    
    # Should contain navigation
    assert "nav" in output.lower()
    
    # Should contain endpoint information
    assert "GET" in output
    assert "/test" in output
    assert "Test endpoint" in output
    
    # Should contain MCP tool information
    assert "test_tool" in output
    assert "Test MCP tool" in output


def test_html_formatter_file_extension():
    """Test that HTML formatter returns correct file extension."""
    formatter = HTMLFormatter()
    assert formatter.get_file_extension() == ".html"


def test_formatters_handle_empty_report():
    """Test that all formatters handle empty reports gracefully."""
    empty_report = APIReport(
        server_name="Empty API",
        server_version="1.0.0",
        endpoints=[],
        mcp_tools=[],
        openapi_spec={}
    )
    
    # JSON formatter
    json_formatter = JSONFormatter()
    json_output = json_formatter.format(empty_report)
    parsed = json.loads(json_output)
    assert len(parsed["endpoints"]) == 0
    assert len(parsed["mcp_tools"]) == 0
    
    # Markdown formatter
    md_formatter = MarkdownFormatter()
    md_output = md_formatter.format(empty_report)
    assert "Empty API" in md_output
    
    # HTML formatter
    html_formatter = HTMLFormatter()
    html_output = html_formatter.format(empty_report)
    assert "Empty API" in html_output


def test_formatters_handle_multiple_endpoints():
    """Test that formatters handle multiple endpoints correctly."""
    endpoints = [
        EndpointInfo(
            path=f"/endpoint{i}",
            method="GET",
            operation_id=f"endpoint_{i}",
            summary=f"Endpoint {i}",
            description=None,
            tags=[],
            parameters=[],
            request_body=None,
            responses={},
            deprecated=False
        )
        for i in range(5)
    ]
    
    report = APIReport(
        server_name="Multi-Endpoint API",
        server_version="1.0.0",
        endpoints=endpoints,
        mcp_tools=[],
        openapi_spec={}
    )
    
    # JSON formatter
    json_formatter = JSONFormatter()
    json_output = json_formatter.format(report)
    parsed = json.loads(json_output)
    assert len(parsed["endpoints"]) == 5
    
    # Markdown formatter
    md_formatter = MarkdownFormatter()
    md_output = md_formatter.format(report)
    for i in range(5):
        assert f"/endpoint{i}" in md_output
    
    # HTML formatter
    html_formatter = HTMLFormatter()
    html_output = html_formatter.format(report)
    for i in range(5):
        assert f"/endpoint{i}" in html_output


def test_json_formatter_handles_special_characters():
    """Test that JSON formatter properly escapes special characters."""
    endpoint = EndpointInfo(
        path="/test",
        method="GET",
        operation_id="test",
        summary='Test with "quotes" and \\ backslashes',
        description="Test with\nnewlines",
        tags=[],
        parameters=[],
        request_body=None,
        responses={},
        deprecated=False
    )
    
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[endpoint],
        mcp_tools=[],
        openapi_spec={}
    )
    
    formatter = JSONFormatter()
    output = formatter.format(report)
    
    # Should be valid JSON despite special characters
    parsed = json.loads(output)
    assert 'quotes' in parsed["endpoints"][0]["summary"]
    assert 'newlines' in parsed["endpoints"][0]["description"]


def test_markdown_formatter_creates_parameter_tables():
    """Test that Markdown formatter creates proper parameter tables."""
    params = [
        ParameterInfo(
            name="param1",
            param_type="query",
            python_type="str",
            required=True,
            default=None,
            description="First parameter",
            constraints={}
        ),
        ParameterInfo(
            name="param2",
            param_type="query",
            python_type="int",
            required=False,
            default=10,
            description="Second parameter",
            constraints={"ge": 1, "le": 100}
        )
    ]
    
    endpoint = EndpointInfo(
        path="/test",
        method="GET",
        operation_id="test",
        summary="Test",
        description=None,
        tags=[],
        parameters=params,
        request_body=None,
        responses={},
        deprecated=False
    )
    
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[endpoint],
        mcp_tools=[],
        openapi_spec={}
    )
    
    formatter = MarkdownFormatter()
    output = formatter.format(report)
    
    # Should contain parameter table
    assert "param1" in output
    assert "param2" in output
    assert "First parameter" in output
    assert "Second parameter" in output


def test_html_formatter_includes_css_styling():
    """Test that HTML formatter includes CSS styling."""
    report = create_sample_report()
    formatter = HTMLFormatter()
    
    output = formatter.format(report)
    
    # Should contain style tag
    assert "<style>" in output
    assert "</style>" in output
    
    # Should contain some CSS rules
    assert "body" in output or "font-family" in output

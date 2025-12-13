"""
Tests for the EndpointReporter class.

Feature: endpoint-reporter, Property 19, 20, 21, 22: Reporter Functionality
Validates: Requirements 4.4, 4.5, 5.1, 5.4
"""
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI
from fastapi_report.reporter import EndpointReporter
from fastapi_report.models import APIReport


def test_reporter_with_module_mode():
    """
    Feature: endpoint-reporter, Property 21: Dynamic Module Loading
    For any valid Python module name, the system should successfully import and analyze it.
    """
    # Create a simple FastAPI app
    app = FastAPI(title="Test API", version="1.0.0")
    
    @app.get("/test")
    def test_endpoint():
        return {"message": "test"}
    
    # Mock the module import
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_module.app = app
        mock_import.return_value = mock_module
        
        reporter = EndpointReporter("test_module")
        
        assert reporter.app == app
        assert reporter.mode == 'module'
        # Module is imported twice: once in load_server, once in load_mcp
        assert mock_import.call_count >= 1


def test_reporter_with_url_mode():
    """
    Test that reporter correctly identifies URL mode.
    """
    reporter = EndpointReporter("http://localhost:8000")
    
    assert reporter.mode == 'url'
    assert reporter.base_url == "http://localhost:8000"
    assert reporter.app is None


@patch('fastapi_report.reporter.requests.get')
def test_generate_report_from_url(mock_get):
    """
    Test report generation from URL mode.
    """
    # Mock OpenAPI schema response
    mock_response = Mock()
    mock_response.json.return_value = {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {
            "/test": {
                "get": {
                    "operationId": "test_get",
                    "summary": "Test endpoint",
                    "parameters": [],
                    "responses": {
                        "200": {"description": "Success"}
                    }
                }
            }
        }
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    reporter = EndpointReporter("http://localhost:8000")
    report = reporter.generate_report()
    
    assert report.server_name == "Test API"
    assert report.server_version == "1.0.0"
    assert len(report.endpoints) == 1
    assert report.endpoints[0].path == "/test"
    assert report.endpoints[0].method == "GET"


def test_output_report_creates_files():
    """
    Feature: endpoint-reporter, Property 20: File Output Correctness
    For any specified output path, the system should write files to the correct location.
    """
    # Create a sample report
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[],
        mcp_tools=[],
        openapi_spec={}
    )
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "output"
        
        # Create a mock reporter
        reporter = EndpointReporter("http://localhost:8000")
        reporter.output_report(report, ["json", "md", "html"], str(output_path))
        
        # Verify files were created
        assert (output_path / "api_documentation.json").exists()
        assert (output_path / "api_documentation.md").exists()
        assert (output_path / "api_documentation.html").exists()
        
        # Verify JSON content
        with open(output_path / "api_documentation.json") as f:
            data = json.load(f)
            assert data["server_name"] == "Test API"


def test_multi_format_generation():
    """
    Feature: endpoint-reporter, Property 19: Multi-Format Generation
    For any report generation request with multiple formats, all should be produced.
    """
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[],
        mcp_tools=[],
        openapi_spec={}
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = EndpointReporter("http://localhost:8000")
        reporter.output_report(report, ["json", "md", "html"], tmpdir)
        
        # All three formats should be generated
        output_dir = Path(tmpdir)
        assert (output_dir / "api_documentation.json").exists()
        assert (output_dir / "api_documentation.md").exists()
        assert (output_dir / "api_documentation.html").exists()


def test_load_server_handles_missing_module():
    """
    Feature: endpoint-reporter, Property 22: Import Error Handling
    For any invalid module name, the system should report a clear error message.
    """
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_import.side_effect = ModuleNotFoundError("No module named 'nonexistent'")
        
        with pytest.raises(SystemExit) as exc_info:
            reporter = EndpointReporter("nonexistent_module")
        
        assert exc_info.value.code == 1


def test_load_server_handles_missing_app():
    """
    Test that load_server handles modules without FastAPI app.
    """
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        # Module has no 'app', 'application', or 'api' attribute
        mock_module.app = None
        mock_module.application = None
        mock_module.api = None
        mock_import.return_value = mock_module
        
        with pytest.raises(SystemExit) as exc_info:
            reporter = EndpointReporter("module_without_app")
        
        assert exc_info.value.code == 1


def test_load_mcp_from_app():
    """
    Test that load_mcp correctly extracts MCP instance from app.
    """
    app = FastAPI()
    mock_mcp = Mock()
    app.mcp = mock_mcp
    
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_module.app = app
        mock_import.return_value = mock_module
        
        reporter = EndpointReporter("test_module")
        
        assert reporter.mcp == mock_mcp


def test_load_mcp_from_app_state():
    """
    Test that load_mcp can extract MCP from app.state.
    """
    app = FastAPI()
    mock_mcp = Mock()
    app.state.mcp = mock_mcp
    
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_module.app = app
        mock_import.return_value = mock_module
        
        reporter = EndpointReporter("test_module")
        
        assert reporter.mcp == mock_mcp


def test_load_mcp_from_module():
    """
    Test that load_mcp can extract MCP from module-level variable.
    """
    app = FastAPI()
    mock_mcp = Mock()
    
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_module.app = app
        mock_module.mcp = mock_mcp
        mock_import.return_value = mock_module
        
        reporter = EndpointReporter("test_module")
        
        assert reporter.mcp == mock_mcp


def test_generate_report_from_module():
    """
    Test complete report generation from module mode.
    """
    app = FastAPI(title="Module API", version="2.0.0")
    
    @app.get("/module-test")
    def test_endpoint():
        return {}
    
    with patch('fastapi_report.reporter.importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_module.app = app
        mock_import.return_value = mock_module
        
        reporter = EndpointReporter("test_module")
        report = reporter.generate_report()
        
        assert report.server_name == "Module API"
        assert report.server_version == "2.0.0"
        assert len(report.endpoints) > 0


@patch('fastapi_report.reporter.requests.get')
def test_url_mode_handles_network_errors(mock_get):
    """
    Test that URL mode handles network errors gracefully.
    """
    import requests
    mock_get.side_effect = requests.RequestException("Connection failed")
    
    reporter = EndpointReporter("http://localhost:8000")
    
    with pytest.raises(SystemExit) as exc_info:
        reporter.generate_report()
    
    assert exc_info.value.code == 1


def test_output_report_handles_invalid_format():
    """
    Test that output_report handles invalid format names gracefully.
    """
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[],
        mcp_tools=[],
        openapi_spec={}
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = EndpointReporter("http://localhost:8000")
        
        # Should not crash with invalid format
        reporter.output_report(report, ["invalid_format"], tmpdir)
        
        # No files should be created for invalid format
        output_dir = Path(tmpdir)
        assert not (output_dir / "api_documentation.invalid_format").exists()


def test_reporter_creates_output_directory():
    """
    Test that reporter creates output directory if it doesn't exist.
    """
    report = APIReport(
        server_name="Test API",
        server_version="1.0.0",
        endpoints=[],
        mcp_tools=[],
        openapi_spec={}
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "nested" / "output" / "dir"
        
        reporter = EndpointReporter("http://localhost:8000")
        reporter.output_report(report, ["json"], str(output_path))
        
        # Directory should be created
        assert output_path.exists()
        assert (output_path / "api_documentation.json").exists()

# FastAPI Report

Automatically generate comprehensive documentation for FastAPI applications including REST API endpoints and MCP (Model Context Protocol) tools.

## Features

- 🔍 **Automatic Discovery**: Introspects FastAPI applications to extract all endpoints and MCP tools
- 📝 **Multiple Formats**: Generate documentation in JSON, Markdown, and HTML formats
- 🌐 **Dual Mode Support**: 
  - **Module Mode**: Direct Python introspection of local FastAPI applications
  - **URL Mode**: Remote discovery via HTTP using OpenAPI spec and MCP protocol
- 🛠️ **MCP Protocol Support**: Discovers MCP tools from running servers using the MCP JSON-RPC protocol
- 📊 **Rich Metadata**: Captures parameters, types, constraints, descriptions, request/response schemas
- 🎨 **Beautiful Output**: Styled HTML with navigation, formatted Markdown, and structured JSON

## Installation

```bash
pip install "git+https://github.com/maat16/fastapi-report.git"
```

## Quick Start

### Command Line Usage

**Analyze a running server (URL mode):**
```bash
# Discover both REST endpoints and MCP tools from a running server
fastapi-report --server http://localhost:8000 --format all

# Generate only JSON documentation
fastapi-report --server http://localhost:8000 --format json

# Specify custom output directory
fastapi-report --server http://localhost:8000 --format all --output ./docs
```

**Analyze a Python module (Module mode):**
```bash
# Analyze a local FastAPI module
fastapi-report --server my_api_module --format all

# Analyze nested module
fastapi-report --server app.main --format md
```

### Python API Usage

```python
from fastapi_report.reporter import EndpointReporter

# URL mode - analyze running server
reporter = EndpointReporter("http://localhost:8000")
report = reporter.generate_report()

print(f"Found {len(report.endpoints)} endpoints")
print(f"Found {len(report.mcp_tools)} MCP tools")

# Generate documentation files
reporter.output_report(report, ["json", "md", "html"], "./output")

# Module mode - analyze local module
reporter = EndpointReporter("my_api_module")
report = reporter.generate_report()
```

## How It Works

### Module Mode
When you provide a Python module name, the tool:
1. Dynamically imports the module
2. Extracts the FastAPI application instance
3. Introspects routes using FastAPI's internal APIs
4. Discovers MCP tools from the MCP instance (if available)
5. Generates comprehensive documentation

### URL Mode
When you provide a URL, the tool:
1. Fetches the OpenAPI specification from `/openapi.json`
2. Parses REST endpoints from the OpenAPI spec
3. **Discovers MCP tools using the MCP protocol:**
   - Calls `/mcp` with `initialize` method to establish a session
   - Extracts `Mcp-Session-Id` from response headers
   - Calls `/mcp` with `tools/list` method using the session ID
   - Parses tool metadata (name, description, input schema)
4. Generates documentation from discovered information

## MCP Protocol Discovery

The tool supports discovering MCP tools from running servers using the MCP JSON-RPC protocol:

```python
# The tool automatically:
# 1. Initializes MCP session
POST /mcp
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "fastapi-report", "version": "1.0.0"}
  }
}

# 2. Lists available tools
POST /mcp
Headers: Mcp-Session-Id: <session-id>
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {"cursor": null}
}
```

## Output Formats

### JSON
Structured JSON with complete metadata:
```json
{
  "server_name": "My API",
  "server_version": "1.0.0",
  "endpoints": [...],
  "mcp_tools": [...],
  "openapi_spec": {...},
  "generated_at": "2024-01-01T12:00:00"
}
```

### Markdown
Human-readable documentation with tables and code blocks:
```markdown
# My API

## REST Endpoints

### GET /users
Get all users

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | int | No | Maximum results |

## MCP Tools

### get_users
Retrieve user list via MCP
```

### HTML
Styled, browsable web page with:
- Navigation sidebar
- Syntax-highlighted code
- Collapsible sections
- Responsive design

## Development

### Setup
```bash
# Clone the repository
git clone https://github.com/maat16/fastapi-report.git
cd fastapi-report

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fastapi_report --cov-report=html

# Run specific test file
pytest tests/test_mcp_discovery.py -v
```

### Test Coverage
The package includes comprehensive tests:
- **Property-based tests** using Hypothesis for data models
- **Unit tests** for all discovery components
- **Integration tests** for formatters and reporters
- **Mock-based tests** for MCP protocol discovery

Current test coverage: **46 tests, all passing**

## Requirements

- Python 3.8+
- FastAPI 0.100.0+
- Pydantic 2.0.0+
- Requests 2.28.0+

## Use Cases

- **API Documentation**: Generate up-to-date documentation automatically
- **CI/CD Integration**: Include in pipelines to validate API changes
- **Development**: Quick reference for available endpoints and tools
- **Testing**: Verify endpoint metadata and MCP tool configurations
- **Comparison**: Compare production vs. mock server implementations

## Examples

### Example 1: Basic Usage
```bash
fastapi-report --server http://localhost:8000 --format all
```

Output:
```
Analyzing http://localhost:8000 (URL)...
Discovering endpoints and tools...
Found 10 endpoints and 4 MCP tools
Generating documentation in json, md, html format(s)...
✓ Generated JSON report: reports/api_documentation.json
✓ Generated MD report: reports/api_documentation.md
✓ Generated HTML report: reports/api_documentation.html
✓ Documentation generation complete!
```

### Example 2: Module Analysis
```bash
fastapi-report --server my_app.main --format md --output ./docs
```

### Example 3: Programmatic Usage
```python
from fastapi_report.reporter import EndpointReporter
from fastapi_report.formatters import MarkdownFormatter

# Generate report
reporter = EndpointReporter("http://localhost:8000")
report = reporter.generate_report()

# Custom formatting
formatter = MarkdownFormatter()
markdown_content = formatter.format(report)

# Save to file
with open("api_docs.md", "w") as f:
    f.write(markdown_content)
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Changelog

### Version 1.0.0
- Initial release
- REST endpoint discovery
- MCP tool discovery (module and URL modes)
- MCP protocol support for remote discovery
- JSON, Markdown, and HTML formatters
- Comprehensive test suite
- CLI and Python API

## Support

For issues, questions, or contributions, please visit:
https://github.com/maat16/fastapi-report

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing

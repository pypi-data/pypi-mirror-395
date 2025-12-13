"""HTML formatter for API reports."""
import json
from fastapi_report.models import APIReport, EndpointInfo, MCPToolInfo
from .base import BaseFormatter


class HTMLFormatter(BaseFormatter):
    """Formats API reports as styled HTML pages."""
    
    def format(self, report: APIReport) -> str:
        """
        Convert report to styled HTML page.
        
        Args:
            report: APIReport to format
            
        Returns:
            HTML string with embedded CSS
        """
        html_parts = []
        
        # HTML header with CSS
        html_parts.append(self._get_html_header(report.server_name))
        
        # Body start
        html_parts.append("<body>")
        
        # Navigation
        html_parts.append(self.generate_navigation(report.endpoints, report.mcp_tools))
        
        # Main content
        html_parts.append('<div class="content">')
        
        # Title
        html_parts.append(f"<h1>{report.server_name} API Documentation</h1>")
        html_parts.append(f'<p class="metadata">Version: {report.server_version} | Generated: {report.generated_at}</p>')
        
        # Endpoints section
        html_parts.append('<h2 id="endpoints">REST Endpoints</h2>')
        
        if not report.endpoints:
            html_parts.append("<p><em>No endpoints found.</em></p>")
        else:
            for endpoint in report.endpoints:
                html_parts.append(self.generate_endpoint_section(endpoint))
        
        # MCP Tools section
        if report.mcp_tools:
            html_parts.append('<h2 id="mcp-tools">MCP Tools</h2>')
            html_parts.append(f'<p class="tool-count">Total Tools: <strong>{len(report.mcp_tools)}</strong></p>')
            
            # Tool summary cards
            html_parts.append('<div class="tool-summary">')
            html_parts.append('<h3>Available Tools</h3>')
            html_parts.append('<div class="tool-cards">')
            for tool in report.mcp_tools:
                desc_first_line = tool.description.split('\n')[0] if tool.description else "No description"
                html_parts.append(f'''
                <div class="tool-card">
                    <a href="#tool-{tool.name}">
                        <h4>{tool.name}</h4>
                        <p>{desc_first_line[:100]}...</p>
                        {f'<code class="endpoint-badge">{tool.mapped_endpoint}</code>' if tool.mapped_endpoint else ''}
                    </a>
                </div>
                ''')
            html_parts.append('</div>')
            html_parts.append('</div>')
            
            # Detailed tool documentation
            html_parts.append('<h3>Tool Details</h3>')
            for tool in report.mcp_tools:
                html_parts.append(self._generate_mcp_tool_section(tool))
        
        html_parts.append("</div>")  # Close content
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return "\n".join(html_parts)
    
    def _get_html_header(self, title: str) -> str:
        """Generate HTML header with embedded CSS."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - API Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .nav {{
            position: fixed;
            left: 0;
            top: 0;
            width: 250px;
            height: 100vh;
            background: #2c3e50;
            color: white;
            padding: 20px;
            overflow-y: auto;
        }}
        
        .nav h3 {{
            margin-bottom: 15px;
            color: #ecf0f1;
        }}
        
        .nav ul {{
            list-style: none;
        }}
        
        .nav li {{
            margin: 8px 0;
        }}
        
        .nav a {{
            color: #ecf0f1;
            text-decoration: none;
            font-size: 14px;
        }}
        
        .nav a:hover {{
            color: #3498db;
        }}
        
        .content {{
            margin-left: 270px;
            padding: 40px;
            max-width: 1200px;
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}
        
        .metadata {{
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        
        .endpoint {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .endpoint-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .method {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
            margin-right: 10px;
        }}
        
        .method.get {{ background: #61affe; color: white; }}
        .method.post {{ background: #49cc90; color: white; }}
        .method.put {{ background: #fca130; color: white; }}
        .method.delete {{ background: #f93e3e; color: white; }}
        .method.patch {{ background: #50e3c2; color: white; }}
        
        .path {{
            font-family: 'Courier New', monospace;
            font-size: 18px;
            color: #2c3e50;
        }}
        
        .deprecated {{
            background: #e74c3c;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 10px;
        }}
        
        .summary {{
            font-size: 16px;
            color: #555;
            margin-bottom: 10px;
        }}
        
        .description {{
            color: #666;
            margin-bottom: 15px;
        }}
        
        .tags {{
            margin-bottom: 15px;
        }}
        
        .tag {{
            display: inline-block;
            background: #ecf0f1;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 12px;
            margin-right: 5px;
            color: #555;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        th {{
            background: #34495e;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .required {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        pre code {{
            background: transparent;
            color: #ecf0f1;
            padding: 0;
            font-size: 13px;
        }}
        
        code {{
            font-family: 'Courier New', monospace;
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
            color: #2c3e50;
        }}
        
        .section-title {{
            font-weight: 600;
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .tool-count {{
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        
        .tool-summary {{
            margin-bottom: 40px;
        }}
        
        .tool-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .tool-card {{
            background: white;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        
        .tool-card:hover {{
            border-color: #3498db;
            box-shadow: 0 4px 8px rgba(52, 152, 219, 0.2);
            transform: translateY(-2px);
        }}
        
        .tool-card a {{
            text-decoration: none;
            color: inherit;
        }}
        
        .tool-card h4 {{
            color: #2c3e50;
            margin: 0 0 10px 0;
            font-size: 16px;
        }}
        
        .tool-card p {{
            color: #666;
            margin: 0 0 10px 0;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .endpoint-badge {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-top: 5px;
        }}
        
        .tool-detail {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .schema-container {{
            margin-top: 15px;
        }}
        
        .schema-toggle {{
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .schema-toggle:hover {{
            background: #2980b9;
        }}
        
        .schema-content {{
            display: none;
            margin-top: 10px;
        }}
        
        .schema-content.show {{
            display: block;
        }}
    </style>
    <script>
        function toggleSchema(toolName) {{
            const content = document.getElementById('schema-' + toolName);
            const button = document.getElementById('btn-' + toolName);
            if (content.classList.contains('show')) {{
                content.classList.remove('show');
                button.textContent = 'Show Full Schema';
            }} else {{
                content.classList.add('show');
                button.textContent = 'Hide Schema';
            }}
        }}
    </script>
</head>"""
    
    def generate_navigation(self, endpoints: list, mcp_tools: list) -> str:
        """
        Generate HTML navigation menu.
        
        Args:
            endpoints: List of EndpointInfo objects
            mcp_tools: List of MCPToolInfo objects
            
        Returns:
            HTML navigation string
        """
        nav_parts = ['<div class="nav">']
        nav_parts.append("<h3>Navigation</h3>")
        nav_parts.append("<ul>")
        nav_parts.append('<li><a href="#endpoints">REST Endpoints</a></li>')
        
        if endpoints:
            nav_parts.append("<ul>")
            for endpoint in endpoints:
                endpoint_id = f"{endpoint.method.lower()}-{endpoint.path.replace('/', '-').replace('{', '').replace('}', '')}"
                nav_parts.append(f'<li><a href="#{endpoint_id}">{endpoint.method} {endpoint.path}</a></li>')
            nav_parts.append("</ul>")
        
        if mcp_tools:
            nav_parts.append('<li><a href="#mcp-tools">MCP Tools</a></li>')
        
        nav_parts.append("</ul>")
        nav_parts.append("</div>")
        
        return "\n".join(nav_parts)
    
    def generate_endpoint_section(self, endpoint: EndpointInfo) -> str:
        """
        Generate HTML section for endpoint.
        
        Args:
            endpoint: EndpointInfo to format
            
        Returns:
            HTML string for endpoint section
        """
        endpoint_id = f"{endpoint.method.lower()}-{endpoint.path.replace('/', '-').replace('{', '').replace('}', '')}"
        
        parts = [f'<div class="endpoint" id="{endpoint_id}">']
        
        # Header
        parts.append('<div class="endpoint-header">')
        parts.append(f'<span class="method {endpoint.method.lower()}">{endpoint.method}</span>')
        parts.append(f'<span class="path">{endpoint.path}</span>')
        if endpoint.deprecated:
            parts.append('<span class="deprecated">DEPRECATED</span>')
        parts.append('</div>')
        
        # Summary
        if endpoint.summary:
            parts.append(f'<div class="summary">{endpoint.summary}</div>')
        
        # Description
        if endpoint.description:
            parts.append(f'<div class="description">{endpoint.description}</div>')
        
        # Tags
        if endpoint.tags:
            parts.append('<div class="tags">')
            for tag in endpoint.tags:
                parts.append(f'<span class="tag">{tag}</span>')
            parts.append('</div>')
        
        # Parameters
        if endpoint.parameters:
            parts.append('<div class="section-title">Parameters</div>')
            parts.append('<table>')
            parts.append('<tr><th>Name</th><th>Type</th><th>In</th><th>Required</th><th>Default</th><th>Description</th></tr>')
            
            for param in endpoint.parameters:
                required_mark = '<span class="required">✓</span>' if param.required else '✗'
                default_val = str(param.default) if param.default is not None else '-'
                desc = param.description or '-'
                
                # Add constraints
                if param.constraints:
                    constraint_strs = [f"{k}={v}" for k, v in param.constraints.items()]
                    desc += f" <code>({', '.join(constraint_strs)})</code>"
                
                parts.append(f'<tr><td><code>{param.name}</code></td><td>{param.python_type}</td><td>{param.param_type}</td><td>{required_mark}</td><td>{default_val}</td><td>{desc}</td></tr>')
            
            parts.append('</table>')
        
        # Request body
        if endpoint.request_body:
            parts.append('<div class="section-title">Request Body</div>')
            parts.append('<pre><code>')
            parts.append(json.dumps(endpoint.request_body, indent=2))
            parts.append('</code></pre>')
        
        # Responses
        if endpoint.responses:
            parts.append('<div class="section-title">Responses</div>')
            parts.append('<table>')
            parts.append('<tr><th>Status Code</th><th>Description</th></tr>')
            
            for status_code, response_data in sorted(endpoint.responses.items()):
                desc = response_data.get('description', '')
                parts.append(f'<tr><td><strong>{status_code}</strong></td><td>{desc}</td></tr>')
            
            parts.append('</table>')
        
        parts.append('</div>')  # Close endpoint div
        
        return "\n".join(parts)
    
    def _generate_mcp_tool_section(self, tool: MCPToolInfo) -> str:
        """Generate HTML section for MCP tool."""
        # Create safe ID for the tool
        tool_id = tool.name.replace('_', '-')
        
        parts = [f'<div class="tool-detail" id="tool-{tool.name}">']
        
        parts.append(f'<h3>{tool.name}</h3>')
        
        if tool.mapped_endpoint:
            parts.append(f'<div class="section-title">Mapped Endpoint: <code class="endpoint-badge">{tool.mapped_endpoint}</code></div>')
        
        if tool.description:
            # Show first paragraph
            desc_parts = tool.description.split('\n\n')
            parts.append(f'<div class="description">{desc_parts[0]}</div>')
        
        # Show parameters in a table if available
        if tool.input_schema and tool.input_schema.get('properties'):
            parts.append('<div class="section-title">Parameters</div>')
            parts.append('<table>')
            parts.append('<tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr>')
            
            properties = tool.input_schema.get('properties', {})
            required = tool.input_schema.get('required', [])
            
            for param_name, param_schema in properties.items():
                param_type = param_schema.get('type', 'any')
                is_required = '<span class="required">✓</span>' if param_name in required else '✗'
                param_desc = param_schema.get('description', '-')
                
                # Handle anyOf types
                if 'anyOf' in param_schema:
                    types = [t.get('type', 'any') for t in param_schema['anyOf'] if 'type' in t]
                    param_type = ' | '.join(set(types))
                
                parts.append(f'<tr><td><code>{param_name}</code></td><td>{param_type}</td><td>{is_required}</td><td>{param_desc}</td></tr>')
            
            parts.append('</table>')
        
        # Collapsible full schema
        if tool.input_schema:
            parts.append('<div class="schema-container">')
            parts.append(f'<button class="schema-toggle" id="btn-{tool_id}" onclick="toggleSchema(\'{tool_id}\')">Show Full Schema</button>')
            parts.append(f'<div class="schema-content" id="schema-{tool_id}">')
            parts.append('<pre><code>')
            parts.append(json.dumps(tool.input_schema, indent=2))
            parts.append('</code></pre>')
            parts.append('</div>')
            parts.append('</div>')
        
        parts.append('</div>')
        
        return "\n".join(parts)
    
    def get_file_extension(self) -> str:
        """Return HTML file extension."""
        return ".html"

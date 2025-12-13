"""Markdown formatter for API reports."""
from fastapi_report.models import APIReport, EndpointInfo, ParameterInfo, MCPToolInfo
from .base import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """Formats API reports as Markdown documentation."""
    
    def format(self, report: APIReport) -> str:
        """
        Convert report to Markdown documentation.
        
        Args:
            report: APIReport to format
            
        Returns:
            Markdown formatted string
        """
        lines = []
        
        # Title and metadata
        lines.append(f"# {report.server_name} API Documentation")
        lines.append("")
        lines.append(f"**Version:** {report.server_version}")
        lines.append(f"**Generated:** {report.generated_at}")
        lines.append("")
        
        # Table of contents
        lines.append("## Table of Contents")
        lines.append("")
        lines.append("- [REST Endpoints](#rest-endpoints)")
        if report.mcp_tools:
            lines.append("- [MCP Tools](#mcp-tools)")
        lines.append("")
        
        # REST Endpoints section
        lines.append("## REST Endpoints")
        lines.append("")
        
        if not report.endpoints:
            lines.append("*No endpoints found.*")
            lines.append("")
        else:
            for endpoint in report.endpoints:
                lines.extend(self.format_endpoint(endpoint))
                lines.append("")
        
        # MCP Tools section
        if report.mcp_tools:
            lines.append("## MCP Tools")
            lines.append("")
            lines.append(f"**Total Tools:** {len(report.mcp_tools)}")
            lines.append("")
            
            # Tool summary list
            lines.append("### Available Tools")
            lines.append("")
            for tool in report.mcp_tools:
                # Extract first line of description
                desc_first_line = tool.description.split('\n')[0] if tool.description else "No description"
                lines.append(f"- **[{tool.name}](#{tool.name.replace('_', '-')})** - {desc_first_line}")
            lines.append("")
            
            # Detailed tool documentation
            lines.append("### Tool Details")
            lines.append("")
            for tool in report.mcp_tools:
                lines.extend(self.format_mcp_tool(tool))
                lines.append("")
        
        return "\n".join(lines)
    
    def format_endpoint(self, endpoint: EndpointInfo) -> list:
        """
        Format single endpoint as Markdown section.
        
        Args:
            endpoint: EndpointInfo to format
            
        Returns:
            List of markdown lines
        """
        lines = []
        
        # Endpoint header
        lines.append(f"### `{endpoint.method} {endpoint.path}`")
        lines.append("")
        
        if endpoint.summary:
            lines.append(f"**Summary:** {endpoint.summary}")
            lines.append("")
        
        if endpoint.description:
            lines.append(endpoint.description)
            lines.append("")
        
        if endpoint.tags:
            lines.append(f"**Tags:** {', '.join(endpoint.tags)}")
            lines.append("")
        
        if endpoint.deprecated:
            lines.append("⚠️ **DEPRECATED**")
            lines.append("")
        
        # Parameters
        if endpoint.parameters:
            lines.append("**Parameters:**")
            lines.append("")
            lines.extend(self.format_parameters_table(endpoint.parameters))
            lines.append("")
        
        # Request body
        if endpoint.request_body:
            lines.append("**Request Body:**")
            lines.append("")
            lines.append("```json")
            lines.append(str(endpoint.request_body))
            lines.append("```")
            lines.append("")
        
        # Responses
        if endpoint.responses:
            lines.append("**Responses:**")
            lines.append("")
            for status_code, response_data in sorted(endpoint.responses.items()):
                desc = response_data.get('description', '')
                lines.append(f"- **{status_code}**: {desc}")
            lines.append("")
        
        return lines
    
    def format_parameters_table(self, params: list) -> list:
        """
        Format parameters as Markdown table.
        
        Args:
            params: List of ParameterInfo objects
            
        Returns:
            List of markdown table lines
        """
        lines = []
        
        # Table header
        lines.append("| Name | Type | In | Required | Default | Description |")
        lines.append("|------|------|----|---------|---------| ------------|")
        
        # Table rows
        for param in params:
            name = param.name
            ptype = param.python_type
            location = param.param_type
            required = "✓" if param.required else "✗"
            default = str(param.default) if param.default is not None else "-"
            desc = param.description or "-"
            
            # Add constraints to description
            if param.constraints:
                constraint_strs = []
                for key, value in param.constraints.items():
                    constraint_strs.append(f"{key}={value}")
                if constraint_strs:
                    desc += f" ({', '.join(constraint_strs)})"
            
            lines.append(f"| {name} | {ptype} | {location} | {required} | {default} | {desc} |")
        
        return lines
    
    def format_mcp_tool(self, tool: MCPToolInfo) -> list:
        """
        Format MCP tool as Markdown section.
        
        Args:
            tool: MCPToolInfo to format
            
        Returns:
            List of markdown lines
        """
        lines = []
        
        # Use tool name as anchor
        lines.append(f"#### {tool.name}")
        lines.append("")
        
        if tool.mapped_endpoint:
            lines.append(f"**Mapped Endpoint:** `{tool.mapped_endpoint}`")
            lines.append("")
        
        if tool.description:
            # Show first paragraph prominently
            desc_parts = tool.description.split('\n\n')
            lines.append(desc_parts[0])
            lines.append("")
            
            # Show rest in details if there's more
            if len(desc_parts) > 1:
                lines.append("<details>")
                lines.append("<summary>Show full description</summary>")
                lines.append("")
                for part in desc_parts[1:]:
                    lines.append(part)
                    lines.append("")
                lines.append("</details>")
                lines.append("")
        
        if tool.input_schema and tool.input_schema.get('properties'):
            lines.append("**Parameters:**")
            lines.append("")
            
            # Show parameters in a table
            properties = tool.input_schema.get('properties', {})
            required = tool.input_schema.get('required', [])
            
            if properties:
                lines.append("| Parameter | Type | Required | Description |")
                lines.append("|-----------|------|----------|-------------|")
                
                for param_name, param_schema in properties.items():
                    param_type = param_schema.get('type', 'any')
                    is_required = "✓" if param_name in required else "✗"
                    param_desc = param_schema.get('description', '-')
                    
                    # Handle anyOf types
                    if 'anyOf' in param_schema:
                        types = [t.get('type', 'any') for t in param_schema['anyOf'] if 'type' in t]
                        param_type = ' | '.join(set(types))
                    
                    lines.append(f"| {param_name} | {param_type} | {is_required} | {param_desc} |")
                
                lines.append("")
            
            # Collapsible full schema
            lines.append("<details>")
            lines.append("<summary>Show full JSON schema</summary>")
            lines.append("")
            lines.append("```json")
            import json
            lines.append(json.dumps(tool.input_schema, indent=2))
            lines.append("```")
            lines.append("</details>")
            lines.append("")
        
        return lines
    
    def get_file_extension(self) -> str:
        """Return Markdown file extension."""
        return ".md"

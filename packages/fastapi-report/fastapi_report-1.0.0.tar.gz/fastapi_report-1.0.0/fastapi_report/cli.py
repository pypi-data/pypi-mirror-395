#!/usr/bin/env python3
"""
FastAPI Report - CLI Entry Point

Command-line tool for automatically generating comprehensive documentation
for FastAPI applications including REST endpoints and MCP tools.
"""
import argparse
import sys

from fastapi_report.reporter import EndpointReporter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FastAPI Endpoint Documentation Generator - Works with ANY FastAPI app!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate docs from Python module
  fastapi-report --server my_api --format all
  
  # Generate docs from running server URL
  fastapi-report --server http://localhost:8000 --format all
  
  # Generate docs for nested module
  fastapi-report --server app.main --format json
  
  # Custom output directory
  fastapi-report --server http://127.0.0.1:1234 --format md --output ./docs
        """
    )
    
    parser.add_argument(
        "--server",
        required=True,
        help="Python module name OR server URL. Examples: 'my_api', 'app.main', 'http://localhost:8000'"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "md", "html", "all"],
        default="all",
        help="Output format (default: all)"
    )
    
    parser.add_argument(
        "--output",
        default="./reports",
        help="Output directory (default: ./reports)"
    )
    
    args = parser.parse_args()
    
    # Determine formats
    if args.format == "all":
        formats = ["json", "md", "html"]
    else:
        formats = [args.format]
    
    try:
        # Determine source type
        source_type = "URL" if args.server.startswith(('http://', 'https://')) else "module"
        print(f"Analyzing {args.server} ({source_type})...")
        
        # Create reporter and generate report
        reporter = EndpointReporter(args.server)
        
        print("Discovering endpoints and tools...")
        report = reporter.generate_report()
        
        print(f"Found {len(report.endpoints)} endpoints and {len(report.mcp_tools)} MCP tools")
        
        print(f"Generating documentation in {', '.join(formats)} format(s)...")
        reporter.output_report(report, formats, args.output)
        
        print("\n✓ Documentation generation complete!")
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

"""JSON formatter for API reports."""
import json
from fastapi_report.models import APIReport
from .base import BaseFormatter


class JSONFormatter(BaseFormatter):
    """Formats API reports as JSON."""
    
    def format(self, report: APIReport) -> str:
        """
        Convert report to formatted JSON.
        
        Args:
            report: APIReport to format
            
        Returns:
            JSON string with proper indentation
        """
        report_dict = report.to_dict()
        return json.dumps(report_dict, indent=2, default=str)
    
    def get_file_extension(self) -> str:
        """Return JSON file extension."""
        return ".json"

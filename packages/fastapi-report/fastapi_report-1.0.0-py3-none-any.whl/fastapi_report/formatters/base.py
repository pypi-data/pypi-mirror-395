"""Base formatter abstract class."""
from abc import ABC, abstractmethod
from fastapi_report.models import APIReport


class BaseFormatter(ABC):
    """Abstract base class for report formatters."""
    
    @abstractmethod
    def format(self, report: APIReport) -> str:
        """
        Format report into output string.
        
        Args:
            report: APIReport to format
            
        Returns:
            Formatted string
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Return file extension for this format.
        
        Returns:
            File extension including dot (e.g., '.json')
        """
        pass

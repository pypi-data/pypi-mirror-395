"""
Base Reporter Classes
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime


@dataclass
class ReportConfig:
    """
    Configuration for report generation.
    
    Attributes:
        title: Report title.
        author: Report author.
        include_responses: Include full responses.
        include_charts: Include chart placeholders.
        max_response_length: Truncate responses at length.
    """
    
    title: str = "Evaluation Report"
    author: str = "PromptMachine"
    include_responses: bool = False
    include_charts: bool = True
    max_response_length: int = 500


class Reporter(ABC):
    """
    Abstract base class for report generators.
    """
    
    def __init__(self, config: Optional[ReportConfig] = None) -> None:
        self.config = config or ReportConfig()
    
    @abstractmethod
    def generate(self, data: dict[str, Any]) -> str:
        """
        Generate report content.
        
        Args:
            data: Report data (rankings, battles, etc.)
            
        Returns:
            Formatted report string.
        """
        pass
    
    def save(self, content: str, filepath: str) -> None:
        """Save report to file."""
        with open(filepath, "w") as f:
            f.write(content)


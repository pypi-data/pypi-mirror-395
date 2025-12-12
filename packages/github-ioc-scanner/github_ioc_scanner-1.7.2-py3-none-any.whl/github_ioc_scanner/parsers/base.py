"""Base parser interface for package managers."""

from abc import ABC, abstractmethod
from typing import List

from ..models import PackageDependency


class PackageParser(ABC):
    """Abstract base class for package manager parsers."""
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """
        Check if this parser can handle the given file path.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if this parser can handle the file, False otherwise
        """
        pass
    
    @abstractmethod
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse the file content and extract package dependencies.
        
        Args:
            content: Raw file content as string
            
        Returns:
            List of PackageDependency objects found in the file
            
        Raises:
            ValueError: If the file content is malformed or cannot be parsed
        """
        pass
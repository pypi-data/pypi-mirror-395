"""Package parser factory with pattern-based registration."""

import re
from typing import Dict, List, Optional, Type

from ..exceptions import UnsupportedFileFormatError, ParsingError, wrap_exception
from ..logging_config import get_logger, log_exception
from .base import PackageParser

logger = get_logger(__name__)


class PackageParserFactory:
    """Factory for creating package parsers based on file patterns."""
    
    def __init__(self):
        """Initialize the factory with an empty parser registry."""
        self._parsers: Dict[str, Type[PackageParser]] = {}
        self._compiled_patterns: Dict[str, re.Pattern] = {}
    
    def register_parser(self, pattern: str, parser_class: Type[PackageParser]) -> None:
        """
        Register a parser class for files matching the given pattern.
        
        Args:
            pattern: Regular expression pattern to match file paths
            parser_class: Parser class that implements PackageParser interface
            
        Raises:
            ValueError: If pattern is invalid or parser_class doesn't implement PackageParser
        """
        if not issubclass(parser_class, PackageParser):
            raise ValueError(f"Parser class {parser_class.__name__} must inherit from PackageParser")
        
        try:
            compiled_pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        
        self._parsers[pattern] = parser_class
        self._compiled_patterns[pattern] = compiled_pattern
    
    def get_parser(self, file_path: str) -> Optional[PackageParser]:
        """
        Get a parser instance for the given file path.
        
        Args:
            file_path: Path to the file that needs parsing
            
        Returns:
            Parser instance if a matching parser is found, None otherwise
        """
        try:
            for pattern, parser_class in self._parsers.items():
                try:
                    if self._compiled_patterns[pattern].search(file_path):
                        parser_instance = parser_class()
                        # Double-check with the parser's own can_parse method
                        if parser_instance.can_parse(file_path):
                            logger.debug(f"Found parser {parser_class.__name__} for {file_path}")
                            return parser_instance
                except Exception as e:
                    logger.warning(f"Error checking parser {parser_class.__name__} for {file_path}: {e}")
                    continue
            
            # Log when no parser is found for better debugging
            filename = file_path.split('/')[-1] if '/' in file_path else file_path
            logger.debug(f"No parser found for file: {filename}")
            return None
            
        except Exception as e:
            log_exception(logger, f"Unexpected error finding parser for {file_path}", e)
            return None
    
    def get_supported_patterns(self) -> List[str]:
        """
        Get list of all registered file patterns.
        
        Returns:
            List of regex patterns that have registered parsers
        """
        return list(self._parsers.keys())
    
    def clear_parsers(self) -> None:
        """Clear all registered parsers. Mainly useful for testing."""
        self._parsers.clear()
        self._compiled_patterns.clear()


# Global factory instance
_factory_instance: Optional[PackageParserFactory] = None


def get_parser_factory() -> PackageParserFactory:
    """
    Get the global parser factory instance.
    
    Returns:
        Singleton PackageParserFactory instance
    """
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = PackageParserFactory()
    return _factory_instance


def register_parser(pattern: str, parser_class: Type[PackageParser]) -> None:
    """
    Convenience function to register a parser with the global factory.
    
    Args:
        pattern: Regular expression pattern to match file paths
        parser_class: Parser class that implements PackageParser interface
    """
    get_parser_factory().register_parser(pattern, parser_class)


def get_parser(file_path: str) -> Optional[PackageParser]:
    """
    Convenience function to get a parser from the global factory.
    
    Args:
        file_path: Path to the file that needs parsing
        
    Returns:
        Parser instance if a matching parser is found, None otherwise
    """
    try:
        return get_parser_factory().get_parser(file_path)
    except Exception as e:
        log_exception(logger, f"Error getting parser for {file_path}", e)
        return None


def parse_file_safely(file_path: str, content: str) -> List:
    """
    Safely parse a file with comprehensive error handling.
    
    Args:
        file_path: Path to the file being parsed
        content: File content to parse
        
    Returns:
        List of PackageDependency objects, empty list if parsing fails
        
    Raises:
        UnsupportedFileFormatError: If no parser is available for the file
        ParsingError: If parsing fails due to malformed content
    """
    try:
        parser = get_parser(file_path)
        if parser is None:
            filename = file_path.split('/')[-1] if '/' in file_path else file_path
            logger.warning(f"No parser available for file format: {filename}")
            raise UnsupportedFileFormatError(file_path)
        
        try:
            packages = parser.parse(content)
            logger.debug(f"Successfully parsed {len(packages)} packages from {file_path}")
            return packages
            
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            raise ParsingError(f"Failed to parse file content: {e}", file_path, cause=e)
            
    except (UnsupportedFileFormatError, ParsingError):
        raise
    except Exception as e:
        log_exception(logger, f"Unexpected error parsing {file_path}", e)
        raise wrap_exception(e, f"Unexpected error parsing {file_path}", ParsingError)
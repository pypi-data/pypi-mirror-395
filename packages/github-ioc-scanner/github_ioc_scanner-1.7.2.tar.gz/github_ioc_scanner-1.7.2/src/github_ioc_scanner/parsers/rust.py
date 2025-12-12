"""Rust package manager parsers."""

# Handle tomllib import for different Python versions
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python versions
    except ImportError:
        tomllib = None

from typing import List, Dict, Any

from .base import PackageParser
from ..models import PackageDependency


class CargoLockParser(PackageParser):
    """Parser for Cargo.lock files (Rust lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle Cargo.lock files."""
        return file_path.endswith('Cargo.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse Cargo.lock content and extract crate dependencies.
        
        Cargo.lock format (TOML):
        version = 3
        
        [[package]]
        name = "serde"
        version = "1.0.147"
        source = "registry+https://github.com/rust-lang/crates.io-index"
        checksum = "d193d69bae983fc11a79df82342761dfbf28a99fc8d203dca4c3c1b590948965"
        
        [[package]]
        name = "tokio"
        version = "1.21.2"
        source = "registry+https://github.com/rust-lang/crates.io-index"
        checksum = "a9e03c497dc955702ba729190dc4aac6f2a0ce97f913e5b1b5912fc5039d9099"
        dependencies = [
            "bytes",
            "libc",
            "memchr",
            "mio",
            "num_cpus",
            "once_cell",
            "parking_lot",
            "pin-project-lite",
            "signal-hook-registry",
            "socket2",
            "tokio-macros",
            "winapi",
        ]
        
        Args:
            content: Raw Cargo.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If TOML is malformed or invalid
        """
        if tomllib is None:
            raise ValueError("TOML parsing not available. Install 'tomli' package for Python < 3.11")
        
        try:
            data = tomllib.loads(content)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Invalid TOML in Cargo.lock: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("Cargo.lock must contain a TOML object")
        
        dependencies = []
        
        # Parse package sections
        if 'package' in data and isinstance(data['package'], list):
            for package_info in data['package']:
                if not isinstance(package_info, dict):
                    continue
                
                package_name = package_info.get('name')
                version = package_info.get('version')
                
                if package_name and version:
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=version,
                        dependency_type='dependencies'
                    ))
        
        return dependencies
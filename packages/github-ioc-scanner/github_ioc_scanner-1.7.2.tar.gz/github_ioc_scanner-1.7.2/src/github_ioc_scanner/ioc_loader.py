"""IOC (Indicators of Compromise) loader for scanning Python files in issues directory."""

import hashlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

from .exceptions import (
    IOCLoaderError,
    IOCDirectoryNotFoundError,
    IOCFileError,
    wrap_exception,
    get_error_context
)
from .logging_config import get_logger, log_exception
from .models import IOCDefinition

logger = get_logger(__name__)


class IOCLoader:
    """Loads IOC definitions from Python files in the issues directory."""
    
    def __init__(self, issues_dir: Optional[str] = None):
        """Initialize the IOC loader.
        
        Args:
            issues_dir: Path to the directory containing IOC definition files.
                       If None, uses the built-in IOC definitions from the package.
        """
        if issues_dir is None:
            # Use built-in IOC definitions from the package
            import github_ioc_scanner
            package_dir = Path(github_ioc_scanner.__file__).parent
            self.issues_dir = package_dir / "issues"
        else:
            self.issues_dir = Path(issues_dir)
        
        self._ioc_definitions: Dict[str, IOCDefinition] = {}
        self._ioc_hash: Optional[str] = None
    
    def load_iocs(self) -> Dict[str, IOCDefinition]:
        """Load all IOC definitions from Python files in the issues directory.
        
        Returns:
            Dictionary mapping source file names to IOCDefinition objects
            
        Raises:
            IOCDirectoryNotFoundError: If the issues directory doesn't exist
            IOCLoaderError: If no IOC files are found in the directory
        """
        try:
            if not self.issues_dir.exists():
                raise IOCDirectoryNotFoundError(str(self.issues_dir))
            
            if not self.issues_dir.is_dir():
                raise IOCDirectoryNotFoundError(str(self.issues_dir))
            
            # Find all Python files in the issues directory
            try:
                python_files = list(self.issues_dir.glob("*.py"))
            except (OSError, PermissionError) as e:
                raise IOCLoaderError(
                    f"Cannot access issues directory '{self.issues_dir}'",
                    cause=e
                )
            
            if not python_files:
                raise IOCLoaderError(
                    f"No Python files found in issues directory '{self.issues_dir}'"
                )
            
            self._ioc_definitions.clear()
            loaded_count = 0
            errors = []
            
            for py_file in python_files:
                try:
                    ioc_def = self._load_ioc_file(py_file)
                    if ioc_def:
                        self._ioc_definitions[py_file.name] = ioc_def
                        loaded_count += 1
                        logger.info(f"Loaded IOC definitions from {py_file.name}")
                except IOCFileError as e:
                    error_msg = f"Failed to load IOC file {py_file.name}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    # Continue with other files instead of failing completely
                    continue
                except Exception as e:
                    error_msg = f"Unexpected error loading IOC file {py_file.name}: {e}"
                    log_exception(logger, error_msg, e)
                    errors.append(error_msg)
                    continue
            
            if loaded_count == 0:
                error_details = "\n".join(errors) if errors else "No specific errors recorded"
                raise IOCLoaderError(
                    f"No valid IOC definitions found in any Python files in '{self.issues_dir}'. "
                    f"Errors encountered:\n{error_details}"
                )
            
            # Invalidate cached hash since definitions changed
            self._ioc_hash = None
            
            if errors:
                logger.warning(f"Successfully loaded IOC definitions from {loaded_count} files, "
                             f"but {len(errors)} files had errors")
            else:
                logger.info(f"Successfully loaded IOC definitions from {loaded_count} files")
            
            return self._ioc_definitions.copy()
            
        except (IOCDirectoryNotFoundError, IOCLoaderError):
            raise
        except Exception as e:
            log_exception(logger, f"Unexpected error loading IOC definitions from {self.issues_dir}", e)
            raise wrap_exception(e, f"Failed to load IOC definitions from {self.issues_dir}")
    
    def _load_ioc_file(self, file_path: Path) -> Optional[IOCDefinition]:
        """Load IOC definitions from a single Python file.
        
        Args:
            file_path: Path to the Python file to load
            
        Returns:
            IOCDefinition object if successful, None if no IOC_PACKAGES found
            
        Raises:
            IOCFileError: If the file cannot be loaded or parsed
        """
        try:
            # Check file accessibility
            if not file_path.exists():
                raise IOCFileError(f"File does not exist: {file_path.name}", source_file=str(file_path))
            
            if not file_path.is_file():
                raise IOCFileError(f"Path is not a file: {file_path.name}", source_file=str(file_path))
            
            try:
                # Load the Python module dynamically
                spec = importlib.util.spec_from_file_location(
                    f"ioc_{file_path.stem}", file_path
                )
                if spec is None or spec.loader is None:
                    raise IOCFileError(f"Cannot create module spec for {file_path.name}", source_file=str(file_path))
                
                module = importlib.util.module_from_spec(spec)
                
                # Execute the module to load its contents
                spec.loader.exec_module(module)
                
            except (ImportError, SyntaxError, NameError) as e:
                raise IOCFileError(
                    f"Python syntax or import error in {file_path.name}: {e}",
                    source_file=str(file_path),
                    cause=e
                )
            except Exception as e:
                raise IOCFileError(
                    f"Failed to execute Python file {file_path.name}: {e}",
                    source_file=str(file_path),
                    cause=e
                )
            
            # Check if IOC_PACKAGES exists in the module
            if not hasattr(module, 'IOC_PACKAGES'):
                logger.debug(f"No IOC_PACKAGES found in {file_path.name} (expected for __init__.py)")
                return None
            
            ioc_packages = getattr(module, 'IOC_PACKAGES')
            
            # Validate and normalize the IOC_PACKAGES structure
            try:
                validated_packages = self._validate_ioc_packages(ioc_packages, file_path.name)
            except IOCFileError:
                raise
            except Exception as e:
                raise IOCFileError(
                    f"Validation error in {file_path.name}: {e}",
                    source_file=str(file_path),
                    cause=e
                )
            
            # Check for Maven IOC packages (optional)
            validated_maven_packages = None
            if hasattr(module, 'MAVEN_IOC_PACKAGES'):
                maven_ioc_packages = getattr(module, 'MAVEN_IOC_PACKAGES')
                if maven_ioc_packages:  # Only validate if not empty
                    try:
                        validated_maven_packages = self._validate_ioc_packages(
                            maven_ioc_packages, file_path.name, package_type="Maven"
                        )
                        logger.info(f"Loaded {len(validated_maven_packages)} Maven IOC packages from {file_path.name}")
                    except IOCFileError:
                        raise
                    except Exception as e:
                        raise IOCFileError(
                            f"Maven IOC validation error in {file_path.name}: {e}",
                            source_file=str(file_path),
                            cause=e
                        )
            
            return IOCDefinition(
                packages=validated_packages,
                source_file=str(file_path),
                maven_packages=validated_maven_packages
            )
            
        except IOCFileError:
            raise
        except Exception as e:
            log_exception(logger, f"Unexpected error loading IOC file {file_path.name}", e)
            raise IOCFileError(
                f"Unexpected error loading {file_path.name}: {e}",
                source_file=str(file_path),
                cause=e
            )
    
    def _validate_ioc_packages(self, ioc_packages: object, source_file: str, package_type: str = "npm") -> Dict[str, Optional[Set[str]]]:
        """Validate and normalize IOC_PACKAGES dictionary structure.
        
        Args:
            ioc_packages: The IOC_PACKAGES object from the loaded module
            source_file: Name of the source file for error reporting
            package_type: Type of packages being validated ("npm" or "Maven")
            
        Returns:
            Validated and normalized packages dictionary
            
        Raises:
            IOCFileError: If the structure is invalid
        """
        type_label = f"{package_type} IOC_PACKAGES" if package_type != "npm" else "IOC_PACKAGES"
        
        if not isinstance(ioc_packages, dict):
            raise IOCFileError(
                f"{type_label} in {source_file} must be a dictionary, got {type(ioc_packages)}"
            )
        
        if not ioc_packages:
            raise IOCFileError(f"{type_label} in {source_file} is empty")
        
        validated_packages: Dict[str, Optional[Set[str]]] = {}
        
        for package_name, versions in ioc_packages.items():
            # Validate package name
            if not isinstance(package_name, str):
                raise IOCFileError(
                    f"Package name in {source_file} must be a string, got {type(package_name)}"
                )
            
            if not package_name.strip():
                raise IOCFileError(f"Empty package name found in {source_file}")
            
            package_name = package_name.strip()
            
            # Validate versions
            if versions is None:
                # None means any version is compromised
                validated_packages[package_name] = None
            elif isinstance(versions, (list, tuple, set)):
                # Convert to set of strings
                version_set = set()
                for version in versions:
                    if not isinstance(version, str):
                        raise IOCFileError(
                            f"Version for package '{package_name}' in {source_file} "
                            f"must be a string, got {type(version)}"
                        )
                    version = version.strip()
                    if not version:
                        raise IOCFileError(
                            f"Empty version found for package '{package_name}' in {source_file}"
                        )
                    version_set.add(version)
                
                if not version_set:
                    raise IOCFileError(
                        f"No valid versions found for package '{package_name}' in {source_file}"
                    )
                
                validated_packages[package_name] = version_set
            else:
                raise IOCFileError(
                    f"Versions for package '{package_name}' in {source_file} "
                    f"must be None, list, tuple, or set, got {type(versions)}"
                )
        
        return validated_packages
    
    def get_ioc_hash(self) -> str:
        """Generate a hash of all loaded IOC definitions for cache invalidation.
        
        Returns:
            SHA-256 hash of all IOC definitions
            
        Raises:
            IOCLoaderError: If no IOC definitions are loaded
        """
        if not self._ioc_definitions:
            raise IOCLoaderError("No IOC definitions loaded. Call load_iocs() first.")
        
        if self._ioc_hash is None:
            self._ioc_hash = self._calculate_ioc_hash()
        
        return self._ioc_hash
    
    def _calculate_ioc_hash(self) -> str:
        """Calculate SHA-256 hash of all IOC definitions.
        
        Returns:
            Hexadecimal SHA-256 hash string
        """
        hasher = hashlib.sha256()
        
        # Sort by source file name for consistent hashing
        for source_file in sorted(self._ioc_definitions.keys()):
            ioc_def = self._ioc_definitions[source_file]
            
            # Add source file name to hash
            hasher.update(source_file.encode('utf-8'))
            
            # Sort npm packages by name for consistent hashing
            for package_name in sorted(ioc_def.packages.keys()):
                versions = ioc_def.packages[package_name]
                
                # Add package name to hash
                hasher.update(package_name.encode('utf-8'))
                
                # Add versions to hash
                if versions is None:
                    hasher.update(b'__ANY_VERSION__')
                else:
                    # Sort versions for consistent hashing
                    for version in sorted(versions):
                        hasher.update(version.encode('utf-8'))
            
            # Include Maven packages in hash calculation
            if ioc_def.maven_packages:
                hasher.update(b'__MAVEN_PACKAGES__')
                for package_name in sorted(ioc_def.maven_packages.keys()):
                    versions = ioc_def.maven_packages[package_name]
                    hasher.update(package_name.encode('utf-8'))
                    if versions is None:
                        hasher.update(b'__ANY_VERSION__')
                    else:
                        for version in sorted(versions):
                            hasher.update(version.encode('utf-8'))
        
        return hasher.hexdigest()
    
    def get_all_packages(self) -> Dict[str, Optional[Set[str]]]:
        """Get all npm IOC packages merged from all loaded definitions.
        
        Returns:
            Dictionary mapping package names to version sets (or None for any version)
            
        Raises:
            IOCLoaderError: If no IOC definitions are loaded
        """
        if not self._ioc_definitions:
            raise IOCLoaderError("No IOC definitions loaded. Call load_iocs() first.")
        
        merged_packages: Dict[str, Optional[Set[str]]] = {}
        
        for ioc_def in self._ioc_definitions.values():
            for package_name, versions in ioc_def.packages.items():
                if package_name in merged_packages:
                    existing_versions = merged_packages[package_name]
                    
                    # If either definition says "any version", use None
                    if existing_versions is None or versions is None:
                        merged_packages[package_name] = None
                    else:
                        # Merge version sets
                        merged_packages[package_name] = existing_versions.union(versions)
                else:
                    merged_packages[package_name] = versions
        
        return merged_packages
    
    def get_all_maven_packages(self) -> Dict[str, Optional[Set[str]]]:
        """Get all Maven IOC packages merged from all loaded definitions.
        
        Returns:
            Dictionary mapping "groupId:artifactId" to version sets (or None for any version)
            
        Raises:
            IOCLoaderError: If no IOC definitions are loaded
        """
        if not self._ioc_definitions:
            raise IOCLoaderError("No IOC definitions loaded. Call load_iocs() first.")
        
        merged_packages: Dict[str, Optional[Set[str]]] = {}
        
        for ioc_def in self._ioc_definitions.values():
            if not ioc_def.maven_packages:
                continue
                
            for package_name, versions in ioc_def.maven_packages.items():
                if package_name in merged_packages:
                    existing_versions = merged_packages[package_name]
                    
                    # If either definition says "any version", use None
                    if existing_versions is None or versions is None:
                        merged_packages[package_name] = None
                    else:
                        # Merge version sets
                        merged_packages[package_name] = existing_versions.union(versions)
                else:
                    merged_packages[package_name] = versions
        
        return merged_packages
    
    def get_ioc_statistics(self) -> Dict[str, int]:
        """Get statistics about loaded IOC definitions.
        
        Returns:
            Dictionary with counts of npm packages, Maven packages, and total
            
        Raises:
            IOCLoaderError: If no IOC definitions are loaded
        """
        if not self._ioc_definitions:
            raise IOCLoaderError("No IOC definitions loaded. Call load_iocs() first.")
        
        npm_packages = self.get_all_packages()
        maven_packages = self.get_all_maven_packages()
        
        return {
            "npm_packages": len(npm_packages),
            "maven_packages": len(maven_packages),
            "total_packages": len(npm_packages) + len(maven_packages),
            "source_files": len(self._ioc_definitions)
        }
    
    def is_package_compromised(self, package_name: str, version: str, package_type: str = "npm") -> bool:
        """Check if a specific package version is compromised.
        
        Args:
            package_name: Name of the package to check (for Maven: "groupId:artifactId")
            version: Version of the package to check
            package_type: Type of package - "npm" or "maven"
            
        Returns:
            True if the package version is compromised, False otherwise
            
        Raises:
            IOCLoaderError: If no IOC definitions are loaded
        """
        if package_type.lower() == "maven":
            all_packages = self.get_all_maven_packages()
        else:
            all_packages = self.get_all_packages()
        
        if package_name not in all_packages:
            return False
        
        compromised_versions = all_packages[package_name]
        
        # None means any version is compromised
        if compromised_versions is None:
            return True
        
        # Check if the specific version is in the compromised set
        return version in compromised_versions
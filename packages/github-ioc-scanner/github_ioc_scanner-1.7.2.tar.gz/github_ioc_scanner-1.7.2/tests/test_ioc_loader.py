"""Tests for the IOC loader module."""

import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.github_ioc_scanner.ioc_loader import (
    IOCDirectoryNotFoundError,
    IOCFileError,
    IOCLoader,
    IOCLoaderError,
)
from src.github_ioc_scanner.models import IOCDefinition


class TestIOCLoader(unittest.TestCase):
    """Test cases for IOCLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.issues_dir = Path(self.temp_dir) / "issues"
        self.issues_dir.mkdir()
        
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_ioc_file(self, filename: str, content: str) -> Path:
        """Create an IOC file with the given content."""
        file_path = self.issues_dir / filename
        file_path.write_text(content)
        return file_path
    
    def test_load_iocs_success(self):
        """Test successful loading of IOC definitions."""
        # Create test IOC files
        self.create_ioc_file("test1.py", '''
IOC_PACKAGES = {
    "malicious-pkg": ["1.0.0", "1.0.1"],
    "bad-pkg": None,
}
''')
        
        self.create_ioc_file("test2.py", '''
IOC_PACKAGES = {
    "another-bad-pkg": ["2.0.0"],
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        definitions = loader.load_iocs()
        
        self.assertEqual(len(definitions), 2)
        self.assertIn("test1.py", definitions)
        self.assertIn("test2.py", definitions)
        
        # Check test1.py definitions
        test1_def = definitions["test1.py"]
        self.assertIsInstance(test1_def, IOCDefinition)
        self.assertEqual(len(test1_def.packages), 2)
        self.assertEqual(test1_def.packages["malicious-pkg"], {"1.0.0", "1.0.1"})
        self.assertIsNone(test1_def.packages["bad-pkg"])
        
        # Check test2.py definitions
        test2_def = definitions["test2.py"]
        self.assertEqual(len(test2_def.packages), 1)
        self.assertEqual(test2_def.packages["another-bad-pkg"], {"2.0.0"})
    
    def test_load_iocs_directory_not_found(self):
        """Test error when issues directory doesn't exist."""
        non_existent_dir = Path(self.temp_dir) / "nonexistent"
        loader = IOCLoader(str(non_existent_dir))
        
        with self.assertRaises(IOCDirectoryNotFoundError) as cm:
            loader.load_iocs()
        
        self.assertIn("does not exist", str(cm.exception))
    
    def test_load_iocs_path_is_file(self):
        """Test error when issues path is a file, not directory."""
        file_path = Path(self.temp_dir) / "not_a_dir.txt"
        file_path.write_text("test")
        
        loader = IOCLoader(str(file_path))
        
        with self.assertRaises(IOCDirectoryNotFoundError) as cm:
            loader.load_iocs()
        
        self.assertIn("is not a directory", str(cm.exception))
    
    def test_load_iocs_no_python_files(self):
        """Test error when no Python files are found."""
        # Create a non-Python file
        (self.issues_dir / "readme.txt").write_text("Not a Python file")
        
        loader = IOCLoader(str(self.issues_dir))
        
        with self.assertRaises(IOCLoaderError) as cm:
            loader.load_iocs()
        
        self.assertIn("No Python files found", str(cm.exception))
    
    def test_load_iocs_no_valid_definitions(self):
        """Test error when no valid IOC definitions are found."""
        # Create Python files without IOC_PACKAGES
        self.create_ioc_file("empty.py", "# Empty file")
        self.create_ioc_file("no_ioc.py", "OTHER_VAR = 'test'")
        
        loader = IOCLoader(str(self.issues_dir))
        
        with self.assertRaises(IOCLoaderError) as cm:
            loader.load_iocs()
        
        self.assertIn("No valid IOC definitions found", str(cm.exception))
    
    def test_load_iocs_malformed_file_continues(self):
        """Test that malformed files are skipped and loading continues."""
        # Create one good file and one bad file
        self.create_ioc_file("good.py", '''
IOC_PACKAGES = {
    "good-pkg": ["1.0.0"],
}
''')
        
        self.create_ioc_file("bad.py", '''
IOC_PACKAGES = "not a dict"
''')
        
        loader = IOCLoader(str(self.issues_dir))
        
        with patch('src.github_ioc_scanner.ioc_loader.logger') as mock_logger:
            definitions = loader.load_iocs()
        
        # Should load the good file and skip the bad one
        self.assertEqual(len(definitions), 1)
        self.assertIn("good.py", definitions)
        self.assertNotIn("bad.py", definitions)
        
        # Should log error for bad file
        mock_logger.error.assert_called()
    
    def test_validate_ioc_packages_valid_formats(self):
        """Test validation of various valid IOC_PACKAGES formats."""
        test_cases = [
            # List format
            '''IOC_PACKAGES = {"pkg": ["1.0.0", "1.0.1"]}''',
            # Tuple format
            '''IOC_PACKAGES = {"pkg": ("1.0.0", "1.0.1")}''',
            # Set format
            '''IOC_PACKAGES = {"pkg": {"1.0.0", "1.0.1"}}''',
            # None format (any version)
            '''IOC_PACKAGES = {"pkg": None}''',
            # Mixed formats
            '''IOC_PACKAGES = {"pkg1": ["1.0.0"], "pkg2": None}''',
        ]
        
        for i, content in enumerate(test_cases):
            with self.subTest(case=i):
                self.create_ioc_file(f"test{i}.py", content)
                loader = IOCLoader(str(self.issues_dir))
                definitions = loader.load_iocs()
                self.assertGreater(len(definitions), 0)
                # Clean up for next test
                (self.issues_dir / f"test{i}.py").unlink()
    
    def test_validate_ioc_packages_invalid_formats(self):
        """Test validation rejects invalid IOC_PACKAGES formats."""
        invalid_cases = [
            # Not a dictionary
            '''IOC_PACKAGES = "not a dict"''',
            # Empty dictionary
            '''IOC_PACKAGES = {}''',
            # Non-string package name
            '''IOC_PACKAGES = {123: ["1.0.0"]}''',
            # Empty package name
            '''IOC_PACKAGES = {"": ["1.0.0"]}''',
            # Invalid version type
            '''IOC_PACKAGES = {"pkg": [123]}''',
            # Empty version
            '''IOC_PACKAGES = {"pkg": [""]}''',
            # Invalid versions container
            '''IOC_PACKAGES = {"pkg": "1.0.0"}''',
        ]
        
        for i, content in enumerate(invalid_cases):
            with self.subTest(case=i):
                self.create_ioc_file(f"invalid{i}.py", content)
                loader = IOCLoader(str(self.issues_dir))
                
                with patch('src.github_ioc_scanner.ioc_loader.logger'):
                    with self.assertRaises(IOCLoaderError):
                        loader.load_iocs()
                
                # Clean up for next test
                (self.issues_dir / f"invalid{i}.py").unlink()
    
    def test_get_ioc_hash_consistency(self):
        """Test that IOC hash is consistent for same definitions."""
        self.create_ioc_file("test.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.0", "1.0.1"],
    "pkg2": None,
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        loader.load_iocs()
        
        hash1 = loader.get_ioc_hash()
        hash2 = loader.get_ioc_hash()
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)  # SHA-256 hex length
    
    def test_get_ioc_hash_changes_with_content(self):
        """Test that IOC hash changes when definitions change."""
        # Create initial file
        self.create_ioc_file("test.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.0"],
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        loader.load_iocs()
        hash1 = loader.get_ioc_hash()
        
        # Modify file
        self.create_ioc_file("test.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.0", "1.0.1"],
}
''')
        
        loader.load_iocs()  # Reload
        hash2 = loader.get_ioc_hash()
        
        self.assertNotEqual(hash1, hash2)
    
    def test_get_ioc_hash_no_definitions_loaded(self):
        """Test error when getting hash without loading definitions."""
        loader = IOCLoader(str(self.issues_dir))
        
        with self.assertRaises(IOCLoaderError) as cm:
            loader.get_ioc_hash()
        
        self.assertIn("No IOC definitions loaded", str(cm.exception))
    
    def test_get_all_packages_merge(self):
        """Test merging packages from multiple IOC files."""
        self.create_ioc_file("file1.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.0"],
    "pkg2": None,
}
''')
        
        self.create_ioc_file("file2.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.1"],  # Additional version for pkg1
    "pkg3": ["2.0.0"],
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        loader.load_iocs()
        
        all_packages = loader.get_all_packages()
        
        self.assertEqual(len(all_packages), 3)
        self.assertEqual(all_packages["pkg1"], {"1.0.0", "1.0.1"})  # Merged versions
        self.assertIsNone(all_packages["pkg2"])  # Any version
        self.assertEqual(all_packages["pkg3"], {"2.0.0"})
    
    def test_get_all_packages_any_version_override(self):
        """Test that None (any version) overrides specific versions."""
        self.create_ioc_file("file1.py", '''
IOC_PACKAGES = {
    "pkg1": ["1.0.0", "1.0.1"],
}
''')
        
        self.create_ioc_file("file2.py", '''
IOC_PACKAGES = {
    "pkg1": None,  # Any version - should override specific versions
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        loader.load_iocs()
        
        all_packages = loader.get_all_packages()
        
        self.assertIsNone(all_packages["pkg1"])  # Should be None (any version)
    
    def test_is_package_compromised(self):
        """Test package compromise checking."""
        self.create_ioc_file("test.py", '''
IOC_PACKAGES = {
    "specific-versions": ["1.0.0", "1.0.1"],
    "any-version": None,
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        loader.load_iocs()
        
        # Test specific versions
        self.assertTrue(loader.is_package_compromised("specific-versions", "1.0.0"))
        self.assertTrue(loader.is_package_compromised("specific-versions", "1.0.1"))
        self.assertFalse(loader.is_package_compromised("specific-versions", "1.0.2"))
        
        # Test any version
        self.assertTrue(loader.is_package_compromised("any-version", "1.0.0"))
        self.assertTrue(loader.is_package_compromised("any-version", "999.999.999"))
        
        # Test non-existent package
        self.assertFalse(loader.is_package_compromised("non-existent", "1.0.0"))
    
    def test_is_package_compromised_no_definitions(self):
        """Test error when checking compromise without loading definitions."""
        loader = IOCLoader(str(self.issues_dir))
        
        with self.assertRaises(IOCLoaderError):
            loader.is_package_compromised("pkg", "1.0.0")
    
    def test_file_with_syntax_error(self):
        """Test handling of Python files with syntax errors."""
        self.create_ioc_file("syntax_error.py", '''
IOC_PACKAGES = {
    "pkg": ["1.0.0"
    # Missing closing bracket - syntax error
''')
        
        self.create_ioc_file("good.py", '''
IOC_PACKAGES = {
    "good-pkg": ["1.0.0"],
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        
        with patch('src.github_ioc_scanner.ioc_loader.logger') as mock_logger:
            definitions = loader.load_iocs()
        
        # Should load the good file and skip the bad one
        self.assertEqual(len(definitions), 1)
        self.assertIn("good.py", definitions)
        
        # Should log error for syntax error file
        mock_logger.error.assert_called()
    
    def test_whitespace_handling(self):
        """Test that whitespace in package names and versions is handled correctly."""
        self.create_ioc_file("whitespace.py", '''
IOC_PACKAGES = {
    "  pkg-with-spaces  ": ["  1.0.0  ", "1.0.1"],
}
''')
        
        loader = IOCLoader(str(self.issues_dir))
        definitions = loader.load_iocs()
        
        # Should strip whitespace
        packages = definitions["whitespace.py"].packages
        self.assertIn("pkg-with-spaces", packages)
        self.assertEqual(packages["pkg-with-spaces"], {"1.0.0", "1.0.1"})


if __name__ == '__main__':
    unittest.main()
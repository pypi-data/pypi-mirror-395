"""Tests for CLI batch processing integration."""

import json
import os
import tempfile
import pytest
from unittest.mock import patch

from src.github_ioc_scanner.cli import CLIInterface
from src.github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from src.github_ioc_scanner.exceptions import ValidationError


class TestCLIBatchIntegration:
    """Test CLI integration with batch processing options."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
    
    def test_batch_size_argument(self):
        """Test --batch-size argument parsing."""
        args = ["--org", "testorg", "--batch-size", "25"]
        config = self.cli.parse_arguments(args)
        
        assert config.batch_size == 25
        assert self.cli.validate_arguments(config)
    
    def test_max_concurrent_argument(self):
        """Test --max-concurrent argument parsing."""
        args = ["--org", "testorg", "--max-concurrent", "15"]
        config = self.cli.parse_arguments(args)
        
        assert config.max_concurrent == 15
        assert self.cli.validate_arguments(config)
    
    def test_batch_strategy_argument(self):
        """Test --batch-strategy argument parsing."""
        args = ["--org", "testorg", "--batch-strategy", "aggressive"]
        config = self.cli.parse_arguments(args)
        
        assert config.batch_strategy == "aggressive"
        assert self.cli.validate_arguments(config)
    
    def test_enable_cross_repo_batching_argument(self):
        """Test --enable-cross-repo-batching argument parsing."""
        args = ["--org", "testorg", "--enable-cross-repo-batching"]
        config = self.cli.parse_arguments(args)
        
        assert config.enable_cross_repo_batching is True
        assert self.cli.validate_arguments(config)
    
    def test_disable_cross_repo_batching_argument(self):
        """Test --disable-cross-repo-batching argument parsing."""
        args = ["--org", "testorg", "--disable-cross-repo-batching"]
        config = self.cli.parse_arguments(args)
        
        assert config.enable_cross_repo_batching is False
        assert self.cli.validate_arguments(config)
    
    def test_batch_config_file_argument(self):
        """Test --batch-config argument parsing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"default_batch_size": 15}, f)
            config_file = f.name
        
        try:
            args = ["--org", "testorg", "--batch-config", config_file]
            config = self.cli.parse_arguments(args)
            
            assert config.batch_config_file == config_file
            assert self.cli.validate_arguments(config)
        finally:
            os.unlink(config_file)
    
    def test_all_batch_arguments_together(self):
        """Test all batch arguments used together."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"default_batch_size": 10}, f)
            config_file = f.name
        
        try:
            args = [
                "--org", "testorg",
                "--batch-size", "30",
                "--max-concurrent", "20",
                "--batch-strategy", "parallel",
                "--enable-cross-repo-batching",
                "--batch-config", config_file
            ]
            config = self.cli.parse_arguments(args)
            
            assert config.batch_size == 30
            assert config.max_concurrent == 20
            assert config.batch_strategy == "parallel"
            assert config.enable_cross_repo_batching is True
            assert config.batch_config_file == config_file
            assert self.cli.validate_arguments(config)
        finally:
            os.unlink(config_file)
    
    def test_batch_size_validation_too_small(self):
        """Test validation fails for batch size too small."""
        args = ["--org", "testorg", "--batch-size", "0"]
        config = self.cli.parse_arguments(args)
        
        assert not self.cli.validate_arguments(config)
    
    def test_batch_size_validation_too_large(self):
        """Test validation fails for batch size too large."""
        args = ["--org", "testorg", "--batch-size", "250"]
        config = self.cli.parse_arguments(args)
        
        assert not self.cli.validate_arguments(config)
    
    def test_max_concurrent_validation_too_small(self):
        """Test validation fails for max concurrent too small."""
        args = ["--org", "testorg", "--max-concurrent", "0"]
        config = self.cli.parse_arguments(args)
        
        assert not self.cli.validate_arguments(config)
    
    def test_max_concurrent_validation_too_large(self):
        """Test validation fails for max concurrent too large."""
        args = ["--org", "testorg", "--max-concurrent", "150"]
        config = self.cli.parse_arguments(args)
        
        assert not self.cli.validate_arguments(config)
    
    def test_invalid_batch_strategy(self):
        """Test validation fails for invalid batch strategy."""
        args = ["--org", "testorg", "--batch-strategy", "invalid"]
        
        # This should fail at argument parsing level
        with pytest.raises(SystemExit):
            self.cli.parse_arguments(args)
    
    def test_batch_config_file_not_exists(self):
        """Test validation fails for non-existent config file."""
        args = ["--org", "testorg", "--batch-config", "/nonexistent/file.json"]
        config = self.cli.parse_arguments(args)
        
        assert not self.cli.validate_arguments(config)
    
    def test_batch_config_file_invalid_extension(self):
        """Test validation fails for invalid config file extension."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("some content")
            config_file = f.name
        
        try:
            args = ["--org", "testorg", "--batch-config", config_file]
            config = self.cli.parse_arguments(args)
            
            assert not self.cli.validate_arguments(config)
        finally:
            os.unlink(config_file)


class TestBatchConfigFileLoading:
    """Test batch configuration file loading."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
    
    def test_load_json_config_file(self):
        """Test loading JSON configuration file."""
        config_data = {
            "max_concurrent_requests": 20,
            "default_batch_size": 25,
            "default_strategy": "aggressive",
            "enable_cross_repo_batching": True
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            loaded_config = self.cli.load_batch_config_from_file(config_file)
            
            assert loaded_config["max_concurrent_requests"] == 20
            assert loaded_config["default_batch_size"] == 25
            assert loaded_config["default_strategy"] == "aggressive"
            assert loaded_config["enable_cross_repo_batching"] is True
        finally:
            os.unlink(config_file)
    
    def test_load_yaml_config_file(self):
        """Test loading YAML configuration file."""
        yaml_content = """
max_concurrent_requests: 20
default_batch_size: 25
default_strategy: "aggressive"
enable_cross_repo_batching: true
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            config_file = f.name
        
        try:
            # Mock yaml import since it might not be available
            with patch('yaml.safe_load') as mock_yaml:
                mock_yaml.return_value = {
                    "max_concurrent_requests": 20,
                    "default_batch_size": 25,
                    "default_strategy": "aggressive",
                    "enable_cross_repo_batching": True
                }
                
                loaded_config = self.cli.load_batch_config_from_file(config_file)
                
                assert loaded_config["max_concurrent_requests"] == 20
                assert loaded_config["default_batch_size"] == 25
                assert loaded_config["default_strategy"] == "aggressive"
                assert loaded_config["enable_cross_repo_batching"] is True
        finally:
            os.unlink(config_file)
    
    def test_load_invalid_json_file(self):
        """Test loading invalid JSON file raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            config_file = f.name
        
        try:
            with pytest.raises(ValidationError, match="Invalid JSON"):
                self.cli.load_batch_config_from_file(config_file)
        finally:
            os.unlink(config_file)
    
    def test_load_non_dict_json_file(self):
        """Test loading JSON file that's not a dictionary raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(["not", "a", "dict"], f)
            config_file = f.name
        
        try:
            with pytest.raises(ValidationError, match="must contain a JSON object"):
                self.cli.load_batch_config_from_file(config_file)
        finally:
            os.unlink(config_file)
    
    def test_load_config_with_unknown_keys(self):
        """Test loading config with unknown keys logs warnings."""
        config_data = {
            "max_concurrent_requests": 20,
            "unknown_key": "unknown_value",
            "another_unknown": 123
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            with patch('src.github_ioc_scanner.cli.logger') as mock_logger:
                loaded_config = self.cli.load_batch_config_from_file(config_file)
                
                assert loaded_config["max_concurrent_requests"] == 20
                assert "unknown_key" in loaded_config
                mock_logger.warning.assert_called_once()
        finally:
            os.unlink(config_file)


class TestBatchConfigCreation:
    """Test BatchConfig creation from ScanConfig."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
    
    def test_create_batch_config_defaults(self):
        """Test creating BatchConfig with default values."""
        args = ["--org", "testorg"]
        scan_config = self.cli.parse_arguments(args)
        
        batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
        
        assert isinstance(batch_config, BatchConfig)
        assert batch_config.max_concurrent_requests == 10  # Default value
        assert batch_config.default_batch_size == 10  # Default value
        assert batch_config.default_strategy == BatchStrategy.ADAPTIVE
    
    def test_create_batch_config_with_cli_overrides(self):
        """Test creating BatchConfig with CLI argument overrides."""
        args = [
            "--org", "testorg",
            "--batch-size", "25",
            "--max-concurrent", "15",
            "--batch-strategy", "aggressive",
            "--enable-cross-repo-batching"
        ]
        scan_config = self.cli.parse_arguments(args)
        
        batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
        
        assert batch_config.default_batch_size == 25
        assert batch_config.max_batch_size >= 25  # Should be adjusted
        assert batch_config.max_concurrent_requests == 15
        assert batch_config.default_strategy == BatchStrategy.AGGRESSIVE
        assert batch_config.enable_cross_repo_batching is True
    
    def test_create_batch_config_with_file_config(self):
        """Test creating BatchConfig with file configuration."""
        config_data = {
            "max_concurrent_requests": 30,
            "default_batch_size": 40,
            "max_batch_size": 80,
            "default_strategy": "conservative",
            "enable_cross_repo_batching": False
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            args = ["--org", "testorg", "--batch-config", config_file]
            scan_config = self.cli.parse_arguments(args)
            
            batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
            
            assert batch_config.max_concurrent_requests == 30
            assert batch_config.default_batch_size == 40
            assert batch_config.max_batch_size == 80
            assert batch_config.default_strategy == BatchStrategy.CONSERVATIVE
            assert batch_config.enable_cross_repo_batching is False
        finally:
            os.unlink(config_file)
    
    def test_create_batch_config_cli_overrides_file(self):
        """Test that CLI arguments override file configuration."""
        config_data = {
            "max_concurrent_requests": 30,
            "default_batch_size": 40,
            "default_strategy": "conservative"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            args = [
                "--org", "testorg",
                "--batch-config", config_file,
                "--batch-size", "50",  # Override file config
                "--max-concurrent", "20",  # Override file config
                "--batch-strategy", "aggressive"  # Override file config
            ]
            scan_config = self.cli.parse_arguments(args)
            
            batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
            
            # CLI arguments should take precedence
            assert batch_config.default_batch_size == 50
            assert batch_config.max_concurrent_requests == 20
            assert batch_config.default_strategy == BatchStrategy.AGGRESSIVE
        finally:
            os.unlink(config_file)
    
    def test_create_batch_config_invalid_strategy_in_file(self):
        """Test handling invalid strategy in config file."""
        config_data = {
            "default_strategy": "invalid_strategy"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            args = ["--org", "testorg", "--batch-config", config_file]
            scan_config = self.cli.parse_arguments(args)
            
            with patch('src.github_ioc_scanner.cli.logger') as mock_logger:
                batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
                
                # Should use default strategy and log warning
                assert batch_config.default_strategy == BatchStrategy.ADAPTIVE
                mock_logger.warning.assert_called()
        finally:
            os.unlink(config_file)
    
    def test_create_batch_config_validation_error(self):
        """Test that validation errors are raised for invalid configuration."""
        args = ["--org", "testorg"]
        scan_config = self.cli.parse_arguments(args)
        
        # Force invalid values that will fail BatchConfig validation
        scan_config.max_concurrent = -1  # Invalid max concurrent
        
        with pytest.raises(ValidationError):
            self.cli.create_batch_config_from_scan_config(scan_config)
    
    def test_create_batch_config_file_load_error(self):
        """Test handling file load errors gracefully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            config_file = f.name
        
        try:
            args = ["--org", "testorg", "--batch-config", config_file]
            scan_config = self.cli.parse_arguments(args)
            
            with patch('src.github_ioc_scanner.cli.logger') as mock_logger:
                # Should continue with default config and log error
                batch_config = self.cli.create_batch_config_from_scan_config(scan_config)
                
                assert isinstance(batch_config, BatchConfig)
                mock_logger.error.assert_called()
        finally:
            os.unlink(config_file)
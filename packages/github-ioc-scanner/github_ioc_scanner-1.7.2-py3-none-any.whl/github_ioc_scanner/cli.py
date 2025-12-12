"""Command-line interface for the GitHub IOC Scanner."""

import argparse
import sys
import time
from datetime import datetime
from typing import List, Optional

from .exceptions import (
    GitHubIOCScannerError,
    ValidationError,
    format_error_message
)
from .logging_config import get_logger, setup_logging
from .models import IOCMatch, ScanConfig, CacheStats, ScanResults, WorkflowFinding, SecretFinding

logger = get_logger(__name__)


class CLIInterface:
    """Handles command-line argument parsing and output formatting."""

    def parse_arguments(self, args: Optional[List[str]] = None) -> ScanConfig:
        """Parse command-line arguments and return a ScanConfig.
        
        Args:
            args: Optional list of arguments to parse (for testing)
        """
        parser = argparse.ArgumentParser(
            prog="github-ioc-scan",
            description="Scan GitHub repositories for Indicators of Compromise (IOCs)",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Scan all repositories in an organization
  github-ioc-scan --org myorg

  # Scan repositories belonging to a specific team
  github-ioc-scan --org myorg --team security-team

  # Scan a specific repository
  github-ioc-scan --org myorg --repo myrepo

  # Fast scan (root-level files only)
  github-ioc-scan --org myorg --fast

  # Include archived repositories
  github-ioc-scan --org myorg --include-archived

  # Use custom IOC definitions directory
  github-ioc-scan --org myorg --issues-dir /path/to/iocs

  # Verbose mode with detailed logging
  github-ioc-scan --org myorg --verbose

  # Quiet mode (only show threats and errors)
  github-ioc-scan --org myorg --quiet

  # Custom log file location
  github-ioc-scan --org myorg --log-file /path/to/scan.log

  # Enable detailed rate limit debugging
  github-ioc-scan --org myorg --debug-rate-limits

  # Show full stack traces for all errors
  github-ioc-scan --org myorg --show-stack-traces

  # Suppress rate limit user messages completely
  github-ioc-scan --org myorg --suppress-rate-limit-messages

Cache Management:
  # Display cache information
  github-ioc-scan --cache-info

  # Clear all cache data
  github-ioc-scan --clear-cache

  # Clear specific cache type
  github-ioc-scan --clear-cache-type file

  # Refresh cache for specific repository
  github-ioc-scan --refresh-repo myorg/myrepo

  # Clean up cache entries older than 30 days
  github-ioc-scan --cleanup-cache 30

Batch Processing:
  # Use custom batch size
  github-ioc-scan --org myorg --batch-size 20

  # Limit concurrent requests
  github-ioc-scan --org myorg --max-concurrent 5

  # Use aggressive batching strategy
  github-ioc-scan --org myorg --batch-strategy aggressive

  # Enable cross-repository batching
  github-ioc-scan --org myorg --enable-cross-repo-batching

  # Use batch configuration file
  github-ioc-scan --org myorg --batch-config batch-config.json

Security Scanning:
  # Enable GitHub Actions workflow security scanning
  github-ioc-scan --org myorg --scan-workflows

  # Enable secrets detection (AWS keys, GitHub tokens, etc.)
  github-ioc-scan --org myorg --scan-secrets

  # Enable both workflow and secrets scanning
  github-ioc-scan --org myorg --scan-workflows --scan-secrets

  # Disable Maven scanning (enabled by default)
  github-ioc-scan --org myorg --disable-maven

Scan Modes:
  Organization Mode: Scan all repositories in an organization
    Usage: --org ORGANIZATION [--include-archived]
    
  Team Mode: Scan repositories belonging to a specific team
    Usage: --org ORGANIZATION --team TEAM_NAME
    
  Repository Mode: Scan a specific repository
    Usage: --org ORGANIZATION --repo REPOSITORY_NAME

Authentication:
  Set GITHUB_TOKEN environment variable or use 'gh auth token' command
            """,
        )

        parser.add_argument(
            "--org",
            type=str,
            metavar="ORGANIZATION",
            help="GitHub organization name to scan (required)",
        )

        parser.add_argument(
            "--team",
            type=str,
            metavar="TEAM_NAME",
            help="GitHub team name to scan (requires --org)",
        )

        parser.add_argument(
            "--team-first-org",
            action="store_true",
            help="Team-first organization scan: scan all teams first, then remaining repos (requires --org)",
        )

        parser.add_argument(
            "--repo",
            type=str,
            metavar="REPOSITORY",
            help="Specific repository name to scan (requires --org)",
        )

        parser.add_argument(
            "--fast",
            action="store_true",
            help="Fast mode: only scan root-level lockfiles (faster but less comprehensive)",
        )

        parser.add_argument(
            "--include-archived",
            action="store_true",
            help="Include archived repositories in the scan (default: skip archived repos)",
        )

        parser.add_argument(
            "--issues-dir",
            type=str,
            default=None,
            metavar="DIRECTORY",
            help="Directory containing IOC definition files (default: built-in IOCs)",
        )

        # SBOM scanning options
        sbom_group = parser.add_argument_group("SBOM scanning")
        
        sbom_group.add_argument(
            "--enable-sbom",
            action="store_true",
            default=True,
            help="Enable SBOM (Software Bill of Materials) scanning (default: enabled)",
        )
        
        sbom_group.add_argument(
            "--disable-sbom",
            action="store_true",
            help="Disable SBOM scanning (scan only traditional lockfiles)",
        )
        
        sbom_group.add_argument(
            "--sbom-only",
            action="store_true",
            help="Scan only SBOM files (skip traditional lockfiles)",
        )

        # Authentication options
        auth_group = parser.add_argument_group("authentication")
        
        auth_group.add_argument(
            "--github-app-config",
            type=str,
            metavar="CONFIG_PATH",
            help="Path to GitHub App configuration file (enables GitHub App authentication)",
        )

        # Resume/checkpoint options
        resume_group = parser.add_argument_group("resume and checkpointing")
        
        resume_group.add_argument(
            "--resume",
            type=str,
            metavar="SCAN_ID",
            help="Resume a previous scan using its scan ID",
        )
        
        resume_group.add_argument(
            "--list-scans",
            action="store_true",
            help="List available scans that can be resumed",
        )
        
        resume_group.add_argument(
            "--save-state",
            action="store_true",
            default=True,
            help="Save scan state for resumability (default: enabled)",
        )
        
        resume_group.add_argument(
            "--no-save-state",
            action="store_true",
            help="Disable scan state saving",
        )

        # IOC management options
        ioc_group = parser.add_argument_group("IOC management")
        
        ioc_group.add_argument(
            "--update-iocs",
            action="store_true",
            help="Update Shai-Hulud IOC definitions from Wiz Research and exit",
        )

        # Cache management options
        cache_group = parser.add_argument_group("cache management")
        
        cache_group.add_argument(
            "--clear-cache",
            action="store_true",
            help="Clear all cached data before scanning",
        )

        cache_group.add_argument(
            "--clear-cache-type",
            type=str,
            choices=["file", "packages", "results", "repos", "etags"],
            metavar="TYPE",
            help="Clear specific type of cached data (file, packages, results, repos, etags)",
        )

        cache_group.add_argument(
            "--refresh-repo",
            type=str,
            metavar="REPOSITORY",
            help="Refresh cached data for specific repository (format: org/repo)",
        )

        cache_group.add_argument(
            "--cache-info",
            action="store_true",
            help="Display detailed cache information and exit",
        )

        cache_group.add_argument(
            "--cleanup-cache",
            type=int,
            metavar="DAYS",
            help="Remove cache entries older than specified days",
        )

        cache_group.add_argument(
            "--refresh-repos",
            action="store_true",
            help="Refresh repository list from GitHub (ignore cached repository list)",
        )

        # Output and logging options
        output_group = parser.add_argument_group("output and logging")
        
        output_group.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output (show detailed logging information)",
        )

        output_group.add_argument(
            "--log-file",
            type=str,
            metavar="FILE",
            help="Write detailed logs to specified file (default: github-ioc-scan.log)",
        )

        output_group.add_argument(
            "--quiet",
            action="store_true",
            help="Suppress all output except IOC matches and errors",
        )
        
        output_group.add_argument(
            "--debug-rate-limits",
            action="store_true",
            help="Enable detailed rate limit debugging information",
        )
        
        output_group.add_argument(
            "--show-stack-traces",
            action="store_true",
            help="Show full stack traces for all errors (overrides suppression)",
        )
        
        output_group.add_argument(
            "--suppress-rate-limit-messages",
            action="store_true",
            help="Completely suppress rate limit user messages",
        )

        # Batch processing options
        batch_group = parser.add_argument_group("batch processing")
        
        batch_group.add_argument(
            "--enable-batch-processing",
            action="store_true",
            help="Enable batch processing for improved performance (default: enabled)",
        )
        
        batch_group.add_argument(
            "--disable-batch-processing",
            action="store_true",
            help="Disable batch processing and use sequential processing",
        )
        
        batch_group.add_argument(
            "--batch-size",
            type=int,
            metavar="SIZE",
            help="Number of files to process in each batch (default: auto-calculated)",
        )

        batch_group.add_argument(
            "--max-concurrent",
            type=int,
            metavar="COUNT",
            help="Maximum number of concurrent requests (default: 10)",
        )

        batch_group.add_argument(
            "--batch-strategy",
            type=str,
            choices=["sequential", "parallel", "adaptive", "aggressive", "conservative"],
            metavar="STRATEGY",
            help="Batch processing strategy (default: adaptive)",
        )

        batch_group.add_argument(
            "--enable-cross-repo-batching",
            action="store_true",
            help="Enable cross-repository batching optimizations",
        )

        batch_group.add_argument(
            "--disable-cross-repo-batching",
            action="store_true",
            help="Disable cross-repository batching optimizations",
        )

        batch_group.add_argument(
            "--batch-config",
            type=str,
            metavar="FILE",
            help="Path to batch configuration file (JSON format)",
        )

        # Rate limiting options
        rate_limit_group = parser.add_argument_group("rate limiting")
        
        rate_limit_group.add_argument(
            "--rate-limit-strategy",
            type=str,
            choices=["conservative", "normal", "aggressive"],
            default="normal",
            help="Rate limiting strategy: conservative (prioritize avoiding limits), "
                 "normal (balanced approach), aggressive (maximize throughput)",
        )
        
        rate_limit_group.add_argument(
            "--disable-intelligent-rate-limiting",
            action="store_true",
            help="Disable intelligent rate limit prevention and budget distribution",
        )
        
        rate_limit_group.add_argument(
            "--rate-limit-safety-margin",
            type=int,
            default=50,
            metavar="N",
            help="Number of requests to keep in reserve (default: 50)",
        )

        # Security scanning options
        security_group = parser.add_argument_group("security scanning")
        
        security_group.add_argument(
            "--scan-workflows",
            action="store_true",
            help="Enable GitHub Actions workflow scanning for security issues (dangerous triggers, malicious runners)",
        )
        
        security_group.add_argument(
            "--no-scan-workflows",
            action="store_true",
            help="Disable GitHub Actions workflow scanning",
        )
        
        security_group.add_argument(
            "--scan-secrets",
            action="store_true",
            help="Enable secrets scanning to detect exfiltrated credentials (AWS keys, GitHub tokens, API keys)",
        )
        
        security_group.add_argument(
            "--no-scan-secrets",
            action="store_true",
            help="Disable secrets scanning",
        )
        
        security_group.add_argument(
            "--enable-maven",
            action="store_true",
            default=True,
            help="Enable Maven (pom.xml) scanning for Java dependencies (default: enabled)",
        )
        
        security_group.add_argument(
            "--disable-maven",
            action="store_true",
            help="Disable Maven (pom.xml) scanning",
        )

        # Parse arguments (use provided args for testing, otherwise parse from sys.argv)
        parsed_args = parser.parse_args(args)

        # Handle cross-repo batching flags
        enable_cross_repo = None
        if parsed_args.enable_cross_repo_batching:
            enable_cross_repo = True
        elif parsed_args.disable_cross_repo_batching:
            enable_cross_repo = False

        # Handle SBOM scanning options
        enable_sbom = True  # Default to enabled
        if parsed_args.disable_sbom:
            enable_sbom = False
        elif parsed_args.enable_sbom:
            enable_sbom = True

        # Handle security scanning options
        scan_workflows = False  # Default to disabled
        if parsed_args.scan_workflows:
            scan_workflows = True
        elif parsed_args.no_scan_workflows:
            scan_workflows = False
        
        scan_secrets = False  # Default to disabled
        if parsed_args.scan_secrets:
            scan_secrets = True
        elif parsed_args.no_scan_secrets:
            scan_secrets = False
        
        enable_maven = True  # Default to enabled
        if parsed_args.disable_maven:
            enable_maven = False
        elif parsed_args.enable_maven:
            enable_maven = True

        return ScanConfig(
            org=parsed_args.org,
            team=parsed_args.team,
            repo=parsed_args.repo,
            team_first_org=getattr(parsed_args, 'team_first_org', False),
            fast_mode=parsed_args.fast,
            include_archived=parsed_args.include_archived,
            issues_dir=parsed_args.issues_dir,
            enable_sbom=enable_sbom,
            disable_sbom=parsed_args.disable_sbom,
            sbom_only=getattr(parsed_args, 'sbom_only', False),
            github_app_config=getattr(parsed_args, 'github_app_config', None),
            resume=getattr(parsed_args, 'resume', None),
            list_scans=getattr(parsed_args, 'list_scans', False),
            save_state=not getattr(parsed_args, 'no_save_state', False),
            no_save_state=getattr(parsed_args, 'no_save_state', False),
            update_iocs=getattr(parsed_args, 'update_iocs', False),
            clear_cache=parsed_args.clear_cache,
            clear_cache_type=parsed_args.clear_cache_type,
            refresh_repo=parsed_args.refresh_repo,
            cache_info=parsed_args.cache_info,
            cleanup_cache=parsed_args.cleanup_cache,
            use_repo_cache=not getattr(parsed_args, 'refresh_repos', False),
            verbose=getattr(parsed_args, 'verbose', False),
            log_file=getattr(parsed_args, 'log_file', None),
            quiet=getattr(parsed_args, 'quiet', False),
            debug_rate_limits=getattr(parsed_args, 'debug_rate_limits', False),
            show_stack_traces=getattr(parsed_args, 'show_stack_traces', False),
            suppress_rate_limit_messages=getattr(parsed_args, 'suppress_rate_limit_messages', False),
            enable_batch_processing=not getattr(parsed_args, 'disable_batch_processing', False),
            batch_size=getattr(parsed_args, 'batch_size', None),
            max_concurrent=getattr(parsed_args, 'max_concurrent', None),
            batch_strategy=getattr(parsed_args, 'batch_strategy', None),
            enable_cross_repo_batching=enable_cross_repo,
            batch_config_file=getattr(parsed_args, 'batch_config', None),
            rate_limit_strategy=getattr(parsed_args, 'rate_limit_strategy', 'normal'),
            enable_intelligent_rate_limiting=not getattr(parsed_args, 'disable_intelligent_rate_limiting', False),
            rate_limit_safety_margin=getattr(parsed_args, 'rate_limit_safety_margin', 50),
            scan_workflows=scan_workflows,
            scan_secrets=scan_secrets,
            enable_maven=enable_maven,
        )

    def validate_arguments(self, config: ScanConfig) -> bool:
        """Validate the parsed arguments and return True if valid.
        
        Prints detailed error messages for invalid configurations.
        
        Raises:
            ValidationError: If validation fails with specific field information
        """
        errors = []

        # Check if this is a cache-only, resume-only, or IOC-update operation
        is_cache_only = any([
            config.cache_info,
            config.clear_cache,
            config.clear_cache_type is not None,
            config.refresh_repo is not None,
            config.cleanup_cache is not None
        ])
        
        is_resume_only = any([
            config.list_scans,
            config.resume is not None
        ])
        
        is_ioc_update = config.update_iocs
        
        # Organization is required for all scan modes (but not cache-only, resume-only, or IOC-update operations)
        if not config.org and not is_cache_only and not is_resume_only and not is_ioc_update:
            errors.append(ValidationError("--org is required for all scan modes", field="org"))

        # Team requires organization
        if config.team and not config.org:
            errors.append(ValidationError("--team requires --org to be specified", field="team"))

        # Repository requires organization  
        if config.repo and not config.org:
            errors.append(ValidationError("--repo requires --org to be specified", field="repo"))

        # Team and repo are mutually exclusive
        if config.team and config.repo:
            errors.append(ValidationError("--team and --repo cannot be used together (choose one scan mode)", field="team"))

        # Team-first-org requires organization and is mutually exclusive with team/repo
        if config.team_first_org:
            if not config.org:
                errors.append(ValidationError("--team-first-org requires --org to be specified", field="team_first_org"))
            if config.team:
                errors.append(ValidationError("--team-first-org and --team cannot be used together", field="team_first_org"))
            if config.repo:
                errors.append(ValidationError("--team-first-org and --repo cannot be used together", field="team_first_org"))

        # Validate organization name format (basic validation)
        if config.org and not self._is_valid_github_name(config.org):
            errors.append(ValidationError(
                f"Invalid organization name '{config.org}' (must contain only alphanumeric characters, hyphens, and underscores)",
                field="org"
            ))

        # Validate team name format
        if config.team and not self._is_valid_github_name(config.team):
            errors.append(ValidationError(
                f"Invalid team name '{config.team}' (must contain only alphanumeric characters, hyphens, and underscores)",
                field="team"
            ))

        # Validate repository name format
        if config.repo and not self._is_valid_github_name(config.repo):
            errors.append(ValidationError(
                f"Invalid repository name '{config.repo}' (must contain only alphanumeric characters, hyphens, underscores, and dots)",
                field="repo"
            ))

        # Validate issues directory path
        if config.issues_dir and not config.issues_dir.strip():
            errors.append(ValidationError("Issues directory path cannot be empty", field="issues_dir"))

        if errors:
            self.display_error("Invalid arguments:")
            for error in errors:
                print(f"  - {error.message}", file=sys.stderr)
            print("\nUse --help for usage examples", file=sys.stderr)
            return False

        # Validate cache management arguments
        if not self.validate_cache_arguments(config):
            return False

        # Validate batch processing arguments
        if not self.validate_batch_arguments(config):
            return False

        # Validate security scanning arguments
        if not self.validate_security_arguments(config):
            return False

        return True

    def _is_valid_github_name(self, name: str) -> bool:
        """Validate GitHub organization/team/repository name format."""
        if not name:
            return False
        
        # Basic validation: alphanumeric, hyphens, underscores, dots
        # GitHub names can't start or end with hyphens
        if name.startswith('-') or name.endswith('-'):
            return False
            
        # Check for valid characters
        valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.')
        return all(c in valid_chars for c in name) and len(name) <= 100

    def validate_batch_arguments(self, config: ScanConfig) -> bool:
        """Validate batch processing arguments."""
        errors = []

        # Validate batch size
        if config.batch_size is not None:
            if config.batch_size < 1:
                errors.append(ValidationError("Batch size must be at least 1", field="batch_size"))
            elif config.batch_size > 200:
                errors.append(ValidationError("Batch size cannot exceed 200", field="batch_size"))

        # Validate max concurrent
        if config.max_concurrent is not None:
            if config.max_concurrent < 1:
                errors.append(ValidationError("Max concurrent requests must be at least 1", field="max_concurrent"))
            elif config.max_concurrent > 100:
                errors.append(ValidationError("Max concurrent requests cannot exceed 100", field="max_concurrent"))

        # Validate batch strategy
        valid_strategies = ["sequential", "parallel", "adaptive", "aggressive", "conservative"]
        if config.batch_strategy is not None and config.batch_strategy not in valid_strategies:
            errors.append(ValidationError(
                f"Invalid batch strategy '{config.batch_strategy}'. Must be one of: {', '.join(valid_strategies)}",
                field="batch_strategy"
            ))

        # Validate batch config file
        if config.batch_config_file is not None:
            import os
            if not os.path.isfile(config.batch_config_file):
                errors.append(ValidationError(
                    f"Batch configuration file '{config.batch_config_file}' does not exist",
                    field="batch_config_file"
                ))
            elif not config.batch_config_file.endswith(('.json', '.yaml', '.yml')):
                errors.append(ValidationError(
                    "Batch configuration file must be JSON or YAML format",
                    field="batch_config_file"
                ))

        if errors:
            self.display_error("Invalid batch processing arguments:")
            for error in errors:
                print(f"  - {error.message}", file=sys.stderr)
            return False

        return True

    def validate_security_arguments(self, config: ScanConfig) -> bool:
        """Validate security scanning arguments.
        
        Args:
            config: The parsed scan configuration
            
        Returns:
            True if validation passes, False otherwise
        """
        # No conflicting options to validate currently
        # Both scan_workflows and scan_secrets can be enabled simultaneously
        # enable_maven is independent of other options
        
        # Log info about enabled security features if verbose
        if config.verbose:
            enabled_features = []
            if config.scan_workflows:
                enabled_features.append("workflow scanning")
            if config.scan_secrets:
                enabled_features.append("secrets scanning")
            if config.enable_maven:
                enabled_features.append("Maven scanning")
            
            if enabled_features:
                logger.info(f"Security features enabled: {', '.join(enabled_features)}")
        
        return True

    def load_batch_config_from_file(self, config_file: str) -> dict:
        """Load batch configuration from a file.
        
        Args:
            config_file: Path to the configuration file (JSON or YAML)
            
        Returns:
            Dictionary containing batch configuration
            
        Raises:
            ValidationError: If the file cannot be loaded or is invalid
        """
        import json
        import os
        
        if not os.path.isfile(config_file):
            raise ValidationError(f"Configuration file '{config_file}' does not exist")
        
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.json'):
                    config_data = json.load(f)
                elif config_file.endswith(('.yaml', '.yml')):
                    try:
                        import yaml
                        config_data = yaml.safe_load(f)
                    except ImportError:
                        raise ValidationError("PyYAML is required to load YAML configuration files")
                else:
                    raise ValidationError("Configuration file must be JSON or YAML format")
            
            # Validate the configuration structure
            if not isinstance(config_data, dict):
                raise ValidationError("Configuration file must contain a JSON object or YAML mapping")
            
            # Validate known configuration keys
            valid_keys = {
                'max_concurrent_requests', 'max_concurrent_repos', 'default_batch_size',
                'max_batch_size', 'min_batch_size', 'rate_limit_buffer', 'retry_attempts',
                'retry_delay_base', 'max_memory_usage_mb', 'stream_large_files_threshold',
                'default_strategy', 'enable_cross_repo_batching', 'enable_file_prioritization',
                'enable_performance_monitoring', 'log_batch_metrics'
            }
            
            unknown_keys = set(config_data.keys()) - valid_keys
            if unknown_keys:
                logger.warning(f"Unknown configuration keys in {config_file}: {', '.join(unknown_keys)}")
            
            return config_data
            
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ValidationError(f"Error loading configuration file: {e}")

    def create_batch_config_from_scan_config(self, scan_config: ScanConfig) -> 'BatchConfig':
        """Create a BatchConfig from CLI arguments and optional config file.
        
        Args:
            scan_config: The parsed scan configuration
            
        Returns:
            BatchConfig instance with merged settings
        """
        from .batch_models import BatchConfig, BatchStrategy
        
        # Start with default configuration
        batch_config = BatchConfig()
        
        # Load from file if specified
        if scan_config.batch_config_file:
            try:
                file_config = self.load_batch_config_from_file(scan_config.batch_config_file)
                
                # Apply file configuration
                for key, value in file_config.items():
                    if hasattr(batch_config, key):
                        # Handle strategy enum conversion
                        if key == 'default_strategy' and isinstance(value, str):
                            try:
                                value = BatchStrategy(value.lower())
                            except ValueError:
                                logger.warning(f"Invalid strategy '{value}' in config file, using default")
                                continue
                        
                        setattr(batch_config, key, value)
                    else:
                        logger.warning(f"Unknown batch configuration key: {key}")
                        
            except ValidationError as e:
                logger.error(f"Failed to load batch configuration file: {e}")
                # Continue with default configuration
        
        # Override with CLI arguments (CLI takes precedence)
        if scan_config.batch_size is not None:
            batch_config.default_batch_size = scan_config.batch_size
            batch_config.max_batch_size = max(batch_config.max_batch_size, scan_config.batch_size)
        
        if scan_config.max_concurrent is not None:
            batch_config.max_concurrent_requests = scan_config.max_concurrent
        
        if scan_config.batch_strategy is not None:
            try:
                batch_config.default_strategy = BatchStrategy(scan_config.batch_strategy.lower())
            except ValueError:
                logger.warning(f"Invalid strategy '{scan_config.batch_strategy}', using default")
        
        if scan_config.enable_cross_repo_batching is not None:
            batch_config.enable_cross_repo_batching = scan_config.enable_cross_repo_batching
        
        # Validate the final configuration
        validation_errors = batch_config.validate()
        if validation_errors:
            error_msg = "Invalid batch configuration: " + "; ".join(validation_errors)
            raise ValidationError(error_msg)
        
        return batch_config

    def display_results(self, results: List[IOCMatch]) -> None:
        """Display scan results in the specified format: {org}/{repo} | {file} | {package} | {version}"""
        if not results:
            print("Keine Treffer gefunden.")
            return

        # Sort results for consistent output
        sorted_results = sorted(results, key=lambda x: (x.repo, x.file_path, x.package_name))
        
        for match in sorted_results:
            print(f"{match.repo} | {match.file_path} | {match.package_name} | {match.version}")

    def display_results_with_header(self, results: List[IOCMatch]) -> None:
        """Display scan results with a header for better readability."""
        if not results:
            print("Keine Treffer gefunden.")
            return

        print(f"Found {len(results)} IOC match{'es' if len(results) != 1 else ''}:")
        print("Repository | File | Package | Version")
        print("-" * 60)
        
        # Sort results for consistent output
        sorted_results = sorted(results, key=lambda x: (x.repo, x.file_path, x.package_name))
        
        for match in sorted_results:
            print(f"{match.repo} | {match.file_path} | {match.package_name} | {match.version}")

    def display_cache_stats(self, stats: CacheStats) -> None:
        """Display cache statistics with hits, misses, and time saved."""
        print(f"\nCache Statistics:")
        print(f"  Hits: {stats.hits}")
        print(f"  Misses: {stats.misses}")
        
        total_operations = stats.hits + stats.misses
        if total_operations > 0:
            hit_rate = (stats.hits / total_operations) * 100
            print(f"  Hit rate: {hit_rate:.1f}%")
            
        print(f"  Time saved: {stats.time_saved:.2f}s")
        print(f"  Cache size: {stats.cache_size} entries")
        
        # Add performance insight
        if stats.time_saved > 0:
            print(f"  Performance: Cache saved {stats.time_saved:.1f} seconds of API calls")
        elif total_operations > 0 and stats.hits == 0:
            print(f"  Performance: First scan - building cache for future runs")

    def display_error(self, message: str) -> None:
        """Display an error message to stderr."""
        print(f"Error: {message}", file=sys.stderr)

    def display_warning(self, message: str) -> None:
        """Display a warning message."""
        print(f"Warning: {message}", file=sys.stderr)

    def display_scan_summary(self, repositories_scanned: int, files_scanned: int) -> None:
        """Display a summary of the scan operation."""
        print(f"\nScan Summary:")
        print(f"  Repositories scanned: {repositories_scanned}")
        print(f"  Files scanned: {files_scanned}")

    def display_progress(self, message: str) -> None:
        """Display a progress message."""
        print(f"[INFO] {message}")

    def display_scan_start(self, config: ScanConfig) -> None:
        """Display scan start information."""
        if config.quiet:
            return
            
        if config.repo:
            print(f"🔍 Scanning repository: {config.org}/{config.repo}")
        elif config.team:
            print(f"🔍 Scanning team repositories: {config.org}/{config.team}")
        else:
            print(f"🔍 Scanning organization: {config.org}")
            
        scan_mode = []
        if config.fast_mode:
            scan_mode.append("fast mode")
        if config.include_archived:
            scan_mode.append("including archived")
        
        if scan_mode:
            print(f"📋 Scan mode: {', '.join(scan_mode)}")
        
        if config.verbose:
            print(f"📁 IOC definitions directory: {config.issues_dir}")
        print()

    def display_professional_scan_start(self, config: ScanConfig, total_iocs: int) -> None:
        """Display professional scan start information for security analysts."""
        if config.quiet:
            return
            
        print("=" * 60)
        print("GitHub IOC Scanner - Security Analysis Report")
        print("=" * 60)
        
        # Scan target
        if config.repo:
            print(f"Target: Repository {config.org}/{config.repo}")
        elif config.team:
            print(f"Target: Team '{config.team}' in organization '{config.org}'")
        else:
            print(f"Target: Organization '{config.org}'")
        
        # Scan configuration
        scan_config = []
        if config.fast_mode:
            scan_config.append("Fast mode (root-level files only)")
        else:
            scan_config.append("Comprehensive mode (all files)")
        
        if config.include_archived:
            scan_config.append("Including archived repositories")
        else:
            scan_config.append("Excluding archived repositories")
        
        print(f"Configuration: {', '.join(scan_config)}")
        
        # Show enabled security scans
        enabled_scans = ["Package IOC detection"]
        if config.scan_workflows:
            enabled_scans.append("Workflow security analysis")
        if config.scan_secrets:
            enabled_scans.append("Secrets detection")
        if config.enable_maven:
            enabled_scans.append("Maven/pom.xml support")
        
        print(f"Security scans: {', '.join(enabled_scans)}")
        print(f"IOC Database: {total_iocs:,} threat indicators loaded (incl. Heise-reported npm attacks)")
        print(f"Scan initiated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)

    def display_professional_results(self, results: List[IOCMatch], config: ScanConfig,
                                      workflow_findings: Optional[List[WorkflowFinding]] = None,
                                      secret_findings: Optional[List[SecretFinding]] = None) -> None:
        """Display results in a professional format for security analysts."""
        has_ioc_results = bool(results)
        has_workflow_findings = bool(workflow_findings)
        has_secret_findings = bool(secret_findings)
        
        if not has_ioc_results and not has_workflow_findings and not has_secret_findings:
            if not config.quiet:
                print("✅ SCAN COMPLETE - No threats detected")
                print("   All scanned packages are clean")
            return

        # Security alert header
        print("🚨 SECURITY ALERT - THREATS DETECTED")
        print("=" * 60)
        
        total_issues = len(results) if results else 0
        if workflow_findings:
            total_issues += len(workflow_findings)
        if secret_findings:
            total_issues += len(secret_findings)
        
        print(f"Found {total_issues} security issues:")
        print()

        # Display IOC matches
        if has_ioc_results:
            print("📦 COMPROMISED PACKAGES:")
            print("-" * 40)
            # Group results by repository for better readability
            repo_groups = {}
            for match in results:
                if match.repo not in repo_groups:
                    repo_groups[match.repo] = []
                repo_groups[match.repo].append(match)

            # Display results grouped by repository
            for repo, matches in sorted(repo_groups.items()):
                print(f"   Repository: {repo}")
                print(f"   Threats found: {len(matches)}")
                
                for match in sorted(matches, key=lambda x: (x.file_path, x.package_name)):
                    print(f"   ⚠️  {match.file_path} | {match.package_name} | {match.version}")
                print()

        # Display workflow findings
        if has_workflow_findings:
            print("🔧 WORKFLOW SECURITY ISSUES:")
            print("-" * 40)
            # Group by repository
            workflow_by_repo = {}
            for finding in workflow_findings:
                if finding.repo not in workflow_by_repo:
                    workflow_by_repo[finding.repo] = []
                workflow_by_repo[finding.repo].append(finding)
            
            for repo, findings in sorted(workflow_by_repo.items()):
                print(f"   Repository: {repo}")
                for finding in findings:
                    severity_icon = "🔴" if finding.severity == "critical" else "🟠" if finding.severity == "high" else "🟡"
                    print(f"   {severity_icon} [{finding.severity.upper()}] {finding.finding_type}")
                    print(f"      File: {finding.file_path}")
                    print(f"      {finding.description}")
                    if finding.recommendation:
                        print(f"      💡 {finding.recommendation}")
                print()

        # Display secret findings
        if has_secret_findings:
            print("🔑 EXPOSED SECRETS:")
            print("-" * 40)
            # Group by repository
            secrets_by_repo = {}
            for finding in secret_findings:
                if finding.repo not in secrets_by_repo:
                    secrets_by_repo[finding.repo] = []
                secrets_by_repo[finding.repo].append(finding)
            
            for repo, findings in sorted(secrets_by_repo.items()):
                print(f"   Repository: {repo}")
                for finding in findings:
                    severity_icon = "🔴" if finding.severity == "critical" else "🟠" if finding.severity == "high" else "🟡"
                    print(f"   {severity_icon} [{finding.severity.upper()}] {finding.secret_type}")
                    print(f"      File: {finding.file_path}:{finding.line_number}")
                    print(f"      Masked value: {finding.masked_value}")
                    if finding.recommendation:
                        print(f"      💡 {finding.recommendation}")
                print()

        # Summary
        print("-" * 60)
        summary_parts = []
        if has_ioc_results:
            summary_parts.append(f"{len(results)} compromised packages")
        if has_workflow_findings:
            summary_parts.append(f"{len(workflow_findings)} workflow issues")
        if has_secret_findings:
            summary_parts.append(f"{len(secret_findings)} exposed secrets")
        
        print(f"SUMMARY: {', '.join(summary_parts)}")
        print("ACTION REQUIRED: Review and remediate identified threats")

    def display_professional_summary(self, repos_scanned: int, files_scanned: int, 
                                   cache_stats: 'CacheStats', config: ScanConfig,
                                   workflow_findings: Optional[List[WorkflowFinding]] = None,
                                   secret_findings: Optional[List[SecretFinding]] = None) -> None:
        """Display professional scan summary."""
        if config.quiet:
            return
            
        print("-" * 60)
        print("SCAN STATISTICS:")
        print(f"  Repositories scanned: {repos_scanned:,}")
        print(f"  Files analyzed: {files_scanned:,}")
        
        # Show workflow and secrets scan statistics if enabled
        if config.scan_workflows:
            workflow_count = len(workflow_findings) if workflow_findings else 0
            print(f"  Workflow issues found: {workflow_count}")
        
        if config.scan_secrets:
            secrets_count = len(secret_findings) if secret_findings else 0
            print(f"  Secrets detected: {secrets_count}")
        
        if cache_stats.hits + cache_stats.misses > 0:
            hit_rate = (cache_stats.hits / (cache_stats.hits + cache_stats.misses)) * 100
            print(f"  Cache efficiency: {hit_rate:.1f}% ({cache_stats.hits:,} hits, {cache_stats.misses:,} misses)")
            
            if cache_stats.time_saved > 0:
                print(f"  Time saved by caching: {cache_stats.time_saved:.1f}s")
        
        print(f"Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    def display_progress(self, current: int, total: int, repo_name: str, config: ScanConfig, 
                        start_time: float = None) -> None:
        """Display scan progress for repositories."""
        if config.quiet:
            return
            
        # Calculate progress percentage
        percentage = (current / total) * 100 if total > 0 else 0
        
        # Create progress bar
        bar_length = 30  # Shorter bar to make room for ETA
        filled_length = int(bar_length * current // total) if total > 0 else 0
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Calculate ETA if start_time is provided
        eta_str = ""
        if start_time and current > 0:
            elapsed = time.time() - start_time
            avg_time_per_repo = elapsed / current
            remaining_repos = total - current
            eta_seconds = remaining_repos * avg_time_per_repo
            
            if eta_seconds > 60:
                eta_str = f" | ETA: {int(eta_seconds // 60)}m {int(eta_seconds % 60)}s"
            elif eta_seconds > 0:
                eta_str = f" | ETA: {int(eta_seconds)}s"
        
        # Display progress
        if config.verbose:
            print(f"[{current:3d}/{total:3d}] [{bar}] {percentage:5.1f}%{eta_str} | Scanning: {repo_name}")
        else:
            # Compact progress for normal mode
            repo_display = repo_name[:35] if len(repo_name) > 35 else repo_name
            print(f"\r[{current:3d}/{total:3d}] [{bar}] {percentage:5.1f}%{eta_str} | {repo_display:<35}", end='', flush=True)
    
    def clear_progress_line(self, config: ScanConfig) -> None:
        """Clear the progress line after completion."""
        if not config.quiet and not config.verbose:
            print("\r" + " " * 80 + "\r", end='', flush=True)

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format."""
        if seconds < 1:
            return f"{seconds * 1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.1f}s"

    def display_cache_info(self, cache_info: dict) -> None:
        """Display detailed cache information."""
        print("Cache Information:")
        print(f"  Location: {cache_info.get('cache_path', 'Unknown')}")
        print(f"  Database size: {self.format_file_size(cache_info.get('db_size_bytes', 0))}")
        print()
        
        print("Cache Contents:")
        print(f"  File content entries: {cache_info.get('file_cache', 0):,}")
        print(f"  Parsed packages entries: {cache_info.get('parsed_packages', 0):,}")
        print(f"  Scan results entries: {cache_info.get('scan_results', 0):,}")
        print(f"  Repository metadata entries: {cache_info.get('repo_metadata', 0):,}")
        print(f"  ETag entries: {cache_info.get('etag_cache', 0):,}")
        
        total_entries = sum([
            cache_info.get('file_cache', 0),
            cache_info.get('parsed_packages', 0),
            cache_info.get('scan_results', 0),
            cache_info.get('repo_metadata', 0),
            cache_info.get('etag_cache', 0)
        ])
        print(f"  Total entries: {total_entries:,}")
        
        # Display top repositories if available
        if 'top_repositories' in cache_info and cache_info['top_repositories']:
            print()
            print("Top Cached Repositories:")
            for repo_info in cache_info['top_repositories']:
                print(f"  {repo_info['repo']}: {repo_info['files']:,} files")
        
        # Display cache age information if available
        if 'cache_age' in cache_info:
            age_info = cache_info['cache_age']
            print()
            print("Cache Age:")
            if age_info.get('oldest_entry'):
                print(f"  Oldest entry: {age_info['oldest_entry']}")
            if age_info.get('newest_entry'):
                print(f"  Newest entry: {age_info['newest_entry']}")
            if age_info.get('average_age_days') is not None:
                print(f"  Average age: {age_info['average_age_days']:.1f} days")

    def display_cache_operation_result(self, operation: str, count: int = 0, cache_type: str = None) -> None:
        """Display the result of a cache operation."""
        if operation == "clear":
            if cache_type:
                print(f"Cleared {cache_type} cache")
            else:
                print("Cleared all cache data")
        elif operation == "refresh":
            print(f"Refreshed repository cache: removed {count:,} entries")
        elif operation == "cleanup":
            print(f"Cleaned up old cache entries: removed {count:,} entries")

    def validate_cache_arguments(self, config: ScanConfig) -> bool:
        """Validate cache management arguments."""
        errors = []
        
        # Validate refresh-repo format
        if config.refresh_repo:
            if '/' not in config.refresh_repo:
                errors.append(ValidationError(
                    f"Invalid repository format '{config.refresh_repo}' (expected: org/repo)",
                    field="refresh_repo"
                ))
            else:
                org, repo = config.refresh_repo.split('/', 1)
                if not self._is_valid_github_name(org) or not self._is_valid_github_name(repo):
                    errors.append(ValidationError(
                        f"Invalid repository name '{config.refresh_repo}'",
                        field="refresh_repo"
                    ))
        
        # Validate cleanup-cache value
        if config.cleanup_cache is not None:
            if config.cleanup_cache < 1:
                errors.append(ValidationError(
                    "Cleanup days must be a positive integer",
                    field="cleanup_cache"
                ))
        
        # Check for conflicting cache operations
        cache_operations = [
            config.clear_cache,
            config.clear_cache_type is not None,
            config.refresh_repo is not None,
            config.cache_info,
            config.cleanup_cache is not None
        ]
        
        if sum(cache_operations) > 1:
            errors.append(ValidationError(
                "Only one cache management operation can be specified at a time",
                field="cache"
            ))
        
        if errors:
            self.display_error("Invalid cache management arguments:")
            for error in errors:
                print(f"  - {error.message}", file=sys.stderr)
            return False
        
        return True


def main() -> None:
    """Main entry point for the CLI application."""
    try:
        cli = CLIInterface()
        config = cli.parse_arguments()
        
        if not cli.validate_arguments(config):
            sys.exit(1)
        
        # Configure logging based on user preferences
        log_file = config.log_file or "github-ioc-scan.log"
        
        # Determine logging configuration
        debug_rate_limits = config.debug_rate_limits
        suppress_stack_traces = not config.show_stack_traces
        separate_user_messages = not config.suppress_rate_limit_messages
        
        if config.verbose:
            # Verbose mode: show detailed logs on console
            setup_logging(
                level="INFO", 
                log_file=log_file,
                debug_rate_limits=debug_rate_limits,
                suppress_stack_traces=suppress_stack_traces,
                separate_user_messages=separate_user_messages
            )
        elif config.quiet:
            # Quiet mode: only critical errors on console, everything to file
            setup_logging(
                level="CRITICAL", 
                log_file=log_file,
                debug_rate_limits=debug_rate_limits,
                suppress_stack_traces=suppress_stack_traces,
                separate_user_messages=False  # No user messages in quiet mode
            )
            # Set file handler to capture all logs
            import logging
            file_logger = logging.getLogger()
            for handler in file_logger.handlers:
                if hasattr(handler, 'baseFilename'):  # FileHandler
                    handler.setLevel(logging.DEBUG)
        else:
            # Normal mode: minimal console output, detailed file logging
            setup_logging(
                level="ERROR", 
                log_file=log_file,
                debug_rate_limits=debug_rate_limits,
                suppress_stack_traces=suppress_stack_traces,
                separate_user_messages=separate_user_messages
            )
            # Set file handler to capture all logs
            import logging
            file_logger = logging.getLogger()
            for handler in file_logger.handlers:
                if hasattr(handler, 'baseFilename'):  # FileHandler
                    handler.setLevel(logging.INFO)
        
        # Import here to avoid circular imports
        from .cache import CacheManager
        from .github_client import GitHubClient
        from .ioc_loader import IOCLoader
        from .scanner import GitHubIOCScanner
        
        # Handle IOC update operation
        if config.update_iocs:
            if not config.quiet:
                print("=" * 60)
                print("Shai-Hulud IOC Auto-Update")
                print("=" * 60)
                print()
            
            try:
                import csv
                from datetime import datetime
                from pathlib import Path
                from urllib.request import urlopen
                
                # Download CSV
                url = "https://raw.githubusercontent.com/wiz-sec-public/wiz-research-iocs/main/reports/shai-hulud-2-packages.csv"
                if not config.quiet:
                    print(f"Downloading IOC data from Wiz Research...")
                
                with urlopen(url) as response:
                    content = response.read().decode('utf-8')
                
                reader = csv.DictReader(content.splitlines())
                packages_data = list(reader)
                
                if not config.quiet:
                    print(f"✓ Downloaded {len(packages_data)} packages")
                
                # Parse packages
                ioc_packages = {}
                for row in packages_data:
                    package_name = (row.get('Package') or row.get('package', '')).strip()
                    version = (row.get('Version') or row.get('version', '')).strip()
                    
                    if version.startswith('= '):
                        version = version[2:].strip()
                    
                    if not package_name:
                        continue
                    
                    if package_name not in ioc_packages:
                        ioc_packages[package_name] = []
                    
                    if version and version not in ioc_packages[package_name]:
                        ioc_packages[package_name].append(version)
                
                if not config.quiet:
                    print(f"✓ Parsed {len(ioc_packages)} unique packages")
                
                # Load existing IOCs for comparison
                ioc_file = Path(__file__).parent / "issues" / "shai_hulud_2.py"
                old_packages = {}
                if ioc_file.exists():
                    try:
                        # Read existing file
                        old_content = ioc_file.read_text()
                        # Extract IOC_PACKAGES dict
                        if 'IOC_PACKAGES = {' in old_content:
                            import ast
                            # Parse the Python file to extract IOC_PACKAGES
                            tree = ast.parse(old_content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Assign):
                                    for target in node.targets:
                                        if isinstance(target, ast.Name) and target.id == 'IOC_PACKAGES':
                                            old_packages = ast.literal_eval(node.value)
                                            break
                    except Exception as e:
                        if not config.quiet:
                            print(f"⚠️  Could not parse existing IOCs: {e}")
                
                # Compare old and new packages
                new_package_names = set(ioc_packages.keys()) - set(old_packages.keys())
                removed_package_names = set(old_packages.keys()) - set(ioc_packages.keys())
                updated_packages = []
                
                for pkg in set(ioc_packages.keys()) & set(old_packages.keys()):
                    old_versions = set(old_packages[pkg] or [])
                    new_versions = set(ioc_packages[pkg] or [])
                    if old_versions != new_versions:
                        new_vers = new_versions - old_versions
                        if new_vers:
                            updated_packages.append((pkg, list(new_vers)))
                
                # Generate IOC file
                lines = [
                    '"""',
                    'Shai-Hulud 2.0 Supply Chain Attack IOC Definitions',
                    '',
                    'Source: Wiz Research',
                    'URL: https://github.com/wiz-sec-public/wiz-research-iocs',
                    f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    '"""',
                    '',
                    'IOC_PACKAGES = {',
                ]
                
                for package_name in sorted(ioc_packages.keys()):
                    versions = ioc_packages[package_name]
                    if versions:
                        versions_str = ', '.join(f'"{v}"' for v in sorted(versions))
                        lines.append(f'    "{package_name}": [{versions_str}],')
                    else:
                        lines.append(f'    "{package_name}": None,')
                
                lines.append('}')
                lines.append('')
                
                ioc_file.write_text('\n'.join(lines))
                
                if not config.quiet:
                    print(f"✓ Successfully updated {ioc_file}")
                    print()
                    
                    # Show changes
                    if new_package_names or updated_packages or removed_package_names:
                        print("📊 Changes detected:")
                        print("-" * 60)
                        
                        if new_package_names:
                            print(f"  🆕 New packages: {len(new_package_names)}")
                            if len(new_package_names) <= 10:
                                for pkg in sorted(new_package_names):
                                    print(f"     - {pkg}")
                            else:
                                for pkg in sorted(list(new_package_names)[:10]):
                                    print(f"     - {pkg}")
                                print(f"     ... and {len(new_package_names) - 10} more")
                        
                        if updated_packages:
                            print(f"  🔄 Updated packages: {len(updated_packages)}")
                            if len(updated_packages) <= 10:
                                for pkg, new_vers in updated_packages:
                                    print(f"     - {pkg}: {', '.join(new_vers)}")
                            else:
                                for pkg, new_vers in updated_packages[:10]:
                                    print(f"     - {pkg}: {', '.join(new_vers)}")
                                print(f"     ... and {len(updated_packages) - 10} more")
                        
                        if removed_package_names:
                            print(f"  ➖ Removed packages: {len(removed_package_names)}")
                            if len(removed_package_names) <= 10:
                                for pkg in sorted(removed_package_names):
                                    print(f"     - {pkg}")
                            else:
                                for pkg in sorted(list(removed_package_names)[:10]):
                                    print(f"     - {pkg}")
                                print(f"     ... and {len(removed_package_names) - 10} more")
                        
                        print()
                    else:
                        print("ℹ️  No changes detected - IOCs are up to date")
                        print()
                    
                    print("=" * 60)
                    print("✓ Update complete!")
                    print("=" * 60)
                
                return
                
            except Exception as e:
                print(f"✗ Failed to update IOCs: {e}", file=sys.stderr)
                sys.exit(1)
        
        # Handle cache-only operations first
        if config.cache_info or config.clear_cache or config.clear_cache_type or config.refresh_repo or config.cleanup_cache:
            cache_manager = CacheManager()
            
            if config.cache_info:
                if not config.quiet:
                    print("📊 Cache Information")
                    print("=" * 40)
                cache_info = cache_manager.get_cache_info()
                cli.display_cache_info(cache_info)
                return
            
            if config.clear_cache:
                if not config.quiet:
                    print("🧹 Clearing all cache data...")
                cache_manager.clear_cache()
                if not config.quiet:
                    print("✅ Cache cleared successfully")
                return
            
            if config.clear_cache_type:
                if not config.quiet:
                    print(f"🧹 Clearing {config.clear_cache_type} cache...")
                cache_manager.clear_cache(config.clear_cache_type)
                if not config.quiet:
                    print(f"✅ {config.clear_cache_type.title()} cache cleared successfully")
                return
            
            if config.refresh_repo:
                if not config.quiet:
                    print(f"🔄 Refreshing cache for {config.refresh_repo}...")
                count = cache_manager.refresh_repository_cache(config.refresh_repo)
                if not config.quiet:
                    print(f"✅ Refreshed repository cache: removed {count:,} entries")
                return
            
            if config.cleanup_cache:
                if not config.quiet:
                    print(f"🧹 Cleaning up cache entries older than {config.cleanup_cache} days...")
                count = cache_manager.cleanup_old_entries(config.cleanup_cache)
                if not config.quiet:
                    print(f"✅ Cleaned up old cache entries: removed {count:,} entries")
                return
        
        # Handle resume and scan listing commands
        if config.list_scans:
            from .resume_cli import list_resumable_scans
            list_resumable_scans()
            return
        
        if config.resume:
            from .resume_cli import show_resume_info
            from .scan_state import ScanStateManager
            
            if not show_resume_info(config.resume):
                return
            
            # Load the scan state
            state_manager = ScanStateManager()
            scan_state = state_manager.load_state(config.resume)
            
            if not scan_state:
                print(f"\n❌ Could not load scan state for ID: {config.resume}")
                return
            
            print(f"\n🔄 Resuming scan: {config.resume}")
            print(f"   Organization: {scan_state.org}")
            print(f"   Scan type: {scan_state.scan_type}")
            print(f"   Progress: {scan_state.repositories_scanned}/{scan_state.total_repositories} repositories")
            
            # Create a new config from the saved state
            config_dict = scan_state.config.copy()
            config_dict.update({
                'org': scan_state.org,
                'team_first_org': scan_state.scan_type == 'team-first-org',
                'team': scan_state.target if scan_state.scan_type == 'team' else None,
                'repo': scan_state.target if scan_state.scan_type == 'repo' else None,
            })
            
            resumed_config = ScanConfig(**config_dict)
            
            # Resume the scan
            try:
                from .scanner import GitHubIOCScanner
                from .github_client import GitHubClient
                from .cache import CacheManager
                from .ioc_loader import IOCLoader
                
                # Initialize required components
                github_client = GitHubClient(
                    github_app_config=resumed_config.github_app_config,
                    org=resumed_config.org
                )
                cache_manager = CacheManager()
                ioc_loader = IOCLoader(resumed_config.issues_dir)
                
                # Initialize scanner
                scanner = GitHubIOCScanner(
                    resumed_config,
                    github_client,
                    cache_manager,
                    ioc_loader,
                    enable_batch_processing=getattr(resumed_config, 'enable_batch_processing', True),
                    enable_sbom_scanning=resumed_config.enable_sbom and not resumed_config.disable_sbom
                )
                
                # Set up resume state in scanner
                scanner.resume_state = scan_state
                
                print(f"\n🚀 Starting resumed scan...")
                start_time = time.time()
                
                results = scanner.scan()
                
                duration = time.time() - start_time
                
                # Display results
                self.display_results(results, resumed_config, duration)
                
                # Clean up completed scan state
                state_manager.cleanup_completed_scan(config.resume)
                
                print(f"\n✅ Resumed scan completed successfully!")
                
            except Exception as e:
                print(f"\n❌ Resume failed: {e}")
                logger.error(f"Resume failed for scan {config.resume}: {e}")
                import traceback
                traceback.print_exc()
            
            return
        
        # Suggest resume if available scans exist
        if config.org and not config.resume:
            scan_type = 'team-first-org' if config.team_first_org else 'org'
            if config.team:
                scan_type = 'team'
            elif config.repo:
                scan_type = 'repo'
            
            from .resume_cli import suggest_resume_if_available
            suggest_resume_if_available(config.org, scan_type)
        
        # Initialize components for scanning
        try:
            # Load IOC definitions
            ioc_loader = IOCLoader(config.issues_dir)
            iocs = ioc_loader.load_iocs()
            
            if not iocs:
                cli.display_error(f"No IOC definitions found in '{config.issues_dir}' directory")
                sys.exit(1)
            
            # Count total IOC packages
            total_ioc_packages = sum(len(ioc_def.packages) for ioc_def in iocs.values())
            
            if config.verbose:
                logger.info(f"Loaded {len(iocs)} IOC files with {total_ioc_packages} total packages")
            
            # Initialize GitHub client with GitHub App support
            github_client = GitHubClient(
                github_app_config=config.github_app_config,
                org=config.org
            )
            
            # Initialize cache manager
            cache_manager = CacheManager()
            
            # Create progress callback
            def progress_callback(current: int, total: int, repo_name: str, start_time: float = None):
                cli.display_progress(current, total, repo_name, config, start_time)
            
            # Determine SBOM scanning configuration
            enable_sbom_scanning = config.enable_sbom and not config.disable_sbom
            
            # Create batch configuration with rate limiting settings
            from .batch_models import BatchConfig
            batch_config = None
            if config.enable_batch_processing:
                batch_config = BatchConfig(
                    rate_limit_strategy=config.rate_limit_strategy,
                    enable_proactive_rate_limiting=config.enable_intelligent_rate_limiting,
                    rate_limit_safety_margin=config.rate_limit_safety_margin,
                    enable_budget_distribution=config.enable_intelligent_rate_limiting,
                    enable_adaptive_timing=config.enable_intelligent_rate_limiting
                )
            
            # Initialize scanner with progress callback and SBOM options
            scanner = GitHubIOCScanner(
                config, 
                github_client, 
                cache_manager, 
                ioc_loader, 
                progress_callback,
                batch_config=batch_config,
                enable_batch_processing=config.enable_batch_processing,
                enable_sbom_scanning=enable_sbom_scanning
            )
            
            # Display professional scan start information
            cli.display_professional_scan_start(config, total_ioc_packages)
            
            # Run the scan
            results = scanner.scan()
            
            # Clear progress line after completion
            cli.clear_progress_line(config)
            
            # Display results in professional format
            cli.display_professional_results(
                results.matches, 
                config,
                workflow_findings=results.workflow_findings,
                secret_findings=results.secret_findings
            )
            
            # Close cache connection for cleanup
            try:
                cache_manager.close()
            except Exception as e:
                logger.debug(f"Error closing cache: {e}")
            
            # Display professional summary
            cli.display_professional_summary(
                results.repositories_scanned, 
                results.files_scanned, 
                results.cache_stats, 
                config,
                workflow_findings=results.workflow_findings,
                secret_findings=results.secret_findings
            )
            
        except Exception as e:
            cli.display_error(f"Failed to initialize scanner: {e}")
            logger.error(f"Scanner initialization failed: {e}", exc_info=True)
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(130)  # Standard exit code for SIGINT
    except GitHubIOCScannerError as e:
        error_msg = format_error_message(e, include_cause=False)
        print(f"Error: {error_msg}", file=sys.stderr)
        logger.debug(f"Full error details: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
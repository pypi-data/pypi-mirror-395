# GitHub IOC Scanner

A powerful command-line tool for scanning GitHub repositories to detect Indicators of Compromise (IOCs) in package dependencies across multiple programming languages and package managers.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/security-focused-green.svg)](https://github.com/christianherweg0807/github_package_scanner)

## 🚀 Features

- **Multi-Language Support**: JavaScript/Node.js, Python, Ruby, PHP, Go, Rust, Java/Maven
- **SBOM Integration**: Native support for Software Bill of Materials (SPDX, CycloneDX formats)
- **GitHub Actions Security**: Detect dangerous workflow configurations and malicious runners
- **Secrets Detection**: Identify exfiltrated credentials and API keys in repositories
- **Flexible Scanning**: Organization-wide, team-specific, team-first organization, or individual repository scanning
- **High Performance**: Parallel processing with intelligent batching and caching
- **Real-time Progress**: Live progress tracking with ETA calculations
- **Supply Chain Security**: Detect compromised packages and typosquatting attacks
- **Comprehensive IOCs**: Pre-loaded with 2932+ known malicious packages including recent npm attacks

## 📦 Supported Package Managers & SBOM Formats

| Language | Package Managers | Files Scanned |
|----------|------------------|---------------|
| **JavaScript/Node.js** | npm, yarn, pnpm, bun | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` |
| **Python** | pip, pipenv, poetry | `requirements.txt`, `Pipfile.lock`, `poetry.lock`, `pyproject.toml` |
| **Ruby** | bundler | `Gemfile.lock` |
| **PHP** | composer | `composer.lock` |
| **Go** | go modules | `go.mod`, `go.sum` |
| **Rust** | cargo | `Cargo.lock` |
| **Java** | Maven | `pom.xml` |

### SBOM (Software Bill of Materials) Support

| Format | File Extensions | Description |
|--------|----------------|-------------|
| **SPDX** | `.json`, `.xml` | Industry standard SBOM format |
| **CycloneDX** | `.json`, `.xml` | OWASP SBOM standard |
| **Generic** | `.json`, `.xml` | Custom SBOM formats |

**Supported SBOM Files**: `sbom.json`, `bom.json`, `cyclonedx.json`, `spdx.json`, `software-bill-of-materials.json`, and XML variants

## 🛠️ Installation

### From PyPI (Recommended)

```bash
pip install github-ioc-scanner
```

### From Source

```bash
git clone https://github.com/christianherweg0807/github_package_scanner.git
cd github_package_scanner
pip install -e .
```
### Locally via docker

```bash
git clone https://github.com/christianherweg0807/github_package_scanner.git
cd github_package_scanner
docker build -t github-ioc-scanner .
docker run -e GITHUB_TOKEN=ghp_xyz -t github-ioc-scanner --org your-org <etc> 
```

### Development Installation

```bash
git clone https://github.com/christianherweg0807/github_package_scanner.git
cd github_package_scanner
pip install -e ".[dev]"
```

## ⚡ Quick Start

### 1. Authentication

#### Option A: Personal Access Token (Simple)
```bash
export GITHUB_TOKEN="your_github_token_here"
```

#### Option B: GitHub App (Enterprise)
For better security and higher rate limits, use GitHub App authentication:

```bash
# Create ~/github/apps.yaml with your GitHub App credentials
github-ioc-scan --org your-org --github-app-config ~/github/apps.yaml
```

**Benefits of GitHub Apps:**
- Higher rate limits (5,000 requests/hour per installation)
- Fine-grained permissions
- Enterprise-friendly audit trails
- Automatic token refresh

See [GitHub App Authentication Guide](docs/GITHUB_APP_AUTHENTICATION.md) for setup instructions.

### 2. Basic Usage

```bash
# Scan all repositories in an organization
github-ioc-scan --org your-org

# Scan a specific repository
github-ioc-scan --org your-org --repo your-repo

# Fast scan (root-level files only)
github-ioc-scan --org your-org --fast
```

## 📋 Usage Examples

### Organization Scanning

Scan all repositories in an organization:
```bash
github-ioc-scan --org your-org
```

### Team-based Scanning

Scan repositories belonging to a specific team:
```bash
github-ioc-scan --org your-org --team security-team
```

### Team-First Organization Scanning

Scan all repositories in an organization, organized by teams for better visibility:
```bash
github-ioc-scan --org your-org --team-first-org
```

This approach:
1. **Discovers all teams** in the organization
2. **Scans team repositories** and displays results grouped by team
3. **Scans remaining repositories** not assigned to any team
4. **Provides team-level visibility** into security issues

**Benefits:**
- Clear visibility into which teams have security issues
- Better organization of scan results
- Easier to assign remediation tasks to specific teams
- Comprehensive coverage of all repositories

**Example Output:**
```
🚨 TEAM 'security-team' - THREATS DETECTED
============================================================
Found 2 indicators of compromise:

📦 Repository: your-org/security-app
   Threats found: 2
   ⚠️  package.json | malicious-package | 1.0.0
   ⚠️  requirements.txt | compromised-lib | 2.1.0

✅ TEAM 'frontend-team' - NO THREATS DETECTED
   Repositories scanned: 5
   Files analyzed: 127

🚨 TEAM 'backend-team' - THREATS DETECTED
============================================================
Found 1 indicators of compromise:

📦 Repository: your-org/api-service
   Threats found: 1
   ⚠️  Cargo.lock | unsafe-crate | 0.3.2
```

### Repository-specific Scanning

Scan a specific repository:
```bash
github-ioc-scan --org your-org --repo your-repo
```

### Fast Mode

For quick assessments, use fast mode to scan only root-level files:
```bash
github-ioc-scan --org your-org --fast
```

### Include Archived Repositories

By default, archived repositories are skipped. Include them with:
```bash
github-ioc-scan --org your-org --include-archived
```

### SBOM Scanning

Scan Software Bill of Materials files alongside traditional lockfiles:

```bash
# Default: Scan both lockfiles and SBOM files
github-ioc-scan --org your-org

# Scan only SBOM files (skip traditional lockfiles)
github-ioc-scan --org your-org --sbom-only

# Disable SBOM scanning (traditional lockfiles only)
github-ioc-scan --org your-org --disable-sbom
```

**Supported SBOM Formats:**
- SPDX (JSON/XML): `spdx.json`, `spdx.xml`
- CycloneDX (JSON/XML): `cyclonedx.json`, `bom.xml`
- Generic formats: `sbom.json`, `software-bill-of-materials.json`

### Security Scanning

Enable advanced security scanning features:

```bash
# Enable GitHub Actions workflow security scanning
github-ioc-scan --org your-org --scan-workflows

# Enable secrets detection (AWS keys, GitHub tokens, API keys)
github-ioc-scan --org your-org --scan-secrets

# Enable both workflow and secrets scanning
github-ioc-scan --org your-org --scan-workflows --scan-secrets

# Comprehensive security scan with all features
github-ioc-scan --org your-org --scan-workflows --scan-secrets --enable-maven
```

### Batch Processing

For large organizations, use batch processing for optimal performance:
```bash
# Aggressive batching strategy
github-ioc-scan --org your-org --batch-strategy aggressive

# Custom concurrency limits
github-ioc-scan --org your-org --max-concurrent 10

# Enable cross-repository batching
github-ioc-scan --org your-org --enable-cross-repo-batching
```

### Verbose Output

Get detailed information during scanning:
```bash
github-ioc-scan --org your-org --verbose
```

## 🔍 Current IOC Coverage

The scanner includes comprehensive IOC definitions for:

### 🚨 Latest npm Supply Chain Attack (September 2025)
**Heise Security Report**: [Neuer NPM-Großangriff: Selbst-vermehrende Malware infiziert Dutzende Pakete](https://www.heise.de/news/Neuer-NPM-Grossangriff-Selbst-vermehrende-Malware-infiziert-Dutzende-Pakete-10651111.html)

✅ **Fully Covered**: All packages from this attack are included in our built-in IOC database

### Recent Supply Chain Attacks
- **S1ngularity/NX Attack (September 2025)**: 2039+ compromised npm packages with self-replicating worm payload
  - **Coverage**: Fully covered in built-in IOC database
  - **Reference**: [Heise Security Report](https://www.heise.de/news/Neuer-NPM-Grossangriff-Selbst-vermehrende-Malware-infiziert-Dutzende-Pakete-10651111.html)
  - **Technical Details**: [Aikido Security Analysis](https://www.aikido.dev/blog/s1ngularity-nx-attackers-strike-again)
- **CrowdStrike Typosquatting Campaign**: 400+ malicious packages impersonating CrowdStrike
- **Shai Hulud Attack**: 99+ compromised packages with advanced evasion techniques
- **Historical Attacks**: Various documented supply chain compromises

### Attack Types Detected
- **Typosquatting**: Packages with names similar to popular libraries
- **Dependency Confusion**: Malicious packages targeting internal dependencies  
- **Compromised Packages**: Legitimate packages that were later compromised
- **Backdoored Libraries**: Libraries with hidden malicious functionality

### Total Coverage
- **2857+ IOC Definitions**: Comprehensive coverage of known malicious packages (2833 npm + 24 Maven)
- **Regular Updates**: IOC definitions are continuously updated with new threats
- **Multi-language**: Coverage across all supported package managers including Java/Maven
- **Current as of November 2025**: Includes latest npm and Maven supply chain attacks

## 📊 Output Formats

### Standard Output
```
🔍 Scanning organization: your-org
📁 Found 45 repositories to scan
[████████████████████████████████] 100% | 45/45 repositories | ETA: 0s

⚠️  THREATS DETECTED:

Repository: your-org/frontend-app
├── package.json
│   └── 🚨 CRITICAL: malicious-package@1.0.0
│       └── IOC Source: s1ngularity_nx_attack_2024.py
│       └── Description: Compromised package from S1ngularity NX attack

📈 Scan Summary:
├── Repositories scanned: 45
├── Files analyzed: 127
├── Threats found: 1
└── Scan duration: 23.4s
```

### JSON Output
```bash
github-ioc-scan --org your-org --output json
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub personal access token | Required (if not using GitHub App) |
| `GITHUB_IOC_CACHE_DIR` | Cache directory location | `~/.cache/github-ioc-scanner` |
| `GITHUB_IOC_LOG_LEVEL` | Logging level | `INFO` |

**Note**: When using GitHub App authentication, `GITHUB_TOKEN` is not required.

### Configuration File

Create a `config.yaml` file:

```yaml
github:
  token: "your_token_here"
  
scanning:
  fast_mode: false
  include_archived: false
  max_concurrent: 5
  
batch:
  strategy: "adaptive"
  enable_cross_repo_batching: true
  
cache:
  enabled: true
  ttl_hours: 24
```

## 🚀 Performance Features

### Intelligent Caching
- **File-level caching**: Avoid re-scanning unchanged files
- **ETag support**: Efficient GitHub API usage
- **Smart invalidation**: Automatic cache updates

### Parallel Processing
- **Concurrent requests**: Multiple repositories processed simultaneously
- **Batch optimization**: Intelligent request batching
- **Rate limit management**: Automatic rate limit handling

### Progress Tracking
- **Real-time updates**: Live progress bars with ETA
- **Detailed metrics**: Success rates, processing speeds
- **Performance monitoring**: Automatic performance optimization

### New Features Performance Impact

The new security scanning features (Maven, Workflow, Secrets) add minimal overhead:

| Feature | Typical Time | Impact |
|---------|--------------|--------|
| Maven Parser | ~0.1-0.5ms per file | Negligible |
| Workflow Scanner | ~0.3-1ms per file | Negligible |
| Secrets Scanner | ~2-5ms per 1000 lines | Low |
| **Combined Overhead** | ~20-30% | Minimal vs network latency |

All features scale linearly and are optimized for large repositories. See [Performance Documentation](docs/PERFORMANCE.md) for detailed benchmarks.

### Parallel Scanning (v1.7.0+)

Workflow and secrets scanning now runs in parallel for significantly faster scans:

| Repositories | Workers | Speed Improvement |
|--------------|---------|-------------------|
| 16 repos | 5 workers | ~3x faster |
| 50 repos | 10 workers | ~5x faster |
| 100+ repos | 10 workers | ~5-8x faster |

### Incremental Repository Caching (v1.7.0+)

Repository lists are now cached and incrementally updated:

| Scenario | API Calls | Time Saved |
|----------|-----------|------------|
| First scan (1000 repos) | 10 calls | Baseline |
| Repeat scan (5 new repos) | 1 call | ~90% |
| Repeat scan (no changes) | 1 call | ~95% |

Use `--refresh-repos` to force a full refresh when needed.

## 🛡️ Security Features

### Supply Chain Protection
- **Comprehensive IOC database**: 2932+ known malicious packages (including Heise-reported npm attacks)
- **Typosquatting detection**: Advanced pattern matching
- **Dependency analysis**: Deep dependency tree scanning

### GitHub Actions Security Scanning
Detect dangerous workflow configurations that could be exploited in supply chain attacks:

- **Dangerous Triggers**: Detection of `pull_request_target` with unsafe checkout configurations
- **Privilege Escalation**: Identification of `workflow_run` triggers that could enable privilege escalation
- **Malicious Runners**: Detection of known malicious self-hosted runners (e.g., SHA1HULUD)
- **Shai Hulud 2 Patterns**: Detection of attack-specific workflow files (`discussion.yaml`, `formatter_123456789.yml`)

```bash
# Enable workflow scanning
github-ioc-scan --org your-org --scan-workflows

# Disable workflow scanning (default)
github-ioc-scan --org your-org --no-scan-workflows
```

See [Workflow Scanning Documentation](docs/WORKFLOW_SCANNING.md) for details.

### Secrets Detection
Identify exfiltrated credentials and sensitive data in repositories:

- **AWS Credentials**: Access keys (AKIA...) and secret keys
- **GitHub Tokens**: Personal access tokens (ghp_), OAuth tokens (gho_), app tokens (ghs_)
- **API Keys**: Generic API key patterns and service-specific tokens
- **Private Keys**: RSA, EC, and OpenSSH private keys
- **Shai Hulud 2 Artifacts**: Detection of exfiltration files (cloud.json, environment.json, truffleSecrets.json)

```bash
# Enable secrets scanning
github-ioc-scan --org your-org --scan-secrets

# Disable secrets scanning (default)
github-ioc-scan --org your-org --no-scan-secrets
```

See [Secrets Detection Documentation](docs/SECRETS_DETECTION.md) for details.

### Maven/Java Scanning
Scan Maven `pom.xml` files for compromised Java dependencies:

```bash
# Maven scanning is enabled by default
github-ioc-scan --org your-org

# Disable Maven scanning
github-ioc-scan --org your-org --disable-maven

# Explicitly enable Maven scanning
github-ioc-scan --org your-org --enable-maven
```

See [Maven Support Documentation](docs/MAVEN_SUPPORT.md) for details.

### Privacy & Security
- **Local processing**: All analysis done locally
- **Secure API usage**: Proper token handling
- **No data collection**: No telemetry or data sharing
- **Secret Masking**: Detected secrets are always masked in output (first 4 chars + ***)

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [**Batch Processing Guide**](docs/BATCH_PROCESSING_TUTORIAL.md) - Advanced batch processing features
- [**Performance Optimization**](docs/PERFORMANCE.md) - Performance tuning and optimization
- [**Package Manager Support**](docs/PACKAGE_MANAGERS.md) - Detailed package manager information
- [**Maven Support**](docs/MAVEN_SUPPORT.md) - Maven/Java dependency scanning
- [**Workflow Scanning**](docs/WORKFLOW_SCANNING.md) - GitHub Actions security scanning
- [**Secrets Detection**](docs/SECRETS_DETECTION.md) - Credential and secret detection
- [**IOC Definitions**](docs/S1NGULARITY_IOC_SUMMARY.md) - Current IOC coverage and sources
- [**API Reference**](docs/BATCH_API_REFERENCE.md) - Complete API documentation

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/github_ioc_scanner

# Run specific test categories
pytest tests/test_parsers.py  # Parser tests
pytest tests/test_batch_*.py  # Batch processing tests
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -e ".[dev]"`
5. Run tests: `pytest`

### Adding New IOCs

To add new IOC definitions:

1. Create or update files in the `issues/` directory
2. Follow the existing format: `IOC_PACKAGES = {"package-name": ["version1", "version2"]}`
3. Add documentation about the source and nature of the IOCs
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/christianherweg0807/github_package_scanner)
- [PyPI Package](https://pypi.org/project/github-ioc-scanner/)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/christianherweg0807/github_package_scanner/issues)

## ⚠️ Disclaimer

This tool is provided for security research and defensive purposes only. The IOC definitions are based on publicly available threat intelligence and research. Always verify findings independently and follow responsible disclosure practices.

## 🙏 Acknowledgments

- Security researchers and organizations who share threat intelligence
- The open-source community for package manager tools and libraries
- GitHub for providing comprehensive APIs for repository analysis

---

**Made with ❤️ for the security community**

# Pristy Support

[![PyPI version](https://badge.fury.io/py/pristy-support.svg)](https://badge.fury.io/py/pristy-support)
[![Python Version](https://img.shields.io/pypi/pyversions/pristy-support.svg)](https://pypi.org/project/pristy-support/)
[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Audit and support tools for Pristy ECM installations.

## Overview

Pristy Support is a command-line tool designed to help support teams diagnose and audit Pristy installations. It performs comprehensive checks on system resources, services, logs, database statistics, and configuration files, generating detailed reports in multiple formats.

## Features

### System Checks
- ✅ Systemd services status (enabled/active)
- ✅ Docker containers health with creation timestamps
- ✅ Memory configuration and limits validation
- ✅ Swap presence and size
- ✅ Firewall status detection
- ✅ Disk space monitoring with warning thresholds
- ✅ System load analysis
- ✅ Detailed error reporting with specific issues listed

### Logs Analysis
- 🔍 Journalctl log analysis for all Pristy services
- 🔍 Error, warning, and critical message detection
- 🔍 Log severity aggregation by service
- 🔍 Common error pattern extraction
- 🔍 Configurable time period analysis

### Database Statistics
- 📊 Node, property, and aspect counts
- 📊 User statistics (internal with password vs external SSO/LDAP)
- 📊 Group and site statistics with detailed lists
- 📊 Content statistics and store distribution
- 📊 Database and table sizes
- 📊 Top 10 node types analysis
- 📊 Useful ratios (properties/node, aspects/node)

### Configuration Review
- 📄 Alfresco global.properties analysis
- 📄 Pristy Vue.js application configurations (env-config.json)
- 📄 Key parameter extraction and validation
- 📄 Configuration issue detection and warnings
- 📄 Missing parameter identification

### Export Formats
- 📝 **Markdown**: Clean text reports with tables
- 🌐 **HTML**: Styled, navigable reports with TOC and metrics
- 📦 **ZIP**: Complete archives with all data and reports

### Reporting Features
- 🕒 Timezone-aware timestamps (local + Paris time)
- ⏱️ Container age display (shows how long ago containers were created)
- 📋 Detailed error listing in CLI output
- 🎨 Color-coded status badges (OK, WARNING, ERROR)
- 📊 Interactive HTML reports with navigation

## Installation

### From PyPI (Recommended)

```bash
pip install pristy-support
```

### From Source with uv (Recommended)

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
uv sync
```

### From Source with pip

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### For Development

With uv (recommended):

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
uv sync
```

Or with pip:

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
pip install -e ".[dev]"
```

## Quick Start

Run a complete audit:

```bash
pristy-support audit
```

This generates reports in the current directory showing:
- System health status
- Service and container states
- Log errors and warnings
- Database statistics
- Configuration issues

## Configuration

Pristy Support can be customized via YAML configuration files. The tool looks for configuration in these locations (in order of priority):
1. Custom path specified with `--config` option
2. `./pristy-support.yml` (current directory)
3. `./.pristy-support.yml` (current directory, hidden)
4. `~/.pristy-support.yml` (user home directory)
5. `~/.config/pristy-support/config.yml` (XDG config directory)
6. `/etc/pristy/pristy-support.yml` (system-wide configuration)

### Generate Default Configuration

Create a configuration file with all default values:

```bash
pristy-support init-config
```

This creates `pristy-support.yml` in the current directory. You can specify a custom output path:

```bash
pristy-support init-config --output /path/to/config.yml
```

### Configuration Options

The configuration file allows you to customize:
- **System**: Services to check, memory thresholds, disk space thresholds
- **Docker**: Container name patterns to monitor
- **Logs**: Services to analyze, time periods, severity keywords, max samples per severity
- **Database**: PostgreSQL connection parameters
- **Config Paths**: Paths for Alfresco and Pristy application configurations
- **Audit**: Default export formats and output directory

Example configuration snippet:

```yaml
system:
  services:
    - postgres
    - kafka
    - alfresco
  memory:
    min_ram_gb: 8
    recommended_ram_gb: 12
    min_swap_gb: 2
  disk_thresholds:
    /: 10
    /var/lib/docker: 30

logs:
  services:
    - alfresco
    - solr6
  default_since: 7d
  max_samples_per_severity: 10
  severity_keywords:
    critical: [CRITICAL, FATAL]
    error: [ERROR]
    warning: [WARN, WARNING]
```

### Using Custom Configuration

```bash
pristy-support --config /path/to/config.yml audit
```

## Usage

### Full Audit

Run a complete audit of your Pristy installation:

```bash
pristy-support audit
```

This will generate reports in the current directory in all formats (Markdown, HTML, and ZIP).

Example output:
```
🔍 Starting Pristy installation audit...

Detecting permissions...
Permission Detection:
  Root user: No
  Sudo available: Yes
  Docker: Available

Running system checks...
  System checks: WARNING
    ❌ Disk /var/lib/docker: only 5.2% free
    ⚠️  Firewall: Not detected
    ⚠️  Container pristy-acs-1: Stopped
    ⚠️  ... and 2 more container(s) with issues

Analyzing logs (last 7d)...
  Logs analysis: OK

Collecting database statistics...
  Database audit: OK

Reviewing configuration...
  Configuration audit: WARNING
    ⚠️  Alfresco: Missing key parameter 'db.pool.max'

Generating reports...
  ✅ Markdown report: ./pristy_audit_report.md
  ✅ HTML report: ./pristy_audit_report.html
  ✅ ZIP archive: ./pristy_audit.zip

✨ Audit complete!
```

#### Options

```bash
pristy-support audit --output-dir /path/to/output --formats md,html,zip --since 30d
```

- `--output-dir`, `-o`: Output directory for reports (default: current directory)
- `--formats`, `-f`: Export formats, comma-separated (default: `md,html,zip`)
  - Available formats: `md`, `markdown`, `html`, `zip`
- `--since`, `-s`: Time period for log analysis (default: `7d`)

Examples:
- `--since 24h`: Last 24 hours
- `--since 7d`: Last 7 days (default)
- `--since 30d`: Last 30 days

### Individual Checks

Run specific checks independently:

#### System Checks Only

```bash
pristy-support system-check
```

Shows:
- System information (hostname, OS)
- CPU and memory usage
- Network interfaces
- Docker version and containers
- Service status
- Disk space and system load

#### Logs Analysis Only

```bash
pristy-support logs-check --since 7d
```

Analyzes logs for the specified time period and displays services with errors or warnings.

#### Database Statistics Only

```bash
pristy-support database-check
```

Displays:
- Node, property, and aspect counts
- User statistics (internal/external breakdown)
- Group and site lists
- Database size
- Nodes by store and type

#### Configuration Review Only

```bash
pristy-support config-check
```

Reviews configuration files and shows:
- Alfresco configuration status
- Pristy application configurations
- Missing or invalid parameters
- Configuration warnings

### Debug Mode

Enable debug mode to see all commands executed by the tool:

```bash
pristy-support --debug audit
```

Debug mode displays:
- All system commands before execution (systemctl, journalctl, docker, etc.)
- Command results (success/failure with exit codes)
- Docker exec operations with container names
- File read/write operations

Example output:
```
DEBUG [pristy_support] 🔧 Checking systemctl availability
DEBUG [pristy_support]    $ systemctl --version
DEBUG [pristy_support]    ✓ Command succeeded (exit code: 0)
DEBUG [pristy_support] 🔧 Listing Docker containers
DEBUG [pristy_support]    $ docker ps --format {{.ID}}|{{.Names}}|{{.Status}}|{{.Image}} -a
DEBUG [pristy_support]    ✓ Command succeeded (exit code: 0)
DEBUG [pristy_support] 🐳 Executing in container 'postgres':
DEBUG [pristy_support]    $ psql -U alfresco -d alfresco -t -A -c SELECT COUNT(*) FROM alf_node;
```

This is useful for:
- Troubleshooting issues
- Understanding what the tool is doing
- Debugging permission problems
- Support and diagnostics

### Help

```bash
pristy-support --help
pristy-support audit --help
pristy-support system-check --help
```

### Version

```bash
pristy-support --version
```

## Requirements

### System Requirements

- Python 3.9 or higher
- Linux operating system (systemd-based)
- Docker (for container checks and PostgreSQL access)

### Permissions

The tool automatically detects available permissions and adapts its checks accordingly:

- **Root/sudo**: Full access to all checks
- **Docker group**: Access to Docker commands
- **Standard user**: Limited checks (may miss some system information)

For best results, run with sudo or as root:

```bash
sudo pristy-support audit
```

### Pristy Installation

The tool expects a standard Pristy installation with:

- Systemd services for Pristy components
- Docker containers running Pristy services
- PostgreSQL database in a Docker container named `postgres`
- Configuration files in standard locations:
  - `/opt/alfresco/tomcat/shared/classes/alfresco-global.properties`
  - `/opt/pristy-*/public/env-config.json`

These paths can be customized via the configuration file.

## Architecture

### Project Structure

```
pristy-support/
├── pristy_support/
│   ├── __init__.py
│   ├── __main__.py          # Entry point for python -m pristy_support
│   ├── cli.py               # CLI interface (Click)
│   ├── config_manager.py    # Configuration management
│   ├── modules/             # Audit modules
│   │   ├── system.py        # System checks
│   │   ├── logs.py          # Log analysis
│   │   ├── database.py      # Database statistics
│   │   └── config.py        # Configuration review
│   ├── exporters/           # Report exporters
│   │   ├── markdown.py      # Markdown exporter
│   │   ├── html.py          # HTML exporter
│   │   └── zip_exporter.py  # ZIP archive exporter
│   ├── utils/               # Utilities
│   │   ├── permissions.py   # Permission detection
│   │   ├── docker_utils.py  # Docker utilities
│   │   └── logger.py        # Debug logging
│   └── templates/           # HTML templates (future)
├── tests/                   # Unit tests
│   ├── test_cli.py
│   ├── test_config_manager.py
│   └── test_exporters.py
├── pyproject.toml           # Package metadata (PEP 621 + hatchling)
├── uv.lock                  # uv lock file
├── PUBLISHING.md            # PyPI publishing guide
├── README.md                # This file
└── LICENSE                  # AGPL-3.0 license
```

### Modules

#### System Module (`system.py`)
Checks system resources and services:
- Systemd service status
- Docker container health and age
- Memory and swap configuration
- Disk space availability
- System load
- Firewall detection

#### Logs Module (`logs.py`)
Analyzes system logs via journalctl:
- Searches for ERROR, WARN, FATAL, CRITICAL keywords
- Aggregates by service and severity
- Extracts error samples
- Configurable time periods and keywords

#### Database Module (`database.py`)
Collects PostgreSQL statistics:
- Executes queries via `docker exec` on postgres container
- Counts nodes, properties, aspects, users, groups
- Distinguishes internal (password-based) from external (SSO/LDAP) users
- Lists groups and sites
- Calculates useful ratios
- Reports database and table sizes
- Analyzes node distribution by store and type

#### Config Module (`config.py`)
Reviews configuration files:
- Parses alfresco-global.properties
- Reads Vue.js env-config.json files
- Validates key parameters
- Detects configuration issues
- Identifies missing parameters

### Exporters

#### Markdown Exporter
Generates clean, readable text reports with:
- Status badges (✅ ⚠️ ❌)
- Formatted tables
- Timestamp with timezone information
- Container age display

#### HTML Exporter
Creates styled HTML reports with:
- Responsive layout
- Interactive table of contents
- Color-coded status badges
- Sortable tables
- Metrics cards
- System overview section

#### ZIP Exporter
Bundles all reports and raw data:
- Markdown report
- HTML report
- Raw JSON data
- Individual module data files

## Development

### Setup Development Environment

With uv (recommended):

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
uv sync
```

With pip:

```bash
git clone https://gitlab.com/pristy-oss/pristy-support.git
cd pristy-support
pip install -e ".[dev]"
```

### Run Tests

With uv:

```bash
uv run pytest
uv run pytest -v                    # Verbose
uv run pytest --cov                 # With coverage
```

With pip:

```bash
pytest
pytest -v
pytest --cov
```

Current test coverage: **15%** (13 tests passing)

### Code Formatting

```bash
uv run black pristy_support/
# Or
black pristy_support/
```

### Type Checking

```bash
uv run mypy pristy_support/
# Or
mypy pristy_support/
```

### Linting

```bash
uv run flake8 pristy_support/
# Or
flake8 pristy_support/
```

### Building the Package

```bash
uv build
```

This creates wheel and source distributions in `dist/`.


## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest`)
6. Format code with Black (`uv run black pristy_support/`)
7. Commit your changes using conventional commits
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Merge Request

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 100)
- Add type hints where possible
- Write docstrings for all functions and classes
- All code comments in English
- Include license header in all source files

### Commit Messages

Use conventional commits format:
- `feat(module): add new feature`
- `fix(logs): correct error detection`
- `docs(readme): update installation instructions`
- `refactor(system): improve memory check logic`
- `test(database): add tests for user statistics`
- `chore(deps): update dependencies`

## License

This project is licensed under the GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later).

See [LICENSE](LICENSE) file for details.

## Authors

- **Jérémie Lesage** - JECI SARL - [https://www.jeci.fr](https://jeci.fr/en/)

## Links

- **Pristy**: [https://www.pristy.fr](https://pristy.fr/en)
- **Homepage**: [https://gitlab.com/pristy-oss/pristy-support](https://gitlab.com/pristy-oss/pristy-support)
- **PyPI**: [https://pypi.org/project/pristy-support/](https://pypi.org/project/pristy-support/)
- **Issues**: [https://gitlab.com/pristy-oss/pristy-support/-/issues](https://gitlab.com/pristy-oss/pristy-support/-/issues)

## Support

For issues, questions, or contributions:
- GitLab Issues: [https://gitlab.com/pristy-oss/pristy-support/-/issues](https://gitlab.com/pristy-oss/pristy-support/-/issues)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2025-12-08

### Added
- logs: count logs (journald) size for each system unit

## [1.2.1] - 2025-11-26

### Added
- Add Access Logs Analysis
- html: Add System Load report
- html: Publish HTML report to web directory.
- publish: Add more debug log

### Documentation
- Automation for publishing report

## [1.2.0] - 2025-11-21

### Added
- disk: new disk usage calculation based on findmnt

### Fixed
- fix: no timeout on disk usage command and sql queries


## [1.1.2] - 2025-11-21

### Fixed
- fix: use has_sudo instead of sudo_available


## [1.1.1] - 2025-11-21

### Added
- feat(directory): add missing logger 

### Fixed
- fix(solr): need sudo to read solr secret


## [1.1.0] - 2025-11-21

### Added
- Solr 6 statistics module for comprehensive index monitoring
  - Index statistics (nodes, transactions, ACLs, unindexed nodes, error nodes)
  - Lag information (transaction lag, changeset lag)
  - Tracker status monitoring (Metadata, Content, ACL trackers)
  - Cache performance metrics (hits, lookups, hit ratio, evictions)
  - Handler statistics (requests, errors, timeouts, average response time)
  - FTS (Full-Text Search) synchronization status
  - Detailed synchronization reports comparing database and index
- Add directory size computation

### Changed
- **BREAKING**: Migrated from Poetry to uv for package management


## [1.0.1] - 2025-10-23

### Changed
- HTML report: Improved CSS styling to better distinguish section levels (h2, h3, h4)

### Fixed
- fix(user): internal users may have password or passwordHash
- fix(user): ignore ROLE_ and guest


## [1.0.0] - 2025-10-23

Initial release.

### Added

**Core Features:**
- System checks (services, containers, memory, disk, load, firewall)
- Logs analysis with error/warning/critical detection
- Database statistics collection with user type distinction
- Configuration review for Alfresco and Pristy apps
- Multiple export formats (Markdown, HTML, ZIP)

**Improvements:**
- Automatic permission detection and adaptation
- CLI interface with Click framework
- Debug mode with command tracing
- YAML configuration system with customizable parameters
- `init-config` command to generate default configuration
- Detailed error reporting in CLI output
- Container age display (shows elapsed time since creation)
- Timezone-aware timestamps (local + Paris time)
- HTML reports with TOC and metrics overview
- Comprehensive test suite (13 tests)

**Technical:**
- Python 3.9+ support
- Poetry package management
- Published on PyPI
- AGPL-3.0-or-later license

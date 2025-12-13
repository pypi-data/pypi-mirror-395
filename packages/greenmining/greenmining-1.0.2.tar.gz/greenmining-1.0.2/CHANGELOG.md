# Changelog

## [0.1.12] - 2025-12-03

### Added
- Custom search keywords for repository fetching (`--keywords` option)
- `fetch_repositories()` function exposed in public API
- Users can now search for any topic (kubernetes, docker, serverless, etc.)

### Changed
- README updated to reflect 122 patterns (was showing 76 in PyPI description)
- CLI `fetch` command now accepts `--keywords` parameter
- Repository fetching no longer hardcoded to "microservices"

### Fixed
- Outdated pattern count in PyPI package description

## [0.1.11] - 2025-12-03

### Added
- Expanded pattern database from 76 to 122 patterns
- Added 9 new categories (Resource, Caching, Data, Async, Code, Monitoring, Network, Microservices, Infrastructure)
- Expanded keywords from 190 to 321
- VU Amsterdam 2024 research patterns for ML systems

### Changed
- README with comprehensive feature documentation
- Detection rate improved to 37.15% (up from 33.79%)

## [0.1.7] - 2025-12-02

### Added
- New release


## [0.1.6] - 2025-12-02

### Added
- New release


## [0.1.5] - 2025-12-02

### Added
- New release


## [0.1.4] - 2025-12-02

### Added
- New release


## [0.1.3] - 2025-12-02

### Added
- New release


## [0.1.2] - 2025-12-02

### Added
- New release


## [0.1.1] - 2025-12-02

### Added
- New release


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with MCP architecture
- GSF patterns database (76 patterns, 190 keywords)
- GitHub repository fetching and analysis
- PyDriller integration for commit mining
- Pattern matching engine
- Green awareness detection
- Data analysis and reporting
- CLI interface with Click
- Docker support with multi-stage builds
- GitHub Actions CI/CD pipeline
- PyPI publishing workflow
- Docker Hub and GHCR publishing
- Comprehensive test suite
- Documentation and examples

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - TBD

### Added
- Initial release
- Core functionality for GSF pattern mining
- CLI tool `greenmining`
- Support for 100 microservices repositories
- Pattern matching with 76 GSF patterns
- Green awareness analysis
- Data export capabilities
- Docker containerization
- CI/CD automation

[Unreleased]: https://github.com/yourusername/greenmining/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/greenmining/releases/tag/v0.1.0

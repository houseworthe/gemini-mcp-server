# Changelog

All notable changes to the Gemini MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive CI/CD pipeline with GitHub Actions
- Automated testing across multiple Python versions (3.8-3.12)
- Security scanning with Bandit and Safety
- Code quality checks with Ruff, Black, and mypy
- Cross-platform testing (Windows, macOS, Linux)
- Docker support for containerized deployment
- Proper Python packaging with pyproject.toml
- Test suite with pytest
- Contributing guidelines and code of conduct
- Security policy and reporting guidelines

### Changed
- Improved error handling and logging
- Updated documentation for open source release

### Security
- Removed hardcoded API keys from repository
- Added secure environment variable handling
- Implemented proper file permissions for sensitive data

## [1.0.0] - 2025-01-18

### Added
- Initial release of Gemini MCP Server
- Four main tools:
  - `ask_gemini` - Direct questions to Gemini
  - `gemini_code_review` - Code analysis and review
  - `gemini_brainstorm` - Creative ideation
  - `gemini_analyze_large` - Large document/codebase analysis
- One-line installation script
- Automatic Claude CLI registration
- Comprehensive documentation
- Integration test suite
- Support for Gemini 1.5 Flash model
- Configurable generation parameters
- Async implementation for better performance

### Security
- Secure local storage of API keys
- HTTPS-only API communication

[Unreleased]: https://github.com/ethanhouseworth1/gemini-mcp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ethanhouseworth1/gemini-mcp/releases/tag/v1.0.0
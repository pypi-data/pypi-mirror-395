# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-12-04

### Added
- **Trace Visualization & Observability** - 8 new optional fields for distributed tracing and observability
  - `environment` - Deployment environment with fallback detection
  - `region` - Cloud region with AWS/Azure/GCP auto-detection
  - `credential_alias` - Human-readable API key names
  - `trace_type` - Workflow category identifier (validated, max 128 chars)
  - `trace_name` - Human-readable trace instance label (auto-truncates at 256 chars)
  - `parent_transaction_id` - Parent transaction reference for distributed tracing
  - `transaction_name` - Human-friendly operation name
  - `operation_subtype` - Additional operation context
- New module `trace_fields.py` for centralized field capture and validation
- Auto-detection of operation types (CHAT, TOOL_CALL)
- Environment variable support for all trace fields with cloud provider fallbacks
- Test coverage for trace visualization
- Example code demonstrating trace visualization features

### Changed
- Updated `log_token_usage()` signature with 8 new optional parameters
- Updated `create_metering_call()` to capture and pass trace fields

### Dependencies
- Requires `revenium_middleware>=0.3.5` for trace field support in the metering API

## [0.2.27] - 2025-11-17

### Changed
- Updated Quick Start section with step-by-step virtual environment setup instructions

## [0.2.26] - 2025-11-17

### Changed
- Added virtual environment setup instructions to examples README

## [0.2.25] - 2025-11-14

### Added
- E2E test suite for comprehensive validation
- Simplified getting_started.py example with zero external dependencies

### Changed
- Streamlined README with focused code examples
- Standardized metadata structure across all examples

### Fixed
- Bedrock streaming examples now handle edge cases correctly

## [0.2.24] - 2025-11-09

### Changed
- Updated app and API address references
- Changed pyproject version
- Converted relative URLs to absolute GitHub URLs for PyPI compatibility

### Fixed
- Fixed URL compatibility for PyPI package page

## [0.2.23] - 2025-11-08

### Added
- AWS Bedrock integration support
- Bedrock streaming support
- usage_context export for streaming scenarios

### Changed
- Refactored provider detection logic
- Updated test imports to use current revenium_middleware module

### Fixed
- Fixed Bedrock metering parameter compatibility
- Fixed usage of revenium_middleware.client instead of non-existent Client class
- Fixed streaming token counting edge case

## [0.2.22] - 2025-09-16

### Changed
- Removed unused auto_patch.py (legacy duplicate monkey-patching path)
- Improved success detection for metering responses
- Updated logging levels: DEBUG for success, WARNING only for true failures

### Fixed
- Fixed erroneous 'Unexpected metering response' debug warnings
- Improved Revenium resource response handling (MeteringResponseResource)

## [0.2.21] - 2025-09-16

### Changed
- Updated README.md documentation
- Switched examples to use PyPI import
- Simplified example output

### Fixed
- Fixed usage_metadata nesting in examples
- Added installation hints to examples

## [0.2.20] - 2025-09-15

### Changed
- Removed usage_context support in favor of standardized usage_metadata
- Removed decorative emojis from customer-facing output
- Eliminated code duplication in parameter handling

### Added
- Comprehensive debug logging improvements
- Enhanced usage_metadata parameter support

## [0.2.19] - 2025-09-14

### Fixed
- Updated onboarding test for monkey-patching approach
- Ensured .env is properly ignored

### Added
- Added original onboarding test

## [0.2.18] - 2025-09-13

### Changed
- Enhanced main branch with usage_metadata parameter support
- Removed unnecessary files from enhanced main branch

## [0.2.17] - 2025-09-12

### Fixed
- Fixed streaming functionality
- Refactored README.md structure

## [0.2.16] - 2025-09-11

### Changed
- General improvements and bug fixes

## [0.2.15] - 2025-09-10

### Changed
- General improvements and bug fixes

## [0.2.14] - 2025-09-09

### Changed
- General improvements and bug fixes

## [0.2.13] - 2025-09-08

### Changed
- General improvements and bug fixes

## [0.2.12] - 2025-09-07

### Changed
- General improvements and bug fixes

## [0.2.11] - 2025-09-06

### Changed
- General improvements and bug fixes

## [0.2.10] - 2025-09-05

### Changed
- General improvements and bug fixes

## [0.2.9] - 2025-09-04

### Changed
- General improvements and bug fixes

## [0.2.8] - 2025-09-03

### Changed
- General improvements and bug fixes

## [0.2.7] - 2025-09-02

### Changed
- General improvements and bug fixes

## [0.2.6] - 2025-09-01

### Changed
- General improvements and bug fixes

## [0.2.5] - 2025-08-31

### Changed
- General improvements and bug fixes

## [0.2.4] - 2025-08-30

### Changed
- General improvements and bug fixes

## [0.2.3] - 2025-08-29

### Changed
- General improvements and bug fixes

## [0.2.2] - 2025-08-28

### Changed
- General improvements and bug fixes

## [0.2.1] - 2025-08-27

### Changed
- General improvements and bug fixes

## [0.2.0] - 2025-08-26

### Added
- Initial public release
- Anthropic API middleware support
- Token usage tracking
- Automatic metering to Revenium

[unreleased]: https://github.com/revenium/revenium-middleware-anthropic-python/compare/v0.2.25...HEAD
[0.2.25]: https://github.com/revenium/revenium-middleware-anthropic-python/compare/v0.2.24...v0.2.25
[0.2.24]: https://github.com/revenium/revenium-middleware-anthropic-python/compare/v0.2.23...v0.2.24
[0.2.23]: https://github.com/revenium/revenium-middleware-anthropic-python/releases/tag/v0.2.23


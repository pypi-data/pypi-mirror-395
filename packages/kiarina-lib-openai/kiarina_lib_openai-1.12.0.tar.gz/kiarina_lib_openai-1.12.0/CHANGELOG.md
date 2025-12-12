# Changelog

All notable changes to kiarina-lib-openai will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.12.0] - 2025-12-05

### Changed
- No changes

## [1.11.2] - 2025-12-02

### Changed
- No changes

## [1.11.1] - 2025-12-01

### Changed
- Made `api_key` field optional (can be `None`) to support environment variable configuration without explicit settings

## [1.11.0] - 2025-12-01

### Added
- Initial release with OpenAI API configuration management
- `OpenAISettings` class with API key, organization ID, and base URL support
- API key protection using `SecretStr`
- Multiple configuration support via `pydantic-settings-manager`
- Environment variable configuration with `KIARINA_LIB_OPENAI_` prefix
- Custom base URL support for OpenAI-compatible APIs

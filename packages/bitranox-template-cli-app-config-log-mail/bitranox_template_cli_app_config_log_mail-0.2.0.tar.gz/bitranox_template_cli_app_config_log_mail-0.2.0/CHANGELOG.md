# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.



## [0.2.0] - 2025-12-07

### Added
- `--profile` option for `config` command to load profile-specific configuration
- `--profile` option for `config-deploy` command to deploy to profile directories
- Profile parameter support in `get_config()`, `display_config()`, and `deploy_configuration()`
- Profile-specific configuration paths (e.g., `~/.config/slug/profile/<name>/config.toml`)
- `OutputFormat` and `DeployTarget` enums for type-safe CLI options
- `LoggingConfig` Pydantic model for validated logging configuration
- 4 new behavioral tests for profile functionality
- PYTHONIOENCODING=utf-8 for all subprocess calls in scripts

### Changed
- Centralized test fixtures in `conftest.py` (`MockConfig`, `mock_config_factory`, `clear_config_cache`)
- Flattened `test_mail.py` from class-based to function-based tests
- Added `@pytest.mark.os_agnostic` markers to all mail tests
- Increased lru_cache maxsize from 1 to 4 in `get_config()` for profile variations
- Added lru_cache to `get_default_config_path()` since the path never changes at runtime
- Updated `config_deploy.py` to use `DeployTarget` enum instead of strings
- Updated README with profile configuration documentation and examples

### Fixed
- UTF-8 encoding issues in subprocess calls across different locales

## [0.1.0] - 2025-12-07

### Added
- Email sending functionality via `btx-lib-mail>=1.0.1` integration
- Two new CLI commands: `send-email` and `send-notification`
- Email configuration support via lib_layered_config with sensible defaults
- Comprehensive email wrapper with `EmailConfig` dataclass in `mail.py`
- Email configuration validation in `__post_init__` (timeout, from_address, SMTP host:port format)
- Real SMTP integration tests using .env configuration (TEST_SMTP_SERVER, TEST_EMAIL_ADDRESS)
- 48 new tests covering email functionality:
  - 18 EmailConfig validation tests
  - 4 configuration loading tests
  - 6 email sending tests (unit)
  - 2 notification tests (unit)
  - 5 error scenario tests
  - 5 edge case tests
  - 3 real SMTP integration tests
  - 10 CLI integration tests
- `.env.example` documentation for TEST_SMTP_SERVER and TEST_EMAIL_ADDRESS
- DotEnv loading in test suite for integration test configuration

### Changed
- Extracted `_load_and_validate_email_config()` helper function to eliminate code duplication between CLI email commands
- Updated test suite from 56 to 104 passing tests
- Increased code coverage from 79% to 87.50%
- Enhanced `conftest.py` with automatic .env loading for integration tests

### Dependencies
- Added `btx-lib-mail>=1.0.1` for SMTP email sending capabilities

## [0.0.1] - 2025-11-11
- Bootstrap 

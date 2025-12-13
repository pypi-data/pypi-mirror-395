# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.


## [0.1.1] - 2025-12-08

### Fixed
- `config --format json` now outputs valid JSON by suppressing info log messages that were polluting stdout

## [0.1.0] - 2025-12-07

### Added
- `--profile` option to `config` command for loading configuration from named profiles
- `--profile` option to `config-deploy` command for deploying configuration to profile-specific directories
- Profile support enables environment isolation (e.g., `production`, `staging`, `test`)
- Profile-specific paths: `~/.config/<slug>/profile/<name>/config.toml`
- Comprehensive test coverage for profile functionality (154 tests, 93% coverage)
- Default configuration values in `defaultconfig.toml` for `[lib_log_rich]` section

### Fixed
- Windows Unicode encoding issues in CI tests (subprocess handling of emoji characters)
- Set `PYTHONIOENCODING=utf-8` in CI workflow for cross-platform compatibility

## [0.0.1] - 2025-11-11
- Bootstrap 

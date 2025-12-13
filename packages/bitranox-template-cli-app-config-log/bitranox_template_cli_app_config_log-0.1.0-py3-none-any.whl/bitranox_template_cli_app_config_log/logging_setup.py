"""Centralized logging initialization for all entry points.

Provides a single source of truth for lib_log_rich runtime configuration,
eliminating duplication between module entry (__main__.py) and console script
(cli.py) while ensuring initialization happens exactly once.

This module contains:
    - :func:`init_logging`: idempotent logging initialization with layered config.
    - :func:`_build_runtime_config`: constructs RuntimeConfig from layered sources.

Note:
    Lives in the adapters/platform layer. All entry points (module execution,
    console scripts, tests) delegate to this module for logging setup, ensuring
    consistent runtime behavior across invocation paths.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import lib_log_rich.config
import lib_log_rich.runtime

from . import __init__conf__
from .config import get_config

# Module-level storage for the runtime configuration
# Set during init_logging() for potential future use
_runtime_config: lib_log_rich.runtime.RuntimeConfig | None = None


def _get_log_config_value(log_config: Mapping[str, Any], key: str, default: Any) -> Any:
    """Extract a value from log config with a fallback default.

    Args:
        log_config: Mapping from layered config's lib_log_rich section.
        key: Configuration key to retrieve.
        default: Default value if key is not present.

    Returns:
        The configuration value or the default.
    """
    return log_config.get(key, default)


def _build_runtime_config() -> lib_log_rich.runtime.RuntimeConfig:
    """Build RuntimeConfig from layered configuration sources.

    Centralizes the mapping from lib_layered_config to lib_log_rich
    RuntimeConfig, ensuring all configuration sources (defaults, app,
    host, user, dotenv, env) are respected.

    Loads configuration via get_config() and extracts the [lib_log_rich]
    section, providing defaults for required parameters (service, environment).
    Uses typed extraction to build the RuntimeConfig.

    Returns:
        Fully configured runtime settings ready for lib_log_rich.init().

    Note:
        Configuration is read from the [lib_log_rich] section. All parameters
        documented in defaultconfig.toml can be specified. Unspecified values
        use lib_log_rich's built-in defaults. The service and environment
        parameters default to package metadata when not configured.
    """
    config = get_config()
    log_config: Mapping[str, Any] = config.get("lib_log_rich", default={})

    # Extract required parameters with application defaults
    service = _get_log_config_value(log_config, "service", __init__conf__.name)
    environment = _get_log_config_value(log_config, "environment", "prod")

    # Build config dict with required parameters, then add any additional config
    # This approach minimizes dict operations while maintaining type safety at the boundary
    runtime_kwargs: dict[str, Any] = {
        "service": service,
        "environment": environment,
    }

    # Add any additional configuration from lib_log_rich section
    # These override our defaults if present in the config
    for key, value in log_config.items():
        if key not in runtime_kwargs or key in log_config:
            runtime_kwargs[key] = value

    # Build RuntimeConfig at the system boundary
    # Note: TOML arrays are passed as lists; lib_log_rich accepts both lists and tuples
    return lib_log_rich.runtime.RuntimeConfig(**runtime_kwargs)


def init_logging() -> None:
    """Initialize lib_log_rich runtime with layered configuration if not already done.

    All entry points need logging configured, but the runtime should only
    be initialized once regardless of how many times this function is called.

    Loads .env files (to make LOG_* variables available), checks if lib_log_rich
    is already initialized, and configures it with settings from layered
    configuration sources (defaults → app → host → user → dotenv → env).
    Bridges standard Python logging to lib_log_rich for domain code compatibility.

    Note:
        Loads .env files into the process environment on first invocation.
        May initialize the global lib_log_rich runtime on first invocation.
        Subsequent calls have no effect.

        This function is safe to call multiple times. The first call loads .env
        and initializes the runtime; subsequent calls check the initialization
        state and return immediately if already initialized.

        The .env loading enables lib_log_rich to read LOG_* environment variables
        from .env files in the current directory or parent directories. This
        provides the highest precedence override mechanism for logging configuration.

        The logger_level for attach_std_logging is derived from the console_level
        configuration to ensure standard logging uses the same threshold.
    """
    if not lib_log_rich.runtime.is_initialised():
        global _runtime_config

        # Enable .env file discovery and loading before runtime initialization
        # This allows LOG_* variables from .env files to override configuration
        lib_log_rich.config.enable_dotenv()

        _runtime_config = _build_runtime_config()
        lib_log_rich.runtime.init(_runtime_config)
        lib_log_rich.runtime.attach_std_logging()


__all__ = [
    "init_logging",
]

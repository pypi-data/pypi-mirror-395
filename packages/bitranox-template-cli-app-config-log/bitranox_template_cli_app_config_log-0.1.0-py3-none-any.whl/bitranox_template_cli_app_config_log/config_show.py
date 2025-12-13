"""Configuration display functionality for CLI config command.

Provides the business logic for displaying merged configuration from all
sources in human-readable or JSON format. Keeps CLI layer thin by handling
all formatting and display logic here.

This module contains:
    - :func:`display_config`: displays configuration in requested format.

Note:
    Lives in the behaviors layer. The CLI command delegates to this module for
    all configuration display logic, keeping presentation concerns separate from
    command-line argument parsing.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, cast

import click

from .config import get_config
from .enums import OutputFormat


def _format_value(value: Any) -> str:
    """Format a configuration value for human-readable output.

    Args:
        value: The configuration value to format.

    Returns:
        Formatted string representation suitable for display.
    """
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, (list, Mapping)):
        return json.dumps(value)
    return str(value)


def _display_section_items(section_data: Mapping[str, Any]) -> None:
    """Display items within a configuration section.

    Args:
        section_data: Mapping of key-value pairs to display.
    """
    for key, value in section_data.items():
        click.echo(f"  {key} = {_format_value(value)}")


def _display_section(section_name: str, section_data: Mapping[str, Any] | Any) -> None:
    """Display a single configuration section with its header.

    Args:
        section_name: Name of the section to display.
        section_data: Data within the section (typically a mapping).
    """
    click.echo(f"\n[{section_name}]")
    if isinstance(section_data, Mapping):
        _display_section_items(cast(Mapping[str, Any], section_data))
    else:
        click.echo(f"  {section_data}")


def _emit_section_not_found(section: str) -> None:
    """Emit error message for missing section and exit.

    Args:
        section: Name of the section that was not found.

    Raises:
        SystemExit: Always raises with code 1.
    """
    click.echo(f"Section '{section}' not found or empty", err=True)
    raise SystemExit(1)


def display_config(
    *,
    format: OutputFormat = OutputFormat.HUMAN,
    section: str | None = None,
    profile: str | None = None,
) -> None:
    """Display the current merged configuration from all sources.

    Provides visibility into the effective configuration loaded from
    defaults, app configs, host configs, user configs, .env files, and
    environment variables. Loads configuration via get_config() and outputs
    it in the requested format.

    Args:
        format: Output format enum: HUMAN for TOML-like display or JSON for JSON.
            Defaults to OutputFormat.HUMAN.
        section: Optional section name to display only that section. When None,
            displays all configuration.
        profile: Optional profile name for environment isolation. When specified,
            loads configuration from profile-specific subdirectories
            (e.g., ~/.config/slug/profile/<name>/config.toml).

    Raises:
        SystemExit: With code 1 if requested section doesn't exist.

    Note:
        Writes formatted configuration to stdout via click.echo().
        The human-readable format mimics TOML syntax for consistency with the
        configuration file format. JSON format provides machine-readable output
        suitable for parsing by other tools.

    Example:
        >>> display_config()  # doctest: +SKIP
        [lib_log_rich]
          service = "bitranox_template_cli_app_config_log"
          environment = "prod"

        >>> display_config(format=OutputFormat.JSON)  # doctest: +SKIP
        {
          "lib_log_rich": {
            "service": "bitranox_template_cli_app_config_log",
            "environment": "prod"
          }
        }

        >>> display_config(profile="production")  # doctest: +SKIP
    """
    config = get_config(profile=profile)

    if format == OutputFormat.JSON:
        _display_json_format(config, section)
    else:
        _display_human_format(config, section)


def _display_json_format(config: Any, section: str | None) -> None:
    """Display configuration in JSON format.

    Args:
        config: The configuration object from lib_layered_config.
        section: Optional section to filter output.

    Raises:
        SystemExit: With code 1 if section not found.
    """
    if section:
        section_data = config.get(section, default={})
        if section_data:
            click.echo(json.dumps({section: section_data}, indent=2))
        else:
            _emit_section_not_found(section)
    else:
        click.echo(config.to_json(indent=2))


def _display_human_format(config: Any, section: str | None) -> None:
    """Display configuration in human-readable format.

    Args:
        config: The configuration object from lib_layered_config.
        section: Optional section to filter output.

    Raises:
        SystemExit: With code 1 if section not found.
    """
    if section:
        section_data = config.get(section, default={})
        if section_data:
            _display_section(section, section_data)
        else:
            _emit_section_not_found(section)
    else:
        config_data = config.as_dict()
        for section_name, section_data in config_data.items():
            _display_section(section_name, section_data)


__all__ = [
    "display_config",
]

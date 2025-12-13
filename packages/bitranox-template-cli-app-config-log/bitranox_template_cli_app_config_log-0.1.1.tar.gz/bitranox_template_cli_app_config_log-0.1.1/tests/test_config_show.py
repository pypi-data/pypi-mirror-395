"""Configuration display tests: each format tells a clear story.

Unit tests for the config_show module covering:
- JSON and human format output
- Section filtering
- Error handling for missing sections

Tests use controlled mock configs to verify formatting behavior.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from bitranox_template_cli_app_config_log import config_show
from bitranox_template_cli_app_config_log.enums import OutputFormat


def _make_mock_get_config(mock_config: MagicMock) -> Any:
    """Create a typed mock for get_config that accepts profile parameter."""

    def mock_get_config(*, profile: str | None = None, start_dir: str | None = None) -> MagicMock:
        return mock_config

    return mock_get_config


# =============================================================================
# Display Config Human Format Tests
# =============================================================================


@pytest.mark.os_agnostic
class TestDisplayConfigHumanFormat:
    """Tests for display_config with human format."""

    def test_displays_section_header(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When human format is used, section headers appear in brackets."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"my_section": {"key": "value"}}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert "[my_section]" in captured.out

    def test_displays_string_value_quoted(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When a string value is displayed, it is quoted."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"name": "test"}}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert 'name = "test"' in captured.out

    def test_displays_integer_value_unquoted(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When an integer value is displayed, it is not quoted."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"count": 42}}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert "count = 42" in captured.out

    def test_displays_list_value_as_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When a list value is displayed, it appears as JSON."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"items": ["a", "b"]}}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert '["a", "b"]' in captured.out

    def test_displays_dict_value_as_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When a nested dict value is displayed, it appears as JSON."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"nested": {"inner": "value"}}}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert '{"inner": "value"}' in captured.out

    def test_displays_non_mapping_section_directly(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When section data is not a mapping, it is displayed directly."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"simple": "just a string"}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert "[simple]" in captured.out
        assert "just a string" in captured.out

    def test_displays_multiple_sections(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When multiple sections exist, all are displayed."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {
            "section1": {"key1": "value1"},
            "section2": {"key2": "value2"},
        }
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN)

        captured = capsys.readouterr()
        assert "[section1]" in captured.out
        assert "[section2]" in captured.out


@pytest.mark.os_agnostic
class TestDisplayConfigHumanFormatWithSection:
    """Tests for display_config human format with section filter."""

    def test_displays_only_requested_section(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When a section is specified, only that section appears."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"setting": "filtered"}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.HUMAN, section="my_section")

        captured = capsys.readouterr()
        assert "[my_section]" in captured.out
        assert 'setting = "filtered"' in captured.out


# =============================================================================
# Display Config JSON Format Tests
# =============================================================================


@pytest.mark.os_agnostic
class TestDisplayConfigJsonFormat:
    """Tests for display_config with JSON format."""

    def test_displays_json_output(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When JSON format is used, JSON is output."""
        mock_config = MagicMock()
        mock_config.to_json.return_value = '{"section": {"key": "value"}}'
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.JSON)

        captured = capsys.readouterr()
        assert '{"section": {"key": "value"}}' in captured.out


@pytest.mark.os_agnostic
class TestDisplayConfigJsonFormatWithSection:
    """Tests for display_config JSON format with section filter."""

    def test_displays_filtered_json(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When JSON format with section is used, filtered JSON appears."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"setting": "filtered"}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        config_show.display_config(format=OutputFormat.JSON, section="my_section")

        captured = capsys.readouterr()
        assert "my_section" in captured.out
        assert "filtered" in captured.out


# =============================================================================
# Display Config Error Handling Tests
# =============================================================================


@pytest.mark.os_agnostic
class TestDisplayConfigSectionNotFound:
    """Tests for section not found error handling."""

    def test_human_format_missing_section_raises_exit(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When section is not found in human format, SystemExit is raised."""
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        with pytest.raises(SystemExit) as exc:
            config_show.display_config(format=OutputFormat.HUMAN, section="missing")

        assert exc.value.code == 1

    def test_json_format_missing_section_raises_exit(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When section is not found in JSON format, SystemExit is raised."""
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        with pytest.raises(SystemExit) as exc:
            config_show.display_config(format=OutputFormat.JSON, section="missing")

        assert exc.value.code == 1

    def test_missing_section_shows_error_message(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When section is not found, error message appears in stderr."""
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        monkeypatch.setattr(config_show, "get_config", _make_mock_get_config(mock_config))

        with pytest.raises(SystemExit):
            config_show.display_config(section="nonexistent")

        captured = capsys.readouterr()
        assert "nonexistent" in captured.err
        assert "not found or empty" in captured.err


# =============================================================================
# Display Config Profile Tests
# =============================================================================


@pytest.mark.os_agnostic
class TestDisplayConfigProfile:
    """Tests for display_config with profile parameter."""

    def test_profile_is_passed_to_get_config(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When profile is specified, it is passed to get_config."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"key": "value"}}
        captured_profile: list[str | None] = []

        def capturing_get_config(*, profile: str | None = None, start_dir: str | None = None) -> MagicMock:
            captured_profile.append(profile)
            return mock_config

        monkeypatch.setattr(config_show, "get_config", capturing_get_config)

        config_show.display_config(format=OutputFormat.HUMAN, profile="production")

        assert captured_profile == ["production"]

    def test_profile_none_is_passed_when_not_specified(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """When profile is not specified, None is passed to get_config."""
        mock_config = MagicMock()
        mock_config.as_dict.return_value = {"section": {"key": "value"}}
        captured_profile: list[str | None] = []

        def capturing_get_config(*, profile: str | None = None, start_dir: str | None = None) -> MagicMock:
            captured_profile.append(profile)
            return mock_config

        monkeypatch.setattr(config_show, "get_config", capturing_get_config)

        config_show.display_config(format=OutputFormat.HUMAN)

        assert captured_profile == [None]

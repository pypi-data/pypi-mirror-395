import argparse

import pytest

from argparse_boost import BoostedArgumentParser


@pytest.fixture()
def sut():
    """Default EnvArgumentParser with TEST_ prefix for testing."""
    return BoostedArgumentParser(prog="test", env_prefix="TEST_")


@pytest.fixture()
def make_sut():
    """Factory for creating EnvArgumentParser with custom configuration."""

    def _make(env_prefix="TEST_", prog="test", **kwargs):
        return BoostedArgumentParser(prog=prog, env_prefix=env_prefix, **kwargs)

    return _make


def test_env_section_appears_when_env_variables_set(sut, monkeypatch):
    """ENV section should appear in help when environment variables are set."""
    # Arrange
    sut.add_argument("--log-level", default="INFO", help="Logging level")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert "--log-level" in help_output
    assert "TEST_LOG_LEVEL=DEBUG" in help_output


def test_env_section_not_shown_when_no_env_variables_set(sut):
    """ENV section should not appear when no environment variables are set."""
    # Arrange
    sut.add_argument("--log-level", default="INFO", help="Logging level")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_respects_env_prefix(make_sut, monkeypatch):
    """ENV section should use correct prefix when converting option names."""
    # Arrange
    parser = make_sut(env_prefix="MYAPP_")
    parser.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("MYAPP_LOG_LEVEL", "DEBUG")

    # Act
    help_output = parser.format_help()

    # Assert
    assert "MYAPP_LOG_LEVEL=DEBUG" in help_output
    assert "TEST_LOG_LEVEL" not in help_output


def test_env_section_without_prefix(make_sut, monkeypatch):
    """ENV section should work without prefix."""
    # Arrange
    parser = make_sut(env_prefix="")
    parser.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")

    # Act
    help_output = parser.format_help()

    # Assert
    assert "LOG_LEVEL=WARNING" in help_output


def test_env_section_shows_multiple_variables(sut, monkeypatch):
    """ENV section should show all set environment variables."""
    # Arrange
    sut.add_argument("--log-level", default="INFO")
    sut.add_argument("--output-dir", default="/tmp")  # noqa: S108
    sut.add_argument("--batch-size", type=int, default=100)
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TEST_OUTPUT_DIR", "/var/data")
    monkeypatch.setenv("TEST_BATCH_SIZE", "500")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert "TEST_LOG_LEVEL=DEBUG" in help_output
    assert "TEST_OUTPUT_DIR=/var/data" in help_output
    assert "TEST_BATCH_SIZE=500" in help_output


def test_env_section_only_shows_long_options(sut, monkeypatch):
    """ENV section should only process --long-form options, not -short."""
    # Arrange
    sut.add_argument("-l", "--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "--log-level" in help_output
    assert "TEST_LOG_LEVEL=DEBUG" in help_output
    # ENV section should show --log-level (long form), not -l (short form)
    env_section = help_output.split("Environment variables set:")[1]
    assert "--log-level" in env_section
    assert "TEST_LOG_LEVEL=DEBUG" in env_section
    # The line in ENV section should not start with -l
    env_lines = [line for line in env_section.split("\n") if "TEST_LOG_LEVEL" in line]
    assert len(env_lines) == 1
    assert env_lines[0].strip().startswith("--log-level")


def test_env_section_ignores_short_only_options(sut, monkeypatch):
    """ENV section should not process arguments with only short form."""
    # Arrange
    sut.add_argument("-v", action="store_true")
    monkeypatch.setenv("TEST_V", "true")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_truncates_long_values(sut, monkeypatch):
    """Values longer than 50 characters should be truncated with ellipsis."""
    # Arrange
    sut.add_argument("--api-key", default="")
    long_value = "x" * 100
    monkeypatch.setenv("TEST_API_KEY", long_value)

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert f"TEST_API_KEY={'x' * 47}..." in help_output
    assert long_value not in help_output


def test_env_section_does_not_truncate_short_values(sut, monkeypatch):
    """Values exactly 50 characters or less should not be truncated."""
    # Arrange
    sut.add_argument("--value", default="")
    value_50 = "x" * 50
    monkeypatch.setenv("TEST_VALUE", value_50)

    # Act
    help_output = sut.format_help()

    # Assert
    assert f"TEST_VALUE={value_50}" in help_output
    assert "..." not in help_output.split("TEST_VALUE=")[1].split("\n")[0]


def test_env_section_aligns_columns(sut, monkeypatch):
    """Option names should be aligned for readability."""
    # Arrange
    sut.add_argument("--a", default="1")
    sut.add_argument("--very-long-option", default="2")
    monkeypatch.setenv("TEST_A", "value1")
    monkeypatch.setenv("TEST_VERY_LONG_OPTION", "value2")

    # Act
    help_output = sut.format_help()

    # Assert
    env_lines = [
        line
        for line in help_output.split("\n")
        if line.strip().startswith("--") and "TEST_" in line
    ]
    assert len(env_lines) == 2
    # Both lines should start with "  " (two spaces)
    assert all(line.startswith("  ") for line in env_lines)
    # Verify alignment by checking spacing
    # --a should be padded to match --very-long-option width
    assert "  --a                 TEST_A=value1" in help_output
    assert "  --very-long-option  TEST_VERY_LONG_OPTION=value2" in help_output


def test_env_section_converts_dashes_to_underscores(sut, monkeypatch):
    """Option with multiple dashes should convert all to underscores."""
    # Arrange
    sut.add_argument("--some-long-option-name", default="value")
    monkeypatch.setenv("TEST_SOME_LONG_OPTION_NAME", "custom")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "TEST_SOME_LONG_OPTION_NAME=custom" in help_output


def test_env_section_appears_at_end_of_help(sut, monkeypatch):
    """ENV section should appear after the main help text."""
    # Arrange
    sut.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    # Standard help sections come first
    assert help_output.index("usage:") < help_output.index("Environment variables set:")
    # ENV section should be near the end
    env_section_pos = help_output.index("Environment variables set:")
    assert env_section_pos > len(help_output) * 0.5


def test_env_section_ignores_boolean_store_true_flags(sut, monkeypatch):
    """Boolean store_true flags should not appear in ENV section."""
    # Arrange
    sut.add_argument("--verbose", action="store_true")
    monkeypatch.setenv("TEST_VERBOSE", "true")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_ignores_boolean_store_false_flags(sut, monkeypatch):
    """Boolean store_false flags should not appear in ENV section."""
    # Arrange
    sut.add_argument("--quiet", action="store_false")
    monkeypatch.setenv("TEST_QUIET", "false")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_ignores_store_const_actions(sut, monkeypatch):
    """Store const actions should not appear in ENV section."""
    # Arrange
    sut.add_argument("--const-opt", action="store_const", const=42)
    monkeypatch.setenv("TEST_CONST_OPT", "100")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_ignores_count_actions(sut, monkeypatch):
    """Count actions should not appear in ENV section."""
    # Arrange
    sut.add_argument("--verbose", "-v", action="count")
    monkeypatch.setenv("TEST_VERBOSE", "3")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_only_shows_one_option_per_action(sut, monkeypatch):
    """When action has both short and long forms, only show long form once."""
    # Arrange
    sut.add_argument("-l", "--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    env_lines = [line for line in help_output.split("\n") if "TEST_LOG_LEVEL" in line]
    # Should only appear once in ENV section
    assert len(env_lines) == 1


def test_env_section_with_subparsers_shows_parent_env_vars(make_sut, monkeypatch):
    """Subparser help should show parent ENV variables."""
    # Arrange
    parent = make_sut(env_prefix="MYAPP_")
    parent.add_argument("--global-opt", default="global_default")

    subparsers = parent.add_subparsers(dest="command")
    child = subparsers.add_parser("build")
    child.add_argument("--output", default="out")

    monkeypatch.setenv("MYAPP_GLOBAL_OPT", "global_from_env")
    monkeypatch.setenv("MYAPP_OUTPUT", "custom_out")

    # Act
    help_output = child.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert "MYAPP_OUTPUT=custom_out" in help_output


def test_env_section_with_mixed_set_and_unset_variables(sut, monkeypatch):
    """ENV section should only show variables that are actually set."""
    # Arrange
    sut.add_argument("--option-a", default="value_a")
    sut.add_argument("--option-b", default="value_b")
    sut.add_argument("--option-c", default="value_c")
    monkeypatch.setenv("TEST_OPTION_A", "custom_a")
    monkeypatch.setenv("TEST_OPTION_C", "custom_c")
    # TEST_OPTION_B is not set

    # Act
    help_output = sut.format_help()

    # Assert
    assert "TEST_OPTION_A=custom_a" in help_output
    assert "TEST_OPTION_C=custom_c" in help_output
    assert "TEST_OPTION_B" not in help_output


def test_env_section_with_empty_string_value(sut, monkeypatch):
    """Empty string environment variable should be shown."""
    # Arrange
    sut.add_argument("--value", default="default")
    monkeypatch.setenv("TEST_VALUE", "")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert "TEST_VALUE=" in help_output


def test_env_section_with_special_characters_in_value(sut, monkeypatch):
    """Values with special characters should be displayed correctly."""
    # Arrange
    sut.add_argument("--path", default="/tmp")  # noqa: S108
    monkeypatch.setenv("TEST_PATH", "/path/with spaces/and-dashes")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "TEST_PATH=/path/with spaces/and-dashes" in help_output


def test_env_section_with_numeric_values(sut, monkeypatch):
    """Numeric values should be displayed as strings."""
    # Arrange
    sut.add_argument("--port", type=int, default=8080)
    monkeypatch.setenv("TEST_PORT", "3000")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "TEST_PORT=3000" in help_output


def test_env_section_format_matches_specification(sut, monkeypatch):
    """ENV section format should match expected layout."""
    # Arrange
    sut.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    # Should have header
    assert "\nEnvironment variables set:\n" in help_output
    # Should have entry with proper indentation and format
    assert "  --log-level  TEST_LOG_LEVEL=DEBUG" in help_output


def test_env_section_with_no_arguments_defined(make_sut, monkeypatch):
    """Parser with no arguments should not show ENV section."""
    # Arrange
    parser = make_sut()
    monkeypatch.setenv("TEST_RANDOM_VAR", "value")

    # Act
    help_output = parser.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_with_positional_arguments_only(sut, monkeypatch):
    """Parser with only positional arguments should not show ENV section."""
    # Arrange
    sut.add_argument("filename")
    monkeypatch.setenv("TEST_FILENAME", "test.txt")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" not in help_output


def test_env_section_shows_first_long_option_when_multiple_long_forms(sut, monkeypatch):
    """When action has multiple long options, show the first one."""
    # Arrange
    sut.add_argument("--log-level", "--level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    help_output = sut.format_help()

    # Assert
    env_section = help_output.split("Environment variables set:")[1]
    # Should show --log-level (first long option)
    assert "--log-level" in env_section
    assert "TEST_LOG_LEVEL=DEBUG" in env_section


def test_format_help_omits_env_section_when_no_vars(sut):
    """_format_env_section should return empty string when no ENV vars set."""
    # Arrange
    sut.add_argument("--log-level", default="INFO")

    # Act
    result = sut.format_help()

    # Assert
    assert "Environment variables set" not in result


def test_format_help_renders_env_section_when_vars_set(
    sut,
    monkeypatch,
):
    """_format_env_section should return formatted string when ENV vars exist."""
    # Arrange
    sut.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    result = sut.format_help()

    # Assert
    assert "Environment variables set" in result
    assert "TEST_LOG_LEVEL=DEBUG" in result
    assert result.endswith("\n")


def test_env_section_with_argparse_suppress_default(sut, monkeypatch):
    """Arguments with SUPPRESS default should still show in ENV section if var set."""
    # Arrange
    sut.add_argument("--value", default=argparse.SUPPRESS)
    monkeypatch.setenv("TEST_VALUE", "custom")

    # Act
    help_output = sut.format_help()

    # Assert
    assert "Environment variables set:" in help_output
    assert "TEST_VALUE=custom" in help_output

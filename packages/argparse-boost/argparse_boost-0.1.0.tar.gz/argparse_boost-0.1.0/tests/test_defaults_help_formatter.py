import argparse

import pytest

from argparse_boost import DefaultsHelpFormatter


@pytest.fixture()
def parser_with_formatter():
    """ArgumentParser using DefaultsHelpFormatter."""
    return argparse.ArgumentParser(formatter_class=DefaultsHelpFormatter)


def test_help_formatter_appends_required_suffix(parser_with_formatter):
    """Required arguments should display 'Required' suffix in help text."""
    # Arrange
    parser_with_formatter.add_argument("--name", required=True, help="Your name")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--name" in help_output
    assert "Your name. Required" in help_output


def test_help_formatter_strips_trailing_dot_before_required(parser_with_formatter):
    """Required suffix should not create double periods."""
    # Arrange
    parser_with_formatter.add_argument("--name", required=True, help="Your name.")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "Your name. Required" in help_output
    assert "Your name.. Required" not in help_output


def test_help_formatter_appends_default_value(parser_with_formatter):
    """Arguments with defaults should display 'Default: <value>' suffix."""
    # Arrange
    parser_with_formatter.add_argument("--level", default="INFO", help="Log level")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--level" in help_output
    assert "Log level. Default: INFO" in help_output


def test_help_formatter_strips_trailing_dot_before_default(parser_with_formatter):
    """Default suffix should not create double periods."""
    # Arrange
    parser_with_formatter.add_argument("--level", default="INFO", help="Log level.")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "Log level. Default: INFO" in help_output
    assert "Log level.. Default: INFO" not in help_output


def test_help_formatter_skips_none_default(parser_with_formatter):
    """Arguments with None default should not show default value."""
    # Arrange
    parser_with_formatter.add_argument("--name", default=None, help="Your name")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--name" in help_output
    assert "Your name" in help_output
    name_lines = [line for line in help_output.split("\n") if "--name" in line]
    assert len(name_lines) > 0
    assert "Default:" not in name_lines[0]


def test_help_formatter_skips_suppress_default(parser_with_formatter):
    """Arguments with SUPPRESS default should not show default value."""
    # Arrange
    parser_with_formatter.add_argument(
        "--name",
        default=argparse.SUPPRESS,
        help="Your name",
    )

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--name" in help_output
    assert "Your name" in help_output
    name_lines = [line for line in help_output.split("\n") if "--name" in line]
    assert len(name_lines) > 0
    assert "Default:" not in name_lines[0]


def test_help_formatter_avoids_duplicate_default_placeholder(parser_with_formatter):
    """Should not duplicate default value when %(default)s already present."""
    # Arrange
    parser_with_formatter.add_argument(
        "--level",
        default="INFO",
        help="Log level (default: %(default)s)",
    )

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--level" in help_output
    assert help_output.count("INFO") == 1
    assert "Log level (default: INFO)" in help_output


def test_help_formatter_handles_empty_help_text(parser_with_formatter):
    """Empty help text should not cause errors or show default."""
    # Arrange
    parser_with_formatter.add_argument("--name", default="test", help="")

    # Act
    help_output = parser_with_formatter.format_help()

    # Assert
    assert "--name" in help_output
    assert "Default: test" not in help_output

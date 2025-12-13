import argparse

import pytest

from argparse_boost import BoostedArgumentParser


@pytest.fixture()
def make_parser():
    def maker(env_prefix: str = ""):
        return BoostedArgumentParser(prog="test", env_prefix=env_prefix)

    return maker


@pytest.fixture()
def parser(make_parser):
    return make_parser(env_prefix="TEST_")


@pytest.fixture()
def parser_no_prefix(make_parser):
    return make_parser(env_prefix="")


def test_parser_stores_env_prefix(parser):
    """EnvArgumentParser should store the provided env_prefix."""
    assert parser.env_prefix == "TEST_"


def test_parser_converts_option_to_env_var_name_with_prefix(
    parser,
    monkeypatch,
):
    """Option --log-level should map to TEST_LOG_LEVEL environment variable."""
    # Arrange
    parser.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.log_level == "DEBUG"


def test_parser_converts_option_to_env_var_name_without_prefix(
    parser_no_prefix,
    monkeypatch,
):
    """Without prefix, --log-level should map to LOG_LEVEL environment variable."""
    # Arrange
    parser_no_prefix.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    # Act
    args = parser_no_prefix.parse_args([])

    # Assert
    assert args.log_level == "DEBUG"


def test_parser_handles_multiple_dashes(parser, monkeypatch):
    """Multi-word options should convert all dashes to underscores."""
    # Arrange
    parser.add_argument("--some-long-option", default="value1")
    monkeypatch.setenv("TEST_SOME_LONG_OPTION", "value2")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.some_long_option == "value2"


def test_parser_applies_env_var_to_default(parser, monkeypatch):
    """Environment variable should override argument default."""
    # Arrange
    parser.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.log_level == "DEBUG"


def test_parser_cli_arg_overrides_env_var(parser, monkeypatch):
    """CLI argument should take priority over environment variable."""
    # Arrange
    parser.add_argument("--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "DEBUG")

    # Act
    args = parser.parse_args(["--log-level", "WARNING"])

    # Assert
    assert args.log_level == "WARNING"


def test_parser_uses_default_when_no_env_var(parser):
    """Without environment variable, should use original default value."""
    # Arrange
    parser.add_argument("--log-level", default="INFO")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.log_level == "INFO"


def test_parser_ignores_short_options(parser, monkeypatch):
    """Short-form options should not be mapped to environment variables."""
    # Arrange
    parser.add_argument("-l", "--log-level", default="INFO")
    monkeypatch.setenv("TEST_L", "DEBUG")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.log_level == "INFO"


def test_parser_processes_long_option_when_short_exists(parser, monkeypatch):
    """Long-form option should work even when short-form is also defined."""
    # Arrange
    parser.add_argument("-l", "--log-level", default="INFO")
    monkeypatch.setenv("TEST_LOG_LEVEL", "WARNING")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.log_level == "WARNING"


def test_parser_skips_store_true_action(parser, monkeypatch):
    """Boolean store_true flags should not be affected by environment variables."""
    # Arrange
    parser.add_argument("--verbose", action="store_true", default=False)
    monkeypatch.setenv("TEST_VERBOSE", "true")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.verbose is False


def test_parser_skips_store_false_action(parser, monkeypatch):
    """Boolean store_false flags should not be affected by environment variables."""
    # Arrange
    parser.add_argument("--quiet", action="store_false", default=True)
    monkeypatch.setenv("TEST_QUIET", "false")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.quiet is True


def test_parser_skips_store_const_action(parser, monkeypatch):
    """Const actions should not be affected by environment variables."""
    # Arrange
    parser.add_argument("--const-opt", action="store_const", const=42, default=0)
    monkeypatch.setenv("TEST_CONST_OPT", "100")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.const_opt == 0


def test_parser_skips_count_action(parser, monkeypatch):
    """Count actions should not be affected by environment variables."""
    # Arrange
    parser.add_argument("--verbose", "-v", action="count", default=0)
    monkeypatch.setenv("TEST_VERBOSE", "3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.verbose == 0


def test_parser_converts_int_type(parser, monkeypatch):
    """Environment variable string should be converted to int when type specified."""
    # Arrange
    parser.add_argument("--count", type=int, default=10)
    monkeypatch.setenv("TEST_COUNT", "42")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.count == 42
    assert isinstance(args.count, int)


def test_parser_raises_error_for_invalid_int(parser, monkeypatch):
    """Invalid int conversion should raise SystemExit."""
    # Arrange
    parser.add_argument("--count", type=int, default=10)
    monkeypatch.setenv("TEST_COUNT", "not_a_number")

    # Act & Assert
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_validates_choices_accepts_valid(parser, monkeypatch):
    """Environment variable value in choices should be accepted."""
    # Arrange
    parser.add_argument("--level", choices=["INFO", "DEBUG", "WARNING"])
    monkeypatch.setenv("TEST_LEVEL", "DEBUG")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.level == "DEBUG"


def test_parser_validates_choices_rejects_invalid(parser, monkeypatch):
    """Environment variable value not in choices should raise SystemExit."""
    # Arrange
    parser.add_argument("--level", choices=["INFO", "DEBUG", "WARNING"])
    monkeypatch.setenv("TEST_LEVEL", "INVALID")

    # Act & Assert
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_subparsers_inherit_env_prefix():
    """Child parsers created via add_parser should inherit parent env_prefix."""
    # Arrange
    parent = BoostedArgumentParser(prog="parent", env_prefix="MYAPP_")
    subparsers = parent.add_subparsers(dest="command")

    # Act
    child = subparsers.add_parser("child")

    # Assert
    assert isinstance(child, BoostedArgumentParser)
    assert child.env_prefix == "MYAPP_"


def test_subparsers_use_env_argument_parser_by_default(parser):
    """Subparsers should auto-inject EnvArgumentParser as parser_class."""
    # Arrange
    subparsers = parser.add_subparsers(dest="command")

    # Act
    child = subparsers.add_parser("cmd")

    # Assert
    assert isinstance(child, BoostedArgumentParser)


def test_subparsers_respect_custom_parser_class(parser):
    """Explicit parser_class parameter should override EnvArgumentParser."""
    # Arrange
    subparsers = parser.add_subparsers(
        dest="command",
        parser_class=argparse.ArgumentParser,
    )

    # Act
    child = subparsers.add_parser("cmd")

    # Assert
    assert isinstance(child, argparse.ArgumentParser)
    assert type(child).__name__ == "ArgumentParser"


def test_subparsers_allow_env_prefix_override(make_parser):
    """Explicitly passing env_prefix to add_parser should override parent prefix."""
    # Arrange
    parent = make_parser(env_prefix="PARENT_")
    subparsers = parent.add_subparsers(dest="command")

    # Act
    child = subparsers.add_parser("child", env_prefix="CHILD_")

    # Assert
    assert isinstance(child, BoostedArgumentParser)
    assert child.env_prefix == "CHILD_"


def test_subparser_applies_env_vars_with_inherited_prefix(monkeypatch, make_parser):
    """Subcommand arguments should respect inherited env_prefix."""
    # Arrange
    parent = make_parser(env_prefix="MYAPP_")
    parent.add_argument("--global-opt", default="global_default")

    subparsers = parent.add_subparsers(dest="command", required=True)
    child = subparsers.add_parser("build")
    child.add_argument("--output", default="out")

    monkeypatch.setenv("MYAPP_GLOBAL_OPT", "global_from_env")
    monkeypatch.setenv("MYAPP_OUTPUT", "custom_out")

    # Act
    args = parent.parse_args(["build"])

    # Assert
    assert args.global_opt == "global_from_env"
    assert args.output == "custom_out"


def test_env_vars_applied_without_cli_args(monkeypatch, make_parser):
    """Environment variables should work when no CLI arguments provided."""
    # Arrange
    parent = make_parser(env_prefix="MYAPP_")
    parent.add_argument("--global-opt", default="global_default")

    monkeypatch.setenv("MYAPP_GLOBAL_OPT", "global_from_env")

    # Act
    args = parent.parse_args([])

    # Assert
    assert args.global_opt == "global_from_env"

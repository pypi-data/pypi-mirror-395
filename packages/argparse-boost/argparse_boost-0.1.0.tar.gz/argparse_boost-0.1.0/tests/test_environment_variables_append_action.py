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


def test_append_action_splits_comma_separated_values(parser, monkeypatch):
    """Comma-separated ENV values should be split into list."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]


def test_append_action_with_single_value(parser, monkeypatch):
    """Single value in ENV should work correctly."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "single")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["single"]


def test_append_action_with_empty_env_var(parser, monkeypatch):
    """Empty ENV value should result in no values added."""
    # Arrange
    parser.add_argument("--items", action="append", default=None)
    monkeypatch.setenv("TEST_ITEMS", "")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items is None


def test_append_action_strips_whitespace(parser, monkeypatch):
    """Whitespace around values should be stripped."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1, 2 , 3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]


def test_append_action_filters_empty_values(parser, monkeypatch):
    """Empty values from multiple commas should be filtered out."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,,2,")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2"]


def test_append_action_with_spaces_in_values(parser, monkeypatch):
    """Values containing spaces should be preserved."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "hello world,foo bar")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["hello world", "foo bar"]


def test_append_action_with_only_whitespace(parser, monkeypatch):
    """ENV with only whitespace should result in no values."""
    # Arrange
    parser.add_argument("--items", action="append", default=None)
    monkeypatch.setenv("TEST_ITEMS", "  ,  ,  ")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items is None


def test_append_action_with_int_type(parser, monkeypatch):
    """Integer type conversion should work correctly."""
    # Arrange
    parser.add_argument("--nums", action="append", type=int)
    monkeypatch.setenv("TEST_NUMS", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.nums == [1, 2, 3]


def test_append_action_with_float_type(parser, monkeypatch):
    """Float type conversion should work correctly."""
    # Arrange
    parser.add_argument("--values", action="append", type=float)
    monkeypatch.setenv("TEST_VALUES", "1.5,2.7,3.9")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.values == [1.5, 2.7, 3.9]


def test_append_action_invalid_type_raises_error(parser, monkeypatch):
    """Invalid type conversion should raise error."""
    # Arrange
    parser.add_argument("--nums", action="append", type=int)
    monkeypatch.setenv("TEST_NUMS", "a,b,c")

    # Act & Assert
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_append_action_cli_overrides_env_completely(parser, monkeypatch):
    """CLI values should completely override ENV values."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    args = parser.parse_args(["--items=4"])

    # Assert
    assert args.items == ["4"]


def test_append_action_env_used_when_no_cli(parser, monkeypatch):
    """ENV values should be used when no CLI args provided."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]


def test_append_action_cli_only_when_env_not_set(parser):
    """CLI-only values should work when ENV not set."""
    # Arrange
    parser.add_argument("--items", action="append")

    # Act
    args = parser.parse_args(["--items=1", "--items=2"])

    # Assert
    assert args.items == ["1", "2"]


def test_append_action_multiple_cli_values_override_env(parser, monkeypatch):
    """Multiple CLI values should completely replace ENV."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "a,b,c")

    # Act
    args = parser.parse_args(["--items=x", "--items=y"])

    # Assert
    assert args.items == ["x", "y"]


def test_append_action_with_none_default(parser, monkeypatch):
    """ENV values should work with None default."""
    # Arrange
    parser.add_argument("--items", action="append", default=None)
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]


def test_append_action_no_env_no_cli_uses_default(parser):
    """Default should be used when neither ENV nor CLI provided."""
    # Arrange
    parser.add_argument("--items", action="append", default=None)

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items is None


def test_multiple_append_actions(parser, monkeypatch):
    """Multiple append arguments should work independently."""
    # Arrange
    parser.add_argument("--items", action="append")
    parser.add_argument("--values", action="append")
    monkeypatch.setenv("TEST_ITEMS", "a,b,c")
    monkeypatch.setenv("TEST_VALUES", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["a", "b", "c"]
    assert args.values == ["1", "2", "3"]


def test_append_and_store_actions_together(parser, monkeypatch):
    """Append and store actions should work together."""
    # Arrange
    parser.add_argument("--items", action="append")
    parser.add_argument("--name")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")
    monkeypatch.setenv("TEST_NAME", "test_name")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]
    assert args.name == "test_name"


def test_append_action_without_prefix(parser_no_prefix, monkeypatch):
    """Append action should work without ENV prefix."""
    # Arrange
    parser_no_prefix.add_argument("--items", action="append")
    monkeypatch.setenv("ITEMS", "1,2,3")

    # Act
    args = parser_no_prefix.parse_args([])

    # Assert
    assert args.items == ["1", "2", "3"]


def test_append_const_ignored_by_env_parser(parser, monkeypatch):
    """append_const should be ignored by ENV parser."""
    # Arrange
    parser.add_argument("--verbose", action="append_const", const="v")
    monkeypatch.setenv("TEST_VERBOSE", "value")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.verbose is None


def test_append_const_works_with_cli(parser):
    """append_const should still work from CLI."""
    # Arrange
    parser.add_argument("--verbose", action="append_const", const="v")

    # Act
    args = parser.parse_args(["--verbose", "--verbose"])

    # Assert
    assert args.verbose == ["v", "v"]


def test_append_action_shown_in_help_section(parser, monkeypatch, capsys):
    """Append action ENV values should be shown in help."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])

    # Assert
    captured = capsys.readouterr()
    assert "TEST_ITEMS=1,2,3" in captured.out


def test_append_action_long_value_truncated_in_help(parser, monkeypatch, capsys):
    """Long comma-separated values should be truncated in help."""
    # Arrange
    parser.add_argument("--items", action="append")
    long_value = ",".join([str(i) for i in range(100)])
    monkeypatch.setenv("TEST_ITEMS", long_value)

    # Act
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])

    # Assert
    captured = capsys.readouterr()
    assert "TEST_ITEMS=" in captured.out
    assert "..." in captured.out


def test_append_action_empty_list_not_shown_in_help(parser, monkeypatch, capsys):
    """Empty ENV value should not appear in help."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "")

    # Act
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])

    # Assert
    captured = capsys.readouterr()
    assert "TEST_ITEMS" not in captured.out


def test_append_action_ignores_short_options(parser, monkeypatch):
    """Short options should be ignored, only long options processed."""
    # Arrange
    parser.add_argument("-i", "--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "1,2,3")

    # Act
    args = parser.parse_args([])

    # Assert
    # Should still work because --items (long option) is present
    assert args.items == ["1", "2", "3"]


def test_append_action_with_special_characters(parser, monkeypatch):
    """Values with special characters should be preserved."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "foo-bar,baz_qux,test@example.com")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["foo-bar", "baz_qux", "test@example.com"]


def test_append_action_with_equals_in_value(parser, monkeypatch):
    """Values containing equals signs should be preserved."""
    # Arrange
    parser.add_argument("--items", action="append")
    monkeypatch.setenv("TEST_ITEMS", "key=value,foo=bar")

    # Act
    args = parser.parse_args([])

    # Assert
    assert args.items == ["key=value", "foo=bar"]

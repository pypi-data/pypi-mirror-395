from dataclasses import dataclass, field
from typing import Annotated

import pytest

from argparse_boost import (
    BoostedArgumentParser,
    DefaultsHelpFormatter,
    Help,
    Parser,
    dict_from_args,
    env_for_dataclass,
    field_path_to_env_name,
    from_dict,
)


@pytest.fixture()
def env_prefix():
    return "APP_"


@pytest.fixture()
def parser(env_prefix):
    return BoostedArgumentParser(prog="test", env_prefix=env_prefix)


def test_cli_parsing_supports_list_with_comma(parser):
    @dataclass(kw_only=True)
    class Config:
        tags: list[str]

    parser.parse_arguments_from_dataclass(Config)
    args = parser.parse_args(["--tags", "one,two,three"])

    merged = dict_from_args(args, Config)
    config = from_dict(merged, Config)

    assert config.tags == ["one", "two", "three"]


def test_from_dict_applies_defaults_and_optionals(parser):
    @dataclass(kw_only=True)
    class Nested:
        value: str = "fallback"

    @dataclass(kw_only=True)
    class Config:
        required: int
        optional_value: int | None = None
        with_default: str = "default"
        nested: Nested = field(default_factory=Nested)

    parser.parse_arguments_from_dataclass(Config)
    args = parser.parse_args(["--required", "10"])

    merged = dict_from_args(args, Config)
    config = from_dict(merged, Config)

    assert config.required == 10
    assert config.optional_value is None
    assert config.with_default == "default"
    assert config.nested.value == "fallback"


def test_cli_values_override_env(monkeypatch):
    @dataclass(kw_only=True)
    class Config:
        name: str

    parser = BoostedArgumentParser(prog="test", env_prefix="APP_")
    parser.parse_arguments_from_dataclass(Config)
    monkeypatch.setenv("APP_NAME", "env-name")

    args = parser.parse_args(["--name", "cli-name"])
    merged = env_for_dataclass(
        Config,
        name_maker=field_path_to_env_name(env_prefix="APP_"),
    )
    merged.update(dict_from_args(args, Config))
    config = from_dict(merged, Config)

    assert config.name == "cli-name"


def test_invalid_bool_from_cli_raises():
    @dataclass(kw_only=True)
    class Config:
        enabled: bool

    parser = BoostedArgumentParser(prog="test", env_prefix="APP_")
    parser.parse_arguments_from_dataclass(Config)

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--enabled", "not-a-bool"])

    assert exc_info.value.code == 2


def test_required_field_missing_triggers_system_exit(parser):
    @dataclass(kw_only=True)
    class Config:
        required: int

    parser.parse_arguments_from_dataclass(Config)

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args([])

    assert exc_info.value.code == 2


def test_help_includes_default_value_from_dataclass():
    @dataclass(kw_only=True)
    class Config:
        threshold: Annotated[int, Help("Example threshold.")] = 42

    parser = BoostedArgumentParser(
        prog="test",
        env_prefix="APP_",
        formatter_class=DefaultsHelpFormatter,
    )
    parser.parse_arguments_from_dataclass(Config)

    help_text = parser.format_help()

    assert "--threshold" in help_text
    assert "Default: 42" in help_text


def _double_int(value: str) -> int:
    # TODO: dont call two times (one from argparse, one from us)
    # maybe don't use value from Parser in argparse
    if isinstance(value, int):
        return value
    return int(value) * 2


def test_dataclass_cli_and_env_merge_into_nested_config(monkeypatch):
    @dataclass(kw_only=True)
    class Database:
        host: str
        port: int = 5432
        use_ssl: bool = False

    @dataclass(kw_only=True)
    class Config:
        name: str
        tags: list[str] = field(default_factory=list)
        limits: dict[str, int] = field(default_factory=dict)
        multiplier: Annotated[int, Parser(_double_int)] = 1
        note: Annotated[str, Help("Optional note.")] = "n/a"
        db: Database = field(
            default_factory=lambda: Database(host="localhost"),
        )

    parser = BoostedArgumentParser(prog="test", env_prefix="APP_")
    parser.parse_arguments_from_dataclass(Config)
    monkeypatch.setenv("APP_DB_HOST", "env-db.local")
    monkeypatch.setenv("APP_LIMITS", "daily=5,monthly=10")
    monkeypatch.setenv("APP_NOTE", "from-env")
    monkeypatch.setenv("APP_MULTIPLIER", "3")

    args = parser.parse_args(
        [
            "--name",
            "cli-name",
            "--db-port",
            "15432",
            "--db-use-ssl",
            "true",
            "--tags",
            "blue,green",
        ],
    )

    config_data = env_for_dataclass(
        Config,
        name_maker=field_path_to_env_name(env_prefix="APP_"),
    )
    config_data.update(dict_from_args(args, Config))
    config = from_dict(config_data, Config)

    assert config.name == "cli-name"
    assert config.db.host == "env-db.local"
    assert config.db.port == 15432
    assert config.db.use_ssl is True
    assert config.tags == ["blue", "green"]
    assert config.limits == {"daily": 5, "monthly": 10}
    assert config.multiplier == 6
    assert config.note == "from-env"

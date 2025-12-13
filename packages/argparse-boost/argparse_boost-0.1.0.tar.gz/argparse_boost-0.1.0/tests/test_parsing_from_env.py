import argparse
from dataclasses import dataclass, field
from typing import Annotated

import pytest

from argparse_boost import (
    BoostedArgumentParser,
    FieldNameConflictError,
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


@pytest.fixture(params=["cli", "non_cli"])
def construct_data(request, parser, env_prefix):
    def maker(dataclass_type):
        if request.param == "cli":
            parser.parse_arguments_from_dataclass(dataclass_type)
            args = parser.parse_args([])
            data = dict_from_args(args, dataclass_type)
        else:
            data = env_for_dataclass(
                dataclass_type,
                name_maker=field_path_to_env_name(env_prefix=env_prefix),
            )
        return from_dict(data, dataclass_type)

    return maker


def test_env_parsing_supports_bool_list_and_dict(monkeypatch, construct_data):
    @dataclass(kw_only=True)
    class Config:
        enabled: bool
        numbers: list[int]
        mapping: dict[str, int]

    monkeypatch.setenv("APP_ENABLED", "on")
    monkeypatch.setenv("APP_NUMBERS", "1,2,3")
    monkeypatch.setenv("APP_MAPPING", "a=1,b=2")

    config = construct_data(Config)

    assert config.enabled is True
    assert config.numbers == [1, 2, 3]
    assert config.mapping == {"a": 1, "b": 2}


def test_cli_field_name_conflict_is_reported(construct_data):
    @dataclass(kw_only=True)
    class Database:
        password: str

    @dataclass(kw_only=True)
    class Conflicted:
        db_password: str
        db: Database

    with pytest.raises(FieldNameConflictError):
        construct_data(Conflicted)


def test_nested_defaults_preserved_when_overriding_partial(monkeypatch, construct_data):
    @dataclass(kw_only=True)
    class Nested:
        a: str = "A"
        b: str = "B"

    @dataclass(kw_only=True)
    class Config:
        nested: Nested = field(default_factory=Nested)

    monkeypatch.setenv("APP_NESTED_A", "override")
    config = construct_data(Config)

    assert config.nested.a == "override"
    assert config.nested.b == "B"


def test_custom_parser_is_applied_for_env_values(monkeypatch, construct_data):
    def triple(value: str) -> int:
        # TODO: fix this behaviour
        if isinstance(value, int):
            return value
        return int(value) * 3

    @dataclass(kw_only=True)
    class Config:
        factor: Annotated[int, Parser(triple)]

    monkeypatch.setenv("APP_FACTOR", "4")

    config = construct_data(Config)

    assert config.factor == 12


def test_dict_from_args_skips_missing_values():
    @dataclass
    class Config:
        required: int

    args = argparse.Namespace()

    assert dict_from_args(args, Config) == {}

from dataclasses import dataclass

import pytest

from argparse_boost import from_dict


@pytest.mark.parametrize(
    "data",
    [
        {"name": None},
        {"name": "null"},
        {"name": "NULL"},
        {"name": "Null"},
        {"name": "None"},
    ],
)
def test_can_parse_none_field(data):
    @dataclass
    class Config:
        name: None

    parsed = from_dict(data, Config)

    assert parsed.name is None


def test_can_parse_value_for_optional_field():
    @dataclass
    class Config:
        age: int | None

    parsed = from_dict({"age": 42}, Config)

    assert parsed.age == 42


@pytest.mark.parametrize(
    "data",
    [
        {"name": None},
        {"name": "null"},
        {"name": "NULL"},
        {"name": "Null"},
        {"name": "None"},
    ],
)
def test_can_parse_none_for_optional_field(data):
    @dataclass
    class Config:
        name: int | None

    parsed = from_dict(data, Config)

    assert parsed.name is None


def test_can_parse_string_none_for_optional_string_field():
    @dataclass
    class Config:
        name: str | None

    parsed = from_dict({"name": "null"}, Config)

    assert parsed.name is None


@pytest.mark.parametrize(
    "data",
    [
        {"name": [None, "Alice", "Bob", None]},
        {"name": "None,Alice,Bob,NULL"},
    ],
)
def test_can_parse_optional_value_from_list_of_strings(data):
    @dataclass
    class Config:
        name: list[str | None]

    parsed = from_dict(data, Config)

    assert parsed.name == [None, "Alice", "Bob", None]


@pytest.mark.parametrize(
    "data",
    [
        {"scores": {"alice": None, "bob": "2", "carol": 3}},
        {"scores": "alice=None,bob=2,carol=3"},
    ],
)
def test_can_parse_optional_value_from_dict_of_ints(data):
    @dataclass
    class Config:
        scores: dict[str, int | None]

    parsed = from_dict(data, Config)

    assert parsed.scores == {"alice": None, "bob": 2, "carol": 3}

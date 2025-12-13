from dataclasses import dataclass
from typing import Any, Dict, List

import pytest

from argparse_boost import UnsupportedFieldTypeError, from_dict


def test_cant_use_union_fields():
    @dataclass
    class Config:
        value: int | str

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"value": "test"}, Config)


def test_cant_use_optional_list():
    @dataclass
    class Config:
        values: list[int] | None = None

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"values": [1, 2, 3]}, Config)


def test_cant_use_optional_dict():
    @dataclass
    class Config:
        mapping: dict[str, int] | None = None

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"mapping": {"a": 1, "b": 2}}, Config)


def test_cant_use_nested_list():
    @dataclass
    class Config:
        buckets: list[list[int]]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"buckets": [[1, 2], [3, 4]]}, Config)


def test_cant_use_list_with_dicts():
    @dataclass
    class Config:
        items: list[dict[str, int]]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"items": [{"a": 1}, {"b": 2}]}, Config)


def test_cant_use_nested_dict():
    @dataclass
    class Config:
        mapping: dict[str, dict[str, int]]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"mapping": {"outer": {"inner": 1}}}, Config)


def test_cant_use_dict_with_lists():
    @dataclass
    class Config:
        data: dict[str, list[int]]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"data": {"numbers": [1, 2, 3]}}, Config)


def test_cant_use_unsupported_value_type():
    @dataclass
    class Config:
        data: set[str]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"data": {"1"}}, Config)


def test_cant_use_dict_with_unsupported_value_type():
    @dataclass
    class Config:
        data: dict[str, object]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"data": {"key": "value"}}, Config)


def test_cant_use_list_with_any():
    @dataclass
    class Config:
        items: list

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"items": [1, "two", 3.0]}, Config)


def test_cant_use_dict_with_any():
    @dataclass
    class Config:
        mapping: dict

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"mapping": {"a": 1, "b": "two"}}, Config)


def test_cant_use_any_field():
    @dataclass
    class Config:
        value: Any

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"value": "some value"}, Config)


def test_cant_use_unparameterized_typing_list():
    @dataclass
    class Config:
        items: List

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"items": ["a", "b"]}, Config)


def test_cant_use_unparameterized_typing_dict():
    @dataclass
    class Config:
        mapping: Dict

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"mapping": {"a": 1}}, Config)


def test_cant_use_dict_with_non_simple_key():
    @dataclass
    class Config:
        mapping: dict[list[int], str]

    with pytest.raises(UnsupportedFieldTypeError):
        from_dict({"mapping": {1: "one"}}, Config)

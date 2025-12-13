import re
from dataclasses import MISSING, dataclass, field, fields
from typing import ClassVar

import pytest

from argparse_boost import UnsupportedFieldTypeError, from_dict


def test_unsupported_atom_type_is_reported():
    @dataclass
    class Config:
        payload: object

    with pytest.raises(
        UnsupportedFieldTypeError,
        match=re.escape("Unsupported field type for 'payload': <class 'object'>"),
    ):
        from_dict({"payload": "value"}, Config)


def test_float_and_bool_values_are_parsed():
    @dataclass
    class Config:
        ratio: float
        enabled: bool
        disabled: bool

    parsed = from_dict({"ratio": "3.5", "enabled": True, "disabled": "no"}, Config)

    assert parsed.ratio == pytest.approx(3.5)
    assert parsed.enabled is True
    assert parsed.disabled is False


def test_none_type_rejects_unparsable_string():
    @dataclass
    class Config:
        marker: None

    with pytest.raises(UnsupportedFieldTypeError, match="Cannot parse None"):
        from_dict({"marker": "nope"}, Config)


def test_list_parses_brackets_and_empty_content():
    @dataclass
    class Config:
        numbers: list[int]

    parsed = from_dict({"numbers": "[]"}, Config)

    assert parsed.numbers == []


def test_dict_parses_empty_and_colon_separated_pairs():
    @dataclass
    class Config:
        mapping: dict[str, int]

    empty = from_dict({"mapping": "   "}, Config)
    assert empty.mapping == {}

    parsed = from_dict({"mapping": "foo:1,bar:2"}, Config)
    assert parsed.mapping == {"foo": 1, "bar": 2}

    with pytest.raises(UnsupportedFieldTypeError, match="Cannot parse dict item"):
        from_dict({"mapping": "foo-1"}, Config)


def test_missing_value_for_non_optional_field_errors():
    @dataclass
    class Config:
        count: int

    with pytest.raises(UnsupportedFieldTypeError, match="Missing value"):
        from_dict({"count": None}, Config)


def test_nested_dataclass_requires_mapping():
    @dataclass
    class Child:
        value: int

    @dataclass
    class Config:
        child: Child

    with pytest.raises(UnsupportedFieldTypeError, match="Expected mapping"):
        from_dict({"child": "value"}, Config)


def test_non_optional_union_is_rejected():
    @dataclass
    class Config:
        value: int | str

    with pytest.raises(
        UnsupportedFieldTypeError,
        match=re.escape("Unsupported field type for 'value': int | str"),
    ):
        from_dict({"value": "1"}, Config)


def test_default_factory_and_missing_detection():
    @dataclass
    class FactoryDefault:
        items: list[int] = field(default_factory=list)

    @dataclass
    class RequiredOnly:
        required: int

    # take_default is exercised internally by from_dict(parse_dataclass)
    assert from_dict({}, FactoryDefault).items == []

    required_field = fields(RequiredOnly)[0]
    assert required_field.default is MISSING


def test_optional_field_set_to_none_when_missing():
    @dataclass
    class Config:
        token: str | None

    parsed = from_dict({}, Config)

    assert parsed.token is None


def test_nested_dataclass_without_prefix_is_parsed():
    @dataclass
    class Child:
        enabled: bool = False

    @dataclass
    class Parent:
        child: Child

    parsed = from_dict({}, Parent)

    assert parsed.child == Child(enabled=False)


def test_missing_required_field_raises_key_error():
    @dataclass
    class Config:
        name: str

    with pytest.raises(KeyError, match="Missing required configuration key: name"):
        from_dict({}, Config)


def test_classvar_fields_are_ignored():
    @dataclass
    class Config:
        version: ClassVar[int | str] = 1
        value: int

    config = from_dict({"value": "7", "version": "42"}, Config)

    assert config.value == 7
    assert Config.version == 1

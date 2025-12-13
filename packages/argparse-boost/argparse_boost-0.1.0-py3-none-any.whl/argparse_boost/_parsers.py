from __future__ import annotations

from dataclasses import MISSING, Field, fields, is_dataclass
from functools import singledispatch
from types import NoneType
from typing import Annotated, Any, cast, get_args, get_origin, get_type_hints

from argparse_boost._exceptions import UnsupportedFieldTypeError
from argparse_boost._framework import check_dataclass, unwrap_annotated


def strip_annotated(type_hint: Any) -> Any:
    """Drop Annotated metadata, keep the real type."""
    origin = get_origin(type_hint)
    if origin is Annotated:
        return get_args(type_hint)[0]
    return type_hint


def is_optional_type(type_hint: Any) -> bool:
    hint = strip_annotated(type_hint)
    origin = get_origin(hint)
    if origin is None:
        return False
    return NoneType in get_args(hint)


def optional_inner(type_hint: Any) -> Any:
    hint = strip_annotated(type_hint)
    return next(arg for arg in get_args(hint) if arg is not NoneType)


@singledispatch
def parse_atom(expected_type: Any, raw: str) -> Any:  # noqa: ARG001
    msg = f"Not supported type: {expected_type!r}"
    raise TypeError(msg)


@parse_atom.register(str)
def _parse_str(_: str, raw: str) -> str:
    return raw


@parse_atom.register(int)
def _parse_int(_: int, raw: str) -> int:
    return int(raw)


@parse_atom.register(float)
def _parse_float(_: float, raw: str) -> float:
    return float(raw)


@parse_atom.register(bool)
def _parse_bool(_: bool, raw: str) -> bool:
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    msg = f"Cannot parse boolean from {raw!r}"
    raise ValueError(msg)


@parse_atom.register(NoneType)
def _parse_none(_: None, raw: str) -> None:
    if _is_string_none(raw):
        return None
    msg = f"Cannot parse None from {raw!r}"
    raise ValueError(msg)


def _is_string_none(raw: str) -> bool:
    return raw.upper() == "NULL" or raw == "None"


def parse_list(raw: str | list[Any], item_type: Any) -> list[Any]:
    if isinstance(raw, list):
        items = raw
    else:
        text = raw.strip()
        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1]
        if not text:
            items = []
        else:
            items = [chunk.strip() for chunk in text.split(",") if chunk.strip()]
    return [parse_value(item_type, item) for item in items]


def parse_dict(
    raw: str | dict[Any, Any],
    key_type: Any,
    value_type: Any,
) -> dict[Any, Any]:
    if isinstance(raw, dict):
        iterator = list(raw.items())
    else:
        text = raw.strip()
        if not text:
            return {}
        pairs = [piece for piece in text.split(",") if piece.strip()]
        iterator = []
        for pair in pairs:
            if "=" in pair:
                key_text, value_text = pair.split("=", 1)
            elif ":" in pair:
                key_text, value_text = pair.split(":", 1)
            else:
                msg = f"Cannot parse dict item {pair!r}"
                raise ValueError(msg)
            iterator.append((key_text.strip(), value_text.strip()))
    return {
        parse_value(key_type, key): parse_value(value_type, value)
        for key, value in iterator
    }


UNION_ERROR_MSG = "Only Optional[T] (Union[T, None]) is supported"


def parse_value(type_hint: Any, raw: Any) -> Any:
    try:
        hint = strip_annotated(type_hint)
        if raw is None:
            if is_optional_type(hint) or hint is NoneType:
                return None
            msg = f"Missing value for non-optional field {hint!r}"
            raise ValueError(msg)

        if is_optional_type(hint):
            if isinstance(raw, str) and _is_string_none(raw):
                return None
            return parse_value(optional_inner(hint), raw)

        origin = get_origin(hint)
        if origin is list:
            (item_type,) = get_args(hint) or (str,)
            return parse_list(raw, item_type)
        if origin is dict:
            key_type, value_type = get_args(hint) or (str, str)
            return parse_dict(raw, key_type, value_type)

        if is_dataclass(hint):
            if is_dataclass(raw):
                return raw
            if not isinstance(raw, dict):
                msg = f"Expected mapping, got {raw!r}"
                raise TypeError(msg)
            return parse_dataclass(hint, raw)

        if not isinstance(raw, str):
            return raw

        try:
            parser = parse_atom.dispatch(hint)
        except TypeError as exc:
            if "UnionType" in str(exc):
                raise UnsupportedFieldTypeError(UNION_ERROR_MSG) from exc
            raise
        return parser(hint, raw)
    except Exception as exc:
        msg = str(exc)
        raise UnsupportedFieldTypeError(msg) from exc


def take_default(field_def: Field) -> Any:
    if field_def.default is not MISSING:
        return field_def.default
    if field_def.default_factory is not MISSING:
        return field_def.default_factory()
    return MISSING


def extract_prefixed(data: dict[str, str], prefix: str) -> dict[str, str]:
    prefix_with_sep = f"{prefix}_"
    return {
        key[len(prefix_with_sep) :]: value
        for key, value in data.items()
        if key.startswith(prefix_with_sep)
    }


def parse_dataclass(cls: Any, flat_data: dict[str, Any]) -> Any:
    type_hints = get_type_hints(cls, include_extras=True)
    parsed = {}
    for field_def in fields(cls):
        hint = type_hints.get(field_def.name, field_def.type)
        if field_def.name in flat_data:
            _, parser_wrapper, _ = unwrap_annotated(hint)
            if parser_wrapper:
                parsed[field_def.name] = parser_wrapper.func(flat_data[field_def.name])
            else:
                parsed[field_def.name] = parse_value(hint, flat_data[field_def.name])
            continue

        nested_data = extract_prefixed(flat_data, field_def.name)
        if nested_data and is_dataclass(strip_annotated(hint)):
            parsed[field_def.name] = parse_dataclass(strip_annotated(hint), nested_data)
            continue

        default_value = take_default(field_def)
        if default_value is not MISSING:
            parsed[field_def.name] = default_value
            continue

        if is_optional_type(hint):
            parsed[field_def.name] = None
            continue

        if is_dataclass(strip_annotated(hint)):
            parsed[field_def.name] = parse_dataclass(strip_annotated(hint), nested_data)
            continue

        msg = f"Missing required configuration key: {field_def.name}"
        raise KeyError(msg)

    return cls(**parsed)


def from_dict(
    data: dict[tuple[str, ...], Any] | dict[str, Any],
    dc_type: type[Any],
) -> Any:
    """Construct a dataclass instance from flat mapping (CLI/env merged)."""
    check_dataclass(dc_type)
    if any(isinstance(key, tuple) for key in data):
        data = {"_".join(path): value for path, value in data.items()}
    return parse_dataclass(dc_type, cast("dict[str, Any]", data))

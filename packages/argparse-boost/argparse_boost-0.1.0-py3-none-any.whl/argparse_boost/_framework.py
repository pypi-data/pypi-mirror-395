from __future__ import annotations

import argparse
import inspect
import os
import types
import typing
from collections.abc import Callable, Sequence
from dataclasses import MISSING, dataclass, fields, is_dataclass
from types import NoneType
from typing import Annotated, Any, get_args, get_origin

from argparse_boost._exceptions import FieldNameConflictError, UnsupportedFieldTypeError


class Parser:
    """Wrapper for custom argument parser function.

    Used with Annotated to specify custom parsing logic for dataclass fields.

    Example:
        def parse_percentage(value: str) -> float:
            return float(value.rstrip('%')) / 100

        @dataclass
        class Config:
            value: Annotated[float, Parser(parse_percentage)] = 0.5
    """

    def __init__(self, func: Callable[[str], Any]) -> None:
        self.func = func


class Help:
    """Wrapper for help text description.

    Used with Annotated to provide help text for dataclass fields in CLI.

    Example:
        @dataclass
        class Config:
            value: Annotated[str, Help("Description for --value argument")]
    """

    def __init__(self, description: str) -> None:
        self.description = description


def check_dataclass(
    dc_type: type[Any],
    specs: Sequence[FieldSpec] | None = None,
) -> None:
    specs = specs or field_specs_from_dataclass(dc_type)
    _check_field_name_conflicts(specs)
    _validate_supported_types(dc_type)


SUPPORTED_TYPES_DESCRIPTION = (
    "Supported field types: int, float, str, bool, None; "
    "list[T] or dict[K, V] with T/K/V from the same simple types or Optional of them; "
    "Union is only supported as Optional[T] (T | None) for simple types; "
    "list | None and dict | None are not supported; Any is not supported."
)


def _check_field_name_conflicts(specs: Sequence[FieldSpec]) -> None:
    """Ensure flattened field names do not collide for CLI/env separators."""
    seen: dict[str, tuple[str, ...]] = {}
    sep = "_"
    for spec in specs:
        name = sep.join(spec.path).upper()
        if name in seen:
            conflict_path = ".".join(seen[name])
            new_path = ".".join(spec.path)
            msg = f"key conflict for '{name}': {conflict_path!s} vs {new_path!s}"
            raise FieldNameConflictError(msg)
        seen[name] = spec.path


def _validate_supported_types(dc_type: type[Any], path: tuple[str, ...] = ()) -> None:
    hints = typing.get_type_hints(dc_type, include_extras=True)
    for f in fields(dc_type):
        hinted_type = hints.get(f.name, f.type)
        field_type, parser, _ = unwrap_annotated(hinted_type)
        if parser:
            # Custom parser provided; skip type validation
            continue
        origin = get_origin(field_type)
        if origin is typing.ClassVar:
            continue
        _validate_supported_type(field_type, (*path, f.name))


def _validate_supported_type(type_hint: Any, path: tuple[str, ...]) -> None:
    optional, base_type = _parse_optional_union(type_hint)
    if optional:
        if not _is_simple_type(base_type):
            _raise_unsupported_type(path, type_hint)
        return

    if type_hint is Any:
        _raise_unsupported_type(path, type_hint)

    origin = get_origin(type_hint)
    if _is_simple_type(type_hint):
        return
    if _is_dataclass_type(type_hint):
        _validate_supported_types(get_origin(type_hint) or type_hint, path)
        return
    if origin is list:
        _validate_list_type(type_hint, path)
        return
    if origin is dict:
        _validate_dict_type(type_hint, path)
        return
    if origin in (types.UnionType, typing.Union):
        _raise_unsupported_type(path, type_hint)

    _raise_unsupported_type(path, type_hint)


def _validate_list_type(type_hint: Any, path: tuple[str, ...]) -> None:
    args = get_args(type_hint)
    if len(args) != 1:
        _raise_unsupported_type(path, type_hint)
    (item_type,) = args
    if not _is_simple_or_optional_simple_type(item_type):
        _raise_unsupported_type(path, type_hint)


def _validate_dict_type(type_hint: Any, path: tuple[str, ...]) -> None:
    args = get_args(type_hint)
    if len(args) != 2:
        _raise_unsupported_type(path, type_hint)
    key_type, value_type = args
    if not _is_simple_or_optional_simple_type(key_type):
        _raise_unsupported_type(path, type_hint)
    if not _is_simple_or_optional_simple_type(value_type):
        _raise_unsupported_type(path, type_hint)


def _is_simple_type(type_hint: Any) -> bool:
    return type_hint in {int, float, str, bool, NoneType}


def _is_simple_or_optional_simple_type(type_hint: Any) -> bool:
    if _is_simple_type(type_hint):
        return True
    optional, base = _parse_optional_union(type_hint)
    return optional and _is_simple_type(base)


def _raise_unsupported_type(path: tuple[str, ...], type_hint: Any) -> None:
    field_path = ".".join(path)
    msg = (
        f"Unsupported field type for '{field_path}': {type_hint!r}. "
        f"{SUPPORTED_TYPES_DESCRIPTION}"
    )
    raise UnsupportedFieldTypeError(msg)


def dict_from_args(
    args: argparse.Namespace,
    dc_type: type[Any],
) -> dict[tuple[str, ...], Any]:
    """Extract provided CLI args into a flat mapping keyed by field paths."""
    specs = field_specs_from_dataclass(dc_type)
    result: dict[tuple[str, ...], Any] = {}
    for spec in specs:
        dest = "_".join(spec.path)
        value = getattr(args, dest, _UNSET)
        if value is _UNSET:
            continue
        result[spec.path] = value
    return result


def field_path_to_env_name(env_prefix: str = "") -> Callable[[tuple[str, ...]], str]:
    """Return a function that maps field paths to environment variable names."""

    def mapper(path: tuple[str, ...]) -> str:
        return _env_name_from_parts(path, env_prefix)

    return mapper


def env_for_dataclass(
    dc_type: type[Any],
    *,
    name_maker: Callable[[tuple[str, ...]], str] = field_path_to_env_name(),
) -> dict[tuple[str, ...], str]:
    """Read configuration values for a dataclass from environment variables."""
    specs = field_specs_from_dataclass(dc_type)
    result: dict[tuple[str, ...], Any] = {}
    for spec in specs:
        env_name = name_maker(spec.path)
        if env_name not in os.environ:
            continue
        raw_value = os.environ[env_name]
        result[spec.path] = raw_value
    return result


def arg_option_to_env_name(env_prefix: str = "") -> Callable[[str], str]:
    """Return a function that maps field paths to environment variable names."""

    def mapper(option: str) -> str:
        parts = option.lstrip("-").replace("-", "_").split("_")
        return _env_name_from_parts(parts, env_prefix)

    return mapper


def env_for_argparser(
    parser: argparse.ArgumentParser,
    args: Sequence[str] | None = None,
    *,
    name_maker: Callable[[str], str] = arg_option_to_env_name(),
) -> list[tuple[str, str, str | list[str]]]:
    applied_options: set[str] = set()
    if args:
        applied_options = {
            arg.split("=", maxsplit=1)[0] for arg in args if arg.startswith("-")
        }
    env_values: list[tuple[str, str, str | list[str]]] = []
    for action in parser._actions:  # noqa: SLF001
        # Skip append_const actions (like store_const)
        if isinstance(action, argparse._AppendConstAction):  # noqa: SLF001
            continue

        # Check if action is store or append
        is_store = isinstance(action, argparse._StoreAction)  # noqa: SLF001
        is_append = isinstance(action, argparse._AppendAction)  # noqa: SLF001

        if not (is_store or is_append):
            continue
        if not action.option_strings:
            continue
        if applied_options and any(
            opt in applied_options for opt in action.option_strings
        ):
            continue
        for opt in action.option_strings:
            if opt.startswith("--"):
                env_var_name = name_maker(opt)
                if env_var_name in os.environ:
                    raw_value = os.environ[env_var_name]

                    if is_append:
                        # Split comma-separated values for append actions
                        values = [v.strip() for v in raw_value.split(",") if v.strip()]
                        if values:  # Only add if non-empty after filtering
                            env_values.append((opt, env_var_name, values))
                    else:
                        # Store action: single value
                        env_values.append((opt, env_var_name, raw_value))
    return env_values


_UNSET = object()


@dataclass(frozen=True)
class FieldSpec:
    path: tuple[str, ...]
    type_: Any
    parser: Callable[[str], Any] | None
    help_text: str | None
    has_default: bool
    default: Any
    default_factory: Callable[[], Any] | None
    parent_optional: bool


def field_specs_from_dataclass(
    dc_type: type[Any],
    parent_path: tuple[str, ...] = (),
    parent_optional: bool = False,
    *,
    type_hints: dict[str, Any] | None = None,
) -> list[FieldSpec]:
    specs: list[FieldSpec] = []
    hints = type_hints or typing.get_type_hints(dc_type, include_extras=True)
    for f in fields(dc_type):
        hinted_type = hints.get(f.name, f.type)
        field_type, parser_wrapper, help_wrapper = unwrap_annotated(hinted_type)
        optional, base_type = _parse_optional_union(field_type)
        has_default, default, default_factory = _field_default_info(f)
        path = (*parent_path, f.name)

        # Skip ClassVar and InitVar
        origin = get_origin(field_type)
        if origin is typing.ClassVar:
            continue

        if _is_dataclass_type(base_type):
            nested_hints = typing.get_type_hints(
                get_origin(base_type) or base_type,
                include_extras=True,
            )
            specs.extend(
                field_specs_from_dataclass(
                    get_origin(base_type) or base_type,
                    parent_path=path,
                    parent_optional=parent_optional or has_default or optional,
                    type_hints=nested_hints,
                ),
            )
            continue

        help_text = help_wrapper.description if help_wrapper else None
        specs.append(
            FieldSpec(
                path=path,
                type_=base_type,
                parser=parser_wrapper.func if parser_wrapper else None,
                help_text=help_text,
                has_default=has_default,
                default=default,
                default_factory=default_factory,
                parent_optional=parent_optional or has_default or optional,
            ),
        )
    return specs


def unwrap_annotated(field_type: Any) -> tuple[Any, Parser | None, Help | None]:
    """Return base type and custom Parser/Help metadata if present."""
    if get_origin(field_type) is Annotated:
        base, *extras = get_args(field_type)
        parser = next((e for e in extras if isinstance(e, Parser)), None)
        help_wrapper = next((e for e in extras if isinstance(e, Help)), None)
        return base, parser, help_wrapper
    return field_type, None, None


def _parse_optional_union(tp: Any) -> tuple[bool, Any]:
    origin = get_origin(tp)
    if origin in (types.UnionType, typing.Union):
        args = get_args(tp)
        non_none = [arg for arg in args if arg is not type(None)]
        if len(non_none) == 1 and len(args) == 2:
            return True, non_none[0]
    return False, tp


def _field_default_info(dc_field: Any) -> tuple[bool, Any, Callable[[], Any] | None]:
    """Return default presence along with value or factory."""
    if dc_field.default is not MISSING:
        return True, dc_field.default, None
    if dc_field.default_factory is not MISSING:
        return True, _UNSET, dc_field.default_factory
    return False, None, None


def _is_dataclass_type(tp: Any) -> bool:
    """Return True if tp (or its origin) is a dataclass type."""
    base = get_origin(tp) or tp
    return inspect.isclass(base) and is_dataclass(base)


def _env_name_from_parts(parts: Sequence[str], env_prefix: str) -> str:
    return f"{env_prefix}{'_'.join(parts).upper()}"

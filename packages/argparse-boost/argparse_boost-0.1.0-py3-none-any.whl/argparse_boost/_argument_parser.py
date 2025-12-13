from __future__ import annotations

import argparse
import shlex
import sys
from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from argparse_boost._framework import (
    _UNSET,
    FieldSpec,
    arg_option_to_env_name,
    check_dataclass,
    env_for_argparser,
    field_specs_from_dataclass,
)
from argparse_boost._parsers import parse_value as parse_value_original


class DefaultsHelpFormatter(argparse.HelpFormatter):
    """Append default values to help text in a consistent format."""

    def _get_help_string(self, action: argparse.Action) -> str:
        help_text = action.help or ""

        if getattr(action, "required", False):
            suffix = "Required"
            if help_text.endswith("."):
                help_text = help_text.rstrip()
                help_text += f" {suffix}"
            else:
                help_text = f"{help_text}. {suffix}" if help_text else suffix
        elif (
            action.default not in (None, argparse.SUPPRESS)
            and "%(default)" not in help_text
        ):
            suffix = "Default: %(default)s"
            if help_text.endswith("."):
                help_text = help_text.rstrip()
                help_text += f" {suffix}"
            else:
                help_text = f"{help_text}. {suffix}" if help_text else suffix

        return help_text


_N = TypeVar("_N", bound=argparse.Namespace)


class BoostedArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that supports reading values from environment variables.

    Environment variables are read before command-line parsing, with CLI args
    taking priority. Only long-form arguments (--option) are supported, not
    short-form (-o). Boolean flags (store_true/store_false) are excluded.

    Args:
        env_prefix: Optional prefix for environment variable names.
                    e.g., env_prefix="APP" converts --log-level to APP_LOG_LEVEL

    Example:
        parser = EnvArgumentParser(prog="myapp", env_prefix="MYAPP")
        parser.add_argument("--log-level", choices=["INFO", "DEBUG"])

        # Usage:
        # MYAPP_LOG_LEVEL=DEBUG myapp command
    """

    def __init__(self, *args: Any, env_prefix: str = "", **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.env_prefix = env_prefix
        self._env_name_maker = arg_option_to_env_name(env_prefix=env_prefix)

    def add_subparsers(self, **kwargs: Any) -> argparse._SubParsersAction:
        """Override to auto-propagate env_prefix to child parsers."""
        subparsers = super().add_subparsers(**kwargs)
        original_add_parser = subparsers.add_parser

        def add_parser_with_env_prefix(
            *args: Any,
            **parser_kwargs: Any,
        ) -> argparse.ArgumentParser:
            parser_class = parser_kwargs.get(
                "parser_class",
                subparsers._parser_class,  # noqa: SLF001
            )
            if (
                issubclass(parser_class, BoostedArgumentParser)
                and "env_prefix" not in parser_kwargs
            ):
                parser_kwargs["env_prefix"] = self.env_prefix
            return original_add_parser(*args, **parser_kwargs)

        subparsers.add_parser = add_parser_with_env_prefix  # type: ignore[method-assign]
        return subparsers

    def parse_known_args(  # type: ignore[override]
        self,
        args: Sequence[str] | None = None,
        namespace: _N | None = None,
    ) -> tuple[argparse.Namespace | _N, list[str]]:
        if env_values := env_for_argparser(self, args, name_maker=self._env_name_maker):
            if args is None:
                args = sys.argv[1:]
            expanded_args = []
            for opt, _, val in env_values:
                if isinstance(val, list):
                    expanded_args.extend([f"{opt}={v}" for v in val])
                else:
                    expanded_args.extend(shlex.split(f"{opt} {val}"))
            args = list(args)
            if "-h" not in args and "--help" not in args:
                args = expanded_args + args
        return super().parse_known_args(args, namespace)

    def _format_env_section(self) -> str:
        """Format section showing which parameters have ENV variables set.

        Returns:
            Formatted string with ENV variables section, or empty string if none found.
        """
        env_vars = []
        for opt_name, env_name, env_value in env_for_argparser(
            self,
            name_maker=self._env_name_maker,
        ):
            # Convert list values to comma-separated string for display
            if isinstance(env_value, list):
                env_value = ",".join(env_value)

            if len(env_value) > 50:
                env_value = env_value[:47] + "..."
            env_vars.append((opt_name, env_name, env_value))

        if not env_vars:
            return ""

        max_opt_len = max(len(opt) for opt, _, _ in env_vars)

        lines = ["\nEnvironment variables set:"]
        for opt, var_name, value in env_vars:
            lines.append(f"  {opt:<{max_opt_len}}  {var_name}={value}")

        return "\n".join(lines) + "\n"

    def format_help(self) -> str:
        """Format help message with additional ENV variables section."""
        help_text = super().format_help()
        env_section = self._format_env_section()
        return help_text + env_section

    def parse_arguments_from_dataclass(
        self,
        dc_type: type[Any],
    ) -> None:
        """Register CLI arguments for every leaf field of a dataclass."""
        specs = field_specs_from_dataclass(dc_type)
        check_dataclass(dc_type, specs)
        for spec in specs:
            parser_callable, default_value = self._parser_and_default_for_spec(spec)
            kwargs: dict[str, Any] = {
                "required": not spec.has_default and not spec.parent_optional,
                "default": default_value,
                "dest": "_".join(spec.path),
                "type": parser_callable,
            }
            if spec.help_text:
                kwargs["help"] = spec.help_text

            option = "--" + "-".join(part.replace("_", "-") for part in spec.path)
            self.add_argument(option, **kwargs)

        # Store mapping for later use in dict_from_args
        existing = getattr(self, "_field_specs", {})
        existing[dc_type] = specs
        self._field_specs = existing

    def _parser_and_default_for_spec(self, spec: FieldSpec) -> tuple[Any, Any]:
        default_value = argparse.SUPPRESS
        if spec.default is not _UNSET:
            default_value = spec.default
        elif spec.default_factory:
            default_value = spec.default_factory()
        return self.make_value_parser(spec), default_value

    @staticmethod
    def make_value_parser(spec: FieldSpec) -> Callable[[str], Any]:
        def parse_value(raw: str) -> Any:
            try:
                if spec.parser:
                    return spec.parser(raw)
                # just parse for validation
                # but return raw string
                parse_value_original(spec.type_, raw)
                return raw
            except Exception as exc:
                msg = str(exc)
                raise argparse.ArgumentTypeError(msg) from exc

        return parse_value

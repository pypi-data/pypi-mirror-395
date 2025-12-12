from __future__ import annotations

import inspect
import sys
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any, get_args, get_origin, get_type_hints

from .command import CommandDefinition
from .core import (
    Argument as SchemaArgument,
)
from .core import (
    Command,
    PithSchema,
    Tier1,
    Tier2,
    Tier3,
)
from .core import (
    Option as SchemaOption,
)
from .discovery import export_schema, render_command, render_overview, render_search
from .parameters import Argument, Option, infer_pith_type
from .parsing import extract_docstring_content


class Pith:
    def __init__(self, name: str, pith: str) -> None:
        self.name = name
        self.pith = pith
        self._commands: dict[str, CommandDefinition] = {}

    # Decorators
    def command(
        self, *, name: str | None = None, pith: str | None = None, priority: int = 50
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cmd_name = name or func.__name__
            summary = pith or _first_line(func.__doc__) or cmd_name
            meta = getattr(func, "_pith_meta", {})
            intents = list(meta.get("intents", []))
            hints = list(meta.get("hints", []))
            docstring_content = extract_docstring_content(func.__doc__)
            # Merge docstring related with decorator hints
            all_related = hints + docstring_content.related
            self._commands[cmd_name] = CommandDefinition(
                name=cmd_name,
                callback=func,
                summary=summary,
                intents=intents,
                hints=all_related,
                examples=docstring_content.examples,
                priority=priority,
            )
            return func

        return decorator

    def intents(
        self, *intents_values: str
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            _merge_meta(func, "intents", intents_values)
            return func

        return decorator

    def hints(
        self, *hints_values: str
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            _merge_meta(func, "hints", hints_values)
            return func

        return decorator

    # Runtime helpers
    def schema(self) -> PithSchema:
        commands: dict[str, Command] = {}
        for command_def in self._commands.values():
            commands[command_def.name] = self._build_schema_command(command_def)
        return PithSchema(tool=self.name, pith=self.pith, commands=commands)

    def run(self, argv: Sequence[str] | None = None) -> None:
        from .utils import PithException

        args = list(argv) if argv is not None else sys.argv[1:]
        try:
            self._run_internal(args)
        except PithException as e:
            e.show()
            sys.exit(e.exit_code)

    def _run_internal(self, args: list[str]) -> None:
        if not args:
            print(render_overview(self.schema()))
            return

        if args[0] == "pith":
            self._run_discovery(args[1:])
            return

        name = args[0]
        if name in self._commands:
            self._invoke_command(name, args[1:])
        else:
            print(render_overview(self.schema()))

    # Internal
    def _run_discovery(self, args: Sequence[str]) -> None:
        # Parse --json flag
        use_json = "--json" in args
        args = [a for a in args if a != "--json"]

        # Parse --find flag and query
        find_query: str | None = None
        if "--find" in args:
            idx = args.index("--find")
            if idx + 1 < len(args):
                find_query = args[idx + 1]
                args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]
            else:
                # --find without query, show error
                print("Error: --find requires a query argument")
                return

        # Handle search mode
        if find_query:
            print(render_search(self.schema(), find_query, use_json=use_json))
            return

        if not args:
            print(render_overview(self.schema(), use_json=use_json))
            return

        if args[0] == "export":
            path = args[1] if len(args) > 1 else None
            print(export_schema(self.schema(), path))
            return

        name = args[0]
        definition = self._commands.get(name)
        if not definition:
            print(render_overview(self.schema(), use_json=use_json))
            return

        verbosity = _verbosity(args[1:])
        print(render_command(self.schema(), definition, verbosity, use_json=use_json))

    def _invoke_command(self, name: str, argv: Sequence[str]) -> None:
        definition = self._commands[name]
        sig = inspect.signature(definition.callback)

        # Get type hints for conversion
        try:
            hints = get_type_hints(definition.callback)
        except Exception:
            hints = {}

        # Build option/param mappings and parse argv
        option_map, param_defaults, _ = _build_option_map(sig, hints)
        positional_args, kwargs = _parse_argv(argv, option_map, param_defaults, hints)
        final_kwargs = _build_final_kwargs(sig, positional_args, kwargs, hints)

        definition.callback(**final_kwargs)

    def _build_schema_command(self, definition: CommandDefinition) -> Command:
        arguments: list[SchemaArgument] = []
        options: list[SchemaOption] = []

        sig = inspect.signature(definition.callback)

        # Get type hints for type inference
        try:
            hints = get_type_hints(definition.callback)
        except Exception:
            hints = {}

        for param in sig.parameters.values():
            default = param.default
            param_hint = hints.get(param.name)

            if isinstance(default, Argument):
                # Use explicit type if provided, otherwise infer from annotation
                arg_type = (
                    default.type
                    if default.type != "text"
                    else infer_pith_type(param_hint)
                )
                # Preserve native types for JSON serialization (bool, int, float, str, None)
                arg_default = default.default if not default.required else None
                arguments.append(
                    SchemaArgument(
                        name=param.name,
                        description=default.pith or param.name,
                        type=arg_type,
                        required=default.required,
                        default=arg_default,
                    )
                )
            elif isinstance(default, Option):
                aliases = default.aliases or [f"--{param.name}"]
                # Use explicit type if provided, otherwise infer from annotation
                opt_type = (
                    default.type
                    if default.type != "text"
                    else infer_pith_type(param_hint)
                )
                # Preserve native types for JSON serialization (bool, int, float, str, None)
                opt_default = default.default if not default.required else None
                options.append(
                    SchemaOption(
                        name=param.name,
                        aliases=aliases,
                        description=default.pith or param.name,
                        type=opt_type,
                        required=default.required,
                        default=opt_default,
                    )
                )

        tier2 = (
            Tier2(arguments=arguments, options=options)
            if arguments or options
            else None
        )
        tier3 = (
            Tier3(examples=definition.examples, related=definition.hints)
            if definition.examples or definition.hints
            else None
        )

        return Command(
            name=definition.name,
            pith=definition.summary,
            tier1=Tier1(
                summary=definition.summary,
                run="",  # Empty: let build_run_line() generate dynamically per tier
            ),
            tier2=tier2,
            tier3=tier3,
            intents=definition.intents,
            priority=definition.priority,
        )


def _build_option_map(
    sig: inspect.Signature,
    hints: dict[str, Any],
) -> tuple[dict[str, str], dict[str, Any], set[str]]:
    """Build mappings from option aliases to parameter names.

    Returns:
        Tuple of (option_map, param_defaults, bool_params)
    """
    option_map: dict[str, str] = {}
    param_defaults: dict[str, Any] = {}
    bool_params: set[str] = set()

    for param in sig.parameters.values():
        default = param.default
        param_defaults[param.name] = default
        if isinstance(default, Option):
            for alias in default.aliases:
                option_map[alias] = param.name
            option_map[f"--{param.name}"] = param.name
            # Track boolean parameters for --no-X handling
            param_hint = hints.get(param.name)
            if param_hint is bool or default.type == "flag":
                bool_params.add(param.name)
                # Add --no-{name} -> param.name with negation marker
                option_map[f"--no-{param.name}"] = f"!{param.name}"

    return option_map, param_defaults, bool_params


def _handle_combined_flags(
    arg: str,
    option_map: dict[str, str],
    param_defaults: dict[str, Any],
    hints: dict[str, Any],
    kwargs: dict[str, Any],
) -> None:
    """Handle combined short flags like -rf."""
    for char in arg[1:]:
        flag = f"-{char}"
        if flag in option_map:
            param_name = option_map[flag]
            param_default = param_defaults.get(param_name)
            if isinstance(param_default, Option):
                param_hint = hints.get(param_name)
                if param_hint is bool or param_default.type == "flag":
                    kwargs[param_name] = True
                else:
                    kwargs[param_name] = True


def _handle_single_option(
    arg: str,
    argv: Sequence[str],
    i: int,
    option_map: dict[str, str],
    param_defaults: dict[str, Any],
    hints: dict[str, Any],
    kwargs: dict[str, Any],
) -> int:
    """Handle a single option flag.

    Returns:
        The number of argv items consumed
    """
    mapped_name = option_map[arg]

    # Handle negated boolean flags (--no-X)
    if mapped_name.startswith("!"):
        param_name = mapped_name[1:]
        kwargs[param_name] = False
        return 1

    param_name = mapped_name
    param_default = param_defaults.get(param_name)
    if not isinstance(param_default, Option):
        return 1

    param_hint = hints.get(param_name)
    if param_hint is bool or param_default.type == "flag":
        kwargs[param_name] = True
        return 1

    # Expect a value
    if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
        kwargs[param_name] = argv[i + 1]
        return 2

    kwargs[param_name] = True
    return 1


def _parse_argv(
    argv: Sequence[str],
    option_map: dict[str, str],
    param_defaults: dict[str, Any],
    hints: dict[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    """Parse command-line arguments into positional args and keyword args."""
    positional_args: list[str] = []
    kwargs: dict[str, Any] = {}
    i = 0

    while i < len(argv):
        arg = argv[i]
        if not arg.startswith("-"):
            positional_args.append(arg)
            i += 1
        elif arg.startswith("-") and not arg.startswith("--") and len(arg) > 2:
            _handle_combined_flags(arg, option_map, param_defaults, hints, kwargs)
            i += 1
        elif arg in option_map:
            consumed = _handle_single_option(
                arg, argv, i, option_map, param_defaults, hints, kwargs
            )
            i += consumed
        else:
            i += 1

    return positional_args, kwargs


def _build_final_kwargs(
    sig: inspect.Signature,
    positional_args: list[str],
    kwargs: dict[str, Any],
    hints: dict[str, Any],
) -> dict[str, Any]:
    """Build final keyword arguments by matching positional args to parameters."""
    final_kwargs: dict[str, Any] = {}
    positional_idx = 0

    for param in sig.parameters.values():
        default = param.default
        param_hint = hints.get(param.name)

        if isinstance(default, Argument):
            if positional_idx < len(positional_args):
                value = positional_args[positional_idx]
                final_kwargs[param.name] = _convert_value(value, param_hint)
                positional_idx += 1
            elif not default.required:
                final_kwargs[param.name] = default.default

        elif isinstance(default, Option):
            if param.name in kwargs:
                value = kwargs[param.name]
                if isinstance(value, bool):
                    final_kwargs[param.name] = value
                else:
                    final_kwargs[param.name] = _convert_value(value, param_hint)
            else:
                final_kwargs[param.name] = default.default

    return final_kwargs


def _first_line(docstring: str | None) -> str | None:
    if not docstring:
        return None
    stripped = [line.strip() for line in docstring.splitlines() if line.strip()]
    return stripped[0] if stripped else None


def _merge_meta(func: Callable[..., Any], key: str, values: Iterable[str]) -> None:
    meta: dict[str, list[str]] = getattr(func, "_pith_meta", {})
    existing = list(meta.get(key, []))
    existing.extend(values)
    meta[key] = existing
    func._pith_meta = meta  # type: ignore[attr-defined]


def _verbosity(args: Sequence[str]) -> int:
    if any(arg == "-vv" for arg in args):
        return 3
    if any(arg == "-v" for arg in args):
        return 2
    return 1


def _convert_value(value: str, type_hint: Any) -> Any:
    """Convert a string value to the appropriate type based on type hint.

    Args:
        value: The string value to convert
        type_hint: The Python type annotation

    Returns:
        The converted value
    """
    if type_hint is None:
        return value

    # Handle Optional types by extracting the non-None type
    origin = get_origin(type_hint)
    if origin is not None:
        args = get_args(type_hint)
        non_none_args = [a for a in args if a is not type(None)]
        if non_none_args:
            type_hint = non_none_args[0]

    # Convert based on type
    if type_hint is bool:
        return value.lower() in ("true", "1", "yes")
    if type_hint is Path or (
        isinstance(type_hint, type) and issubclass(type_hint, Path)
    ):
        return Path(value)
    if type_hint is int:
        return int(value)
    if type_hint is float:
        return float(value)

    return value

"""Internal adapters converting public API declarations into runtime structures."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, cast

from hil_testbench.api.command import CommandDeclaration
from hil_testbench.api.parser import ParserDeclaration
from hil_testbench.api.schema import SchemaDeclaration
from hil_testbench.data_processing.schema_parser import SchemaParser
from hil_testbench.task.specs import CommandDefinition, CommandValidator, Parser, ParserDefinition
from hil_testbench.utils.schema_builder import build_schema


def schema_to_dict(
    declaration: SchemaDeclaration | Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Convert a schema declaration into the raw mapping expected by the framework."""

    if declaration is None:
        return {}
    if isinstance(declaration, SchemaDeclaration):
        return declaration.to_dict()
    if isinstance(declaration, Mapping):
        return dict(declaration)
    raise TypeError(f"Unsupported schema declaration type: {type(declaration)!r}")


def build_commands(
    declarations: Iterable[CommandDeclaration],
    *,
    config: Any,
) -> list[CommandDefinition]:
    """Convert command declarations into internal CommandDefinition objects."""

    commands: list[CommandDefinition] = []
    for declaration in declarations:
        host = _resolve_host(declaration.host, config)
        parameters_schema = _convert_parameters_schema(declaration.parameters_schema)
        run_callable = _resolve_run_callable(declaration)
        commands.append(
            CommandDefinition(
                name=declaration.name,
                run=run_callable,
                host=host,
                use_pty=declaration.use_pty,
                use_shell_wrapper=declaration.use_shell_wrapper,
                immediate=declaration.immediate,
                long_running=declaration.long_running,
                retry=declaration.retry,
                env=dict(declaration.env) if declaration.env else {},
                cwd=declaration.cwd,
                validator=_wrap_validator(declaration.validator),
                startup_delay=float(declaration.delay),
                depends_on=list(declaration.depends_on),
                tags=list(declaration.tags),
                parameters_schema=parameters_schema,
                owned_parameters=list(declaration.owned_parameters)
                if declaration.owned_parameters is not None
                else None,
                exclusive=declaration.exclusive,
            )
        )
    return commands


def build_parser(
    declaration: ParserDeclaration | None,
    *,
    config: Any,
    schema_provider: Callable[[], Mapping[str, Any]] | None = None,
) -> ParserDefinition | None:
    """Convert parser declarations into internal ParserDefinition objects."""

    if declaration is None:
        return None

    match declaration.kind:
        case "custom":
            factory_obj = declaration.options.get("factory")
            if not callable(factory_obj):
                raise TypeError("parser.custom() requires a callable factory")
            parser_factory = cast(Callable[[], Parser], factory_obj)
            return ParserDefinition(factory=parser_factory)
        case "schema":
            schema_value = declaration.options.get("schema")
            if schema_value is None:
                raise TypeError("parser.schema_parser() requires a schema declaration")
            schema_dict = schema_to_dict(schema_value)
            parameters_schema = build_schema(schema_dict)
            return ParserDefinition(factory=lambda: SchemaParser(parameters_schema))
        case "custom_schema":
            factory_obj = declaration.options.get("factory")
            if not callable(factory_obj):
                raise TypeError("parser.custom_with_schema() requires a callable factory")
            schema_value = declaration.options.get("schema")
            if schema_value is None:
                raise TypeError("parser.custom_with_schema() requires schema declaration")
            schema_dict = schema_to_dict(schema_value)
            parameters_schema = build_schema(schema_dict)
            schema_factory = cast(Callable[[Any], Parser], factory_obj)

            def _factory() -> Parser:
                return cast(Parser, schema_factory(parameters_schema))

            return ParserDefinition(factory=_factory)
        case "json_stream":
            callback_obj = declaration.options.get("get_param_name")
            if not callable(callback_obj):
                raise TypeError("parser.json_stream() requires get_param_name callback")
            callback = cast(Callable[[Mapping[str, Any]], str], callback_obj)
            return ParserDefinition(factory=lambda: _JsonStreamParser(callback))
        case "text":
            callback_obj = declaration.options.get("get_param_name")
            if not callable(callback_obj):
                raise TypeError("parser.text() requires get_param_name callback")
            callback = cast(Callable[[Mapping[str, Any]], str], callback_obj)
            return ParserDefinition(factory=lambda: _TextLineParser(callback))
        case _:
            raise ValueError(f"Unknown parser declaration kind: {declaration.kind!r}")


def _resolve_host(host_reference: Any, config: Any) -> Any:
    if host_reference is None:
        return None
    if isinstance(host_reference, str):
        return config.get_host(host_reference)
    return host_reference


def _convert_parameters_schema(
    declaration: SchemaDeclaration | Mapping[str, Any] | None,
):
    if declaration is None:
        return None
    schema_dict = schema_to_dict(declaration)
    if not schema_dict:
        return None
    return build_schema(schema_dict)


def _resolve_run_callable(declaration: CommandDeclaration) -> Callable[[Any], Any]:
    if declaration.run is not None:
        return declaration.run
    if declaration.argv is not None:
        argv = tuple(declaration.argv)
        runtime_env = dict(declaration.env) if declaration.env else None

        def _runner(context: Any) -> Any:
            return context.run(argv, env=runtime_env, cwd=declaration.cwd)

        return _runner
    if declaration.shell is not None:
        command_text = declaration.shell
        runtime_env = dict(declaration.env) if declaration.env else None

        def _runner(context: Any) -> Any:
            return context.run(command_text, env=runtime_env, cwd=declaration.cwd)

        return _runner
    raise ValueError(f"Command declaration {declaration.name!r} missing execution payload")


def _wrap_validator(
    validator: Callable[..., tuple[bool, str | None]] | None,
) -> CommandValidator | None:
    if validator is None:
        return None

    class _FunctionalValidator:
        def __init__(self, func: Callable[..., tuple[bool, str | None]]) -> None:
            self._func = func

        def validate(
            self,
            exit_code: int,
            stdout: str,
            stderr: str,
            duration: float,
            parameter_count: int = 0,
        ) -> tuple[bool, str | None]:
            return self._func(
                exit_code,
                stdout,
                stderr,
                duration,
                parameter_count=parameter_count,
            )

    return _FunctionalValidator(validator)


@dataclass
class _JsonStreamParser:
    get_param_name: Callable[[Mapping[str, Any]], str]

    def feed(
        self,
        line: str,
        is_error: bool,
        context: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if is_error:
            return []
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return []
        param_name = self.get_param_name(context or {})
        if not param_name:
            return []
        if isinstance(payload, Mapping):
            value = payload.get("value")
            if value is None:
                return []
            event = {"param_name": param_name, "value": value}
            for key in ("unit", "timestamp", "metadata"):
                if key in payload:
                    event[key] = payload[key]
            return [event]
        return []


@dataclass
class _TextLineParser:
    get_param_name: Callable[[Mapping[str, Any]], str]

    def feed(
        self,
        line: str,
        is_error: bool,
        context: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if is_error:
            return []
        param_name = self.get_param_name(context or {})
        if not param_name:
            return []
        stripped = line.strip()
        if not stripped:
            return []
        return [{"param_name": param_name, "value": stripped}]

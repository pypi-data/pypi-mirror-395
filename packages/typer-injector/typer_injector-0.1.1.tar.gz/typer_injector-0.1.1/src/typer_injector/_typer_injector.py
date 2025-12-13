from functools import wraps
from typing import Callable, ParamSpec, cast

import typer
from typer.models import CommandFunctionType

from typer_injector._inject import inject


_P = ParamSpec('_P')


def _make_injecting_command(
    super_method: Callable[_P, Callable[[CommandFunctionType], CommandFunctionType]] = typer.Typer.command,
) -> Callable[_P, Callable[[CommandFunctionType], CommandFunctionType]]:
    """Wrap `Typer.command` while preserving its typer signature."""

    @wraps(super_method)
    def injecting_command(*args: _P.args, **kwargs: _P.kwargs) -> Callable[[CommandFunctionType], CommandFunctionType]:
        super_decorator = super_method(*args, **kwargs)

        def injecting_decorator(f: CommandFunctionType) -> CommandFunctionType:
            super_decorator(cast(CommandFunctionType, inject(f)))
            return f

        return injecting_decorator

    return injecting_command


class InjectingTyper(typer.Typer):
    """Typer subclass with dependency injection support."""

    command = _make_injecting_command()

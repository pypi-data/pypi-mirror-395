"""Unit tests."""

import pytest
import typer
from typer.testing import CliRunner
from typing_extensions import Annotated

from typer_injector import Depends, InjectingTyper
from typer_injector.exceptions import CircularDependencyError, ParameterNameConflictError


def test_simple_dependency() -> None:
    """Test a simple dependency."""
    app = InjectingTyper()

    def simple_dependency(a: Annotated[str, typer.Option()], b: Annotated[int, typer.Option()]) -> tuple[str, int]:
        return a, b

    @app.command()
    def cmd(dep: Annotated[tuple[str, int], Depends(simple_dependency)]) -> tuple[str, int]:
        return dep

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337'],
        standalone_mode=False,
    ).return_value == ('hello', 1337)


def test_nested_dependency() -> None:
    """Test a nested dependency."""
    app = InjectingTyper()

    def inner_dependency(a: Annotated[str, typer.Option()], b: Annotated[int, typer.Option()]) -> tuple[str, int]:
        return a, b

    def outer_dependency(
        inner: Annotated[tuple[str, int], Depends(inner_dependency)],
        c: Annotated[bool, typer.Option()],
    ) -> tuple[tuple[str, int], float]:
        return inner, c

    @app.command()
    def cmd(dep: Annotated[tuple[str, int, float], Depends(outer_dependency)]) -> tuple[str, int, float]:
        return dep

    runner = CliRunner()

    assert runner.invoke(
        app,
        ['--a', 'hello', '--b', '1337', '--c'],
        standalone_mode=False,
    ).return_value == (
        ('hello', 1337),
        True,
    )


def test_dendency_caching() -> None:
    """Test dependency caching."""
    app = InjectingTyper()

    def obj_dependency() -> object:
        return object()

    @app.command()
    def cmd(
        dep1: Annotated[object, Depends(obj_dependency)],
        dep2: Annotated[object, Depends(obj_dependency)],
    ) -> tuple[object, object]:
        return dep1, dep2

    runner = CliRunner()

    result = runner.invoke(
        app,
        [],
        standalone_mode=False,
    ).return_value

    assert result[0] is result[1]


def test_parameter_conflict() -> None:
    """Test that parameter conflict raises an error."""
    app = InjectingTyper()

    def conflicting_dependency(a: Annotated[str, typer.Option()]) -> str:
        return a

    with pytest.raises(ParameterNameConflictError):

        @app.command()
        def cmd(
            a: Annotated[str, typer.Option()],
            dep: Annotated[str, Depends(conflicting_dependency)],
        ) -> None:
            pass


def test_circular_dependency() -> None:
    """Test that circular dependency raises an error."""
    app = InjectingTyper()

    global dep_b  # necessary for evaluation of forward reference

    def dep_a(b: 'Annotated[str, Depends(dep_b)]') -> str:
        return b

    def dep_b(a: Annotated[str, Depends(dep_a)]) -> str:
        return a

    with pytest.raises(CircularDependencyError):

        @app.command()
        def cmd(
            dep: Annotated[str, Depends(dep_a)],
        ) -> None:
            pass

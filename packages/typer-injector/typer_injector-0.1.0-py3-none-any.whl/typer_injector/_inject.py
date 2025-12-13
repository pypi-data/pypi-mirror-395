from collections.abc import Iterator
from functools import update_wrapper
import inspect
from inspect import Parameter, signature
from typing import Annotated, Any, Callable, NamedTuple, get_origin

from ._types import Depends, ParameterSourceEntry
from .exceptions import CircularDependencyError, ParameterNameConflictError, TyperInjectorError


def get_depends(annotation: Any) -> Depends | None:
    """Retrieve the `Depends` metadata from an annotation, if present."""
    if get_origin(annotation) is Annotated:
        for meta in annotation.__metadata__:
            if isinstance(meta, Depends):
                return meta

    return None


class FlattenedParam(NamedTuple):
    parameter: Parameter
    source: tuple[ParameterSourceEntry, ...]


def collect_params(
    func: Callable[..., Any],
    source: tuple[ParameterSourceEntry, ...] = (),
    processed_dependencies: set[Depends] | None = None,
) -> Iterator[FlattenedParam]:
    """Iterate over the parameters of `func`, recursing into dependencies' parameters.

    If the same dependency is encountered multiple times, it will only be processed once.

    Tracks the source of each parameter for error reporting purposes.
    """
    if processed_dependencies is None:
        processed_dependencies = set()

    sig = signature(func)
    for param in sig.parameters.values():
        if not (depends := get_depends(param.annotation)):
            yield FlattenedParam(param.replace(kind=Parameter.KEYWORD_ONLY), source)
            continue

        # Check for circular dependencies
        if any(depends == entry.depends for entry in source):
            raise CircularDependencyError(source + (ParameterSourceEntry(param.name, depends),), func)

        # Skip already processed dependencies
        if depends in processed_dependencies:
            continue
        processed_dependencies.add(depends)

        dependency_sig = signature(depends.dependency)
        for dep_param in dependency_sig.parameters.values():
            if dep_param.kind == Parameter.POSITIONAL_ONLY:
                raise TyperInjectorError('Positional-only parameters are not supported in dependencies')

        yield from collect_params(
            depends.dependency,
            source + (ParameterSourceEntry(param.name, depends),),
            processed_dependencies,
        )


def invoke_with_dependencies(
    func: Callable[..., Any],
    kwargs: dict[str, Any],
    resolved_dependencies: dict[Depends, Any],
) -> Any:
    """Invoke `func` with `kwargs`, recursively resolving and caching dependencies."""
    sig = signature(func)
    func_kwargs: dict[str, Any] = {}
    for param in sig.parameters.values():
        if depends := get_depends(param.annotation):
            if depends not in resolved_dependencies:
                # Resolve dependency and cache result
                resolved_dependencies[depends] = invoke_with_dependencies(
                    depends.dependency,
                    kwargs,
                    resolved_dependencies,
                )
            func_kwargs[param.name] = resolved_dependencies[depends]
        else:
            func_kwargs[param.name] = kwargs.pop(param.name)

    return func(**func_kwargs)


def flatten_signature(func: Callable[..., Any]) -> inspect.Signature:
    """Create a new function signature by recurisvely expanding transient parameters from dependencies."""
    new_params: dict[str, Parameter] = {}
    param_sources: dict[str, tuple[ParameterSourceEntry, ...]] = {}

    for param, source in collect_params(func):
        if param.name in new_params:
            raise ParameterNameConflictError(param.name, source, param_sources[param.name], func)
        new_params[param.name] = param
        param_sources[param.name] = source

    return signature(func).replace(parameters=list(new_params.values()))


def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    """Inject dependencies into a function.

    The decorated function's signature will be flattened to include parameters from its dependencies.
    When invoked, dependencies will be resolved recursively.

    :param func: The function to decorate.
    :return: The decorated function with dependency injection enabled.
    """
    new_signature = flatten_signature(func)

    def wrapper(**kwargs: Any) -> Any:
        return invoke_with_dependencies(func, kwargs, {})

    update_wrapper(wrapper, func)
    wrapper.__signature__ = new_signature  # pyright: ignore[reportFunctionMemberAccess]
    return wrapper

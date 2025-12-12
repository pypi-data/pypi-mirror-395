from __future__ import annotations

import functools
from collections.abc import Iterable
from functools import wraps
from typing import (
    TYPE_CHECKING,
    ParamSpec,
    TypeVar,
    TypeVarTuple,
    overload,
)

from brikk.returns import Error, Nothing, Ok, Option, Result, Some

if TYPE_CHECKING:
    from collections.abc import Callable

P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")
AnyE = TypeVar("AnyE")
E = TypeVar("E", bound=Exception)
Ts = TypeVarTuple("Ts")


def result_of(
    func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
) -> Result[T, Exception]:
    """Execute a function and wrap its result in a Result.

    :param Callable[P, T] func: The function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.

    :Example:

    >>> def div(a, b):
    ...     return a / b
    >>> result_of(div, 4, 2)
    Ok(2.0)
    >>> result_of(div, 4, 0)
    Error(ZeroDivisionError(...))

    :return: Ok(value) if successful, Error(exception) otherwise.
    :rtype: Result[T, Exception]
    """
    return as_result(func, (Exception,))(*args, **kwargs)


def optional_of(
    func: Callable[P, T | None], *args: P.args, **kwargs: P.kwargs
) -> Option[T]:
    """Execute a function and wrap its result in an Option.

    :param Callable[P, T | None] func: The function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.

    :Example:

    >>> def find(x):
    ...    return x if x > 0 else None
    >>> optional_of(find, 5)
    Some(5)
    >>> optional_of(find, -1)
    Nothing()

    :return: Some(value) if not None, Nothing otherwise.
    :rtype: Option[T]
    """
    return as_optional(func)(*args, **kwargs)


def as_result(
    func: Callable[P, T],
    exceptions: tuple[type[E], ...] = (Exception,),
) -> Callable[P, Result[T, E]]:
    """Wrap a function so its result is returned as a Result.

    :param Callable[P, T] func: The function to wrap.
    :param tuple exceptions: Exception types to catch.

    :Example:

    >>> def div(a, b):
    ...     return a / b
    >>> as_result(div)(4, 2)
    Ok(2.0)
    >>> as_result(div)(4, 2)
    Error(ZeroDivisionError(...))

    :return: Wrapped function returning Ok or Error.
    :rtype: Callable[P, Result[T, E]]
    """

    @wraps(func)
    def _wrapped(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        try:
            return Ok(func(*args, **kwargs))
        except exceptions as e:
            return Error(e)

    return _wrapped


def as_optional(func: Callable[P, T | None]) -> Callable[P, Option[T]]:
    """Wrap a function so its result is returned as an Option.

    :param Callable[P, T | None] func: The function to wrap.

    :Example:

    >>> @as_optional
    ... def find(x):
    ...     return x if x > 0 else None
    >>> find(5)
    Some(5)
    >>> find(-1)
    Nothing()

    :return: Wrapped function returning Some or Nothing.
    :rtype: Callable[P, Option[T]]
    """

    @wraps(func)
    def _wrapped(*args: P.args, **kwargs: P.kwargs) -> Option[T]:
        result = func(*args, **kwargs)
        if result is None:
            return Nothing()
        return Some(result)

    return _wrapped


def safe(
    exceptions: tuple[type[E], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, Result[T, E]]]:
    """Return a decorator that wraps a function to return a Result.

    :param tuple exceptions: Exception types to catch.

    :Example:

    >>> @safe((ZeroDivisionError,))
    ... def div(a, b):
    ...     return a / b
    >>> div(4, 2)
    Ok(2.0)
    >>> div(4, 0)
    Error(ZeroDivisionError(...))

    :return: Decorator for wrapping functions to return Result.
    :rtype: Callable[[Callable[P, T]], Callable[P, Result[T, E]]]
    """

    def _make(func: Callable[P, T]):
        return as_result(func, exceptions)

    return _make


@overload
def collect(
    initial: Result[tuple[T, ...], AnyE], iterable: Iterable[Result[T, AnyE]]
) -> Result[tuple[T, ...], AnyE]: ...


@overload
def collect(
    initial: Option[tuple[T, ...]], iterable: Iterable[Option[T]]
) -> Option[tuple[T, ...]]: ...


def collect(
    initial: Result[tuple[T, ...], AnyE] | Option[tuple[T, ...]],
    iterable: Iterable[Result[T, AnyE]] | Iterable[Option[T]],
) -> Result[tuple[T, ...], AnyE] | Option[tuple[T, ...]]:
    return functools.reduce(
        lambda a, b: a.and_then(lambda initial: b.map(lambda value: (*initial, value))),  # type: ignore
        iterable,
        initial,
    )


def unpack(func: Callable[[*Ts], T]) -> Callable[[tuple[*Ts]], T]:
    @wraps(func)
    def _wrapper(args: tuple[*Ts]) -> T:
        return func(*args)

    return _wrapper


@overload
def zipped(
    func: Callable[[T], Result[U, AnyE]],
) -> Callable[[T], Result[tuple[T, U], AnyE]]: ...
@overload
def zipped(
    func: Callable[[T], Option[U]],
) -> Callable[[T], Option[tuple[T, U]]]: ...
@overload
def zipped(
    func: Callable[[*Ts], Result[U, AnyE]],
) -> Callable[[tuple[*Ts]], Result[tuple[*Ts, U], AnyE]]: ...
@overload
def zipped(
    func: Callable[[*Ts], Option[U]],
) -> Callable[[tuple[*Ts]], Option[tuple[*Ts, U]]]: ...


def zipped(func):  # type: ignore
    @wraps(func)
    def _wrapper(*args):
        if len(args) == 1 and isinstance(args[0], tuple):
            _args = args[0]
        else:
            _args = args

        return func(*_args).map(lambda other: (*_args, other))

    return _wrapper

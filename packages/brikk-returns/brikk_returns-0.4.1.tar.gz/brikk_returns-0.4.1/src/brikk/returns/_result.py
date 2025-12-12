from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeAlias,
    TypeGuard,
    TypeVar,
    TypeVarTuple,
    cast,
)

from brikk.returns._errors import ResultExpectError, ResultUnwrapError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from brikk.returns import Nothing, Option, Some


T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")
Ts = TypeVarTuple("Ts")
_AnyException = TypeVar("_AnyException", bound=Exception)


def is_ok(result: Result[T, E]) -> TypeGuard[Ok[T, E]]:
    return result.is_ok()


def is_err(result: Result[T, E]) -> TypeGuard[Error[T, E]]:
    return result.is_err()


Result: TypeAlias = "Ok[T, E] | Error[T, E]"


class _ResultBase(Generic[T, E]):
    def __init__(self, **kwargs) -> None:
        if "value" in kwargs:
            self.value = cast(T, kwargs["value"])
        if "error" in kwargs:
            self.error = cast(E, kwargs["error"])

    def is_ok(self) -> bool:
        return hasattr(self, "value")

    def is_ok_and(self, func: Callable[[T], bool]) -> bool:
        return self.is_ok() and func(self.value)

    def is_err(self) -> bool:
        return hasattr(self, "error")

    def is_err_and(self, func: Callable[[E], bool]) -> bool:
        return self.is_err() and func(self.error)

    def ok(self) -> Option[T]:
        from brikk.returns import Nothing, Some

        if hasattr(self, "value"):
            return Some(self.value)
        return Nothing()

    def err(self) -> Option[E]:
        from brikk.returns import Nothing, Some

        if hasattr(self, "error"):
            return Some(self.error)
        return Nothing()

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        if self.is_ok():
            return Ok(func(self.value))
        return Error(self.error)

    def map_or(self, default: U, func: Callable[[T], U]) -> U:
        if self.is_ok():
            return func(self.value)
        return default

    def map_or_else(self, default: Callable[[E], U], func: Callable[[T], U]) -> U:
        if self.is_ok():
            return func(self.value)
        return default(self.error)

    def map_err(self, func: Callable[[E], F]) -> Result[T, F]:
        if self.is_err():
            return Error(func(self.error))
        return Ok(self.value)

    def inspect(self, func: Callable[[T], None]) -> Result[T, E]:
        if self.is_ok():
            func(self.value)
        return self  # type: ignore

    def inspect_err(self, func: Callable[[E], None]) -> Result[T, E]:
        if self.is_err():
            func(self.error)
        return self  # type: ignore

    def iter(self) -> Iterator[T]:
        if self.is_ok():
            yield self.value

    def expect(self, msg: str) -> T:
        if self.is_ok():
            return self.value

        _msg = f"{msg}: {self.error}"
        raise ResultExpectError(_msg)

    def unwrap(self) -> T:
        if self.is_ok():
            return self.value

        _msg = f"{self.error}"
        raise ResultUnwrapError(_msg)

    def expect_err(self, msg: str) -> E:
        if self.is_err():
            return self.error

        _msg = f"{msg}: {self.value}"
        raise ResultExpectError(_msg)

    def unwrap_err(self) -> E:
        if self.is_err():
            return self.error

        _msg = f"{self.value}"
        raise ResultUnwrapError(_msg)

    def and_(self, result: Result[U, E]) -> Result[U, E]:
        if self.is_ok():
            return result
        return Error(self.error)

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        if self.is_ok():
            return func(self.value)
        return Error(self.error)

    def or_(self, default: Result[T, F]) -> Result[T, F]:
        if self.is_err():
            return default
        return Ok(self.value)

    def or_else(self, default: Callable[[E], Result[T, F]]) -> Result[T, F]:
        if self.is_err():
            return default(self.error)
        return Ok(self.value)

    def unwrap_or(self, default: T) -> T:
        if self.is_ok():
            return self.value
        return default

    def unwrap_or_else(self, default: Callable[[E], T]) -> T:
        if self.is_ok():
            return self.value
        return default(self.error)

    def unwrap_or_raise(self: _ResultBase[T, _AnyException]) -> T:
        if self.is_err():
            raise self.error
        return self.value


class Ok(_ResultBase[T, E]):
    __match_args__ = ("value",)
    __slots__ = ("value",)

    value: T

    def __init__(self, value: T) -> None:
        super().__init__(value=value)

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return other.value == self.value
        return False

    def flatten(
        self: Ok[Ok[U, E], E] | Ok[Error[U, E], E] | Ok[Result[U, E], E],
    ) -> Result[U, E]:
        return self.and_then(lambda val: val)

    def transpose(
        self: Ok[Some[U], E] | Ok[Nothing[U], E] | Ok[Option[U], E],
    ) -> Option[Result[U, E]]:
        from brikk.returns import Nothing, Some, is_some

        if is_some(self.value):
            return Some(Ok(self.value.value))
        return Nothing()


class Error(_ResultBase[T, E]):
    __match_args__ = ("error",)
    __slots__ = ("error",)

    error: E

    def __init__(self, error: E) -> None:
        super().__init__(error=error)

    def __repr__(self) -> str:
        return f"Error({self.error!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Error):
            return other.error == self.error
        return False

    def flatten(
        self: Error[Ok[U, E], E] | Error[Error[U, E], E] | Error[Result[U, E], E],
    ) -> Result[U, E]:
        return self.and_then(lambda val: val)

    def transpose(
        self: Error[Some[U], E] | Error[Nothing[U], E] | Error[Option[U], E],
    ) -> Option[Result[U, E]]:
        from brikk.returns import Some

        return Some(Error(self.error))

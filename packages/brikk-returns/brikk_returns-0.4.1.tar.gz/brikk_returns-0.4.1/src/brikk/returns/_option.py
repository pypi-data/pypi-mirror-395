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

from brikk.returns._errors import OptionExpectError, OptionUnwrapError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from brikk.returns import Error, Ok, Result


T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
Ts = TypeVarTuple("Ts")

Option: TypeAlias = "Some[T] | Nothing[T]"


def is_some(result: Option[T]) -> TypeGuard[Some[T]]:
    return result.is_some()


def is_none(result: Option[T]) -> TypeGuard[Nothing[T]]:
    return result.is_none()


class _OptionBase(Generic[T]):
    def __init__(self, **kwargs) -> None:
        if "value" in kwargs:
            self.value = cast(T, kwargs["value"])

    def is_some(self) -> bool:
        return hasattr(self, "value")

    def is_some_and(self, func: Callable[[T], bool]) -> bool:
        return self.is_some() and func(self.value)

    def is_none(self) -> bool:
        return not hasattr(self, "value")

    def is_none_or(self, func: Callable[[T], bool]) -> bool:
        return self.is_none() or func(self.value)

    def expect(self, msg: str) -> T:
        if self.is_some():
            return self.value
        raise OptionExpectError(msg)

    def unwrap(self) -> T:
        if self.is_some():
            return self.value
        raise OptionUnwrapError

    def unwrap_or(self, default: T) -> T:
        if self.is_some():
            return self.value
        return default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        if self.is_some():
            return self.value
        return func()

    def map(self, func: Callable[[T], U]) -> Option[U]:
        if self.is_some():
            return Some(func(self.value))
        return Nothing()

    def inspect(self, func: Callable[[T], None]) -> Option[T]:
        if self.is_some():
            func(self.value)
        return Nothing()

    def map_or(self, default: U, func: Callable[[T], U]) -> U:
        if self.is_some():
            return func(self.value)
        return default

    def map_or_else(self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        if self.is_some():
            return func(self.value)
        return default()

    def ok_or(self, error: E) -> Result[T, E]:
        from brikk.returns import Error, Ok

        if self.is_some():
            return Ok(self.value)
        return Error(error)

    def ok_or_else(self, error: Callable[[], E]) -> Result[T, E]:
        from brikk.returns import Error, Ok

        if self.is_some():
            return Ok(self.value)
        return Error(error())

    def iter(self) -> Iterator[T]:
        if self.is_some():
            yield self.value

    def and_(self, option: Option[U]) -> Option[U]:
        if self.is_some():
            return option
        return Nothing()

    def and_then(self, func: Callable[[T], Option[U]]) -> Option[U]:
        if self.is_some():
            return func(self.value)
        return Nothing()

    def filter(self, predicate: Callable[[T], bool]) -> Option[T]:
        if self.is_some_and(predicate):
            return Some(self.value)
        return Nothing()

    def or_(self, default: Option[T]) -> Option[T]:
        if self.is_none():
            return default
        return Some(self.value)

    def or_else(self, default: Callable[[], Option[T]]) -> Option[T]:
        if self.is_some():
            return Some(self.value)
        return default()

    def xor(self, option: Option[T]) -> Option[T]:
        if self.is_some() != option.is_some():
            return Some(self.value) if self.is_some() else Some(option.value)
        return Nothing()


class Some(_OptionBase[T]):
    __match_args__ = ("value",)
    __slots__ = ("value",)

    value: T

    def __init__(self, value: T) -> None:
        super().__init__(value=value)

    def __repr__(self) -> str:
        return f"Some({self.value!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Some):
            return other.value == self.value
        return False

    def flatten(self: Some[Option[U]] | Some[Some[U]] | Some[Nothing[U]]) -> Option[U]:
        return self.and_then(lambda val: val)

    def transpose(
        self: Some[Result[U, E]] | Some[Ok[U, E]] | Some[Error[U, E]],
    ) -> Result[Option[U], E]:
        from brikk.returns import Error, Ok

        match self.value:
            case Ok(val):
                return Ok(Some(val))
            case Error(err):
                return Error(err)


class Nothing(_OptionBase[T]):
    __slots__ = tuple()

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return "Nothing()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Nothing)

    def flatten(
        self: Nothing[Option[U]] | Nothing[Some[U]] | Nothing[Nothing[U]],
    ) -> Option[U]:
        return self.and_then(lambda val: val)

    def transpose(
        self: Nothing[Result[U, E]] | Nothing[Ok[U, E]] | Nothing[Error[U, E]],
    ) -> Result[Option[U], E]:
        from brikk.returns import Ok

        return Ok(Nothing())

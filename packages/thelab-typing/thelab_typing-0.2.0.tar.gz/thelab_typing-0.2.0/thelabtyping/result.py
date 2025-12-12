"""
Inspired in part by:

- https://github.com/rustedpy/result
- https://gcanti.github.io/fp-ts/

Provides an Either / Result type, as well as a decorator to convert normal
exception-throwing functions into functions which return a Result type.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable, Iterator
from functools import wraps
from typing import Any, Literal, NoReturn, Self


class UnwrapError(TypeError):
    """Raised when attempting to unwrap a Result in the wrong state."""

    pass


class DoException[E](Exception):
    """
    This is used to signal to `do()` that the result is an `Err`,
    which short-circuits the generator and returns that Err.
    Using this exception for control flow in `do()` allows us
    to simulate `and_then()` in the Err case: namely, we don't call `op`,
    we just return `self` (the Err).
    """

    def __init__(self, err: Err[E]) -> None:
        self.err = err


class _Result[_OK, _Err](ABC):
    """Abstract base class for Result types."""

    ok_value: _OK
    err_value: _Err

    @property
    @abstractmethod
    def is_ok(self) -> bool: ...  # pragma: no cover

    @property
    @abstractmethod
    def is_err(self) -> bool: ...  # pragma: no cover

    @abstractmethod
    def ok(self) -> _OK | None: ...  # pragma: no cover

    @abstractmethod
    def err(self) -> _Err | None: ...  # pragma: no cover

    def unwrap(self) -> _OK:
        if self.is_ok:
            return self.ok_value
        raise UnwrapError("Called Either.unwrap() on an Err value")

    def unwrap_err(self) -> _Err:
        if self.is_err:
            return self.err_value
        raise UnwrapError("Called Either.unwrap_err() on an Ok value")


class Ok[_OK](_Result[_OK, None]):
    """Represents a successful result containing a value."""

    def __init__(self, value: _OK) -> None:
        self.ok_value = value
        self.err_value = None

    def __iter__(self) -> Iterator[_OK]:
        yield self.ok_value

    def __repr__(self) -> str:
        return f"Ok({repr(self.ok_value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self.ok_value == other.ok_value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self.ok_value))

    @property
    def is_ok(self) -> Literal[True]:
        return True

    @property
    def is_err(self) -> Literal[False]:
        return False

    def ok(self) -> _OK:
        return self.ok_value

    def err(self) -> None:
        return None

    def and_then[L, R](self, op: Callable[[_OK], Result[L, R]]) -> Result[L, R]:
        return op(self.ok_value)


class Err[_Err](_Result[None, _Err]):
    """Represents a failed result containing an error."""

    def __init__(self, value: _Err) -> None:
        self.ok_value = None
        self.err_value = value

    def __iter__(self) -> Iterator[NoReturn]:
        def _iter() -> Iterator[NoReturn]:
            # Exception will be raised when the iterator is advanced, not
            # when it's created
            raise DoException(self)
            # This yield will never be reached, but is necessary to create a
            # generator
            yield

        return _iter()

    def __repr__(self) -> str:
        return f"Err({repr(self.err_value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self.err_value == other.err_value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self.err_value))

    @property
    def is_ok(self) -> Literal[False]:
        return False

    @property
    def is_err(self) -> Literal[True]:
        return True

    def ok(self) -> None:
        return None

    def err(self) -> _Err:
        return self.err_value

    def and_then(self, op: object) -> Self:
        return self


type Result[_OK, _Err] = Ok[_OK] | Err[_Err]


def as_result[**P, R, E: Exception](
    *catch: type[E],
) -> Callable[[Callable[P, R]], Callable[P, Result[R, E]]]:
    """Decorator that converts exception-throwing functions to return Result types."""

    def decorator(fn: Callable[P, R]) -> Callable[P, Result[R, E]]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
            try:
                val = fn(*args, **kwargs)
                return Ok(val)
            except catch as e:
                return Err(e)

        return wrapper

    return decorator


def do[T, E](gen: Generator[Result[T, E]]) -> Result[T, E]:
    """
    Do notation for Result (syntactic sugar for sequence of `and_then()` calls).
    """
    try:
        return next(gen)
    except DoException as e:
        out: Err[E] = e.err
        return out


def partition_results[T, E](
    results: Iterable[Result[T, E]],
) -> tuple[
    list[T],
    list[E],
]:
    """
    Take an iterable of Results and partition them into two lists, one with all
    the OK values, one with all the Err values.
    """
    oks: list[T] = []
    errs: list[E] = []
    for res in results:
        if res.is_ok:
            oks.append(res.ok_value)
        else:
            errs.append(res.err_value)
    return oks, errs

from __future__ import annotations
from typing import Callable, Any, Iterable, TypeVar, cast

"""
PURELY 💧
A lightweight library for cleaner, safer, and more fluent Python.
Embrace purity, banish boilerplate.
"""

# Sentinel for missing values
_SENTINEL = object()

# Type variable for generics
T = TypeVar("T")


# -----------------------------------------------------------------------------
# 1. RUST-STYLE OPTION (Defined first for dependency reasons)
# -----------------------------------------------------------------------------


class Option[T]:
    """
    A container that represents either a value (Some) or nothing (None).

    It wraps any object and provides general attribute access (getattr),
    item getters and setters, and calling, to allow null-safe navigation.
    """

    def __init__(self, value: T | None):
        self._value = value

    def is_some(self) -> bool:
        return self._value is not None

    def is_none(self) -> bool:
        return self._value is None

    def unwrap(
        self,
        default: Any = _SENTINEL,
        error: str | Exception = ValueError("Called unwrap on None"),
    ) -> T:
        """Returns the contained value or raises error/returns default."""
        if self._value is not None:
            return self._value

        if default is not _SENTINEL:
            return default

        # Use the global ensure logic (which handles exceptions)
        if isinstance(error, str):
            raise ValueError(error)

        raise error

    def convert[U](self, func: Callable[[T], U]) -> Option[U]:
        """Strictly typed transformation."""
        if self._value is None:
            return Option(None)

        return Option(func(self._value))

    def __or__[U](self, func: Callable[[T], U]) -> Option[U]:
        return self.convert(func)

    def keepif(self, predicate: Callable[[T], bool]) -> Option[T]:
        if self._value is not None and predicate(self._value):
            return self

        return Option(None)

    # --- Null Coalescing / Safe Navigation Proxies ---

    def __getattr__(self, name: str) -> Option[Any]:
        """
        Runtime hook for safe attribute access.
        Option(obj).attr returns Option(obj.attr) or Option(None).
        """
        if self._value is None:
            return Option(None)

        return Option(getattr(self._value, name))

    def __call__(self, *args: Any, **kwargs: Any) -> Option[Any]:
        """
        Runtime hook for safe method calls.
        Option(func)(args) returns Option(func(args)) or Option(None).
        """
        if self._value is None:
            return Option(None)

        caller = getattr(self._value, "__call__")
        return Option(caller(*args, **kwargs))

    def __getitem__(self, key: Any) -> Option[Any]:
        """
        Runtime hook for safe item access.
        Option(obj)[key] returns Option(obj[key]) or Option(None).
        """
        if self._value is None:
            return Option(None)

        getter = getattr(self._value, "__getitem__")
        return Option(getter(key))

    def __setitem__(self, key: Any, value: Any):
        """
        Runtime hook for safe item setting.
        Option(obj)[key] = value will work if the underlying works.
        """
        if self._value is None:
            pass

        setter = getattr(self._value, "__setitem__")
        setter(key, value)

    def __eq__(self, other: object) -> bool:
        """
        Check the underlying value for equality.
        """
        if isinstance(other, Option):
            return self._value == other._value

        return self._value == other


# -----------------------------------------------------------------------------
# 2. CORE UTILITIES (ensure, tap, safe)
# -----------------------------------------------------------------------------


def ensure(
    value: T | Option[T] | None, error: str | Exception = ValueError("Value is None")
) -> T:
    """
    Asserts existence.

    If 'value' is an Option (from safe() runtime), it unwraps it.
    If 'value' is a raw value (from safe() static lie), it checks for None.
    """
    # Runtime check: Handle the 'Safe' proxy case
    if isinstance(value, Option):
        return value.unwrap(error=error)

    if value is None:
        if isinstance(error, str):
            raise ValueError(error)

        raise error

    return cast(T, value)


def safe[T](obj: T | None) -> T:
    """
    Wraps a object in Option[T] but returns T typehint.

    This allows the user you continue using Intellisense
    and type-checking from the IDE but maintaining the
    null-safe navigation.
    """
    return cast(T, Option(obj))


def tap[T](value: T, func: Callable[[T], Any]) -> T:
    """Executes func for side effects and returns value."""
    func(value)
    return value


def pipe[T](value: T, *funcs: Callable[[Any], Any]) -> Any:
    """Pipes value through functions."""
    result = value
    for func in funcs:
        result = func(result)
    return result


# -----------------------------------------------------------------------------
# 3. FLUENT INTERFACE (Chain)
# -----------------------------------------------------------------------------


class Chain[T]:
    """
    A unified, monadic container for:

    1. Pipelines (then)
    2. Vectorized Operations (map, filter)
    3. Error Handling (catch, test)
    """

    def __init__(self, value: T | None, error: Exception | None = None):
        self._value = value
        self._error = error

    @classmethod
    def fail(cls, error: Exception) -> Chain[Any]:
        """Factory: Create a Chain in a failed state."""
        return cls(None, error)

    @property
    def is_ok(self) -> bool:
        return self._error is None

    # --- Pipeline Operations ---

    def then[R](self, func: Callable[[T], R]) -> Chain[R]:
        """
        Pipes the *entire* value through func.

        Chain(5).then(lambda x: x * 2) -> Chain(10)
        Chain(None).then(lambda x: x + 1) -> Chain(Error) [Swallows exception]
        """
        if self._error:
            return cast(Chain[R], self)

        try:
            return Chain(func(self._value))  # type: ignore
        except Exception as e:
            return Chain(None, error=e)

    def __or__[R](self, func: Callable[[T], R]) -> Chain[R]:
        """Syntactic sugar for .then()"""
        return self.then(func)

    def tap(self, func: Callable[[T], Any]) -> Chain[T]:
        if self.is_ok:
            try:
                func(self._value)  # type: ignore
            except Exception as e:
                return Chain(None, e)

        return self

    # --- Vectorized Operations (Seq) ---

    def map[R](self, func: Callable[[Any], R]) -> Chain[Iterable[R]]:
        """
        Maps func over *each item* in the internal value.

        Requirements:
        1. Value must be Iterable (list, tuple, etc.)
        2. Value must NOT be str or bytes (to avoid accidental char mapping)

        If requirements fail, the Chain switches to Error state.
        """
        if self._error:
            return cast(Chain[Iterable[R]], self)

        try:
            val = self._value

            if not isinstance(val, Iterable) or isinstance(val, (str, bytes)):
                raise TypeError(
                    f"Chain.map expects a non-string Iterable, got {type(val).__name__}"
                )

            # Greedily evaluate to list to catch errors immediately during iteration
            return Chain([func(x) for x in val])
        except Exception as e:
            return Chain(None, error=e)

    def filter(self, predicate: Callable[[Any], bool]) -> Chain[list]:
        """
        Filters *each item* in the internal value.
        Same strict iterable requirements as .map().
        """
        if self._error:
            return cast(Chain[list], self)

        try:
            val = self._value
            if not isinstance(val, Iterable) or isinstance(val, (str, bytes)):
                raise TypeError(
                    f"Chain.filter expects a non-string Iterable, got {type(val).__name__}"
                )

            return Chain([x for x in val if predicate(x)])
        except Exception as e:
            return Chain(None, error=e)

    # --- Error Handling & Exiting ---

    def unwrap(self, default: Any = _SENTINEL) -> T:
        """
        Returns value if OK.
        If Error: Raises the error (or returns default if provided).
        """
        if self._error is None:
            return cast(T, self._value)

        if default is not _SENTINEL:
            return default

        raise self._error

    def catch(self, func: Callable[[Exception], T]) -> Chain[T]:
        """
        Recovers from an error state.
        If Error: Runs func(error) to get a new value (and clears error).
        If OK: Skips.
        """
        if self._error is None:
            return self

        try:
            # Recover!
            return Chain(func(self._error))
        except Exception as e:
            # Recovery failed, new error replaces old one
            return Chain(None, error=e)

    def test(self) -> None:
        """
        Terminal check.
        If Error: Raises it immediately.
        If OK: Does nothing.
        Useful for 'asserting' a chain succeeded without returning a value.
        """
        if self._error:
            raise self._error

    def error(self) -> Exception | None:
        """
        Returns the exception object if failed, else None.
        (Renamed from 'fail' to avoid conflict with classmethod factory)
        """
        return self._error

    def __eq__(self, other):
        self.test()

        if isinstance(other, (Chain, Option)):
            return self._value == other.unwrap()

        return self._value == other

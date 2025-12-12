import functools
from typing import Callable, Any

"""
PURELY 💧
A lightweight library for cleaner, safer, and more fluent Python.
Embrace purity, banish boilerplate.
"""

# Sentinel for missing values
_SENTINEL = object()

# -----------------------------------------------------------------------------
# 1. THE ESSENTIALS (Direct helpers)
# -----------------------------------------------------------------------------


def ensure[T](
    value: T | None, error: str | Exception = ValueError("Value is None")
) -> T:
    """
    Takes a value T | None. Returns T or raises an exception.
    Similar to Rust's unwrap().

    Usage:
        user_id = purely.ensure(get_id(), "User ID missing")
    """
    if value is None:
        if isinstance(error, str):
            raise ValueError(error)
        raise error
    return value


def tap[T](value: T, func: Callable[[T], Any]) -> T:
    """
    Executes a function for side effects (like logging) and returns the original value.
    Useful for debugging fluent chains without breaking them.
    """
    func(value)
    return value


def pipe[T](value: T, *funcs: Callable[[Any], Any]) -> Any:
    """
    Pipes a value through a sequence of functions.
    pipe(x, f, g, h) is equivalent to h(g(f(x)))
    """
    result = value
    for func in funcs:
        result = func(result)
    return result


# -----------------------------------------------------------------------------
# 2. THE FLUENT INTERFACE (Chain)
# -----------------------------------------------------------------------------


class Chain[T]:
    """
    A wrapper to allow method chaining on any object.

    Usage:
        Chain(5).map(double).value
        Chain(5) | double | str
    """

    def __init__(self, value: T):
        self._value = value

    def map[U](self, func: Callable[[T], U]) -> "Chain[U]":
        """Apply a function to the contained value."""
        return Chain(func(self._value))

    def then[U](self, func: Callable[[T], U]) -> "Chain[U]":
        """Alias for map, reads better in some contexts."""
        return self.map(func)

    def __or__[U](self, func: Callable[[T], U]) -> "Chain[U]":
        """
        Allows usage of the pipe operator | to chain functions.
        Chain(5) | double | str
        """
        return self.map(func)

    def tap(self, func: Callable[[T], Any]) -> "Chain[T]":
        """Run a side effect, ignore return, pass original value forward."""
        func(self._value)
        return self

    def ensure(
        self, error: str | Exception = ValueError("Chain value is None")
    ) -> "Chain[T]":
        """Asserts the internal value is not None."""
        ensure(self._value, error)
        return self

    def __eq__(self, other: object) -> bool:
        """Checks equality against another Chain or the raw value."""
        if isinstance(other, Chain):
            return self._value == other._value

        return self._value == other

    @property
    def value(self) -> T:
        """Return the raw value (property). No checks performed."""
        return self._value


# -----------------------------------------------------------------------------
# 3. RUST-STYLE OPTION (Safe handling)
# -----------------------------------------------------------------------------


class Option[T]:
    """
    A container that represents either a value (Some) or nothing (None).
    Forces safe handling of nullables.
    """

    def __init__(self, value: T | None):
        self._value = value

    @classmethod
    def of(cls, value: T | None) -> "Option[T]":
        return cls(value)

    def is_some(self) -> bool:
        return self._value is not None

    def is_none(self) -> bool:
        return self._value is None

    def unwrap(
        self,
        default: Any = _SENTINEL,
        error: str | Exception = ValueError("Called unwrap on None"),
    ) -> T:
        """
        Returns the contained value.

        If the value is None:
            1. Returns 'default' if provided.
            2. Raises 'error' if no default is provided.
        """
        if self._value is not None:
            return self._value

        if default is not _SENTINEL:
            return default

        return ensure(self._value, error)

    def map[U](self, func: Callable[[T], U]) -> "Option[U]":
        """If Some, applies func. If None, stays None."""
        if self._value is None:
            return Option(None)

        return Option(func(self._value))

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        """If Some and predicate is true, keep it. Else become None."""
        if self._value is not None and predicate(self._value):
            return self

        return Option(None)

    def __eq__(self, other: object) -> bool:
        """Checks equality against another Option or the raw value."""
        if isinstance(other, Option):
            return self._value == other._value

        return self._value == other

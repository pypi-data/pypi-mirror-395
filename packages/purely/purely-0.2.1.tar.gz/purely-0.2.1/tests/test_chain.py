import pytest
from purely.core import Chain, Option, safe, ensure

# -----------------------------------------------------------------------------
# 1. PIPELINE TESTS (.then)
# -----------------------------------------------------------------------------


def test_chain_pipeline_happy_path():
    """
    Verify standard top-to-bottom chaining.
    Flow: 5 -> 10 -> "10" -> "10!"
    """
    res = Chain(5).then(lambda x: x * 2).then(str).then(lambda s: s + "!").unwrap()
    assert res == "10!"


def test_chain_pipeline_pipe_operator():
    """
    Verify the | operator works as an alias for .then()
    """
    res = (Chain(5) | (lambda x: x + 5) | str).unwrap()
    assert res == "10"


def test_chain_pipeline_error_capture():
    """
    Verify that exceptions in the pipeline are caught and stored,
    stopping execution of subsequent steps.
    """

    def broken_func(x):
        raise ValueError("Something went wrong")

    # The chain should NOT raise immediately
    c = (
        Chain(10)
        .then(lambda x: x * 2)  # 20
        .then(broken_func)  # Fails here
        .then(lambda x: x + 100)  # Should be skipped
    )

    # Assert state
    assert not c.is_ok
    assert isinstance(c.error(), ValueError)

    # Now verify it raises on unwrap
    with pytest.raises(ValueError, match="Something went wrong"):
        c.unwrap()


def test_chain_pipeline_none_handling():
    """
    Verify Chain treats None as a normal value until it causes an issue.
    """
    # Case 1: Function handles None fine
    # str(None) -> "None" (Valid)
    res = Chain(None).then(str).unwrap()
    assert res == "None"

    # Case 2: Function chokes on None
    # None + 1 -> TypeError (Caught by Chain)
    c = Chain(None).then(lambda x: x + 1)
    assert not c.is_ok
    assert isinstance(c.error(), TypeError)


# -----------------------------------------------------------------------------
# 2. VECTORIZED OPERATIONS (.map / .filter)
# -----------------------------------------------------------------------------


def test_chain_map_vectorized_list():
    """Verify .map() applies function to each item in a list."""
    data = [1, 2, 3]
    res = Chain(data).map(lambda x: x * 10).unwrap()
    assert res == [10, 20, 30]


def test_chain_map_fails_on_non_iterable():
    """Verify .map() fails (safely) if the value is not a list/iterable."""
    # Passing an int to .map() should error
    c = Chain(123).map(lambda x: x * 2)

    assert not c.is_ok
    assert isinstance(c.error(), TypeError)
    assert "expects a non-string Iterable" in str(c.error())


def test_chain_map_fails_on_string():
    """
    Verify .map() specifically rejects strings to prevent
    accidental character-wise mapping.
    """
    c = Chain("hello").map(lambda char: char.upper())

    assert not c.is_ok
    assert "expects a non-string Iterable" in str(c.error())


def test_chain_filter_vectorized():
    """Verify .filter() removes items from the internal list."""
    data = [1, 2, 3, 4, 5]
    res = Chain(data).filter(lambda x: x % 2 == 0).unwrap()
    assert res == [2, 4]


def test_chain_filter_fails_safely():
    """Verify .filter() captures errors inside the predicate."""
    data = [1, 2, 3, "four", 5]

    # "four" % 2 will raise TypeError inside the loop
    c = Chain(data).filter(lambda x: x % 2 == 0)

    assert not c.is_ok
    assert isinstance(c.error(), TypeError)


# -----------------------------------------------------------------------------
# 3. ERROR HANDLING & RECOVERY (.catch / .test)
# -----------------------------------------------------------------------------


def test_chain_catch_recovery():
    """Verify .catch() provides a fallback value on error."""
    res = (
        Chain(10)
        .then(lambda x: x / 0)  # ZeroDivisionError
        .catch(lambda e: "Recovered")  # Catch and return string
        .unwrap()
    )
    assert res == "Recovered"


def test_chain_catch_skipped_on_success():
    """Verify .catch() is ignored if there is no error."""
    res = Chain(10).then(lambda x: x + 5).catch(lambda e: 0).unwrap()  # Should not run
    assert res == 15


def test_chain_test_assertion():
    """
    Verify .test() raises the error if present, useful for
    terminating a chain without returning a value.
    """
    # Happy path: does nothing
    Chain(10).test()

    # Error path: raises
    with pytest.raises(ZeroDivisionError):
        Chain(10).then(lambda x: x / 0).test()


# -----------------------------------------------------------------------------
# 4. INTEGRATION: Chain + Option + Safe
# -----------------------------------------------------------------------------


class User:
    def __init__(self, name, friends=None):
        self.name = name
        self.friends = friends or []


def test_integration_chain_and_safe():
    """
    Demonstrate using safe() to navigate objects and Chain() to process lists.
    """
    u1 = User("Alice")
    u2 = User("Bob")
    admin = User("Admin", friends=[u1, u2])

    # Scenario:
    # 1. Safely access admin.friends (returns Option)
    # 2. Unwrap it to get the raw list (or empty list)
    # 3. Use Chain to map over the list and extract names

    friends_list = ensure(safe(admin).friends)

    names = (
        Chain(friends_list)
        .map(lambda u: u.name)  # Vectorized map over users
        .map(lambda n: n.upper())  # Vectorized map over names
        .unwrap()
    )

    assert names == ["ALICE", "BOB"]


def test_integration_mixed_failure():
    """
    Verify a complex chain that fails in the middle of a list processing step.
    """
    # A list with a None in it
    data = [10, 20, None, 40]

    # We try to divide by x. None will cause TypeError. 0 will cause ZeroDivision.

    c = Chain(data).map(lambda x: 100 / x)

    # It should fail because one item (None) caused a TypeError
    assert not c.is_ok
    assert isinstance(c.error(), TypeError)

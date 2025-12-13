import pytest
from purely import ensure, tap, pipe, Chain, Option, safe

# --- Setup: Mock Data Structures for Testing ---


class City:
    def __init__(self, name):
        self.name = name


class Address:
    def __init__(self, city=None, street="Main St"):
        self.city = city
        self.street = street
        self.metadata = {"zip": "12345", "zone": None}

    def get_full_address(self):
        return f"{self.street}, {self.city.name if self.city else 'Unknown'}"


class User:
    def __init__(self, address=None, tags=None):
        self.address = address
        self.tags = tags or []

    def get_primary_tag(self):
        return self.tags[0] if self.tags else None


# --- Tests ---


def test_safe_navigation_happy_path():
    """Test that safe() correctly proxies attributes when they exist."""
    u = User(address=Address(city=City("Berlin")))

    # Chaining attributes: .address.city.name
    res = safe(u).address.city.name
    assert ensure(res) == "Berlin"


def test_safe_navigation_none_in_middle():
    """Test that the chain stops gracefully if an intermediate attribute is None."""
    u = User(address=None)  # Address is missing

    # .address is None, so .city should be safe (returns Option(None))
    res = safe(u).address.city.name

    # ensure() raises because the final result is None (wrapped in Option)
    with pytest.raises(ValueError, match="Chain broken"):
        ensure(res, "Chain broken")


def test_safe_navigation_method_calls():
    """Test that methods can be called safely in the chain."""
    u = User(address=Address(city=City("Paris")))

    # Call .get_full_address() safely
    res = safe(u).address.get_full_address()
    assert ensure(res) == "Main St, Paris"

    # Call a string method at the end (.upper())
    res_upper = safe(u).address.city.name.upper()
    assert ensure(res_upper) == "PARIS"


def test_safe_navigation_method_on_none():
    """Test calling a method on a None value in the chain."""
    u = User(address=None)

    # .address is None, so .get_full_address() should not execute and return Option(None)
    res = safe(u).address.get_full_address()

    assert isinstance(res, Option)
    assert res.is_none()


def test_safe_navigation_indexing():
    """Test that dictionary/list indexing (brackets) works safely."""
    u = User(address=Address())

    # 1. Success case: accessing existing key
    zip_code = safe(u).address.metadata["zip"]
    assert ensure(zip_code) == "12345"

    # 2. Failure case: accessing None value inside dict
    # metadata["zone"] is None. chain continues as Option(None)
    zone = safe(u).address.metadata["zone"]
    assert isinstance(zone, Option)
    assert zone.is_none()


def test_safe_navigation_start_with_none():
    """Test usage when the initial object passed to safe() is None."""
    u: User | None = None

    res = safe(u).address.city
    assert res.is_none()
    assert res.unwrap(default="Nothing") == "Nothing"


def test_mixed_safe_and_functional():
    """Test mixing safe navigation with functional .map() / .filter()."""
    u = User(address=Address(city=City("Tokyo")))

    res = (
        safe(u)
        .address.city.name.convert(  # Safe navigation -> Option("Tokyo")
            lambda s: s.upper()
        )  # Functional map -> Option("TOKYO")
        .keepif(lambda s: "Y" in s)  # Functional filter -> Option("TOKYO")
    )
    assert ensure(res) == "TOKYO"


def test_ensure_integration():
    """
    Verify ensure() works on:
    1. Raw values
    2. Option(value)
    3. Option(None)
    """
    # Raw value
    assert ensure("raw") == "raw"

    # Wrapped Option
    assert ensure(Option("wrapped")) == "wrapped"

    with pytest.raises(ValueError):
        ensure(safe(User()).address)

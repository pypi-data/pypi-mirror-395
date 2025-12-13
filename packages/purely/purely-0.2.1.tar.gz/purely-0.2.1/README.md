# Purely 💧

**A lightweight elixir for cleaner, safer, and more fluent Python.**

<!-- Project badges -->
![PyPI - Version](https://img.shields.io/pypi/v/purely)
![PyPi - Python Version](https://img.shields.io/pypi/pyversions/purely)
![Github - Open Issues](https://img.shields.io/github/issues-raw/apiad/purely)
![PyPi - Downloads (Monthly)](https://img.shields.io/pypi/dm/purely)
![Github - Commits](https://img.shields.io/github/commit-activity/m/apiad/purely)

---

**Purely** is a zero-dependency library designed to bring the best parts of functional programming—safety, pipelines, and immutability—into Python without the academic overhead or complex types. It allows you to write code that reads from top to bottom, rather than inside out.

## 🧠 Motivation

Python is a beautiful language, but production code often becomes cluttered with defensive checks and nested function calls.

1.  **The "None" Paranoia:** We often write 3 lines of code just to check if a variable exists before using it.
2.  **Nested Hell:** Functional transformations often look like `save(validate(parse(read(data))))`, which forces you to read backwards.
3.  **List Comprehension Fatigue:** While powerful, chaining multiple list comprehensions (map/filter/reduce) can quickly become unreadable.

**Purely** solves this with three core tools: `ensure` for assertions, `safe` for null-safe navigation, and `Chain` for fluent pipelines.

## 📦 Installation

**Purely** leverages modern Python features (generics) and requires **Python 3.12+**.

```bash
pip install purely
```

## 🚀 Quick Start

### The Old Way vs. The Purely Way

```python
from purely import ensure, safe, Chain

# ❌ The Old Way: Defensive and Nested
user_data = get_user(123)
if user_data is None:
    raise ValueError("User not found")

city = None
if user_data.address and user_data.address.city:
    city = user_data.address.city.name.upper()

# ✅ The Purely Way: Fluent and Safe
user_data = ensure(get_user(123), "User not found")

# Null-safe navigation + Pipeline
city = safe(user_data).address.city.name | str.upper
```

-----

## 📚 User Guide

### 1. `ensure`: The Rusty Unwrap

Stop writing multiline `if x is None` checks. `ensure` asserts that a value is not `None` and returns it, acting as a type-narrowing barrier.

```python
from purely import ensure

# Throws ValueError("API Key missing") if the value is None
api_key = ensure(os.getenv("API_KEY"), "API Key missing")

# Works transparently with Purely's Option/Safe types
name = ensure(safe(user).name)
```

### 2. `safe`: Null-Safe Navigation

Accessing deeply nested attributes on objects that might be `None` is a common source of `AttributeError`. The `safe` utility wraps your object in a proxy that swallows `None` errors gracefully.

**Key Features:**

  * **Deep Access:** Navigate attributes, items, or methods arbitrarily deep.
  * **IDE Friendly:** Uses type hinting tricks to keep your autocomplete working.
  * **Graceful Exit:** If any link in the chain is `None`, the whole chain returns an `Option(None)`.

<!-- end list -->

```python
from purely import safe, ensure

class User:
    def __init__(self, address=None):
        self.address = address

u = User(address=None)

# ❌ Raises AttributeError
# print(u.address.city)

# ✅ Returns Option(None) - No crash
result = safe(u).address.city

# Use ensure() to crash intentionally if the value MUST be there
city = ensure(result, "City is required")
```

### 3. `Chain`: The Fluent Pipe

`Chain` is a unified wrapper that allows you to pipe values through functions and perform vectorized operations on lists.

#### Simple Pipelines

Use `.then()` or the `|` operator to pass data forward.

```python
from purely import Chain

def double(x): return x * 2

# 5 -> 10 -> "10"
result = Chain(5) | double | str
assert result.unwrap() == "10"
```

#### Vectorized Operations

If the wrapped value is a list (or iterable), `.map()` and `.filter()` apply to **each item** in the list, not the list itself.

```python
users = ["alice", "bob", "charlie"]

names = (
    Chain(users)
    .filter(lambda name: len(name) > 3)  # Filters list: ["alice", "charlie"]
    .map(lambda name: name.upper())      # Maps list: ["ALICE", "CHARLIE"]
    .unwrap()
)
```

#### Error Handling

`Chain` captures exceptions effectively, allowing you to handle errors at the end of the pipeline.

```python
result = (
    Chain(10)
    .then(lambda x: x / 0)        # Fails internally (ZeroDivisionError)
    .then(lambda x: x + 10)       # Skipped
    .catch(lambda e: "Recovered") # Catches error and returns fallback
    .unwrap()
)
assert result == "Recovered"
```

### 4. `Option`: Functional Safety

Under the hood, `safe` uses `Option`. You can use it directly for functional null handling.

  * `.map(func)`: Transforms value only if it exists.
  * `.filter(predicate)`: Turns value to `None` if predicate fails.
  * `.unwrap(default=...)`: Extracts value or returns default.

<!-- end list -->

```python
from purely import Option

val = Option(10).map(lambda x: x * 2).filter(lambda x: x > 50)
assert val.is_none()
```

## 🛠 Contribution

We use `uv` for dependency management and `makefile` for orchestration.

1.  **Clone and Setup:**

    ```bash
    git clone https://github.com/apiad/purely.git
    cd purely
    make format-check  # Verifies environment
    ```

2.  **Testing:**
    We use `pytest` with coverage.

    ```bash
    make test-all
    ```

3.  **Formatting:**
    Ensure your code is formatted with `black`.

    ```bash
    make format
    ```

## 📝 License

Distributed under the MIT License.

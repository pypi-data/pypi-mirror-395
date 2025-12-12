# Purely 💧

**A lightweight elixir for cleaner, safer, and more fluent Python.**

**Purely** is a zero-dependency library designed to bring the best parts of functional programming--safety, pipelines, and immutability--into Python without the academic overhead.

## 📦 Installation

**Purely** requires **Python 3.12+** (due to modern generic syntax).

```
pip install purely
```

## ✨ Features at a Glance

### 1. `ensure`: The Rusty Unwrap

Stop writing multiline `if x is None` checks. Assert existence in one line.

```python
from purely import ensure

# ❌ Old Way
user_id = get_id()
if user_id is None:
    raise ValueError("User ID missing!")

# ✅ The Purely Way
user_id = ensure(get_id(), "User ID missing!")
```

### 2. `Chain`: The Fluent Pipe

Read your code from top-to-bottom, not inside-out. Use the `|` operator to pipe values through functions.

```python
from purely import Chain

def double(x): return x * 2
def shout(x): return f"{x}!"

# ❌ Old Way (Nested Hell)
result = shout(double(5))

# ✅ The Purely Way
result = Chain(5).map(double).map(shout).value

# 🚀 The "Super Duper" Way (Pipe Operator)
result = Chain(5) | double | shout

# Now result == "10!"
```

### 3. `Option`: Type-Safe Null Handling

Handle optional values gracefully. If a value becomes `None` mid-stream, the chain handles it safely instead of crashing.

```python
from purely import Option

result = (
    Option.of(10)
    .map(lambda x: x * 2)       # 20
    .filter(lambda x: x > 100)  # Becomes None (20 is not > 100)
    .map(lambda x: x + 5)       # Skipped (because it's None)
    .unwrap(default=0)          # Returns 0 safely
)
```

## 📚 API Reference

### Core Utilities

|Function|Description|
|---|---|
|`ensure(val, error)`|Returns `val` if not None, otherwise raises `error`.|
|`tap(val, func)`|Runs `func(val)` for side effects (logging, etc) and returns `val` unchanged.|
|`pipe(val, *funcs)`|Pushes `val` through a list of functions in order.|

### `Chain[T]`

_The "Identity Monad" for fluent programming._

- `.map(func)` / `.then(func)`: Transforms the value.
- `| func`: Syntactic sugar for `.map(func)`.
- `.tap(func)`: Run side effects.
- `.ensure(error)`: Crash if the inner value is None.
- `.value`: Access the raw value (property).


### `Option[T]`

_The "Maybe Monad" for safety._

- `.map(func)`: Transforms value only if it exists.
- `.filter(predicate)`: Turns value to `None` if predicate fails.
- `.unwrap(default=..., error=...)`: Extracts value, returns default, or raises error.


## 🤝 Collaboration

We believe in pure code and open collaboration!

1. **Fork** the repository.
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.


Please ensure you write tests for any new features (we use `pytest`).

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

import pytest
from purely import ensure, tap, pipe, Chain, Option


def test_ensure():
    assert ensure("exists") == "exists"
    with pytest.raises(ValueError, match="Custom Error"):
        ensure(None, "Custom Error")


def test_pipe():
    # 5 -> *2 -> +10 -> str
    result = pipe(5, lambda x: x * 2, lambda x: x + 10, str)
    assert result == "20"


def test_chain_fluent():
    res = (
        Chain(5)
        .then(lambda x: x * 2)
        .tap(lambda x: print(f"Debug: {x}"))
        .then(lambda x: x + 5)
    )
    assert res == 15


def test_chain_operator():
    # Testing the | operator
    res = Chain(10) | (lambda x: x / 2) | int
    assert res == 5


def test_option_some():
    opt = Option(10).map(lambda x: x * 2).filter(lambda x: x > 5)
    assert opt.is_some()
    assert opt == 20


def test_option_none():
    opt = Option(10).filter(lambda x: x > 100).map(lambda x: x * 2)
    assert opt.is_none()
    assert opt.unwrap(default=999) == 999

"""Test for setting __tracebackhide__ within an inner scope."""

# pylint: disable=too-few-public-methods, redefined-outer-name


def test_something() -> None:
    """My test."""
    __tracebackhide__ = True
    __tracebackhide__ = lambda x: isinstance(x, str)
    lam = lambda x: x  # [unnecessary-lambda-assignment]
    lam("")


class TestClass:
    """Some tests."""

    def assert_something(self) -> None:
        """My test."""
        __tracebackhide__ = True
        __tracebackhide__ = lambda x: isinstance(x, str)
        var = ""  # [unused-variable]


__tracebackhide__ = True
__tracebackhide__ = lambda x: isinstance(x, str)  # [unnecessary-lambda-assignment]

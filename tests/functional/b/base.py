"""Test to see that the functional test framework works."""
1  # [pointless-statement]
var = lambda x: x  # [unnecessary-lambda-assignment]
var("")


def func():
    """My function."""
    variable = 1  # [unused-variable]

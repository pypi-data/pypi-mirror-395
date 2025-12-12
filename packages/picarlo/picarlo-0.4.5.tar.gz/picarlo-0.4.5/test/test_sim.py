import random

import pytest

from picarlo.sim import (
    Config,
    monte_carlo_pi,
    monte_carlo_pi_parallel,
    stringify_the_float,
)


@pytest.fixture(autouse=True)
def seed_random():
    """
    Seed the random number generator for deterministic testing.
    This fixture runs automatically for every test.
    """
    random.seed(42)


def test_config():
    """
    Test the configuration settings.

    This test verifies that the default number of samples in the configuration
    is set to 10,000,000.
    """
    config = Config()
    assert config.num_samples == 10000


@pytest.mark.parametrize(
    "input, expected",
    [
        (3.14159, "3 dot 14"),
        (122.71828, "122 dot 71"),
        (0.41421, "0 dot 41"),
        (1.0, "1 dot 0"),
        (1, "1 dot 0"),
        (0.1, "0 dot 10"),
        (0.09, "0 dot 9"),
    ],
)
def test_stringify_the_float(input, expected):
    """
    Test the stringify_the_float function.

    Args:
        input (float): The input float value to be stringified.
        expected (str): The expected string representation of the input float.

    Asserts:
        The function asserts that the output of stringify_the_float(input)
        matches the expected string representation.
    """
    assert stringify_the_float(input) == expected


def test_monte_carlo_pi():
    """
    Test the monte_carlo_pi function to ensure it returns a value
    within the expected range for a large number of iterations.

    This test runs the monte_carlo_pi function with 1,000,000 iterations
    and asserts that the result is between 3.1 and 3.2, which is a reasonable
    approximation of the value of Pi.

    Raises:
        AssertionError: If the result is not within the expected range.
    """
    result, _ = monte_carlo_pi(1000000)
    assert 3.1 < result < 3.2


def test_monte_carlo_pi_parallel():
    """
    Test the monte_carlo_pi_parallel function to ensure it returns a value
    within the expected range for a large number of iterations and processes.

    This test runs the monte_carlo_pi_parallel function with 1,000,000 iterations
    and 4 processes, and asserts that the result is between 3.1 and 3.2, which is
    a reasonable approximation of the value of Pi.

    Raises:
        AssertionError: If the result is not within the expected range.
    """
    result, _ = monte_carlo_pi_parallel(250000, 4)
    assert 3.1 < result < 3.2

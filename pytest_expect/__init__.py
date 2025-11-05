"""
pytest-expect: A pytest plugin for soft assertions and multiple expectations.

This plugin allows you to write multiple expectations in a single test,
collecting all failures and reporting them at the end instead of stopping
at the first assertion failure.

Usage:
    def test_example(expect):
        expect.equal(5, 5)
        expect.greater_than(10, 5)
        expect.close(3.14, 3.14159, abs_tol=0.01)
        expect.matches("hello world", r"hello.*")
"""

from .expectations import Expect, ExpectationResult, ExpectationFailure
from .plugin import expect

__version__ = "0.1.0"
__all__ = ["Expect", "ExpectationResult", "ExpectationFailure", "expect"]

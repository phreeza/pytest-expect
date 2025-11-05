"""Tests for the expectations module."""

import re
import pytest


def test_equal_passing(expect):
    """Test that equal expectation passes with matching values."""
    assert expect.equal(5, 5)
    assert expect.equal("hello", "hello")
    assert expect.equal([1, 2, 3], [1, 2, 3])


def test_equal_failing(expect):
    """Test that equal expectation fails with non-matching values."""
    expect.equal(5, 10)
    expect.equal("hello", "world")
    # This test should fail with 2 expectation failures


def test_not_equal(expect):
    """Test not_equal expectations."""
    assert expect.not_equal(5, 10)
    assert expect.not_equal("hello", "world")


def test_greater_than(expect):
    """Test greater_than expectations."""
    assert expect.greater_than(10, 5)
    assert expect.greater_than(100, 50)
    expect.greater_than(5, 10)  # This should fail


def test_less_than(expect):
    """Test less_than expectations."""
    assert expect.less_than(5, 10)
    assert expect.less_than(50, 100)
    expect.less_than(10, 5)  # This should fail


def test_greater_or_equal(expect):
    """Test greater_or_equal expectations."""
    assert expect.greater_or_equal(10, 5)
    assert expect.greater_or_equal(10, 10)
    expect.greater_or_equal(5, 10)  # This should fail


def test_less_or_equal(expect):
    """Test less_or_equal expectations."""
    assert expect.less_or_equal(5, 10)
    assert expect.less_or_equal(10, 10)
    expect.less_or_equal(10, 5)  # This should fail


def test_close(expect):
    """Test close expectations for floating point comparisons."""
    assert expect.close(3.14, 3.14159, abs_tol=0.01)
    assert expect.close(1.0, 1.0000001, rel_tol=1e-6)
    expect.close(3.14, 2.71, abs_tol=0.01)  # This should fail


def test_matches(expect):
    """Test regex matching expectations."""
    assert expect.matches("hello world", r"hello.*")
    assert expect.matches("test123", r"\w+\d+")
    expect.matches("hello", r"^\d+$")  # This should fail


def test_matches_with_compiled_pattern(expect):
    """Test regex matching with compiled pattern."""
    pattern = re.compile(r"hello.*")
    assert expect.matches("hello world", pattern)


def test_contains(expect):
    """Test contains expectations."""
    assert expect.contains([1, 2, 3], 2)
    assert expect.contains("hello world", "world")
    expect.contains([1, 2, 3], 5)  # This should fail


def test_not_contains(expect):
    """Test not_contains expectations."""
    assert expect.not_contains([1, 2, 3], 5)
    assert expect.not_contains("hello", "world")
    expect.not_contains([1, 2, 3], 2)  # This should fail


def test_is_true(expect):
    """Test is_true expectations."""
    assert expect.is_true(True)
    expect.is_true(False)  # This should fail
    expect.is_true(1)  # This should also fail (1 is not True)


def test_is_false(expect):
    """Test is_false expectations."""
    assert expect.is_false(False)
    expect.is_false(True)  # This should fail
    expect.is_false(0)  # This should also fail (0 is not False)


def test_is_none(expect):
    """Test is_none expectations."""
    assert expect.is_none(None)
    expect.is_none(0)  # This should fail


def test_is_not_none(expect):
    """Test is_not_none expectations."""
    assert expect.is_not_none(0)
    assert expect.is_not_none("")
    expect.is_not_none(None)  # This should fail


def test_is_instance(expect):
    """Test is_instance expectations."""
    assert expect.is_instance(5, int)
    assert expect.is_instance("hello", str)
    assert expect.is_instance([1, 2], list)
    expect.is_instance(5, str)  # This should fail


def test_in_range(expect):
    """Test in_range expectations."""
    assert expect.in_range(5, 1, 10)
    assert expect.in_range(1, 1, 10)
    assert expect.in_range(10, 1, 10)
    expect.in_range(15, 1, 10)  # This should fail


def test_has_length(expect):
    """Test has_length expectations."""
    assert expect.has_length([1, 2, 3], 3)
    assert expect.has_length("hello", 5)
    expect.has_length([1, 2], 5)  # This should fail


def test_is_empty(expect):
    """Test is_empty expectations."""
    assert expect.is_empty([])
    assert expect.is_empty("")
    expect.is_empty([1, 2, 3])  # This should fail


def test_is_not_empty(expect):
    """Test is_not_empty expectations."""
    assert expect.is_not_empty([1, 2, 3])
    assert expect.is_not_empty("hello")
    expect.is_not_empty([])  # This should fail


def test_raises(expect):
    """Test raises expectations."""
    def raise_value_error():
        raise ValueError("test error")

    def raise_type_error():
        raise TypeError("test error")

    def no_error():
        pass

    assert expect.raises(ValueError, raise_value_error)
    expect.raises(TypeError, raise_value_error)  # This should fail (wrong exception)
    expect.raises(ValueError, no_error)  # This should fail (no exception)


def test_multiple_expectations_all_pass(expect):
    """Test that multiple passing expectations work correctly."""
    expect.equal(5, 5)
    expect.greater_than(10, 5)
    expect.less_than(5, 10)
    expect.contains([1, 2, 3], 2)
    expect.matches("hello", r"^h")
    # All should pass


def test_multiple_expectations_mixed(expect):
    """Test multiple expectations with some passing and some failing."""
    expect.equal(5, 5)  # Pass
    expect.equal(10, 20)  # Fail
    expect.greater_than(10, 5)  # Pass
    expect.greater_than(5, 10)  # Fail
    expect.is_true(True)  # Pass
    expect.is_true(False)  # Fail
    # Should report 3 failures


def test_custom_message(expect):
    """Test expectations with custom messages."""
    expect.equal(5, 10, msg="Custom error message for equal")
    expect.greater_than(5, 10, msg="Custom error message for greater_than")

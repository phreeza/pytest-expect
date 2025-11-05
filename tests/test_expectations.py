"""Tests for the expectations module."""

import re


def test_equal_passing(expect):
    """Test that equal expectation passes with matching values."""
    assert expect.equal(5, 5)
    assert expect.equal("hello", "hello")
    assert expect.equal([1, 2, 3], [1, 2, 3])


def test_not_equal_passing(expect):
    """Test not_equal expectations."""
    assert expect.not_equal(5, 10)
    assert expect.not_equal("hello", "world")
    assert expect.not_equal([1, 2], [3, 4])


def test_greater_than_passing(expect):
    """Test greater_than expectations."""
    assert expect.greater_than(10, 5)
    assert expect.greater_than(100, 50)
    assert expect.greater_than(-5, -10)


def test_less_than_passing(expect):
    """Test less_than expectations."""
    assert expect.less_than(5, 10)
    assert expect.less_than(50, 100)
    assert expect.less_than(-10, -5)


def test_greater_or_equal_passing(expect):
    """Test greater_or_equal expectations."""
    assert expect.greater_or_equal(10, 5)
    assert expect.greater_or_equal(10, 10)
    assert expect.greater_or_equal(100, 50)


def test_less_or_equal_passing(expect):
    """Test less_or_equal expectations."""
    assert expect.less_or_equal(5, 10)
    assert expect.less_or_equal(10, 10)
    assert expect.less_or_equal(50, 100)


def test_close_passing(expect):
    """Test close expectations for floating point comparisons."""
    assert expect.close(3.14, 3.14159, abs_tol=0.01)
    assert expect.close(1.0, 1.0000001, rel_tol=1e-6)
    assert expect.close(2.5, 2.5)


def test_matches_passing(expect):
    """Test regex matching expectations."""
    assert expect.matches("hello world", r"hello.*")
    assert expect.matches("test123", r"\w+\d+")
    assert expect.matches("email@example.com", r"^\w+@\w+\.\w+$")


def test_matches_with_compiled_pattern(expect):
    """Test regex matching with compiled pattern."""
    pattern = re.compile(r"hello.*")
    assert expect.matches("hello world", pattern)


def test_contains_passing(expect):
    """Test contains expectations."""
    assert expect.contains([1, 2, 3], 2)
    assert expect.contains("hello world", "world")
    assert expect.contains({"a": 1, "b": 2}, "a")


def test_not_contains_passing(expect):
    """Test not_contains expectations."""
    assert expect.not_contains([1, 2, 3], 5)
    assert expect.not_contains("hello", "world")
    assert expect.not_contains({"a": 1}, "b")


def test_is_true_passing(expect):
    """Test is_true expectations."""
    assert expect.is_true(True)
    assert expect.is_true(1 == 1)
    assert expect.is_true(5 > 3)


def test_is_false_passing(expect):
    """Test is_false expectations."""
    assert expect.is_false(False)
    assert expect.is_false(1 == 2)
    assert expect.is_false(5 < 3)


def test_is_none_passing(expect):
    """Test is_none expectations."""
    assert expect.is_none(None)
    value = None
    assert expect.is_none(value)


def test_is_not_none_passing(expect):
    """Test is_not_none expectations."""
    assert expect.is_not_none(0)
    assert expect.is_not_none("")
    assert expect.is_not_none([])
    assert expect.is_not_none(False)


def test_is_instance_passing(expect):
    """Test is_instance expectations."""
    assert expect.is_instance(5, int)
    assert expect.is_instance("hello", str)
    assert expect.is_instance([1, 2], list)
    assert expect.is_instance({"a": 1}, dict)


def test_in_range_passing(expect):
    """Test in_range expectations."""
    assert expect.in_range(5, 1, 10)
    assert expect.in_range(1, 1, 10)
    assert expect.in_range(10, 1, 10)
    assert expect.in_range(0, -5, 5)


def test_has_length_passing(expect):
    """Test has_length expectations."""
    assert expect.has_length([1, 2, 3], 3)
    assert expect.has_length("hello", 5)
    assert expect.has_length({"a": 1, "b": 2}, 2)


def test_is_empty_passing(expect):
    """Test is_empty expectations."""
    assert expect.is_empty([])
    assert expect.is_empty("")
    assert expect.is_empty({})


def test_is_not_empty_passing(expect):
    """Test is_not_empty expectations."""
    assert expect.is_not_empty([1, 2, 3])
    assert expect.is_not_empty("hello")
    assert expect.is_not_empty({"a": 1})


def test_raises_passing(expect):
    """Test raises expectations."""

    def raise_value_error():
        raise ValueError("test error")

    def raise_type_error():
        raise TypeError("test error")

    assert expect.raises(ValueError, raise_value_error)
    assert expect.raises(TypeError, raise_type_error)


def test_multiple_expectations_all_pass(expect):
    """Test that multiple passing expectations work correctly."""
    expect.equal(5, 5)
    expect.greater_than(10, 5)
    expect.less_than(5, 10)
    expect.contains([1, 2, 3], 2)
    expect.matches("hello", r"^h")
    # All should pass


def test_custom_message_passing(expect):
    """Test expectations with custom messages."""
    assert expect.equal(5, 5, msg="Custom success message")
    assert expect.greater_than(10, 5, msg="Ten is greater than five")

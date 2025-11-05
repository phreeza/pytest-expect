"""Tests for the pytest plugin integration."""

import pytest


def test_fixture_available(expect):
    """Test that the expect fixture is available."""
    assert expect is not None


def test_fixture_has_methods(expect):
    """Test that the expect fixture has all expected methods."""
    assert hasattr(expect, 'equal')
    assert hasattr(expect, 'not_equal')
    assert hasattr(expect, 'greater_than')
    assert hasattr(expect, 'less_than')
    assert hasattr(expect, 'close')
    assert hasattr(expect, 'matches')
    assert hasattr(expect, 'contains')
    assert hasattr(expect, 'is_true')
    assert hasattr(expect, 'is_false')
    assert hasattr(expect, 'is_none')
    assert hasattr(expect, 'is_not_none')
    assert hasattr(expect, 'is_instance')
    assert hasattr(expect, 'in_range')
    assert hasattr(expect, 'has_length')
    assert hasattr(expect, 'is_empty')
    assert hasattr(expect, 'is_not_empty')
    assert hasattr(expect, 'raises')


def test_expectation_result_isolation(expect):
    """Test that expectation results are isolated between tests."""
    # This test should have its own clean ExpectationResult
    # If isolation is broken, it might see failures from other tests
    expect.equal(1, 1)
    expect.equal(2, 2)
    # Both should pass, proving this test has a clean slate

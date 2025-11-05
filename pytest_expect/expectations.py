"""Core expectation classes for pytest-expect."""

import re
import math
import traceback
from typing import Any, Optional, Pattern, Union
from dataclasses import dataclass, field


@dataclass
class ExpectationFailure:
    """Represents a single expectation failure."""

    description: str
    expected: Any
    actual: Any
    traceback: str
    line_info: str

    def __str__(self) -> str:
        """Format the failure message."""
        return (
            f"\n{self.line_info}\n"
            f"  {self.description}\n"
            f"  Expected: {self.expected!r}\n"
            f"  Actual:   {self.actual!r}\n"
        )


@dataclass
class ExpectationResult:
    """Holds all expectation results for a test."""

    failures: list[ExpectationFailure] = field(default_factory=list)
    total_expectations: int = 0

    def add_failure(self, failure: ExpectationFailure) -> None:
        """Add a failure to the results."""
        self.failures.append(failure)

    def has_failures(self) -> bool:
        """Check if there are any failures."""
        return len(self.failures) > 0

    def get_summary(self) -> str:
        """Get a summary of the results."""
        if not self.has_failures():
            return f"All {self.total_expectations} expectations passed"

        failure_count = len(self.failures)
        passed_count = self.total_expectations - failure_count

        summary = [
            f"\n{'=' * 70}",
            f"EXPECTATION FAILURES: {failure_count} failed, {passed_count} passed, {self.total_expectations} total",
            f"{'=' * 70}",
        ]

        for i, failure in enumerate(self.failures, 1):
            summary.append(f"\nFailure {i}/{failure_count}:")
            summary.append(str(failure))

        summary.append(f"{'=' * 70}\n")
        return "\n".join(summary)


class Expect:
    """Main expectation class for soft assertions."""

    def __init__(self, result: ExpectationResult):
        """Initialize with an ExpectationResult collector."""
        self._result = result

    def _record_expectation(
        self,
        passed: bool,
        description: str,
        expected: Any,
        actual: Any,
    ) -> bool:
        """Record an expectation result."""
        self._result.total_expectations += 1

        if not passed:
            # Get the caller's stack frame to show where the expectation was called
            stack = traceback.extract_stack()
            # Find the frame that's not in this file
            caller_frame = None
            for frame in reversed(stack[:-1]):  # Exclude current frame
                if 'expectations.py' not in frame.filename:
                    caller_frame = frame
                    break

            if caller_frame:
                line_info = f"File \"{caller_frame.filename}\", line {caller_frame.lineno}, in {caller_frame.name}"
                traceback_str = f"    {caller_frame.line}" if caller_frame.line else ""
            else:
                line_info = "Unknown location"
                traceback_str = ""

            failure = ExpectationFailure(
                description=description,
                expected=expected,
                actual=actual,
                traceback=traceback_str,
                line_info=line_info,
            )
            self._result.add_failure(failure)

        return passed

    def equal(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual equals expected."""
        passed = actual == expected
        description = msg or "Values should be equal"
        return self._record_expectation(passed, description, expected, actual)

    def not_equal(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual does not equal expected."""
        passed = actual != expected
        description = msg or "Values should not be equal"
        return self._record_expectation(passed, description, f"not {expected!r}", actual)

    def greater_than(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is greater than expected."""
        passed = actual > expected
        description = msg or f"Value should be greater than {expected!r}"
        return self._record_expectation(passed, description, f"> {expected!r}", actual)

    def greater_or_equal(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is greater than or equal to expected."""
        passed = actual >= expected
        description = msg or f"Value should be greater than or equal to {expected!r}"
        return self._record_expectation(passed, description, f">= {expected!r}", actual)

    def less_than(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is less than expected."""
        passed = actual < expected
        description = msg or f"Value should be less than {expected!r}"
        return self._record_expectation(passed, description, f"< {expected!r}", actual)

    def less_or_equal(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is less than or equal to expected."""
        passed = actual <= expected
        description = msg or f"Value should be less than or equal to {expected!r}"
        return self._record_expectation(passed, description, f"<= {expected!r}", actual)

    def close(
        self,
        actual: float,
        expected: float,
        rel_tol: float = 1e-9,
        abs_tol: float = 0.0,
        msg: Optional[str] = None,
    ) -> bool:
        """Expect that actual is close to expected (for floating point comparisons)."""
        passed = math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol)
        description = msg or f"Value should be close to {expected!r} (rel_tol={rel_tol}, abs_tol={abs_tol})"
        return self._record_expectation(passed, description, expected, actual)

    def matches(self, actual: str, pattern: Union[str, Pattern], msg: Optional[str] = None) -> bool:
        """Expect that actual matches the regex pattern."""
        if isinstance(pattern, str):
            pattern_obj = re.compile(pattern)
        else:
            pattern_obj = pattern

        passed = pattern_obj.search(actual) is not None
        description = msg or f"String should match pattern {pattern_obj.pattern!r}"
        return self._record_expectation(passed, description, f"match {pattern_obj.pattern!r}", actual)

    def contains(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual contains expected."""
        passed = expected in actual
        description = msg or f"Should contain {expected!r}"
        return self._record_expectation(passed, description, f"contain {expected!r}", actual)

    def not_contains(self, actual: Any, expected: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual does not contain expected."""
        passed = expected not in actual
        description = msg or f"Should not contain {expected!r}"
        return self._record_expectation(passed, description, f"not contain {expected!r}", actual)

    def is_true(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is True."""
        passed = actual is True
        description = msg or "Value should be True"
        return self._record_expectation(passed, description, True, actual)

    def is_false(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is False."""
        passed = actual is False
        description = msg or "Value should be False"
        return self._record_expectation(passed, description, False, actual)

    def is_none(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is None."""
        passed = actual is None
        description = msg or "Value should be None"
        return self._record_expectation(passed, description, None, actual)

    def is_not_none(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is not None."""
        passed = actual is not None
        description = msg or "Value should not be None"
        return self._record_expectation(passed, description, "not None", actual)

    def is_instance(self, actual: Any, expected_type: type, msg: Optional[str] = None) -> bool:
        """Expect that actual is an instance of expected_type."""
        passed = isinstance(actual, expected_type)
        description = msg or f"Value should be instance of {expected_type.__name__}"
        return self._record_expectation(passed, description, expected_type.__name__, type(actual).__name__)

    def in_range(self, actual: Any, min_val: Any, max_val: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is in range [min_val, max_val]."""
        passed = min_val <= actual <= max_val
        description = msg or f"Value should be in range [{min_val!r}, {max_val!r}]"
        return self._record_expectation(passed, description, f"[{min_val!r}, {max_val!r}]", actual)

    def has_length(self, actual: Any, expected_length: int, msg: Optional[str] = None) -> bool:
        """Expect that actual has the expected length."""
        actual_length = len(actual)
        passed = actual_length == expected_length
        description = msg or f"Length should be {expected_length}"
        return self._record_expectation(passed, description, expected_length, actual_length)

    def is_empty(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is empty."""
        passed = len(actual) == 0
        description = msg or "Should be empty"
        return self._record_expectation(passed, description, "empty (length 0)", f"length {len(actual)}")

    def is_not_empty(self, actual: Any, msg: Optional[str] = None) -> bool:
        """Expect that actual is not empty."""
        passed = len(actual) > 0
        description = msg or "Should not be empty"
        return self._record_expectation(passed, description, "not empty (length > 0)", f"length {len(actual)}")

    def raises(self, exception_type: type, callable_obj: callable, *args, **kwargs) -> bool:
        """Expect that calling callable_obj raises the specified exception type."""
        try:
            callable_obj(*args, **kwargs)
            # If we get here, no exception was raised
            return self._record_expectation(
                False,
                f"Should raise {exception_type.__name__}",
                exception_type.__name__,
                "No exception raised"
            )
        except exception_type:
            # Expected exception was raised
            return self._record_expectation(
                True,
                f"Should raise {exception_type.__name__}",
                exception_type.__name__,
                exception_type.__name__
            )
        except Exception as e:
            # Different exception was raised
            return self._record_expectation(
                False,
                f"Should raise {exception_type.__name__}",
                exception_type.__name__,
                f"{type(e).__name__}: {e}"
            )

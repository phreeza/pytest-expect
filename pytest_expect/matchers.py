"""Matcher system for pytest-expect, inspired by gmock matchers."""

import re
from abc import ABC, abstractmethod
from typing import Any, Pattern, Type, Union


class Matcher(ABC):
    """Base class for all matchers."""

    @abstractmethod
    def matches(self, value: Any) -> bool:
        """Check if the value matches the matcher's condition."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Return a description of what this matcher matches."""
        pass

    def describe_mismatch(self, value: Any) -> str:
        """Return a description of why the value didn't match."""
        return f"was {value!r}"


# =============================================================================
# Wildcard Matchers
# =============================================================================


class AnythingMatcher(Matcher):
    """Matches any value."""

    def matches(self, value: Any) -> bool:  # noqa: ARG002
        return True

    def describe(self) -> str:
        return "anything"


class TypeMatcher(Matcher):
    """Matches any value of a specific type (including subclasses)."""

    def __init__(self, expected_type: Type):
        self.expected_type = expected_type

    def matches(self, value: Any) -> bool:
        return isinstance(value, self.expected_type)

    def describe(self) -> str:
        return f"an instance of {self.expected_type.__name__}"

    def describe_mismatch(self, value: Any) -> str:
        return f"was {type(value).__name__}: {value!r}"


class ExactTypeMatcher(Matcher):
    """Matches values of an exact type (subclasses not accepted)."""

    def __init__(self, expected_type: Type):
        self.expected_type = expected_type

    def matches(self, value: Any) -> bool:
        return type(value) == self.expected_type  # noqa: E721 - exact type check required

    def describe(self) -> str:
        return f"exactly type {self.expected_type.__name__}"

    def describe_mismatch(self, value: Any) -> str:
        actual_type = type(value)
        if isinstance(value, self.expected_type):
            return f"was subclass {actual_type.__name__}: {value!r}"
        return f"was {actual_type.__name__}: {value!r}"


# =============================================================================
# Comparison Matchers
# =============================================================================


class EqualToMatcher(Matcher):
    """Matches values equal to the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value == self.expected

    def describe(self) -> str:
        return f"equal to {self.expected!r}"


class NotEqualToMatcher(Matcher):
    """Matches values not equal to the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value != self.expected

    def describe(self) -> str:
        return f"not equal to {self.expected!r}"


class LessThanMatcher(Matcher):
    """Matches values less than the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value < self.expected

    def describe(self) -> str:
        return f"less than {self.expected!r}"


class LessOrEqualMatcher(Matcher):
    """Matches values less than or equal to the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value <= self.expected

    def describe(self) -> str:
        return f"less than or equal to {self.expected!r}"


class GreaterThanMatcher(Matcher):
    """Matches values greater than the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value > self.expected

    def describe(self) -> str:
        return f"greater than {self.expected!r}"


class GreaterOrEqualMatcher(Matcher):
    """Matches values greater than or equal to the expected value."""

    def __init__(self, expected: Any):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return value >= self.expected

    def describe(self) -> str:
        return f"greater than or equal to {self.expected!r}"


class IsNoneMatcher(Matcher):
    """Matches None values."""

    def matches(self, value: Any) -> bool:
        return value is None

    def describe(self) -> str:
        return "None"


class NotNoneMatcher(Matcher):
    """Matches non-None values."""

    def matches(self, value: Any) -> bool:
        return value is not None

    def describe(self) -> str:
        return "not None"


# =============================================================================
# String Matchers
# =============================================================================


class StringEqualMatcher(Matcher):
    """Matches strings equal to the expected string."""

    def __init__(self, expected: str):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and value == self.expected

    def describe(self) -> str:
        return f"string equal to {self.expected!r}"


class StringCaseEqualMatcher(Matcher):
    """Matches strings equal to the expected string (case-insensitive)."""

    def __init__(self, expected: str):
        self.expected = expected

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and value.lower() == self.expected.lower()

    def describe(self) -> str:
        return f"string equal to {self.expected!r} (case-insensitive)"


class HasSubstrMatcher(Matcher):
    """Matches strings containing a substring."""

    def __init__(self, substring: str):
        self.substring = substring

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and self.substring in value

    def describe(self) -> str:
        return f"string containing {self.substring!r}"


class StartsWithMatcher(Matcher):
    """Matches strings starting with a prefix."""

    def __init__(self, prefix: str):
        self.prefix = prefix

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and value.startswith(self.prefix)

    def describe(self) -> str:
        return f"string starting with {self.prefix!r}"


class EndsWithMatcher(Matcher):
    """Matches strings ending with a suffix."""

    def __init__(self, suffix: str):
        self.suffix = suffix

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and value.endswith(self.suffix)

    def describe(self) -> str:
        return f"string ending with {self.suffix!r}"


class MatchesRegexMatcher(Matcher):
    """Matches strings matching a regex pattern (full match)."""

    def __init__(self, pattern: Union[str, Pattern]):
        self.pattern = re.compile(pattern) if isinstance(pattern, str) else pattern

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and self.pattern.match(value) is not None

    def describe(self) -> str:
        return f"string matching regex {self.pattern.pattern!r}"


class ContainsRegexMatcher(Matcher):
    """Matches strings containing a regex pattern (partial match)."""

    def __init__(self, pattern: Union[str, Pattern]):
        self.pattern = re.compile(pattern) if isinstance(pattern, str) else pattern

    def matches(self, value: Any) -> bool:
        return isinstance(value, str) and self.pattern.search(value) is not None

    def describe(self) -> str:
        return f"string containing regex {self.pattern.pattern!r}"


# =============================================================================
# Container Matchers
# =============================================================================


class ContainsMatcher(Matcher):
    """Matches containers that contain a matching element."""

    def __init__(self, matcher: Union[Matcher, Any]):
        self.matcher = _ensure_matcher(matcher)

    def matches(self, value: Any) -> bool:
        try:
            return any(self.matcher.matches(item) for item in value)
        except TypeError:
            return False

    def describe(self) -> str:
        return f"contains element that is {self.matcher.describe()}"


class ElementsAreMatcher(Matcher):
    """Matches containers with exact elements in order."""

    def __init__(self, *matchers: Union[Matcher, Any]):
        self.matchers = [_ensure_matcher(m) for m in matchers]

    def matches(self, value: Any) -> bool:
        try:
            value_list = list(value)
            if len(value_list) != len(self.matchers):
                return False
            return all(m.matches(v) for m, v in zip(self.matchers, value_list))
        except TypeError:
            return False

    def describe(self) -> str:
        descriptions = [m.describe() for m in self.matchers]
        return f"elements are [{', '.join(descriptions)}]"

    def describe_mismatch(self, value: Any) -> str:
        try:
            value_list = list(value)
            if len(value_list) != len(self.matchers):
                return f"has {len(value_list)} elements, expected {len(self.matchers)}"
            mismatches = []
            for i, (m, v) in enumerate(zip(self.matchers, value_list)):
                if not m.matches(v):
                    mismatches.append(f"element {i}: {m.describe_mismatch(v)}")
            return "; ".join(mismatches) if mismatches else "matched"
        except TypeError:
            return f"is not iterable: {value!r}"


class UnorderedElementsAreMatcher(Matcher):
    """Matches containers with exact elements in any order."""

    def __init__(self, *matchers: Union[Matcher, Any]):
        self.matchers = [_ensure_matcher(m) for m in matchers]

    def matches(self, value: Any) -> bool:
        try:
            value_list = list(value)
            if len(value_list) != len(self.matchers):
                return False

            # Try to match each value with a matcher
            used_matchers = [False] * len(self.matchers)
            for v in value_list:
                matched = False
                for i, m in enumerate(self.matchers):
                    if not used_matchers[i] and m.matches(v):
                        used_matchers[i] = True
                        matched = True
                        break
                if not matched:
                    return False
            return True
        except TypeError:
            return False

    def describe(self) -> str:
        descriptions = [m.describe() for m in self.matchers]
        return f"unordered elements are [{', '.join(descriptions)}]"


class IsEmptyMatcher(Matcher):
    """Matches empty containers."""

    def matches(self, value: Any) -> bool:
        try:
            return len(value) == 0
        except TypeError:
            return False

    def describe(self) -> str:
        return "empty"

    def describe_mismatch(self, value: Any) -> str:
        try:
            return f"has {len(value)} elements"
        except TypeError:
            return f"is not a container: {value!r}"


class SizeIsMatcher(Matcher):
    """Matches containers of a specific size."""

    def __init__(self, size_matcher: Union[Matcher, int]):
        if isinstance(size_matcher, int):
            self.size_matcher = EqualToMatcher(size_matcher)
        else:
            self.size_matcher = size_matcher

    def matches(self, value: Any) -> bool:
        try:
            return self.size_matcher.matches(len(value))
        except TypeError:
            return False

    def describe(self) -> str:
        return f"size is {self.size_matcher.describe()}"

    def describe_mismatch(self, value: Any) -> str:
        try:
            return f"has size {len(value)}"
        except TypeError:
            return f"is not a container: {value!r}"


class EachMatcher(Matcher):
    """Matches containers where every element matches the given matcher."""

    def __init__(self, matcher: Union[Matcher, Any]):
        self.matcher = _ensure_matcher(matcher)

    def matches(self, value: Any) -> bool:
        try:
            return all(self.matcher.matches(item) for item in value)
        except TypeError:
            return False

    def describe(self) -> str:
        return f"each element is {self.matcher.describe()}"


# =============================================================================
# Composite Matchers
# =============================================================================


class AllOfMatcher(Matcher):
    """Matches values that match all of the given matchers (AND)."""

    def __init__(self, *matchers: Union[Matcher, Any]):
        self.matchers = [_ensure_matcher(m) for m in matchers]

    def matches(self, value: Any) -> bool:
        return all(m.matches(value) for m in self.matchers)

    def describe(self) -> str:
        descriptions = [m.describe() for m in self.matchers]
        return f"({' AND '.join(descriptions)})"

    def describe_mismatch(self, value: Any) -> str:
        failed = [m.describe() for m in self.matchers if not m.matches(value)]
        return f"failed: {', '.join(failed)}"


class AnyOfMatcher(Matcher):
    """Matches values that match at least one of the given matchers (OR)."""

    def __init__(self, *matchers: Union[Matcher, Any]):
        self.matchers = [_ensure_matcher(m) for m in matchers]

    def matches(self, value: Any) -> bool:
        return any(m.matches(value) for m in self.matchers)

    def describe(self) -> str:
        descriptions = [m.describe() for m in self.matchers]
        return f"({' OR '.join(descriptions)})"


class NotMatcher(Matcher):
    """Matches values that do not match the given matcher."""

    def __init__(self, matcher: Union[Matcher, Any]):
        self.matcher = _ensure_matcher(matcher)

    def matches(self, value: Any) -> bool:
        return not self.matcher.matches(value)

    def describe(self) -> str:
        return f"not ({self.matcher.describe()})"


# =============================================================================
# Field/Property Matchers
# =============================================================================


class FieldMatcher(Matcher):
    """Matches objects with a field/attribute matching a condition."""

    def __init__(self, field_name: str, matcher: Union[Matcher, Any]):
        self.field_name = field_name
        self.matcher = _ensure_matcher(matcher)

    def matches(self, value: Any) -> bool:
        try:
            field_value = getattr(value, self.field_name)
            return self.matcher.matches(field_value)
        except AttributeError:
            return False

    def describe(self) -> str:
        return f"has field '{self.field_name}' that is {self.matcher.describe()}"

    def describe_mismatch(self, value: Any) -> str:
        try:
            field_value = getattr(value, self.field_name)
            return f"field '{self.field_name}' {self.matcher.describe_mismatch(field_value)}"
        except AttributeError:
            return f"has no field '{self.field_name}'"


class PropertyMatcher(Matcher):
    """Matches objects with a property/dict key matching a condition."""

    def __init__(self, key: str, matcher: Union[Matcher, Any]):
        self.key = key
        self.matcher = _ensure_matcher(matcher)

    def matches(self, value: Any) -> bool:
        try:
            prop_value = value[self.key] if isinstance(value, dict) else getattr(value, self.key)
            return self.matcher.matches(prop_value)
        except (KeyError, AttributeError):
            return False

    def describe(self) -> str:
        return f"has property '{self.key}' that is {self.matcher.describe()}"

    def describe_mismatch(self, value: Any) -> str:
        try:
            prop_value = value[self.key] if isinstance(value, dict) else getattr(value, self.key)
            return f"property '{self.key}' {self.matcher.describe_mismatch(prop_value)}"
        except (KeyError, AttributeError):
            return f"has no property '{self.key}'"


# =============================================================================
# Numeric Matchers
# =============================================================================


class CloseMatcher(Matcher):
    """Matches floating point values close to the expected value."""

    def __init__(self, expected: float, rel_tol: float = 1e-9, abs_tol: float = 0.0):
        self.expected = expected
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def matches(self, value: Any) -> bool:
        try:
            import math

            return math.isclose(value, self.expected, rel_tol=self.rel_tol, abs_tol=self.abs_tol)
        except (TypeError, ValueError):
            return False

    def describe(self) -> str:
        return f"close to {self.expected} (rel_tol={self.rel_tol}, abs_tol={self.abs_tol})"


class InRangeMatcher(Matcher):
    """Matches values within a range [min, max]."""

    def __init__(self, min_val: Any, max_val: Any):
        self.min_val = min_val
        self.max_val = max_val

    def matches(self, value: Any) -> bool:
        try:
            return self.min_val <= value <= self.max_val
        except TypeError:
            return False

    def describe(self) -> str:
        return f"in range [{self.min_val}, {self.max_val}]"


# =============================================================================
# Helper Functions
# =============================================================================


def _ensure_matcher(value: Union[Matcher, Any]) -> Matcher:
    """Convert a value to a matcher if it isn't already one."""
    if isinstance(value, Matcher):
        return value
    return EqualToMatcher(value)


# =============================================================================
# Public API Functions
# =============================================================================

# Wildcard
_ = AnythingMatcher()


def A(type_: Type) -> TypeMatcher:
    """Match any value of the given type (including subclasses)."""
    return TypeMatcher(type_)


def An(type_: Type) -> TypeMatcher:
    """Alias for A() - match any value of the given type (including subclasses)."""
    return TypeMatcher(type_)


def ExactType(type_: Type) -> ExactTypeMatcher:
    """Match values of exactly the given type (subclasses not accepted)."""
    return ExactTypeMatcher(type_)


# Comparison
def Eq(value: Any) -> EqualToMatcher:
    """Match values equal to the given value."""
    return EqualToMatcher(value)


def Ne(value: Any) -> NotEqualToMatcher:
    """Match values not equal to the given value."""
    return NotEqualToMatcher(value)


def Lt(value: Any) -> LessThanMatcher:
    """Match values less than the given value."""
    return LessThanMatcher(value)


def Le(value: Any) -> LessOrEqualMatcher:
    """Match values less than or equal to the given value."""
    return LessOrEqualMatcher(value)


def Gt(value: Any) -> GreaterThanMatcher:
    """Match values greater than the given value."""
    return GreaterThanMatcher(value)


def Ge(value: Any) -> GreaterOrEqualMatcher:
    """Match values greater than or equal to the given value."""
    return GreaterOrEqualMatcher(value)


def IsNone() -> IsNoneMatcher:
    """Match None values."""
    return IsNoneMatcher()


def NotNone() -> NotNoneMatcher:
    """Match non-None values."""
    return NotNoneMatcher()


# String
def StrEq(string: str) -> StringEqualMatcher:
    """Match strings equal to the given string."""
    return StringEqualMatcher(string)


def StrCaseEq(string: str) -> StringCaseEqualMatcher:
    """Match strings equal to the given string (case-insensitive)."""
    return StringCaseEqualMatcher(string)


def HasSubstr(substring: str) -> HasSubstrMatcher:
    """Match strings containing the given substring."""
    return HasSubstrMatcher(substring)


def StartsWith(prefix: str) -> StartsWithMatcher:
    """Match strings starting with the given prefix."""
    return StartsWithMatcher(prefix)


def EndsWith(suffix: str) -> EndsWithMatcher:
    """Match strings ending with the given suffix."""
    return EndsWithMatcher(suffix)


def MatchesRegex(pattern: Union[str, Pattern]) -> MatchesRegexMatcher:
    """Match strings matching the given regex pattern (full match)."""
    return MatchesRegexMatcher(pattern)


def ContainsRegex(pattern: Union[str, Pattern]) -> ContainsRegexMatcher:
    """Match strings containing the given regex pattern (partial match)."""
    return ContainsRegexMatcher(pattern)


# Container
def Contains(matcher: Union[Matcher, Any]) -> ContainsMatcher:
    """Match containers that contain an element matching the given matcher."""
    return ContainsMatcher(matcher)


def ElementsAre(*matchers: Union[Matcher, Any]) -> ElementsAreMatcher:
    """Match containers with exact elements in order."""
    return ElementsAreMatcher(*matchers)


def UnorderedElementsAre(*matchers: Union[Matcher, Any]) -> UnorderedElementsAreMatcher:
    """Match containers with exact elements in any order."""
    return UnorderedElementsAreMatcher(*matchers)


def IsEmpty() -> IsEmptyMatcher:
    """Match empty containers."""
    return IsEmptyMatcher()


def SizeIs(size_matcher: Union[Matcher, int]) -> SizeIsMatcher:
    """Match containers of a specific size."""
    return SizeIsMatcher(size_matcher)


def Each(matcher: Union[Matcher, Any]) -> EachMatcher:
    """Match containers where every element matches the given matcher."""
    return EachMatcher(matcher)


# Composite
def AllOf(*matchers: Union[Matcher, Any]) -> AllOfMatcher:
    """Match values that match all of the given matchers (AND)."""
    return AllOfMatcher(*matchers)


def AnyOf(*matchers: Union[Matcher, Any]) -> AnyOfMatcher:
    """Match values that match at least one of the given matchers (OR)."""
    return AnyOfMatcher(*matchers)


def Not(matcher: Union[Matcher, Any]) -> NotMatcher:
    """Match values that do not match the given matcher."""
    return NotMatcher(matcher)


# Field/Property
def Field(field_name: str, matcher: Union[Matcher, Any]) -> FieldMatcher:
    """Match objects with a field/attribute matching a condition."""
    return FieldMatcher(field_name, matcher)


def Property(key: str, matcher: Union[Matcher, Any]) -> PropertyMatcher:
    """Match objects with a property/dict key matching a condition."""
    return PropertyMatcher(key, matcher)


# Numeric
def Close(expected: float, rel_tol: float = 1e-9, abs_tol: float = 0.0) -> CloseMatcher:
    """Match floating point values close to the expected value."""
    return CloseMatcher(expected, rel_tol, abs_tol)


def InRange(min_val: Any, max_val: Any) -> InRangeMatcher:
    """Match values within a range [min, max]."""
    return InRangeMatcher(min_val, max_val)

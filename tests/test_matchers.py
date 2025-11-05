"""Tests for the matcher system."""

from pytest_expect import matchers

# =============================================================================
# Wildcard Matchers
# =============================================================================


def test_anything_matcher(expect):
    """Test that _ matcher matches any value."""
    expect.that(5, matchers._)
    expect.that("hello", matchers._)
    expect.that([1, 2, 3], matchers._)
    expect.that(None, matchers._)


def test_type_matcher(expect):
    """Test A() and An() type matchers."""
    expect.that(5, matchers.A(int))
    expect.that("hello", matchers.An(str))
    expect.that([1, 2], matchers.A(list))
    expect.that({"a": 1}, matchers.A(dict))


def test_type_matcher_with_subclasses(expect):
    """Test that A() and An() accept subclasses."""

    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()
    # A() should match both exact type and subclasses
    expect.that(dog, matchers.A(Dog))
    expect.that(dog, matchers.A(Animal))  # Subclass should match


def test_exact_type_matcher(expect):
    """Test ExactType() for exact type matching."""

    class Animal:
        pass

    class Dog(Animal):
        pass

    dog = Dog()
    animal = Animal()

    # ExactType should only match exact type, not subclasses
    expect.that(dog, matchers.ExactType(Dog))
    expect.that(animal, matchers.ExactType(Animal))

    # Built-in types
    expect.that(5, matchers.ExactType(int))
    expect.that("hello", matchers.ExactType(str))
    expect.that([1, 2], matchers.ExactType(list))


def test_exact_type_vs_subclass_difference(expect):
    """Test the difference between ExactType and A/An with subclasses."""

    class Base:
        pass

    class Derived(Base):
        pass

    derived = Derived()

    # A() accepts subclasses
    expect.that(derived, matchers.A(Base))

    # ExactType() does not - but we can't test failure in passing tests
    # Just verify it works for exact types
    expect.that(derived, matchers.ExactType(Derived))

    # Test with bool (bool is subclass of int in Python)
    expect.that(True, matchers.A(int))  # bool is subclass of int
    expect.that(True, matchers.ExactType(bool))  # Exact type is bool


# =============================================================================
# Comparison Matchers
# =============================================================================


def test_eq_matcher(expect):
    """Test Eq() equality matcher."""
    expect.that(5, matchers.Eq(5))
    expect.that("hello", matchers.Eq("hello"))
    expect.that([1, 2], matchers.Eq([1, 2]))


def test_ne_matcher(expect):
    """Test Ne() not equal matcher."""
    expect.that(5, matchers.Ne(10))
    expect.that("hello", matchers.Ne("world"))


def test_lt_matcher(expect):
    """Test Lt() less than matcher."""
    expect.that(5, matchers.Lt(10))
    expect.that(0, matchers.Lt(1))


def test_le_matcher(expect):
    """Test Le() less or equal matcher."""
    expect.that(5, matchers.Le(10))
    expect.that(10, matchers.Le(10))


def test_gt_matcher(expect):
    """Test Gt() greater than matcher."""
    expect.that(10, matchers.Gt(5))
    expect.that(1, matchers.Gt(0))


def test_ge_matcher(expect):
    """Test Ge() greater or equal matcher."""
    expect.that(10, matchers.Ge(5))
    expect.that(10, matchers.Ge(10))


def test_is_none_matcher(expect):
    """Test IsNone() matcher."""
    expect.that(None, matchers.IsNone())


def test_not_none_matcher(expect):
    """Test NotNone() matcher."""
    expect.that(0, matchers.NotNone())
    expect.that("", matchers.NotNone())
    expect.that([], matchers.NotNone())


# =============================================================================
# String Matchers
# =============================================================================


def test_str_eq_matcher(expect):
    """Test StrEq() string equality matcher."""
    expect.that("hello", matchers.StrEq("hello"))


def test_str_case_eq_matcher(expect):
    """Test StrCaseEq() case-insensitive equality matcher."""
    expect.that("Hello", matchers.StrCaseEq("hello"))
    expect.that("WORLD", matchers.StrCaseEq("world"))


def test_has_substr_matcher(expect):
    """Test HasSubstr() substring matcher."""
    expect.that("hello world", matchers.HasSubstr("world"))
    expect.that("testing", matchers.HasSubstr("est"))


def test_starts_with_matcher(expect):
    """Test StartsWith() prefix matcher."""
    expect.that("hello world", matchers.StartsWith("hello"))
    expect.that("testing", matchers.StartsWith("test"))


def test_ends_with_matcher(expect):
    """Test EndsWith() suffix matcher."""
    expect.that("hello world", matchers.EndsWith("world"))
    expect.that("testing", matchers.EndsWith("ing"))


def test_matches_regex_matcher(expect):
    """Test MatchesRegex() full regex match."""
    expect.that("hello123", matchers.MatchesRegex(r"hello\d+"))
    expect.that("test@example.com", matchers.MatchesRegex(r"^\w+@\w+\.\w+$"))


def test_contains_regex_matcher(expect):
    """Test ContainsRegex() partial regex match."""
    expect.that("hello world 123", matchers.ContainsRegex(r"\d+"))
    expect.that("test email@example.com here", matchers.ContainsRegex(r"\w+@\w+\.\w+"))


# =============================================================================
# Container Matchers
# =============================================================================


def test_contains_matcher(expect):
    """Test Contains() matcher for containers."""
    expect.that([1, 2, 3, 4], matchers.Contains(3))
    expect.that([1, 2, 3, 4], matchers.Contains(matchers.Gt(3)))
    expect.that(["hello", "world"], matchers.Contains(matchers.StartsWith("hel")))


def test_elements_are_matcher(expect):
    """Test ElementsAre() exact order matcher."""
    expect.that([1, 2, 3], matchers.ElementsAre(1, 2, 3))
    expect.that([1, 2, 3], matchers.ElementsAre(matchers.Eq(1), matchers.Eq(2), matchers.Eq(3)))
    expect.that(
        ["hello", "world"],
        matchers.ElementsAre(matchers.StartsWith("h"), matchers.EndsWith("d")),
    )


def test_unordered_elements_are_matcher(expect):
    """Test UnorderedElementsAre() any order matcher."""
    expect.that([3, 1, 2], matchers.UnorderedElementsAre(1, 2, 3))
    expect.that([3, 1, 2], matchers.UnorderedElementsAre(matchers.Gt(0), matchers.Lt(3), 2))


def test_is_empty_matcher(expect):
    """Test IsEmpty() matcher."""
    expect.that([], matchers.IsEmpty())
    expect.that("", matchers.IsEmpty())
    expect.that({}, matchers.IsEmpty())


def test_size_is_matcher(expect):
    """Test SizeIs() matcher."""
    expect.that([1, 2, 3], matchers.SizeIs(3))
    expect.that("hello", matchers.SizeIs(5))
    expect.that([1, 2, 3, 4], matchers.SizeIs(matchers.Gt(3)))


def test_each_matcher(expect):
    """Test Each() matcher for all elements."""
    expect.that([2, 4, 6, 8], matchers.Each(matchers.Gt(0)))
    expect.that(["hello", "world", "test"], matchers.Each(matchers.A(str)))


# =============================================================================
# Composite Matchers
# =============================================================================


def test_all_of_matcher(expect):
    """Test AllOf() AND matcher."""
    expect.that(5, matchers.AllOf(matchers.Gt(0), matchers.Lt(10)))
    expect.that(
        "hello",
        matchers.AllOf(matchers.A(str), matchers.StartsWith("h"), matchers.EndsWith("o")),
    )


def test_any_of_matcher(expect):
    """Test AnyOf() OR matcher."""
    expect.that(5, matchers.AnyOf(matchers.Lt(0), matchers.Gt(3)))
    expect.that("hello", matchers.AnyOf(matchers.Eq("world"), matchers.StartsWith("h")))


def test_not_matcher(expect):
    """Test Not() negation matcher."""
    expect.that(5, matchers.Not(matchers.Eq(10)))
    expect.that("hello", matchers.Not(matchers.StartsWith("w")))
    expect.that([1, 2], matchers.Not(matchers.IsEmpty()))


# =============================================================================
# Field/Property Matchers
# =============================================================================


def test_field_matcher(expect):
    """Test Field() matcher for object attributes."""

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    person = Person("Alice", 30)
    expect.that(person, matchers.Field("name", "Alice"))
    expect.that(person, matchers.Field("age", matchers.Gt(25)))


def test_property_matcher_with_dict(expect):
    """Test Property() matcher with dictionaries."""
    data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    expect.that(data, matchers.Property("name", "Alice"))
    expect.that(data, matchers.Property("age", matchers.InRange(25, 35)))
    expect.that(data, matchers.Property("email", matchers.Contains("@")))


def test_property_matcher_with_object(expect):
    """Test Property() matcher with objects."""

    class User:
        def __init__(self, username, score):
            self.username = username
            self.score = score

    user = User("john_doe", 95)
    expect.that(user, matchers.Property("username", matchers.StartsWith("john")))
    expect.that(user, matchers.Property("score", matchers.Ge(90)))


# =============================================================================
# Numeric Matchers
# =============================================================================


def test_close_matcher(expect):
    """Test Close() floating point matcher."""
    expect.that(3.14159, matchers.Close(3.14, abs_tol=0.01))
    expect.that(1.0, matchers.Close(1.0000001, rel_tol=1e-6))


def test_in_range_matcher(expect):
    """Test InRange() matcher."""
    expect.that(5, matchers.InRange(1, 10))
    expect.that(10, matchers.InRange(10, 20))
    expect.that(0, matchers.InRange(-5, 5))


# =============================================================================
# Complex Nested Matchers
# =============================================================================


def test_nested_container_matchers(expect):
    """Test deeply nested container matchers."""
    data = [[1, 2], [3, 4], [5, 6]]
    expect.that(
        data,
        matchers.ElementsAre(
            matchers.ElementsAre(1, 2),
            matchers.ElementsAre(3, 4),
            matchers.ElementsAre(5, 6),
        ),
    )


def test_complex_composite_matchers(expect):
    """Test complex combinations of composite matchers."""
    # A number that is positive, less than 100, and not 50
    expect.that(42, matchers.AllOf(matchers.Gt(0), matchers.Lt(100), matchers.Not(matchers.Eq(50))))

    # A string that starts with 'h' OR ends with 'd', AND is not empty
    expect.that(
        "hello",
        matchers.AllOf(
            matchers.AnyOf(matchers.StartsWith("h"), matchers.EndsWith("d")),
            matchers.Not(matchers.IsEmpty()),
        ),
    )


def test_mixed_matchers_in_containers(expect):
    """Test mixing different matchers in container checks."""
    users = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35},
    ]

    expect.that(
        users,
        matchers.Contains(
            matchers.AllOf(
                matchers.Property("name", "Bob"), matchers.Property("age", matchers.Lt(30))
            )
        ),
    )

    expect.that(users, matchers.Each(matchers.Property("age", matchers.Gt(20))))


def test_matcher_with_field_and_composite(expect):
    """Test combining field matchers with composite matchers."""

    class Product:
        def __init__(self, name, price, in_stock):
            self.name = name
            self.price = price
            self.in_stock = in_stock

    product = Product("Laptop", 999.99, True)

    expect.that(
        product,
        matchers.AllOf(
            matchers.Field("name", matchers.A(str)),
            matchers.Field("price", matchers.AllOf(matchers.Gt(500), matchers.Lt(2000))),
            matchers.Field("in_stock", True),
        ),
    )


# =============================================================================
# Test matcher descriptions
# =============================================================================


def test_matcher_descriptions():
    """Test that matchers have proper descriptions."""
    assert "anything" in matchers._.describe()
    assert "instance of int" in matchers.A(int).describe()
    assert "equal to 5" in matchers.Eq(5).describe()
    assert "greater than 10" in matchers.Gt(10).describe()
    assert "string containing 'test'" in matchers.HasSubstr("test").describe()
    assert "empty" in matchers.IsEmpty().describe()
    assert "AND" in matchers.AllOf(matchers.Gt(0), matchers.Lt(10)).describe()
    assert "OR" in matchers.AnyOf(matchers.Eq(1), matchers.Eq(2)).describe()

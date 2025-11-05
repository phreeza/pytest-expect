# pytest-expect

A lightweight pytest plugin for multiple expectations and soft assertions. Instead of stopping at the first assertion failure, `pytest-expect` collects all expectation failures in a test and provides a comprehensive report at the end.

## Features

- **Multiple Expectations**: Run multiple assertions in a single test without stopping at the first failure
- **Comprehensive Reporting**: Get a detailed report of all expectation failures at the end of each test
- **Rich Assertion Methods**: Includes helpers for common assertion patterns
- **Clean API**: Simple and intuitive interface that feels natural with pytest
- **Detailed Failure Context**: Each failure shows the exact line, expected vs actual values

## Installation

```bash
pip install pytest-expect
```

## Quick Start

```python
def test_user_validation(expect):
    user = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }

    # All expectations are checked, even if some fail
    expect.equal(user["name"], "John Doe")
    expect.in_range(user["age"], 18, 65)
    expect.matches(user["email"], r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

If any expectations fail, you'll get a detailed report:

```
======================================================================
EXPECTATION FAILURES: 1 failed, 2 passed, 3 total
======================================================================

Failure 1/1:
File "test_example.py", line 8, in test_user_validation
  expect.in_range(user["age"], 18, 65)
  Values should be in range [18, 65]
  Expected: [18, 65]
  Actual:   75

======================================================================
```

## Available Expectation Methods

### Equality and Comparison

- `expect.equal(actual, expected, msg=None)` - Assert equality
- `expect.not_equal(actual, expected, msg=None)` - Assert inequality
- `expect.greater_than(actual, expected, msg=None)` - Assert greater than
- `expect.greater_or_equal(actual, expected, msg=None)` - Assert greater than or equal
- `expect.less_than(actual, expected, msg=None)` - Assert less than
- `expect.less_or_equal(actual, expected, msg=None)` - Assert less than or equal

### Numeric Comparisons

- `expect.close(actual, expected, rel_tol=1e-9, abs_tol=0.0, msg=None)` - Assert floating point values are close
- `expect.in_range(actual, min_val, max_val, msg=None)` - Assert value is within range

### String Matching

- `expect.matches(actual, pattern, msg=None)` - Assert string matches regex pattern
- `expect.contains(actual, expected, msg=None)` - Assert container contains value
- `expect.not_contains(actual, expected, msg=None)` - Assert container doesn't contain value

### Type and Value Checks

- `expect.is_true(actual, msg=None)` - Assert value is True
- `expect.is_false(actual, msg=None)` - Assert value is False
- `expect.is_none(actual, msg=None)` - Assert value is None
- `expect.is_not_none(actual, msg=None)` - Assert value is not None
- `expect.is_instance(actual, expected_type, msg=None)` - Assert instance type

### Collection Checks

- `expect.has_length(actual, expected_length, msg=None)` - Assert collection has specific length
- `expect.is_empty(actual, msg=None)` - Assert collection is empty
- `expect.is_not_empty(actual, msg=None)` - Assert collection is not empty

### Exception Handling

- `expect.raises(exception_type, callable_obj, *args, **kwargs)` - Assert callable raises exception

## Usage Examples

### API Response Validation

```python
def test_api_response(expect):
    response = {
        "status": "success",
        "code": 200,
        "data": {"id": 123, "name": "Test"}
    }

    expect.equal(response["status"], "success")
    expect.equal(response["code"], 200)
    expect.is_not_none(response["data"])
    expect.is_instance(response["data"]["id"], int)
```

### Form Validation

```python
def test_form_validation(expect):
    form_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 25,
        "terms_accepted": True
    }

    expect.matches(form_data["username"], r"^[a-z_]+$")
    expect.matches(form_data["email"], r"^[\w\.-]+@[\w\.-]+\.\w+$")
    expect.in_range(form_data["age"], 18, 100)
    expect.is_true(form_data["terms_accepted"])
```

### Data Processing

```python
def test_data_processing(expect):
    numbers = [1, 2, 3, 4, 5]

    expect.has_length(numbers, 5)
    expect.is_not_empty(numbers)
    expect.contains(numbers, 3)
    expect.equal(sum(numbers), 15)
    expect.greater_than(max(numbers), 0)
```

### With Custom Messages

```python
def test_with_custom_messages(expect):
    value = 42

    expect.greater_than(
        value,
        50,
        msg="Value should be greater than 50 for premium users"
    )
```

## Matchers

pytest-expect includes a powerful matcher system inspired by Google Mock (gmock), allowing you to compose complex expectations in a readable way.

### Using Matchers

Use `expect.that(value, matcher)` with any matcher:

```python
from pytest_expect import matchers

def test_with_matchers(expect):
    # Simple matchers
    expect.that(42, matchers.Gt(40))
    expect.that("hello", matchers.StartsWith("hel"))

    # Composite matchers
    expect.that(
        5,
        matchers.AllOf(matchers.Gt(0), matchers.Lt(10))
    )

    # Container matchers
    expect.that(
        [1, 2, 3, 4, 5],
        matchers.Each(matchers.Gt(0))
    )
```

### Matcher Categories

#### Wildcard Matchers
- `matchers._` - Matches any value
- `matchers.A(type)` / `matchers.An(type)` - Matches any value of the given type **or subclass**
- `matchers.ExactType(type)` - Matches only exact type (subclasses not accepted)

```python
expect.that(42, matchers._)  # Always passes
expect.that("hello", matchers.A(str))
expect.that([1, 2], matchers.An(list))

# Type matching with subclasses
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()
expect.that(dog, matchers.A(Animal))  # ✓ Passes - Dog is subclass of Animal
expect.that(dog, matchers.ExactType(Dog))  # ✓ Passes - exact type match
# expect.that(dog, matchers.ExactType(Animal))  # ✗ Would fail - not exact type

# Note: In Python, bool is a subclass of int
expect.that(True, matchers.A(int))  # ✓ Passes
expect.that(True, matchers.ExactType(bool))  # ✓ Passes
# expect.that(True, matchers.ExactType(int))  # ✗ Would fail
```

#### Comparison Matchers
- `matchers.Eq(value)` - Equal to
- `matchers.Ne(value)` - Not equal to
- `matchers.Lt(value)` - Less than
- `matchers.Le(value)` - Less than or equal
- `matchers.Gt(value)` - Greater than
- `matchers.Ge(value)` - Greater than or equal
- `matchers.IsNone()` - Is None
- `matchers.NotNone()` - Is not None

```python
expect.that(5, matchers.Gt(3))
expect.that(10, matchers.Le(10))
expect.that(None, matchers.IsNone())
```

#### String Matchers
- `matchers.StrEq(string)` - String equality
- `matchers.StrCaseEq(string)` - Case-insensitive equality
- `matchers.HasSubstr(substring)` - Contains substring
- `matchers.StartsWith(prefix)` - Starts with prefix
- `matchers.EndsWith(suffix)` - Ends with suffix
- `matchers.MatchesRegex(pattern)` - Full regex match
- `matchers.ContainsRegex(pattern)` - Partial regex match

```python
expect.that("Hello World", matchers.StrCaseEq("hello world"))
expect.that("test@example.com", matchers.ContainsRegex(r"\w+@\w+"))
expect.that("filename.txt", matchers.EndsWith(".txt"))
```

#### Container Matchers
- `matchers.Contains(matcher)` - Has element matching matcher
- `matchers.ElementsAre(*matchers)` - Exact elements in order
- `matchers.UnorderedElementsAre(*matchers)` - Exact elements, any order
- `matchers.IsEmpty()` - Empty container
- `matchers.SizeIs(size_or_matcher)` - Specific size
- `matchers.Each(matcher)` - All elements match

```python
expect.that([1, 2, 3], matchers.Contains(matchers.Gt(2)))
expect.that([1, 2, 3], matchers.ElementsAre(1, 2, 3))
expect.that([3, 1, 2], matchers.UnorderedElementsAre(1, 2, 3))
expect.that([2, 4, 6], matchers.Each(matchers.Gt(0)))
expect.that([1, 2, 3], matchers.SizeIs(matchers.Gt(2)))
```

#### Composite Matchers
- `matchers.AllOf(*matchers)` - All matchers must match (AND)
- `matchers.AnyOf(*matchers)` - At least one matcher matches (OR)
- `matchers.Not(matcher)` - Negates a matcher

```python
# Value between 0 and 100
expect.that(42, matchers.AllOf(matchers.Gt(0), matchers.Lt(100)))

# Either negative or greater than 100
expect.that(-5, matchers.AnyOf(matchers.Lt(0), matchers.Gt(100)))

# Not equal to 42
expect.that(43, matchers.Not(matchers.Eq(42)))
```

#### Field/Property Matchers
- `matchers.Field(name, matcher)` - Object attribute matches
- `matchers.Property(key, matcher)` - Dict key or property matches

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 30)
expect.that(user, matchers.Field("name", "Alice"))
expect.that(user, matchers.Field("age", matchers.Gt(25)))

data = {"status": "success", "code": 200}
expect.that(data, matchers.Property("code", matchers.Eq(200)))
```

#### Numeric Matchers
- `matchers.Close(value, rel_tol=1e-9, abs_tol=0.0)` - Floating point comparison
- `matchers.InRange(min, max)` - Value in range

```python
expect.that(3.14159, matchers.Close(3.14, abs_tol=0.01))
expect.that(5, matchers.InRange(1, 10))
```

### Complex Matcher Examples

```python
def test_complex_data_validation(expect):
    """Validate complex nested data structures."""
    users = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "Bob", "age": 25, "email": "bob@example.com"},
    ]

    # Check that users list contains a user named Bob who is under 30
    expect.that(
        users,
        matchers.Contains(
            matchers.AllOf(
                matchers.Property("name", "Bob"),
                matchers.Property("age", matchers.Lt(30))
            )
        )
    )

    # All users have valid email addresses
    expect.that(
        users,
        matchers.Each(
            matchers.Property("email", matchers.ContainsRegex(r"\w+@\w+\.\w+"))
        )
    )

    # Nested list validation
    matrix = [[1, 2], [3, 4], [5, 6]]
    expect.that(
        matrix,
        matchers.ElementsAre(
            matchers.ElementsAre(1, 2),
            matchers.ElementsAre(3, 4),
            matchers.ElementsAre(5, 6),
        )
    )
```

## Why pytest-expect?

Traditional pytest assertions stop at the first failure:

```python
def test_traditional():
    assert value1 == expected1  # Fails here
    assert value2 == expected2  # Never executed
    assert value3 == expected3  # Never executed
```

With pytest-expect, all expectations are checked:

```python
def test_with_expect(expect):
    expect.equal(value1, expected1)  # Checked
    expect.equal(value2, expected2)  # Checked
    expect.equal(value3, expected3)  # Checked
    # All failures reported together
```

This is especially useful for:
- **Data validation**: Check multiple fields at once
- **API testing**: Validate entire response structures
- **Form validation**: Test all validation rules together
- **Complex objects**: Verify multiple properties in one test

## How It Works

The `expect` fixture is provided by the pytest plugin. It collects all expectation results during test execution and reports failures at the end. Each expectation returns a boolean indicating success, but doesn't raise an exception, allowing the test to continue.

## Development

### Running Tests

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Run with coverage
pytest --cov=pytest_expect --cov-report=html
```

### Code Quality

```bash
# Format code
black pytest_expect tests

# Type checking
mypy pytest_expect

# Linting
flake8 pytest_expect tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/pytest-expect/issues) on GitHub.

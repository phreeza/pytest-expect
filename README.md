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

## Changelog

### 0.1.0 (Initial Release)
- Initial release with core expectation methods
- Support for equality, comparison, and type checks
- String matching and regex support
- Collection validation helpers
- Exception testing support
- Comprehensive failure reporting

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/pytest-expect/issues) on GitHub.

"""Example tests demonstrating pytest-expect usage."""


def test_user_data_validation(expect):
    """Example: Validate multiple aspects of user data."""
    user = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "is_active": True,
        "roles": ["user", "admin"]
    }

    # Check multiple properties without stopping at first failure
    expect.equal(user["name"], "John Doe")
    expect.in_range(user["age"], 18, 65)
    expect.matches(user["email"], r"^[\w\.-]+@[\w\.-]+\.\w+$")
    expect.is_true(user["is_active"])
    expect.contains(user["roles"], "admin")
    expect.has_length(user["roles"], 2)


def test_api_response_validation(expect):
    """Example: Validate multiple fields in an API response."""
    response = {
        "status": "success",
        "code": 200,
        "data": {
            "id": 123,
            "name": "Test Item",
            "price": 19.99
        },
        "timestamp": 1234567890
    }

    expect.equal(response["status"], "success")
    expect.equal(response["code"], 200)
    expect.is_not_none(response["data"])
    expect.is_instance(response["data"]["id"], int)
    expect.greater_than(response["data"]["price"], 0)
    expect.is_instance(response["timestamp"], int)


def test_calculation_results(expect):
    """Example: Validate multiple calculation results."""
    # Simulate some calculations
    result1 = 2 + 2
    result2 = 10 / 3
    result3 = 5 * 6
    result4 = 100 - 25

    # Check all results
    expect.equal(result1, 4)
    expect.close(result2, 3.333, abs_tol=0.001)
    expect.equal(result3, 30)
    expect.equal(result4, 75)
    expect.greater_than(result1 + result3, 30)


def test_list_operations(expect):
    """Example: Validate multiple list operations."""
    numbers = [1, 2, 3, 4, 5]

    expect.has_length(numbers, 5)
    expect.contains(numbers, 3)
    expect.not_contains(numbers, 10)
    expect.equal(numbers[0], 1)
    expect.equal(numbers[-1], 5)
    expect.greater_than(sum(numbers), 10)
    expect.is_not_empty(numbers)


def test_string_validations(expect):
    """Example: Validate multiple string properties."""
    text = "Hello, World! 123"

    expect.contains(text, "World")
    expect.matches(text, r"Hello.*")
    expect.matches(text, r"\d+")
    expect.has_length(text, 17)
    expect.is_not_empty(text)
    expect.is_instance(text, str)


def test_with_intentional_failures(expect):
    """Example: Test with some intentional failures to show reporting."""
    expect.equal(2 + 2, 4)  # Pass
    expect.equal(3 + 3, 7)  # Fail - should be 6
    expect.greater_than(10, 5)  # Pass
    expect.greater_than(5, 10)  # Fail
    expect.is_true(True)  # Pass
    expect.is_false(True)  # Fail
    # This test will show: 3 failed, 3 passed, 6 total

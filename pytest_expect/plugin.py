"""Pytest plugin hooks for pytest-expect."""

import pytest
from .expectations import Expect, ExpectationResult


class ExpectationPlugin:
    """Pytest plugin for expectation-based testing."""

    def __init__(self):
        self.results = {}

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        """Set up expectation result collector for each test."""
        self.results[item.nodeid] = ExpectationResult()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Check for expectation failures after test execution."""
        outcome = yield
        report = outcome.get_result()

        # Only check expectations during the call phase (not setup or teardown)
        if call.when == "call" and item.nodeid in self.results:
            result = self.results[item.nodeid]

            if result.has_failures():
                # Mark the test as failed
                report.outcome = "failed"

                # Add our custom failure message
                summary = result.get_summary()

                if report.longrepr is None:
                    report.longrepr = summary
                else:
                    # Append to existing failure message
                    report.longrepr = f"{report.longrepr}\n\n{summary}"

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_teardown(self, item):
        """Clean up expectation results after test."""
        if item.nodeid in self.results:
            del self.results[item.nodeid]


# Global plugin instance
_plugin = ExpectationPlugin()


@pytest.fixture
def expect(request):
    """
    Fixture that provides the Expect object for soft assertions.

    Example:
        def test_example(expect):
            expect.equal(5, 5)
            expect.greater_than(10, 5)
            expect.close(3.14, 3.14159, abs_tol=0.01)
    """
    result = _plugin.results.get(request.node.nodeid)
    if result is None:
        # Fallback in case the plugin wasn't properly initialized
        result = ExpectationResult()
        _plugin.results[request.node.nodeid] = result

    return Expect(result)


def pytest_configure(config):
    """Register the plugin with pytest."""
    config.pluginmanager.register(_plugin, "expectation_plugin")


def pytest_unconfigure(config):
    """Unregister the plugin."""
    config.pluginmanager.unregister(_plugin)

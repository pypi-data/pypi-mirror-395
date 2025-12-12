"""
Pytest configuration for msgtrace SDK tests.
"""


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "asyncio: mark test as async")

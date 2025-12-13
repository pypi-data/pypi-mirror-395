"""
Test setup file.

This file is regenerated on each run - do not edit directly.
For custom setup, create tests/conftest.py and add your fixtures there.
"""

import pytest
import asyncio


@pytest.fixture(scope='session')
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# TODO: Add global fixtures
# Example:
# @pytest.fixture(scope='session')
# def api_client():
#     """Create API client for tests."""
#     # Setup code
#     yield client
#     # Teardown code

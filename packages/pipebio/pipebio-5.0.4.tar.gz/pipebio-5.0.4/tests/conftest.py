import os
import pytest

@pytest.fixture(scope="session")
def mock_api_response():
    """Fixture for mocked API responses in unit tests."""
    return {
        "status": "success",
        "data": {
            "id": "test-id",
            "name": "test-name"
        }
    } 
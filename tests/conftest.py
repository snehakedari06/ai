import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """
    Provides a FastAPI TestClient fixture for integration testing of routes.
    """
    with TestClient(app) as c:
        yield c

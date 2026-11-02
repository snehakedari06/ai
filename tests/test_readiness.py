from app.inference.base import BaseModel
from app.inference.loader import set_model, initialize_model

class MockNotReadyModel(BaseModel):
    """Mock model representation that is not ready."""
    def load(self) -> None:
        pass
    def predict(self, text: str, options: dict) -> dict:
        return {}
    @property
    def is_ready(self) -> bool:
        return False

def test_readiness_endpoint_ready(client):
    """
    Test that GET /ready returns 200 and {"status": "ready"} when the service is fully ready.
    """
    initialize_model()
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_readiness_endpoint_not_ready(client):
    """
    Test that GET /ready returns 200 and {"status": "not_ready"} when the model is not ready.
    """
    set_model(MockNotReadyModel())
    try:
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "not_ready"}
    finally:
        # Restore original model
        initialize_model()


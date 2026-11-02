import pytest
from app.inference.base import BaseModel
from app.inference.loader import set_model, initialize_model

class MockNotReadyModel(BaseModel):
    """
    Mock model subclass that is explicitly marked as not ready.
    """
    def load(self) -> None:
        pass
    def predict(self, text: str, options: dict) -> dict:
        return {}
    @property
    def is_ready(self) -> bool:
        return False

def test_inference_success(client):
    """
    Test that valid POST /api/v1/inference returns status 200 and standard inference schema.
    """
    # Force default model configuration loader to initialize
    initialize_model()
    
    payload = {
        "input": "Where is the authentication middleware?",
        "options": {"temperature": 0.0}
    }
    response = client.post("/api/v1/inference", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "result" in data
    assert "metadata" in data
    assert data["metadata"]["model"] == "dummy-model"
    assert "latency_ms" in data["metadata"]

def test_inference_validation_error(client):
    """
    Test that invalid input (e.g. empty string) returns status 422 validation error.
    """
    payload = {
        "input": ""  # empty input fails validation min_length constraint
    }
    response = client.post("/api/v1/inference", json=payload)
    assert response.status_code == 422

def test_inference_model_unavailable(client):
    """
    Test that POST /api/v1/inference returns 503 and error payload when active model is not ready.
    """
    # Swap active model with mock not-ready model
    set_model(MockNotReadyModel())
    
    try:
        # Check /ready reports status "not_ready"
        response_ready = client.get("/ready")
        assert response_ready.status_code == 200
        assert response_ready.json() == {"status": "not_ready"}

        # Check /inference returns 503 Service Unavailable
        response_inf = client.post("/api/v1/inference", json={"input": "Hello"})
        assert response_inf.status_code == 503
        
        data = response_inf.json()
        assert "error" in data
        assert data["error"]["code"] == "MODEL_UNAVAILABLE"
        assert "message" in data["error"]
    finally:
        # Restore the original model
        initialize_model()

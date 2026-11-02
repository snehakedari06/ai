def test_health_endpoint(client):
    """
    Test that GET /health returns status 200 and {"status": "ok"}
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

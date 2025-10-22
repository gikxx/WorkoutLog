from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rfc7807_format_validation_error():
    response = client.post("/exercises/", json={"name": "", "workout_id": 0})

    assert response.status_code == 422
    data = response.json()
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "correlation_id" in data


def test_rfc7807_format_not_found():
    response = client.get("/workouts/9999")

    assert response.status_code == 404
    data = response.json()
    assert data["type"] == "about:blank"
    assert data["title"] == "Error"
    assert data["status"] == 404
    assert "correlation_id" in data


def test_no_stack_trace_in_response():
    response = client.get("/nonexistent-endpoint")

    if response.status_code >= 400:
        data = response.json()
        assert "traceback" not in str(data)
        assert "File" not in str(data)
        assert "line" not in str(data)

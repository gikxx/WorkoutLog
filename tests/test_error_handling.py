from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_rfc7807_format_validation_error():
    response = client.post("/exercises/", json={"name": "", "workout_id": 1})
    assert response.status_code == 422
    data = response.json()
    assert "correlation_id" in data
    assert data["type"] == "about:blank"


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_rfc7807_format_not_found():
    response = client.get("/workouts/9999")
    assert response.status_code == 404
    data = response.json()
    assert "correlation_id" in data
    assert data["title"] == "Workout Not Found"


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_no_stack_trace_in_response():
    response = client.get("/nonexistent-endpoint")
    if response.status_code >= 400:
        data = response.json()
        assert "traceback" not in str(data)
        assert "File" not in str(data)

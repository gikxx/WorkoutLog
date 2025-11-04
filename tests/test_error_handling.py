from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


def mock_get_db():
    return MagicMock()


app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
def test_rfc7807_format_validation_error(MockExerciseService):
    mock_service = MagicMock()
    MockExerciseService.return_value = mock_service

    response = client.post("/exercises/", json={"name": "", "workout_id": 1})
    assert response.status_code == 422
    data = response.json()
    assert "correlation_id" in data
    assert data["type"] == "about:blank"


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_rfc7807_format_not_found(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.get_workout_by_id.return_value = None
    MockWorkoutService.return_value = mock_service

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

# test_workouts.py
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


def mock_get_db():
    return MagicMock()


# ОБНОВЛЕННЫЕ мок-данные - добавляем поле 'date'
MOCK_WORKOUT = {
    "id": 1,
    "note": "Test workout",
    "owner_id": 1,
    "date": "2024-01-01",  # ДОБАВЛЕНО поле date
    "created_at": "2024-01-01T00:00:00",
}

MOCK_WORKOUTS = [MOCK_WORKOUT]

app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_get_workouts(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.get_workouts.return_value = MOCK_WORKOUTS
    MockWorkoutService.return_value = mock_service

    response = client.get("/workouts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == 1
    assert "date" in response.json()[0]  # проверяем наличие поля


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_create_workout(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.create_workout.return_value = MOCK_WORKOUT
    MockWorkoutService.return_value = mock_service

    response = client.post("/workouts/", json={"note": "Test workout"})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "date" in response.json()


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_get_workout_detail(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.get_workout_by_id.return_value = MOCK_WORKOUT
    MockWorkoutService.return_value = mock_service

    response = client.get("/workouts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "date" in response.json()


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_get_workout_not_found(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.get_workout_by_id.return_value = None
    MockWorkoutService.return_value = mock_service

    response = client.get("/workouts/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["title"].lower()

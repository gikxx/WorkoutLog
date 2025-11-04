from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


def mock_get_db():
    return MagicMock()


MOCK_EXERCISE = {"id": 1, "name": "Жим лежа", "workout_id": 1}

MOCK_EXERCISES = [MOCK_EXERCISE]

app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
def test_create_exercise(MockExerciseService):
    mock_service = MagicMock()
    mock_service.create_exercise.return_value = MOCK_EXERCISE
    MockExerciseService.return_value = mock_service

    response = client.post("/exercises/", json={"name": "Жим лежа", "workout_id": 1})
    assert response.status_code == 200
    assert response.json()["name"] == "Жим лежа"


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
def test_get_exercises(MockExerciseService):
    mock_service = MagicMock()
    mock_service.get_exercises.return_value = MOCK_EXERCISES
    MockExerciseService.return_value = mock_service

    response = client.get("/exercises/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Жим лежа"

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_create_exercise():
    # Сначала создаем workout
    workout_response = client.post(
        "/workouts/", json={"note": "Test workout for exercise"}
    )
    print("Workout response:", workout_response.status_code, workout_response.json())
    workout_id = workout_response.json()["id"]

    # Теперь создаем exercise
    response = client.post(
        "/exercises/", json={"name": "Жим лежа", "workout_id": workout_id}
    )
    print("Exercise response:", response.status_code, response.json())  # ДОБАВИМ ПРИНТ
    assert response.status_code == 200
    assert response.json()["name"] == "Жим лежа"


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_get_exercises():
    response = client.get("/exercises/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

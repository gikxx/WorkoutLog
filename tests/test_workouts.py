from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_current_user():
    return 1


app.dependency_overrides = {}


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_get_workouts():
    response = client.post("/workouts/", json={"note": "Test workout in English"})
    assert response.status_code == 200

    response = client.get("/workouts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_create_workout():
    response = client.post("/workouts/", json={"note": "Test workout"})
    assert response.status_code == 200
    assert "id" in response.json()


@patch("app.api.dependencies.get_current_user", mock_get_current_user)
def test_get_workout_detail():
    response = client.post("/workouts/", json={"note": "Test workout for detail"})
    workout_id = response.json()["id"]

    response = client.get(f"/workouts/{workout_id}")
    assert response.status_code == 200
    assert response.json()["id"] == workout_id

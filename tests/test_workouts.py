from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_workouts():
    response = client.get("/workouts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_workout():
    response = client.post("/workouts/", json={"note": "Test workout"})
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_workout_detail():
    response = client.get("/workouts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

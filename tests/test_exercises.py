from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_exercise():
    response = client.post("/exercises/", json={"name": "Жим лежа", "workout_id": 1})
    assert response.status_code == 200
    assert response.json()["name"] == "Жим лежа"


def test_get_exercises():
    response = client.get("/exercises/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

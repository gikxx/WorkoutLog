from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_stats():
    response = client.get("/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_workouts" in data
    assert "total_exercises" in data
    assert "last_workout_date" in data

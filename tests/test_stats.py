from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_db():
    return MagicMock()


@patch("app.api.endpoints.stats.get_db", mock_get_db)
@patch("app.api.endpoints.stats.StatsService")
def test_get_stats(MockStatsService):
    mock_service = MagicMock()
    mock_service.get_stats.return_value = {
        "total_workouts": 5,
        "total_exercises": 15,
        "last_workout_date": "2024-01-01",
    }
    MockStatsService.return_value = mock_service

    response = client.get("/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_workouts" in data
    assert "total_exercises" in data
    assert "last_workout_date" in data

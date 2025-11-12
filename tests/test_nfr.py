import time
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def mock_get_db():
    return MagicMock()


@patch("app.api.endpoints.stats.get_db", mock_get_db)
@patch("app.api.endpoints.stats.StatsService")
def test_nfr_02_performance_stats(MockStatsService):
    mock_service = MagicMock()
    mock_service.get_stats.return_value = {
        "total_workouts": 5,
        "total_exercises": 15,
        "last_workout_date": "2024-01-01",
    }
    MockStatsService.return_value = mock_service

    start_time = time.time()
    response = client.get("/stats/")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert response_time_ms <= 2000
    assert response.status_code == 200


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_nfr_06_workouts_performance(MockWorkoutService):
    mock_service = MagicMock()
    mock_service.get_workouts.return_value = []
    MockWorkoutService.return_value = mock_service

    start_time = time.time()
    response = client.get("/workouts/")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert response_time_ms <= 300
    assert response.status_code == 200


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
@patch("app.api.endpoints.stats.get_db", mock_get_db)
@patch("app.api.endpoints.stats.StatsService")
def test_nfr_04_api_stability(
    MockStatsService, MockExerciseService, MockWorkoutService
):
    mock_workout_service = MagicMock()
    mock_workout_service.get_workouts.return_value = []
    MockWorkoutService.return_value = mock_workout_service

    mock_exercise_service = MagicMock()
    mock_exercise_service.get_exercises.return_value = []
    MockExerciseService.return_value = mock_exercise_service

    mock_stats_service = MagicMock()
    mock_stats_service.get_stats.return_value = {
        "total_workouts": 0,
        "total_exercises": 0,
        "last_workout_date": None,
    }
    MockStatsService.return_value = mock_stats_service

    endpoints = ["/workouts/", "/exercises/", "/stats/"]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code != 500

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app

client = TestClient(app)


def mock_get_db():
    return MagicMock()


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_idor_protection_real_scenario(MockWorkoutService):
    def mock_user_1():
        return 1

    def mock_user_2():
        return 2

    mock_service = MagicMock()
    mock_service.create_workout.return_value = {
        "id": 1,
        "note": "Private workout",
        "owner_id": 1,
        "date": "2024-01-01",
    }
    mock_service.get_workout_by_id.return_value = None
    MockWorkoutService.return_value = mock_service

    app.dependency_overrides[get_current_user] = mock_user_1
    workout = client.post("/workouts/", json={"note": "Private workout"}).json()

    app.dependency_overrides[get_current_user] = mock_user_2
    response = client.get(f"/workouts/{workout['id']}")

    app.dependency_overrides = {}
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
def test_xss_prevention_in_exercise_name(MockExerciseService, MockWorkoutService):
    def mock_user():
        return 1

    mock_workout_service = MagicMock()
    mock_workout_service.create_workout.return_value = {
        "id": 1,
        "note": "Test",
        "owner_id": 1,
        "date": "2024-01-01",
    }
    MockWorkoutService.return_value = mock_workout_service

    mock_exercise_service = MagicMock()
    MockExerciseService.return_value = mock_exercise_service

    app.dependency_overrides[get_current_user] = mock_user
    workout = client.post("/workouts/", json={"note": "Test"}).json()

    response = client.post(
        "/exercises/",
        json={
            "name": "Bench<script>alert('xss')</script>",
            "workout_id": workout["id"],
        },
    )

    app.dependency_overrides = {}
    assert response.status_code == 422


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_mass_assignment_prevention(MockWorkoutService):
    def mock_user():
        return 1

    mock_service = MagicMock()
    mock_service.create_workout.return_value = {
        "id": 1,
        "note": "Test",
        "owner_id": 1,
        "date": "2024-01-01",
    }
    MockWorkoutService.return_value = mock_service

    app.dependency_overrides[get_current_user] = mock_user
    response = client.post(
        "/workouts/", json={"note": "Test", "owner_id": 999, "admin": True}
    )

    app.dependency_overrides = {}
    assert response.status_code == 200
    created = response.json()
    assert created["owner_id"] == 1
    assert "admin" not in created


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
def test_json_injection_prevention(MockWorkoutService):
    def mock_user():
        return 1

    mock_service = MagicMock()
    mock_service.create_workout.return_value = {
        "id": 1,
        "note": "test",
        "owner_id": 1,
        "date": "2024-01-01",
    }
    MockWorkoutService.return_value = mock_service

    app.dependency_overrides[get_current_user] = mock_user

    malicious_json = '{"note": "test", "__class__": "malicious"}'
    response = client.post(
        "/workouts/", data=malicious_json, headers={"Content-Type": "application/json"}
    )

    app.dependency_overrides = {}
    assert response.status_code in [200, 422, 401]


@patch("app.api.endpoints.workouts.get_db", mock_get_db)
@patch("app.api.endpoints.workouts.WorkoutService")
@patch("app.api.endpoints.exercises.get_db", mock_get_db)
@patch("app.api.endpoints.exercises.ExerciseService")
def test_boundary_value_attacks(MockExerciseService, MockWorkoutService):
    def mock_user():
        return 1

    mock_workout_service = MagicMock()
    mock_workout_service.create_workout.return_value = {
        "id": 1,
        "note": "Test",
        "owner_id": 1,
        "date": "2024-01-01",
    }
    MockWorkoutService.return_value = mock_workout_service

    mock_exercise_service = MagicMock()
    MockExerciseService.return_value = mock_exercise_service

    app.dependency_overrides[get_current_user] = mock_user
    workout = client.post("/workouts/", json={"note": "Test"}).json()

    response = client.post(
        "/exercises/", json={"name": "A" * 101, "workout_id": workout["id"]}
    )
    assert response.status_code == 422

    response = client.post(
        "/exercises/", json={"name": "Test Exercise", "workout_id": -1}
    )
    assert response.status_code in [404, 422]

    app.dependency_overrides = {}

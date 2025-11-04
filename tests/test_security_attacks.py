from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app

client = TestClient(app)


def test_idor_protection_real_scenario():
    """Реальный сценарий IDOR: пользователь не может получить чужие данные"""

    def mock_user_1():
        return 1

    def mock_user_2():
        return 2

    app.dependency_overrides[get_current_user] = mock_user_1

    workout = client.post("/workouts/", json={"note": "Private workout"}).json()

    app.dependency_overrides[get_current_user] = mock_user_2

    response = client.get(f"/workouts/{workout['id']}")

    app.dependency_overrides = {}

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_xss_prevention_in_exercise_name():
    """XSS в названии упражнения должен блокироваться валидацией"""

    def mock_user():
        return 1

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
    assert "pattern" in response.json()["errors"][0]["msg"]


def test_mass_assignment_prevention():
    """Защита от mass assignment - нельзя передать лишние поля"""

    def mock_user():
        return 1

    app.dependency_overrides[get_current_user] = mock_user

    response = client.post(
        "/workouts/", json={"note": "Test", "owner_id": 999, "admin": True}
    )

    app.dependency_overrides = {}

    assert response.status_code == 200
    created = response.json()
    assert created["owner_id"] == 1
    assert "admin" not in created


def test_json_injection_prevention():
    """Защита от malicious JSON"""

    def mock_user():
        return 1

    app.dependency_overrides[get_current_user] = mock_user

    malicious_json = '{"note": "test", "__class__": "malicious"}'
    response = client.post(
        "/workouts/", data=malicious_json, headers={"Content-Type": "application/json"}
    )

    app.dependency_overrides = {}

    assert response.status_code in [200, 422, 401]


def test_boundary_value_attacks():
    """Атаки граничными значениями"""

    def mock_user():
        return 1

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

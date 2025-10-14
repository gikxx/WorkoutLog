import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import ExerciseCreate, SetCreate, UserCreate, WorkoutCreate

client = TestClient(app)


def test_exercise_name_html_sanitization():
    exercise = ExerciseCreate(
        name="<script>alert('xss')</script>Bench Press", workout_id=1
    )
    assert "<script>" not in exercise.name
    assert "&lt;" in exercise.name


def test_exercise_name_too_short():
    with pytest.raises(ValueError):
        ExerciseCreate(name="", workout_id=1)


def test_exercise_name_too_long():
    with pytest.raises(ValueError):
        ExerciseCreate(name="A" * 101, workout_id=1)


def test_exercise_name_valid_boundaries():
    ExerciseCreate(name="A", workout_id=1)
    ExerciseCreate(name="A" * 100, workout_id=1)


def test_set_weight_too_many_decimals():
    with pytest.raises(ValueError):
        SetCreate(reps=10, weight=50.123, exercise_id=1)


def test_set_weight_valid_decimals():
    SetCreate(reps=10, weight=50.12, exercise_id=1)
    SetCreate(reps=10, weight=50.1, exercise_id=1)
    SetCreate(reps=10, weight=50.0, exercise_id=1)


def test_set_weight_upper_boundary():
    with pytest.raises(ValueError):
        SetCreate(reps=10, weight=500.1, exercise_id=1)


def test_set_weight_lower_boundary():
    with pytest.raises(ValueError):
        SetCreate(reps=10, weight=0.0, exercise_id=1)


def test_set_weight_valid_boundaries():
    SetCreate(reps=10, weight=0.1, exercise_id=1)
    SetCreate(reps=10, weight=500.0, exercise_id=1)


def test_set_reps_zero():
    with pytest.raises(ValueError):
        SetCreate(reps=0, weight=50.0, exercise_id=1)


def test_set_reps_above_max():
    with pytest.raises(ValueError):
        SetCreate(reps=101, weight=50.0, exercise_id=1)


def test_set_reps_valid_boundaries():
    SetCreate(reps=1, weight=50.0, exercise_id=1)
    SetCreate(reps=100, weight=50.0, exercise_id=1)


def test_exercise_workout_id_zero():
    with pytest.raises(ValueError):
        ExerciseCreate(name="Bench Press", workout_id=0)


def test_exercise_workout_id_negative():
    with pytest.raises(ValueError):
        ExerciseCreate(name="Bench Press", workout_id=-1)


def test_workout_note_too_long():
    with pytest.raises(ValueError):
        WorkoutCreate(note="A" * 501)


def test_workout_note_valid_length():
    WorkoutCreate(note="A" * 500)
    WorkoutCreate(note=None)
    WorkoutCreate(note="Normal note")


def test_workout_note_sanitization():
    workout = WorkoutCreate(note="Test <script>alert('xss')</script> workout")
    assert "<script>" not in workout.note
    assert "&lt;" in workout.note


def test_user_email_too_short():
    with pytest.raises(ValueError):
        UserCreate(email="a@b", password="password123")


def test_user_email_too_long():
    with pytest.raises(ValueError):
        UserCreate(email="a" * 95 + "@example.com", password="password123")


def test_user_password_too_short():
    with pytest.raises(ValueError):
        UserCreate(email="test@example.com", password="short")


def test_user_password_too_long():
    with pytest.raises(ValueError):
        UserCreate(email="test@example.com", password="a" * 101)


def test_user_valid_boundaries():
    UserCreate(email="aaaaa@b.com", password="12345678")
    UserCreate(email="a" * 90 + "@test.com", password="a" * 100)


def test_api_validation_errors():
    response = client.post("/exercises/", json={"name": "", "workout_id": 1})
    assert response.status_code in [422, 404]

    response = client.post("/sets/", json={"reps": 0, "weight": 50.0, "exercise_id": 1})
    assert response.status_code in [422, 404]

    response = client.post("/users/", json={"email": "a@b", "password": "short"})
    assert response.status_code in [422, 404]

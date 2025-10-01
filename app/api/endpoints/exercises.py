from fastapi import APIRouter

from app.models.schemas import ExerciseCreate, ExerciseResponse

router = APIRouter()

exercises_db = [
    {"id": 1, "name": "Жим штанги лежа", "workout_id": 1},
    {"id": 2, "name": "Тяга верхнего блока", "workout_id": 1},
    {"id": 3, "name": "Бег на дорожке", "workout_id": 2},
    {"id": 4, "name": "Приседания со штангой", "workout_id": 3},
]
exercise_id = 5


@router.post("/", response_model=ExerciseResponse)
def create_exercise(exercise: ExerciseCreate):
    global exercise_id
    exercise_data = {
        "id": exercise_id,
        "name": exercise.name,
        "workout_id": exercise.workout_id,
    }
    exercises_db.append(exercise_data)
    exercise_id += 1
    return exercise_data


@router.get("/", response_model=list[ExerciseResponse])
def get_exercises():
    return exercises_db

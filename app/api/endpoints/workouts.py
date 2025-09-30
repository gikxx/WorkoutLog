from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.models.schemas import WorkoutCreate, WorkoutResponse

router = APIRouter()

workouts_db = [
    {
        "id": 1,
        "date": datetime(2024, 9, 28, 10, 30),
        "note": "Силовая тренировка: грудь и спина",
        "owner_id": 1,
    },
    {
        "id": 2,
        "date": datetime(2024, 9, 25, 18, 0),
        "note": "Кардио: бег 5 км",
        "owner_id": 1,
    },
    {
        "id": 3,
        "date": datetime(2024, 9, 23, 9, 15),
        "note": "Ноги и плечи",
        "owner_id": 1,
    },
]
current_id = 4


@router.post("/", response_model=WorkoutResponse)
def create_workout(workout: WorkoutCreate):
    global current_id
    workout_data = {
        "id": current_id,
        "date": datetime.now(),
        "note": workout.note,
        "owner_id": 1,
    }
    workouts_db.append(workout_data)
    current_id += 1
    return workout_data


@router.get("/", response_model=list[WorkoutResponse])
def get_workouts():
    return workouts_db


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int):
    workout = next((w for w in workouts_db if w["id"] == workout_id), None)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

from fastapi import APIRouter

from app.api.endpoints.exercises import exercises_db
from app.api.endpoints.workouts import workouts_db

router = APIRouter()


@router.get("/")
def get_stats():
    total_workouts = len(workouts_db)
    total_exercises = len(exercises_db)

    last_workout_date = "No workouts yet"
    recent_notes = None

    if workouts_db:
        last_workout = max(workouts_db, key=lambda x: x["date"])
        last_workout_date = last_workout["date"].strftime("%Y-%m-%d")
        recent_notes = last_workout.get("note")

    return {
        "total_workouts": total_workouts,
        "total_exercises": total_exercises,
        "last_workout_date": last_workout_date,
        "most_recent_workout_notes": recent_notes,
    }

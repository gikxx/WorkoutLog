from sqlalchemy.orm import Session

from app.crud.stats import get_exercises_count, get_last_workout, get_workouts_count


class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self):
        total_workouts = get_workouts_count(self.db)
        total_exercises = get_exercises_count(self.db)
        last_workout = get_last_workout(self.db)

        last_workout_date = "No workouts yet"
        recent_notes = None

        if last_workout:
            last_workout_date = last_workout.date.strftime("%Y-%m-%d")
            recent_notes = last_workout.note

        return {
            "total_workouts": total_workouts,
            "total_exercises": total_exercises,
            "last_workout_date": last_workout_date,
            "most_recent_workout_notes": recent_notes,
        }

from sqlalchemy.orm import Session

from app.crud.workouts import create_workout, get_workout_by_id, get_workouts


class WorkoutService:
    def __init__(self, db: Session):
        self.db = db

    def create_workout(self, workout_data):
        return create_workout(self.db, workout_data)

    def get_workouts(self):
        return get_workouts(self.db)

    def get_workout_by_id(self, workout_id: int):
        return get_workout_by_id(self.db, workout_id)

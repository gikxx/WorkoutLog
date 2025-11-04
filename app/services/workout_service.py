from sqlalchemy.orm import Session

from app.crud.workouts import create_workout, get_workout_by_id, get_workouts


class WorkoutService:
    def __init__(self, db: Session):
        self.db = db

    def create_workout(self, workout_data, owner_id: int):
        return create_workout(self.db, workout_data, owner_id)

    def get_workouts(self, owner_id: int):
        return get_workouts(self.db, owner_id)

    def get_workout_by_id(self, workout_id: int, owner_id: int):
        return get_workout_by_id(self.db, workout_id, owner_id)

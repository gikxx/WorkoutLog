from sqlalchemy.orm import Session

from app.crud.exercises import create_exercise, get_exercises, get_exercises_by_workout


class ExerciseService:
    def __init__(self, db: Session):
        self.db = db

    def create_exercise(self, exercise_data, owner_id: int):
        return create_exercise(self.db, exercise_data, owner_id)

    def get_exercises(self, owner_id: int):
        return get_exercises(self.db, owner_id)

    def get_exercises_by_workout(self, workout_id: int, owner_id: int):
        return get_exercises_by_workout(self.db, workout_id, owner_id)

from sqlalchemy.orm import Session

from app.models.database import Exercise
from app.models.schemas import ExerciseCreate


def create_exercise(db: Session, exercise_data: ExerciseCreate):
    db_exercise = Exercise(name=exercise_data.name, workout_id=exercise_data.workout_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def get_exercises(db: Session):
    return db.query(Exercise).all()


def get_exercises_by_workout(db: Session, workout_id: int):
    return db.query(Exercise).filter(Exercise.workout_id == workout_id).all()

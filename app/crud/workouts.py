from sqlalchemy.orm import Session

from app.models.database import Workout
from app.models.schemas import WorkoutCreate


def create_workout(db: Session, workout_data: WorkoutCreate, owner_id: int = 1):
    db_workout = Workout(note=workout_data.note, owner_id=owner_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def get_workouts(db: Session):
    return db.query(Workout).all()


def get_workout_by_id(db: Session, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()


def get_workouts_with_exercises(db: Session):
    return db.query(Workout).all()

from sqlalchemy.orm import Session

from app.models.database import Workout
from app.models.schemas import WorkoutCreate


def create_workout(db: Session, workout_data: WorkoutCreate, owner_id: int):
    db_workout = Workout(note=workout_data.note, owner_id=owner_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def get_workouts(db: Session, owner_id: int):
    return db.query(Workout).filter(Workout.owner_id == owner_id).all()


def get_workout_by_id(db: Session, workout_id: int, owner_id: int):
    return (
        db.query(Workout)
        .filter(Workout.id == workout_id, Workout.owner_id == owner_id)
        .first()
    )


def get_workouts_with_exercises(db: Session, owner_id: int):
    return db.query(Workout).filter(Workout.owner_id == owner_id).all()
